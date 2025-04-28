import pandas as pd
import os
import json
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import playergamelog, commonplayerinfo, teamgamelog, commonallplayers, leaguedashplayerstats
import time
import random
from datetime import datetime, timedelta
import numpy as np

# Paths for cached data
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
PLAYERS_FILE = os.path.join(DATA_DIR, 'players.csv')
PLAYER_STATS_FILE = os.path.join(DATA_DIR, 'player_stats.csv')
TEAMS_FILE = os.path.join(DATA_DIR, 'teams.csv')

def load_nba_players():
    """
    Load NBA player data with caching.
    Checks if the data is cached, if not creates sample data.
    
    Returns:
        DataFrame containing player information
    """
    # Check if data exists in cache
    players_path = os.path.join('data', 'players.csv')
    
    if not os.path.exists(players_path):
        # If not cached, create sample data
        print("No player data found. Creating sample data...")
        players_df = create_sample_player_data()
    else:
        # Load cached data
        print("Loading players from cache...")
        players_df = pd.read_csv(players_path)
        
    # Check if we need to enhance the dataset
    if len(players_df) < 200:  # Less than 200 players means we should enhance
        print("Current dataset has only", len(players_df), "players. Enhancing dataset...")
        players_df = enhance_player_dataset()
    
    return players_df

def load_player_stats():
    """
    Load player statistics, prioritizing sample data for speed.
    
    Returns:
        pandas.DataFrame: DataFrame with player statistics
    """
    # Check if we have cached data
    if os.path.exists(PLAYER_STATS_FILE):
        print("Loading player stats from cache...")
        return pd.read_csv(PLAYER_STATS_FILE)
    
    print("Creating sample player statistics...")
    return create_sample_player_stats()

def load_team_data():
    """
    Load team data, either from cache or sample data.
    
    Returns:
        pandas.DataFrame: DataFrame with team data
    """
    # Check if we have cached data
    if os.path.exists(TEAMS_FILE):
        print("Loading teams from cache...")
        return pd.read_csv(TEAMS_FILE)
    
    print("Creating sample team data...")
    return create_sample_teams()

def create_sample_players():
    """
    Create sample player data with real NBA player names and teams.
    
    Returns:
        pandas.DataFrame: DataFrame with sample player data
    """
    print("Creating sample player data with real NBA players...")
    
    # Get real team data from static resource (this is fast)
    nba_teams = teams.get_teams()
    teams_dict = {team['id']: team['full_name'] for team in nba_teams}
    
    # Real NBA player data (2023-2024 season)
    real_players = [
        # Lakers
        {"name": "LeBron James", "team_id": 1610612747, "position": "SF/PF", "height": "6'9\"", "weight": 250, "age": 39},
        {"name": "Anthony Davis", "team_id": 1610612747, "position": "PF/C", "weight": 253, "height": "6'10\"", "age": 31},
        {"name": "D'Angelo Russell", "team_id": 1610612747, "position": "PG", "weight": 193, "height": "6'4\"", "age": 28},
        {"name": "Austin Reaves", "team_id": 1610612747, "position": "SG", "weight": 197, "height": "6'5\"", "age": 25},
        {"name": "Rui Hachimura", "team_id": 1610612747, "position": "PF", "weight": 230, "height": "6'8\"", "age": 26},
        
        # Celtics
        {"name": "Jayson Tatum", "team_id": 1610612738, "position": "SF/PF", "weight": 210, "height": "6'8\"", "age": 26},
        {"name": "Jaylen Brown", "team_id": 1610612738, "position": "SG/SF", "weight": 223, "height": "6'6\"", "age": 27},
        {"name": "Jrue Holiday", "team_id": 1610612738, "position": "PG/SG", "weight": 205, "height": "6'4\"", "age": 33},
        {"name": "Kristaps Porzingis", "team_id": 1610612738, "position": "C/PF", "weight": 240, "height": "7'2\"", "age": 28},
        {"name": "Derrick White", "team_id": 1610612738, "position": "PG/SG", "weight": 190, "height": "6'4\"", "age": 29},
        
        # Warriors
        {"name": "Stephen Curry", "team_id": 1610612744, "position": "PG", "weight": 185, "height": "6'2\"", "age": 36},
        {"name": "Klay Thompson", "team_id": 1610612744, "position": "SG", "weight": 215, "height": "6'6\"", "age": 34},
        {"name": "Draymond Green", "team_id": 1610612744, "position": "PF", "weight": 230, "height": "6'6\"", "age": 34},
        {"name": "Andrew Wiggins", "team_id": 1610612744, "position": "SF", "weight": 197, "height": "6'7\"", "age": 29},
        {"name": "Jonathan Kuminga", "team_id": 1610612744, "position": "PF", "weight": 210, "height": "6'7\"", "age": 21},
        
        # Bucks
        {"name": "Giannis Antetokounmpo", "team_id": 1610612749, "position": "PF", "weight": 242, "height": "6'11\"", "age": 29},
        {"name": "Damian Lillard", "team_id": 1610612749, "position": "PG", "weight": 195, "height": "6'2\"", "age": 33},
        {"name": "Khris Middleton", "team_id": 1610612749, "position": "SF", "weight": 222, "height": "6'7\"", "age": 32},
        {"name": "Brook Lopez", "team_id": 1610612749, "position": "C", "weight": 282, "height": "7'0\"", "age": 36},
        {"name": "Bobby Portis", "team_id": 1610612749, "position": "PF/C", "weight": 250, "height": "6'10\"", "age": 29},
        
        # Nuggets
        {"name": "Nikola Jokic", "team_id": 1610612743, "position": "C", "weight": 284, "height": "6'11\"", "age": 29},
        {"name": "Jamal Murray", "team_id": 1610612743, "position": "PG", "weight": 215, "height": "6'4\"", "age": 27},
        {"name": "Michael Porter Jr.", "team_id": 1610612743, "position": "SF", "weight": 218, "height": "6'10\"", "age": 25},
        {"name": "Aaron Gordon", "team_id": 1610612743, "position": "PF", "weight": 235, "height": "6'8\"", "age": 28},
        {"name": "Kentavious Caldwell-Pope", "team_id": 1610612743, "position": "SG", "weight": 204, "height": "6'5\"", "age": 31},
    ]
    
    # Add more players from other teams to get 360 total players
    for team in nba_teams:
        # Skip teams we've already added manually
        if team['id'] in [1610612747, 1610612738, 1610612744, 1610612749, 1610612743]:
            continue
            
        # Add players for each remaining team based on positions
        positions = ['PG', 'SG', 'SF', 'PF', 'C', 'PG/SG', 'SG/SF', 'SF/PF', 'PF/C']
        team_name = team['full_name']
        team_id = team['id']
        
        # Add key players from real NBA teams
        if team['full_name'] == 'Philadelphia 76ers':
            real_players.extend([
                {"name": "Joel Embiid", "team_id": team_id, "position": "C", "weight": 280, "height": "7'0\"", "age": 30},
                {"name": "Tyrese Maxey", "team_id": team_id, "position": "PG", "weight": 200, "height": "6'2\"", "age": 23},
                {"name": "Tobias Harris", "team_id": team_id, "position": "PF", "weight": 226, "height": "6'8\"", "age": 31},
            ])
        elif team['full_name'] == 'Dallas Mavericks':
            real_players.extend([
                {"name": "Luka Doncic", "team_id": team_id, "position": "PG/SF", "weight": 230, "height": "6'7\"", "age": 25},
                {"name": "Kyrie Irving", "team_id": team_id, "position": "PG", "weight": 195, "height": "6'2\"", "age": 32},
                {"name": "Tim Hardaway Jr.", "team_id": team_id, "position": "SG/SF", "weight": 205, "height": "6'5\"", "age": 32},
            ])
        elif team['full_name'] == 'Phoenix Suns':
            real_players.extend([
                {"name": "Kevin Durant", "team_id": team_id, "position": "SF/PF", "weight": 240, "height": "6'10\"", "age": 35},
                {"name": "Devin Booker", "team_id": team_id, "position": "SG", "weight": 206, "height": "6'5\"", "age": 27},
                {"name": "Bradley Beal", "team_id": team_id, "position": "SG", "weight": 207, "height": "6'4\"", "age": 30},
            ])
        # Add remaining teams - just adding a few key players for each to save space
        # The full list would be too long for this example
        else:
            # For other teams, add 3 players with realistic positions
            for i in range(3):
                position = positions[i % len(positions)]
                real_players.append({
                    "name": f"{team_name} Player {i+1}",  # Generic name for other players
                    "team_id": team_id,
                    "position": position,
                    "weight": random.randint(180, 280),
                    "height": f"{random.randint(5, 7)}'{random.randint(0, 11)}",
                    "age": random.randint(20, 35)
                })
    
    # Create full player records with IDs and consistent fields
    sample_players = []
    player_id = 1000
    
    for player in real_players:
        # Split name into first/last
        name_parts = player["name"].split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""
        
        # Create complete player record
        player_record = {
            'player_id': player_id,
            'name': player["name"],
            'first_name': first_name,
            'last_name': last_name,
            'active': True,
            'height': player.get("height", "6'0\""),
            'weight': player.get("weight", 200),
            'position': player.get("position", ""),
            'team_id': player["team_id"],
            'team': teams_dict.get(player["team_id"], ""),
            'age': player.get("age", 25),
            'from_year': datetime.now().year - random.randint(1, 15)
        }
        
        sample_players.append(player_record)
        player_id += 1
    
    # Create a DataFrame
    players_df = pd.DataFrame(sample_players)
    
    # Save to cache for future use
    os.makedirs(DATA_DIR, exist_ok=True)
    players_df.to_csv(PLAYERS_FILE, index=False)
    
    return players_df

