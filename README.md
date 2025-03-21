


![GIF](https://github.com/midani-47/midani-47/blob/main/gifs/Under-Construction-Sign-for-Locator.webp?raw=true)



# NBA Lineup Optimizer

An interactive web application for creating, optimizing, and comparing NBA lineups.

## Features

- Browse NBA players with detailed statistics
- Create custom lineups with your favorite players
- Optimize lineups based on different strategies (scoring, defense, balanced)
- Compare lineups to analyze their strengths and weaknesses
- View player performance metrics and statistics

## Requirements

- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn

## Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/nba-lineup-optimizer.git
cd nba-lineup-optimizer
```

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate a virtual environment (optional but recommended)
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install required packages
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Run the database fix script to ensure everything is set up correctly
python fix_migrations.py
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install
```

## Running the Application

### Option 1: Universal Start Script (Recommended)

From the project root directory:

```bash
# Install required packages
npm install

# Run the application
npm start
```

This script will automatically detect your operating system, start both the backend and frontend servers, and handle errors gracefully.

### Option 2: Manual Start

If you prefer to start the servers manually:

#### Start the Backend

```bash
cd backend
python manage.py runserver
```

#### Start the Frontend

In a new terminal:

```bash
cd frontend
npm start
```

## Usage

1. **Browse Players**: Explore the NBA player database with detailed stats
2. **Create Lineups**: Select players to build your own custom lineups
3. **Optimize Lineups**: Automatically improve your lineups based on different strategies
4. **Compare Lineups**: See how different lineups stack up against each other
5. **View Player Details**: Dive deep into individual player statistics

## Troubleshooting

If you encounter issues:

1. **Database Migration Errors**: Run `python fix_migrations.py` in the backend directory
2. **Image Loading Issues**: Check your internet connection as player images are loaded from NBA's CDN
3. **Startup Script Errors**: Try starting the backend and frontend manually as described in Option 2
4. **Missing Player Data**: The application will create sample data if needed


## License

MIT

