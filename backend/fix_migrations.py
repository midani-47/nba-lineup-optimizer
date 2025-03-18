#!/usr/bin/env python
"""
Fix migrations script for NBA Lineup Optimizer

This script addresses common database issues:
1. Fixes the duplicate image_url column issue
2. Updates player image URLs
3. Creates sample data if needed
"""

import os
import django
import sys
import sqlite3
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.db import connection
from api.models import Player, Team, Lineup

def check_column_exists(table, column):
    """Check if a column exists in a table"""
    with connection.cursor() as cursor:
        cursor.execute(f"PRAGMA table_info({table});")
        columns = [column_info[1] for column_info in cursor.fetchall()]
        return column in columns

def fix_image_url_column():
    """Fix the duplicate image_url column issue"""
    logger.info("Checking for image_url column in api_player table...")
    
    if check_column_exists('api_player', 'image_url'):
        logger.info("image_url column already exists. No action needed.")
        return True
    
    logger.info("image_url column doesn't exist. Adding it...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("ALTER TABLE api_player ADD COLUMN image_url VARCHAR(500);")
        logger.info("Successfully added image_url column")
        return True
    except Exception as e:
        logger.error(f"Error adding image_url column: {e}")
        return False

def update_player_images():
    """Update player image URLs"""
    logger.info("Updating player image URLs...")
    
    try:
        players = Player.objects.all()
        updated_count = 0
        
        for player in players:
            if not player.image_url:
                player.image_url = f"https://cdn.nba.com/headshots/nba/latest/1040x760/{player.player_id}.png"
                player.save(update_fields=['image_url'])
                updated_count += 1
        
        logger.info(f"Updated {updated_count} player image URLs")
        return True
    except Exception as e:
        logger.error(f"Error updating player images: {e}")
        return False

def create_sample_data():
    """Create sample data if tables are empty"""
    logger.info("Checking if we need to create sample data...")
    
    # Check for teams
    if Team.objects.count() == 0:
        logger.info("No teams found. Creating sample teams...")
        try:
            sample_teams = [
                {"team_id": 1610612737, "name": "Hawks", "abbreviation": "ATL", "city": "Atlanta", "conference": "East", "division": "Southeast"},
                {"team_id": 1610612738, "name": "Celtics", "abbreviation": "BOS", "city": "Boston", "conference": "East", "division": "Atlantic"},
                {"team_id": 1610612739, "name": "Cavaliers", "abbreviation": "CLE", "city": "Cleveland", "conference": "East", "division": "Central"},
                {"team_id": 1610612740, "name": "Pelicans", "abbreviation": "NOP", "city": "New Orleans", "conference": "West", "division": "Southwest"},
                {"team_id": 1610612741, "name": "Bulls", "abbreviation": "CHI", "city": "Chicago", "conference": "East", "division": "Central"},
            ]
            
            for team_data in sample_teams:
                Team.objects.create(**team_data)
            
            logger.info(f"Created {len(sample_teams)} sample teams")
        except Exception as e:
            logger.error(f"Error creating sample teams: {e}")
    
    # Check for players
    if Player.objects.count() == 0:
        logger.info("No players found. Creating sample players...")
        try:
            teams = Team.objects.all()
            if not teams:
                logger.error("Cannot create players: No teams available")
                return False
            
            sample_players = [
                {"player_id": 2544, "first_name": "LeBron", "last_name": "James", "position": "F", "height": "6-9", "weight": 250, "jersey_number": 23, "points_per_game": 25.7, "rebounds_per_game": 7.3, "assists_per_game": 7.5, "steals_per_game": 1.1, "blocks_per_game": 0.6, "field_goal_percentage": 0.510, "three_point_percentage": 0.365, "free_throw_percentage": 0.730},
                {"player_id": 201939, "first_name": "Stephen", "last_name": "Curry", "position": "G", "height": "6-2", "weight": 185, "jersey_number": 30, "points_per_game": 29.4, "rebounds_per_game": 5.9, "assists_per_game": 6.3, "steals_per_game": 1.3, "blocks_per_game": 0.4, "field_goal_percentage": 0.472, "three_point_percentage": 0.428, "free_throw_percentage": 0.915},
                {"player_id": 203954, "first_name": "Joel", "last_name": "Embiid", "position": "C", "height": "7-0", "weight": 280, "jersey_number": 21, "points_per_game": 33.1, "rebounds_per_game": 10.2, "assists_per_game": 4.2, "steals_per_game": 1.0, "blocks_per_game": 1.7, "field_goal_percentage": 0.546, "three_point_percentage": 0.352, "free_throw_percentage": 0.857},
                {"player_id": 1629029, "first_name": "Luka", "last_name": "Doncic", "position": "G-F", "height": "6-7", "weight": 230, "jersey_number": 77, "points_per_game": 32.4, "rebounds_per_game": 8.6, "assists_per_game": 8.0, "steals_per_game": 1.4, "blocks_per_game": 0.5, "field_goal_percentage": 0.499, "three_point_percentage": 0.382, "free_throw_percentage": 0.741},
                {"player_id": 203507, "first_name": "Giannis", "last_name": "Antetokounmpo", "position": "F", "height": "6-11", "weight": 242, "jersey_number": 34, "points_per_game": 30.1, "rebounds_per_game": 11.3, "assists_per_game": 5.7, "steals_per_game": 0.8, "blocks_per_game": 1.2, "field_goal_percentage": 0.612, "three_point_percentage": 0.274, "free_throw_percentage": 0.649},
            ]
            
            for i, player_data in enumerate(sample_players):
                team = teams[i % len(teams)]
                player_data['team'] = team
                player_data['image_url'] = f"https://cdn.nba.com/headshots/nba/latest/1040x760/{player_data['player_id']}.png"
                Player.objects.create(**player_data)
            
            logger.info(f"Created {len(sample_players)} sample players")
        except Exception as e:
            logger.error(f"Error creating sample players: {e}")
    
    return True

def main():
    """Main function to fix database issues"""
    logger.info("🏀 NBA Lineup Optimizer - Database Fix Tool 🏀")
    logger.info("===========================================")
    
    # Fix image_url column
    fix_image_url_column()
    
    # Update player images
    update_player_images()
    
    # Create sample data if needed
    create_sample_data()
    
    logger.info("===========================================")
    logger.info("✅ Database fix completed")
    logger.info("===========================================")

if __name__ == "__main__":
    main() 