def create_sample_teams():
    """
    Create sample team data for demonstration purposes.
    
    Returns:
        pandas.DataFrame: DataFrame with sample team data
    """
    print("Creating sample team data...")
    
    # Get real team data from static resource (this is fast)
    nba_teams = teams.get_teams()
    teams_df = pd.DataFrame(nba_teams)
    
    # Rename columns for consistency
    teams_df = teams_df.rename(columns={
        'id': 'team_id',
        'full_name': 'name',
        'abbreviation': 'abbreviation',
        'nickname': 'nickname',
        'city': 'city',
        'state': 'state',
        'year_founded': 'year_founded'
    })
    
    # Save to cache
    os.makedirs(DATA_DIR, exist_ok=True)
    teams_df.to_csv(TEAMS_FILE, index=False)
    
    return teams_df

def create_sample_player_stats():
    """
    Create sample player statistics with realistic distributions based on player positions.
    
    Returns:
        pandas.DataFrame: DataFrame with sample player statistics
    """
    print("Creating sample player statistics...")
    
    # Load or create sample players
    if os.path.exists(PLAYERS_FILE):
        players_df = pd.read_csv(PLAYERS_FILE)
    else:
        players_df = create_sample_players()
    
    # Create sample data for each player
    all_stats = []
    
    # Real NBA player stat ranges based on position and player caliber
    star_ranges = {
        'PG': {'pts': (22, 32), 'reb': (4, 7), 'ast': (6, 11), 'stl': (1, 2.5), 'blk': (0, 1), 
               'fg_pct': (0.44, 0.52), 'fg3_pct': (0.36, 0.44), 'ft_pct': (0.85, 0.92)},
        'SG': {'pts': (20, 30), 'reb': (4, 6), 'ast': (4, 7), 'stl': (1, 2.5), 'blk': (0.5, 1.5), 
               'fg_pct': (0.44, 0.50), 'fg3_pct': (0.37, 0.44), 'ft_pct': (0.83, 0.90)},
        'SF': {'pts': (19, 28), 'reb': (5, 9), 'ast': (3, 7), 'stl': (1, 2), 'blk': (0.5, 1.5), 
               'fg_pct': (0.45, 0.54), 'fg3_pct': (0.35, 0.43), 'ft_pct': (0.80, 0.88)},
        'PF': {'pts': (17, 27), 'reb': (7, 12), 'ast': (2, 5), 'stl': (0.5, 1.5), 'blk': (0.8, 2.2), 
               'fg_pct': (0.48, 0.56), 'fg3_pct': (0.30, 0.38), 'ft_pct': (0.75, 0.85)},
        'C':  {'pts': (15, 25), 'reb': (9, 14), 'ast': (1, 4), 'stl': (0.5, 1.2), 'blk': (1.5, 3), 
               'fg_pct': (0.55, 0.65), 'fg3_pct': (0.25, 0.35), 'ft_pct': (0.65, 0.80)}
    }
    
    role_ranges = {
        'PG': {'pts': (9, 15), 'reb': (2, 4), 'ast': (3, 6), 'stl': (0.5, 1.5), 'blk': (0, 0.5), 
               'fg_pct': (0.40, 0.46), 'fg3_pct': (0.32, 0.39), 'ft_pct': (0.75, 0.85)},
        'SG': {'pts': (8, 15), 'reb': (2, 5), 'ast': (1.5, 3.5), 'stl': (0.5, 1.2), 'blk': (0.2, 0.8), 
               'fg_pct': (0.40, 0.46), 'fg3_pct': (0.34, 0.40), 'ft_pct': (0.78, 0.85)},
        'SF': {'pts': (8, 14), 'reb': (3, 6), 'ast': (1, 3), 'stl': (0.5, 1.2), 'blk': (0.3, 0.8), 
               'fg_pct': (0.42, 0.48), 'fg3_pct': (0.32, 0.38), 'ft_pct': (0.75, 0.83)},
        'PF': {'pts': (7, 13), 'reb': (4, 8), 'ast': (0.8, 2.5), 'stl': (0.3, 1), 'blk': (0.5, 1.5), 
               'fg_pct': (0.45, 0.53), 'fg3_pct': (0.28, 0.35), 'ft_pct': (0.70, 0.80)},
        'C':  {'pts': (7, 12), 'reb': (5, 9), 'ast': (0.5, 2), 'stl': (0.2, 0.8), 'blk': (0.8, 2), 
               'fg_pct': (0.52, 0.60), 'fg3_pct': (0.18, 0.30), 'ft_pct': (0.60, 0.75)}
    }
    
    # Star players by name - realistic stats for known NBA stars
    star_players = [
        "LeBron James", "Anthony Davis", "Stephen Curry", "Klay Thompson", "Draymond Green", 
        "Giannis Antetokounmpo", "Damian Lillard", "Khris Middleton", "Jayson Tatum", 
        "Jaylen Brown", "Jrue Holiday", "Nikola Jokic", "Jamal Murray", "Joel Embiid", 
        "Luka Doncic", "Kyrie Irving", "Kevin Durant", "Devin Booker", "Bradley Beal"
    ]
    
    for _, player in players_df.iterrows():
        # Generate realistic stats for this player
        player_name = player['name']
        position = player['position'].split('/')[0]  # Use primary position
        
        # Determine if this is a star player or role player
        is_star = player_name in star_players
        
        # Use appropriate stat ranges
        stat_ranges = star_ranges if is_star else role_ranges
        
        # Default to SF ranges if position not found
        if position not in stat_ranges:
            position = 'SF'
            
        # Generate consistent stats for this player with some game-to-game variation
        base_pts = random.uniform(stat_ranges[position]['pts'][0], stat_ranges[position]['pts'][1])
        base_reb = random.uniform(stat_ranges[position]['reb'][0], stat_ranges[position]['reb'][1])
        base_ast = random.uniform(stat_ranges[position]['ast'][0], stat_ranges[position]['ast'][1])
        base_stl = random.uniform(stat_ranges[position]['stl'][0], stat_ranges[position]['stl'][1])
        base_blk = random.uniform(stat_ranges[position]['blk'][0], stat_ranges[position]['blk'][1])
        base_fg_pct = random.uniform(stat_ranges[position]['fg_pct'][0], stat_ranges[position]['fg_pct'][1])
        base_fg3_pct = random.uniform(stat_ranges[position]['fg3_pct'][0], stat_ranges[position]['fg3_pct'][1])
        base_ft_pct = random.uniform(stat_ranges[position]['ft_pct'][0], stat_ranges[position]['ft_pct'][1])
        
        # Add specific stats for known NBA superstars
        if player_name == "LeBron James":
            base_pts, base_reb, base_ast = 27.3, 7.5, 8.3
        elif player_name == "Stephen Curry":
            base_pts, base_fg3_pct = 29.4, 0.424
        elif player_name == "Giannis Antetokounmpo":
            base_pts, base_reb = 30.4, 11.5
        elif player_name == "Nikola Jokic":
            base_pts, base_reb, base_ast = 25.8, 12.2, 9.1
        elif player_name == "Luka Doncic":
            base_pts, base_reb, base_ast = 33.9, 8.6, 9.8
        elif player_name == "Joel Embiid":
            base_pts, base_reb = 33.1, 10.2
        
        # Generate random stats for 20 games with variation around the base stats
        for game_idx in range(20):
            game_date = (datetime.now() - timedelta(days=game_idx)).strftime('%Y-%m-%d')
            
            # Add game-to-game variation (±20% from base stats)
            variation = 0.2
            pts = max(0, base_pts * random.uniform(1-variation, 1+variation))
            reb = max(0, base_reb * random.uniform(1-variation, 1+variation))
            ast = max(0, base_ast * random.uniform(1-variation, 1+variation))
            stl = max(0, base_stl * random.uniform(1-variation, 1+variation))
            blk = max(0, base_blk * random.uniform(1-variation, 1+variation))
            
            # Less variation for percentages
            small_variation = 0.1
            fg_pct = max(0, min(1, base_fg_pct * random.uniform(1-small_variation, 1+small_variation)))
            fg3_pct = max(0, min(1, base_fg3_pct * random.uniform(1-small_variation, 1+small_variation)))
            ft_pct = max(0, min(1, base_ft_pct * random.uniform(1-small_variation, 1+small_variation)))
            
            # Common stats
            minutes = random.randint(24 if is_star else 12, 38 if is_star else 28)
            tov = random.uniform(0.8, 3.8) if is_star else random.uniform(0.5, 2)
            pf = random.uniform(1, 3.5)
            plus_minus = random.uniform(-15, 15)
            
            game_stats = {
                'player_id': player['player_id'],
                'player_name': player['name'],
                'game_date': game_date,
                'pts': round(pts, 1),
                'reb': round(reb, 1),
                'ast': round(ast, 1),
                'stl': round(stl, 1),
                'blk': round(blk, 1),
                'fg_pct': round(fg_pct, 3),
                'fg3_pct': round(fg3_pct, 3),
                'ft_pct': round(ft_pct, 3),
                'min': minutes,
                'tov': round(tov, 1),
                'pf': round(pf, 1),
                'plus_minus': round(plus_minus, 1)
            }
            
            all_stats.append(game_stats)
    
    # Create DataFrame
    stats_df = pd.DataFrame(all_stats)
    
    # Save to cache
    os.makedirs(DATA_DIR, exist_ok=True)
    stats_df.to_csv(PLAYER_STATS_FILE, index=False)
    
    return stats_df

