#!/usr/bin/env node

/**
 * Frontend Dependency Fixer for NBA Lineup Optimizer
 * 
 * This script:
 * 1. Cleans up the node_modules directory
 * 2. Removes package-lock.json
 * 3. Clears npm cache
 * 4. Reinstalls dependencies with appropriate flags
 */

const { spawn, execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('🔧 NBA Lineup Optimizer - Frontend Dependency Fixer 🔧');
console.log('====================================================');

// Check if package.json exists in the current directory
if (!fs.existsSync('package.json')) {
  console.error('❌ Error: package.json not found in the current directory.');
  console.error('Please run this script from the frontend directory.');
  process.exit(1);
}

console.log('✅ Found package.json');

// Clean up node_modules
console.log('🧹 Cleaning up node_modules...');
try {
  if (fs.existsSync('node_modules')) {
    // On macOS, using rm -rf is more reliable than rimraf
    execSync('rm -rf node_modules');
  }
} catch (error) {
  console.error('❌ Error removing node_modules:', error.message);
  console.log('Continuing anyway...');
}

// Remove package-lock.json
try {
  if (fs.existsSync('package-lock.json')) {
    fs.unlinkSync('package-lock.json');
    console.log('✅ Removed package-lock.json');
  }
} catch (error) {
  console.error('❌ Error removing package-lock.json:', error.message);
  console.log('Continuing anyway...');
}

// Clear npm cache
console.log('🧹 Clearing npm cache...');
try {
  execSync('npm cache clean --force');
  console.log('✅ Cleared npm cache');
} catch (error) {
  console.error('❌ Error clearing npm cache:', error.message);
  console.log('Continuing anyway...');
}

// Install dependencies
console.log('📦 Reinstalling dependencies...');
const install = spawn('npm', ['install', '--legacy-peer-deps'], {
  stdio: 'inherit',
  shell: true
});

install.on('close', (code) => {
  if (code === 0) {
    console.log('✅ Dependencies reinstalled successfully!');
    
    // Check for React and other crucial dependencies
    if (fs.existsSync(path.join('node_modules', 'react')) && 
        fs.existsSync(path.join('node_modules', 'react-dom'))) {
      console.log('✅ Verified core dependencies are installed');
      console.log('====================================================');
      console.log('✅ Frontend dependencies fixed successfully!');
      console.log('You can now start the application with:');
      console.log('  npm start');
    } else {
      console.error('❌ Some core dependencies are missing!');
      console.log('====================================================');
      console.log('Please try running: npm install --force');
    }
  } else {
    console.error(`❌ Dependency installation failed with code ${code}`);
    console.log('====================================================');
    console.log('Try the following manual steps:');
    console.log('1. Delete the node_modules directory: rm -rf node_modules');
    console.log('2. Delete package-lock.json: rm package-lock.json');
    console.log('3. Clear npm cache: npm cache clean --force');
    console.log('4. Install with force: npm install --force');
  }
}); 