# 🏀 NBA Lineup Optimizer ⛹🏾‍♂️

## Project Description
The NBA Lineup Optimizer is a full-stack web application designed to help users build, compare, and optimize NBA lineups. It leverages real-time player data to provide insights and analytics for lineup management.

## Features
- **Dashboard**: View top performers and quick actions to build or optimize lineups.
- **Players Page**: Browse and filter NBA players by name, position, and team.
- **Lineup Builder**: Create custom lineups with drag-and-drop functionality.
- **Lineup Comparison**: Compare two lineups side by side with statistical and radar charts.
- **Lineup Optimizer**: Optimize lineups based on criteria like offense, defense, or balanced performance.

## Initialization

### Quick Start
For a quick start, you can use the provided shell script:
```bash
chmod +x start.sh  # Make the script executable
./start.sh         # Start both backend and frontend
```
Use `./start.sh --reload-data` to force reload the NBA data.

### Manual Setup
1. **Backend Setup**:
   - Navigate to the backend directory:
     ```bash
     cd nba_lineup_optimizer/backend
     ```
   - Create and activate a virtual environment:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     ```
   - Install the required packages:
     ```bash
     pip install -r ../requirements.txt
     ```
   - Apply database migrations:
     ```bash
     python manage.py migrate
     ```
   - Load initial NBA data:
     ```bash
     python manage.py load_nba_data
     ```
   - Run the Django development server:
     ```bash
     python manage.py runserver 8001
     ```

2. **Frontend Setup**:
   - Navigate to the frontend directory:
     ```bash
     cd nba_lineup_optimizer/frontend
     ```
   - Install the required packages:
     ```bash
     npm install --legacy-peer-deps
     ```
   - Start the React development server:
     ```bash
     npm start
     ```

3. **Access the Application**:
   - Open your browser and go to `http://localhost:3000` to access the application.

## Troubleshooting
- **Backend Port Issues**: If port 8001 is already in use, you can specify a different port:
  ```bash
  python manage.py runserver 8002
  ```
  Remember to update the API_URL in `frontend/src/services/api.js` to match the new port.

- **Missing Data**: If you don't see player data in the frontend, make sure you've run the `load_nba_data` command and that the backend server is running.

- **WebSocket Support**: For real-time updates, install the optional channels package:
  ```bash
  pip install channels channels-redis
  ```
  You'll also need Redis running locally for WebSocket support.

## Next Steps
- Implement user authentication for personalized experiences.
- Enhance optimization algorithms for better lineup suggestions.
- Add mobile responsiveness for better accessibility on different devices.
- Improve performance and scalability for larger datasets. # nba-lineup-optimizer
