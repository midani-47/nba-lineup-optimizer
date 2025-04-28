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
    
    # Calculate average stats per player
    avg_stats = player_stat_filtered.groupby('player_id').mean().reset_index()
    
    # Create a scoring metric based on offensive contribution
    # Points + (Assists * 2.5) + (3P% * 50)
    avg_stats['scoring_metric'] = avg_stats['pts'] + (avg_stats['ast'] * 2.5) + (avg_stats['fg3_pct'] * 50)
    
    # Sort players by scoring metric
    sorted_players = avg_stats.sort_values('scoring_metric', ascending=False)
    
    # Get the top 5 players by scoring metric
    top_players = sorted_players.head(5)['player_id'].tolist()
    
    # Check if we have a balanced lineup (at least one player per position category)
    position_categories = {'G': ['PG', 'SG'], 'F': ['SF', 'PF'], 'C': ['C']}
    
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
            lowest_scorer_id = min(optimized_lineup, key=lambda pid: float(avg_stats[avg_stats['player_id'] == pid]['scoring_metric'].values[0]))
            
            # Find the highest scoring player of the missing category
            category_positions = position_categories[category]
            category_players = player_info_filtered[player_info_filtered['position'].isin(category_positions)]['player_id'].tolist()
            
            # If we have players in this category, find the best one
            if category_players:
                # Get best player of this category by scoring metric
                category_stats = avg_stats[avg_stats['player_id'].isin(category_players)]
                best_category_player = category_stats.sort_values('scoring_metric', ascending=False).iloc[0]['player_id']
                
                # Replace the lowest scorer with the best category player if not already in lineup
                if best_category_player not in optimized_lineup:
                    optimized_lineup.remove(lowest_scorer_id)
                    optimized_lineup.append(best_category_player)
        
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
    
    # Calculate average stats per player
    avg_stats = player_stat_filtered.groupby('player_id').mean().reset_index()
    
    # Create a defensive metric based on defensive contribution
    # (Steals * 2) + (Blocks * 2) + (Rebounds * 1.2)
    avg_stats['defensive_metric'] = (avg_stats['stl'] * 2) + (avg_stats['blk'] * 2) + (avg_stats['reb'] * 1.2)
    
    # Sort players by defensive metric
    sorted_players = avg_stats.sort_values('defensive_metric', ascending=False)
    
    # Get the top 5 players by defensive metric
    top_players = sorted_players.head(5)['player_id'].tolist()
    
    # Check if we have a balanced lineup (at least one player per position category)
    position_categories = {'G': ['PG', 'SG'], 'F': ['SF', 'PF'], 'C': ['C']}
    
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
            # Find the lowest defensive player in the lineup
            lowest_defender_id = min(optimized_lineup, key=lambda pid: float(avg_stats[avg_stats['player_id'] == pid]['defensive_metric'].values[0]))
            
            # Find the highest defensive player of the missing category
            category_positions = position_categories[category]
            category_players = player_info_filtered[player_info_filtered['position'].isin(category_positions)]['player_id'].tolist()
            
            # If we have players in this category, find the best one
            if category_players:
                # Get best player of this category by defensive metric
                category_stats = avg_stats[avg_stats['player_id'].isin(category_players)]
                best_category_player = category_stats.sort_values('defensive_metric', ascending=False).iloc[0]['player_id']
                
                # Replace the lowest defender with the best category player if not already in lineup
                if best_category_player not in optimized_lineup:
                    optimized_lineup.remove(lowest_defender_id)
                    optimized_lineup.append(best_category_player)
        
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
    
    # Calculate average stats per player
    avg_stats = player_stat_filtered.groupby('player_id').mean().reset_index()
    
    # Create scoring and defensive metrics
    avg_stats['scoring_metric'] = avg_stats['pts'] + (avg_stats['ast'] * 2.5) + (avg_stats['fg3_pct'] * 50)
    avg_stats['defensive_metric'] = (avg_stats['stl'] * 2) + (avg_stats['blk'] * 2) + (avg_stats['reb'] * 1.2)
    
    # Normalize the metrics
    avg_stats['scoring_metric_norm'] = (avg_stats['scoring_metric'] - avg_stats['scoring_metric'].min()) / (avg_stats['scoring_metric'].max() - avg_stats['scoring_metric'].min() + 1e-10)
    avg_stats['defensive_metric_norm'] = (avg_stats['defensive_metric'] - avg_stats['defensive_metric'].min()) / (avg_stats['defensive_metric'].max() - avg_stats['defensive_metric'].min() + 1e-10)
    
    # Create a balanced metric
    avg_stats['balanced_metric'] = avg_stats['scoring_metric_norm'] + avg_stats['defensive_metric_norm']
    
    # Sort players by balanced metric
    sorted_players = avg_stats.sort_values('balanced_metric', ascending=False)
    
    # Get the top 5 players by balanced metric
    top_players = sorted_players.head(5)['player_id'].tolist()
    
    # Check if we have a balanced lineup (at least one player per position category)
    position_categories = {'G': ['PG', 'SG'], 'F': ['SF', 'PF'], 'C': ['C']}
    
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
        
        # For each missing category, replace the lowest balanced player with the highest balanced player of that category
        for category in missing_categories:
            # Find the lowest balanced player in the lineup
            lowest_balanced_id = min(optimized_lineup, key=lambda pid: float(avg_stats[avg_stats['player_id'] == pid]['balanced_metric'].values[0]))
            
            # Find the highest balanced player of the missing category
            category_positions = position_categories[category]
            category_players = player_info_filtered[player_info_filtered['position'].isin(category_positions)]['player_id'].tolist()
            
            # If we have players in this category, find the best one
            if category_players:
                # Get best player of this category by balanced metric
                category_stats = avg_stats[avg_stats['player_id'].isin(category_players)]
                best_category_player = category_stats.sort_values('balanced_metric', ascending=False).iloc[0]['player_id']
                
                # Replace the lowest balanced with the best category player if not already in lineup
                if best_category_player not in optimized_lineup:
                    optimized_lineup.remove(lowest_balanced_id)
                    optimized_lineup.append(best_category_player)
        
        return optimized_lineup
    
    return top_players

