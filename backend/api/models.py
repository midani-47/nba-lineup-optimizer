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
        if self.players.count() == 0:
            return
            
        # Simple average of player ratings for now
        # In a real app, this would use more sophisticated calculations
        self.offensive_rating = self.players.aggregate(models.Avg('offensive_rating'))['offensive_rating__avg']
        self.defensive_rating = self.players.aggregate(models.Avg('defensive_rating'))['defensive_rating__avg']
        self.net_rating = self.offensive_rating - self.defensive_rating
        self.save()

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
