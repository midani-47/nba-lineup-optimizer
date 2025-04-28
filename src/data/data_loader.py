import pandas as pd
import numpy as np
import os
import json
from typing import Dict, List, Tuple, Any, Optional
from functools import lru_cache

@lru_cache(maxsize=1)
def load_player_data() -> pd.DataFrame:
    """
    Load player data from CSV file.
    Uses a cache to avoid reloading data multiple times.
    
    Returns:
        DataFrame containing player information
    """
    # Check if data exists in data directory
    data_path = os.path.join('data', 'players.csv')
    
    # If data doesn't exist, create sample data
    if not os.path.exists(data_path):
        return create_sample_player_data()
    
    try:
        df = pd.read_csv(data_path)
        return df
    except Exception as e:
        print(f"Error loading player data: {e}")
        return create_sample_player_data()

@lru_cache(maxsize=1)
def load_player_stats() -> pd.DataFrame:
    """
    Load player statistics from CSV file.
    Uses a cache to avoid reloading data multiple times.
    
    Returns:
        DataFrame containing player statistics
    """
    # Check if data exists in data directory
    data_path = os.path.join('data', 'player_stats.csv')
    
    # If data doesn't exist, create sample data
    if not os.path.exists(data_path):
        return create_sample_player_stats()
    
    try:
        df = pd.read_csv(data_path)
        return df
    except Exception as e:
        print(f"Error loading player stats: {e}")
        return create_sample_player_stats()

@lru_cache(maxsize=1)
def load_team_data() -> pd.DataFrame:
    """
    Load team data from CSV file.
    Uses a cache to avoid reloading data multiple times.
    
    Returns:
        DataFrame containing team information
    """
    # Check if data exists in data directory
    data_path = os.path.join('data', 'teams.csv')
    
    # If data doesn't exist, create sample data
    if not os.path.exists(data_path):
        return create_sample_team_data()
    
    try:
        df = pd.read_csv(data_path)
        return df
    except Exception as e:
        print(f"Error loading team data: {e}")
        return create_sample_team_data()

def get_players_by_team(team_id: str) -> pd.DataFrame:
    """
    Get all players for a specific team.
    
    Args:
        team_id: Team identifier
        
    Returns:
        DataFrame containing players filtered by team
    """
    players = load_player_data()
    return players[players['team'] == team_id]

def get_players_by_position(position: str) -> pd.DataFrame:
    """
    Get all players for a specific position.
    
    Args:
        position: Position code (PG, SG, SF, PF, C)
        
    Returns:
        DataFrame containing players filtered by position
    """
    players = load_player_data()
    return players[players['position'].str.contains(position)]

def get_player_stats(player_id: str) -> pd.DataFrame:
    """
    Get statistics for a specific player.
    
    Args:
        player_id: Player identifier
        
    Returns:
        DataFrame containing player statistics
    """
    stats = load_player_stats()
    return stats[stats['player_id'] == player_id]

def analyze_lineup(player_ids: List[str]) -> Dict[str, Any]:
    """
    Analyze a lineup and return statistical insights.
    
    Args:
        player_ids: List of player IDs in the lineup
        
    Returns:
        Dictionary with lineup analysis
    """
    players = load_player_data()
    stats = load_player_stats()
    
    lineup_players = players[players['player_id'].isin(player_ids)]
    lineup_stats = stats[stats['player_id'].isin(player_ids)]
    
    # If we have no stats, return basic info
    if lineup_stats.empty:
        return {
            'players': lineup_players.to_dict('records'),
            'avg_stats': {},
            'total_stats': {},
            'positions': lineup_players['position'].tolist(),
            'teams': lineup_players['team'].tolist()
        }
    
    # Calculate average and total stats
    avg_stats = lineup_stats.groupby('player_id').mean().mean()
    total_stats = lineup_stats.groupby('player_id').mean().sum()
    
    # Format stats dictionaries
    avg_stats_dict = {
        'pts': round(float(avg_stats['pts']) if 'pts' in avg_stats else 0, 1),
        'reb': round(float(avg_stats['reb']) if 'reb' in avg_stats else 0, 1),
        'ast': round(float(avg_stats['ast']) if 'ast' in avg_stats else 0, 1),
        'stl': round(float(avg_stats['stl']) if 'stl' in avg_stats else 0, 1),
        'blk': round(float(avg_stats['blk']) if 'blk' in avg_stats else 0, 1),
        'fg_pct': round(float(avg_stats['fg_pct']) if 'fg_pct' in avg_stats else 0, 3),
        'fg3_pct': round(float(avg_stats['fg3_pct']) if 'fg3_pct' in avg_stats else 0, 3)
    }
    
    total_stats_dict = {
        'pts': round(float(total_stats['pts']) if 'pts' in total_stats else 0, 1),
        'reb': round(float(total_stats['reb']) if 'reb' in total_stats else 0, 1),
        'ast': round(float(total_stats['ast']) if 'ast' in total_stats else 0, 1),
        'stl': round(float(total_stats['stl']) if 'stl' in total_stats else 0, 1),
        'blk': round(float(total_stats['blk']) if 'blk' in total_stats else 0, 1)
    }
    
    return {
        'players': lineup_players.to_dict('records'),
        'avg_stats': avg_stats_dict,
        'total_stats': total_stats_dict,
        'positions': lineup_players['position'].tolist(),
        'teams': lineup_players['team'].unique().tolist()
    }

