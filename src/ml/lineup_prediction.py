import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from typing import List, Dict, Any, Tuple
import joblib
import os
import random
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

class LineupPredictor:
    """
    Machine learning model for predicting lineup performance.
    """
    
    def __init__(self, model_path: str = 'data/models/lineup_predictor'):
        """Initialize the lineup predictor with default models"""
        self.offense_model = None
        self.defense_model = None
        self.scaler = None
        self.feature_names = None
        self.model_trained = False
        self.model_path = model_path
        
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
        avg_player_stats = lineup_stats.groupby('player_id').mean(numeric_only=True)
        
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
              player_stats: pd.DataFrame) -> Dict[str, Any]:
        """
        Train the prediction models on lineup data.
        
        Args:
            lineups: List of lineups (each a list of player IDs)
            offensive_ratings: List of offensive ratings for each lineup
            defensive_ratings: List of defensive ratings for each lineup
            player_stats: DataFrame containing player statistics
            
        Returns:
            Dictionary with training metrics
        """
        if len(lineups) != len(offensive_ratings) or len(lineups) != len(defensive_ratings):
            return {'error': 'Data size mismatch'}
        
        # Prepare training data
        X = []
        for lineup in lineups:
            features = self._prepare_features(lineup, player_stats)
            X.append(features)
        
        X = np.array(X)
        y_offense = np.array(offensive_ratings)
        y_defense = np.array(defensive_ratings)
        
        # Split data into train/test
        X_train, X_test, y_off_train, y_off_test, y_def_train, y_def_test = train_test_split(
            X, y_offense, y_defense, test_size=0.2, random_state=42
        )
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train models
        self.offense_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.defense_model = RandomForestRegressor(n_estimators=100, random_state=42)
        
        self.offense_model.fit(X_train_scaled, y_off_train)
        self.defense_model.fit(X_train_scaled, y_def_train)
        
        # Evaluate models
        from sklearn.metrics import mean_squared_error, r2_score
        
        y_off_pred = self.offense_model.predict(X_test_scaled)
        y_def_pred = self.defense_model.predict(X_test_scaled)
        
        off_mse = mean_squared_error(y_off_test, y_off_pred)
        off_r2 = r2_score(y_off_test, y_off_pred)
        
        def_mse = mean_squared_error(y_def_test, y_def_pred)
        def_r2 = r2_score(y_def_test, y_def_pred)
        
        self.model_trained = True
        
        # Create directory if it doesn't exist
        os.makedirs(self.model_path, exist_ok=True)
        
        # Save models
        joblib.dump(self.offense_model, os.path.join(self.model_path, 'offense_model.pkl'))
        joblib.dump(self.defense_model, os.path.join(self.model_path, 'defense_model.pkl'))
        joblib.dump(self.scaler, os.path.join(self.model_path, 'scaler.pkl'))
        joblib.dump(self.feature_names, os.path.join(self.model_path, 'feature_names.pkl'))
        
        return {
            'n_samples': len(lineups),
            'n_features': len(self.feature_names),
            'offense_mse': off_mse,
            'offense_r2': off_r2,
            'defense_mse': def_mse,
            'defense_r2': def_r2
        }
    
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
    
    def predict(self, player_ids: List[str], player_stats: pd.DataFrame) -> Tuple[float, float]:
        """
        Predict offensive and defensive ratings for a lineup.
        
        Args:
            player_ids: List of player IDs in the lineup
            player_stats: DataFrame containing player statistics
            
        Returns:
            Tuple of (offensive_rating, defensive_rating)
        """
        if not self.model_trained:
            # Try to load models, and if that fails, use a simple heuristic
            if not self.load_models():
                result = self._simple_prediction(player_ids, player_stats)
                return result['offense'], result['defense']
        
        # Prepare features
        features = self._prepare_features(player_ids, player_stats)
        features = features.reshape(1, -1)
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Make predictions
        offense_pred = self.offense_model.predict(features_scaled)[0]
        defense_pred = self.defense_model.predict(features_scaled)[0]
        
        return float(offense_pred), float(defense_pred)
    
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
        avg_stats = lineup_stats.groupby('player_id').mean(numeric_only=True).mean()
        
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
    
    def generate_training_data(self, player_stats: pd.DataFrame, num_samples: int = 500) -> Tuple[List[List[str]], List[float], List[float]]:
        """
        Generate synthetic training data for model development.
        
        Args:
            player_stats: DataFrame containing player statistics
            num_samples: Number of lineup samples to generate
            
        Returns:
            Tuple of (lineups, offensive_ratings, defensive_ratings)
        """
        # Get all player IDs
        if player_stats.empty:
            return [], [], []
            
        all_player_ids = player_stats['player_id'].unique()
        
        # Generate random lineups
        lineups = []
        offensive_ratings = []
        defensive_ratings = []
        
        for _ in range(num_samples):
            # Randomly select 5 players
            lineup = np.random.choice(all_player_ids, size=5, replace=False).tolist()
            lineups.append(lineup)
            
            # Get lineup stats
            lineup_stats = player_stats[player_stats['player_id'].isin(lineup)]
            
            if lineup_stats.empty:
                # Skip empty lineups
                continue
                
            # Calculate average stats
            avg_stats = lineup_stats.groupby('player_id').mean(numeric_only=True).mean()
            
            # Calculate offensive rating (scoring ability)
            off_rating = 0.0
            if 'pts' in avg_stats:
                off_rating += avg_stats['pts'] * 2.5
            if 'ast' in avg_stats:
                off_rating += avg_stats['ast'] * 5
            if 'fg_pct' in avg_stats:
                off_rating += avg_stats['fg_pct'] * 50
            if 'fg3_pct' in avg_stats:
                off_rating += avg_stats['fg3_pct'] * 60
                
            # Normalize to 0-100 scale
            off_rating = min(100, off_rating / 50 * 100)
            
            # Calculate defensive rating (defensive ability)
            def_rating = 0.0
            if 'stl' in avg_stats:
                def_rating += avg_stats['stl'] * 15
            if 'blk' in avg_stats:
                def_rating += avg_stats['blk'] * 15
            if 'reb' in avg_stats:
                def_rating += avg_stats['reb'] * 3
                
            # Normalize to 0-100 scale
            def_rating = min(100, def_rating / 30 * 100)
            
            # Add some noise to make the data more realistic
            off_rating += np.random.normal(0, 5)  # Add noise with std=5
            def_rating += np.random.normal(0, 5)  # Add noise with std=5
            
            # Clip to 0-100 range
            off_rating = max(0, min(100, off_rating))
            def_rating = max(0, min(100, def_rating))
            
            offensive_ratings.append(off_rating)
            defensive_ratings.append(def_rating)
        
        return lineups, offensive_ratings, defensive_ratings
    
    def get_feature_importance(self) -> pd.DataFrame:
        """
        Get feature importance from trained models.
        
        Returns:
            DataFrame with feature importance for offense and defense models
        """
        if not self.model_trained and not self.load_models():
            # No models available
            return pd.DataFrame()
        
        # Get feature importance
        offense_importance = self.offense_model.feature_importances_
        defense_importance = self.defense_model.feature_importances_
        
        # Create DataFrame
        importance_df = pd.DataFrame({
            'Feature': self.feature_names,
            'Offense Importance': offense_importance,
            'Defense Importance': defense_importance
        })
        
        return importance_df
    
    def predict_best_substitution(self, current_lineup: List[str], bench_players: List[str], 
                               player_stats: pd.DataFrame) -> Dict[str, Any]:
        """
        Find the best substitution to improve lineup performance.
        
        Args:
            current_lineup: Current lineup (list of player IDs)
            bench_players: Available bench players (list of player IDs)
            player_stats: DataFrame containing player statistics
            
        Returns:
            Dictionary with substitution details
        """
        if not self.model_trained and not self.load_models():
            return None
            
        if len(current_lineup) < 5 or not bench_players:
            return None
            
        # Get current lineup ratings
        current_off, current_def = self.predict(current_lineup, player_stats)
        current_overall = (current_off + current_def) / 2
        
        best_improvement = -1
        best_substitution = None
        
        # Try substituting each player in the lineup with each bench player
        for i, starter in enumerate(current_lineup):
            for bench in bench_players:
                # Create new lineup with the substitution
                new_lineup = current_lineup.copy()
                new_lineup[i] = bench
                
                # Predict ratings for new lineup
                new_off, new_def = self.predict(new_lineup, player_stats)
                new_overall = (new_off + new_def) / 2
                
                # Calculate improvement
                overall_improvement = new_overall - current_overall
                
                # Check if this is the best improvement so far
                if overall_improvement > best_improvement:
                    best_improvement = overall_improvement
                    best_substitution = {
                        'replace_player_id': starter,
                        'with_player_id': bench,
                        'overall_improvement': overall_improvement,
                        'offense_improvement': new_off - current_off,
                        'defense_improvement': new_def - current_def
                    }
        
        return best_substitution 

