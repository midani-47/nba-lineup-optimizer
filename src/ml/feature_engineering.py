import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple

class FeatureEngineer:
    """
    Class for feature engineering operations on NBA player data.
    """
    
    def __init__(self):
        """Initialize the feature engineer"""
        self.feature_columns = []
        
    def prepare_player_features(self, player_stats: pd.DataFrame) -> pd.DataFrame:
        """
        Create player features from raw statistics.
        
        Args:
            player_stats: DataFrame with player statistics
            
        Returns:
            DataFrame with engineered features
        """
        if player_stats.empty:
            return pd.DataFrame()
        
        # Create a copy to avoid modifying the original
        df = player_stats.copy()
        
        # Handle missing values
        for col in df.select_dtypes(include=[np.number]).columns:
            df[col] = df[col].fillna(df[col].median())
        
        # Basic efficiency metrics
        if 'pts' in df.columns and 'fga' in df.columns:
            df['points_per_shot'] = df['pts'] / df['fga'].replace(0, 1)
            
        if all(col in df.columns for col in ['pts', 'reb', 'ast', 'stl', 'blk', 'tov']):
            # Create composite metrics
            df['offensive_impact'] = (df['pts'] * 0.5 + df['ast'] * 0.3 + 
                                      df['orb'] * 0.2 if 'orb' in df.columns else 0)
            
            df['defensive_impact'] = (df['stl'] * 0.4 + df['blk'] * 0.4 + 
                                     df['drb'] * 0.2 if 'drb' in df.columns else df['reb'] * 0.2)
            
            # Efficiency metrics
            df['efficiency'] = (df['pts'] + df['reb'] + df['ast'] + df['stl'] + df['blk']) - \
                               (df['tov'] + (df['fga'] - df['fgm']) if 'fgm' in df.columns else 0)
        
        # Shooting efficiency
        if 'fg_pct' in df.columns and 'fg3_pct' in df.columns:
            df['shooting_value'] = df['fg_pct'] * 2 + df['fg3_pct'] * 1.5
        
        # Normalize features to 0-1 range for machine learning
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].max() > df[col].min():
                df[f'{col}_norm'] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
            else:
                df[f'{col}_norm'] = 0
        
        # Store feature columns for future reference
        self.feature_columns = [col for col in df.columns if col.endswith('_norm')]
        
        return df
    
    def generate_lineup_features(self, player_ids: List[str], player_stats: pd.DataFrame) -> Dict[str, float]:
        """
        Generate features for a lineup based on player statistics.
        
        Args:
            player_ids: List of player IDs in the lineup
            player_stats: DataFrame with player statistics including engineered features
            
        Returns:
            Dictionary with lineup features
        """
        # Filter relevant players
        lineup_stats = player_stats[player_stats['player_id'].isin(player_ids)]
        
        if lineup_stats.empty:
            return {}
        
        # Create feature dict
        features = {}
        
        # Basic aggregated features
        for col in self.feature_columns:
            features[f'avg_{col}'] = lineup_stats[col].mean()
            features[f'max_{col}'] = lineup_stats[col].max()
            features[f'min_{col}'] = lineup_stats[col].min()
            features[f'std_{col}'] = lineup_stats[col].std()
        
        # Advanced lineup features
        
        # Positional balance (if position data is available)
        if 'position' in player_stats.columns:
            position_counts = lineup_stats['position'].value_counts().to_dict()
            
            # Position diversity score
            num_positions = len(position_counts)
            features['position_diversity'] = num_positions / 5.0
            
            # Guard-forward-center balance
            features['guards_ratio'] = position_counts.get('PG', 0) + position_counts.get('SG', 0) / 5.0
            features['forwards_ratio'] = position_counts.get('SF', 0) + position_counts.get('PF', 0) / 5.0
            features['centers_ratio'] = position_counts.get('C', 0) / 5.0
        
        # Offensive vs defensive balance
        if 'offensive_impact' in lineup_stats.columns and 'defensive_impact' in lineup_stats.columns:
            features['offense_defense_ratio'] = (lineup_stats['offensive_impact'].sum() / 
                                               lineup_stats['defensive_impact'].sum() 
                                               if lineup_stats['defensive_impact'].sum() > 0 else 1.0)
        
        # Experience balance (if available)
        if 'experience' in lineup_stats.columns:
            features['avg_experience'] = lineup_stats['experience'].mean()
            features['max_experience'] = lineup_stats['experience'].max()
            features['experience_diversity'] = lineup_stats['experience'].std() / lineup_stats['experience'].mean() if lineup_stats['experience'].mean() > 0 else 0
        
        return features
    
    def extract_important_features(self, player_stats: pd.DataFrame) -> pd.DataFrame:
        """
        Extract the most important features for prediction.
        
        Args:
            player_stats: DataFrame with player statistics
            
        Returns:
            DataFrame with the most important features
        """
        # List of important raw statistics for basketball performance
        important_stats = ['pts', 'reb', 'ast', 'stl', 'blk', 'tov', 'fg_pct', 'fg3_pct', 'ft_pct']
        
        # Filter by important stats if they exist
        existing_stats = [stat for stat in important_stats if stat in player_stats.columns]
        
        # Create advanced features
        df = self.prepare_player_features(player_stats)
        
        # Select the most important features
        important_features = []
        
        # Add normalized versions of important statistics
        for stat in existing_stats:
            normalized_stat = f'{stat}_norm'
            if normalized_stat in df.columns:
                important_features.append(normalized_stat)
        
        # Add engineered features if they exist
        engineered_features = ['offensive_impact', 'defensive_impact', 'efficiency', 'shooting_value']
        for feature in engineered_features:
            if feature in df.columns:
                important_features.append(feature)
        
        # Select columns
        if important_features:
            result = df[['player_id'] + important_features]
        else:
            # If no important features found, return basic stats
            result = df[['player_id'] + existing_stats]
        
        return result
    
    def generate_player_similarity_matrix(self, player_stats: pd.DataFrame) -> pd.DataFrame:
        """
        Generate a player similarity matrix based on statistical features.
        
        Args:
            player_stats: DataFrame with player statistics
            
        Returns:
            DataFrame with player similarity scores
        """
        from sklearn.metrics.pairwise import cosine_similarity
        
        # Prepare features
        features_df = self.extract_important_features(player_stats)
        
        if 'player_id' not in features_df.columns or len(features_df) < 2:
            return pd.DataFrame()
        
        # Set player_id as index
        features_df = features_df.set_index('player_id')
        
        # Calculate similarity matrix
        similarity_matrix = cosine_similarity(features_df)
        
        # Convert to DataFrame
        similarity_df = pd.DataFrame(
            similarity_matrix, 
            index=features_df.index, 
            columns=features_df.index
        )
        
        return similarity_df
    
    def get_complementary_players(self, player_id: str, player_stats: pd.DataFrame, 
                                 n: int = 5) -> List[Tuple[str, float]]:
        """
        Find complementary players that would play well with a given player.
        
        Args:
            player_id: ID of the player to find complements for
            player_stats: DataFrame with player statistics
            n: Number of complementary players to return
            
        Returns:
            List of tuples (player_id, complementary_score)
        """
        # Get features for all players
        features_df = self.extract_important_features(player_stats)
        
        if 'player_id' not in features_df.columns or player_id not in features_df['player_id'].values:
            return []
        
        # Get the player's stats
        player_features = features_df[features_df['player_id'] == player_id].iloc[0]
        
        # Remove player_id from features for calculation
        feature_cols = [col for col in features_df.columns if col != 'player_id']
        
        # Initialize complementary scores
        complementary_scores = []
        
        # Calculate complementary score for each player
        for idx, row in features_df.iterrows():
            if row['player_id'] == player_id:
                continue
                
            other_player = row
            
            # Calculate complementary score based on complementary skills
            # (Players are complementary if they are strong in areas where the original player is weak)
            complementary_score = 0
            
            for col in feature_cols:
                # If a player is weak in a stat, we want someone strong in it
                if player_features[col] < 0.5:  # Below average
                    complementary_score += (other_player[col] - 0.5) * 2
                # If a player is already strong, we don't need as much strength there
                else:
                    complementary_score += (other_player[col] - 0.5) * 0.5
            
            complementary_scores.append((row['player_id'], complementary_score))
        
        # Sort by score (descending) and get top n
        complementary_scores.sort(key=lambda x: x[1], reverse=True)
        
        return complementary_scores[:n] 