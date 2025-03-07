from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Team, Player, Lineup, LineupComparison

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class PlayerSerializer(serializers.ModelSerializer):
    team_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Player
        fields = '__all__'
    
    def get_team_name(self, obj):
        if obj.team:
            return f"{obj.team.city} {obj.team.name}"
        return "Free Agent"  # Default for players without a team

class PlayerListSerializer(serializers.ModelSerializer):
    """Simplified player serializer for list views"""
    team_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Player
        fields = ['player_id', 'first_name', 'last_name', 'position', 'team_name', 
                  'points_per_game', 'rebounds_per_game', 'assists_per_game']
    
    def get_team_name(self, obj):
        if obj.team:
            return f"{obj.team.city} {obj.team.name}"
        return "Free Agent"  # Default for players without a team

class LineupPlayerSerializer(serializers.ModelSerializer):
    """Simplified player serializer for lineup views"""
    full_name = serializers.CharField(read_only=True)
    team_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Player
        fields = ['player_id', 'full_name', 'position', 'team_name', 
                  'points_per_game', 'rebounds_per_game', 'assists_per_game']
    
    def get_team_name(self, obj):
        if obj.team:
            return f"{obj.team.city} {obj.team.name}"
        return "Free Agent"  # Default for players without a team

class LineupSerializer(serializers.ModelSerializer):
    players = LineupPlayerSerializer(many=True, read_only=True)
    player_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Lineup
        fields = ['id', 'name', 'user', 'players', 'player_ids', 'offensive_rating', 
                  'defensive_rating', 'net_rating', 'created_at', 'updated_at']
        read_only_fields = ['offensive_rating', 'defensive_rating', 'net_rating']
    
    def create(self, validated_data):
        player_ids = validated_data.pop('player_ids', [])
        lineup = Lineup.objects.create(**validated_data)
        
        # Add players to lineup
        for player_id in player_ids:
            try:
                player = Player.objects.get(player_id=player_id)
                lineup.players.add(player)
            except Player.DoesNotExist:
                pass
        
        # Calculate ratings
        lineup.calculate_ratings()
        return lineup
    
    def update(self, instance, validated_data):
        player_ids = validated_data.pop('player_ids', None)
        
        # Update lineup fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Update players if provided
        if player_ids is not None:
            instance.players.clear()
            for player_id in player_ids:
                try:
                    player = Player.objects.get(player_id=player_id)
                    instance.players.add(player)
                except Player.DoesNotExist:
                    pass
        
        # Calculate ratings
        instance.calculate_ratings()
        instance.save()
        return instance

class LineupComparisonSerializer(serializers.ModelSerializer):
    lineup1_details = LineupSerializer(source='lineup1', read_only=True)
    lineup2_details = LineupSerializer(source='lineup2', read_only=True)
    
    class Meta:
        model = LineupComparison
        fields = ['id', 'name', 'user', 'lineup1', 'lineup2', 
                  'lineup1_details', 'lineup2_details',
                  'points_diff', 'rebounds_diff', 'assists_diff', 'net_rating_diff',
                  'created_at']
        read_only_fields = ['points_diff', 'rebounds_diff', 'assists_diff', 'net_rating_diff']
    
    def create(self, validated_data):
        comparison = LineupComparison.objects.create(**validated_data)
        self._calculate_comparison_metrics(comparison)
        return comparison
    
    def _calculate_comparison_metrics(self, comparison):
        """Calculate comparison metrics between two lineups"""
        lineup1 = comparison.lineup1
        lineup2 = comparison.lineup2
        
        # Ensure ratings are calculated
        lineup1.calculate_ratings()
        lineup2.calculate_ratings()
        
        # Calculate differences
        comparison.points_diff = self._calculate_stat_diff(lineup1, lineup2, 'points_per_game')
        comparison.rebounds_diff = self._calculate_stat_diff(lineup1, lineup2, 'rebounds_per_game')
        comparison.assists_diff = self._calculate_stat_diff(lineup1, lineup2, 'assists_per_game')
        comparison.net_rating_diff = lineup1.net_rating - lineup2.net_rating if lineup1.net_rating and lineup2.net_rating else 0
        
        comparison.save()
    
    def _calculate_stat_diff(self, lineup1, lineup2, stat_field):
        """Calculate the difference in average stats between two lineups"""
        lineup1_avg = lineup1.players.aggregate(avg=serializers.Avg(stat_field))['avg'] or 0
        lineup2_avg = lineup2.players.aggregate(avg=serializers.Avg(stat_field))['avg'] or 0
        return lineup1_avg - lineup2_avg 