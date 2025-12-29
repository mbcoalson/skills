#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const TRACKING_DIR = path.join(process.cwd(), 'User-Files', 'work-tracking');
const ACTIVE_SESSION_FILE = path.join(TRACKING_DIR, 'active-session.json');
const TIME_LOG_FILE = path.join(TRACKING_DIR, 'time-log.jsonl');

// Ensure tracking directory exists
function ensureTrackingDir() {
  if (!fs.existsSync(TRACKING_DIR)) {
    fs.mkdirSync(TRACKING_DIR, { recursive: true });
  }
}

// Format date as ISO string
function formatDateTime(date = new Date()) {
  return date.toISOString();
}

// Parse command line args
function parseArgs() {
  const args = process.argv.slice(2);
  const command = args[0];
  const options = {};

  for (let i = 1; i < args.length; i += 2) {
    const key = args[i].replace(/^--/, '');
    const value = args[i + 1];
    options[key] = value;
  }

  return { command, options };
}

// Generate session ID
function generateSessionId() {
  const now = new Date();
  const date = now.toISOString().slice(0, 10).replace(/-/g, '');
  const time = now.toTimeString().slice(0, 5).replace(/:/g, '');
  return `${date}-${time}`;
}

// Calculate duration in minutes
function calculateDuration(startTime, endTime = new Date()) {
  const start = new Date(startTime);
  const end = new Date(endTime);
  return Math.round((end - start) / 1000 / 60);
}

// Format duration for display
function formatDuration(minutes) {
  if (minutes < 60) {
    return `${minutes}m`;
  }
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  return mins > 0 ? `${hours}h ${mins}m` : `${hours}h`;
}

// Start new session
function startSession(project, projectNumber = '', task = '') {
  ensureTrackingDir();

  if (fs.existsSync(ACTIVE_SESSION_FILE)) {
    const existing = JSON.parse(fs.readFileSync(ACTIVE_SESSION_FILE, 'utf8'));
    if (existing.status === 'active') {
      console.error('ERROR: Active session already exists');
      console.error('Run "status" to view or "finalize" to close it first');
      process.exit(1);
    }
  }

  const session = {
    session_id: generateSessionId(),
    start_time: formatDateTime(),
    project: project,
    project_number: projectNumber,
    initial_task: task,
    activities: task ? [task] : [],
    checkpoints: [],
    status: 'active'
  };

  fs.writeFileSync(ACTIVE_SESSION_FILE, JSON.stringify(session, null, 2));

  console.log('=== SESSION STARTED ===');
  console.log(`Session ID: ${session.session_id}`);
  console.log(`Project: ${session.project}`);
  if (projectNumber) console.log(`Project Number: ${projectNumber}`);
  if (task) console.log(`Task: ${task}`);
  console.log(`Started: ${new Date(session.start_time).toLocaleString()}`);
}

// Checkpoint session (update activities)
function checkpointSession(activity) {
  if (!fs.existsSync(ACTIVE_SESSION_FILE)) {
    console.error('ERROR: No active session found');
    process.exit(1);
  }

  const session = JSON.parse(fs.readFileSync(ACTIVE_SESSION_FILE, 'utf8'));

  if (activity && !session.activities.includes(activity)) {
    session.activities.push(activity);
  }

  session.checkpoints.push({
    timestamp: formatDateTime(),
    duration_so_far: calculateDuration(session.start_time)
  });

  fs.writeFileSync(ACTIVE_SESSION_FILE, JSON.stringify(session, null, 2));

  const duration = calculateDuration(session.start_time);
  console.log('=== SESSION CHECKPOINT ===');
  console.log(`Duration so far: ${formatDuration(duration)}`);
  console.log(`Project: ${session.project}`);
  if (activity) console.log(`Added activity: ${activity}`);
  console.log(`Activities: ${session.activities.length} tracked`);
}

