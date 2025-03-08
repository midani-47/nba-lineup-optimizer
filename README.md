# 🏀 NBA Lineup Optimizer

## Project Description
The NBA Lineup Optimizer is a full-stack web application designed to help users build, compare, and optimize NBA lineups. It leverages real-time player data to provide insights and analytics for lineup management.

## Features
- **Dashboard**: View top performers and quick actions to build or optimize lineups.
- **Players Page**: Browse and filter NBA players by name, position, and team.
- **Lineup Builder**: Create custom lineups with search and add functionality.
- **Lineup Comparison**: Compare two lineups side by side with statistical and radar charts.
- **Lineup Optimizer**: Optimize lineups based on criteria like offense, defense, or balanced performance.

## Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- npm 6 or higher

## Installation and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/midani-47/nba-lineup-optimizer.git
cd nba-lineup-optimizer
```

### 2. Backend Setup

#### Windows
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

### 3. Frontend Setup

#### Windows
```bash
# Navigate to frontend directory from the project root
cd frontend  # Make sure you're in the correct directory

# Install dependencies
npm install --legacy-peer-deps

# Start the frontend server
npm start
```

#### macOS/Linux
```bash
# Navigate to frontend directory from the project root
cd frontend  # Make sure you're in the correct directory

# Install dependencies
npm install --legacy-peer-deps

# Start the frontend server
npm start
```

### 4. Access the Application
- Frontend: Open your browser and go to `http://localhost:3000`
- Backend API: Available at `http://localhost:8001/api`

## Troubleshooting

### Backend Issues

#### Windows
1. If you encounter dependency conflicts:
   ```bash
   pip uninstall channels daphne
   pip install channels>=4.0.0 daphne>=3.0,<4.0
   ```

2. If the database is not populated:
   ```bash
   cd backend
   ..\venv\Scripts\activate
   python manage.py migrate
   python fix_data.py
   ```

3. If the server won't start:
   - Check if port 8001 is in use: `netstat -ano | findstr :8001`
   - Kill any existing process: `taskkill /F /PID <PID>`

4. If player data shows incorrect teams:
   ```bash
   cd backend
   ..\venv\Scripts\activate
   python fix_data.py
   ```

5. If you see "No module named 'cgi'" error:
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
1. If npm install fails:
   ```bash
   rmdir /s /q node_modules
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
