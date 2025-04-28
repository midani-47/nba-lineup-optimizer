import pandas as pd
import numpy as np
from itertools import combinations
from sklearn.preprocessing import MinMaxScaler
from typing import List, Tuple, Dict, Any, Optional, Set

def optimize_lineup_for_scoring(player_ids: List[str], player_stats: pd.DataFrame, player_info: pd.DataFrame) -> List[str]:
    """
    Optimize a lineup for scoring performance.
    
    Args:
        player_ids: List of player IDs to choose from
        player_stats: DataFrame containing player statistics
        player_info: DataFrame containing player information
        
    Returns:
        List of optimized player IDs (5 players)
    """
    # Validate inputs
    if len(player_ids) < 5:
        return player_ids  # Not enough players to optimize
    
    # Get stats for the selected players
    player_stat_filtered = player_stats[player_stats['player_id'].isin(player_ids)]
    player_info_filtered = player_info[player_info['player_id'].isin(player_ids)]
    
    # Check if we have enough data
    if player_stat_filtered.empty or player_info_filtered.empty:
        return player_ids[:5]  # Return first 5 players if no data available
    
    # Check if the required columns exist
    required_columns = ['pts', 'ast', 'fg3_pct']
    if not all(col in player_stat_filtered.columns for col in required_columns):
        # If missing columns, create default values (0 for missing stats)
        for col in required_columns:
            if col not in player_stat_filtered.columns:
                player_stat_filtered[col] = 0.0
    
    # Calculate average stats per player
    avg_stats = player_stat_filtered.groupby('player_id').mean(numeric_only=True).reset_index()
    
    # Create a scoring metric based on offensive contribution
    # Points + (Assists * 2.5) + (3P% * 50)
    avg_stats['scoring_metric'] = avg_stats['pts'] + (avg_stats['ast'] * 2.5) + (avg_stats['fg3_pct'] * 50)
    
    # Sort players by scoring metric
    sorted_players = avg_stats.sort_values('scoring_metric', ascending=False)
    
    # Get the top 5 players by scoring metric
    top_players = sorted_players.head(5)['player_id'].tolist()
    
    # Check if we have a balanced lineup (at least one player per position category)
    position_categories = {'G': ['PG', 'SG'], 'F': ['SF', 'PF'], 'C': ['C']}
    
    # If position column doesn't exist, return top players
    if 'position' not in player_info_filtered.columns:
        return top_players
    
    # Handle missing position values
    player_info_filtered['position'] = player_info_filtered['position'].fillna('F')  # Default to Forward if missing
    
    # Get positions of top players
    top_players_positions = player_info_filtered[player_info_filtered['player_id'].isin(top_players)]['position'].tolist()
    
    # Check if we have all position categories
    has_guard = any(pos in position_categories['G'] for pos in top_players_positions)
    has_forward = any(pos in position_categories['F'] for pos in top_players_positions)
    has_center = any(pos in position_categories['C'] for pos in top_players_positions)
    
    # If lineup is not balanced, replace players to ensure balance
    if not (has_guard and has_forward and has_center):
        # Start with top players
        optimized_lineup = []
        
        # Add to optimized lineup
        for player_id in top_players:
            optimized_lineup.append(player_id)
        
        # Find what positions we're missing
        missing_categories = []
        if not has_guard:
            missing_categories.append('G')
        if not has_forward:
            missing_categories.append('F')
        if not has_center:
            missing_categories.append('C')
        
        # For each missing category, replace the lowest scoring player with the highest scoring player of that category
        for category in missing_categories:
            # Find the lowest scoring player in the lineup
            try:
                lowest_scorer_id = min(optimized_lineup, key=lambda pid: float(avg_stats[avg_stats['player_id'] == pid]['scoring_metric'].values[0]) if len(avg_stats[avg_stats['player_id'] == pid]['scoring_metric'].values) > 0 else 0)
                
                # Find the highest scoring player of the missing category
                category_positions = position_categories[category]
                category_players = player_info_filtered[player_info_filtered['position'].isin(category_positions)]['player_id'].tolist()
                
                # If we have players in this category, find the best one
                if category_players:
                    # Get best player of this category by scoring metric
                    category_stats = avg_stats[avg_stats['player_id'].isin(category_players)]
                    if not category_stats.empty:
                        best_category_player = category_stats.sort_values('scoring_metric', ascending=False).iloc[0]['player_id']
                        
                        # Replace the lowest scorer with the best category player if not already in lineup
                        if best_category_player not in optimized_lineup:
                            optimized_lineup.remove(lowest_scorer_id)
                            optimized_lineup.append(best_category_player)
            except (ValueError, IndexError):
                # Skip if there's an issue finding the players
                continue
        
        # Ensure we have exactly 5 players
        if len(optimized_lineup) > 5:
            return optimized_lineup[:5]
        elif len(optimized_lineup) < 5:
            # Add more players from the original list to reach 5
            remaining_players = [p for p in player_ids if p not in optimized_lineup]
            optimized_lineup.extend(remaining_players[:5-len(optimized_lineup)])
            
        return optimized_lineup
    
    return top_players

