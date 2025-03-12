from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Team, Player, Lineup, LineupComparison
from django.db.models import Avg

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
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Player
        fields = '__all__'
    
    def get_team_name(self, obj):
        try:
            if obj.team:
                return f"{obj.team.city} {obj.team.name}"
        except Exception:
            # Handle case where team doesn't exist
            pass
        return "Free Agent"  # Default for players without a team
    
    def get_image_url(self, obj):
        if obj.image_url:
            return obj.image_url
        try:
            return f"https://cdn.nba.com/headshots/nba/latest/1040x760/{obj.player_id}.png"
        except Exception:
            return "https://via.placeholder.com/300x300/1a428a/ffffff?text=NBA"

class PlayerListSerializer(serializers.ModelSerializer):
    """Simplified player serializer for list views"""
    team_name = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Player
        fields = ['player_id', 'first_name', 'last_name', 'position', 'team_name', 
                  'points_per_game', 'rebounds_per_game', 'assists_per_game', 'image_url']
    
    def get_team_name(self, obj):
        try:
            if obj.team:
                return f"{obj.team.city} {obj.team.name}"
        except Exception:
            # Handle case where team doesn't exist
            pass
        return "Free Agent"  # Default for players without a team
    
    def get_image_url(self, obj):
        if obj.image_url:
            return obj.image_url
        try:
            return f"https://cdn.nba.com/headshots/nba/latest/1040x760/{obj.player_id}.png"
        except Exception:
            return "https://via.placeholder.com/300x300/1a428a/ffffff?text=NBA"

class LineupPlayerSerializer(serializers.ModelSerializer):
    """Simplified player serializer for lineup views"""
    full_name = serializers.CharField(read_only=True)
    team_name = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Player
        fields = ['player_id', 'full_name', 'position', 'team_name', 
                  'points_per_game', 'rebounds_per_game', 'assists_per_game', 'image_url']
    
    def get_team_name(self, obj):
        try:
            if obj.team:
                return f"{obj.team.city} {obj.team.name}"
        except Exception:
            # Handle case where team doesn't exist
            pass
        return "Free Agent"  # Default for players without a team
        
    def get_image_url(self, obj):
        if obj.image_url:
            return obj.image_url
        try:
            return f"https://cdn.nba.com/headshots/nba/latest/1040x760/{obj.player_id}.png"
        except Exception:
            return "https://via.placeholder.com/300x300/1a428a/ffffff?text=NBA"

class LineupSerializer(serializers.ModelSerializer):
    players = LineupPlayerSerializer(many=True, read_only=True)
    player_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    total_stats = serializers.SerializerMethodField()
    
    class Meta:
        model = Lineup
        fields = ['id', 'name', 'user', 'players', 'player_ids', 'total_stats',
                 'offensive_rating', 'defensive_rating', 'net_rating', 
                 'created_at', 'updated_at']
        read_only_fields = ['offensive_rating', 'defensive_rating', 'net_rating']
    
    def get_total_stats(self, obj):
        """Calculate and return total stats for the lineup"""
        if not obj.players.exists():
            return {
                'ppg': 0, 'rpg': 0, 'apg': 0, 'spg': 0, 'bpg': 0,
                'fg_pct': 0, 'fg3_pct': 0, 'ft_pct': 0
            }
        
        players = obj.players.all()
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
    
    def validate_player_ids(self, value):
        """Validate player IDs"""
        if not value:
            raise serializers.ValidationError("At least one player is required")
        
        if len(value) > 5:
            raise serializers.ValidationError("A lineup cannot have more than 5 players")
        
        # Check if all players exist
        existing_ids = set(Player.objects.filter(
            player_id__in=value
        ).values_list('player_id', flat=True))
        
        missing_ids = set(value) - existing_ids
        if missing_ids:
            raise serializers.ValidationError(
                f"Players with IDs {missing_ids} do not exist"
            )
        
        return value
    
    def create(self, validated_data):
        """Create a new lineup with proper error handling"""
        try:
            # Extract and remove player_ids from validated_data
            player_ids = validated_data.pop('player_ids', [])
            
            # Create the lineup
            lineup = Lineup.objects.create(**validated_data)
            
            # Add players
            if player_ids:
                players = Player.objects.filter(player_id__in=player_ids)
                lineup.players.set(players)
            
            # Calculate ratings
            lineup.calculate_ratings()
            
            return lineup
            
        except Exception as e:
            print(f"Error creating lineup: {str(e)}")
            raise serializers.ValidationError(f"Failed to create lineup: {str(e)}")
    
    def update(self, instance, validated_data):
        """Update a lineup with proper error handling"""
        try:
            # Extract and remove player_ids from validated_data
            player_ids = validated_data.pop('player_ids', None)
            
            # Update basic fields
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            
            # Update players if provided
            if player_ids is not None:
                players = Player.objects.filter(player_id__in=player_ids)
                instance.players.set(players)
            
            # Calculate ratings and save
            instance.calculate_ratings()
            instance.save()
            
            return instance
            
        except Exception as e:
            print(f"Error updating lineup: {str(e)}")
            raise serializers.ValidationError(f"Failed to update lineup: {str(e)}")

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
        # Check if a comparison with this name already exists
        name = validated_data.get('name')
        if name and LineupComparison.objects.filter(name__iexact=name).exists():
            raise serializers.ValidationError({"name": "A lineup comparison with this name already exists."})
            
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
        lineup1_avg = lineup1.players.aggregate(avg=Avg(stat_field))['avg'] or 0
        lineup2_avg = lineup2.players.aggregate(avg=Avg(stat_field))['avg'] or 0
        return lineup1_avg - lineup2_avg 