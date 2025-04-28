import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from .metrics import (
    calculate_lineup_rating,
    get_lineup_strengths_weaknesses,
    compare_lineups
)

class LineupAnalyzer:
    """
    Analyzer for NBA lineups that provides insights and comparisons.
    """
    
    def __init__(self, player_stats: pd.DataFrame, player_info: pd.DataFrame):
        """
        Initialize the lineup analyzer with player data.
        
        Args:
            player_stats: DataFrame containing player statistics
            player_info: DataFrame containing player information
        """
        self.player_stats = player_stats
        self.player_info = player_info
    
    def analyze_lineup(self, player_ids: List[str]) -> Dict[str, Any]:
        """
        Analyze a single lineup and return detailed ratings and insights.
        
        Args:
            player_ids: List of player IDs in the lineup
            
        Returns:
            Dictionary containing ratings and analysis
        """
        if len(player_ids) < 1:
            return {
                "error": "Lineup must contain at least one player"
            }
        
        # Get basic player info for the lineup
        lineup_info = self.player_info[self.player_info['player_id'].isin(player_ids)]
        
        # Calculate ratings
        ratings = calculate_lineup_rating(player_ids, self.player_stats, self.player_info)
        
        # Get strengths and weaknesses
        strengths, weaknesses = get_lineup_strengths_weaknesses(ratings)
        
        # Check position distribution
        positions = lineup_info['position'].tolist() if not lineup_info.empty else []
        position_counts = {}
        for pos in positions:
            if pos in position_counts:
                position_counts[pos] += 1
            else:
                position_counts[pos] = 1
        
        # Position categories
        position_categories = {
            'PG': 'Guard',
            'SG': 'Guard',
            'SF': 'Forward',
            'PF': 'Forward',
            'C': 'Center'
        }
        
        # Calculate category counts
        category_counts = {'Guard': 0, 'Forward': 0, 'Center': 0}
        for pos, count in position_counts.items():
            if pos in position_categories:
                category = position_categories[pos]
                category_counts[category] += count
        
        # Check for position balance
        position_balanced = (
            category_counts['Guard'] >= 1 and 
            category_counts['Forward'] >= 1 and 
            category_counts['Center'] >= 1
        )
        
        # Top statistical performers
        lineup_stats = self.player_stats[self.player_stats['player_id'].isin(player_ids)]
        
        # Get player names
        player_names = {}
        if not lineup_info.empty and 'player_name' in lineup_info.columns:
            for _, player in lineup_info.iterrows():
                player_names[player['player_id']] = player['player_name']
        
        # Create analysis result
        result = {
            "lineup_size": len(player_ids),
            "ratings": ratings,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "position_balanced": position_balanced,
            "position_distribution": category_counts,
            "player_ids": player_ids,
            "player_names": player_names
        }
        
        return result
    
    def compare_lineups(self, lineup1_ids: List[str], lineup2_ids: List[str]) -> Dict[str, Any]:
        """
        Compare two lineups and provide detailed analysis of their differences.
        
        Args:
            lineup1_ids: List of player IDs for first lineup
            lineup2_ids: List of player IDs for second lineup
            
        Returns:
            Dictionary with comparison results
        """
        if len(lineup1_ids) < 1 or len(lineup2_ids) < 1:
            return {
                "error": "Both lineups must contain at least one player"
            }
        
        # Get player names for both lineups
        lineup1_info = self.player_info[self.player_info['player_id'].isin(lineup1_ids)]
        lineup2_info = self.player_info[self.player_info['player_id'].isin(lineup2_ids)]
        
        lineup1_names = {}
        lineup2_names = {}
        
        if not lineup1_info.empty and 'player_name' in lineup1_info.columns:
            for _, player in lineup1_info.iterrows():
                lineup1_names[player['player_id']] = player['player_name']
                
        if not lineup2_info.empty and 'player_name' in lineup2_info.columns:
            for _, player in lineup2_info.iterrows():
                lineup2_names[player['player_id']] = player['player_name']
        
        # Get comparison results
        comparison = compare_lineups(lineup1_ids, lineup2_ids, self.player_stats, self.player_info)
        
        # Add player names to the result
        comparison['lineup1_names'] = lineup1_names
        comparison['lineup2_names'] = lineup2_names
        
        return comparison
    
    def find_optimal_replacements(self, 
                                 lineup_ids: List[str], 
                                 candidates: List[str], 
                                 replacement_count: int = 1,
                                 optimize_for: str = 'overall') -> List[Dict[str, Any]]:
        """
        Find optimal player replacements to improve a lineup.
        
        Args:
            lineup_ids: List of player IDs in the current lineup
            candidates: List of player IDs to consider as replacements
            replacement_count: Number of players to replace (default: 1)
            optimize_for: Rating component to optimize ('overall', 'offense', 'defense', etc.)
            
        Returns:
            List of suggested replacements with ratings improvement
        """
        if len(lineup_ids) < 1:
            return [{
                "error": "Lineup must contain at least one player"
            }]
        
        if replacement_count < 1 or replacement_count > len(lineup_ids):
            replacement_count = 1
        
        # Calculate current lineup rating
        current_ratings = calculate_lineup_rating(lineup_ids, self.player_stats, self.player_info)
        current_value = current_ratings.get(optimize_for, 0)
        
        # Test all possible replacements
        replacements = []
        
        # For simplicity, we'll just consider single replacements first
        if replacement_count == 1:
            for player_to_replace in lineup_ids:
                for candidate in candidates:
                    if candidate not in lineup_ids:
                        # Create new lineup with the replacement
                        new_lineup = [p if p != player_to_replace else candidate for p in lineup_ids]
                        
                        # Calculate new rating
                        new_ratings = calculate_lineup_rating(new_lineup, self.player_stats, self.player_info)
                        new_value = new_ratings.get(optimize_for, 0)
                        
                        # Calculate improvement
                        improvement = new_value - current_value
                        
                        # Add to results if there's an improvement
                        if improvement > 0:
                            # Get player names
                            out_player_name = ""
                            in_player_name = ""
                            
                            player_out_info = self.player_info[self.player_info['player_id'] == player_to_replace]
                            player_in_info = self.player_info[self.player_info['player_id'] == candidate]
                            
                            if not player_out_info.empty and 'player_name' in player_out_info.columns:
                                out_player_name = player_out_info.iloc[0]['player_name']
                                
                            if not player_in_info.empty and 'player_name' in player_in_info.columns:
                                in_player_name = player_in_info.iloc[0]['player_name']
                            
                            replacements.append({
                                'player_out_id': player_to_replace,
                                'player_out_name': out_player_name,
                                'player_in_id': candidate,
                                'player_in_name': in_player_name,
                                'improvement': improvement,
                                'new_ratings': new_ratings,
                                'old_ratings': current_ratings
                            })
        
        # Sort by improvement (highest first)
        replacements.sort(key=lambda x: x['improvement'], reverse=True)
        
        # Return top suggestions (max 5)
        return replacements[:5]
    
    def get_player_compatibility(self, player_id: str, lineup_ids: List[str]) -> Dict[str, Any]:
        """
        Evaluate how compatible a player is with an existing lineup.
        
        Args:
            player_id: ID of the player to evaluate
            lineup_ids: List of player IDs in the existing lineup
            
        Returns:
            Dictionary with compatibility analysis
        """
        if player_id in lineup_ids:
            return {
                "error": "Player is already in the lineup"
            }
        
        # Calculate current lineup rating
        current_ratings = calculate_lineup_rating(lineup_ids, self.player_stats, self.player_info)
        
        # Calculate new lineup rating with the player added
        new_lineup = lineup_ids + [player_id]
        new_ratings = calculate_lineup_rating(new_lineup, self.player_stats, self.player_info)
        
        # Calculate differences
        differences = {
            k: new_ratings[k] - current_ratings[k] for k in current_ratings.keys()
        }
        
        # Get player info
        player_info = self.player_info[self.player_info['player_id'] == player_id]
        player_name = ""
        player_position = ""
        
        if not player_info.empty:
            if 'player_name' in player_info.columns:
                player_name = player_info.iloc[0]['player_name']
            if 'position' in player_info.columns:
                player_position = player_info.iloc[0]['position']
        
        # Determine compatibility level
        compatibility_score = differences.get('compatibility', 0)
        if compatibility_score > 10:
            compatibility_level = "Excellent"
        elif compatibility_score > 5:
            compatibility_level = "Good"
        elif compatibility_score > 0:
            compatibility_level = "Fair"
        elif compatibility_score > -5:
            compatibility_level = "Poor"
        else:
            compatibility_level = "Bad"
        
        # Get impact on team strengths and weaknesses
        _, old_weaknesses = get_lineup_strengths_weaknesses(current_ratings)
        new_strengths, new_weaknesses = get_lineup_strengths_weaknesses(new_ratings)
        
        # Find weaknesses addressed
        weaknesses_addressed = [w for w in old_weaknesses if w not in new_weaknesses]
        
        return {
            'player_id': player_id,
            'player_name': player_name,
            'player_position': player_position,
            'compatibility_level': compatibility_level,
            'compatibility_score': compatibility_score,
            'impact': differences,
            'weaknesses_addressed': weaknesses_addressed,
            'new_strengths': new_strengths
        } 