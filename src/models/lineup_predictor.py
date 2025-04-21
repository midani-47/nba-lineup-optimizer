import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib
import os
import random
from datetime import datetime
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from optimizer.lineup_optimizer import calculate_lineup_chemistry, check_lineup_balance

# Define model paths
MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data/models')
POINTS_MODEL_PATH = os.path.join(MODELS_DIR, 'points_model.joblib')
WIN_PROB_MODEL_PATH = os.path.join(MODELS_DIR, 'win_prob_model.joblib')
OFF_RTG_MODEL_PATH = os.path.join(MODELS_DIR, 'off_rtg_model.joblib')
DEF_RTG_MODEL_PATH = os.path.join(MODELS_DIR, 'def_rtg_model.joblib')

def _ensure_model_dir():
    """Ensure the models directory exists."""
    os.makedirs(MODELS_DIR, exist_ok=True)

def _extract_features_from_lineup(player_ids, player_stats, players_df):
    """
    Extract features from a lineup for prediction models.
    
    Args:
        player_ids (list): List of player IDs in the lineup
        player_stats (pandas.DataFrame): DataFrame with player statistics
        players_df (pandas.DataFrame): DataFrame with player information
    
    Returns:
        pandas.DataFrame: DataFrame with lineup features
    """
    # Get player stats
    avg_stats_list = []
    
    for player_id in player_ids:
        player_data = player_stats[player_stats['player_id'] == player_id]
        if not player_data.empty:
            # Calculate average stats for the player
            avg_stats = player_data.mean(numeric_only=True)
            avg_stats_list.append(avg_stats)
    
    if not avg_stats_list:
        # Return empty features if no stats found
        return pd.DataFrame()
    
    # Combine stats and calculate lineup features
    lineup_df = pd.DataFrame(avg_stats_list)
    
    # Basic statistics - average and sum
    key_stats = ['pts', 'reb', 'ast', 'stl', 'blk', 'fg_pct', 'fg3_pct', 'ft_pct']
    sum_stats = lineup_df[key_stats].sum()
    avg_stats = lineup_df[key_stats].mean()
    
    # Create feature vector
    features = {}
    
    # Add summed stats
    for stat in key_stats:
        features[f'sum_{stat}'] = sum_stats[stat]
    
    # Add average stats
    for stat in key_stats:
        features[f'avg_{stat}'] = avg_stats[stat]
    
    # Add standard deviation (measure of variance in skills)
    for stat in key_stats:
        features[f'std_{stat}'] = lineup_df[stat].std()
    
    # Add chemistry score
    chemistry = calculate_lineup_chemistry(player_ids, player_stats)
    features['chemistry'] = chemistry
    
    # Add position balance
    is_balanced, reasons = check_lineup_balance(player_ids, players_df)
    features['position_balance'] = 1 if is_balanced else 0
    features['imbalance_count'] = len(reasons)
    
    # Convert to DataFrame
    return pd.DataFrame([features])

