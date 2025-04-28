import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple

def calculate_lineup_offensive_rating(player_ids: List[str], player_stats: pd.DataFrame) -> float:
    """
    Calculate the offensive rating for a lineup based on player stats.
    
    Args:
        player_ids: List of player IDs in the lineup
        player_stats: DataFrame containing player statistics
        
    Returns:
        Offensive rating score from 0 to 100
    """
    if not player_ids or len(player_ids) == 0:
        return 0.0
    
    # Filter stats for the players in the lineup
    lineup_stats = player_stats[player_stats['player_id'].isin(player_ids)]
    
    if lineup_stats.empty:
        return 50.0  # Default score if no stats available
    
    # Calculate average stats for the lineup
    avg_lineup_stats = lineup_stats.groupby('player_id').mean().reset_index()
    
    # Create offensive metrics based on key offensive stats
    avg_pts = avg_lineup_stats['pts'].mean()
    avg_ast = avg_lineup_stats['ast'].mean()
    avg_fg_pct = avg_lineup_stats['fg_pct'].mean()
    avg_fg3_pct = avg_lineup_stats['fg3_pct'].mean()
    
    # Calculate offensive rating based on weighted stats
    off_rating = (
        (avg_pts * 0.5) +  # Points are very important
        (avg_ast * 1.5) +  # Assists are crucial for team offense
        (avg_fg_pct * 40) +  # Field goal percentage (scaled up)
        (avg_fg3_pct * 60)   # Three-point percentage (scaled up)
    )
    
    # Normalize to 0-100 scale (assuming maximum realistic rating of 60)
    normalized_rating = min(100, (off_rating / 60) * 100)
    
    return normalized_rating

def calculate_lineup_defensive_rating(player_ids: List[str], player_stats: pd.DataFrame) -> float:
    """
    Calculate the defensive rating for a lineup based on player stats.
    
    Args:
        player_ids: List of player IDs in the lineup
        player_stats: DataFrame containing player statistics
        
    Returns:
        Defensive rating score from 0 to 100
    """
    if not player_ids or len(player_ids) == 0:
        return 0.0
    
    # Filter stats for the players in the lineup
    lineup_stats = player_stats[player_stats['player_id'].isin(player_ids)]
    
    if lineup_stats.empty:
        return 50.0  # Default score if no stats available
    
    # Calculate average stats for the lineup
    avg_lineup_stats = lineup_stats.groupby('player_id').mean().reset_index()
    
    # Create defensive metrics based on key defensive stats
    avg_stl = avg_lineup_stats['stl'].mean()
    avg_blk = avg_lineup_stats['blk'].mean()
    avg_reb = avg_lineup_stats['reb'].mean()
    
    # Calculate defensive rating based on weighted stats
    def_rating = (
        (avg_stl * 5) +     # Steals are very valuable
        (avg_blk * 5) +     # Blocks are very valuable
        (avg_reb * 1.5)     # Rebounds are important for defense
    )
    
    # Normalize to 0-100 scale (assuming maximum realistic rating of 30)
    normalized_rating = min(100, (def_rating / 30) * 100)
    
    return normalized_rating

def calculate_lineup_efficiency(player_ids: List[str], player_stats: pd.DataFrame) -> float:
    """
    Calculate the efficiency rating for a lineup based on player stats.
    
    Args:
        player_ids: List of player IDs in the lineup
        player_stats: DataFrame containing player statistics
        
    Returns:
        Efficiency rating score from 0 to 100
    """
    if not player_ids or len(player_ids) == 0:
        return 0.0
    
    # Filter stats for the players in the lineup
    lineup_stats = player_stats[player_stats['player_id'].isin(player_ids)]
    
    if lineup_stats.empty:
        return 50.0  # Default score if no stats available
    
    # Calculate average stats for the lineup
    avg_lineup_stats = lineup_stats.groupby('player_id').mean().reset_index()
    
    # Create efficiency metrics based on key efficiency stats
    avg_fg_pct = avg_lineup_stats['fg_pct'].mean()
    avg_ft_pct = avg_lineup_stats['ft_pct'].mean() if 'ft_pct' in avg_lineup_stats.columns else 0.75  # Default if missing
    avg_to = avg_lineup_stats['to'].mean() if 'to' in avg_lineup_stats.columns else 2.5  # Default if missing
    
    # Calculate efficiency rating based on weighted stats
    eff_rating = (
        (avg_fg_pct * 50) +  # Field goal percentage (scaled up)
        (avg_ft_pct * 30) -  # Free throw percentage (scaled up)
        (avg_to * 5)         # Turnovers are negative
    )
    
    # Normalize to 0-100 scale (assuming maximum realistic rating of 50)
    normalized_rating = min(100, max(0, (eff_rating / 50) * 100))
    
    return normalized_rating

