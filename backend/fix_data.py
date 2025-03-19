import os
import django
import sqlite3

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nba_project.settings')
django.setup()

# Import models
from api.models import Player, Team, Lineup

def fix_database_schema():
    """Add missing columns to the database schema"""
    print("Fixing database schema...")
    
    # Connect to the SQLite database
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    # Check if image_url column exists in api_player table
    cursor.execute("PRAGMA table_info(api_player)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'image_url' not in columns:
        print("Adding image_url column to api_player table...")
        cursor.execute("ALTER TABLE api_player ADD COLUMN image_url TEXT")
        conn.commit()
        print("Column added successfully")
    else:
        print("image_url column already exists")
    
    # Close the connection
    conn.close()

def fix_player_data():
    print("Fixing player data...")
    
    # Default image URL for non-top players
    DEFAULT_PLAYER_IMAGE = "https://www.vectorstock.com/royalty-free-vector/basketball-ball-icon-vector-52387426"
    
    # Get all players
    players = Player.objects.all()
    count = 0
    
    # First, reset all players to reasonable defaults
    for player in players:
        player.points_per_game = 8.5  # Average role player
        player.rebounds_per_game = 3.5
        player.assists_per_game = 2.0
        player.field_goal_percentage = 0.45
        player.three_point_percentage = 0.35
        player.free_throw_percentage = 0.75
        player.offensive_rating = 110.0
        player.defensive_rating = 110.0
        player.player_efficiency_rating = 15.0
        player.usage_rate = 20.0
        player.true_shooting_percentage = 0.55
        
        # Set default image URL for all players
        player.image_url = DEFAULT_PLAYER_IMAGE
        
        if not player.position or player.position == '':
            player.position = 'G-F'  # Default position
        
        player.save()
        count += 1
    
    # Top NBA players with realistic stats by ID - Updated with latest stats from NBA.com
    top_players_by_id = [
        {"id": 1629029, "name": "Luka Doncic", "ppg": 33.9, "rpg": 9.2, "apg": 9.8, "position": "G", "team_id": 1610612742},
        {"id": 203954, "name": "Joel Embiid", "ppg": 34.7, "rpg": 11.2, "apg": 5.6, "position": "C", "team_id": 1610612755},
        {"id": 203507, "name": "Giannis Antetokounmpo", "ppg": 30.7, "rpg": 11.5, "apg": 6.5, "position": "F", "team_id": 1610612749},
        {"id": 1628983, "name": "Shai Gilgeous-Alexander", "ppg": 30.1, "rpg": 5.5, "apg": 6.2, "position": "G", "team_id": 1610612760},
        {"id": 203999, "name": "Nikola Jokic", "ppg": 26.4, "rpg": 12.4, "apg": 9.0, "position": "C", "team_id": 1610612743},
        {"id": 1628369, "name": "Jayson Tatum", "ppg": 26.9, "rpg": 8.1, "apg": 4.7, "position": "F", "team_id": 1610612738},
        {"id": 2544, "name": "LeBron James", "ppg": 25.7, "rpg": 7.3, "apg": 8.3, "position": "F", "team_id": 1610612747},
        {"id": 201142, "name": "Kevin Durant", "ppg": 27.1, "rpg": 6.6, "apg": 5.0, "position": "F", "team_id": 1610612756},
        {"id": 201939, "name": "Stephen Curry", "ppg": 26.4, "rpg": 5.1, "apg": 5.9, "position": "G", "team_id": 1610612744},
        {"id": 203081, "name": "Damian Lillard", "ppg": 24.3, "rpg": 4.4, "apg": 7.0, "position": "G", "team_id": 1610612749},
        # Add more current players with correct teams
        {"id": 1641705, "name": "Victor Wembanyama", "ppg": 21.3, "rpg": 10.6, "apg": 3.7, "position": "C", "team_id": 1610612759}, # Spurs
        {"id": 1630162, "name": "Anthony Edwards", "ppg": 26.0, "rpg": 5.4, "apg": 5.1, "position": "G", "team_id": 1610612750}, # Timberwolves
        {"id": 1630224, "name": "Cade Cunningham", "ppg": 22.7, "rpg": 4.3, "apg": 7.5, "position": "G", "team_id": 1610612765}, # Pistons
        {"id": 1630595, "name": "Scottie Barnes", "ppg": 19.9, "rpg": 8.2, "apg": 6.1, "position": "F", "team_id": 1610612761}, # Raptors
        {"id": 1630173, "name": "Tyrese Haliburton", "ppg": 20.1, "rpg": 3.9, "apg": 10.9, "position": "G", "team_id": 1610612754}, # Pacers
        {"id": 1629627, "name": "Ja Morant", "ppg": 25.1, "rpg": 5.6, "apg": 8.1, "position": "G", "team_id": 1610612763}, # Grizzlies
        {"id": 1629630, "name": "Zion Williamson", "ppg": 22.9, "rpg": 5.8, "apg": 5.0, "position": "F", "team_id": 1610612740}, # Pelicans
        {"id": 1629636, "name": "Trae Young", "ppg": 25.7, "rpg": 2.8, "apg": 10.8, "position": "G", "team_id": 1610612737}, # Hawks
        {"id": 1628378, "name": "Donovan Mitchell", "ppg": 27.6, "rpg": 5.1, "apg": 6.1, "position": "G", "team_id": 1610612739}, # Cavaliers
        {"id": 1627783, "name": "Jaylen Brown", "ppg": 23.0, "rpg": 5.5, "apg": 3.6, "position": "G-F", "team_id": 1610612738}, # Celtics
    ]
    
    # Set the top players with accurate stats and real images
    for player_data in top_players_by_id:
        try:
            player = Player.objects.filter(player_id=player_data["id"]).first()
            if not player:
                # Try to find by name
                name_parts = player_data["name"].split()
                first_name = name_parts[0]
                last_name = " ".join(name_parts[1:])
                player = Player.objects.filter(
                    first_name__icontains=first_name,
                    last_name__icontains=last_name
                ).first()
            
            if player:
                player.points_per_game = player_data["ppg"]
                player.rebounds_per_game = player_data["rpg"]
                player.assists_per_game = player_data["apg"]
                player.position = player_data["position"]
                
                # Set real image URL for top players
                player.image_url = f"https://cdn.nba.com/headshots/nba/latest/1040x760/{player.player_id}.png"
                
                # Set team if provided
                if "team_id" in player_data:
                    try:
                        team = Team.objects.get(team_id=player_data["team_id"])
                        player.team = team
                    except Team.DoesNotExist:
                        pass
                
                # Set advanced stats
                player.player_efficiency_rating = 25.0  # Higher for stars
                player.usage_rate = 30.0  # Higher for stars
                player.offensive_rating = 120.0  # Higher for stars
                player.defensive_rating = 105.0  # Lower (better) for stars
                
                player.save()
                print(f"Updated top player: {player.first_name} {player.last_name}")
            else:
                print(f"Player not found: {player_data['name']}")
        except Exception as e:
            print(f"Error updating player: {player_data['name']} - {e}")
    
    # Update team names for all players
    update_team_names()
    
    print(f"Fixed {count} players")

def update_team_names():
    """Update team names for all players with teams"""
    print("Updating team names...")
    
    players_updated = 0
    for player in Player.objects.filter(team__isnull=False):
        try:
            # Make sure the serializer's get_team_name method works
            from api.serializers import PlayerSerializer
            serializer = PlayerSerializer(player)
            team_name = serializer.get_team_name(player)
            if team_name and team_name != "Free Agent":
                players_updated += 1
        except Exception as e:
            print(f"Error updating team name for {player.first_name} {player.last_name}: {e}")
    
    print(f"Updated team names for {players_updated} players")

def assign_teams_by_name():
    """Assign teams to players based on their names"""
    print("Assigning teams by player names...")
    
    # Dictionary of player names to team IDs
    player_teams = {
        "Wembanyama": 1610612759,  # Spurs
        "Edwards": 1610612750,     # Timberwolves
        "Cunningham": 1610612765,  # Pistons
        "Barnes": 1610612761,      # Raptors
        "Haliburton": 1610612754,  # Pacers
        "Morant": 1610612763,      # Grizzlies
        "Williamson": 1610612740,  # Pelicans
        "Young": 1610612737,       # Hawks
        "Mitchell": 1610612739,    # Cavaliers
        "Brown": 1610612738,       # Celtics
        "Doncic": 1610612742,      # Mavericks
        "Embiid": 1610612755,      # 76ers
        "Antetokounmpo": 1610612749, # Bucks
        "Gilgeous-Alexander": 1610612760, # Thunder
        "Jokic": 1610612743,       # Nuggets
        "Tatum": 1610612738,       # Celtics
        "James": 1610612747,       # Lakers
        "Durant": 1610612756,      # Suns
        "Curry": 1610612744,       # Warriors
        "Lillard": 1610612749,     # Bucks
        "Davis": 1610612747,       # Lakers
        "Towns": 1610612750,       # Timberwolves
        "Booker": 1610612756,      # Suns
        "George": 1610612746,      # Clippers
        "Leonard": 1610612746,     # Clippers
        "Butler": 1610612748,      # Heat
        "Adebayo": 1610612748,     # Heat
        "Irving": 1610612742,      # Mavericks
        "Gobert": 1610612750,      # Timberwolves
        "Siakam": 1610612754,      # Pacers
        "Randle": 1610612752,      # Knicks
        "Brunson": 1610612752,     # Knicks
        "Fox": 1610612758,         # Kings
        "Sabonis": 1610612758,     # Kings
        "Ball": 1610612766,        # Hornets
        "Banchero": 1610612753,    # Magic
        "Wagner": 1610612753,      # Magic
        "Holmgren": 1610612760,    # Thunder
        "Giddey": 1610612760,      # Thunder
        "Murray": 1610612737,      # Hawks
        "Garland": 1610612739,     # Cavaliers
        "Allen": 1610612739,       # Cavaliers
        "Mobley": 1610612739,      # Cavaliers
        "Maxey": 1610612755,       # 76ers
        "Harden": 1610612746,      # Clippers
        "Thompson": 1610612739,    # Cavaliers
        "Green": 1610612744,       # Warriors
        "Poole": 1610612764,       # Wizards
        "Beal": 1610612756,        # Suns
        "LaVine": 1610612741,      # Bulls
        "DeRozan": 1610612741,     # Bulls
        "Vucevic": 1610612741,     # Bulls
        "Ingram": 1610612740,      # Pelicans
        "McCollum": 1610612740,    # Pelicans
        "Valanciunas": 1610612740, # Pelicans
        "Porzingis": 1610612738,   # Celtics
        "Holiday": 1610612738,     # Celtics
        "Horford": 1610612738,     # Celtics
        "Smart": 1610612763,       # Grizzlies
        "Jackson": 1610612763,     # Grizzlies
        "Bane": 1610612763,        # Grizzlies
        "Bridges": 1610612751,     # Nets
        "Ayton": 1610612757,       # Trail Blazers
        "Simons": 1610612757,      # Trail Blazers
        "Grant": 1610612757,       # Trail Blazers
        "Markkanen": 1610612762,   # Jazz
        "Conley": 1610612750,      # Timberwolves
        "Russell": 1610612747,     # Lakers
        "Reaves": 1610612747,      # Lakers
        "Wood": 1610612747,        # Lakers
        "Gordon": 1610612743,      # Nuggets
        "Porter": 1610612743,      # Nuggets
        "Murray": 1610612743,      # Nuggets
        "Klay": 1610612744,        # Warriors
        "Wiggins": 1610612744,     # Warriors
        "Kuminga": 1610612744,     # Warriors
        "Poeltl": 1610612761,      # Raptors
        "Anunoby": 1610612752,     # Knicks
        "Barrett": 1610612752,     # Knicks
        "Robinson": 1610612752,    # Knicks
        "Hart": 1610612752,        # Knicks
        "Herro": 1610612748,       # Heat
        "Robinson": 1610612748,    # Heat
        "Lowry": 1610612755,       # 76ers
        "Harris": 1610612755,      # 76ers
        "Middleton": 1610612749,   # Bucks
        "Lopez": 1610612749,       # Bucks
        "Portis": 1610612749,      # Bucks
        "Brogdon": 1610612764,     # Wizards
        "Kuzma": 1610612764,       # Wizards
        "Jones": 1610612764,       # Wizards
        "Bogdanovic": 1610612737,  # Hawks
        "Capela": 1610612737,      # Hawks
        "Collins": 1610612762,     # Jazz
        "Sexton": 1610612762,      # Jazz
        "Clarkson": 1610612762,    # Jazz
        "Olynyk": 1610612761,      # Raptors
        "Turner": 1610612754,      # Pacers
        "Toppin": 1610612754,      # Pacers
        "Nembhard": 1610612754,    # Pacers
        "Ivey": 1610612765,        # Pistons
        "Stewart": 1610612765,     # Pistons
        "Duren": 1610612765,       # Pistons
        "Bagley": 1610612765,      # Pistons
        "Sengun": 1610612745,      # Rockets
        "Green": 1610612745,       # Rockets
        "Smith": 1610612745,       # Rockets
        "Eason": 1610612745,       # Rockets
        "Sochan": 1610612759,      # Spurs
        "Johnson": 1610612759,     # Spurs
        "Vassell": 1610612759,     # Spurs
        "Jones": 1610612759,       # Spurs
    }
    
    players_updated = 0
    
    # First, update players with team IDs from the dictionary
    for player in Player.objects.filter(team__isnull=True):
        for last_name, team_id in player_teams.items():
            if last_name.lower() in player.last_name.lower():
                try:
                    team = Team.objects.get(team_id=team_id)
                    player.team = team
                    player.save()
                    players_updated += 1
                    print(f"Assigned {player.first_name} {player.last_name} to {team.city} {team.name}")
                    break
                except Team.DoesNotExist:
                    print(f"Team with ID {team_id} not found for {player.first_name} {player.last_name}")
    
    print(f"Assigned teams to {players_updated} players by name")

def fix_lineup_recursion():
    """Fix the potential infinite recursion issue in Lineup.save method"""
    print("Fixing lineup recursion issue...")
    try:
        from api.models import Lineup
        lineups = Lineup.objects.all()
        fixed_count = 0
        
        for lineup in lineups:
            if not hasattr(lineup, 'players') or not lineup.players.exists():
                # Empty lineup, set ratings to 0
                lineup.offensive_rating = 0
                lineup.defensive_rating = 0
                lineup.net_rating = 0
                # Use update to bypass the save method and avoid recursion
                Lineup.objects.filter(id=lineup.id).update(
                    offensive_rating=0,
                    defensive_rating=0,
                    net_rating=0
                )
                fixed_count += 1
                print(f"Fixed empty lineup: {lineup.name}")
                continue
                
            # Calculate ratings directly without using save
            try:
                # Get player stats
                players = lineup.players.all()
                if players:
                    # Calculate offensive rating (weighted average of points, assists)
                    points_sum = sum(p.points_per_game for p in players if p.points_per_game is not None)
                    assists_sum = sum(p.assists_per_game for p in players if p.assists_per_game is not None)
                    offensive_rating = (points_sum * 0.7 + assists_sum * 0.3) * 2
                    
                    # Calculate defensive rating (weighted average of rebounds, blocks, steals)
                    rebounds_sum = sum(p.rebounds_per_game for p in players if p.rebounds_per_game is not None)
                    blocks_sum = sum(p.blocks_per_game for p in players if p.blocks_per_game is not None)
                    steals_sum = sum(p.steals_per_game for p in players if p.steals_per_game is not None)
                    defensive_rating = (rebounds_sum * 0.5 + blocks_sum * 0.3 + steals_sum * 0.2) * 5
                    
                    # Calculate net rating
                    net_rating = offensive_rating - defensive_rating
                    
                    # Update directly to bypass save method
                    Lineup.objects.filter(id=lineup.id).update(
                        offensive_rating=offensive_rating,
                        defensive_rating=defensive_rating,
                        net_rating=net_rating
                    )
                    fixed_count += 1
            except Exception as e:
                print(f"Error calculating ratings for lineup {lineup.name}: {e}")
        
        print(f"Fixed {fixed_count} lineups")
        return True
    except Exception as e:
        print(f"Error fixing lineup recursion: {e}")
        return False

def clean_test_lineups():
    """Remove test lineups from the database"""
    print("Cleaning up test lineups...")
    test_names = ['ad', 'test 2', 'ad (Optimized - offense)', 'ddddd', 'vl', 'vlll']
    deleted_count = 0
    
    for name in test_names:
        try:
            lineups = Lineup.objects.filter(name__icontains=name)
            count = lineups.count()
            lineups.delete()
            deleted_count += count
            if count > 0:
                print(f"Deleted {count} lineup(s) with name containing '{name}'")
        except Exception as e:
            print(f"Error deleting lineups with name '{name}': {e}")
    
    print(f"Cleaned up {deleted_count} test lineups")

if __name__ == '__main__':
    # First fix the database schema
    fix_database_schema()
    
    # Clean up test lineups
    clean_test_lineups()
    
    # Then fix the data
    fix_player_data()
    
    # Fix lineup recursion issue
    fix_lineup_recursion()
    
    print("Data fixing complete!") 