def fetch_real_data_background():
    """
    Alternative function to fetch real NBA data.
    This is separated out to avoid slowing down the app startup.
    
    Only call this if you want to get real data instead of samples.
    """
    print("Warning: Fetching real NBA data. This will take a long time.")
    
    # Get all active players
    active_players = players.get_active_players()
    
    # Create DataFrame
    players_df = pd.DataFrame(active_players)
    
    # Add additional fields (height, weight, etc.) with rate limiting
    heights = []
    weights = []
    positions = []
    
    for i, player in enumerate(active_players[:20]):  # Limit to just 20 players for demo
        try:
            print(f"Fetching details for {player['full_name']} ({i+1}/20)")
            player_info = commonplayerinfo.CommonPlayerInfo(player_id=player['id'])
            player_info_df = player_info.common_player_info.get_data_frame()
            
            if not player_info_df.empty:
                heights.append(player_info_df['HEIGHT'].iloc[0])
                weights.append(player_info_df['WEIGHT'].iloc[0])
                positions.append(player_info_df['POSITION'].iloc[0])
            else:
                heights.append('')
                weights.append(0)
                positions.append('')
            
            # Sleep to avoid hitting API rate limits
            time.sleep(0.6)
            
        except Exception as e:
            print(f"Error fetching details for {player['full_name']}: {e}")
            heights.append('')
            weights.append(0)
            positions.append('')
    
    # Add columns to DataFrame
    players_df['height'] = heights
    players_df['weight'] = weights
    players_df['position'] = positions
    
    # Rename some columns for consistency
    players_df = players_df.rename(columns={
        'id': 'player_id',
        'full_name': 'name',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'is_active': 'active'
    })
    
    # Add team information
    team_ids = []
    for player_id in players_df['player_id']:
        try:
            player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
            player_info_df = player_info.common_player_info.get_data_frame()
            team_id = player_info_df['TEAM_ID'].iloc[0] if not player_info_df.empty else None
            team_ids.append(team_id)
            time.sleep(0.6)  # Respect API rate limits
        except:
            team_ids.append(None)
    
    players_df['team_id'] = team_ids
    
    # Add team names
    teams_data = teams.get_teams()
    teams_dict = {team['id']: team['full_name'] for team in teams_data}
    players_df['team'] = players_df['team_id'].map(teams_dict)
    
    # Add age
    current_year = datetime.now().year
    players_df['age'] = players_df.apply(
        lambda row: current_year - int(row.get('from_year', current_year-5)), 
        axis=1
    )
    
    # Save to cache
    os.makedirs(DATA_DIR, exist_ok=True)
    players_df.to_csv(PLAYERS_FILE, index=False)
    
    print("Real player data fetched and saved.")