def calculate_lineup_versatility(player_ids: List[str], player_stats: pd.DataFrame) -> float:
    """
    Calculate the versatility rating for a lineup based on how well-rounded the players are.
    
    Args:
        player_ids: List of player IDs in the lineup
        player_stats: DataFrame containing player statistics
        
    Returns:
        Versatility rating score from 0 to 100
    """
    if not player_ids or len(player_ids) == 0:
        return 0.0
    
    # Filter stats for the players in the lineup
    lineup_stats = player_stats[player_stats['player_id'].isin(player_ids)]
    
    if lineup_stats.empty:
        return 50.0  # Default score if no stats available
    
    # Calculate average stats for each player
    player_avgs = lineup_stats.groupby('player_id').mean()
    
    # Define key statistical categories
    stat_categories = ['pts', 'reb', 'ast', 'stl', 'blk', 'fg3m']
    
    # Calculate versatility for each player
    player_versatility = []
    for _, player_stats in player_avgs.iterrows():
        # Count categories where player is above average
        above_avg_count = 0
        for stat in stat_categories:
            if stat in player_stats:
                threshold = {
                    'pts': 12.0,   # Points threshold
                    'reb': 5.0,    # Rebounds threshold
                    'ast': 3.0,    # Assists threshold
                    'stl': 1.0,    # Steals threshold
                    'blk': 0.5,    # Blocks threshold
                    'fg3m': 1.0    # Three-pointers made threshold
                }
                if player_stats[stat] >= threshold[stat]:
                    above_avg_count += 1
        
        # Calculate versatility percentage
        versatility_pct = above_avg_count / len(stat_categories)
        player_versatility.append(versatility_pct)
    
    # Calculate average versatility across lineup
    avg_versatility = sum(player_versatility) / len(player_versatility) if player_versatility else 0.5
    
    # Score from 0-100
    versatility_score = avg_versatility * 100
    
    return versatility_score

def calculate_lineup_compatibility(player_ids: List[str], player_stats: pd.DataFrame, player_info: pd.DataFrame) -> float:
    """
    Calculate how compatible the players in a lineup are based on complementary skills.
    
    Args:
        player_ids: List of player IDs in the lineup
        player_stats: DataFrame containing player statistics
        player_info: DataFrame containing player information
        
    Returns:
        Compatibility rating from 0 to 100
    """
    if not player_ids or len(player_ids) < 2:
        return 50.0  # Default for small lineups
    
    # Filter data for the given player IDs
    lineup_stats = player_stats[player_stats['player_id'].isin(player_ids)]
    lineup_info = player_info[player_info['player_id'].isin(player_ids)]
    
    if lineup_stats.empty or lineup_info.empty:
        return 50.0  # Default score if data is missing
    
    # Group by player and get average stats
    player_avgs = lineup_stats.groupby('player_id').mean().reset_index()
    
    # Calculate compatibility score based on complementary skills
    compatibility_score = 0
    
    # 1. Check for skill diversity (25%)
    # Identify roles
    scorers = player_avgs[player_avgs['pts'] > 15].shape[0]
    passers = player_avgs[player_avgs['ast'] > 4].shape[0]
    defenders = player_avgs[(player_avgs['stl'] + player_avgs['blk']) > 1.5].shape[0]
    rebounders = player_avgs[player_avgs['reb'] > 6].shape[0]
    shooters = player_avgs[player_avgs['fg3_pct'] > 0.35].shape[0]
    
    # Assess diversity score
    role_diversity = min(scorers, 3) + min(passers, 2) + min(defenders, 2) + min(rebounders, 2) + min(shooters, 3)
    max_role_diversity = 12  # Maximum possible sum
    diversity_score = (role_diversity / max_role_diversity) * 25
    compatibility_score += diversity_score
    
    # 2. Position compatibility (25%)
    positions = lineup_info['position'].tolist()
    position_categories = {
        'PG': 'Guard',
        'SG': 'Guard',
        'SF': 'Forward',
        'PF': 'Forward',
        'C': 'Center'
    }
    
    # Convert to category counts
    position_category_counts = {'Guard': 0, 'Forward': 0, 'Center': 0}
    for pos in positions:
        if pos in position_categories:
            category = position_categories[pos]
            position_category_counts[category] += 1
    
    # Ideal distribution: 2 guards, 2 forwards, 1 center
    position_score = 25
    if position_category_counts['Guard'] < 1 or position_category_counts['Guard'] > 3:
        position_score -= 8
    if position_category_counts['Forward'] < 1 or position_category_counts['Forward'] > 3:
        position_score -= 8
    if position_category_counts['Center'] < 1 or position_category_counts['Center'] > 2:
        position_score -= 9
    
    compatibility_score += position_score
    
    # 3. Playing style compatibility (25%)
    # High assist/turnover ratio is good for compatibility
    ast_to_ratio = player_avgs['ast'].sum() / max(1, player_avgs['to'].sum() if 'to' in player_avgs.columns else 10)
    
    # Calculate style score
    style_score = min(25, ast_to_ratio * 5)
    compatibility_score += style_score
    
    # 4. Team synergy (25%)
    # Players from the same team might have better compatibility
    teams = lineup_info['team'].tolist()
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
    compatibility_score += synergy_score
    
    # Ensure score is within 0-100 range
    return max(0, min(100, compatibility_score))

