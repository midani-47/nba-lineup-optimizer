import os
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Create the models directory if it doesn't exist
os.makedirs('data/models/lineup_predictor', exist_ok=True)

# Load player stats
def load_player_stats():
    """Load player stats from CSV file"""
    if os.path.exists('data/player_stats.csv'):
        return pd.read_csv('data/player_stats.csv')
    else:
        raise FileNotFoundError("Player stats file not found")

# Train and save a new model
def train_and_save_model():
    print("Training new ML model for lineup prediction...")
    
    # Load player stats
    player_stats = load_player_stats()
    
    # Check for required columns
    if 'player_id' not in player_stats.columns or 'pts' not in player_stats.columns:
        print("Error: player_stats missing required columns")
        return False
    
    # Get numeric columns for features
    numeric_cols = player_stats.select_dtypes(include=['number']).columns
    non_metric_cols = ['player_id', 'home_team', 'away_team']
    metric_cols = [col for col in numeric_cols if col not in non_metric_cols]
    
    # Group by player_id to get average stats per player
    X_data = player_stats.groupby('player_id')[metric_cols].mean().reset_index()
    
    # Create target variable (points as example)
    target_col = 'pts'
    y_data = X_data[target_col]
    
    # Drop target and id from features
    X_data = X_data.drop(['player_id', target_col], axis=1)
    
    # Save feature names
    feature_names = X_data.columns.tolist()
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.2, random_state=42)
    
    # Scale the data
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    # Create and train the model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Save model, scaler and feature names
    model_path = os.path.join('data', 'models', 'lineup_predictor', 'offense_model.pkl')
    scaler_path = os.path.join('data', 'models', 'lineup_predictor', 'scaler.pkl')
    feature_names_path = os.path.join('data', 'models', 'lineup_predictor', 'feature_names.pkl')
    
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    joblib.dump(feature_names, feature_names_path)
    
    print(f"Model trained successfully with {len(feature_names)} features:")
    print(", ".join(feature_names))
    print(f"Files saved to: {os.path.dirname(model_path)}")
    
    return True

if __name__ == "__main__":
    train_and_save_model()