def import_real_nba_data(force_update=False):
    """
    Import complete and updated NBA player data from the NBA API.
    This function uses multiple API calls to get comprehensive player data.
    
    Args:
        force_update (bool): Whether to force an update even if cached data exists
        
    Returns:
        tuple: (players_df, stats_df, teams_df) containing all player, statistics and team data
    """
    import pandas as pd
    import os
    import time
    import json
    from nba_api.stats.static import players, teams
    from nba_api.stats.endpoints import commonallplayers, playergamelog, commonplayerinfo, leaguedashplayerstats
    
    # Check if we should use cached data
    if not force_update and os.path.exists(PLAYERS_FILE) and os.path.exists(PLAYER_STATS_FILE) and os.path.exists(TEAMS_FILE):
        print("Using cached NBA data...")
        return (
            pd.read_csv(PLAYERS_FILE),
            pd.read_csv(PLAYER_STATS_FILE),
            pd.read_csv(TEAMS_FILE)
        )
    
    print("Importing real NBA data. This may take a few minutes...")
    
    # Get team data first (fast)
    print("Fetching team data...")
    nba_teams = teams.get_teams()
    teams_dict = {team['id']: team for team in nba_teams}
    teams_df = pd.DataFrame(nba_teams)
    teams_df = teams_df.rename(columns={
        'id': 'team_id',
        'full_name': 'name',
        'abbreviation': 'abbreviation',
        'nickname': 'nickname',
        'city': 'city',
        'state': 'state',
        'year_founded': 'year_founded'
    })
    
    # Get all players
    print("Fetching all NBA players...")
    try:
        # Use the more comprehensive endpoint that includes current team info
        all_players = commonallplayers.CommonAllPlayers().get_data_frames()[0]
        
        # Filter to active players only
        active_players = all_players[all_players['ROSTERSTATUS'] == 1]
        
        # Create main players dataframe
        players_df = pd.DataFrame({
            'player_id': active_players['PERSON_ID'],
            'name': active_players['DISPLAY_FIRST_LAST'],
            'first_name': active_players['DISPLAY_FIRST_LAST'].str.split(' ').str[0],
            'last_name': active_players['DISPLAY_FIRST_LAST'].str.split(' ').str[-1],
            'team_id': active_players['TEAM_ID'],
            'active': True
        })
        
        # Add team names
        players_df['team'] = players_df['team_id'].map({team['id']: team['full_name'] for team in nba_teams})
        
        # Get player details in batches to avoid rate limiting
        print(f"Fetching details for {len(players_df)} players...")
        players_df['position'] = ""
        players_df['height'] = ""
        players_df['weight'] = 0
        players_df['age'] = 0
        players_df['from_year'] = 0
        
        # Try to get aggregated player stats for the current season (faster)
        try:
            print("Fetching league dashboard player stats (aggregated)...")
            league_stats = leaguedashplayerstats.LeagueDashPlayerStats(
                season='2023-24',
                per_mode_detailed='PerGame'
            ).get_data_frames()[0]
            
            # Create basic stats dataframe from aggregate data
            stats_df = pd.DataFrame()
            
            # If we got stats data successfully, create player game records
            if not league_stats.empty:
                print(f"Processing stats for {len(league_stats)} players...")
                
                # Process each player's aggregate stats and create synthetic game records
                all_stats = []
                
                for _, player_row in league_stats.iterrows():
                    player_id = player_row['PLAYER_ID']
                    player_name = player_row['PLAYER_NAME']
                    
                    # Create 20 synthetic game records based on the player's season averages
                    for game_idx in range(20):
                        game_date = pd.Timestamp.now() - pd.Timedelta(days=game_idx)
                        
                        # Add some variation to each game (±15% from season average)
                        variation = 0.15
                        
                        game_stats = {
                            'player_id': player_id,
                            'player_name': player_name,
                            'game_date': game_date.strftime('%Y-%m-%d'),
                            'pts': round(player_row['PTS'] * (1 + random.uniform(-variation, variation)), 1),
                            'reb': round((player_row['OREB'] + player_row['DREB']) * (1 + random.uniform(-variation, variation)), 1),
                            'ast': round(player_row['AST'] * (1 + random.uniform(-variation, variation)), 1),
                            'stl': round(player_row['STL'] * (1 + random.uniform(-variation, variation)), 1),
                            'blk': round(player_row['BLK'] * (1 + random.uniform(-variation, variation)), 1),
                            'fg_pct': round(max(0, min(1, player_row['FG_PCT'] * (1 + random.uniform(-variation/2, variation/2)))), 3),
                            'fg3_pct': round(max(0, min(1, player_row['FG3_PCT'] * (1 + random.uniform(-variation/2, variation/2)))), 3),
                            'ft_pct': round(max(0, min(1, player_row['FT_PCT'] * (1 + random.uniform(-variation/2, variation/2)))), 3),
                            'min': round(player_row['MIN'] * (1 + random.uniform(-variation/2, variation/2))),
                            'tov': round(player_row['TOV'] * (1 + random.uniform(-variation, variation)), 1),
                            'pf': round(player_row['PF'] * (1 + random.uniform(-variation, variation)), 1),
                            'plus_minus': round(player_row['PLUS_MINUS'] * (1 + random.uniform(-variation, variation)), 1)
                        }
                        all_stats.append(game_stats)
                
                stats_df = pd.DataFrame(all_stats)
            
            # Update player details from the same dashboard data
            for _, player_row in league_stats.iterrows():
                player_id = player_row['PLAYER_ID']
                if player_id in players_df['player_id'].values:
                    players_df.loc[players_df['player_id'] == player_id, 'position'] = player_row['POSITION']
                    
                    # Convert height from ft-in format to standard format
                    height_parts = str(player_row['PLAYER_HEIGHT']).split('-')
                    if len(height_parts) == 2:
                        feet, inches = height_parts
                        height = f"{feet}'{inches}\""
                    else:
                        height = ""
                        
                    players_df.loc[players_df['player_id'] == player_id, 'height'] = height
                    players_df.loc[players_df['player_id'] == player_id, 'weight'] = player_row['PLAYER_WEIGHT']
                    players_df.loc[players_df['player_id'] == player_id, 'age'] = 2024 - player_row['BIRTH_DATE'].year if isinstance(player_row['BIRTH_DATE'], pd.Timestamp) else 0
        
        except Exception as e:
            print(f"Error fetching league dashboard stats: {e}")
            # If aggregate stats fail, fall back to sample data for stats
            print("Falling back to generated stats...")
            # Generate sample stats for all the players we fetched
            stats_df = create_sample_player_stats_for_real_players(players_df)
    
    except Exception as e:
        print(f"Error fetching player data: {e}")
        print("Falling back to sample player data...")
        # Fall back to sample data
        players_df = create_sample_players()
        stats_df = create_sample_player_stats()
    
    # Save data to cache
    os.makedirs(DATA_DIR, exist_ok=True)
    players_df.to_csv(PLAYERS_FILE, index=False)
    stats_df.to_csv(PLAYER_STATS_FILE, index=False)
    teams_df.to_csv(TEAMS_FILE, index=False)
    
    print("NBA data import complete!")
    return players_df, stats_df, teams_df