// Show session status
function showStatus() {
  if (!fs.existsSync(ACTIVE_SESSION_FILE)) {
    console.log('No active session');
    return;
  }

  const session = JSON.parse(fs.readFileSync(ACTIVE_SESSION_FILE, 'utf8'));
  const duration = calculateDuration(session.start_time);
  const startDate = new Date(session.start_time);

  console.log('=== ACTIVE SESSION ===');
  console.log(`Session ID: ${session.session_id}`);
  console.log(`Project: ${session.project}`);
  if (session.project_number) console.log(`Project Number: ${session.project_number}`);
  console.log(`Started: ${startDate.toLocaleString()}`);
  console.log(`Duration: ${formatDuration(duration)}`);
  console.log(`Status: ${session.status}`);

  if (session.activities.length > 0) {
    console.log('\nActivities:');
    session.activities.forEach((activity, i) => {
      console.log(`  ${i + 1}. ${activity}`);
    });
  }

  if (session.checkpoints.length > 0) {
    console.log(`\nCheckpoints: ${session.checkpoints.length}`);
  }
}

// Resume session info (for new chat)
function resumeSession() {
  if (!fs.existsSync(ACTIVE_SESSION_FILE)) {
    console.log('NO_ACTIVE_SESSION');
    return;
  }

  const session = JSON.parse(fs.readFileSync(ACTIVE_SESSION_FILE, 'utf8'));
  const duration = calculateDuration(session.start_time);
  const startDate = new Date(session.start_time);

  // Output in parseable format for skill to use
  console.log(JSON.stringify({
    exists: true,
    session_id: session.session_id,
    project: session.project,
    project_number: session.project_number || null,
    start_time: startDate.toLocaleString(),
    duration_minutes: duration,
    duration_formatted: formatDuration(duration),
    activities_count: session.activities.length,
    activities: session.activities
  }));
}

// Finalize session and log time
function finalizeSession(notes = '') {
  if (!fs.existsSync(ACTIVE_SESSION_FILE)) {
    console.error('ERROR: No active session found');
    process.exit(1);
  }

  ensureTrackingDir();

  const session = JSON.parse(fs.readFileSync(ACTIVE_SESSION_FILE, 'utf8'));
  const endTime = formatDateTime();
  const duration = calculateDuration(session.start_time, endTime);

  // Create time log entry
  const logEntry = {
    date: new Date(session.start_time).toISOString().slice(0, 10),
    session_id: session.session_id,
    project: session.project,
    project_number: session.project_number || null,
    start_time: session.start_time,
    end_time: endTime,
    duration_minutes: duration,
    activities: session.activities,
    notes: notes || session.initial_task || 'Work session'
  };

  // Append to time log (JSONL format)
  const logLine = JSON.stringify(logEntry) + '\n';
  fs.appendFileSync(TIME_LOG_FILE, logLine);

  // Remove active session file
  fs.unlinkSync(ACTIVE_SESSION_FILE);

  console.log('=== SESSION FINALIZED ===');
  console.log(`Project: ${session.project}`);
  if (session.project_number) console.log(`Project Number: ${session.project_number}`);
  console.log(`Duration: ${formatDuration(duration)}`);
  console.log(`Activities: ${session.activities.length}`);
  console.log(`Logged to: ${TIME_LOG_FILE}`);
}

// Main
function main() {
  const { command, options } = parseArgs();

  switch (command) {
    case 'start':
      if (!options.project) {
        console.error('ERROR: --project required');
        console.error('Usage: session-state.js start --project "Project Name" [--project-number "PN-123"] [--task "Initial task"]');
        process.exit(1);
      }
      startSession(options.project, options['project-number'], options.task);
      break;

    case 'checkpoint':
      checkpointSession(options.activity);
      break;

    case 'status':
      showStatus();
      break;

    case 'resume':
      resumeSession();
      break;

    case 'finalize':
      finalizeSession(options.notes);
      break;

    default:
      console.log('Usage: session-state.js <command> [options]');
      console.log('');
      console.log('Commands:');
      console.log('  start      Start new session (--project required, --project-number optional, --task optional)');
      console.log('  checkpoint Update session with activity (--activity optional)');
      console.log('  status     Show current session status');
      console.log('  resume     Get session info for resuming (JSON output)');
      console.log('  finalize   End session and log time (--notes optional)');
      process.exit(1);
  }
}

main();
