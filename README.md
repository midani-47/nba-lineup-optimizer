# NBA Lineup Optimizer

A web application for creating, optimizing, and comparing NBA lineups.

## System Requirements

- Python 3.8 or higher
- Node.js 16 or higher
- 2GB free memory recommended
- Ports 8001 (backend) and 3000 (frontend) must be available

## Quick Start

### Windows
1. Clone this repository: `git clone https://github.com/yourusername/nba-lineup-optimizer.git`
2. Navigate to the project directory: `cd nba-lineup-optimizer`
3. Run the startup script: `.\start.bat`
4. Open http://localhost:3000 in your browser

### Linux/Mac
1. Clone this repository: `git clone https://github.com/yourusername/nba-lineup-optimizer.git`
2. Navigate to the project directory: `cd nba-lineup-optimizer`
3. Make the start script executable: `chmod +x start.sh`
4. Run the startup script: `./start.sh`
5. Open http://localhost:3000 in your browser

## First-Time Setup Issues

If you encounter issues during the first-time setup, here are some common solutions:

### Python Version Issues
- Make sure you have Python 3.8 or higher installed
- Verify your Python version with `python --version` or `python3 --version`
- If you have multiple Python versions, make sure the correct one is in your PATH
- On Windows, you may need to use `py -3.8` or similar to specify the version

### Virtual Environment Issues
- If you get errors about creating a virtual environment:
  - Windows: `pip install virtualenv`
  - Linux/Mac: `pip3 install virtualenv`
- Then try running the startup script again

### Node.js Issues
- Make sure Node.js 16 or higher is installed
- Verify your Node.js version with `node --version`
- If you have an older version, download the latest LTS from https://nodejs.org/

## Manual Installation

If the quick start scripts don't work, follow these steps:

### Backend Setup
1. Create a virtual environment:
   ```bash
   # Windows
   python -m venv venv
   
   # Linux/Mac
   python3 -m venv venv
   ```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. Install dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   cd backend
   python manage.py migrate
   python check_db.py
   python fix_data.py
   ```

5. Start the backend server:
   ```bash
   python manage.py runserver 8001
   ```

### Frontend Setup
1. Install dependencies:
   ```bash
   cd frontend
   npm install --legacy-peer-deps
   ```

2. Start the frontend server:
   ```bash
   npm start
   ```

## Troubleshooting

### Port Conflicts
If ports 8001 or 3000 are in use:
1. Kill the processes using those ports:
   - Windows: `netstat -ano | findstr :8001` or `:3000`, then `taskkill /F /PID <PID>`
   - Linux/Mac: `lsof -i :8001` or `:3000`, then `kill <PID>`
2. Or change the ports:
   - Backend: Edit `backend/nba_project/settings.py`
   - Frontend: Edit `frontend/package.json`

### Memory Issues
- Close unnecessary applications
- Increase system swap/page file size
- Consider upgrading RAM if issues persist

### Database Issues
1. Delete the database file:
   ```bash
   cd backend
   rm db.sqlite3  # Linux/Mac
   del db.sqlite3  # Windows
   ```
2. Recreate the database:
   ```bash
   python manage.py migrate
   python check_db.py
   python fix_data.py
   ```

### Node.js Issues
1. Clear npm cache:
   ```bash
   npm cache clean --force
   ```
2. Delete node_modules:
   ```bash
   cd frontend
   rm -rf node_modules  # Linux/Mac
   rmdir /s /q node_modules  # Windows
   npm install --legacy-peer-deps
   ```

### Django Issues
If you encounter Django-related errors:
1. Verify Django installation:
   ```bash
   python -c "import django; print(django.get_version())"
   ```
2. Reinstall Django if needed:
   ```bash
   pip install django==4.2.10
   ```

## Features

- Create custom lineups with NBA players
- Optimize lineups based on different strategies
- Compare lineups and view detailed statistics
- Real-time player statistics and updates
- Beautiful and responsive user interface

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
