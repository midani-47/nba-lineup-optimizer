from django.core.management.base import BaseCommand
from api.models import Team, Player
from nba_api.stats.static import teams, players
from nba_api.stats.endpoints import leagueleaders, commonplayerinfo
import pandas as pd
import time
from django.utils import timezone
from api.serializers import PlayerSerializer
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Load NBA data from the NBA API'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting NBA data load...'))
        
        # Load teams
        self.load_teams()
        
        # Load players
        self.load_players()
        
        # Load player stats
        self.load_player_stats()
        
        self.stdout.write(self.style.SUCCESS('NBA data load completed successfully!'))
    
    def load_teams(self):
        """Load NBA teams from the NBA API"""
        self.stdout.write('Loading teams...')
        
        try:
            # Get all NBA teams
            nba_teams = teams.get_teams()
            
            for team_data in nba_teams:
                Team.objects.update_or_create(
                    team_id=team_data['id'],
                    defaults={
                        'name': team_data['nickname'],
                        'abbreviation': team_data['abbreviation'],
                        'city': team_data['city'],
                        'conference': team_data.get('conference', ''),
                        'division': team_data.get('division', '')
                    }
                )
            
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(nba_teams)} teams'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading teams: {str(e)}'))
            # Fallback to sample data if API fails
            self.load_sample_teams()
    
    def load_sample_teams(self):
        """Load sample NBA teams as fallback"""
        self.stdout.write('Loading sample teams...')
        
        sample_teams = [
            {"team_id": 1610612737, "name": "Hawks", "abbreviation": "ATL", "city": "Atlanta", "conference": "East", "division": "Southeast"},
            {"team_id": 1610612738, "name": "Celtics", "abbreviation": "BOS", "city": "Boston", "conference": "East", "division": "Atlantic"},
            {"team_id": 1610612739, "name": "Cavaliers", "abbreviation": "CLE", "city": "Cleveland", "conference": "East", "division": "Central"},
            {"team_id": 1610612740, "name": "Pelicans", "abbreviation": "NOP", "city": "New Orleans", "conference": "West", "division": "Southwest"},
            {"team_id": 1610612741, "name": "Bulls", "abbreviation": "CHI", "city": "Chicago", "conference": "East", "division": "Central"},
            {"team_id": 1610612742, "name": "Mavericks", "abbreviation": "DAL", "city": "Dallas", "conference": "West", "division": "Southwest"},
            {"team_id": 1610612743, "name": "Nuggets", "abbreviation": "DEN", "city": "Denver", "conference": "West", "division": "Northwest"},
            {"team_id": 1610612744, "name": "Warriors", "abbreviation": "GSW", "city": "Golden State", "conference": "West", "division": "Pacific"},
            {"team_id": 1610612745, "name": "Rockets", "abbreviation": "HOU", "city": "Houston", "conference": "West", "division": "Southwest"},
            {"team_id": 1610612746, "name": "Clippers", "abbreviation": "LAC", "city": "Los Angeles", "conference": "West", "division": "Pacific"},
        ]
        
        for team_data in sample_teams:
            Team.objects.update_or_create(
                team_id=team_data["team_id"],
                defaults=team_data
            )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(sample_teams)} sample teams'))
    
    def load_players(self):
        """Load NBA players from the NBA API"""
        self.stdout.write('Loading players...')
        
        try:
            # Get all active NBA players
            nba_players = players.get_active_players()
            
            for player_data in nba_players:
                try:
                    team = Team.objects.get(team_id=player_data.get('team_id'))
                except Team.DoesNotExist:
                    team = None
                
                Player.objects.update_or_create(
                    player_id=player_data['id'],
                    defaults={
                        'first_name': player_data['first_name'],
                        'last_name': player_data['last_name'],
                        'team': team,
                        'position': player_data.get('position', ''),
                        'height': player_data.get('height', ''),
                        'weight': player_data.get('weight', 0),
                        'jersey_number': player_data.get('jersey', 0),
                    }
                )
                
                # Sleep to avoid rate limiting
                time.sleep(0.1)
            
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(nba_players)} players'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading players: {str(e)}'))
            # Fallback to sample data if API fails
            self.load_sample_players()
    
    def load_sample_players(self):
        """Load sample NBA players as fallback"""
        self.stdout.write('Loading sample players...')
        
        sample_players = [
            {"player_id": 2544, "first_name": "LeBron", "last_name": "James", "team_id": 1610612747, "position": "F", "points_per_game": 25.7, "rebounds_per_game": 7.3, "assists_per_game": 8.3, "field_goal_percentage": 0.538, "three_point_percentage": 0.397, "player_efficiency_rating": 26.2, "offensive_rating": 118.2, "defensive_rating": 110.5},
            {"player_id": 201939, "first_name": "Stephen", "last_name": "Curry", "team_id": 1610612744, "position": "G", "points_per_game": 29.4, "rebounds_per_game": 6.1, "assists_per_game": 6.3, "field_goal_percentage": 0.485, "three_point_percentage": 0.428, "player_efficiency_rating": 24.6, "offensive_rating": 120.4, "defensive_rating": 112.8},
            {"player_id": 203954, "first_name": "Joel", "last_name": "Embiid", "team_id": 1610612755, "position": "C", "points_per_game": 33.1, "rebounds_per_game": 11.3, "assists_per_game": 4.2, "field_goal_percentage": 0.529, "three_point_percentage": 0.377, "player_efficiency_rating": 31.8, "offensive_rating": 121.5, "defensive_rating": 106.7},
            {"player_id": 203507, "first_name": "Giannis", "last_name": "Antetokounmpo", "team_id": 1610612749, "position": "F", "points_per_game": 30.4, "rebounds_per_game": 11.5, "assists_per_game": 5.7, "field_goal_percentage": 0.612, "three_point_percentage": 0.274, "player_efficiency_rating": 29.3, "offensive_rating": 119.8, "defensive_rating": 107.2},
            {"player_id": 1629029, "first_name": "Luka", "last_name": "Doncic", "team_id": 1610612742, "position": "G", "points_per_game": 32.4, "rebounds_per_game": 9.2, "assists_per_game": 8.9, "field_goal_percentage": 0.495, "three_point_percentage": 0.382, "player_efficiency_rating": 28.4, "offensive_rating": 117.9, "defensive_rating": 112.3},
            {"player_id": 1628369, "first_name": "Jayson", "last_name": "Tatum", "team_id": 1610612738, "position": "F", "points_per_game": 26.9, "rebounds_per_game": 8.1, "assists_per_game": 4.7, "field_goal_percentage": 0.472, "three_point_percentage": 0.371, "player_efficiency_rating": 23.5, "offensive_rating": 116.2, "defensive_rating": 108.4},
            {"player_id": 1627783, "first_name": "Jaylen", "last_name": "Brown", "team_id": 1610612738, "position": "G-F", "points_per_game": 23.5, "rebounds_per_game": 5.6, "assists_per_game": 3.5, "field_goal_percentage": 0.491, "three_point_percentage": 0.354, "player_efficiency_rating": 21.8, "offensive_rating": 115.7, "defensive_rating": 109.2},
            {"player_id": 1629027, "first_name": "Trae", "last_name": "Young", "team_id": 1610612737, "position": "G", "points_per_game": 26.1, "rebounds_per_game": 2.8, "assists_per_game": 10.8, "field_goal_percentage": 0.431, "three_point_percentage": 0.371, "player_efficiency_rating": 22.7, "offensive_rating": 114.8, "defensive_rating": 116.5},
            {"player_id": 1628378, "first_name": "Donovan", "last_name": "Mitchell", "team_id": 1610612739, "position": "G", "points_per_game": 27.6, "rebounds_per_game": 5.1, "assists_per_game": 6.1, "field_goal_percentage": 0.466, "three_point_percentage": 0.374, "player_efficiency_rating": 23.1, "offensive_rating": 116.9, "defensive_rating": 111.3},
            {"player_id": 203081, "first_name": "Damian", "last_name": "Lillard", "team_id": 1610612749, "position": "G", "points_per_game": 24.3, "rebounds_per_game": 4.4, "assists_per_game": 7.0, "field_goal_percentage": 0.435, "three_point_percentage": 0.371, "player_efficiency_rating": 22.4, "offensive_rating": 115.6, "defensive_rating": 113.8},
        ]
        
        for player_data in sample_players:
            team_id = player_data.pop("team_id", None)
            team = None
            if team_id:
                try:
                    team = Team.objects.get(team_id=team_id)
                except Team.DoesNotExist:
                    pass
            
            Player.objects.update_or_create(
                player_id=player_data["player_id"],
                defaults={**player_data, "team": team}
            )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(sample_players)} sample players'))
    
    def load_player_stats(self):
        """Load player statistics from the NBA API"""
        self.stdout.write('Loading player statistics...')
        
        try:
            # Get league leaders for various statistics
            # This is just an example - in a real app, you would fetch more comprehensive stats
            leaders = leagueleaders.LeagueLeaders(season='2023-24').get_data_frames()[0]
            
            for _, row in leaders.iterrows():
                try:
                    player = Player.objects.get(player_id=row['PLAYER_ID'])
                    
                    # Update player stats
                    player.points_per_game = row.get('PTS', 0)
                    player.rebounds_per_game = row.get('REB', 0)
                    player.assists_per_game = row.get('AST', 0)
                    player.steals_per_game = row.get('STL', 0)
                    player.blocks_per_game = row.get('BLK', 0)
                    player.field_goal_percentage = row.get('FG_PCT', 0)
                    player.three_point_percentage = row.get('FG3_PCT', 0)
                    player.free_throw_percentage = row.get('FT_PCT', 0)
                    
                    # For advanced stats, we would need to fetch from other endpoints
                    # This is simplified for the demo
                    player.save()
                    
                except Player.DoesNotExist:
                    pass
                
                # Sleep to avoid rate limiting
                time.sleep(0.1)
            
            self.stdout.write(self.style.SUCCESS('Successfully loaded player statistics'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading player statistics: {str(e)}'))
            # We already have stats in our sample data, so no need for a fallback here 

    def _update_player_stats(self):
        """Update player statistics from the NBA API"""
        self.stdout.write('Updating player statistics...')
        
        try:
            # Get league leaders for various statistics
            leaders = leagueleaders.LeagueLeaders(season='2023-24').get_data_frames()[0]
            
            for _, row in leaders.iterrows():
                try:
                    player = Player.objects.get(player_id=row['PLAYER_ID'])
                    
                    # Update player stats - convert to per-game stats
                    games_played = row.get('GP', 1)  # Default to 1 to avoid division by zero
                    
                    # Make sure we're storing per-game stats
                    player.points_per_game = row.get('PTS', 0) / games_played
                    player.rebounds_per_game = row.get('REB', 0) / games_played
                    player.assists_per_game = row.get('AST', 0) / games_played
                    player.steals_per_game = row.get('STL', 0) / games_played
                    player.blocks_per_game = row.get('BLK', 0) / games_played
                    
                    # Make sure percentages are stored as decimals (0.0-1.0)
                    player.field_goal_percentage = row.get('FG_PCT', 0)
                    player.three_point_percentage = row.get('FG3_PCT', 0)
                    player.free_throw_percentage = row.get('FT_PCT', 0)
                    
                    # Set position if it's empty
                    if not player.position or player.position == '':
                        # Try to infer position from height/weight or set a default
                        player.position = self._infer_position(player) or 'G-F'
                    
                    # For advanced stats, we would need to fetch from other endpoints
                    # This is simplified for the demo
                    if player.player_efficiency_rating == 0:
                        player.player_efficiency_rating = 15.0  # League average PER
                    if player.usage_rate == 0:
                        player.usage_rate = 20.0  # Approximate league average
                    if player.true_shooting_percentage == 0:
                        player.true_shooting_percentage = 0.55  # Approximate league average
                    
                    # Update offensive and defensive ratings if they're zero
                    if player.offensive_rating == 0:
                        player.offensive_rating = 110.0  # Approximate league average
                    if player.defensive_rating == 0:
                        player.defensive_rating = 110.0  # Approximate league average
                    
                    player.last_updated = timezone.now()
                    player.save()
                    
                except Player.DoesNotExist:
                    pass
                
                # Sleep to avoid rate limiting
                time.sleep(0.1)
            
            # Update team names for all players
            self._update_team_names()
            
            self.stdout.write(self.style.SUCCESS('Successfully updated player statistics'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error updating player statistics: {str(e)}'))
            logger.error(f'Error updating player statistics: {str(e)}')

    def _update_team_names(self):
        """Update team names for all players"""
        self.stdout.write('Updating team names...')
        
        players_updated = 0
        for player in Player.objects.filter(team__isnull=False):
            player_serializer = PlayerSerializer(player)
            team_name = player_serializer.get_team_name(player)
            if team_name:
                players_updated += 1
        
        self.stdout.write(self.style.SUCCESS(f'Updated team names for {players_updated} players'))

    def _infer_position(self, player):
        """Infer player position based on height/weight if available"""
        # This is a very simplified position inference
        # In a real app, you would use more sophisticated logic
        
        if player.height and player.weight:
            height_inches = self._convert_height_to_inches(player.height)
            
            if height_inches >= 83:  # 6'11" or taller
                return 'C'
            elif height_inches >= 80:  # 6'8" or taller
                return 'F'
            elif height_inches >= 77:  # 6'5" or taller
                return 'G-F'
            elif height_inches >= 74:  # 6'2" or taller
                return 'G'
            else:
                return 'G'
        
        return None

    def _convert_height_to_inches(self, height_str):
        """Convert height string (e.g., '6-11') to inches"""
        try:
            if '-' in height_str:
                feet, inches = height_str.split('-')
                return int(feet) * 12 + int(inches)
            return 0
        except (ValueError, TypeError):
            return 0 