#!/usr/bin/env node

/**
 * Generic Counter Tool for Work Command Center
 *
 * Usage:
 *   node counter.js <counter-name> [--set N] [--reset] [--list]
 *
 * Examples:
 *   node counter.js rescued-deadlines              # Increment "rescued-deadlines" by 1
 *   node counter.js rescued-deadlines --set 5      # Set "rescued-deadlines" to 5
 *   node counter.js rescued-deadlines --reset      # Reset "rescued-deadlines" to 0
 *   node counter.js --list                         # List all counters
 *
 * Counters are stored in: User-Files/work-tracking/counters.json
 */

const fs = require('fs');
const path = require('path');

// Path to counters data file
const COUNTERS_FILE = path.join(process.cwd(), 'User-Files', 'work-tracking', 'counters.json');

// Ensure directory exists
function ensureDirectory() {
  const dir = path.dirname(COUNTERS_FILE);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

// Load counters from file
function loadCounters() {
  ensureDirectory();
  if (!fs.existsSync(COUNTERS_FILE)) {
    return {};
  }
  try {
    const data = fs.readFileSync(COUNTERS_FILE, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    console.error('Error reading counters file:', error.message);
    return {};
  }
}

// Save counters to file
function saveCounters(counters) {
  ensureDirectory();
  try {
    fs.writeFileSync(COUNTERS_FILE, JSON.stringify(counters, null, 2), 'utf8');
  } catch (error) {
    console.error('Error saving counters file:', error.message);
    process.exit(1);
  }
}

// Parse command line arguments
function parseArgs() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
    console.log(`
Generic Counter Tool for Work Command Center

Usage:
  node counter.js <counter-name>              Increment counter by 1
  node counter.js <counter-name> --set N      Set counter to N
  node counter.js <counter-name> --reset      Reset counter to 0
  node counter.js --list                      List all counters

Examples:
  node counter.js rescued-deadlines           # Increment by 1
  node counter.js rescued-deadlines --set 5   # Set to 5
  node counter.js rescued-deadlines --reset   # Reset to 0
  node counter.js --list                      # Show all counters
    `);
    process.exit(0);
  }

  const result = {
    list: args.includes('--list'),
    reset: false,
    set: null,
    counterName: null
  };

  if (result.list) {
    return result;
  }

  // Find counter name (first arg that doesn't start with --)
  result.counterName = args.find(arg => !arg.startsWith('--'));

  if (!result.counterName) {
    console.error('Error: Counter name required');
    process.exit(1);
  }

  // Check for --reset
  result.reset = args.includes('--reset');

  // Check for --set N
  const setIndex = args.indexOf('--set');
  if (setIndex !== -1 && args[setIndex + 1]) {
    const value = parseInt(args[setIndex + 1], 10);
    if (isNaN(value)) {
      console.error('Error: --set requires a numeric value');
      process.exit(1);
    }
    result.set = value;
  }

  return result;
}

// List all counters
function listCounters(counters) {
  const entries = Object.entries(counters);

  if (entries.length === 0) {
    console.log('No counters found.');
    return;
  }

  console.log('\n=== WORK COMMAND CENTER COUNTERS ===\n');

  // Find longest counter name for alignment
  const maxLength = Math.max(...entries.map(([name]) => name.length));

  entries
    .sort(([a], [b]) => a.localeCompare(b))
    .forEach(([name, data]) => {
      const padding = ' '.repeat(maxLength - name.length);
      console.log(`${name}:${padding} ${data.value} (last updated: ${data.lastUpdated})`);
    });

  console.log('');
}

// Main function
function main() {
  const { list, reset, set, counterName } = parseArgs();

  const counters = loadCounters();

  // List mode
  if (list) {
    listCounters(counters);
    return;
  }

  // Initialize counter if it doesn't exist
  if (!counters[counterName]) {
    counters[counterName] = {
      value: 0,
      created: new Date().toISOString(),
      lastUpdated: new Date().toISOString()
    };
  }

  // Handle operations
  if (reset) {
    counters[counterName].value = 0;
    counters[counterName].lastUpdated = new Date().toISOString();
    saveCounters(counters);
    console.log(`\n✓ Counter "${counterName}" reset to 0\n`);
    return;
  }

  if (set !== null) {
    counters[counterName].value = set;
    counters[counterName].lastUpdated = new Date().toISOString();
    saveCounters(counters);
    console.log(`\n✓ Counter "${counterName}" set to ${set}\n`);
    return;
  }

  // Default: increment by 1
  counters[counterName].value += 1;
  counters[counterName].lastUpdated = new Date().toISOString();
  saveCounters(counters);

  console.log(`\n✓ Counter "${counterName}" incremented to ${counters[counterName].value}\n`);
}

// Run
main();