def compare_lineups(lineup1_ids: List[str], lineup2_ids: List[str]) -> Dict[str, Any]:
    """
    Compare two lineups and return comparison statistics.
    
    Args:
        lineup1_ids: List of player IDs in the first lineup
        lineup2_ids: List of player IDs in the second lineup
        
    Returns:
        Dictionary with lineup comparison
    """
    lineup1_analysis = analyze_lineup(lineup1_ids)
    lineup2_analysis = analyze_lineup(lineup2_ids)
    
    # Compute differences
    stat_diff = {}
    for stat in lineup1_analysis['total_stats']:
        stat_diff[stat] = lineup1_analysis['total_stats'][stat] - lineup2_analysis['total_stats'][stat]
    
    return {
        'lineup1': lineup1_analysis,
        'lineup2': lineup2_analysis,
        'differences': stat_diff
    }

def get_player_radar_data(player_id: str) -> Dict[str, List[float]]:
    """
    Get normalized radar chart data for a player.
    
    Args:
        player_id: Player identifier
        
    Returns:
        Dictionary with radar chart data
    """
    stats = load_player_stats()
    
    player_stats = stats[stats['player_id'] == player_id]
    if player_stats.empty:
        return {
            'categories': ['PTS', 'REB', 'AST', 'STL', 'BLK', '3PT%'],
            'values': [0, 0, 0, 0, 0, 0]
        }
    
    # Calculate player's average stats
    avg_stats = player_stats.mean()
    
    # Define stat categories for radar chart
    categories = ['PTS', 'REB', 'AST', 'STL', 'BLK', '3PT%']
    stats_mapping = {
        'PTS': 'pts',
        'REB': 'reb',
        'AST': 'ast',
        'STL': 'stl',
        'BLK': 'blk',
        '3PT%': 'fg3_pct'
    }
    
    # Get all player stats for normalization
    all_player_avgs = stats.groupby('player_id').mean()
    
    # Normalize the values (percentile rank)
    values = []
    for cat in categories:
        stat_col = stats_mapping[cat]
        if stat_col in avg_stats and stat_col in all_player_avgs:
            # Get value
            val = avg_stats[stat_col]
            
            # Normalize to percentile (0-100)
            if cat == '3PT%':
                # For percentage stats, compare directly
                percentile = np.percentile(all_player_avgs[all_player_avgs[stat_col] > 0][stat_col], 100)
                norm_val = min(100, (val / percentile) * 100) if percentile > 0 else 0
            else:
                # For counting stats, use percentile rank
                rank = sum(all_player_avgs[stat_col] <= val) / len(all_player_avgs) * 100
                norm_val = rank
            
            values.append(norm_val)
        else:
            values.append(0)
    
    return {
        'categories': categories,
        'values': values
    }

