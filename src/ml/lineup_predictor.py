import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
from typing import List, Dict, Tuple, Optional, Union, Any
import logging

from src.ml.feature_engineering import FeatureEngineer

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LineupPredictor:
    """
    Class for predicting lineup performance using machine learning models.
    """
    
    def __init__(self, model_dir: str = 'models/lineup_predictor'):
        """
        Initialize the lineup predictor.
        
        Args:
            model_dir: Directory to save/load models
        """
        self.model_dir = model_dir
        self.feature_engineer = FeatureEngineer()
        self.scaler = None
        self.offense_model = None
        self.defense_model = None
        self.feature_names = []
        
        # Create model directory if it doesn't exist
        os.makedirs(model_dir, exist_ok=True)
        
    def _prepare_features(self, lineup: List[str], player_stats: pd.DataFrame) -> np.ndarray:
        """
        Prepare feature vector for a lineup.
        
        Args:
            lineup: List of player IDs
            player_stats: DataFrame with player statistics
            
        Returns:
            Feature vector
        """
        # Extract stats for players in the lineup
        lineup_stats = player_stats[player_stats['player_id'].isin(lineup)]
        
        if lineup_stats.empty:
            logger.warning(f"No statistics found for lineup {lineup}")
            return np.zeros(len(self.feature_names))
        
        # Generate basic features
        # Use averages of key statistics
        feature_dict = {}
        
        # Calculate averages for available statistics
        for stat in ['pts', 'reb', 'ast', 'stl', 'blk', 'tov', 'fg_pct', 'fg3_pct', 'ft_pct']:
            if stat in lineup_stats.columns:
                feature_dict[f'avg_{stat}'] = lineup_stats[stat].mean()
            else:
                feature_dict[f'avg_{stat}'] = 0.0
        
        # Calculate variance for key stats to measure consistency
        for stat in ['pts', 'reb', 'ast']:
            if stat in lineup_stats.columns:
                feature_dict[f'var_{stat}'] = lineup_stats[stat].var()
            else:
                feature_dict[f'var_{stat}'] = 0.0
        
        # Position balance (assuming position is in the data)
        if 'position' in lineup_stats.columns:
            positions = lineup_stats['position'].value_counts()
            feature_dict['num_guards'] = positions.get('G', 0) + positions.get('PG', 0) + positions.get('SG', 0)
            feature_dict['num_forwards'] = positions.get('F', 0) + positions.get('SF', 0) + positions.get('PF', 0)
            feature_dict['num_centers'] = positions.get('C', 0)
        
        # Convert to feature vector
        feature_vector = []
        for name in self.feature_names:
            feature_vector.append(feature_dict.get(name, 0.0))
            
        return np.array(feature_vector)
    
    def train(self, lineups: List[List[str]], offensive_ratings: List[float], 
              defensive_ratings: List[float], player_stats: pd.DataFrame,
              test_size: float = 0.2, random_state: int = 42) -> Dict[str, float]:
        """
        Train the prediction models.
        
        Args:
            lineups: List of lineups (each a list of player IDs)
            offensive_ratings: List of offensive ratings for each lineup
            defensive_ratings: List of defensive ratings for each lineup
            player_stats: DataFrame with player statistics
            test_size: Proportion of data to use for testing
            random_state: Random seed for reproducibility
            
        Returns:
            Dictionary with training metrics
        """
        if len(lineups) != len(offensive_ratings) or len(lineups) != len(defensive_ratings):
            raise ValueError("Number of lineups must match number of ratings")
            
        if len(lineups) < 10:
            logger.warning("Training with very few examples, results may be unreliable")
        
        # Generate features for each lineup
        features_list = []
        for lineup in lineups:
            lineup_stats = player_stats[player_stats['player_id'].isin(lineup)]
            
            # Skip lineups with no statistics
            if lineup_stats.empty:
                continue
                
            # Generate basic features (same logic as in _prepare_features)
            feature_dict = {}
            
            # Calculate averages for available statistics
            for stat in ['pts', 'reb', 'ast', 'stl', 'blk', 'tov', 'fg_pct', 'fg3_pct', 'ft_pct']:
                if stat in lineup_stats.columns:
                    feature_dict[f'avg_{stat}'] = lineup_stats[stat].mean()
                else:
                    feature_dict[f'avg_{stat}'] = 0.0
            
            # Calculate variance for key stats
            for stat in ['pts', 'reb', 'ast']:
                if stat in lineup_stats.columns:
                    feature_dict[f'var_{stat}'] = lineup_stats[stat].var()
                else:
                    feature_dict[f'var_{stat}'] = 0.0
            
            # Position balance
            if 'position' in lineup_stats.columns:
                positions = lineup_stats['position'].value_counts()
                feature_dict['num_guards'] = positions.get('G', 0) + positions.get('PG', 0) + positions.get('SG', 0)
                feature_dict['num_forwards'] = positions.get('F', 0) + positions.get('SF', 0) + positions.get('PF', 0)
                feature_dict['num_centers'] = positions.get('C', 0)
            
            features_list.append(feature_dict)
        
        # Create feature matrix
        if not features_list:
            logger.error("No features generated for any lineup")
            return {"error": "No features generated"}
            
        # Get all unique feature names
        self.feature_names = sorted(list(set().union(*[f.keys() for f in features_list])))
        
        # Create feature matrix
        X = np.zeros((len(features_list), len(self.feature_names)))
        for i, features in enumerate(features_list):
            for j, feature_name in enumerate(self.feature_names):
                X[i, j] = features.get(feature_name, 0.0)
        
        # Filter out empty lineups
        valid_indices = list(range(len(features_list)))
        Y_off = [offensive_ratings[i] for i in valid_indices]
        Y_def = [defensive_ratings[i] for i in valid_indices]
        
        # Scale features
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        # Train offensive rating model
        X_train_off, X_test_off, y_train_off, y_test_off = train_test_split(
            X_scaled, Y_off, test_size=test_size, random_state=random_state
        )
        
        self.offense_model = RandomForestRegressor(n_estimators=100, random_state=random_state)
        self.offense_model.fit(X_train_off, y_train_off)
        
        # Evaluate offensive model
        y_pred_off = self.offense_model.predict(X_test_off)
        offense_mse = mean_squared_error(y_test_off, y_pred_off)
        offense_r2 = r2_score(y_test_off, y_pred_off)
        
        # Train defensive rating model
        X_train_def, X_test_def, y_train_def, y_test_def = train_test_split(
            X_scaled, Y_def, test_size=test_size, random_state=random_state
        )
        
        self.defense_model = RandomForestRegressor(n_estimators=100, random_state=random_state)
        self.defense_model.fit(X_train_def, y_train_def)
        
        # Evaluate defensive model
        y_pred_def = self.defense_model.predict(X_test_def)
        defense_mse = mean_squared_error(y_test_def, y_pred_def)
        defense_r2 = r2_score(y_test_def, y_pred_def)
        
        # Save models
        self._save_models()
        
        # Return metrics
        return {
            "offense_mse": offense_mse,
            "offense_r2": offense_r2,
            "defense_mse": defense_mse,
            "defense_r2": defense_r2,
            "n_samples": len(valid_indices),
            "n_features": len(self.feature_names)
        }
    
    def _save_models(self) -> None:
        """Save trained models and metadata to disk."""
        if self.offense_model is None or self.defense_model is None:
            logger.warning("No models to save")
            return
            
        # Save models and metadata
        joblib.dump(self.offense_model, f"{self.model_dir}/offense_model.pkl")
        joblib.dump(self.defense_model, f"{self.model_dir}/defense_model.pkl")
        joblib.dump(self.scaler, f"{self.model_dir}/scaler.pkl")
        joblib.dump(self.feature_names, f"{self.model_dir}/feature_names.pkl")
        
        logger.info(f"Models saved to {self.model_dir}")
    
    def load_models(self) -> bool:
        """
        Load trained models from disk.
        
        Returns:
            True if models were loaded successfully, False otherwise
        """
        try:
            model_files = [
                f"{self.model_dir}/offense_model.pkl",
                f"{self.model_dir}/defense_model.pkl",
                f"{self.model_dir}/scaler.pkl",
                f"{self.model_dir}/feature_names.pkl"
            ]
            
            # Check if all files exist
            if not all(os.path.exists(f) for f in model_files):
                logger.warning("Some model files missing, cannot load")
                return False
                
            self.offense_model = joblib.load(model_files[0])
            self.defense_model = joblib.load(model_files[1])
            self.scaler = joblib.load(model_files[2])
            self.feature_names = joblib.load(model_files[3])
            
            logger.info(f"Models loaded from {self.model_dir}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            return False
    
    def predict(self, lineup: List[str], player_stats: pd.DataFrame) -> Tuple[float, float]:
        """
        Predict offensive and defensive ratings for a lineup.
        
        Args:
            lineup: List of player IDs
            player_stats: DataFrame with player statistics
            
        Returns:
            Tuple of (offensive_rating, defensive_rating)
        """
        # If no models available, use simple heuristic
        if self.offense_model is None or self.defense_model is None:
            logger.warning("No models available, using heuristic prediction")
            return self._heuristic_prediction(lineup, player_stats)
            
        # Prepare features for this lineup
        features = self._prepare_features(lineup, player_stats)
        
        # Scale features
        features_scaled = self.scaler.transform(features.reshape(1, -1))
        
        # Make predictions
        offensive_rating = float(self.offense_model.predict(features_scaled)[0])
        defensive_rating = float(self.defense_model.predict(features_scaled)[0])
        
        return offensive_rating, defensive_rating
    
    def _heuristic_prediction(self, lineup: List[str], player_stats: pd.DataFrame) -> Tuple[float, float]:
        """
        Make a simple prediction based on player averages when no model is available.
        
        Args:
            lineup: List of player IDs
            player_stats: DataFrame with player statistics
            
        Returns:
            Tuple of (offensive_rating, defensive_rating)
        """
        # Filter stats for the lineup
        lineup_stats = player_stats[player_stats['player_id'].isin(lineup)]
        
        if lineup_stats.empty:
            logger.warning(f"No statistics found for lineup {lineup}")
            return 100.0, 100.0  # Default values
        
        # Simple offensive rating based on points and assists
        if 'pts' in lineup_stats.columns and 'ast' in lineup_stats.columns:
            avg_pts = lineup_stats['pts'].mean()
            avg_ast = lineup_stats['ast'].mean()
            offensive_rating = 85 + (avg_pts * 0.5) + (avg_ast * 0.25)
        else:
            offensive_rating = 100.0
        
        # Simple defensive rating based on steals and blocks
        if 'stl' in lineup_stats.columns and 'blk' in lineup_stats.columns:
            avg_stl = lineup_stats['stl'].mean()
            avg_blk = lineup_stats['blk'].mean()
            defensive_rating = 110 - (avg_stl * 2) - (avg_blk * 2)
        else:
            defensive_rating = 100.0
            
        return offensive_rating, defensive_rating
    
    def generate_training_data(self, player_stats: pd.DataFrame, n_samples: int = 1000) -> Tuple[List[List[str]], List[float], List[float]]:
        """
        Generate synthetic training data for model training.
        
        Args:
            player_stats: DataFrame with player statistics
            n_samples: Number of training samples to generate
            
        Returns:
            Tuple of (lineups, offensive_ratings, defensive_ratings)
        """
        if 'player_id' not in player_stats.columns:
            raise ValueError("Player statistics DataFrame must contain a 'player_id' column")
            
        logger.info(f"Generating {n_samples} synthetic training examples")
        
        # Get all player IDs
        all_player_ids = player_stats['player_id'].unique().tolist()
        
        if len(all_player_ids) < 5:
            raise ValueError("Need at least 5 players to generate lineups")
            
        # Generate random lineups
        lineups = []
        offensive_ratings = []
        defensive_ratings = []
        
        for _ in range(n_samples):
            # Select 5 random players
            lineup = np.random.choice(all_player_ids, size=5, replace=False).tolist()
            
            # Calculate ratings based on player stats
            lineup_stats = player_stats[player_stats['player_id'].isin(lineup)]
            
            # Skip if no stats
            if lineup_stats.empty:
                continue
                
            # Generate synthetic ratings with some randomness
            # Base on averages with noise
            if 'pts' in lineup_stats.columns and 'ast' in lineup_stats.columns:
                avg_pts = lineup_stats['pts'].mean()
                avg_ast = lineup_stats['ast'].mean()
                offensive_base = 85 + (avg_pts * 0.5) + (avg_ast * 0.25)
                # Add some noise
                offensive_rating = offensive_base + np.random.normal(0, 5)
            else:
                offensive_rating = 100.0 + np.random.normal(0, 5)
                
            if 'stl' in lineup_stats.columns and 'blk' in lineup_stats.columns:
                avg_stl = lineup_stats['stl'].mean()
                avg_blk = lineup_stats['blk'].mean()
                defensive_base = 110 - (avg_stl * 2) - (avg_blk * 2)
                # Add some noise
                defensive_rating = defensive_base + np.random.normal(0, 5)
            else:
                defensive_rating = 100.0 + np.random.normal(0, 5)
                
            lineups.append(lineup)
            offensive_ratings.append(offensive_rating)
            defensive_ratings.append(defensive_rating)
            
        logger.info(f"Generated {len(lineups)} valid training examples")
        return lineups, offensive_ratings, defensive_ratings
    
    def get_feature_importance(self) -> pd.DataFrame:
        """
        Get feature importance from the trained models.
        
        Returns:
            DataFrame with feature importance for both models
        """
        if self.offense_model is None or self.defense_model is None:
            logger.warning("No models available for feature importance")
            return pd.DataFrame()
            
        # Get feature importances
        offense_importance = self.offense_model.feature_importances_
        defense_importance = self.defense_model.feature_importances_
        
        # Average importance
        avg_importance = (offense_importance + defense_importance) / 2
        
        # Create DataFrame
        importance_df = pd.DataFrame({
            'feature': self.feature_names,
            'offense_importance': offense_importance,
            'defense_importance': defense_importance,
            'avg_importance': avg_importance
        })
        
        # Sort by average importance
        importance_df = importance_df.sort_values('avg_importance', ascending=False)
        
        return importance_df
    
    def predict_best_substitution(self, current_lineup: List[str], bench_players: List[str], 
                                 player_stats: pd.DataFrame) -> Dict:
        """
        Predict the best substitution for a lineup.
        
        Args:
            current_lineup: Current lineup (list of player IDs)
            bench_players: Available bench players (list of player IDs)
            player_stats: DataFrame with player statistics
            
        Returns:
            Dictionary with best substitution information
        """
        if len(current_lineup) != 5:
            logger.warning(f"Current lineup has {len(current_lineup)} players, not 5")
            return {"error": "Current lineup must have exactly 5 players"}
            
        if not bench_players:
            logger.warning("No bench players available for substitution")
            return {"error": "No bench players available for substitution"}
            
        # Get current lineup rating
        current_off, current_def = self.predict(current_lineup, player_stats)
        current_net = current_off - current_def
        
        best_sub = {
            "player_out": None,
            "player_in": None,
            "old_offensive_rating": current_off,
            "new_offensive_rating": current_off,
            "old_defensive_rating": current_def,
            "new_defensive_rating": current_def,
            "net_rating_improvement": 0
        }
        
        # Try all possible substitutions
        for player_out in current_lineup:
            for player_in in bench_players:
                # Create new lineup
                new_lineup = [p if p != player_out else player_in for p in current_lineup]
                
                # Predict ratings
                new_off, new_def = self.predict(new_lineup, player_stats)
                new_net = new_off - new_def
                
                # Calculate improvement
                improvement = new_net - current_net
                
                # Update best substitution if better
                if improvement > best_sub["net_rating_improvement"]:
                    best_sub = {
                        "player_out": player_out,
                        "player_in": player_in,
                        "old_offensive_rating": current_off,
                        "new_offensive_rating": new_off,
                        "old_defensive_rating": current_def,
                        "new_defensive_rating": new_def,
                        "net_rating_improvement": improvement
                    }
        
        # Get player names if available
        if "player_name" in player_stats.columns:
            player_map = dict(zip(player_stats["player_id"], player_stats["player_name"]))
            
            if best_sub["player_out"] in player_map:
                best_sub["player_out_name"] = player_map[best_sub["player_out"]]
                
            if best_sub["player_in"] in player_map:
                best_sub["player_in_name"] = player_map[best_sub["player_in"]]
        
        return best_sub 