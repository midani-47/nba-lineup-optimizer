#!/usr/bin/env node

/**
 * macOS-specific startup script for NBA Lineup Optimizer
 * 
 * This script:
 * 1. Detects common macOS issues and provides fixes
 * 2. Ensures Python and Node.js are properly configured
 * 3. Fixes database issues
 * 4. Starts both backend and frontend servers
 */

const { spawn, execSync } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');

// Colors for terminal output
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

// Emoji indicators for better visual feedback
const emoji = {
  success: '✅',
  warning: '⚠️',
  error: '❌',
  info: 'ℹ️',
  working: '🔄',
  database: '🗃️',
  server: '🚀',
  frontend: '🖥️',
  backend: '⚙️'
};

// Logger with timestamps and colors
function log(message, color = colors.reset, icon = '') {
  const timestamp = new Date().toLocaleTimeString();
  console.log(`${colors.dim}[${timestamp}]${colors.reset} ${icon ? icon + ' ' : ''}${color}${message}${colors.reset}`);
}

// Header banner
function showHeader() {
  console.log('\n');
  console.log(`${colors.bright}${colors.blue}╔══════════════════════════════════════════════════╗${colors.reset}`);
  console.log(`${colors.bright}${colors.blue}║             NBA LINEUP OPTIMIZER                 ║${colors.reset}`);
  console.log(`${colors.bright}${colors.blue}║           macOS Initialization System            ║${colors.reset}`);
  console.log(`${colors.bright}${colors.blue}╚══════════════════════════════════════════════════╝${colors.reset}`);
  console.log('\n');
}

// Check for Python installation
async function checkPython() {
  log('Checking Python installation...', colors.cyan, emoji.info);
  
  try {
    // Try python3 first (preferred on macOS)
    const pythonVersion = execSync('python3 --version').toString().trim();
    log(`Found ${pythonVersion}`, colors.green, emoji.success);
    return 'python3';
  } catch (error) {
    try {
      // Fall back to python if python3 is not available
      const pythonVersion = execSync('python --version').toString().trim();
      log(`Found ${pythonVersion}`, colors.green, emoji.success);
      return 'python';
    } catch (error) {
      log('Python not found. Please install Python 3.8 or higher.', colors.red, emoji.error);
      log('You can install Python from https://www.python.org/downloads/', colors.yellow);
      throw new Error('Python not found');
    }
  }
}

// Check for node and npm
function checkNode() {
  log('Checking Node.js installation...', colors.cyan, emoji.info);
  
  try {
    const nodeVersion = execSync('node --version').toString().trim();
    const npmVersion = execSync('npm --version').toString().trim();
    
    log(`Found Node.js ${nodeVersion} and npm ${npmVersion}`, colors.green, emoji.success);
    return true;
  } catch (error) {
    log('Node.js or npm not found. Please install Node.js 14 or higher.', colors.red, emoji.error);
    log('You can install Node.js from https://nodejs.org/', colors.yellow);
    throw new Error('Node.js not found');
  }
}

// Run a shell command with promise
function runCommand(command, args, cwd, silent = false) {
  return new Promise((resolve, reject) => {
    if (!silent) {
      log(`Running: ${command} ${args.join(' ')}`, colors.cyan, emoji.working);
    }
    
    const process = spawn(command, args, {
      cwd,
      stdio: silent ? 'ignore' : 'inherit',
      shell: true
    });
    
    let stdout = '';
    let stderr = '';
    
    if (silent) {
      if (process.stdout) {
        process.stdout.on('data', (data) => {
          stdout += data.toString();
        });
      }
      
      if (process.stderr) {
        process.stderr.on('data', (data) => {
          stderr += data.toString();
        });
      }
    }
    
    process.on('close', (code) => {
      if (code === 0) {
        resolve({ stdout, stderr });
      } else {
        reject(new Error(`Command failed with code ${code}`));
      }
    });
    
    process.on('error', (err) => {
      reject(err);
    });
  });
}

// Fix database issues
async function fixDatabase(pythonCmd, backendPath) {
  log('Running database fix script...', colors.magenta, emoji.database);
  
  try {
    // Run the comprehensive fix_migrations.py script
    await runCommand(pythonCmd, ['fix_migrations.py'], backendPath);
    
    // Then run migrate to ensure schema is up to date
    await runCommand(pythonCmd, ['manage.py', 'migrate'], backendPath);
    
    // Run fix_data.py to populate with sample data if needed
    await runCommand(pythonCmd, ['fix_data.py'], backendPath);
    
    log('Database setup complete', colors.green, emoji.success);
    return true;
  } catch (error) {
    log(`Database fix failed: ${error.message}`, colors.red, emoji.error);
    log('Attempting to continue anyway...', colors.yellow, emoji.warning);
    return false;
  }
}