def create_sample_player_data() -> pd.DataFrame:
    """
    Create sample player data for testing and demonstration.
    
    Returns:
        DataFrame containing sample player information
    """
    # Create sample data
    sample_data = [
        # Lakers
        {'player_id': 'lebron_james', 'name': 'LeBron James', 'position': 'SF', 'team': 'LAL', 'height': '6-9', 'weight': 250, 'age': 38},
        {'player_id': 'anthony_davis', 'name': 'Anthony Davis', 'position': 'PF', 'team': 'LAL', 'height': '6-10', 'weight': 253, 'age': 30},
        {'player_id': 'austin_reaves', 'name': 'Austin Reaves', 'position': 'SG', 'team': 'LAL', 'height': '6-5', 'weight': 197, 'age': 25},
        {'player_id': 'dangelo_russell', 'name': "D'Angelo Russell", 'position': 'PG', 'team': 'LAL', 'height': '6-4', 'weight': 193, 'age': 27},
        {'player_id': 'jarred_vanderbilt', 'name': 'Jarred Vanderbilt', 'position': 'PF', 'team': 'LAL', 'height': '6-8', 'weight': 214, 'age': 24},
        {'player_id': 'rui_hachimura', 'name': 'Rui Hachimura', 'position': 'PF', 'team': 'LAL', 'height': '6-8', 'weight': 230, 'age': 25},
        {'player_id': 'taurean_prince', 'name': 'Taurean Prince', 'position': 'SF', 'team': 'LAL', 'height': '6-6', 'weight': 218, 'age': 29},
        {'player_id': 'christian_wood', 'name': 'Christian Wood', 'position': 'C', 'team': 'LAL', 'height': '6-10', 'weight': 214, 'age': 28},
        {'player_id': 'gabe_vincent', 'name': 'Gabe Vincent', 'position': 'PG', 'team': 'LAL', 'height': '6-3', 'weight': 200, 'age': 27},
        {'player_id': 'jaxson_hayes', 'name': 'Jaxson Hayes', 'position': 'C', 'team': 'LAL', 'height': '7-0', 'weight': 220, 'age': 23},
        
        # Warriors
        {'player_id': 'stephen_curry', 'name': 'Stephen Curry', 'position': 'PG', 'team': 'GSW', 'height': '6-2', 'weight': 185, 'age': 35},
        {'player_id': 'klay_thompson', 'name': 'Klay Thompson', 'position': 'SG', 'team': 'GSW', 'height': '6-6', 'weight': 215, 'age': 33},
        {'player_id': 'draymond_green', 'name': 'Draymond Green', 'position': 'PF', 'team': 'GSW', 'height': '6-6', 'weight': 230, 'age': 33},
        {'player_id': 'andrew_wiggins', 'name': 'Andrew Wiggins', 'position': 'SF', 'team': 'GSW', 'height': '6-7', 'weight': 197, 'age': 28},
        {'player_id': 'kevon_looney', 'name': 'Kevon Looney', 'position': 'C', 'team': 'GSW', 'height': '6-9', 'weight': 222, 'age': 27},
        {'player_id': 'gary_payton', 'name': 'Gary Payton II', 'position': 'SG', 'team': 'GSW', 'height': '6-3', 'weight': 195, 'age': 30},
        {'player_id': 'jonathan_kuminga', 'name': 'Jonathan Kuminga', 'position': 'PF', 'team': 'GSW', 'height': '6-8', 'weight': 210, 'age': 21},
        {'player_id': 'moses_moody', 'name': 'Moses Moody', 'position': 'SG', 'team': 'GSW', 'height': '6-6', 'weight': 205, 'age': 21},
        {'player_id': 'chris_paul', 'name': 'Chris Paul', 'position': 'PG', 'team': 'GSW', 'height': '6-0', 'weight': 175, 'age': 38},
        {'player_id': 'brandin_podziemski', 'name': 'Brandin Podziemski', 'position': 'SG', 'team': 'GSW', 'height': '6-5', 'weight': 205, 'age': 20},
        
        # Celtics
        {'player_id': 'jayson_tatum', 'name': 'Jayson Tatum', 'position': 'SF', 'team': 'BOS', 'height': '6-8', 'weight': 210, 'age': 25},
        {'player_id': 'jaylen_brown', 'name': 'Jaylen Brown', 'position': 'SG', 'team': 'BOS', 'height': '6-6', 'weight': 223, 'age': 27},
        {'player_id': 'kristaps_porzingis', 'name': 'Kristaps Porzingis', 'position': 'C', 'team': 'BOS', 'height': '7-3', 'weight': 240, 'age': 28},
        {'player_id': 'jrue_holiday', 'name': 'Jrue Holiday', 'position': 'PG', 'team': 'BOS', 'height': '6-4', 'weight': 205, 'age': 33},
        {'player_id': 'derrick_white', 'name': 'Derrick White', 'position': 'SG', 'team': 'BOS', 'height': '6-4', 'weight': 190, 'age': 29},
        {'player_id': 'al_horford', 'name': 'Al Horford', 'position': 'PF', 'team': 'BOS', 'height': '6-9', 'weight': 240, 'age': 37},
        {'player_id': 'sam_hauser', 'name': 'Sam Hauser', 'position': 'SF', 'team': 'BOS', 'height': '6-8', 'weight': 217, 'age': 25},
        {'player_id': 'payton_pritchard', 'name': 'Payton Pritchard', 'position': 'PG', 'team': 'BOS', 'height': '6-1', 'weight': 195, 'age': 25},
        {'player_id': 'oshae_brissett', 'name': 'Oshae Brissett', 'position': 'SF', 'team': 'BOS', 'height': '6-7', 'weight': 210, 'age': 25},
        {'player_id': 'luke_kornet', 'name': 'Luke Kornet', 'position': 'C', 'team': 'BOS', 'height': '7-2', 'weight': 250, 'age': 28},
        
        # Nuggets
        {'player_id': 'nikola_jokic', 'name': 'Nikola Jokic', 'position': 'C', 'team': 'DEN', 'height': '6-11', 'weight': 284, 'age': 28},
        {'player_id': 'jamal_murray', 'name': 'Jamal Murray', 'position': 'PG', 'team': 'DEN', 'height': '6-4', 'weight': 215, 'age': 26},
        {'player_id': 'aaron_gordon', 'name': 'Aaron Gordon', 'position': 'PF', 'team': 'DEN', 'height': '6-8', 'weight': 235, 'age': 28},
        {'player_id': 'michael_porter', 'name': 'Michael Porter Jr.', 'position': 'SF', 'team': 'DEN', 'height': '6-10', 'weight': 218, 'age': 25},
        {'player_id': 'kentavious_caldwell_pope', 'name': 'Kentavious Caldwell-Pope', 'position': 'SG', 'team': 'DEN', 'height': '6-5', 'weight': 204, 'age': 30},
        {'player_id': 'russell_westbrook', 'name': 'Russell Westbrook', 'position': 'PG', 'team': 'DEN', 'height': '6-3', 'weight': 200, 'age': 35},
        {'player_id': 'bruce_brown', 'name': 'Bruce Brown', 'position': 'SG', 'team': 'DEN', 'height': '6-4', 'weight': 202, 'age': 27},
        {'player_id': 'reggie_jackson', 'name': 'Reggie Jackson', 'position': 'PG', 'team': 'DEN', 'height': '6-2', 'weight': 208, 'age': 33},
        {'player_id': 'deandre_jordan', 'name': "DeAndre Jordan", 'position': 'C', 'team': 'DEN', 'height': '6-11', 'weight': 265, 'age': 35},
        {'player_id': 'jeff_green', 'name': 'Jeff Green', 'position': 'PF', 'team': 'DEN', 'height': '6-8', 'weight': 235, 'age': 37}
    ]
    
    # Create DataFrame
    df = pd.DataFrame(sample_data)
    
    # Ensure the data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Save to CSV
    df.to_csv('data/players.csv', index=False)
    
    return df