def optimize_lineup_for_defense(player_ids: List[str], player_stats: pd.DataFrame, player_info: pd.DataFrame) -> List[str]:
    """
    Optimize a lineup for defensive performance.
    
    Args:
        player_ids: List of player IDs to choose from
        player_stats: DataFrame containing player statistics
        player_info: DataFrame containing player information
        
    Returns:
        List of optimized player IDs (5 players)
    """
    # Validate inputs
    if len(player_ids) < 5:
        return player_ids  # Not enough players to optimize
    
    # Get stats for the selected players
    player_stat_filtered = player_stats[player_stats['player_id'].isin(player_ids)]
    player_info_filtered = player_info[player_info['player_id'].isin(player_ids)]
    
    # Check if we have enough data
    if player_stat_filtered.empty or player_info_filtered.empty:
        return player_ids[:5]  # Return first 5 players if no data available
    
    # Check if the required columns exist
    required_columns = ['stl', 'blk', 'reb']
    if not all(col in player_stat_filtered.columns for col in required_columns):
        # If missing columns, create default values (0 for missing stats)
        for col in required_columns:
            if col not in player_stat_filtered.columns:
                player_stat_filtered[col] = 0.0
    
    # Calculate average stats per player
    avg_stats = player_stat_filtered.groupby('player_id').mean(numeric_only=True).reset_index()
    
    # Create a defensive metric based on defensive contribution
    # (Steals * 2) + (Blocks * 2) + (Rebounds * 1.2)
    avg_stats['defensive_metric'] = (avg_stats['stl'] * 2) + (avg_stats['blk'] * 2) + (avg_stats['reb'] * 1.2)
    
    # Sort players by defensive metric
    sorted_players = avg_stats.sort_values('defensive_metric', ascending=False)
    
    # Get the top 5 players by defensive metric
    top_players = sorted_players.head(5)['player_id'].tolist()
    
    # Check if we have a balanced lineup (at least one player per position category)
    position_categories = {'G': ['PG', 'SG'], 'F': ['SF', 'PF'], 'C': ['C']}
    
    # If position column doesn't exist, return top players
    if 'position' not in player_info_filtered.columns:
        return top_players
    
    # Handle missing position values
    player_info_filtered['position'] = player_info_filtered['position'].fillna('F')  # Default to Forward if missing
    
    # Get positions of top players
    top_players_positions = player_info_filtered[player_info_filtered['player_id'].isin(top_players)]['position'].tolist()
    
    # Check if we have all position categories
    has_guard = any(pos in position_categories['G'] for pos in top_players_positions)
    has_forward = any(pos in position_categories['F'] for pos in top_players_positions)
    has_center = any(pos in position_categories['C'] for pos in top_players_positions)
    
    # If lineup is not balanced, replace players to ensure balance
    if not (has_guard and has_forward and has_center):
        # Start with top players
        optimized_lineup = []
        
        # Add to optimized lineup
        for player_id in top_players:
            optimized_lineup.append(player_id)
        
        # Find what positions we're missing
        missing_categories = []
        if not has_guard:
            missing_categories.append('G')
        if not has_forward:
            missing_categories.append('F')
        if not has_center:
            missing_categories.append('C')
        
        # For each missing category, replace the lowest defensive player with the highest defensive player of that category
        for category in missing_categories:
            try:
                # Find the lowest defensive player in the lineup
                lowest_defender_id = min(optimized_lineup, key=lambda pid: float(avg_stats[avg_stats['player_id'] == pid]['defensive_metric'].values[0]) if len(avg_stats[avg_stats['player_id'] == pid]['defensive_metric'].values) > 0 else 0)
                
                # Find the highest defensive player of the missing category
                category_positions = position_categories[category]
                category_players = player_info_filtered[player_info_filtered['position'].isin(category_positions)]['player_id'].tolist()
                
                # If we have players in this category, find the best one
                if category_players:
                    # Get best player of this category by defensive metric
                    category_stats = avg_stats[avg_stats['player_id'].isin(category_players)]
                    if not category_stats.empty:
                        best_category_player = category_stats.sort_values('defensive_metric', ascending=False).iloc[0]['player_id']
                        
                        # Replace the lowest defender with the best category player if not already in lineup
                        if best_category_player not in optimized_lineup:
                            optimized_lineup.remove(lowest_defender_id)
                            optimized_lineup.append(best_category_player)
            except (ValueError, IndexError):
                # Skip if there's an issue finding the players
                continue
        
        # Ensure we have exactly 5 players
        if len(optimized_lineup) > 5:
            return optimized_lineup[:5]
        elif len(optimized_lineup) < 5:
            # Add more players from the original list to reach 5
            remaining_players = [p for p in player_ids if p not in optimized_lineup]
            optimized_lineup.extend(remaining_players[:5-len(optimized_lineup)])
            
        return optimized_lineup
    
    return top_players

