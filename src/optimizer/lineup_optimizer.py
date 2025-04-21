import pandas as pd
import numpy as np
from itertools import combinations
from sklearn.preprocessing import MinMaxScaler

def optimize_lineup_for_scoring(current_player_ids, player_stats, players_df):
    """
    Optimize a lineup for maximum scoring potential.
    
    Args:
        current_player_ids (list): List of player IDs in the current lineup
        player_stats (pandas.DataFrame): DataFrame with player statistics
        players_df (pandas.DataFrame): DataFrame with player information
    
    Returns:
        list: List of optimized player IDs for the lineup
    """
    # For demonstration, we'll use a simple algorithm
    # In a real app, this would be more sophisticated
    
    # Get positions of current lineup
    current_positions = []
    for player_id in current_player_ids:
        player = players_df[players_df['player_id'] == player_id]
        if not player.empty:
            current_positions.append(player['position'].iloc[0])
    
    # For each player, calculate their scoring metrics
    scoring_metrics = {}
    for player_id in current_player_ids:
        player_data = player_stats[player_stats['player_id'] == player_id]
        if not player_data.empty:
            # Calculate scoring metric: points + 0.5*assists + 0.3*3pt%*100
            avg_stats = player_data.mean(numeric_only=True)
            scoring_metric = avg_stats['pts'] + 0.5 * avg_stats['ast'] + 30 * avg_stats['fg3_pct']
            scoring_metrics[player_id] = scoring_metric
    
    # Sort players by scoring metric (highest first)
    sorted_players = sorted(scoring_metrics.items(), key=lambda x: x[1], reverse=True)
    
    # Keep top 3 scorers
    core_players = [player_id for player_id, _ in sorted_players[:3]]
    players_to_replace = [player_id for player_id, _ in sorted_players[3:]]
    
    # Find suitable replacements that maintain position balance
    # Here we'll use a simplified approach - in a real app you'd use more sophisticated methods
    if players_to_replace:
        replaced_positions = []
        for player_id in players_to_replace:
            player = players_df[players_df['player_id'] == player_id]
            if not player.empty:
                replaced_positions.append(player['position'].iloc[0])
        
        # Get top scoring players by position to replace
        replacements = []
        for position in replaced_positions:
            # Get players with similar position who aren't in the lineup
            similar_position_players = players_df[
                (players_df['position'].str.contains(position.split('/')[0])) & 
                (~players_df['player_id'].isin(current_player_ids + replacements))
            ]
            
            if not similar_position_players.empty:
                # Get stats for these players
                position_player_stats = []
                for idx, row in similar_position_players.iterrows():
                    player_data = player_stats[player_stats['player_id'] == row['player_id']]
                    if not player_data.empty:
                        avg_stats = player_data.mean(numeric_only=True)
                        scoring_metric = avg_stats['pts'] + 0.5 * avg_stats['ast'] + 30 * avg_stats['fg3_pct']
                        position_player_stats.append((row['player_id'], scoring_metric))
                
                # Sort by scoring metric and take the best
                if position_player_stats:
                    best_replacement = sorted(position_player_stats, key=lambda x: x[1], reverse=True)[0][0]
                    replacements.append(best_replacement)
        
        # Combine core players with replacements
        optimized_lineup = core_players + replacements
        
        # If we don't have 5 players, pad with original players
        if len(optimized_lineup) < 5:
            remaining = [p for p in current_player_ids if p not in optimized_lineup]
            optimized_lineup.extend(remaining[:5 - len(optimized_lineup)])
        
        return optimized_lineup
    
    return current_player_ids

