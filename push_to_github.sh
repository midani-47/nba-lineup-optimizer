#!/bin/bash

# Script to push the NBA Lineup Optimizer to GitHub

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Error: git is not installed. Please install git first."
    exit 1
fi

# Initialize git repository if not already initialized
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
fi

# Create .gitignore file
echo "Creating .gitignore file..."
cat > .gitignore << EOL
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg
venv/

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
media

# React
node_modules/
/frontend/build
.DS_Store
.env.local
.env.development.local
.env.test.local
.env.production.local
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# IDE
.idea/
.vscode/
*.swp
*.swo
EOL

# Add all files
echo "Adding files to git..."
git add .

# Commit changes
echo "Committing changes..."
git commit -m "Initial commit of NBA Lineup Optimizer"

# Add remote repository
echo "Adding remote repository..."
git remote add origin https://github.com/midani-47/nba-lineup-optimizer.git

# Push to GitHub
echo "Pushing to GitHub..."
git push -u origin master

echo "Done! The NBA Lineup Optimizer has been pushed to GitHub." 