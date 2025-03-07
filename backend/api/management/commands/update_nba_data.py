from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import time
import json
import logging
from api.models import Player, Team
from nba_api.stats.static import teams, players
from nba_api.stats.endpoints import leagueleaders, commonplayerinfo

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Update NBA data periodically and broadcast changes via WebSockets'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--continuous',
            action='store_true',
            help='Run continuously with the interval specified in settings',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force update even if data was recently updated',
        )
    
    def handle(self, *args, **options):
        if options['continuous']:
            self.stdout.write(self.style.SUCCESS('Starting continuous NBA data updates...'))
            interval = getattr(settings, 'DATA_UPDATE_INTERVAL', 3600)  # Default to 1 hour
            
            while True:
                try:
                    self.update_data()
                    self.stdout.write(self.style.SUCCESS(f'Data updated successfully at {timezone.now()}'))
                    time.sleep(interval)
                except KeyboardInterrupt:
                    self.stdout.write(self.style.WARNING('Update process stopped by user'))
                    break
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error updating data: {str(e)}'))
                    # Wait a bit before retrying
                    time.sleep(60)
        else:
            force = options['force']
            
            # Check if data was updated recently (within the last 24 hours)
            last_updated = None
            try:
                last_player = Player.objects.latest('last_updated')
                last_updated = last_player.last_updated
            except (Player.DoesNotExist, AttributeError):
                pass
            
            if last_updated and not force:
                time_since_update = timezone.now() - last_updated
                if time_since_update.total_seconds() < 86400:  # 24 hours
                    self.stdout.write(self.style.WARNING(
                        f'Data was updated recently ({time_since_update.total_seconds() / 3600:.1f} hours ago). '
                        f'Use --force to update anyway.'
                    ))
                    return
            
            self.stdout.write(self.style.SUCCESS('Starting NBA data update...'))
            
            # Update teams
            self._update_teams()
            
            # Update players
            self._update_players()
            
            # Update player stats
            self._update_player_stats()
            
            self.stdout.write(self.style.SUCCESS('NBA data update completed successfully!'))
    
    def _update_teams(self):
        """Update NBA teams from the NBA API"""
        self.stdout.write('Updating teams...')
        
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
            
            self.stdout.write(self.style.SUCCESS(f'Successfully updated {len(nba_teams)} teams'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error updating teams: {str(e)}'))
            logger.error(f'Error updating teams: {str(e)}')
    
    def _update_players(self):
        """Update NBA players from the NBA API"""
        self.stdout.write('Updating players...')
        
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
                        'last_updated': timezone.now(),
                    }
                )
                
                # Sleep to avoid rate limiting
                time.sleep(0.1)
            
            self.stdout.write(self.style.SUCCESS(f'Successfully updated {len(nba_players)} players'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error updating players: {str(e)}'))
            logger.error(f'Error updating players: {str(e)}')
    
    def _update_player_stats(self):
        """Update player statistics from the NBA API"""
        self.stdout.write('Updating player statistics...')
        
        try:
            # Get league leaders for various statistics
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
            
            self.stdout.write(self.style.SUCCESS('Successfully updated player statistics'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error updating player statistics: {str(e)}'))
            logger.error(f'Error updating player statistics: {str(e)}')
    
    def broadcast_updates(self, changes):
        """Broadcast updates to connected WebSocket clients"""
        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "nba_updates",
                {
                    "type": "nba_update",
                    "data": changes
                }
            )
            self.stdout.write(self.style.SUCCESS('Updates broadcasted to connected clients'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error broadcasting updates: {str(e)}')) 