def optimize_lineup_for_defense(current_player_ids, player_stats, players_df):
    """
    Optimize a lineup for maximum defensive potential.
    
    Args:
        current_player_ids (list): List of player IDs in the current lineup
        player_stats (pandas.DataFrame): DataFrame with player statistics
        players_df (pandas.DataFrame): DataFrame with player information
    
    Returns:
        list: List of optimized player IDs for the lineup
    """
    # For demonstration, we'll use a simple algorithm
    # In a real app, this would be more sophisticated
    
    # Get positions of current lineup
    current_positions = []
    for player_id in current_player_ids:
        player = players_df[players_df['player_id'] == player_id]
        if not player.empty:
            current_positions.append(player['position'].iloc[0])
    
    # For each player, calculate their defensive metrics
    defensive_metrics = {}
    for player_id in current_player_ids:
        player_data = player_stats[player_stats['player_id'] == player_id]
        if not player_data.empty:
            # Calculate defensive metric: steals + blocks + rebounds*0.5
            avg_stats = player_data.mean(numeric_only=True)
            defensive_metric = avg_stats['stl'] + avg_stats['blk'] + 0.5 * avg_stats['reb']
            defensive_metrics[player_id] = defensive_metric
    
    # Sort players by defensive metric (highest first)
    sorted_players = sorted(defensive_metrics.items(), key=lambda x: x[1], reverse=True)
    
    # Keep top 3 defenders
    core_players = [player_id for player_id, _ in sorted_players[:3]]
    players_to_replace = [player_id for player_id, _ in sorted_players[3:]]
    
    # Find suitable replacements that maintain position balance
    if players_to_replace:
        replaced_positions = []
        for player_id in players_to_replace:
            player = players_df[players_df['player_id'] == player_id]
            if not player.empty:
                replaced_positions.append(player['position'].iloc[0])
        
        # Get top defensive players by position to replace
        replacements = []
        for position in replaced_positions:
            # Get players with similar position who aren't in the lineup
            similar_position_players = players_df[
                (players_df['position'].str.contains(position.split('/')[0])) & 
                (~players_df['player_id'].isin(current_player_ids + replacements))
            ]
            
            if not similar_position_players.empty:
                # Get stats for these players
                position_player_stats = []
                for idx, row in similar_position_players.iterrows():
                    player_data = player_stats[player_stats['player_id'] == row['player_id']]
                    if not player_data.empty:
                        avg_stats = player_data.mean(numeric_only=True)
                        defensive_metric = avg_stats['stl'] + avg_stats['blk'] + 0.5 * avg_stats['reb']
                        position_player_stats.append((row['player_id'], defensive_metric))
                
                # Sort by defensive metric and take the best
                if position_player_stats:
                    best_replacement = sorted(position_player_stats, key=lambda x: x[1], reverse=True)[0][0]
                    replacements.append(best_replacement)
        
        # Combine core players with replacements
        optimized_lineup = core_players + replacements
        
        # If we don't have 5 players, pad with original players
        if len(optimized_lineup) < 5:
            remaining = [p for p in current_player_ids if p not in optimized_lineup]
            optimized_lineup.extend(remaining[:5 - len(optimized_lineup)])
        
        return optimized_lineup
    
    return current_player_ids

def optimize_lineup_for_balanced(current_player_ids, player_stats, players_df):
    """
    Optimize a lineup for a balanced approach (scoring and defense).
    
    Args:
        current_player_ids (list): List of player IDs in the current lineup
        player_stats (pandas.DataFrame): DataFrame with player statistics
        players_df (pandas.DataFrame): DataFrame with player information
    
    Returns:
        list: List of optimized player IDs for the lineup
    """
    # For demonstration, we'll use a simple algorithm
    # In a real app, this would be more sophisticated
    
    # For each player, calculate their balanced metrics
    balanced_metrics = {}
    for player_id in current_player_ids:
        player_data = player_stats[player_stats['player_id'] == player_id]
        if not player_data.empty:
            # Calculate balanced metric: combination of offensive and defensive stats
            avg_stats = player_data.mean(numeric_only=True)
            offensive_metric = avg_stats['pts'] + 0.5 * avg_stats['ast'] + 30 * avg_stats['fg3_pct']
            defensive_metric = avg_stats['stl'] + avg_stats['blk'] + 0.5 * avg_stats['reb']
            balanced_metric = (offensive_metric + defensive_metric) / 2
            balanced_metrics[player_id] = balanced_metric
    
    # Sort players by balanced metric (highest first)
    sorted_players = sorted(balanced_metrics.items(), key=lambda x: x[1], reverse=True)
    
    # Keep top 3 balanced players
    core_players = [player_id for player_id, _ in sorted_players[:3]]
    players_to_replace = [player_id for player_id, _ in sorted_players[3:]]
    
    # Get positions of players to replace
    replaced_positions = []
    for player_id in players_to_replace:
        player = players_df[players_df['player_id'] == player_id]
        if not player.empty:
            replaced_positions.append(player['position'].iloc[0])
    
    # Find suitable replacements that maintain position balance
    replacements = []
    for position in replaced_positions:
        # Get players with similar position who aren't in the lineup
        similar_position_players = players_df[
            (players_df['position'].str.contains(position.split('/')[0])) & 
            (~players_df['player_id'].isin(current_player_ids + replacements))
        ]
        
        if not similar_position_players.empty:
            # Get stats for these players
            position_player_stats = []
            for idx, row in similar_position_players.iterrows():
                player_data = player_stats[player_stats['player_id'] == row['player_id']]
                if not player_data.empty:
                    avg_stats = player_data.mean(numeric_only=True)
                    offensive_metric = avg_stats['pts'] + 0.5 * avg_stats['ast'] + 30 * avg_stats['fg3_pct']
                    defensive_metric = avg_stats['stl'] + avg_stats['blk'] + 0.5 * avg_stats['reb']
                    balanced_metric = (offensive_metric + defensive_metric) / 2
                    position_player_stats.append((row['player_id'], balanced_metric))
            
            # Sort by balanced metric and take the best
            if position_player_stats:
                best_replacement = sorted(position_player_stats, key=lambda x: x[1], reverse=True)[0][0]
                replacements.append(best_replacement)
    
    # Combine core players with replacements
    optimized_lineup = core_players + replacements
    
    # If we don't have 5 players, pad with original players
    if len(optimized_lineup) < 5:
        remaining = [p for p in current_player_ids if p not in optimized_lineup]
        optimized_lineup.extend(remaining[:5 - len(optimized_lineup)])
    
    return optimized_lineup