def train_models(player_stats, players_df, sample_lineups=None):
    """
    Train machine learning models for lineup prediction.
    For demonstration, this uses simulated data since we don't have actual game results.
    
    Args:
        player_stats (pandas.DataFrame): DataFrame with player statistics
        players_df (pandas.DataFrame): DataFrame with player information
        sample_lineups (list, optional): List of sample lineups for training
    
    Returns:
        dict: Dictionary with trained models
    """
    print("Training prediction models...")
    _ensure_model_dir()
    
    # If no sample lineups provided, generate some random ones
    if not sample_lineups:
        # Get active players
        active_player_ids = players_df['player_id'].tolist()
        
        # Generate 200 random lineups
        sample_lineups = []
        for _ in range(200):
            if len(active_player_ids) >= 5:
                lineup = random.sample(active_player_ids, 5)
                sample_lineups.append(lineup)
    
    # Create training data
    features_list = []
    points_targets = []
    win_prob_targets = []
    off_rtg_targets = []
    def_rtg_targets = []
    
    for lineup in sample_lineups:
        # Extract features
        features = _extract_features_from_lineup(lineup, player_stats, players_df)
        
        if not features.empty:
            features_list.append(features)
            
            # For demonstration, we'll generate synthetic targets based on the features
            # In a real app, these would come from actual game data
            
            # Points prediction (based on sum of player points with some noise)
            pts = features['sum_pts'].iloc[0]
            pts_noise = np.random.normal(0, 5)
            points_targets.append(pts + pts_noise)
            
            # Win probability (based on overall stats quality)
            stat_quality = (
                features['avg_pts'].iloc[0] / 20 +  # Normalize by expected max
                features['avg_reb'].iloc[0] / 10 +
                features['avg_ast'].iloc[0] / 8 +
                features['avg_stl'].iloc[0] / 2 +
                features['avg_blk'].iloc[0] / 2
            ) / 5  # Average of normalized stats
            
            win_prob = min(0.95, max(0.05, stat_quality + np.random.normal(0, 0.1)))
            win_prob_targets.append(win_prob)
            
            # Offensive rating (based mainly on scoring stats)
            off_rtg = 85 + 2 * features['avg_pts'].iloc[0] + 3 * features['avg_ast'].iloc[0] + np.random.normal(0, 5)
            off_rtg_targets.append(off_rtg)
            
            # Defensive rating (based mainly on defensive stats, lower is better)
            def_rtg = 115 - 5 * features['avg_stl'].iloc[0] - 5 * features['avg_blk'].iloc[0] - features['avg_reb'].iloc[0] + np.random.normal(0, 5)
            def_rtg_targets.append(def_rtg)
    
    if not features_list:
        print("No valid features found for training. Using default models.")
        return {}
    
    # Combine all features
    X = pd.concat(features_list, ignore_index=True)
    
    # Train points model
    points_model = RandomForestRegressor(n_estimators=50, random_state=42)
    points_model.fit(X, points_targets)
    joblib.dump(points_model, POINTS_MODEL_PATH)
    
    # Train win probability model
    win_prob_model = RandomForestRegressor(n_estimators=50, random_state=42)
    win_prob_model.fit(X, win_prob_targets)
    joblib.dump(win_prob_model, WIN_PROB_MODEL_PATH)
    
    # Train offensive rating model
    off_rtg_model = RandomForestRegressor(n_estimators=50, random_state=42)
    off_rtg_model.fit(X, off_rtg_targets)
    joblib.dump(off_rtg_model, OFF_RTG_MODEL_PATH)
    
    # Train defensive rating model
    def_rtg_model = RandomForestRegressor(n_estimators=50, random_state=42)
    def_rtg_model.fit(X, def_rtg_targets)
    joblib.dump(def_rtg_model, DEF_RTG_MODEL_PATH)
    
    models = {
        'points': points_model,
        'win_prob': win_prob_model,
        'off_rtg': off_rtg_model,
        'def_rtg': def_rtg_model
    }
    
    print("Models trained and saved.")
    return models

def load_or_train_models(player_stats, players_df):
    """
    Load existing models or train new ones if they don't exist.
    
    Args:
        player_stats (pandas.DataFrame): DataFrame with player statistics
        players_df (pandas.DataFrame): DataFrame with player information
    
    Returns:
        dict: Dictionary with loaded models
    """
    models = {}
    
    # Check if model files exist
    if (os.path.exists(POINTS_MODEL_PATH) and
        os.path.exists(WIN_PROB_MODEL_PATH) and
        os.path.exists(OFF_RTG_MODEL_PATH) and
        os.path.exists(DEF_RTG_MODEL_PATH)):
        
        print("Loading existing models...")
        
        try:
            points_model = joblib.load(POINTS_MODEL_PATH)
            win_prob_model = joblib.load(WIN_PROB_MODEL_PATH)
            off_rtg_model = joblib.load(OFF_RTG_MODEL_PATH)
            def_rtg_model = joblib.load(DEF_RTG_MODEL_PATH)
            
            models = {
                'points': points_model,
                'win_prob': win_prob_model,
                'off_rtg': off_rtg_model,
                'def_rtg': def_rtg_model
            }
            
            print("Models loaded successfully.")
            
        except Exception as e:
            print(f"Error loading models: {e}")
            print("Training new models...")
            models = train_models(player_stats, players_df)
    else:
        print("Models not found. Training new models...")
        models = train_models(player_stats, players_df)
    
    return models

