#!/usr/bin/env python
"""
Database connectivity check and repair script for NBA Lineup Optimizer
"""

import os
import sys
import django
import time
import json
from django.db import connection
from django.db.utils import OperationalError

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nba_project.settings')
django.setup()

# Import models after Django setup
from api.models import Team, Player, Lineup
from django.contrib.auth.models import User

def check_connection():
    """Check if database connection is working"""
    try:
        connection.ensure_connection()
        print("✅ Database connection successful")
        return True
    except OperationalError as e:
        print(f"❌ Database connection failed: {e}")
        return False

def check_tables():
    """Check if required tables exist and have data"""
    tables = {
        'Teams': Team,
        'Players': Player,
        'Lineups': Lineup,
        'Users': User
    }
    
    all_good = True
    for name, model in tables.items():
        try:
            count = model.objects.count()
            if count > 0:
                print(f"✅ {name} table exists with {count} records")
            else:
                print(f"⚠️ {name} table exists but has no records")
                all_good = False
        except Exception as e:
            print(f"❌ Error accessing {name} table: {e}")
            all_good = False
    
    return all_good

def fix_player_data():
    """Fix common issues with player data"""
    try:
        # Fix missing positions
        players_no_position = Player.objects.filter(position__isnull=True) | Player.objects.filter(position='')
        for player in players_no_position:
            player.position = 'G-F'  # Default position
            player.save()
        
        # Fix missing stats
        players_no_stats = Player.objects.filter(
            points_per_game=0, 
            rebounds_per_game=0, 
            assists_per_game=0
        )
        
        if players_no_stats.exists():
            print(f"⚠️ Found {players_no_stats.count()} players with missing stats")
            # Set some default stats based on position
            for player in players_no_stats:
                if 'G' in player.position:
                    player.points_per_game = 12.5
                    player.rebounds_per_game = 3.2
                    player.assists_per_game = 4.8
                elif 'F' in player.position:
                    player.points_per_game = 11.2
                    player.rebounds_per_game = 5.8
                    player.assists_per_game = 2.1
                elif 'C' in player.position:
                    player.points_per_game = 10.4
                    player.rebounds_per_game = 8.2
                    player.assists_per_game = 1.5
                else:
                    player.points_per_game = 8.5
                    player.rebounds_per_game = 4.0
                    player.assists_per_game = 2.0
                
                player.save()
            
            print(f"✅ Fixed stats for {players_no_stats.count()} players")
        else:
            print("✅ All players have basic stats")
        
        # Fix missing team references
        players_no_team = Player.objects.filter(team__isnull=True)
        if players_no_team.exists():
            print(f"⚠️ Found {players_no_team.count()} players without team references")
            # Try to run the fix_team_references script
            try:
                from fix_team_references import fix_team_references
                fixed = fix_team_references()
                print(f"✅ Fixed team references for {fixed} players")
            except ImportError:
                print("❌ Could not import fix_team_references script")
        else:
            print("✅ All players have team references")
            
        return True
    except Exception as e:
        print(f"❌ Error fixing player data: {e}")
        return False

def create_sample_data():
    """Create sample data if tables are empty"""
    try:
        # Create sample teams if none exist
        if Team.objects.count() == 0:
            print("⚠️ No teams found, creating sample teams...")
            sample_teams = [
                {"team_id": 1610612737, "name": "Hawks", "abbreviation": "ATL", "city": "Atlanta", "conference": "East", "division": "Southeast"},
                {"team_id": 1610612738, "name": "Celtics", "abbreviation": "BOS", "city": "Boston", "conference": "East", "division": "Atlantic"},
                {"team_id": 1610612739, "name": "Cavaliers", "abbreviation": "CLE", "city": "Cleveland", "conference": "East", "division": "Central"},
                {"team_id": 1610612740, "name": "Pelicans", "abbreviation": "NOP", "city": "New Orleans", "conference": "West", "division": "Southwest"},
                {"team_id": 1610612741, "name": "Bulls", "abbreviation": "CHI", "city": "Chicago", "conference": "East", "division": "Central"},
            ]
            
            for team_data in sample_teams:
                Team.objects.create(**team_data)
            
            print(f"✅ Created {len(sample_teams)} sample teams")
        
        # Create sample players if none exist
        if Player.objects.count() == 0:
            print("⚠️ No players found, creating sample players...")
            sample_players = [
                {"player_id": 2544, "first_name": "LeBron", "last_name": "James", "team_id": 1610612747, "position": "F", "points_per_game": 25.7, "rebounds_per_game": 7.3, "assists_per_game": 8.3},
                {"player_id": 201939, "first_name": "Stephen", "last_name": "Curry", "team_id": 1610612744, "position": "G", "points_per_game": 29.4, "rebounds_per_game": 6.1, "assists_per_game": 6.3},
                {"player_id": 203954, "first_name": "Joel", "last_name": "Embiid", "team_id": 1610612755, "position": "C", "points_per_game": 33.1, "rebounds_per_game": 11.3, "assists_per_game": 4.2},
                {"player_id": 203507, "first_name": "Giannis", "last_name": "Antetokounmpo", "team_id": 1610612749, "position": "F", "points_per_game": 30.4, "rebounds_per_game": 11.5, "assists_per_game": 5.7},
                {"player_id": 1629029, "first_name": "Luka", "last_name": "Doncic", "team_id": 1610612742, "position": "G", "points_per_game": 32.4, "rebounds_per_game": 9.2, "assists_per_game": 8.9},
            ]
            
            for player_data in sample_players:
                team_id = player_data.pop("team_id", None)
                team = None
                if team_id:
                    try:
                        team = Team.objects.get(team_id=team_id)
                    except Team.DoesNotExist:
                        pass
                
                Player.objects.create(**player_data, team=team)
            
            print(f"✅ Created {len(sample_players)} sample players")
        
        return True
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        return False

def main():
    """Main function to check and fix database issues"""
    print("\n🏀 NBA Lineup Optimizer - Database Check Tool 🏀")
    print("==============================================\n")
    
    # Step 1: Check database connection
    if not check_connection():
        print("\n❌ Cannot proceed without database connection")
        sys.exit(1)
    
    # Step 2: Check tables
    print("\nChecking database tables...")
    tables_ok = check_tables()
    
    # Step 3: Fix player data
    print("\nChecking player data...")
    player_data_ok = fix_player_data()
    
    # Step 4: Create sample data if needed
    if not tables_ok:
        print("\nCreating sample data...")
        create_sample_data()
    
    # Final status
    print("\n==============================================")
    if tables_ok and player_data_ok:
        print("✅ Database check completed successfully")
    else:
        print("⚠️ Database check completed with warnings")
    print("==============================================\n")

if __name__ == "__main__":
    main() 