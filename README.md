# NBA Lineup Optimizer

## Overview
This application showcases data science and machine learning techniques applied to NBA data. It allows users to create, optimize, and predict the performance of NBA lineups using statistical analysis and machine learning models.

## Features

### Player Explorer
- Browse and filter NBA players by team, position, and name
- View detailed player statistics with visualizations 
- Add players to your custom lineup

### Lineup Builder
- Create and manage custom lineups
- Analyze lineup position distribution
- View team statistics for your lineup

### Lineup Optimizer
- Optimize lineups based on different strategies:
  - Scoring: Focus on offensive performance
  - Defense: Focus on defensive capabilities
  - Balanced: Balance of offense and defense
- Compare original and optimized lineups
- Analyze lineup chemistry and position balance

### ML Prediction
- Train Random Forest models to predict lineup performance
- View feature importance for offense and defense
- Predict offensive and defensive ratings for lineups
- Get recommendations for lineup improvements

## Data Science & Machine Learning Techniques
This project demonstrates several key data science and machine learning concepts:

1. **Data Preprocessing**: Cleaning and transforming NBA player statistics
2. **Feature Engineering**: Creating meaningful features from raw statistics
3. **Model Training**: Using Random Forest Regression to predict lineup performance
4. **Statistical Analysis**: Developing metrics for lineup chemistry and balance
5. **Data Visualization**: Creating interactive charts to analyze players and lineups

## Setup Instructions

### Requirements
- Python 3.7+


### Installation
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `streamlit run app.py`

## Project Structure
- `app.py`: Main Streamlit application
- `src/`: Source code directory
  - `data_loader.py`: Functions to load and preprocess NBA data
  - `ml/`: Machine learning models and feature engineering
  - `optimizer/`: Lineup optimization algorithms
  - `visualization/`: Data visualization functions

## Data
The application uses a combination of real and synthetic NBA data:
- Player information: Names, teams, positions, physical attributes
- Player statistics: Points, rebounds, assists, etc.
- Team data: Team information and statistics

## Future Improvements
- Integration with live NBA data
- Enhanced visualization options
- Support for historical lineup analysis
- Integration with fantasy basketball platforms

## License
This project is for educational purposes only. NBA data is subject to NBA licensing.
