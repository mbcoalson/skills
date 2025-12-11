#!/usr/bin/env node

/**
 * Weekly Timesheet Generator
 * Reads time-log.jsonl and generates weekly timesheet summaries
 * Usage: node weekly-timesheet.js [--week YYYY-MM-DD] [--json]
 */

const fs = require('fs');
const path = require('path');

// Get command line arguments
const args = process.argv.slice(2);
const jsonOutput = args.includes('--json');
const weekIndex = args.indexOf('--week');
const targetWeekStart = weekIndex >= 0 ? new Date(args[weekIndex + 1]) : null;

// Read time log
const logPath = path.join(__dirname, '..', 'time-log.jsonl');
let entries = [];

if (fs.existsSync(logPath)) {
  const content = fs.readFileSync(logPath, 'utf8');
  entries = content
    .trim()
    .split('\n')
    .filter(line => line.trim())
    .map(line => JSON.parse(line));
}

// Helper function to get week start (Monday)
function getWeekStart(date) {
  const d = new Date(date);
  const day = d.getDay();
  const diff = d.getDate() - day + (day === 0 ? -6 : 1); // Adjust when day is Sunday
  return new Date(d.setDate(diff));
}

// Helper function to format date as YYYY-MM-DD
function formatDate(date) {
  return date.toISOString().split('T')[0];
}

// Group entries by week
const weeklyData = {};
entries.forEach(entry => {
  const entryDate = new Date(entry.date);
  const weekStart = getWeekStart(entryDate);
  const weekKey = formatDate(weekStart);

  if (!weeklyData[weekKey]) {
    weeklyData[weekKey] = {
      weekStart: weekKey,
      entries: [],
      projectHours: {},
      totalMinutes: 0
    };
  }

  weeklyData[weekKey].entries.push(entry);
  weeklyData[weekKey].totalMinutes += entry.duration_minutes;

  const project = entry.project || 'Unspecified';
  if (!weeklyData[weekKey].projectHours[project]) {
    weeklyData[weekKey].projectHours[project] = 0;
  }
  weeklyData[weekKey].projectHours[project] += entry.duration_minutes;
});

// Get current week or specified week
const today = new Date();
const currentWeekStart = targetWeekStart || getWeekStart(today);
const currentWeekKey = formatDate(currentWeekStart);

if (jsonOutput) {
  // JSON output
  if (weeklyData[currentWeekKey]) {
    console.log(JSON.stringify(weeklyData[currentWeekKey], null, 2));
  } else {
    console.log(JSON.stringify({ weekStart: currentWeekKey, entries: [], projectHours: {}, totalMinutes: 0 }, null, 2));
  }
} else {
  // Human-readable output
  console.log('=== WEEKLY TIMESHEET ===');
  console.log(`Week of: ${currentWeekKey}\n`);

  if (weeklyData[currentWeekKey]) {
    const data = weeklyData[currentWeekKey];

    console.log('Project Hours:');
    Object.entries(data.projectHours)
      .sort((a, b) => b[1] - a[1])
      .forEach(([project, minutes]) => {
        const hours = (minutes / 60).toFixed(1);
        console.log(`  ${project}: ${hours} hrs`);
      });

    console.log(`\nTotal Time: ${(data.totalMinutes / 60).toFixed(1)} hours`);
    console.log(`\nSession Details:`);

    data.entries.forEach(entry => {
      const duration = (entry.duration_minutes / 60).toFixed(1);
      console.log(`  ${entry.date} - ${duration}h - ${entry.project}: ${entry.task}`);
      if (entry.notes) {
        console.log(`    Note: ${entry.notes}`);
      }
    });
  } else {
    console.log('No entries found for this week.');
  }

  console.log('\n=== ALL WEEKS ===');
  Object.keys(weeklyData)
    .sort()
    .reverse()
    .slice(0, 4)
    .forEach(weekKey => {
      const totalHours = (weeklyData[weekKey].totalMinutes / 60).toFixed(1);
      const entryCount = weeklyData[weekKey].entries.length;
      console.log(`${weekKey}: ${totalHours} hours (${entryCount} sessions)`);
    });
}
