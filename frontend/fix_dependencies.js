/**
 * This script helps fix common dependency issues in the frontend.
 * Run with: node fix_dependencies.js
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('🔧 NBA Lineup Optimizer - Frontend Dependency Fixer 🔧');
console.log('====================================================');

// Check if package.json exists
const packageJsonPath = path.join(__dirname, 'package.json');
if (!fs.existsSync(packageJsonPath)) {
  console.error('❌ package.json not found. Make sure you are in the frontend directory.');
  process.exit(1);
}

// Read package.json
let packageJson;
try {
  packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
  console.log('✅ Found package.json');
} catch (error) {
  console.error('❌ Error reading package.json:', error.message);
  process.exit(1);
}

// Ensure ajv dependency is present
if (!packageJson.dependencies.ajv) {
  console.log('⚠️ Adding missing ajv dependency...');
  packageJson.dependencies.ajv = '^8.12.0';
  fs.writeFileSync(packageJsonPath, JSON.stringify(packageJson, null, 2));
  console.log('✅ Added ajv dependency to package.json');
}

// Clean up node_modules and reinstall
try {
  console.log('🧹 Cleaning up node_modules...');
  
  // Check if node_modules exists
  const nodeModulesPath = path.join(__dirname, 'node_modules');
  if (fs.existsSync(nodeModulesPath)) {
    if (process.platform === 'win32') {
      // Windows - use rimraf for reliability
      console.log('📦 Installing rimraf to safely remove node_modules...');
      execSync('npm install -g rimraf', { stdio: 'inherit' });
      execSync('rimraf node_modules', { stdio: 'inherit' });
    } else {
      // macOS/Linux
      execSync('rm -rf node_modules', { stdio: 'inherit' });
    }
    console.log('✅ Removed node_modules directory');
  }
  
  // Remove package-lock.json
  const packageLockPath = path.join(__dirname, 'package-lock.json');
  if (fs.existsSync(packageLockPath)) {
    fs.unlinkSync(packageLockPath);
    console.log('✅ Removed package-lock.json');
  }
  
  // Clear npm cache
  console.log('🧹 Clearing npm cache...');
  execSync('npm cache clean --force', { stdio: 'inherit' });
  console.log('✅ Cleared npm cache');
  
  // Reinstall dependencies
  console.log('📦 Reinstalling dependencies...');
  execSync('npm install --legacy-peer-deps', { stdio: 'inherit' });
  console.log('✅ Dependencies reinstalled successfully');
  
  console.log('\n🎉 All done! You can now run the frontend with: npm start');
} catch (error) {
  console.error('❌ Error during dependency fix:', error.message);
  console.log('\n⚠️ Please try manually running these commands:');
  console.log('1. Delete the node_modules folder');
  console.log('2. Delete package-lock.json');
  console.log('3. Run: npm cache clean --force');
  console.log('4. Run: npm install --legacy-peer-deps');
  process.exit(1);
} 