def calculate_lineup_rating(player_ids: List[str], player_stats: pd.DataFrame, player_info: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate an overall rating and component ratings for a lineup.
    
    Args:
        player_ids: List of player IDs in the lineup
        player_stats: DataFrame containing player statistics
        player_info: DataFrame containing player information
        
    Returns:
        Dictionary containing overall rating and component ratings
    """
    # Calculate component ratings
    offensive_rating = calculate_lineup_offensive_rating(player_ids, player_stats)
    defensive_rating = calculate_lineup_defensive_rating(player_ids, player_stats)
    efficiency_rating = calculate_lineup_efficiency(player_ids, player_stats)
    versatility_rating = calculate_lineup_versatility(player_ids, player_stats)
    compatibility_rating = calculate_lineup_compatibility(player_ids, player_stats, player_info)
    
    # Calculate overall rating with weighting
    overall_rating = (
        offensive_rating * 0.35 +
        defensive_rating * 0.25 +
        efficiency_rating * 0.15 +
        versatility_rating * 0.1 +
        compatibility_rating * 0.15
    )
    
    # Return all ratings
    return {
        'overall': overall_rating,
        'offense': offensive_rating,
        'defense': defensive_rating,
        'efficiency': efficiency_rating,
        'versatility': versatility_rating,
        'compatibility': compatibility_rating
    }

def get_lineup_strengths_weaknesses(lineup_ratings: Dict[str, float]) -> Tuple[List[str], List[str]]:
    """
    Analyze a lineup's ratings to determine its strengths and weaknesses.
    
    Args:
        lineup_ratings: Dictionary of ratings returned by calculate_lineup_rating
        
    Returns:
        Tuple of (strengths, weaknesses) as lists of strings
    """
    strengths = []
    weaknesses = []
    
    # Define thresholds
    strength_threshold = 70
    weakness_threshold = 40
    
    # Check each rating component
    component_names = {
        'offense': 'Offensive production',
        'defense': 'Defensive capability',
        'efficiency': 'Shooting efficiency',
        'versatility': 'Player versatility',
        'compatibility': 'Team chemistry'
    }
    
    for component, name in component_names.items():
        if component in lineup_ratings:
            rating = lineup_ratings[component]
            if rating >= strength_threshold:
                strengths.append(name)
            elif rating <= weakness_threshold:
                weaknesses.append(name)
    
    # Add overall assessment if not already covered
    overall = lineup_ratings.get('overall', 50)
    if overall >= 80 and 'Overall excellence' not in strengths:
        strengths.append('Overall excellence')
    elif overall <= 30 and 'Overall performance' not in weaknesses:
        weaknesses.append('Overall performance')
    
    return strengths, weaknesses

def compare_lineups(lineup1_ids: List[str], lineup2_ids: List[str], 
                    player_stats: pd.DataFrame, player_info: pd.DataFrame) -> Dict[str, Any]:
    """
    Compare two lineups and show where one outperforms the other.
    
    Args:
        lineup1_ids: List of player IDs for first lineup
        lineup2_ids: List of player IDs for second lineup
        player_stats: DataFrame containing player statistics
        player_info: DataFrame containing player information
        
    Returns:
        Dictionary with comparison results
    """
    # Calculate ratings for both lineups
    lineup1_ratings = calculate_lineup_rating(lineup1_ids, player_stats, player_info)
    lineup2_ratings = calculate_lineup_rating(lineup2_ids, player_stats, player_info)
    
    # Determine differences
    rating_diffs = {
        key: lineup1_ratings[key] - lineup2_ratings[key] 
        for key in lineup1_ratings
        if key in lineup2_ratings
    }
    
    # Determine which lineup is better overall
    lineup1_better = lineup1_ratings['overall'] > lineup2_ratings['overall']
    
    # Calculate advantage percentage
    overall_advantage = abs(lineup1_ratings['overall'] - lineup2_ratings['overall'])
    
    # Determine key advantages (components with >10 point difference)
    advantages = []
    for component, diff in rating_diffs.items():
        if abs(diff) >= 10:
            if diff > 0:
                advantages.append({
                    'component': component,
                    'lineup': 1,
                    'difference': diff
                })
            else:
                advantages.append({
                    'component': component,
                    'lineup': 2,
                    'difference': -diff
                })
    
    # Sort advantages by magnitude
    advantages.sort(key=lambda x: x['difference'], reverse=True)
    
    return {
        'lineup1_ratings': lineup1_ratings,
        'lineup2_ratings': lineup2_ratings,
        'lineup1_better': lineup1_better,
        'overall_advantage': overall_advantage,
        'key_advantages': advantages,
        'lineup1_strengths': get_lineup_strengths_weaknesses(lineup1_ratings)[0],
        'lineup1_weaknesses': get_lineup_strengths_weaknesses(lineup1_ratings)[1],
        'lineup2_strengths': get_lineup_strengths_weaknesses(lineup2_ratings)[0],
        'lineup2_weaknesses': get_lineup_strengths_weaknesses(lineup2_ratings)[1]
    } 