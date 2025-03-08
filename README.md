# 🏀 NBA Lineup Optimizer

## Project Description
The NBA Lineup Optimizer is a full-stack web application designed to help users build, compare, and optimize NBA lineups. It leverages real-time player data to provide insights and analytics for lineup management.

## Features
- **Homepage**: A beautiful introduction to the app with quick access to all features.
- **Dashboard**: View top performers and quick actions to build or optimize lineups.
- **Players Page**: Browse and filter NBA players by name, position, and team.
- **Lineup Builder**: Create custom lineups with search and add functionality.
- **Lineup Comparison**: Compare two lineups side by side with statistical and radar charts.
- **Lineup Optimizer**: Optimize lineups based on criteria like offense, defense, or balanced performance.

## Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher (recommended: Node.js 16.x LTS)
- npm 8 or higher

## Important Version Notes
- Django 4.2.10 and Django REST Framework 3.14.0 are required for compatibility
- React 18.2.0 is used for the frontend
- Using the exact versions in requirements.txt is strongly recommended

## Installation and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/midani-47/nba-lineup-optimizer.git
cd nba-lineup-optimizer
```

### 2. Quick Start

#### Windows
```bash
# Simply run the start script
start.bat
```

#### macOS/Linux
```bash
# Make the script executable
chmod +x start.sh

# Run the start script
./start.sh
```

The start scripts will:
- Create a virtual environment if it doesn't exist
- Install all required dependencies
- Check and fix database issues
- Apply migrations
- Start both backend and frontend servers

### 3. Manual Setup (if the quick start doesn't work)

#### Backend Setup (Windows)
```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Navigate to backend directory
cd backend

# Apply database migrations
python manage.py migrate

# Load initial data and fix player stats
python manage.py load_nba_data
python fix_data.py

# Start the backend server
python manage.py runserver 8001
```

#### macOS/Linux
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Navigate to backend directory
cd backend

# Apply database migrations
python3 manage.py migrate

# Load initial data and fix player stats
python3 manage.py load_nba_data
python3 fix_data.py

# Start the backend server
python3 manage.py runserver 8001
```

### 4. Frontend Setup

#### Windows
```bash
# Navigate to frontend directory from the project root
cd frontend  # Make sure you're in the correct directory

# Option 1: Standard installation
npm install --legacy-peer-deps

# Option 2: If you encounter dependency issues, use the fix script
node fix_dependencies.js

# Start the frontend server
npm start
```

#### macOS/Linux
```bash
# Navigate to frontend directory from the project root
cd frontend  # Make sure you're in the correct directory

# Option 1: Standard installation
npm install --legacy-peer-deps

# Option 2: If you encounter dependency issues, use the fix script
node fix_dependencies.js

# Start the frontend server
npm start
```

### 5. Access the Application
- Frontend: Open your browser and go to `http://localhost:3000`
- Backend API: Available at `http://localhost:8001/api`

## Troubleshooting

### Backend Issues

#### Windows
1. If you encounter dependency conflicts:
   ```bash
   pip uninstall channels daphne djangorestframework
   pip install -r requirements.txt
   ```

2. If you see "cannot import name 'parse_header'" error:
   - This is a compatibility issue between Django and DRF versions
   - Make sure to use Django 4.2.10 and djangorestframework 3.14.0
   ```bash
   pip install Django==4.2.10 djangorestframework==3.14.0
   ```

3. If the database is not populated:
   ```bash
   cd backend
   ..\venv\Scripts\activate
   python manage.py migrate
   python fix_data.py
   ```

4. If the server won't start:
   - Check if port 8001 is in use: `netstat -ano | findstr :8001`
   - Kill any existing process: `taskkill /F /PID <PID>`

5. If player data shows incorrect teams:
   ```bash
   cd backend
   ..\venv\Scripts\activate
   python fix_data.py
   ```

6. If you see "No module named 'cgi'" error:
   - Update to channels 4.0.0 or higher: `pip install channels>=4.0.0`

#### macOS/Linux
1. If you see "command not found: python":
   - Use `python3` instead of `python` on macOS
   - Ensure Python 3 is installed: `brew install python3`

2. If the database is not populated:
   ```bash
   cd backend
   source ../venv/bin/activate
   python3 manage.py migrate
   python3 fix_data.py
   ```

3. If the server won't start:
   - Check if port 8001 is in use: `lsof -i :8001`
   - Kill any existing process: `kill -9 <PID>`

4. If player data shows incorrect teams:
   ```bash
   cd backend
   source ../venv/bin/activate
   python3 fix_data.py
   ```

### Frontend Issues

#### Windows
1. If npm install fails with "Cannot find module 'ajv/dist/compile/codegen'" error:
   ```bash
   # Use our automated fix script
   cd frontend
   node fix_dependencies.js
   ```
   
   Or manually:
   ```bash
   # PowerShell
   Remove-Item -Recurse -Force node_modules
   Remove-Item package-lock.json
   npm cache clean --force
   npm install --legacy-peer-deps
   ```

2. If the frontend is slow to load:
   - Check browser console for errors
   - Ensure backend API is responding quickly
   - Try clearing browser cache
   - Consider using a production build for better performance:
     ```bash
     npm run build
     npx serve -s build
     ```

2. If the frontend can't connect to the backend:
   - Ensure backend is running on port 8001
   - Check browser console for CORS errors
   - Verify API_URL in `src/services/api.js`

3. If you can't save lineups with the same name:
   - This is by design to prevent duplicate lineup names
   - Choose a different name for each lineup

#### macOS/Linux
1. If npm install fails:
   ```bash
   rm -rf node_modules
   npm cache clean --force
   npm install --legacy-peer-deps
   ```

2. If the frontend can't connect to the backend:
   - Ensure backend is running on port 8001
   - Check browser console for CORS errors
   - Verify API_URL in `src/services/api.js`

3. If you can't save lineups with the same name:
   - This is by design to prevent duplicate lineup names
   - Choose a different name for each lineup

## Files to Include in Version Control
- All source code files (*.py, *.js, *.jsx, *.css)
- Configuration files (requirements.txt, package.json, etc.)
- Documentation files (README.md, CHANGELOG.md)
- Migration files

## Files to Exclude (already in .gitignore)
- Virtual environment (venv/)
- Node modules (node_modules/)
- Database files (db.sqlite3)
- Compiled Python files (__pycache__/)
- Environment files (.env)
- Build directories (build/, dist/)
- Media and upload files (uploads/, media/)
- IDE specific files (.vscode/, .idea/)
- System files (.DS_Store)

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Notifications
The notification icon in the top navigation bar provides real-time updates about:

1. **Player Stats Updates**: Notifications when player statistics are updated with the latest game data
2. **Lineup Recommendations**: Suggestions for new lineups based on recent player performance
3. **Game Schedules**: Alerts about upcoming NBA games that might affect your lineup decisions
4. **Optimization Results**: Notifications when your saved lineups have been automatically optimized

The notification system helps you stay informed about changes that might affect your lineup decisions without having to constantly check for updates manually. Click on the bell icon in the top navigation bar to view your notifications.

## Performance Optimizations
The application includes several performance optimizations:

1. **API Caching**: Frequently accessed data is cached to reduce API calls
2. **Lazy Loading**: Components like charts are loaded only when needed
3. **Memoization**: React components are memoized to prevent unnecessary re-renders
4. **Database Optimizations**: Queries use select_related and prefetch_related for efficient data retrieval
