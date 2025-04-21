import pandas as pd
import os
import json
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import playergamelog, commonplayerinfo, teamgamelog
import time
import random
from datetime import datetime, timedelta

# Paths for cached data
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
PLAYERS_FILE = os.path.join(DATA_DIR, 'players.csv')
PLAYER_STATS_FILE = os.path.join(DATA_DIR, 'player_stats.csv')
TEAMS_FILE = os.path.join(DATA_DIR, 'teams.csv')

def load_nba_players():
    """
    Load NBA player data, prioritizing sample data for speed.
    
    Returns:
        pandas.DataFrame: DataFrame with player data
    """
    # Check if we have cached data
    if os.path.exists(PLAYERS_FILE):
        print("Loading players from cache...")
        return pd.read_csv(PLAYERS_FILE)
    
    print("Creating sample player data...")
    return create_sample_players()

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
    Create sample player data for demonstration purposes.
    
    Returns:
        pandas.DataFrame: DataFrame with sample player data
    """
    print("Creating sample player data...")
    
    # Get real team data from static resource (this is fast)
    nba_teams = teams.get_teams()
    
    # Create sample positions
    positions = ['PG', 'SG', 'SF', 'PF', 'C', 'PG/SG', 'SG/SF', 'SF/PF', 'PF/C']
    
    # Create sample players with realistic attributes
    sample_players = []
    player_id = 1000
    
    # Add team-based players
    for team in nba_teams:
        team_name = team['full_name']
        team_id = team['id']
        
        # Add 12 players per team
        for i in range(12):
            # Choose position based on index
            if i < 2:
                position = 'PG' if i == 0 else 'PG/SG'
            elif i < 4:
                position = 'SG' if i == 2 else 'SG/SF'
            elif i < 7:
                position = 'SF' if i == 4 else ('SF/PF' if i == 5 else 'PF')
            elif i < 10:
                position = 'PF' if i == 7 else ('PF/C' if i == 8 else 'C')
            else:
                position = random.choice(positions)
            
            # Generate player data
            first_name = f"Player{player_id}"
            last_name = f"{chr(65 + i)}{team['abbreviation']}"
            height = f"{random.randint(5, 7)}'{random.randint(0, 11)}"
            weight = random.randint(175, 285)
            age = random.randint(19, 38)
            
            player = {
                'player_id': player_id,
                'name': f"{first_name} {last_name}",
                'first_name': first_name,
                'last_name': last_name,
                'active': True,
                'height': height,
                'weight': weight,
                'position': position,
                'team_id': team_id,
                'team': team_name,
                'age': age,
                'from_year': datetime.now().year - random.randint(0, 15)
            }
            
            sample_players.append(player)
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
    Create sample player statistics for demonstration purposes.
    
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
    
    for _, player in players_df.iterrows():
        # Generate random stats for 20 games
        for game_idx in range(20):
            game_date = (datetime.now() - timedelta(days=game_idx)).strftime('%Y-%m-%d')
            
            # Player's position affects their stats distribution
            position = player['position'].split('/')[0]  # Use primary position
            
            # Base stats with some randomness
            if position in ['PG', 'SG']:  # Guards
                pts = random.randint(8, 25)
                reb = random.randint(1, 7)
                ast = random.randint(3, 12)
                stl = random.randint(0, 3)
                blk = random.randint(0, 1)
                fg_pct = round(random.uniform(0.35, 0.55), 3)
                fg3_pct = round(random.uniform(0.30, 0.45), 3)
            elif position in ['SF', 'PF']:  # Forwards
                pts = random.randint(10, 22)
                reb = random.randint(4, 12)
                ast = random.randint(1, 6)
                stl = random.randint(0, 2)
                blk = random.randint(0, 2)
                fg_pct = round(random.uniform(0.40, 0.60), 3)
                fg3_pct = round(random.uniform(0.25, 0.40), 3)
            else:  # Centers
                pts = random.randint(8, 20)
                reb = random.randint(7, 15)
                ast = random.randint(0, 4)
                stl = random.randint(0, 1)
                blk = random.randint(0, 4)
                fg_pct = round(random.uniform(0.45, 0.65), 3)
                fg3_pct = round(random.uniform(0.10, 0.35), 3)
            
            # Common stats
            ft_pct = round(random.uniform(0.65, 0.95), 3)
            minutes = random.randint(10, 38)
            tov = random.randint(0, 5)
            pf = random.randint(0, 5)
            plus_minus = random.randint(-20, 20)
            
            game_stats = {
                'player_id': player['player_id'],
                'player_name': player['name'],
                'game_date': game_date,
                'pts': pts,
                'reb': reb,
                'ast': ast,
                'stl': stl,
                'blk': blk,
                'fg_pct': fg_pct,
                'fg3_pct': fg3_pct,
                'ft_pct': ft_pct,
                'min': minutes,
                'tov': tov,
                'pf': pf,
                'plus_minus': plus_minus
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

if __name__ == "__main__":
    # Test data loading
    players_df = load_nba_players()
    stats_df = load_player_stats()
    teams_df = load_team_data()
    
    print(f"Loaded {len(players_df)} players")
    print(f"Loaded {len(stats_df)} player game records")
    print(f"Loaded {len(teams_df)} teams") 