// Start backend server
function startBackend(pythonCmd, backendPath) {
  log('Starting backend server...', colors.blue, emoji.backend);
  
  // Redirect output to log file to avoid cluttering the console
  const logFile = path.join(backendPath, 'backend_log.txt');
  
  // Create or truncate log file
  fs.writeFileSync(logFile, `Backend server started at ${new Date().toString()}\n\n`);
  
  const serverProcess = spawn(pythonCmd, ['manage.py', 'runserver'], {
    cwd: backendPath,
    detached: true,
    stdio: ['ignore', 
      fs.openSync(logFile, 'a'),
      fs.openSync(logFile, 'a')
    ]
  });
  
  // Detach the process
  serverProcess.unref();
  
  log(`Backend server started with PID ${serverProcess.pid}`, colors.green, emoji.success);
  log(`Logs are being written to: ${logFile}`, colors.dim);
  
  return serverProcess;
}

// Start frontend server
function startFrontend(frontendPath) {
  log('Starting frontend development server...', colors.blue, emoji.frontend);
  
  // Redirect output to log file to avoid cluttering the console
  const logFile = path.join(frontendPath, 'frontend_log.txt');
  
  // Create or truncate log file
  fs.writeFileSync(logFile, `Frontend server started at ${new Date().toString()}\n\n`);
  
  const serverProcess = spawn('npm', ['start'], {
    cwd: frontendPath,
    detached: true,
    stdio: ['ignore', 
      fs.openSync(logFile, 'a'),
      fs.openSync(logFile, 'a')
    ]
  });
  
  // Detach the process
  serverProcess.unref();
  
  log(`Frontend server started with PID ${serverProcess.pid}`, colors.green, emoji.success);
  log(`Logs are being written to: ${logFile}`, colors.dim);
  
  return serverProcess;
}

// Check if the frontend build is needed
async function checkFrontendDependencies(frontendPath) {
  log('Checking frontend dependencies...', colors.cyan, emoji.info);
  
  const nodeModulesPath = path.join(frontendPath, 'node_modules');
  
  if (!fs.existsSync(nodeModulesPath) || 
      !fs.existsSync(path.join(nodeModulesPath, 'react')) || 
      !fs.existsSync(path.join(nodeModulesPath, 'react-dom'))) {
    log('Frontend dependencies not installed or incomplete', colors.yellow, emoji.warning);
    log('Installing frontend dependencies (this may take a few minutes)...', colors.magenta);
    
    try {
      await runCommand('npm', ['install', '--legacy-peer-deps'], frontendPath);
      log('Frontend dependencies installed successfully', colors.green, emoji.success);
      return true;
    } catch (error) {
      log(`Frontend dependency installation failed: ${error.message}`, colors.red, emoji.error);
      log('Attempting to continue anyway...', colors.yellow, emoji.warning);
      return false;
    }
  } else {
    log('Frontend dependencies already installed', colors.green, emoji.success);
    return true;
  }
}

// Main function to run the startup sequence
async function main() {
  showHeader();
  
  try {
    // Set up paths
    const rootPath = process.cwd();
    const backendPath = path.join(rootPath, 'backend');
    const frontendPath = path.join(rootPath, 'frontend');
    
    // Verify directory structure
    if (!fs.existsSync(backendPath) || !fs.existsSync(frontendPath)) {
      log('Invalid project structure. Make sure you run this script from the project root.', colors.red, emoji.error);
      process.exit(1);
    }
    
    // Check environment dependencies
    const pythonCmd = await checkPython();
    checkNode();
    
    // Fix database issues
    await fixDatabase(pythonCmd, backendPath);
    
    // Check and install frontend dependencies if needed
    await checkFrontendDependencies(frontendPath);
    
    // Start backend server
    const backendProcess = startBackend(pythonCmd, backendPath);
    
    // Wait a moment to allow backend to initialize
    log('Waiting for backend server to initialize...', colors.dim);
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    // Start frontend server
    const frontendProcess = startFrontend(frontendPath);
    
    // Display success message with URLs
    log('\n', colors.reset);
    log('🎉 NBA Lineup Optimizer is now running!', colors.bright + colors.green);
    log('Backend API: http://localhost:8000/api/', colors.cyan);
    log('Frontend UI: http://localhost:3000/', colors.cyan);
    log('\n', colors.reset);
    log('Press Ctrl+C to shut down both servers', colors.yellow);
    
    // Handle graceful shutdown
    const shutdown = () => {
      log('\nShutting down servers...', colors.yellow, emoji.info);
      
      try {
        // On macOS, negative PID kills the process group
        if (backendProcess && backendProcess.pid) {
          process.kill(-backendProcess.pid);
        }
        
        if (frontendProcess && frontendProcess.pid) {
          process.kill(-frontendProcess.pid);
        }
      } catch (error) {
        // Ignore errors during shutdown
      }
      
      log('Servers shut down successfully', colors.green, emoji.success);
      process.exit(0);
    };
    
    // Register signal handlers
    process.on('SIGINT', shutdown);
    process.on('SIGTERM', shutdown);
    
  } catch (error) {
    log(`Initialization failed: ${error.message}`, colors.red, emoji.error);
    process.exit(1);
  }
}

// Run the main function
main(); 