# NBA Lineup Optimizer

A user-friendly tool for NBA lineup analysis and optimization, designed for data science beginners.

## Features

- Browse NBA players with detailed statistics
- Create custom lineups with your favorite players
- Optimize lineups based on different strategies (scoring, defense, balanced)
- Compare lineups to analyze their strengths and weaknesses
- View player performance metrics and statistics
- ML-based predictions for lineup performance

## Quick Start

### Windows
```
start.bat
```

### macOS/Linux
```
./start.sh
```

That's it! The app will automatically:
1. Create a virtual environment (if needed)
2. Install all required dependencies
3. Generate sample NBA player data
4. Launch the application in your browser

## Reset Data

If you want to clear cached data and start fresh:

### Windows
```
reset.bat
```

### macOS/Linux
```
./reset.sh
```

## Technical Documentation

### Data Loading System
The application uses a tiered data loading approach:
1. **Cached Data**: First checks for locally stored CSV files in the `/data` directory
2. **Sample Data Generation**: If no cache exists, generates realistic NBA player data using `create_sample_players()` and `create_sample_player_stats()`
3. **Real NBA API**: Optional background loading via `fetch_real_data_background()` using the NBA API

Data loading is optimized for fast startup using:
- Static team data from the NBA API
- Pre-defined player profiles with real NBA player names and teams
- Statistical distributions based on player positions and star status

### Lineup Creation
- Player selection implemented via multi-page approach (browse and direct selection)
- Lineup composition uses a 5-player model with position tracking
- Session state management ensures lineup persistence between pages
- Validation ensures complete lineups before saving

### Statistical Analysis
- Player stats are processed using pandas DataFrames with groupby operations
- Positional analysis maps players to appropriate roles
- Visualization tools in the `src/visualization` module use Plotly for:
  - Radar charts for overall player profile visualization
  - Bar charts for direct player comparisons
  - Percentage comparisons for shooting efficiency
  - Team performance metrics

### Lineup Optimization
The application offers three optimization strategies:
1. **Scoring Focus**: Prioritizes points, shooting percentages, and assists
   - Algorithm: Weighted score calculation with emphasis on offensive metrics
   - Implementation: `optimize_lineup_for_scoring()` in `src/optimizer/lineup_optimizer.py`

2. **Defensive Focus**: Prioritizes rebounds, steals, blocks, and plus/minus
   - Algorithm: Weighted score calculation with emphasis on defensive metrics
   - Implementation: `optimize_lineup_for_defense()` in `src/optimizer/lineup_optimizer.py`

3. **Balanced Approach**: Optimizes for overall team chemistry and versatility
   - Algorithm: Uniform weighting across all statistical categories
   - Implementation: `optimize_lineup_for_balanced()` in `src/optimizer/lineup_optimizer.py`

Each optimization algorithm:
1. Evaluates individual player statistics
2. Calculates positional balance
3. Considers complementary skill sets
4. Returns the optimal 5-player combination

### Machine Learning Predictions
The ML prediction system uses:
1. **Feature Engineering**: Extracts relevant statistics from player data
2. **Model Application**: Applies pre-trained models to predict:
   - Expected points per game
   - Win probability
   - Chemistry score
   - Offensive and defensive ratings
3. **Implementation**: `predict_lineup_performance()` in `src/models/lineup_predictor.py`

### Data Visualization
All visualizations use Plotly for interactive charts:
- Player radar charts (`plot_player_radar_chart`)
- Lineup comparisons (`plot_player_comparison`)
- Team performance metrics (`plot_team_performance`)

Charts are optimized for Streamlit's display system with responsive layouts.

## Advanced Setup (Optional)

### Requirements

- Python 3.8 or higher
- pip (Python package installer)

### Manual Installation

#### Windows

```
# Clone this repository
git clone https://github.com/yourusername/nba-lineup-optimizer.git
cd nba-lineup-optimizer

# Create a virtual environment 
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m streamlit run app.py
```

#### macOS/Linux

```
# Clone this repository
git clone https://github.com/yourusername/nba-lineup-optimizer.git
cd nba-lineup-optimizer

# Create a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m streamlit run app.py
```

#### macOS with Homebrew (Recommended for macOS)

For macOS users with Homebrew, we recommend using the helper script which installs necessary system dependencies:

```
./mac_setup.sh
```

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
