#!/usr/bin/env node

/**
 * Time Log Entry Tool
 * Appends a new time entry to time-log.jsonl
 * Usage: node log-time.js --duration 60 --task "Task description" --project "Project Name" [--notes "Optional notes"]
 */

const fs = require('fs');
const path = require('path');

// Parse command line arguments
const args = process.argv.slice(2);
const getArg = (flag) => {
  const index = args.indexOf(flag);
  return index >= 0 ? args[index + 1] : null;
};

const duration = parseInt(getArg('--duration')) || 0;
const task = getArg('--task');
const project = getArg('--project') || 'Unspecified';
const notes = getArg('--notes');

// Validate required arguments
if (!duration || !task) {
  console.error('Error: --duration and --task are required');
  console.error('Usage: node log-time.js --duration 60 --task "Task description" --project "Project Name" [--notes "Notes"]');
  process.exit(1);
}

// Create time entry
const now = new Date();
const entry = {
  date: now.toISOString().split('T')[0],
  time: now.toTimeString().split(' ')[0].slice(0, 5),
  session_start: now.toISOString(),
  duration_minutes: duration,
  task: task,
  project: project
};

if (notes) {
  entry.notes = notes;
}

// Append to log file
const logPath = path.join(__dirname, '..', 'time-log.jsonl');
const logEntry = JSON.stringify(entry) + '\n';

fs.appendFileSync(logPath, logEntry);

console.log('✓ Time logged successfully');
console.log(`  Project: ${project}`);
console.log(`  Duration: ${duration} minutes (${(duration / 60).toFixed(1)} hours)`);
console.log(`  Task: ${task}`);
if (notes) {
  console.log(`  Notes: ${notes}`);
}
