# NBA Lineup Optimizer

A user-friendly tool for NBA lineup analysis and optimization, designed for data science beginners.

## Features

- Browse NBA players with detailed statistics
- Create custom lineups with your favorite players
- Optimize lineups based on different strategies (scoring, defense, balanced)
- Compare lineups to analyze their strengths and weaknesses
- View player performance metrics and statistics
- ML-based predictions for lineup performance

## Requirements

- Python 3.8 or higher
- pip (Python package installer)

## Installation

### Windows

```
# Clone this repository
git clone https://github.com/yourusername/nba-lineup-optimizer.git
cd nba-lineup-optimizer

# Create a virtual environment 
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### macOS/Linux

```
# Clone this repository
git clone https://github.com/yourusername/nba-lineup-optimizer.git
cd nba-lineup-optimizer

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Application

```
streamlit run app.py
```

This will start the web application and automatically open it in your default browser.

## Project Structure

- `app.py`: Main Streamlit application entry point
- `data/`: Data storage directory
- `src/`: Source code
  - `data_loader.py`: Functions for loading NBA data
  - `models/`: ML models for lineup optimization
  - `analysis/`: Statistical analysis modules
  - `visualization/`: Data visualization components
  - `optimizer/`: Lineup optimization algorithms

## How to Use

1. **Browse Players**: View all available NBA players with their stats
2. **Create Lineup**: Select players to create your own custom lineup
3. **Optimize Lineup**: Use different optimization strategies for your lineup
4. **Analyze Performance**: View statistical analysis of your lineup
5. **ML Predictions**: Get performance predictions based on machine learning models

## For Beginners

This project is designed to be beginner-friendly. Each module contains detailed comments and explanations to help you understand the statistical methods and ML concepts being used.

Feel free to explore, modify, and learn from the code!

## License

MIT
