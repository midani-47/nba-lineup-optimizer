from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q, F
from django.contrib.auth.models import User
from .models import Team, Player, Lineup, LineupComparison
from .serializers import (
    UserSerializer, TeamSerializer, PlayerSerializer, PlayerListSerializer,
    LineupSerializer, LineupComparisonSerializer
)
from nba_api.stats.endpoints import leagueleaders, commonplayerinfo, teamdetails
import pandas as pd
import numpy as np

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'city', 'abbreviation']
    
    @action(detail=False, methods=['post'])
    def refresh_teams(self, request):
        """Refresh team data from NBA API"""
        try:
            # This is a placeholder - in a real app, you would use nba_api to fetch team data
            # For demo purposes, we'll create some sample teams
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
            
            return Response({"message": "Teams refreshed successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'team__name', 'position']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PlayerListSerializer
        return PlayerSerializer
    
    def get_queryset(self):
        queryset = Player.objects.all()
        
        # Check if pagination should be disabled
        if self.request.query_params.get('limit') == '1000':
            self.pagination_class = None
        
        # Filter by position if provided
        position = self.request.query_params.get('position', None)
        if position:
            queryset = queryset.filter(position__icontains=position)
        
        # Filter by team if provided
        team = self.request.query_params.get('team', None)
        if team:
            queryset = queryset.filter(team=team)
        
        return queryset
    
    @action(detail=False, methods=['post'])
    def refresh_players(self, request):
        """Refresh player data from NBA API"""
        try:
            # This is a placeholder - in a real app, you would use nba_api to fetch player data
            # For demo purposes, we'll create some sample players
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
                
                player, created = Player.objects.update_or_create(
                    player_id=player_data["player_id"],
                    defaults={**player_data, "team": team}
                )
            
            return Response({"message": "Players refreshed successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def top_players(self, request):
        """Get top players by points, rebounds, or assists"""
        stat = request.query_params.get('stat', 'points_per_game')
        limit = int(request.query_params.get('limit', 10))
        
        valid_stats = ['points_per_game', 'rebounds_per_game', 'assists_per_game', 
                       'steals_per_game', 'blocks_per_game', 'field_goal_percentage',
                       'three_point_percentage', 'player_efficiency_rating']
        
        if stat not in valid_stats:
            return Response({"error": f"Invalid stat. Choose from {', '.join(valid_stats)}"},
                           status=status.HTTP_400_BAD_REQUEST)
        
        players = Player.objects.order_by(f'-{stat}')[:limit]
        
        # Fix the data on the fly
        for player in players:
            # Set default position if empty
            if not player.position or player.position == '':
                player.position = 'G-F'  # Default position
            
            # Convert total stats to per-game stats if they seem too high
            if player.points_per_game > 100:  # Clearly not per-game
                player.points_per_game /= 82  # Approximate games in a season
            if player.rebounds_per_game > 50:
                player.rebounds_per_game /= 82
            if player.assists_per_game > 50:
                player.assists_per_game /= 82
            
            # Save the changes
            player.save()
        
        serializer = PlayerListSerializer(players, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = super().get_queryset()
        # Ensure all necessary stats are available
        for player in queryset:
            if player.player_efficiency_rating is None:
                player.player_efficiency_rating = 0.0
            if player.usage_rate is None:
                player.usage_rate = 0.0
            if player.true_shooting_percentage is None:
                player.true_shooting_percentage = 0.0
            if player.position is None:
                player.position = 'Unknown'
            if player.height is None:
                player.height = 0
            if player.weight is None:
                player.weight = 0
            if player.team_id is None:
                player.team_id = 0
        return queryset

class LineupViewSet(viewsets.ModelViewSet):
    serializer_class = LineupSerializer
    permission_classes = [AllowAny]  # Allow anonymous users
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Lineup.objects.filter(user=self.request.user)
        return Lineup.objects.none()
    
    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            # For anonymous users, create lineup without user
            serializer.save(user=None)
    
    @action(detail=True, methods=['post'])
    def optimize(self, request, pk=None):
        """Optimize a lineup based on specific criteria"""
        lineup = self.get_object()
        optimization_type = request.data.get('optimization_type', 'balanced')
        
        # Get all available players
        all_players = Player.objects.filter(is_active=True)
        
        # Simple optimization logic (this would be more sophisticated in a real app)
        if optimization_type == 'offense':
            # Optimize for offense - get players with highest offensive ratings
            optimized_players = all_players.order_by('-offensive_rating')[:5]
        elif optimization_type == 'defense':
            # Optimize for defense - get players with lowest defensive ratings (lower is better)
            optimized_players = all_players.order_by('defensive_rating')[:5]
        else:  # balanced
            # Optimize for net rating (offensive - defensive)
            optimized_players = all_players.annotate(
                net_rating=F('offensive_rating') - F('defensive_rating')
            ).order_by('-net_rating')[:5]
        
        # Update lineup with optimized players
        lineup.players.clear()
        for player in optimized_players:
            lineup.players.add(player)
        
        lineup.calculate_ratings()
        
        serializer = self.get_serializer(lineup)
        return Response(serializer.data)

class LineupComparisonViewSet(viewsets.ModelViewSet):
    serializer_class = LineupComparisonSerializer
    permission_classes = [AllowAny]  # Allow anonymous users
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return LineupComparison.objects.filter(user=self.request.user)
        return LineupComparison.objects.filter(user=None)
    
    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            # For anonymous users, create comparison without user
            serializer.save(user=None)