def optimize_lineup_for_balanced(player_ids: List[str], player_stats: pd.DataFrame, player_info: pd.DataFrame) -> List[str]:
    """
    Optimize a lineup for balanced performance (both offense and defense).
    
    Args:
        player_ids: List of player IDs to choose from
        player_stats: DataFrame containing player statistics
        player_info: DataFrame containing player information
        
    Returns:
        List of optimized player IDs (5 players)
    """
    # Validate inputs
    if len(player_ids) < 5:
        return player_ids  # Not enough players to optimize
    
    # Get stats for the selected players
    player_stat_filtered = player_stats[player_stats['player_id'].isin(player_ids)]
    player_info_filtered = player_info[player_info['player_id'].isin(player_ids)]
    
    # Check if we have enough data
    if player_stat_filtered.empty or player_info_filtered.empty:
        return player_ids[:5]  # Return first 5 players if no data available
    
    # Check if the required columns exist
    required_columns = ['pts', 'ast', 'stl', 'blk', 'reb', 'fg3_pct']
    if not all(col in player_stat_filtered.columns for col in required_columns):
        # If missing columns, create default values (0 for missing stats)
        for col in required_columns:
            if col not in player_stat_filtered.columns:
                player_stat_filtered[col] = 0.0
    
    # Calculate average stats per player
    avg_stats = player_stat_filtered.groupby('player_id').mean(numeric_only=True).reset_index()
    
    # Create offensive and defensive metrics
    avg_stats['offensive_metric'] = avg_stats['pts'] + (avg_stats['ast'] * 2.5) + (avg_stats.get('fg3_pct', 0) * 50)
    avg_stats['defensive_metric'] = (avg_stats['stl'] * 2) + (avg_stats['blk'] * 2) + (avg_stats['reb'] * 1.2)
    
    # Create balanced metric (equal weight to offense and defense)
    # Normalize both metrics to 0-1 scale first to make them comparable
    scaler = MinMaxScaler()
    if len(avg_stats) > 1:  # Need at least 2 players for scaling
        try:
            # Scale both metrics to 0-1 range
            avg_stats[['offensive_metric_scaled', 'defensive_metric_scaled']] = scaler.fit_transform(
                avg_stats[['offensive_metric', 'defensive_metric']])
            
            # Combined metric is average of scaled metrics
            avg_stats['balanced_metric'] = (avg_stats['offensive_metric_scaled'] + 
                                           avg_stats['defensive_metric_scaled']) / 2
        except (ValueError, TypeError):
            # If scaling fails, use simple average of raw metrics
            avg_stats['balanced_metric'] = (avg_stats['offensive_metric'] + avg_stats['defensive_metric']) / 2
    else:
        # If only one player, use simple average
        avg_stats['balanced_metric'] = (avg_stats['offensive_metric'] + avg_stats['defensive_metric']) / 2
    
    # Sort players by balanced metric
    sorted_players = avg_stats.sort_values('balanced_metric', ascending=False)
    
    # Get the top 5 players by balanced metric
    top_players = sorted_players.head(5)['player_id'].tolist()
    
    # Check if we have a balanced lineup (at least one player per position category)
    position_categories = {'G': ['PG', 'SG'], 'F': ['SF', 'PF'], 'C': ['C']}
    
    # If position column doesn't exist, return top players
    if 'position' not in player_info_filtered.columns:
        return top_players
    
    # Handle missing position values
    player_info_filtered['position'] = player_info_filtered['position'].fillna('F')  # Default to Forward if missing
    
    # Get positions of top players
    top_players_positions = player_info_filtered[player_info_filtered['player_id'].isin(top_players)]['position'].tolist()
    
    # Check if we have all position categories
    has_guard = any(pos in position_categories['G'] for pos in top_players_positions)
    has_forward = any(pos in position_categories['F'] for pos in top_players_positions)
    has_center = any(pos in position_categories['C'] for pos in top_players_positions)
    
    # If lineup is not balanced, replace players to ensure balance
    if not (has_guard and has_forward and has_center):
        # Start with top players
        optimized_lineup = []
        
        # Add to optimized lineup
        for player_id in top_players:
            optimized_lineup.append(player_id)
        
        # Find what positions we're missing
        missing_categories = []
        if not has_guard:
            missing_categories.append('G')
        if not has_forward:
            missing_categories.append('F')
        if not has_center:
            missing_categories.append('C')
        
        # For each missing category, replace the lowest balanced metric player with the highest balanced metric player of that category
        for category in missing_categories:
            try:
                # Find the lowest balanced metric player in the lineup
                lowest_balanced_id = min(optimized_lineup, key=lambda pid: float(avg_stats[avg_stats['player_id'] == pid]['balanced_metric'].values[0]) if len(avg_stats[avg_stats['player_id'] == pid]['balanced_metric'].values) > 0 else 0)
                
                # Find the highest balanced metric player of the missing category
                category_positions = position_categories[category]
                category_players = player_info_filtered[player_info_filtered['position'].isin(category_positions)]['player_id'].tolist()
                
                # If we have players in this category, find the best one
                if category_players:
                    # Get best player of this category by balanced metric
                    category_stats = avg_stats[avg_stats['player_id'].isin(category_players)]
                    if not category_stats.empty:
                        best_category_player = category_stats.sort_values('balanced_metric', ascending=False).iloc[0]['player_id']
                        
                        # Replace the lowest balanced metric player with the best category player if not already in lineup
                        if best_category_player not in optimized_lineup:
                            optimized_lineup.remove(lowest_balanced_id)
                            optimized_lineup.append(best_category_player)
            except (ValueError, IndexError):
                # Skip if there's an issue finding the players
                continue
        
        # Ensure we have exactly 5 players
        if len(optimized_lineup) > 5:
            return optimized_lineup[:5]
        elif len(optimized_lineup) < 5:
            # Add more players from the original list to reach 5
            remaining_players = [p for p in player_ids if p not in optimized_lineup]
            optimized_lineup.extend(remaining_players[:5-len(optimized_lineup)])
            
        return optimized_lineup
    
    return top_players