def check_lineup_balance(player_ids, players_df):
    """
    Check if a lineup has a good balance of positions.
    
    Args:
        player_ids (list): List of player IDs in the lineup
        players_df (pandas.DataFrame): DataFrame with player information
    
    Returns:
        tuple: (is_balanced, reasons)
    """
    # Get positions in the lineup
    positions = []
    for player_id in player_ids:
        player = players_df[players_df['player_id'] == player_id]
        if not player.empty:
            positions.append(player['position'].iloc[0])
    
    # Convert multi-positions (e.g., "PG/SG") to primary positions
    primary_positions = [pos.split('/')[0] for pos in positions]
    
    # Count positions
    position_counts = {}
    for pos in primary_positions:
        position_counts[pos] = position_counts.get(pos, 0) + 1
    
    # Check for position balance
    reasons = []
    
    # A balanced lineup typically has at least one guard, one forward, and one center
    if not any(pos in ['PG', 'SG'] for pos in position_counts):
        reasons.append("No guards in lineup")
    
    if not any(pos in ['SF', 'PF'] for pos in position_counts):
        reasons.append("No forwards in lineup")
    
    if 'C' not in position_counts:
        reasons.append("No center in lineup")
    
    # Check for overloaded positions
    for pos, count in position_counts.items():
        if count > 2:
            reasons.append(f"Too many {pos} players ({count})")
    
    return len(reasons) == 0, reasons

def calculate_lineup_chemistry(player_ids, player_stats):
    """
    Calculate a "chemistry" score for a lineup based on complementary skills.
    This is a simplified model for demonstration purposes.
    
    Args:
        player_ids (list): List of player IDs in the lineup
        player_stats (pandas.DataFrame): DataFrame with player statistics
    
    Returns:
        float: Chemistry score from 0-100
    """
    # Get player stats
    lineup_stats = []
    for player_id in player_ids:
        player_data = player_stats[player_stats['player_id'] == player_id]
        if not player_data.empty:
            avg_stats = player_data.mean(numeric_only=True)
            lineup_stats.append(avg_stats)
    
    if not lineup_stats:
        return 50.0  # Default score
    
    # Create a DataFrame with player stats
    lineup_df = pd.DataFrame(lineup_stats)
    
    # Check for skill diversity - a good lineup has diverse skills
    skill_diversity = 0
    
    # Calculate standard deviation for key stats
    # Higher std dev means more diversity in skills
    key_stats = ['pts', 'reb', 'ast', 'stl', 'blk']
    
    if all(stat in lineup_df.columns for stat in key_stats):
        std_devs = lineup_df[key_stats].std()
        normalized_std_devs = std_devs / lineup_df[key_stats].mean()
        skill_diversity = normalized_std_devs.mean() * 50  # Scale to 0-50 range
    
    # Check for skill complementation - do players complement each other?
    skill_complement = 0
    
    # Calculate correlation between different stats
    # Lower correlation is better (players specialize in different areas)
    if all(stat in lineup_df.columns for stat in key_stats) and len(lineup_df) > 1:
        corr_matrix = lineup_df[key_stats].corr()
        # Get average of absolute correlations (excluding self-correlations)
        corrs = []
        for i in range(len(key_stats)):
            for j in range(i+1, len(key_stats)):
                corrs.append(abs(corr_matrix.iloc[i, j]))
        
        if corrs:
            avg_corr = sum(corrs) / len(corrs)
            skill_complement = (1 - avg_corr) * 50  # Scale to 0-50 range
    
    # Combine scores and ensure within 0-100 range
    chemistry = min(100, max(0, skill_diversity + skill_complement))
    
    return chemistry 