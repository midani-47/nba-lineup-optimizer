import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nba_project.settings')
django.setup()

# Import models
from api.models import Lineup

def fix_lineup_recursion():
    """Fix the infinite recursion issue in Lineup model"""
    print("Fixing lineup recursion issue...")
    
    # Get all lineups
    lineups = Lineup.objects.all()
    
    for lineup in lineups:
        try:
            # Get all players in a single query
            players = lineup.players.all()
            
            if not players.exists():
                lineup.offensive_rating = 0
                lineup.defensive_rating = 0
                lineup.net_rating = 0
                # Use skip_ratings=True to avoid recursion
                lineup.save(skip_ratings=True)
                print(f"Fixed empty lineup: {lineup.name}")
                continue
            
            # Calculate offensive rating (weighted average of points and assists)
            total_points = sum(p.points_per_game for p in players)
            total_assists = sum(p.assists_per_game for p in players)
            lineup.offensive_rating = (total_points * 0.7 + total_assists * 0.3) * 2
            
            # Calculate defensive rating (weighted average of rebounds, steals, and blocks)
            total_rebounds = sum(p.rebounds_per_game for p in players)
            total_steals = sum(p.steals_per_game for p in players)
            total_blocks = sum(p.blocks_per_game for p in players)
            lineup.defensive_rating = (
                total_rebounds * 0.5 + 
                total_steals * 0.25 + 
                total_blocks * 0.25
            ) * 2
            
            # Calculate net rating
            lineup.net_rating = lineup.offensive_rating - lineup.defensive_rating
            
            # Ensure ratings are not null
            lineup.offensive_rating = lineup.offensive_rating or 0
            lineup.defensive_rating = lineup.defensive_rating or 0
            lineup.net_rating = lineup.net_rating or 0
            
            # Save with skip_ratings=True to avoid recursion
            lineup.save(skip_ratings=True)
            print(f"Fixed lineup: {lineup.name}")
        except Exception as e:
            print(f"Error fixing lineup {lineup.id}: {str(e)}")

if __name__ == "__main__":
    fix_lineup_recursion()
    print("Lineup recursion fixing complete!") 