const { spawn } = require('child_process');
const path = require('path');
const os = require('os');

// Function to determine the Python executable path
function getPythonPath() {
  if (os.platform() === 'win32') {
    return 'python';
  }
  return 'python3';
}

// Function to determine the npm executable path
function getNpmPath() {
  if (os.platform() === 'win32') {
    return 'npm.cmd';
  }
  return 'npm';
}

// Function to run a command and handle its output
function runCommand(command, args, cwd) {
  return new Promise((resolve, reject) => {
    const process = spawn(command, args, {
      cwd,
      stdio: 'inherit',
      shell: true
    });

    process.on('close', (code) => {
      if (code === 0) {
        resolve();
      } else {
        reject(new Error(`Command failed with code ${code}`));
      }
    });

    process.on('error', (err) => {
      reject(err);
    });
  });
}

// Main function to start both backend and frontend
async function start() {
  try {
    console.log('Starting NBA Lineup Optimizer...');

    // Start backend
    console.log('Starting backend server...');
    const backendPath = path.join(__dirname, 'backend');
    await runCommand(getPythonPath(), ['manage.py', 'runserver'], backendPath);

    // Start frontend
    console.log('Starting frontend server...');
    const frontendPath = path.join(__dirname, 'frontend');
    await runCommand(getNpmPath(), ['start'], frontendPath);

  } catch (error) {
    console.error('Error starting the application:', error);
    process.exit(1);
  }
}

// Run the start function
start(); 