def train_lineup_prediction_model(player_stats, target_metric, n_estimators=100, max_depth=10):
    """
    Train a lineup prediction model based on player statistics.
    
    Parameters:
    -----------
    player_stats : pandas.DataFrame
        DataFrame containing player statistics
    target_metric : str
        The metric to predict (pts, reb, ast, stl, blk)
    n_estimators : int, default=100
        Number of trees in the random forest
    max_depth : int, default=10
        Maximum depth of the trees
        
    Returns:
    --------
    tuple
        (model, X_test, y_test, top_features, feature_importances, mse, y_pred)
    """
    # Ensure we have enough data
    if len(player_stats) < 50:
        # Generate more training data by resampling
        player_stats = player_stats.sample(n=200, replace=True)
    
    # Select features - use all numeric columns except player_id and target
    features = player_stats.select_dtypes(include=['number']).columns.tolist()
    features = [f for f in features if f != 'player_id' and f != target_metric]
    
    # Prepare features and target
    X = player_stats[features]
    y = player_stats[target_metric]
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    
    # Train the model
    model = RandomForestRegressor(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # Get feature importance
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    # Get top 10 features
    top_indices = indices[:10]
    top_features = [features[i] for i in top_indices]
    feature_importances = [importances[i] for i in top_indices]
    
    # Evaluate the model
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    
    return model, X_test, y_test, top_features, feature_importances, mse, y_pred 