def create_sample_player_stats_for_real_players(players_df):
    """
    Create sample player statistics for real players when API data is unavailable.
    
    Args:
        players_df (pandas.DataFrame): DataFrame with real player data
        
    Returns:
        pandas.DataFrame: DataFrame with sample player statistics
    """
    print("Creating sample statistics for real players...")
    
    # Real NBA player stat ranges based on position and player caliber
    star_ranges = {
        'PG': {'pts': (22, 32), 'reb': (4, 7), 'ast': (6, 11), 'stl': (1, 2.5), 'blk': (0, 1), 
               'fg_pct': (0.44, 0.52), 'fg3_pct': (0.36, 0.44), 'ft_pct': (0.85, 0.92)},
        'SG': {'pts': (20, 30), 'reb': (4, 6), 'ast': (4, 7), 'stl': (1, 2.5), 'blk': (0.5, 1.5), 
               'fg_pct': (0.44, 0.50), 'fg3_pct': (0.37, 0.44), 'ft_pct': (0.83, 0.90)},
        'SF': {'pts': (19, 28), 'reb': (5, 9), 'ast': (3, 7), 'stl': (1, 2), 'blk': (0.5, 1.5), 
               'fg_pct': (0.45, 0.54), 'fg3_pct': (0.35, 0.43), 'ft_pct': (0.80, 0.88)},
        'PF': {'pts': (17, 27), 'reb': (7, 12), 'ast': (2, 5), 'stl': (0.5, 1.5), 'blk': (0.8, 2.2), 
               'fg_pct': (0.48, 0.56), 'fg3_pct': (0.30, 0.38), 'ft_pct': (0.75, 0.85)},
        'C':  {'pts': (15, 25), 'reb': (9, 14), 'ast': (1, 4), 'stl': (0.5, 1.2), 'blk': (1.5, 3), 
               'fg_pct': (0.55, 0.65), 'fg3_pct': (0.25, 0.35), 'ft_pct': (0.65, 0.80)}
    }
    
    role_ranges = {
        'PG': {'pts': (9, 15), 'reb': (2, 4), 'ast': (3, 6), 'stl': (0.5, 1.5), 'blk': (0, 0.5), 
               'fg_pct': (0.40, 0.46), 'fg3_pct': (0.32, 0.39), 'ft_pct': (0.75, 0.85)},
        'SG': {'pts': (8, 15), 'reb': (2, 5), 'ast': (1.5, 3.5), 'stl': (0.5, 1.2), 'blk': (0.2, 0.8), 
               'fg_pct': (0.40, 0.46), 'fg3_pct': (0.34, 0.40), 'ft_pct': (0.78, 0.85)},
        'SF': {'pts': (8, 14), 'reb': (3, 6), 'ast': (1, 3), 'stl': (0.5, 1.2), 'blk': (0.3, 0.8), 
               'fg_pct': (0.42, 0.48), 'fg3_pct': (0.32, 0.38), 'ft_pct': (0.75, 0.83)},
        'PF': {'pts': (7, 13), 'reb': (4, 8), 'ast': (0.8, 2.5), 'stl': (0.3, 1), 'blk': (0.5, 1.5), 
               'fg_pct': (0.45, 0.53), 'fg3_pct': (0.28, 0.35), 'ft_pct': (0.70, 0.80)},
        'C':  {'pts': (7, 12), 'reb': (5, 9), 'ast': (0.5, 2), 'stl': (0.2, 0.8), 'blk': (0.8, 2), 
               'fg_pct': (0.52, 0.60), 'fg3_pct': (0.18, 0.30), 'ft_pct': (0.60, 0.75)}
    }
    
    # Star player names - assuming top players by team
    star_players = [
        "LeBron James", "Stephen Curry", "Giannis Antetokounmpo", "Nikola Jokic", "Joel Embiid",
        "Luka Doncic", "Kevin Durant", "Jayson Tatum", "Damian Lillard", "Anthony Davis",
        "Devin Booker", "Trae Young", "Ja Morant", "Kawhi Leonard", "Jimmy Butler",
        "Bam Adebayo", "Donovan Mitchell", "Zion Williamson", "Karl-Anthony Towns"
    ]
    
    # Create sample data for each player
    all_stats = []
    
    for _, player in players_df.iterrows():
        # Generate realistic stats for this player
        player_name = player['name']
        
        # Extract primary position or default to SF
        position = player['position']
        if isinstance(position, str) and len(position) > 0:
            position = position.split('/')[0]
        else:
            position = 'SF'
            
        # Default to SF if position not in our mapping
        if position not in ['PG', 'SG', 'SF', 'PF', 'C']:
            position = 'SF'
        
        # Determine if this is a star player or role player
        is_star = player_name in star_players
        
        # Use appropriate stat ranges
        stat_ranges = star_ranges if is_star else role_ranges
            
        # Generate consistent stats for this player with some game-to-game variation
        base_pts = random.uniform(stat_ranges[position]['pts'][0], stat_ranges[position]['pts'][1])
        base_reb = random.uniform(stat_ranges[position]['reb'][0], stat_ranges[position]['reb'][1])
        base_ast = random.uniform(stat_ranges[position]['ast'][0], stat_ranges[position]['ast'][1])
        base_stl = random.uniform(stat_ranges[position]['stl'][0], stat_ranges[position]['stl'][1])
        base_blk = random.uniform(stat_ranges[position]['blk'][0], stat_ranges[position]['blk'][1])
        base_fg_pct = random.uniform(stat_ranges[position]['fg_pct'][0], stat_ranges[position]['fg_pct'][1])
        base_fg3_pct = random.uniform(stat_ranges[position]['fg3_pct'][0], stat_ranges[position]['fg3_pct'][1])
        base_ft_pct = random.uniform(stat_ranges[position]['ft_pct'][0], stat_ranges[position]['ft_pct'][1])
        
        # Add specific stats for known NBA superstars
        if player_name == "LeBron James":
            base_pts, base_reb, base_ast = 27.3, 7.5, 8.3
        elif player_name == "Stephen Curry":
            base_pts, base_fg3_pct = 29.4, 0.424
        elif player_name == "Giannis Antetokounmpo":
            base_pts, base_reb = 30.4, 11.5
        elif player_name == "Nikola Jokic":
            base_pts, base_reb, base_ast = 25.8, 12.2, 9.1
        elif player_name == "Luka Doncic":
            base_pts, base_reb, base_ast = 33.9, 8.6, 9.8
        elif player_name == "Joel Embiid":
            base_pts, base_reb = 33.1, 10.2
        
        # Generate random stats for 20 games with variation around the base stats
        for game_idx in range(20):
            game_date = (datetime.now() - timedelta(days=game_idx)).strftime('%Y-%m-%d')
            
            # Add game-to-game variation (±20% from base stats)
            variation = 0.2
            pts = max(0, base_pts * random.uniform(1-variation, 1+variation))
            reb = max(0, base_reb * random.uniform(1-variation, 1+variation))
            ast = max(0, base_ast * random.uniform(1-variation, 1+variation))
            stl = max(0, base_stl * random.uniform(1-variation, 1+variation))
            blk = max(0, base_blk * random.uniform(1-variation, 1+variation))
            
            # Less variation for percentages
            small_variation = 0.1
            fg_pct = max(0, min(1, base_fg_pct * random.uniform(1-small_variation, 1+small_variation)))
            fg3_pct = max(0, min(1, base_fg3_pct * random.uniform(1-small_variation, 1+small_variation)))
            ft_pct = max(0, min(1, base_ft_pct * random.uniform(1-small_variation, 1+small_variation)))
            
            # Common stats
            minutes = random.randint(24 if is_star else 12, 38 if is_star else 28)
            tov = random.uniform(0.8, 3.8) if is_star else random.uniform(0.5, 2)
            pf = random.uniform(1, 3.5)
            plus_minus = random.uniform(-15, 15)
            
            game_stats = {
                'player_id': player['player_id'],
                'player_name': player['name'],
                'game_date': game_date,
                'pts': round(pts, 1),
                'reb': round(reb, 1),
                'ast': round(ast, 1),
                'stl': round(stl, 1),
                'blk': round(blk, 1),
                'fg_pct': round(fg_pct, 3),
                'fg3_pct': round(fg3_pct, 3),
                'ft_pct': round(ft_pct, 3),
                'min': minutes,
                'tov': round(tov, 1),
                'pf': round(pf, 1),
                'plus_minus': round(plus_minus, 1)
            }
            
            all_stats.append(game_stats)
    
    # Create DataFrame
    stats_df = pd.DataFrame(all_stats)
    return stats_df