def predict_lineup_performance(player_ids, player_stats, players_df):
    """
    Predict performance for a lineup.
    
    Args:
        player_ids (list): List of player IDs in the lineup
        player_stats (pandas.DataFrame): DataFrame with player statistics
        players_df (pandas.DataFrame): DataFrame with player information
    
    Returns:
        dict: Dictionary with performance predictions
    """
    # Load or train models
    models = load_or_train_models(player_stats, players_df)
    
    if not models:
        # If models couldn't be loaded/trained, return sensible defaults
        return {
            'points_per_game': 100.0,
            'win_probability': 0.5,
            'offensive_rating': 100.0,
            'defensive_rating': 100.0,
            'chemistry_score': 70.0,
            'confidence_level': 'Low (using defaults)',
            'strengths': ["No specific strengths identified"],
            'weaknesses': ["No specific weaknesses identified"]
        }
    
    # Extract features for the lineup
    features = _extract_features_from_lineup(player_ids, player_stats, players_df)
    
    if features.empty:
        # If features couldn't be extracted, return sensible defaults
        return {
            'points_per_game': 100.0,
            'win_probability': 0.5,
            'offensive_rating': 100.0,
            'defensive_rating': 100.0,
            'chemistry_score': 70.0,
            'confidence_level': 'Low (insufficient data)',
            'strengths': ["No specific strengths identified"],
            'weaknesses': ["No specific weaknesses identified"]
        }
    
    # Make predictions
    points_pred = models['points'].predict(features)[0]
    win_prob_pred = models['win_prob'].predict(features)[0]
    off_rtg_pred = models['off_rtg'].predict(features)[0]
    def_rtg_pred = models['def_rtg'].predict(features)[0]
    
    # Get chemistry score
    chemistry = calculate_lineup_chemistry(player_ids, player_stats)
    
    # Determine confidence level based on data quality
    # For demonstration, we'll use a simple heuristic
    confidence_level = 'Medium'
    
    # Identify strengths and weaknesses
    strengths = []
    weaknesses = []
    
    # Check basic stats
    if points_pred > 110:
        strengths.append("High scoring potential")
    elif points_pred < 95:
        weaknesses.append("Low scoring potential")
    
    if off_rtg_pred > 110:
        strengths.append("Efficient offensive production")
    elif off_rtg_pred < 100:
        weaknesses.append("Inefficient offense")
    
    if def_rtg_pred < 105:
        strengths.append("Strong defensive capability")
    elif def_rtg_pred > 110:
        weaknesses.append("Weak defensive capability")
    
    # Check position balance
    is_balanced, balance_reasons = check_lineup_balance(player_ids, players_df)
    if is_balanced:
        strengths.append("Well-balanced positions")
    else:
        weaknesses.append(f"Position imbalance: {', '.join(balance_reasons)}")
    
    # Check chemistry
    if chemistry > 80:
        strengths.append("Excellent team chemistry")
    elif chemistry < 50:
        weaknesses.append("Poor team chemistry")
    
    # If no specific strengths/weaknesses identified, add generic ones
    if not strengths:
        strengths.append("Balanced overall performance")
    if not weaknesses:
        weaknesses.append("No significant weaknesses detected")
    
    # Prepare results
    predictions = {
        'points_per_game': points_pred,
        'win_probability': win_prob_pred,
        'offensive_rating': off_rtg_pred,
        'defensive_rating': def_rtg_pred,
        'chemistry_score': chemistry,
        'confidence_level': confidence_level,
        'strengths': strengths,
        'weaknesses': weaknesses
    }
    
    return predictions

if __name__ == "__main__":
    # Test the prediction functionality
    from data_loader import load_nba_players, load_player_stats
    
    players_df = load_nba_players()
    player_stats = load_player_stats()
    
    # Select a random lineup for testing
    player_ids = players_df['player_id'].sample(5).tolist()
    
    predictions = predict_lineup_performance(player_ids, player_stats, players_df)
    print(f"Points per game: {predictions['points_per_game']:.1f}")
    print(f"Win probability: {predictions['win_probability']:.1%}")
    print(f"Offensive rating: {predictions['offensive_rating']:.1f}")
    print(f"Defensive rating: {predictions['defensive_rating']:.1f}")
    print(f"Chemistry score: {predictions['chemistry_score']:.0f}/100")
    print(f"Confidence level: {predictions['confidence_level']}")
    print("Strengths:")
    for strength in predictions['strengths']:
        print(f"- {strength}")
    print("Weaknesses:")
    for weakness in predictions['weaknesses']:
        print(f"- {weakness}") 