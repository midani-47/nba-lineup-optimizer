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
    Load NBA player data, either from cache or API.
    
    Returns:
        pandas.DataFrame: DataFrame with player data
    """
    # Check if we have cached data
    if os.path.exists(PLAYERS_FILE):
        print("Loading players from cache...")
        return pd.read_csv(PLAYERS_FILE)
    
    print("Fetching players from NBA API...")
    # Get all active players
    active_players = players.get_active_players()
    
    # Create DataFrame
    players_df = pd.DataFrame(active_players)
    
    # Add additional fields (height, weight, etc.) with rate limiting
    heights = []
    weights = []
    positions = []
    
    for i, player in enumerate(active_players):
        try:
            print(f"Fetching details for {player['full_name']} ({i+1}/{len(active_players)})")
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
    
    return players_df

def load_player_stats():
    """
    Load player statistics, either from cache or API.
    
    Returns:
        pandas.DataFrame: DataFrame with player statistics
    """
    # Check if we have cached data
    if os.path.exists(PLAYER_STATS_FILE):
        print("Loading player stats from cache...")
        return pd.read_csv(PLAYER_STATS_FILE)
    
    print("Fetching player stats from NBA API...")
    
    # Get active players
    active_players = players.get_active_players()
    
    # Get current season
    current_year = datetime.now().year
    season = f"{current_year-1}-{str(current_year)[2:]}" if datetime.now().month < 10 else f"{current_year}-{str(current_year+1)[2:]}"
    
    # Fetch game logs for each player
    all_stats = []
    
    for i, player in enumerate(active_players[:100]):  # Limit to 100 players for demo
        try:
            print(f"Fetching game log for {player['full_name']} ({i+1}/100)")
            
            # Get game logs from current season
            game_logs = playergamelog.PlayerGameLog(
                player_id=player['id'],
                season=season
            )
            df = game_logs.get_data_frames()[0]
            
            if not df.empty:
                # Add player ID and name
                df['player_id'] = player['id']
                df['player_name'] = player['full_name']
                
                # Append to list of dataframes
                all_stats.append(df)
            
            # Sleep to avoid hitting API rate limits
            time.sleep(0.6)
            
        except Exception as e:
            print(f"Error fetching game log for {player['full_name']}: {e}")
    
    # Combine all stats
    if all_stats:
        combined_stats = pd.concat(all_stats, ignore_index=True)
        
        # Rename columns for consistency
        combined_stats = combined_stats.rename(columns={
            'GAME_DATE': 'game_date',
            'PTS': 'pts',
            'REB': 'reb',
            'AST': 'ast',
            'STL': 'stl',
            'BLK': 'blk',
            'FG_PCT': 'fg_pct',
            'FG3_PCT': 'fg3_pct',
            'FT_PCT': 'ft_pct',
            'MIN': 'min',
            'TOV': 'tov',
            'PF': 'pf',
            'PLUS_MINUS': 'plus_minus'
        })
        
        # Save to cache
        os.makedirs(DATA_DIR, exist_ok=True)
        combined_stats.to_csv(PLAYER_STATS_FILE, index=False)
        
        return combined_stats
    else:
        print("No player stats fetched. Using sample data.")
        return create_sample_player_stats()

def load_team_data():
    """
    Load team data, either from cache or API.
    
    Returns:
        pandas.DataFrame: DataFrame with team data
    """
    # Check if we have cached data
    if os.path.exists(TEAMS_FILE):
        print("Loading teams from cache...")
        return pd.read_csv(TEAMS_FILE)
    
    print("Fetching teams from NBA API...")
    
    # Get all NBA teams
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
    
    # Get active players
    all_players = players.get_active_players()
    
    # Randomly select 100 players
    selected_players = random.sample(all_players, min(100, len(all_players)))
    
    # Create sample data for the last 20 games
    all_stats = []
    
    for player in selected_players:
        # Generate random stats for 20 games
        for game_idx in range(20):
            game_date = (datetime.now() - timedelta(days=game_idx)).strftime('%Y-%m-%d')
            
            # Random stats with some realistic constraints
            pts = random.randint(0, 40)
            reb = random.randint(0, 15)
            ast = random.randint(0, 12)
            stl = random.randint(0, 5)
            blk = random.randint(0, 4)
            fg_pct = round(random.uniform(0.2, 0.9), 3)
            fg3_pct = round(random.uniform(0.1, 0.6), 3)
            ft_pct = round(random.uniform(0.6, 1.0), 3)
            minutes = random.randint(5, 48)
            tov = random.randint(0, 8)
            pf = random.randint(0, 6)
            plus_minus = random.randint(-30, 30)
            
            game_stats = {
                'player_id': player['id'],
                'player_name': player['full_name'],
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

if __name__ == "__main__":
    # Test data loading
    players_df = load_nba_players()
    stats_df = load_player_stats()
    teams_df = load_team_data()
    
    print(f"Loaded {len(players_df)} players")
    print(f"Loaded {len(stats_df)} player game records")
    print(f"Loaded {len(teams_df)} teams") 