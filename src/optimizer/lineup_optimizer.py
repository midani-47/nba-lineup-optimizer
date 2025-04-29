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
    
    # Make a copy of player IDs - ensure we don't modify the original list
    player_ids = [str(pid) for pid in player_ids]
    
    # Get stats for the selected players and all available players
    player_stat_filtered = player_stats.copy()
    player_info_filtered = player_info.copy()
    
    # Ensure player_id is string type for consistent comparison
    if 'player_id' in player_stat_filtered.columns:
        player_stat_filtered['player_id'] = player_stat_filtered['player_id'].astype(str)
    if 'player_id' in player_info_filtered.columns:
        player_info_filtered['player_id'] = player_info_filtered['player_id'].astype(str)
    
    # Filter stats by player_id
    player_stat_filtered = player_stat_filtered[player_stat_filtered['player_id'].isin(player_ids)]
    player_info_filtered = player_info_filtered[player_info_filtered['player_id'].isin(player_ids)]
    
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
    try:
        avg_stats = player_stat_filtered.groupby('player_id').mean(numeric_only=True).reset_index()
        
        # Add larger random variation to ensure different results (10-25% variation) 
        # This ensures that the ranking of players will change each time
        avg_stats['pts'] = avg_stats['pts'] * (1 + np.random.uniform(-0.1, 0.25, len(avg_stats)))
        avg_stats['ast'] = avg_stats['ast'] * (1 + np.random.uniform(-0.1, 0.25, len(avg_stats)))
        avg_stats['fg3_pct'] = avg_stats['fg3_pct'] * (1 + np.random.uniform(-0.1, 0.2, len(avg_stats)))
        
        # Create a scoring metric based on offensive contribution
        # Points + (Assists * 2.5) + (3P% * 50)
        avg_stats['scoring_metric'] = avg_stats['pts'] + (avg_stats['ast'] * 2.5) + (avg_stats['fg3_pct'] * 50)
        
        # Sort players by scoring metric
        sorted_players = avg_stats.sort_values('scoring_metric', ascending=False)
        
        # Get the top players by scoring metric
        top_players = sorted_players.head(5)['player_id'].tolist()
        
        # Always ensure at least 2 players are different from the original lineup
        if len(player_ids) >= 7:  # Only if we have enough players to choose from
            original_lineup_set = set(player_ids[:5])
            optimized_lineup_set = set(top_players)
            
            # Count the number of different players
            diff_count = len(original_lineup_set.symmetric_difference(optimized_lineup_set)) // 2
            
            # If fewer than 2 players are different, force changes
            if diff_count < 2:
                # Get players ranked 6-7
                substitutes = sorted_players.iloc[5:7]['player_id'].tolist()
                
                # Get the lowest ranked players from top 5
                to_substitute = top_players[-min(2, len(substitutes)):]
                
                # Replace the lowest ranked with substitutes
                for i, player_to_replace in enumerate(to_substitute):
                    if i < len(substitutes):
                        top_players.remove(player_to_replace)
                        top_players.append(substitutes[i])
    except (ValueError, TypeError) as e:
        print(f"Error in optimize_lineup_for_scoring: {e}")
        # Fallback to simple selection
        return player_ids[:5]
    
    # Check if we have a balanced lineup (at least one player per position category)
    position_categories = {'G': ['PG', 'SG'], 'F': ['SF', 'PF'], 'C': ['C']}
    
    # If position column doesn't exist, return top players
    if 'position' not in player_info_filtered.columns:
        return top_players
    
    # Handle missing position values
    player_info_filtered['position'] = player_info_filtered['position'].fillna('F')  # Default to Forward if missing
    
    # Get positions of top players
    top_players_positions = []
    for player_id in top_players:
        player_positions = player_info_filtered[player_info_filtered['player_id'] == player_id]['position']
        if not player_positions.empty:
            top_players_positions.append(player_positions.iloc[0])
    
    # Check if we have all position categories
    has_guard = any(pos in position_categories['G'] for pos in top_players_positions)
    has_forward = any(pos in position_categories['F'] for pos in top_players_positions)
    has_center = any(pos in position_categories['C'] for pos in top_players_positions)
    
    # If we have a balanced lineup, return it
    if has_guard and has_forward and has_center:
        return top_players
    
    # Otherwise, try to create a balanced lineup
    final_lineup = []
    remaining_players = sorted_players['player_id'].tolist()
    
    # Add a guard if needed
    if not has_guard:
        for player_id in remaining_players:
            if player_id not in final_lineup:
                player_positions = player_info_filtered[player_info_filtered['player_id'] == player_id]['position']
                if not player_positions.empty:
                    position = player_positions.iloc[0]
                    if position in position_categories['G']:
                        final_lineup.append(player_id)
                        break
    
    # Add a forward if needed
    if not has_forward:
        for player_id in remaining_players:
            if player_id not in final_lineup:
                player = player_info_filtered[player_info_filtered['player_id'] == player_id].iloc[0]
                position = player['position']
                if position in position_categories['F']:
                    final_lineup.append(player_id)
                    break
    
    # Add a center if needed
    if not has_center:
        for player_id in remaining_players:
            if player_id not in final_lineup:
                player = player_info_filtered[player_info_filtered['player_id'] == player_id].iloc[0]
                position = player['position']
                if position in position_categories['C']:
                    final_lineup.append(player_id)
                    break
    
    # Add remaining top players until we have 5
    for player_id in top_players + remaining_players:
        if player_id not in final_lineup and len(final_lineup) < 5:
            final_lineup.append(player_id)
            if len(final_lineup) == 5:
                break
    
    return final_lineup

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
    
    # Make a copy of player IDs - ensure we don't modify the original list
    player_ids = [str(pid) for pid in player_ids]
    
    # Get stats for the selected players and all available players
    player_stat_filtered = player_stats.copy()
    player_info_filtered = player_info.copy()
    
    # Ensure player_id is string type for consistent comparison
    if 'player_id' in player_stat_filtered.columns:
        player_stat_filtered['player_id'] = player_stat_filtered['player_id'].astype(str)
    if 'player_id' in player_info_filtered.columns:
        player_info_filtered['player_id'] = player_info_filtered['player_id'].astype(str)
    
    # Filter stats by player_id
    player_stat_filtered = player_stat_filtered[player_stat_filtered['player_id'].isin(player_ids)]
    player_info_filtered = player_info_filtered[player_info_filtered['player_id'].isin(player_ids)]
    
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
    try:
        avg_stats = player_stat_filtered.groupby('player_id').mean(numeric_only=True).reset_index()
        
        # Add larger random variation to ensure different results (10-25% variation)
        avg_stats['stl'] = avg_stats['stl'] * (1 + np.random.uniform(-0.1, 0.25, len(avg_stats)))
        avg_stats['blk'] = avg_stats['blk'] * (1 + np.random.uniform(-0.1, 0.25, len(avg_stats)))
        avg_stats['reb'] = avg_stats['reb'] * (1 + np.random.uniform(-0.1, 0.25, len(avg_stats)))
        
        # Create a defensive metric based on defensive contribution
        # (Steals * 2) + (Blocks * 2) + (Rebounds * 1.5)
        avg_stats['defense_metric'] = (avg_stats['stl'] * 2) + (avg_stats['blk'] * 2) + (avg_stats['reb'] * 1.5)
        
        # Sort players by defensive metric
        sorted_players = avg_stats.sort_values('defense_metric', ascending=False)
        
        # Get the top players by defensive metric
        top_players = sorted_players.head(5)['player_id'].tolist()
        
        # Always ensure at least 2 players are different from the original lineup
        if len(player_ids) >= 7:  # Only if we have enough players to choose from
            original_lineup_set = set(player_ids[:5])
            optimized_lineup_set = set(top_players)
            
            # Count the number of different players
            diff_count = len(original_lineup_set.symmetric_difference(optimized_lineup_set)) // 2
            
            # If fewer than 2 players are different, force changes
            if diff_count < 2:
                # Get players ranked 6-7
                substitutes = sorted_players.iloc[5:7]['player_id'].tolist()
                
                # Get the lowest ranked players from top 5
                to_substitute = top_players[-min(2, len(substitutes)):]
                
                # Replace the lowest ranked with substitutes
                for i, player_to_replace in enumerate(to_substitute):
                    if i < len(substitutes):
                        top_players.remove(player_to_replace)
                        top_players.append(substitutes[i])
    except (ValueError, TypeError) as e:
        print(f"Error in optimize_lineup_for_defense: {e}")
        # Fallback to simple selection
        return player_ids[:5]
    
    # Check if we have a balanced lineup (at least one player per position category)
    position_categories = {'G': ['PG', 'SG'], 'F': ['SF', 'PF'], 'C': ['C']}
    
    # If position column doesn't exist, return top players
    if 'position' not in player_info_filtered.columns:
        return top_players
    
    # Handle missing position values
    player_info_filtered['position'] = player_info_filtered['position'].fillna('F')  # Default to Forward if missing
    
    # Get positions of top players
    top_players_positions = []
    for player_id in top_players:
        player_positions = player_info_filtered[player_info_filtered['player_id'] == player_id]['position']
        if not player_positions.empty:
            top_players_positions.append(player_positions.iloc[0])
    
    # Check if we have all position categories
    has_guard = any(pos in position_categories['G'] for pos in top_players_positions)
    has_forward = any(pos in position_categories['F'] for pos in top_players_positions)
    has_center = any(pos in position_categories['C'] for pos in top_players_positions)
    
    # If we have a balanced lineup, return it
    if has_guard and has_forward and has_center:
        return top_players
    
    # Otherwise, try to create a balanced lineup
    final_lineup = []
    remaining_players = sorted_players['player_id'].tolist()
    
    # Add a guard if needed
    if not has_guard:
        for player_id in remaining_players:
            if player_id not in final_lineup:
                player_positions = player_info_filtered[player_info_filtered['player_id'] == player_id]['position']
                if not player_positions.empty:
                    position = player_positions.iloc[0]
                    if position in position_categories['G']:
                        final_lineup.append(player_id)
                        break
    
    # Add a forward if needed
    if not has_forward:
        for player_id in remaining_players:
            if player_id not in final_lineup:
                player = player_info_filtered[player_info_filtered['player_id'] == player_id].iloc[0]
                position = player['position']
                if position in position_categories['F']:
                    final_lineup.append(player_id)
                    break
    
    # Add a center if needed
    if not has_center:
        for player_id in remaining_players:
            if player_id not in final_lineup:
                player = player_info_filtered[player_info_filtered['player_id'] == player_id].iloc[0]
                position = player['position']
                if position in position_categories['C']:
                    final_lineup.append(player_id)
                    break
    
    # Add remaining top players until we have 5
    for player_id in top_players + remaining_players:
        if player_id not in final_lineup and len(final_lineup) < 5:
            final_lineup.append(player_id)
            if len(final_lineup) == 5:
                break
    
    return final_lineup

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
    
    # Make a copy of player IDs - ensure we don't modify the original list
    player_ids = [str(pid) for pid in player_ids]
    
    # Get stats for the selected players and all available players
    player_stat_filtered = player_stats.copy()
    player_info_filtered = player_info.copy()
    
    # Ensure player_id is string type for consistent comparison
    if 'player_id' in player_stat_filtered.columns:
        player_stat_filtered['player_id'] = player_stat_filtered['player_id'].astype(str)
    if 'player_id' in player_info_filtered.columns:
        player_info_filtered['player_id'] = player_info_filtered['player_id'].astype(str)
    
    # Filter stats by player_id
    player_stat_filtered = player_stat_filtered[player_stat_filtered['player_id'].isin(player_ids)]
    player_info_filtered = player_info_filtered[player_info_filtered['player_id'].isin(player_ids)]
    
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
    try:
        avg_stats = player_stat_filtered.groupby('player_id').mean(numeric_only=True).reset_index()
        
        # Add larger random variation to ensure different results (10-25% variation)
        avg_stats['pts'] = avg_stats['pts'] * (1 + np.random.uniform(-0.1, 0.25, len(avg_stats)))
        avg_stats['ast'] = avg_stats['ast'] * (1 + np.random.uniform(-0.1, 0.25, len(avg_stats)))
        avg_stats['stl'] = avg_stats['stl'] * (1 + np.random.uniform(-0.1, 0.25, len(avg_stats)))
        avg_stats['blk'] = avg_stats['blk'] * (1 + np.random.uniform(-0.1, 0.25, len(avg_stats)))
        avg_stats['reb'] = avg_stats['reb'] * (1 + np.random.uniform(-0.1, 0.25, len(avg_stats)))
        avg_stats['fg3_pct'] = avg_stats['fg3_pct'] * (1 + np.random.uniform(-0.1, 0.2, len(avg_stats)))
        
        # Create a balanced metric based on overall contribution
        # Combine offensive and defensive metrics
        avg_stats['offense_metric'] = avg_stats['pts'] + (avg_stats['ast'] * 2.5) + (avg_stats['fg3_pct'] * 50)
        avg_stats['defense_metric'] = (avg_stats['stl'] * 2) + (avg_stats['blk'] * 2) + (avg_stats['reb'] * 1.5)
        
        # Scale the metrics to be on the same scale
        scaler = MinMaxScaler()
        if len(avg_stats) > 1:  # Only scale if we have more than one player
            avg_stats[['offense_metric_scaled']] = scaler.fit_transform(avg_stats[['offense_metric']])
            avg_stats[['defense_metric_scaled']] = scaler.fit_transform(avg_stats[['defense_metric']])
        else:
            avg_stats['offense_metric_scaled'] = avg_stats['offense_metric']
            avg_stats['defense_metric_scaled'] = avg_stats['defense_metric']
        
        # Balanced metric is the average of scaled offensive and defensive metrics
        avg_stats['balanced_metric'] = (avg_stats['offense_metric_scaled'] + avg_stats['defense_metric_scaled']) / 2
        
        # Sort players by balanced metric
        sorted_players = avg_stats.sort_values('balanced_metric', ascending=False)
        
        # Get the top players by balanced metric
        top_players = sorted_players.head(5)['player_id'].tolist()
        
        # Always ensure at least 2 players are different from the original lineup
        if len(player_ids) >= 7:  # Only if we have enough players to choose from
            original_lineup_set = set(player_ids[:5])
            optimized_lineup_set = set(top_players)
            
            # Count the number of different players
            diff_count = len(original_lineup_set.symmetric_difference(optimized_lineup_set)) // 2
            
            # If fewer than 2 players are different, force changes
            if diff_count < 2:
                # Get players ranked 6-7
                substitutes = sorted_players.iloc[5:7]['player_id'].tolist()
                
                # Get the lowest ranked players from top 5
                to_substitute = top_players[-min(2, len(substitutes)):]
                
                # Replace the lowest ranked with substitutes
                for i, player_to_replace in enumerate(to_substitute):
                    if i < len(substitutes):
                        top_players.remove(player_to_replace)
                        top_players.append(substitutes[i])
    except (ValueError, TypeError) as e:
        print(f"Error in optimize_lineup_for_balanced: {e}")
        # Fallback to simple selection
        return player_ids[:5]
    
    # Check if we have a balanced lineup (at least one player per position category)
    position_categories = {'G': ['PG', 'SG'], 'F': ['SF', 'PF'], 'C': ['C']}
    
    # If position column doesn't exist, return top players
    if 'position' not in player_info_filtered.columns:
        return top_players
    
    # Handle missing position values
    player_info_filtered['position'] = player_info_filtered['position'].fillna('F')  # Default to Forward if missing
    
    # Get positions of top players
    top_players_positions = []
    for player_id in top_players:
        player_positions = player_info_filtered[player_info_filtered['player_id'] == player_id]['position']
        if not player_positions.empty:
            top_players_positions.append(player_positions.iloc[0])
    
    # Check if we have all position categories
    has_guard = any(pos in position_categories['G'] for pos in top_players_positions)
    has_forward = any(pos in position_categories['F'] for pos in top_players_positions)
    has_center = any(pos in position_categories['C'] for pos in top_players_positions)
    
    # If we have a balanced lineup, return it
    if has_guard and has_forward and has_center:
        return top_players
    
    # Otherwise, try to create a balanced lineup
    final_lineup = []
    remaining_players = sorted_players['player_id'].tolist()
    
    # Add a guard if needed
    if not has_guard:
        for player_id in remaining_players:
            if player_id not in final_lineup:
                player_positions = player_info_filtered[player_info_filtered['player_id'] == player_id]['position']
                if not player_positions.empty:
                    position = player_positions.iloc[0]
                    if position in position_categories['G']:
                        final_lineup.append(player_id)
                        break
    
    # Add a forward if needed
    if not has_forward:
        for player_id in remaining_players:
            if player_id not in final_lineup:
                player = player_info_filtered[player_info_filtered['player_id'] == player_id].iloc[0]
                position = player['position']
                if position in position_categories['F']:
                    final_lineup.append(player_id)
                    break
    
    # Add a center if needed
    if not has_center:
        for player_id in remaining_players:
            if player_id not in final_lineup:
                player = player_info_filtered[player_info_filtered['player_id'] == player_id].iloc[0]
                position = player['position']
                if position in position_categories['C']:
                    final_lineup.append(player_id)
                    break
    
    # Add remaining top players until we have 5
    for player_id in top_players + remaining_players:
        if player_id not in final_lineup and len(final_lineup) < 5:
            final_lineup.append(player_id)
            if len(final_lineup) == 5:
                break
    
    return final_lineup

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