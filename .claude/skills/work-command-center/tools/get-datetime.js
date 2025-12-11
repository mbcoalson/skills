#!/usr/bin/env node

/**
 * Date/Time Utility for Work Command Center
 * Provides current date/time context for deadline tracking and priority management
 */

function getDateTime() {
  const now = new Date();

  // Format options
  const dateOptions = {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  };

  const timeOptions = {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: true
  };

  // Get various formats
  const fullDate = now.toLocaleDateString('en-US', dateOptions);
  const time = now.toLocaleTimeString('en-US', timeOptions);
  const isoDate = now.toISOString().split('T')[0]; // YYYY-MM-DD
  const isoDateTime = now.toISOString();

  // Calculate week information
  const startOfYear = new Date(now.getFullYear(), 0, 1);
  const days = Math.floor((now - startOfYear) / (24 * 60 * 60 * 1000));
  const weekNumber = Math.ceil((days + startOfYear.getDay() + 1) / 7);

  // Day of week and year
  const dayOfWeek = now.getDay(); // 0 = Sunday
  const dayOfYear = Math.floor((now - startOfYear) / (24 * 60 * 60 * 1000)) + 1;

  // Output structured data
  const result = {
    current: {
      fullDate: fullDate,
      time: time,
      isoDate: isoDate,
      isoDateTime: isoDateTime,
      dayOfWeek: now.toLocaleDateString('en-US', { weekday: 'long' }),
      weekNumber: weekNumber,
      dayOfYear: dayOfYear
    },
    formatted: {
      display: `${fullDate} at ${time}`,
      short: isoDate,
      filename: isoDate.replace(/-/g, ''),
      logFormat: `${isoDate} ${time}`
    },
    timestamps: {
      unix: Math.floor(now.getTime() / 1000),
      milliseconds: now.getTime()
    }
  };

  // Return formatted output
  console.log('=== CURRENT DATE & TIME ===');
  console.log(`Date: ${result.current.fullDate}`);
  console.log(`Time: ${result.current.time}`);
  console.log(`ISO Format: ${result.current.isoDate}`);
  console.log(`Day of Week: ${result.current.dayOfWeek}`);
  console.log(`Week Number: ${result.current.weekNumber}`);
  console.log('');
  console.log('Quick Reference:');
  console.log(`  Display: ${result.formatted.display}`);
  console.log(`  Filename: ${result.formatted.filename}`);
  console.log(`  Log Format: ${result.formatted.logFormat}`);
  console.log('');

  // Return JSON if --json flag
  if (process.argv.includes('--json')) {
    console.log('JSON Output:');
    console.log(JSON.stringify(result, null, 2));
  }
}

// Run if called directly
if (require.main === module) {
  getDateTime();
}

module.exports = { getDateTime };
