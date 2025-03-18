const { spawn } = require('child_process');
const path = require('path');
const os = require('os');
const fs = require('fs');

// Console colors for better output
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  dim: '\x1b[2m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m'
};

// Function to log with timestamp and color
function log(message, color = colors.reset) {
  const timestamp = new Date().toLocaleTimeString();
  console.log(`${colors.dim}[${timestamp}]${colors.reset} ${color}${message}${colors.reset}`);
}

// Function to determine the Python executable path
function getPythonPath() {
  // Check multiple possibilities based on platform
  const platform = os.platform();
  
  if (platform === 'win32') {
    const possiblePaths = ['python', 'py', 'python3'];
    for (const pythonCmd of possiblePaths) {
      try {
        const result = spawn.sync(pythonCmd, ['-c', 'print("Python found")'], { shell: true });
        if (result.status === 0) {
          log(`Found Python executable: ${pythonCmd}`, colors.green);
          return pythonCmd;
        }
      } catch (error) {
        // Continue checking other commands
      }
    }
  } else {
    // Linux/macOS
    const possiblePaths = ['python3', 'python'];
    for (const pythonCmd of possiblePaths) {
      try {
        const result = spawn.sync(pythonCmd, ['-c', 'print("Python found")'], { shell: true });
        if (result.status === 0) {
          log(`Found Python executable: ${pythonCmd}`, colors.green);
          return pythonCmd;
        }
      } catch (error) {
        // Continue checking other commands
      }
    }
  }

  log('Could not find Python executable', colors.red);
  return platform === 'win32' ? 'python' : 'python3'; // Default fallback
}

// Function to determine the npm executable path
function getNpmPath() {
  if (os.platform() === 'win32') {
    return 'npm.cmd';
  }
  return 'npm';
}

// Function to run a command and handle its output
function runCommand(command, args, cwd, stdioMode = 'inherit') {
  return new Promise((resolve, reject) => {
    log(`Running command: ${command} ${args.join(' ')}`, colors.cyan);
    
    const process = spawn(command, args, {
      cwd,
      stdio: stdioMode,
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

// Function to check if a directory exists
function checkDirExists(dirPath) {
  try {
    return fs.existsSync(dirPath) && fs.statSync(dirPath).isDirectory();
  } catch (error) {
    return false;
  }
}

// Function to check if we can connect to the database
async function checkDatabase() {
  const backendPath = path.join(__dirname, 'backend');
  
  try {
    log('Running database fix script...', colors.yellow);
    await runCommand(getPythonPath(), ['fix_migrations.py'], backendPath);
    return true;
  } catch (error) {
    log(`Database fix failed: ${error.message}`, colors.red);
    return false;
  }
}

// Main function to start both backend and frontend
async function start() {
  try {
    // Print header
    console.log('\n');
    log('🏀 Starting NBA Lineup Optimizer 🏀', colors.bright + colors.blue);
    log('======================================', colors.dim);
    
    // Check if directories exist
    const backendPath = path.join(__dirname, 'backend');
    const frontendPath = path.join(__dirname, 'frontend');
    
    if (!checkDirExists(backendPath)) {
      throw new Error(`Backend directory not found: ${backendPath}`);
    }
    
    if (!checkDirExists(frontendPath)) {
      throw new Error(`Frontend directory not found: ${frontendPath}`);
    }
    
    // Check and fix database
    log('Checking database...', colors.yellow);
    await checkDatabase();
    
    // Start backend server
    log('Starting backend server...', colors.magenta);
    const backendProcess = spawn(getPythonPath(), ['manage.py', 'runserver'], {
      cwd: backendPath,
      stdio: 'inherit',
      shell: true,
      detached: true
    });
    
    // Give the backend a moment to start
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Start frontend
    log('Starting frontend server...', colors.magenta);
    const frontendProcess = spawn(getNpmPath(), ['start'], {
      cwd: frontendPath,
      stdio: 'inherit',
      shell: true,
      detached: true
    });
    
    log('Both servers are running!', colors.green);
    log('Press Ctrl+C to stop the servers', colors.yellow);
    
    // Handle cleanup
    const cleanup = () => {
      log('Stopping servers...', colors.yellow);
      if (backendProcess) process.kill(-backendProcess.pid);
      if (frontendProcess) process.kill(-frontendProcess.pid);
      process.exit(0);
    };
    
    process.on('SIGINT', cleanup);
    process.on('SIGTERM', cleanup);

  } catch (error) {
    log(`Error starting the application: ${error.message}`, colors.red);
    process.exit(1);
  }
}

// Run the start function
start(); 