def calculate_lineup_chemistry(player_ids: List[str], player_stats: pd.DataFrame, player_info: pd.DataFrame) -> float:
    """
    Calculate the chemistry score for a lineup.
    
    Args:
        player_ids: List of player IDs in the lineup
        player_stats: DataFrame containing player statistics
        player_info: DataFrame containing player information
        
    Returns:
        Chemistry score from 0 to 100
    """
    # Validate inputs
    if len(player_ids) < 2:
        return 50.0  # Not enough players to calculate chemistry
    
    # Get stats for the selected players
    player_stat_filtered = player_stats[player_stats['player_id'].isin(player_ids)]
    player_info_filtered = player_info[player_info['player_id'].isin(player_ids)]
    
    # Calculate average stats per player
    avg_stats = player_stat_filtered.groupby('player_id').mean().reset_index()
    
    # Define chemistry factors
    chemistry_score = 0
    
    # 1. Position balance (25%)
    position_categories = {'G': ['PG', 'SG'], 'F': ['SF', 'PF'], 'C': ['C']}
    
    # Get positions of players
    player_positions = player_info_filtered['position'].tolist()
    
    has_guard = any(pos in position_categories['G'] for pos in player_positions)
    has_forward = any(pos in position_categories['F'] for pos in player_positions)
    has_center = any(pos in position_categories['C'] for pos in player_positions)
    
    position_score = 0
    if has_guard:
        position_score += 8
    if has_forward:
        position_score += 8
    if has_center:
        position_score += 9
    
    chemistry_score += position_score
    
    # 2. Skill complementarity (25%)
    # Assess if the lineup has a good mix of scorers, passers, and defenders
    has_scorer = any(avg_stats['pts'] > 20)
    has_passer = any(avg_stats['ast'] > 5)
    has_defender = any((avg_stats['stl'] + avg_stats['blk']) > 2)
    has_rebounder = any(avg_stats['reb'] > 8)
    
    skill_score = 0
    if has_scorer:
        skill_score += 6
    if has_passer:
        skill_score += 6
    if has_defender:
        skill_score += 6
    if has_rebounder:
        skill_score += 7
    
    chemistry_score += skill_score
    
    # 3. Team diversity (25%)
    # Check if the lineup has diverse shooting abilities
    three_point_shooters = sum(avg_stats['fg3_pct'] > 0.35)
    inside_scorers = sum((avg_stats['fg_pct'] > 0.50) & (avg_stats['pts'] > 10))
    
    diversity_score = 0
    if three_point_shooters >= 2:
        diversity_score += 12
    elif three_point_shooters >= 1:
        diversity_score += 6
    
    if inside_scorers >= 2:
        diversity_score += 13
    elif inside_scorers >= 1:
        diversity_score += 7
    
    chemistry_score += diversity_score
    
    # 4. Same team bonus (25%)
    # Players from the same team might have better chemistry
    teams = player_info_filtered['team'].tolist()
    team_counts = {}
    for team in teams:
        if team in team_counts:
            team_counts[team] += 1
        else:
            team_counts[team] = 1
    
    # Calculate team synergy score
    synergy_score = 0
    for team, count in team_counts.items():
        if count >= 3:
            synergy_score += 25  # Strong synergy
        elif count == 2:
            synergy_score += 15  # Moderate synergy
    
    # Cap synergy score at 25
    synergy_score = min(synergy_score, 25)
    chemistry_score += synergy_score
    
    return chemistry_score