# Fix the enhance_player_dataset function to use correct team columns
def enhance_player_dataset():
    """
    Enhance the player dataset by tripling the number of players while maintaining realistic data.
    This function loads existing player data, generates new players based on team data,
    and saves the enhanced dataset.
    
    Returns:
        pandas.DataFrame: The enhanced player dataset
    """
    import pandas as pd
    import numpy as np
    import os
    from datetime import datetime
    
    # Load existing data
    players_path = os.path.join('data', 'players.csv')
    stats_path = os.path.join('data', 'player_stats.csv')
    teams_path = os.path.join('data', 'teams.csv')
    
    if not all(os.path.exists(path) for path in [players_path, stats_path, teams_path]):
        print("Required data files not found. Creating sample data first.")
        players = create_sample_player_data()
        stats = create_sample_player_stats()
        teams = load_team_data()
    else:
        players = pd.read_csv(players_path)
        stats = pd.read_csv(stats_path)
        teams = pd.read_csv(teams_path)
    
    # Get the highest player_id to start new IDs from
    max_player_id = players['player_id'].max()
    current_players_count = len(players)
    new_players_count = current_players_count * 2  # Tripling = original + 2x more
    
    # Create list for new players
    new_players = []
    new_stats = []
    
    # Real NBA player first names and last names for generating realistic names
    first_names = [
        "James", "Michael", "Chris", "Kevin", "Anthony", "Stephen", "Russell", "Damian", 
        "Giannis", "Joel", "Devin", "Jayson", "Kawhi", "Paul", "Jimmy", "Donovan", 
        "Trae", "Zion", "Luka", "Kyrie", "Ja", "Bam", "Bradley", "Nikola", "Jamal",
        "Brandon", "De'Aaron", "John", "Zach", "Jrue", "Tyler", "Malcolm", "Khris",
        "Pascal", "Kyle", "Fred", "Gordon", "Aaron", "Draymond", "Jerami", "Lou",
        "Evan", "Marcus", "Ben", "Lamelo", "Cade", "Paolo", "Victor", "Jaylen"
    ]
    
    last_names = [
        "James", "Jordan", "Paul", "Durant", "Davis", "Curry", "Westbrook", "Lillard",
        "Antetokounmpo", "Embiid", "Booker", "Tatum", "Leonard", "George", "Butler", "Mitchell",
        "Young", "Williamson", "Doncic", "Irving", "Morant", "Adebayo", "Beal", "Jokic", "Murray",
        "Ingram", "Fox", "Wall", "LaVine", "Holiday", "Herro", "Brogdon", "Middleton",
        "Siakam", "Lowry", "VanVleet", "Hayward", "Gordon", "Green", "Grant", "Williams",
        "Fournier", "Smart", "Simmons", "Ball", "Cunningham", "Banchero", "Wembanyama", "Brown"
    ]
    
    # Realistic heights and weights by position
    position_attributes = {
        "PG": {"height_range": (70, 76), "weight_range": (175, 200)},
        "SG": {"height_range": (74, 78), "weight_range": (185, 215)},
        "SF": {"height_range": (76, 81), "weight_range": (200, 230)},
        "PF": {"height_range": (79, 83), "weight_range": (220, 250)},
        "C":  {"height_range": (81, 87), "weight_range": (240, 290)}
    }
    
    # Create new players
    for i in range(new_players_count):
        # Generate a new unique player ID
        new_player_id = max_player_id + i + 1
        
        # Randomly select a team from existing teams
        team = teams.sample(1).iloc[0]
        team_id = team['team_id']
        team_name = team['name']  # Changed from 'full_name' to 'name'
        
        # Generate a random position
        positions = ["PG", "SG", "SF", "PF", "C"]
        weights = [0.2, 0.2, 0.2, 0.2, 0.2]  # Equal distribution
        position = np.random.choice(positions, p=weights)
        
        # Sometimes create combo positions
        if np.random.random() < 0.3:  # 30% chance of combo position
            secondary_position = np.random.choice([p for p in positions if p != position])
            position = f"{position}/{secondary_position}"
        
        # Get appropriate height and weight ranges for the position
        base_position = position.split('/')[0]  # Use the primary position for attributes
        height_range = position_attributes[base_position]["height_range"]
        weight_range = position_attributes[base_position]["weight_range"]
        
        # Generate height and weight
        height_inches = np.random.randint(*height_range)
        height_feet = height_inches // 12
        height_remainder = height_inches % 12
        height = f"{height_feet}'{height_remainder}\""
        
        weight = np.random.randint(*weight_range)
        
        # Generate random age between 19 and 37
        age = np.random.randint(19, 38)
        
        # Random year they joined (between 2010 and 2024)
        from_year = np.random.randint(2010, 2025)
        
        # Generate name
        first_name = np.random.choice(first_names)
        last_name = np.random.choice(last_names)
        full_name = f"{first_name} {last_name}"
        
        # Create player record
        new_player = {
            'player_id': new_player_id,
            'name': full_name,
            'first_name': first_name,
            'last_name': last_name,
            'active': True,
            'height': height,
            'weight': weight,
            'position': position,
            'team_id': team_id,
            'team': team_name,
            'age': age,
            'from_year': from_year
        }
        
        new_players.append(new_player)
        
        # Generate player stats based on position
        # Base stats on position
        if base_position == "PG":
            # Point guards tend to have more assists and steals
            pts_base = np.random.uniform(12, 25)
            reb_base = np.random.uniform(2, 6)
            ast_base = np.random.uniform(5, 10)
            stl_base = np.random.uniform(1, 2.5)
            blk_base = np.random.uniform(0.1, 0.8)
            fg_pct_base = np.random.uniform(0.40, 0.48)
            fg3_pct_base = np.random.uniform(0.32, 0.42)
            ft_pct_base = np.random.uniform(0.75, 0.90)
        elif base_position == "SG":
            # Shooting guards tend to score more and shoot 3s
            pts_base = np.random.uniform(15, 27)
            reb_base = np.random.uniform(3, 6)
            ast_base = np.random.uniform(3, 7)
            stl_base = np.random.uniform(0.8, 2.0)
            blk_base = np.random.uniform(0.2, 1.0)
            fg_pct_base = np.random.uniform(0.42, 0.48)
            fg3_pct_base = np.random.uniform(0.35, 0.45)
            ft_pct_base = np.random.uniform(0.78, 0.90)
        elif base_position == "SF":
            # Small forwards are all-around players
            pts_base = np.random.uniform(14, 26)
            reb_base = np.random.uniform(5, 8)
            ast_base = np.random.uniform(2, 6)
            stl_base = np.random.uniform(0.8, 1.8)
            blk_base = np.random.uniform(0.5, 1.3)
            fg_pct_base = np.random.uniform(0.44, 0.50)
            fg3_pct_base = np.random.uniform(0.33, 0.40)
            ft_pct_base = np.random.uniform(0.75, 0.88)
        elif base_position == "PF":
            # Power forwards get rebounds and blocks
            pts_base = np.random.uniform(12, 23)
            reb_base = np.random.uniform(7, 12)
            ast_base = np.random.uniform(1.5, 4.5)
            stl_base = np.random.uniform(0.5, 1.5)
            blk_base = np.random.uniform(0.8, 2.0)
            fg_pct_base = np.random.uniform(0.48, 0.56)
            fg3_pct_base = np.random.uniform(0.28, 0.38)
            ft_pct_base = np.random.uniform(0.70, 0.85)
        else:  # Center
            # Centers focus on rebounds, blocks, and high FG%
            pts_base = np.random.uniform(10, 22)
            reb_base = np.random.uniform(8, 14)
            ast_base = np.random.uniform(1, 4)
            stl_base = np.random.uniform(0.4, 1.2)
            blk_base = np.random.uniform(1.0, 2.5)
            fg_pct_base = np.random.uniform(0.52, 0.65)
            fg3_pct_base = np.random.uniform(0.20, 0.33)
            ft_pct_base = np.random.uniform(0.60, 0.80)
        
        # Add some random variation for 10 games
        for game in range(10):
            # Generate a random opponent from teams
            opponent_team = teams.sample(1).iloc[0]['team_id']
            
            # Add some game-to-game variation
            pts = max(0, pts_base + np.random.normal(0, pts_base * 0.2))
            reb = max(0, reb_base + np.random.normal(0, reb_base * 0.2))
            ast = max(0, ast_base + np.random.normal(0, ast_base * 0.2))
            stl = max(0, stl_base + np.random.normal(0, stl_base * 0.3))
            blk = max(0, blk_base + np.random.normal(0, blk_base * 0.3))
            
            # More stable percentages with small variations
            fg_pct = max(0, min(1, fg_pct_base + np.random.normal(0, 0.05)))
            fg3_pct = max(0, min(1, fg3_pct_base + np.random.normal(0, 0.07)))
            ft_pct = max(0, min(1, ft_pct_base + np.random.normal(0, 0.06)))
            
            # Create game stat record
            game_stat = {
                'player_id': new_player_id,
                'game_id': f"G{new_player_id}_{game}",
                'date': (datetime.now().date() - pd.Timedelta(days=game)).strftime('%Y-%m-%d'),
                'home_team': team_id,
                'away_team': opponent_team,
                'pts': round(pts, 1),
                'reb': round(reb, 1),
                'ast': round(ast, 1),
                'stl': round(stl, 1),
                'blk': round(blk, 1),
                'fg_pct': round(fg_pct, 3),
                'fg3_pct': round(fg3_pct, 3),
                'ft_pct': round(ft_pct, 3),
                'turnover': round(max(0, np.random.normal(2, 1)), 1),
                'pf': round(max(0, np.random.normal(2.5, 1)), 1)
            }
            
            new_stats.append(game_stat)
    
    # Convert to DataFrame
    new_players_df = pd.DataFrame(new_players)
    new_stats_df = pd.DataFrame(new_stats)
    
    # Combine with existing data
    enhanced_players = pd.concat([players, new_players_df], ignore_index=True)
    enhanced_stats = pd.concat([stats, new_stats_df], ignore_index=True)
    
    # Save enhanced datasets
    enhanced_players.to_csv(players_path, index=False)
    enhanced_stats.to_csv(stats_path, index=False)
    
    print(f"Enhanced player dataset from {current_players_count} to {len(enhanced_players)} players")
    print(f"Enhanced stats dataset to {len(enhanced_stats)} records")
    
    return enhanced_players

if __name__ == "__main__":
    # Test data loading
    players_df = load_nba_players()
    stats_df = load_player_stats()
    teams_df = load_team_data()
    
    print(f"Loaded {len(players_df)} players")
    print(f"Loaded {len(stats_df)} player game records")
    print(f"Loaded {len(teams_df)} teams") 