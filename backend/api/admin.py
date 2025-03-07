from django.contrib import admin
from .models import Team, Player, Lineup, LineupComparison

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_id', 'name', 'city', 'abbreviation', 'conference', 'division')
    search_fields = ('name', 'city', 'abbreviation')
    list_filter = ('conference', 'division')

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('player_id', 'first_name', 'last_name', 'team', 'position', 
                   'points_per_game', 'rebounds_per_game', 'assists_per_game')
    search_fields = ('first_name', 'last_name', 'team__name')
    list_filter = ('position', 'team', 'is_active', 'is_injured')

@admin.register(Lineup)
class LineupAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'offensive_rating', 'defensive_rating', 'net_rating', 'created_at')
    search_fields = ('name', 'user__username')
    list_filter = ('created_at',)
    filter_horizontal = ('players',)

@admin.register(LineupComparison)
class LineupComparisonAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'lineup1', 'lineup2', 'points_diff', 'net_rating_diff', 'created_at')
    search_fields = ('name', 'user__username')
    list_filter = ('created_at',)