def check_lineup_balance(player_ids: List[str], player_info: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Check if a lineup has a good balance of positions.
    
    Args:
        player_ids: List of player IDs in the lineup
        player_info: DataFrame containing player information
        
    Returns:
        Tuple of (is_balanced, reasons)
    """
    if len(player_ids) != 5:
        return False, ["Lineup must have exactly 5 players"]
    
    # Get positions for the selected players
    player_info_filtered = player_info[player_info['player_id'].isin(player_ids)]
    player_positions = player_info_filtered['position'].tolist()
    
    # Define position categories
    position_categories = {
        'PG': 'Guard',
        'SG': 'Guard',
        'SF': 'Forward',
        'PF': 'Forward',
        'C': 'Center'
    }
    
    # Count positions by category
    position_counts = {
        'Guard': 0,
        'Forward': 0,
        'Center': 0
    }
    
    for pos in player_positions:
        category = position_categories.get(pos, 'Unknown')
        if category in position_counts:
            position_counts[category] += 1
    
    # Check if we have a balanced lineup
    reasons = []
    is_balanced = True
    
    # Need at least one guard
    if position_counts['Guard'] < 1:
        reasons.append("Lineup needs at least one guard (PG or SG)")
        is_balanced = False
    
    # Need at least one forward
    if position_counts['Forward'] < 1:
        reasons.append("Lineup needs at least one forward (SF or PF)")
        is_balanced = False
    
    # Need at least one center
    if position_counts['Center'] < 1:
        reasons.append("Lineup needs at least one center (C)")
        is_balanced = False
    
    # Check for too many of one position
    if position_counts['Guard'] > 3:
        reasons.append("Too many guards (more than 3)")
        is_balanced = False
    
    if position_counts['Forward'] > 3:
        reasons.append("Too many forwards (more than 3)")
        is_balanced = False
    
    if position_counts['Center'] > 2:
        reasons.append("Too many centers (more than 2)")
        is_balanced = False
    
    return is_balanced, reasons 