def calculate_lineup_chemistry(player_ids: List[str], player_info: pd.DataFrame) -> float:
    """
    Calculate the chemistry score for a lineup based on player positions and attributes.
    
    Args:
        player_ids: List of player IDs in the lineup
        player_info: DataFrame containing player information
        
    Returns:
        Chemistry score from 0 to 100
    """
    # Default chemistry score if no data available
    if len(player_ids) < 2 or player_info.empty:
        return 50.0
    
    # Get info for the selected players
    lineup_info = player_info[player_info['player_id'].isin(player_ids)]
    
    # If no player info available, return default
    if lineup_info.empty:
        return 50.0
    
    try:
        # Check positional balance
        position_score = 0
        
        # If position column exists
        if 'position' in lineup_info.columns:
            # Fill missing positions with default value
            lineup_info['position'] = lineup_info['position'].fillna('F')
            
            # Count positions
            positions = lineup_info['position'].tolist()
            
            # Position categories
            guards = sum(1 for pos in positions if pos in ['PG', 'SG', 'G'])
            forwards = sum(1 for pos in positions if pos in ['SF', 'PF', 'F'])
            centers = sum(1 for pos in positions if pos in ['C'])
            
            # Ideal distribution is roughly 2 guards, 2 forwards, 1 center
            # Calculate deviation from ideal
            position_deviation = abs(guards - 2) + abs(forwards - 2) + abs(centers - 1)
            
            # Convert to score (higher is better)
            position_score = max(0, 40 - position_deviation * 10)  # 40 points for perfect distribution
        else:
            # If no position data, assign average score
            position_score = 20
        
        # Skill complementarity score (based on height, weight variations)
        skill_score = 0
        
        # Height variety (some tall, some shorter players is better than all the same)
        if 'height' in lineup_info.columns:
            # Fill missing heights with average
            lineup_info['height'] = lineup_info['height'].fillna(lineup_info['height'].mean() if not lineup_info['height'].isna().all() else 200)
            
            height_variance = lineup_info['height'].var()
            # Some variance is good, but not too much
            height_score = min(30, height_variance / 10) if height_variance <= 300 else max(0, 30 - (height_variance - 300) / 10)
            skill_score += height_score
        else:
            # Default height score
            skill_score += 15
        
        # Experience score (if age column exists)
        experience_score = 0
        if 'age' in lineup_info.columns:
            # Fill missing ages with average
            lineup_info['age'] = lineup_info['age'].fillna(lineup_info['age'].mean() if not lineup_info['age'].isna().all() else 25)
            
            # Average age (prime is around 27)
            avg_age = lineup_info['age'].mean()
            age_score = 30 - min(30, abs(avg_age - 27) * 3)
            experience_score = age_score
        else:
            # Default experience score
            experience_score = 15
        
        # Total chemistry score (out of 100)
        chemistry_score = position_score + skill_score + experience_score
        
        # Add random factor (team chemistry is somewhat unpredictable)
        chemistry_score += np.random.normal(0, 5)  # Add some noise
        
        # Ensure score is in 0-100 range
        chemistry_score = max(0, min(100, chemistry_score))
        
        return float(chemistry_score)
    except Exception:
        # If any calculation fails, return default score
        return 50.0

