import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nba_project.settings')
django.setup()

# Import models
from api.models import Player, Team
from django.db import transaction

def fix_team_references():
    print("Fixing team references...")
    
    # Get all players
    players = Player.objects.all()
    fixed_count = 0
    
    with transaction.atomic():
        for player in players:
            try:
                # Try to access the team to see if it exists
                if player.team:
                    team_name = f"{player.team.city} {player.team.name}"
                    print(f"Player {player.first_name} {player.last_name} has valid team: {team_name}")
            except Exception as e:
                print(f"Player {player.first_name} {player.last_name} has invalid team reference: {e}")
                # Set team to None
                player.team = None
                player.save()
                fixed_count += 1
    
    print(f"Fixed {fixed_count} players with invalid team references")

if __name__ == '__main__':
    fix_team_references() 