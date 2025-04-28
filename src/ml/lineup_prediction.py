import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from typing import List, Dict, Any, Tuple
import joblib
import os

class LineupPredictor:
    """
    Machine learning model for predicting lineup performance.
    """
    
    def __init__(self):
        """Initialize the lineup predictor with default models"""
        self.offense_model = None
        self.defense_model = None
        self.scaler = None
        self.feature_names = None
        self.model_trained = False
        self.model_path = os.path.join('models', 'lineup_predictor')
        
    def _prepare_features(self, player_ids: List[str], player_stats: pd.DataFrame) -> np.ndarray:
        """
        Prepare feature vector for a lineup based on player statistics.
        
        Args:
            player_ids: List of player IDs in the lineup
            player_stats: DataFrame containing player statistics
            
        Returns:
            Feature vector for the lineup
        """
        # Filter and aggregate player stats
        lineup_stats = player_stats[player_stats['player_id'].isin(player_ids)]
        
        if lineup_stats.empty:
            # Return zeros if no stats found
            if self.feature_names:
                return np.zeros(len(self.feature_names))
            else:
                # Default feature count if not trained yet
                return np.zeros(20)
        
        # Group by player and get mean stats
        avg_player_stats = lineup_stats.groupby('player_id').mean()
        
        # Select relevant features
        relevant_stats = ['pts', 'reb', 'ast', 'stl', 'blk', 'fg_pct', 'fg3_pct']
        available_stats = [stat for stat in relevant_stats if stat in avg_player_stats.columns]
        
        # Create features for the lineup
        features = {}
        
        # Calculate average stats for the lineup
        for stat in available_stats:
            features[f'avg_{stat}'] = avg_player_stats[stat].mean()
            features[f'max_{stat}'] = avg_player_stats[stat].max()
            features[f'min_{stat}'] = avg_player_stats[stat].min()
            features[f'std_{stat}'] = avg_player_stats[stat].std()
        
        # Convert to numpy array
        if self.feature_names is None:
            # First time, store feature names
            self.feature_names = sorted(features.keys())
        
        feature_vector = np.array([features.get(feat, 0) for feat in self.feature_names])
        
        return feature_vector
    
    def train(self, lineups: List[List[str]], 
              offensive_ratings: List[float], 
              defensive_ratings: List[float],
              player_stats: pd.DataFrame) -> bool:
        """
        Train the prediction models on lineup data.
        
        Args:
            lineups: List of lineups (each a list of player IDs)
            offensive_ratings: List of offensive ratings for each lineup
            defensive_ratings: List of defensive ratings for each lineup
            player_stats: DataFrame containing player statistics
            
        Returns:
            True if training was successful, False otherwise
        """
        if len(lineups) != len(offensive_ratings) or len(lineups) != len(defensive_ratings):
            return False
        
        # Prepare training data
        X = []
        for lineup in lineups:
            features = self._prepare_features(lineup, player_stats)
            X.append(features)
        
        X = np.array(X)
        y_offense = np.array(offensive_ratings)
        y_defense = np.array(defensive_ratings)
        
        # Scale features
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        # Train models
        self.offense_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.defense_model = RandomForestRegressor(n_estimators=100, random_state=42)
        
        self.offense_model.fit(X_scaled, y_offense)
        self.defense_model.fit(X_scaled, y_defense)
        
        self.model_trained = True
        
        # Create directory if it doesn't exist
        os.makedirs(self.model_path, exist_ok=True)
        
        # Save models
        joblib.dump(self.offense_model, os.path.join(self.model_path, 'offense_model.pkl'))
        joblib.dump(self.defense_model, os.path.join(self.model_path, 'defense_model.pkl'))
        joblib.dump(self.scaler, os.path.join(self.model_path, 'scaler.pkl'))
        joblib.dump(self.feature_names, os.path.join(self.model_path, 'feature_names.pkl'))
        
        return True
    
    def load_models(self) -> bool:
        """
        Load trained models from disk.
        
        Returns:
            True if models were loaded successfully, False otherwise
        """
        try:
            self.offense_model = joblib.load(os.path.join(self.model_path, 'offense_model.pkl'))
            self.defense_model = joblib.load(os.path.join(self.model_path, 'defense_model.pkl'))
            self.scaler = joblib.load(os.path.join(self.model_path, 'scaler.pkl'))
            self.feature_names = joblib.load(os.path.join(self.model_path, 'feature_names.pkl'))
            self.model_trained = True
            return True
        except (FileNotFoundError, IOError):
            # Models not found, need to train
            return False
    
    def predict(self, player_ids: List[str], player_stats: pd.DataFrame) -> Dict[str, float]:
        """
        Predict offensive and defensive ratings for a lineup.
        
        Args:
            player_ids: List of player IDs in the lineup
            player_stats: DataFrame containing player statistics
            
        Returns:
            Dictionary with predicted ratings
        """
        if not self.model_trained:
            # Try to load models, and if that fails, use a simple heuristic
            if not self.load_models():
                return self._simple_prediction(player_ids, player_stats)
        
        # Prepare features
        features = self._prepare_features(player_ids, player_stats)
        features = features.reshape(1, -1)
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Make predictions
        offense_pred = self.offense_model.predict(features_scaled)[0]
        defense_pred = self.defense_model.predict(features_scaled)[0]
        
        # Calculate overall rating (weighted average)
        overall_pred = 0.6 * offense_pred + 0.4 * defense_pred
        
        return {
            'offense': float(offense_pred),
            'defense': float(defense_pred),
            'overall': float(overall_pred)
        }
    
    def _simple_prediction(self, player_ids: List[str], player_stats: pd.DataFrame) -> Dict[str, float]:
        """
        Make a simple prediction based on averages when no model is available.
        
        Args:
            player_ids: List of player IDs in the lineup
            player_stats: DataFrame containing player statistics
            
        Returns:
            Dictionary with predicted ratings
        """
        # Filter player stats
        lineup_stats = player_stats[player_stats['player_id'].isin(player_ids)]
        
        if lineup_stats.empty:
            return {'offense': 50.0, 'defense': 50.0, 'overall': 50.0}
        
        # Calculate average offensive and defensive indicators
        avg_stats = lineup_stats.groupby('player_id').mean().mean()
        
        # Offensive rating based on points, assists, and shooting percentages
        offense_rating = 0.0
        if 'pts' in avg_stats:
            offense_rating += avg_stats['pts'] * 2.5
        if 'ast' in avg_stats:
            offense_rating += avg_stats['ast'] * 5
        if 'fg_pct' in avg_stats:
            offense_rating += avg_stats['fg_pct'] * 50
        if 'fg3_pct' in avg_stats:
            offense_rating += avg_stats['fg3_pct'] * 60
            
        # Normalize to 0-100 scale
        offense_rating = min(100, offense_rating / 50 * 100)
        
        # Defensive rating based on steals, blocks, and rebounds
        defense_rating = 0.0
        if 'stl' in avg_stats:
            defense_rating += avg_stats['stl'] * 15
        if 'blk' in avg_stats:
            defense_rating += avg_stats['blk'] * 15
        if 'reb' in avg_stats:
            defense_rating += avg_stats['reb'] * 3
            
        # Normalize to 0-100 scale
        defense_rating = min(100, defense_rating / 30 * 100)
        
        # Overall rating
        overall_rating = 0.6 * offense_rating + 0.4 * defense_rating
        
        return {
            'offense': float(offense_rating),
            'defense': float(defense_rating),
            'overall': float(overall_rating)
        }
    
    def generate_training_data(self, player_stats: pd.DataFrame, player_info: pd.DataFrame, 
                               num_samples: int = 100) -> Tuple[List[List[str]], List[float], List[float]]:
        """
        Generate synthetic training data for model development.
        
        Args:
            player_stats: DataFrame containing player statistics
            player_info: DataFrame containing player information
            num_samples: Number of lineup samples to generate
            
        Returns:
            Tuple of (lineups, offensive_ratings, defensive_ratings)
        """
        from src.optimizer.metrics import calculate_lineup_offensive_rating, calculate_lineup_defensive_rating
        
        # Get all player IDs
        all_player_ids = player_info['player_id'].unique()
        
        # Generate random lineups
        lineups = []
        offensive_ratings = []
        defensive_ratings = []
        
        for _ in range(num_samples):
            # Select 5 random players
            lineup = np.random.choice(all_player_ids, size=5, replace=False).tolist()
            
            # Calculate ratings
            offense_rating = calculate_lineup_offensive_rating(lineup, player_stats)
            defense_rating = calculate_lineup_defensive_rating(lineup, player_stats)
            
            lineups.append(lineup)
            offensive_ratings.append(offense_rating)
            defensive_ratings.append(defense_rating)
        
        return lineups, offensive_ratings, defensive_ratings
    
    def get_feature_importance(self) -> Dict[str, List[Tuple[str, float]]]:
        """
        Get the importance of each feature in the prediction models.
        
        Returns:
            Dictionary with feature importance for each model
        """
        if not self.model_trained and not self.load_models():
            return {"error": "Models not trained"}
        
        # Get feature importance from the models
        offense_importance = self.offense_model.feature_importances_
        defense_importance = self.defense_model.feature_importances_
        
        # Pair with feature names
        offense_features = [(name, float(importance)) 
                           for name, importance in zip(self.feature_names, offense_importance)]
        defense_features = [(name, float(importance)) 
                           for name, importance in zip(self.feature_names, defense_importance)]
        
        # Sort by importance (descending)
        offense_features.sort(key=lambda x: x[1], reverse=True)
        defense_features.sort(key=lambda x: x[1], reverse=True)
        
        return {
            "offense": offense_features[:10],  # Top 10 features
            "defense": defense_features[:10]   # Top 10 features
        } 