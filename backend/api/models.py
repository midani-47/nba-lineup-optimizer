from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    team_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=5)
    city = models.CharField(max_length=100)
    conference = models.CharField(max_length=10)
    division = models.CharField(max_length=20)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.city} {self.name}"

class Player(models.Model):
    player_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players', null=True, blank=True)
    position = models.CharField(max_length=10)
    height = models.CharField(max_length=10, null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    jersey_number = models.IntegerField(null=True, blank=True)
    image_url = models.URLField(max_length=500, null=True, blank=True)
    
    # Basic stats
    points_per_game = models.FloatField(default=0)
    rebounds_per_game = models.FloatField(default=0)
    assists_per_game = models.FloatField(default=0)
    steals_per_game = models.FloatField(default=0)
    blocks_per_game = models.FloatField(default=0)
    turnovers_per_game = models.FloatField(default=0)
    
    # Shooting stats
    field_goal_percentage = models.FloatField(default=0)
    three_point_percentage = models.FloatField(default=0)
    free_throw_percentage = models.FloatField(default=0)
    
    # Advanced stats
    player_efficiency_rating = models.FloatField(default=0)
    usage_rate = models.FloatField(default=0)
    true_shooting_percentage = models.FloatField(default=0)
    offensive_rating = models.FloatField(default=0)
    defensive_rating = models.FloatField(default=0)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_injured = models.BooleanField(default=False)
    
    # Last updated
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Lineup(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lineups', null=True, blank=True)
    players = models.ManyToManyField(Player, related_name='lineups')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Lineup performance metrics (calculated)
    offensive_rating = models.FloatField(null=True, blank=True)
    defensive_rating = models.FloatField(null=True, blank=True)
    net_rating = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def calculate_ratings(self):
        """Calculate offensive, defensive, and net ratings based on player stats"""
        try:
            if not self.players.exists():
                self.offensive_rating = 0
                self.defensive_rating = 0
                self.net_rating = 0
                self.save()
                return
            
            # Get all players in a single query
            players = self.players.all()
            
            # Calculate offensive rating (weighted average of points and assists)
            total_points = sum(p.points_per_game for p in players)
            total_assists = sum(p.assists_per_game for p in players)
            self.offensive_rating = (total_points * 0.7 + total_assists * 0.3) * 2
            
            # Calculate defensive rating (weighted average of rebounds, steals, and blocks)
            total_rebounds = sum(p.rebounds_per_game for p in players)
            total_steals = sum(p.steals_per_game for p in players)
            total_blocks = sum(p.blocks_per_game for p in players)
            self.defensive_rating = (
                total_rebounds * 0.5 + 
                total_steals * 0.25 + 
                total_blocks * 0.25
            ) * 2
            
            # Calculate net rating
            self.net_rating = self.offensive_rating - self.defensive_rating
            
            # Ensure ratings are not null
            self.offensive_rating = self.offensive_rating or 0
            self.defensive_rating = self.defensive_rating or 0
            self.net_rating = self.net_rating or 0
            
            self.save()
            
        except Exception as e:
            print(f"Error calculating ratings for lineup {self.id}: {str(e)}")
            # Set default values in case of error
            self.offensive_rating = 0
            self.defensive_rating = 0
            self.net_rating = 0
            self.save()
    
    def get_total_stats(self):
        """Calculate total stats for the lineup"""
        try:
            if not self.players.exists():
                return {
                    'ppg': 0, 'rpg': 0, 'apg': 0, 'spg': 0, 'bpg': 0,
                    'fg_pct': 0, 'fg3_pct': 0, 'ft_pct': 0
                }
            
            players = self.players.all()
            
            # Calculate totals
            total_ppg = sum(p.points_per_game for p in players)
            total_rpg = sum(p.rebounds_per_game for p in players)
            total_apg = sum(p.assists_per_game for p in players)
            total_spg = sum(p.steals_per_game for p in players)
            total_bpg = sum(p.blocks_per_game for p in players)
            
            # Calculate average percentages
            count = players.count()
            avg_fg = sum(p.field_goal_percentage for p in players) / count if count > 0 else 0
            avg_fg3 = sum(p.three_point_percentage for p in players) / count if count > 0 else 0
            avg_ft = sum(p.free_throw_percentage for p in players) / count if count > 0 else 0
            
            return {
                'ppg': round(total_ppg, 1),
                'rpg': round(total_rpg, 1),
                'apg': round(total_apg, 1),
                'spg': round(total_spg, 1),
                'bpg': round(total_bpg, 1),
                'fg_pct': round(avg_fg, 3),
                'fg3_pct': round(avg_fg3, 3),
                'ft_pct': round(avg_ft, 3)
            }
            
        except Exception as e:
            print(f"Error calculating total stats for lineup {self.id}: {str(e)}")
            return {
                'ppg': 0, 'rpg': 0, 'apg': 0, 'spg': 0, 'bpg': 0,
                'fg_pct': 0, 'fg3_pct': 0, 'ft_pct': 0
            }
    
    def save(self, *args, **kwargs):
        """Override save to ensure ratings are calculated"""
        super().save(*args, **kwargs)
        if not kwargs.get('skip_ratings', False):
            self.calculate_ratings()

class LineupComparison(models.Model):
    """Model to store lineup comparison results"""
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comparisons', null=True, blank=True)
    lineup1 = models.ForeignKey(Lineup, on_delete=models.CASCADE, related_name='comparison_as_first')
    lineup2 = models.ForeignKey(Lineup, on_delete=models.CASCADE, related_name='comparison_as_second')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Comparison metrics
    points_diff = models.FloatField(null=True, blank=True)
    rebounds_diff = models.FloatField(null=True, blank=True)
    assists_diff = models.FloatField(null=True, blank=True)
    net_rating_diff = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"Comparison: {self.lineup1.name} vs {self.lineup2.name}"