def create_sample_player_stats() -> pd.DataFrame:
    """
    Create sample player statistics for testing and demonstration.
    
    Returns:
        DataFrame containing sample player statistics
    """
    # Create player list from sample player data
    players_df = create_sample_player_data()
    player_ids = players_df['player_id'].tolist()
    
    # Create sample stats for each player
    all_stats = []
    
    for player_id in player_ids:
        # Get player info
        player = players_df[players_df['player_id'] == player_id].iloc[0]
        position = player['position']
        
        # Base stats by position (approximates of realistic stats)
        position_stats = {
            'PG': {'pts': 16, 'reb': 3, 'ast': 7, 'stl': 1.2, 'blk': 0.3, 'fg_pct': 0.44, 'fg3_pct': 0.36, 'ft_pct': 0.85, 'tov': 2.5},
            'SG': {'pts': 18, 'reb': 4, 'ast': 3, 'stl': 1.0, 'blk': 0.5, 'fg_pct': 0.45, 'fg3_pct': 0.38, 'ft_pct': 0.82, 'tov': 2.0},
            'SF': {'pts': 17, 'reb': 5.5, 'ast': 2.5, 'stl': 1.0, 'blk': 0.6, 'fg_pct': 0.47, 'fg3_pct': 0.35, 'ft_pct': 0.78, 'tov': 1.8},
            'PF': {'pts': 15, 'reb': 7, 'ast': 2, 'stl': 0.7, 'blk': 1.0, 'fg_pct': 0.50, 'fg3_pct': 0.32, 'ft_pct': 0.75, 'tov': 1.5},
            'C': {'pts': 13, 'reb': 9, 'ast': 1.5, 'stl': 0.5, 'blk': 1.5, 'fg_pct': 0.58, 'fg3_pct': 0.25, 'ft_pct': 0.70, 'tov': 1.8}
        }
        
        # Get base stats for position
        pos = position.split('-')[0] if '-' in position else position.split('/')[0] if '/' in position else position
        base_stats = position_stats.get(pos, position_stats['SF'])
        
        # Handle special cases for star players
        if player_id == 'lebron_james':
            base_stats = {'pts': 25.5, 'reb': 7.8, 'ast': 7.5, 'stl': 1.3, 'blk': 0.8, 'fg_pct': 0.52, 'fg3_pct': 0.35, 'ft_pct': 0.73, 'tov': 3.5}
        elif player_id == 'stephen_curry':
            base_stats = {'pts': 29.5, 'reb': 5.5, 'ast': 6.2, 'stl': 1.2, 'blk': 0.2, 'fg_pct': 0.47, 'fg3_pct': 0.43, 'ft_pct': 0.92, 'tov': 3.0}
        elif player_id == 'nikola_jokic':
            base_stats = {'pts': 24.5, 'reb': 11.5, 'ast': 9.8, 'stl': 1.3, 'blk': 0.7, 'fg_pct': 0.57, 'fg3_pct': 0.35, 'ft_pct': 0.83, 'tov': 3.2}
        elif player_id == 'anthony_davis':
            base_stats = {'pts': 24.0, 'reb': 12.5, 'ast': 2.8, 'stl': 1.2, 'blk': 2.3, 'fg_pct': 0.55, 'fg3_pct': 0.28, 'ft_pct': 0.78, 'tov': 2.0}
        elif player_id == 'jayson_tatum':
            base_stats = {'pts': 27.8, 'reb': 8.5, 'ast': 4.5, 'stl': 1.0, 'blk': 0.7, 'fg_pct': 0.47, 'fg3_pct': 0.37, 'ft_pct': 0.85, 'tov': 2.8}
        
        # Create 10 game stats with some variation
        for game_id in range(1, 11):
            # Add random variation to stats
            game_stats = {
                'player_id': player_id,
                'game_id': f'game_{game_id}',
                'pts': max(0, np.random.normal(base_stats['pts'], base_stats['pts'] * 0.2)),
                'reb': max(0, np.random.normal(base_stats['reb'], base_stats['reb'] * 0.3)),
                'ast': max(0, np.random.normal(base_stats['ast'], base_stats['ast'] * 0.3)),
                'stl': max(0, np.random.normal(base_stats['stl'], 0.7)),
                'blk': max(0, np.random.normal(base_stats['blk'], 0.7)),
                'fg_pct': min(1.0, max(0, np.random.normal(base_stats['fg_pct'], 0.08))),
                'fg3_pct': min(1.0, max(0, np.random.normal(base_stats['fg3_pct'], 0.1))),
                'ft_pct': min(1.0, max(0, np.random.normal(base_stats['ft_pct'], 0.09))),
                'tov': max(0, np.random.normal(base_stats['tov'], 1.2))
            }
            
            all_stats.append(game_stats)
    
    # Create DataFrame
    df = pd.DataFrame(all_stats)
    
    # Round values to reasonable precision
    for col in ['pts', 'reb', 'ast', 'stl', 'blk', 'tov']:
        df[col] = df[col].round(1)
    
    for col in ['fg_pct', 'fg3_pct', 'ft_pct']:
        df[col] = df[col].round(3)
    
    # Ensure the data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Save to CSV
    df.to_csv('data/player_stats.csv', index=False)
    
    return df

def create_sample_team_data() -> pd.DataFrame:
    """
    Create sample team data for testing and demonstration.
    
    Returns:
        DataFrame containing sample team information
    """
    # Create sample data
    sample_data = [
        {'team_id': 'LAL', 'name': 'Los Angeles Lakers', 'conference': 'West', 'division': 'Pacific', 'wins': 43, 'losses': 39},
        {'team_id': 'GSW', 'name': 'Golden State Warriors', 'conference': 'West', 'division': 'Pacific', 'wins': 44, 'losses': 38},
        {'team_id': 'BOS', 'name': 'Boston Celtics', 'conference': 'East', 'division': 'Atlantic', 'wins': 57, 'losses': 25},
        {'team_id': 'DEN', 'name': 'Denver Nuggets', 'conference': 'West', 'division': 'Northwest', 'wins': 53, 'losses': 29}
    ]
    
    # Create DataFrame
    df = pd.DataFrame(sample_data)
    
    # Ensure the data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Save to CSV
    df.to_csv('data/teams.csv', index=False)
    
    return df 