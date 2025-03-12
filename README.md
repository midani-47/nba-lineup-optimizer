# NBA Lineup Optimizer

A web application for creating, optimizing, and comparing NBA lineups.

## System Requirements

- Python 3.8 or higher
- Node.js 16 or higher
- 2GB free memory recommended
- Ports 8001 (backend) and 3000 (frontend) must be available

## Quick Start

### Windows
1. Clone this repository
2. Double-click `start.bat`
3. Open http://localhost:3000 in your browser

### Linux/Mac
1. Clone this repository
2. Make the start script executable: `chmod +x start.sh`
3. Run `./start.sh`
4. Open http://localhost:3000 in your browser

## Manual Installation

If the quick start scripts don't work, follow these steps:

### Backend Setup
1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. Install dependencies:
   ```bash
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
   - Windows: `netstat -ano | findstr :8001` or `:3000`
   - Linux/Mac: `lsof -i :8001` or `:3000`
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
   rm db.sqlite3
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
   rm -rf node_modules
   npm install --legacy-peer-deps
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