def check_lineup_balance(player_ids: List[str], player_info: pd.DataFrame) -> Tuple[bool, Dict[str, bool]]:
    """
    Check if a lineup has good positional balance.
    
    Args:
        player_ids: List of player IDs in the lineup
        player_info: DataFrame containing player information
        
    Returns:
        Tuple of (is_balanced, position_coverage)
    """
    # Get info for the selected players
    lineup_info = player_info[player_info['player_id'].isin(player_ids)]
    
    # Position categories to check
    position_categories = {
        'Guard': ['PG', 'SG', 'G'],
        'Forward': ['SF', 'PF', 'F'],
        'Center': ['C']
    }
    
    # Initialize coverage to False
    position_coverage = {category: False for category in position_categories}
    
    # If player_info is empty or doesn't have position column, return default
    if lineup_info.empty or 'position' not in lineup_info.columns:
        return False, position_coverage
    
    # Fill missing positions with default
    lineup_info['position'] = lineup_info['position'].fillna('F')
    
    # Get positions of lineup players
    positions = lineup_info['position'].tolist()
    
    # Check coverage for each category
    for category, pos_list in position_categories.items():
        position_coverage[category] = any(pos in pos_list for pos in positions)
    
    # Lineup is balanced if all categories are covered
    is_balanced = all(position_coverage.values())
    
    return is_balanced, position_coverage 