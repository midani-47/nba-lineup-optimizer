import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import plotly.express as px
import plotly.graph_objects as go
# import matplotlib.pyplot as plt is not needed as we're using plotly
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib
import random

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import project modules
from src.data_loader import (
    load_nba_players, 
    load_player_stats, 
    load_team_data,
    load_nba_stats,
    import_real_nba_data,
    enhance_player_dataset
)

# Remove unused visualization imports
# from src.visualization.player_charts import (
#     plot_player_radar_chart, 
#     plot_player_comparison
# )
# from src.visualization.team_charts import (
#     plot_team_performance
# )

# Keep only the modules we're using
from src.optimizer.lineup_optimizer import (
    optimize_lineup_for_scoring,
    optimize_lineup_for_defense,
    optimize_lineup_for_balanced,
    calculate_lineup_chemistry,
    check_lineup_balance
)
from src.ml.lineup_prediction import LineupPredictor, train_lineup_prediction_model

# Set page configuration
st.set_page_config(
    page_title="NBA Lineup Optimizer",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App title and description
st.title("NBA Lineup Optimizer")
st.markdown(
    """
    This application showcases data science and machine learning techniques with NBA data.
    Create optimized lineups and predict performance using statistical analysis.
    """
)

# Initialize session state for user selections
if 'selected_players' not in st.session_state:
    st.session_state.selected_players = []
if 'custom_lineups' not in st.session_state:
    st.session_state.custom_lineups = {}
if 'current_lineup_name' not in st.session_state:
    st.session_state.current_lineup_name = "My Lineup"
if 'model_trained' not in st.session_state:
    st.session_state.model_trained = False

# Load data
@st.cache_data
def load_data():
    players = load_nba_players()
    stats = load_player_stats()
    teams = load_team_data()
    return players, stats, teams

players, stats, teams = load_data()

# Create example lineups if none exist
if not st.session_state.custom_lineups:
    # Define specific player groups for example lineups
    allstars = [
        "Stephen Curry",
        "Luka Doncic",
        "Giannis Antetokounmpo",
        "Jayson Tatum",
        "Nikola Jokic"
    ]
    
    ogs = [
        "LeBron James",
        "Kevin Durant",
        "Chris Paul",
        "Klay Thompson",
        "Draymond Green"
    ]
    
    # Create the All-Stars lineup
    allstar_ids = []
    for player_name in allstars:
        player_matches = players[players['name'].str.contains(player_name, case=False, na=False)]
        if not player_matches.empty:
            allstar_ids.append(player_matches.iloc[0]['player_id'])
    
    if len(allstar_ids) >= 5:
        st.session_state.custom_lineups["All-Stars Lineup"] = allstar_ids[:5]
    
    # Create the OGs lineup
    og_ids = []
    for player_name in ogs:
        player_matches = players[players['name'].str.contains(player_name, case=False, na=False)]
        if not player_matches.empty:
            og_ids.append(player_matches.iloc[0]['player_id'])
    
    if len(og_ids) >= 5:
        st.session_state.custom_lineups["OGs Lineup"] = og_ids[:5]
        
    # If we couldn't find enough players for either lineup, create backup examples
    if len(st.session_state.custom_lineups) == 0:
        # Get some star players for example lineups as a fallback
        stars = players.iloc[:10]  # Just take the first 10 players as a backup
        
        if len(stars) >= 5:
            example_lineup1 = stars.iloc[0:5]['player_id'].tolist()
            st.session_state.custom_lineups["All-Star Lineup"] = example_lineup1
            
            # Create a second lineup with different players
            remaining_players = players.iloc[10:20]  # Take the next set of players
            if len(remaining_players) >= 5:
                example_lineup2 = remaining_players.iloc[0:5]['player_id'].tolist()
                st.session_state.custom_lineups["OGs Lineup"] = example_lineup2

# Sidebar navigation
st.sidebar.title("NBA Lineup Optimizer")
st.sidebar.image("https://cdn.nba.com/logos/nba/nba-logoman-75-word_white.svg", width=200)
st.sidebar.markdown("---")

# Navigation with icons and descriptions
st.sidebar.header("Navigation")

page = st.sidebar.radio(
    "Select a page",
    options=["ML Prediction", "Player Explorer", "Lineup Builder", "Lineup Optimizer"],
    format_func=lambda x: {
        "ML Prediction": "⚙️ ML Prediction",
        "Player Explorer": "👤 Player Explorer",
        "Lineup Builder": "🏀 Lineup Builder",
        "Lineup Optimizer": "📊 Lineup Optimizer"
    }[x]
)

# Add page descriptions
if page == "Player Explorer":
    st.sidebar.info("Browse NBA players, view their statistics, and add them to your lineup.")
elif page == "Lineup Builder":
    st.sidebar.info("Review your current lineup, analyze team composition, and view aggregate statistics.")
elif page == "Lineup Optimizer":
    st.sidebar.info("Optimize your lineup using different strategies focusing on scoring, defense, or a balanced approach.")
elif page == "ML Prediction":
    st.sidebar.info("Train machine learning models and predict performance of your lineups with Random Forest algorithms.")

# Selected players section in sidebar
if st.session_state.selected_players:
    st.sidebar.markdown("---")
    st.sidebar.subheader("Current Lineup")
    for i, player_id in enumerate(st.session_state.selected_players[:5]):
        try:
            player = players[players['player_id'] == player_id].iloc[0]
            st.sidebar.text(f"{i+1}. {player['name']} ({player['position']})")
        except:
            st.sidebar.text(f"{i+1}. Player ID: {player_id}")

# Add footer
st.sidebar.markdown("---")
st.sidebar.caption("Made with ❤️ for Data Science")
st.sidebar.caption("© 2025 NBA Lineup Optimizer")

# Utility function to get player stats by ID
def get_player_by_id(player_id):
    return players[players['player_id'] == player_id].iloc[0]

def get_player_stats_by_id(player_id):
    return stats[stats['player_id'] == player_id].iloc[0]

# Page: Player Explorer
if page == "Player Explorer":
    st.header("🔍 NBA Player Explorer")
    st.markdown("""
    <div style='background-color:#f0f2f6;padding:1rem;border-radius:0.5rem;margin-bottom:1rem;color:#333333;'>
    <h4 style='margin-top:0;color:#1e3a8a;'>How to use this page:</h4>
    <ol>
        <li>Use the filters on the left to narrow down the player pool</li>
        <li>Select a player to view detailed statistics and performance metrics</li>
        <li>Click "Add to Lineup" to include players in your custom lineup</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Filter options
        st.markdown("<h3 style='color:#1e3a8a;background-color:#f0f2f6;padding:10px;border-radius:5px;'>Filters</h3>", unsafe_allow_html=True)
        
        # Enhanced team filter with team logo/colors
        teams_list = ["All Teams"] + sorted(players['team'].fillna("Unknown").unique().tolist())
        selected_team = st.selectbox(
            "Team",
            teams_list,
            format_func=lambda x: f"📋 {x}" if x == "All Teams" else f"🏀 {x}"
        )
        
        # Position filter with icon
        positions_list = ["All Positions"] + sorted(players['position'].fillna("Unknown").unique().tolist())
        selected_position = st.selectbox(
            "Position",
            positions_list,
            format_func=lambda x: f"📋 {x}" if x == "All Positions" else f"👤 {x}"
        )
        
        # Enhanced search with placeholder and clear button
        search_placeholder = "Enter player name (e.g., LeBron, Curry)"
        search_name = st.text_input("Search Player", placeholder=search_placeholder)
        
        # Clear filters button
        if st.button("Clear Filters 🔄"):
            # We can't directly modify the selectbox values, but we'll reset the filters
            # on the next refresh using session_state
            st.session_state.clear_filters = True
        
        # Apply filters
        filtered_players = players.copy()
        if selected_team != "All Teams":
            filtered_players = filtered_players[filtered_players['team'] == selected_team]
        if selected_position != "All Positions":
            filtered_players = filtered_players[filtered_players['position'] == selected_position]
        if search_name:
            filtered_players = filtered_players[filtered_players['name'].str.contains(search_name, case=False)]
            
        # Put Stephen Curry at the top of the list if he's in the results
        if not filtered_players.empty:
            curry_players = filtered_players[filtered_players['name'].str.contains('Stephen Curry|Steph Curry', case=False)]
            if not curry_players.empty:
                curry_player = curry_players.iloc[0]
                # Remove curry from filtered_players
                filtered_players = filtered_players[~filtered_players['player_id'].isin(curry_players['player_id'])]
                # Add curry back at the top
                filtered_players = pd.concat([pd.DataFrame([curry_player]), filtered_players], ignore_index=True)
        
        # Player selection with improved UI
        st.markdown("<h3 style='color:#1e3a8a;background-color:#f0f2f6;padding:10px;border-radius:5px;'>Player Selection</h3>", unsafe_allow_html=True)
        if not filtered_players.empty:
            # Show count of filtered players
            st.info(f"Found {len(filtered_players)} players matching your filters")
            
            # Create a more user-friendly player selection interface with pagination
            if 'current_page' not in st.session_state:
                st.session_state.current_page = 0
                
            players_per_page = 10
            page_count = (len(filtered_players) + players_per_page - 1) // players_per_page
            
            # Page navigation
            col_prev, col_page, col_next = st.columns([1, 3, 1])
            with col_prev:
                if st.button("◀ Prev") and st.session_state.current_page > 0:
                    st.session_state.current_page -= 1
            
            with col_page:
                page_options = [f"Page {i+1} of {page_count}" for i in range(page_count)]
                if page_options:
                    page_selection = st.selectbox(
                        "Page", 
                        options=range(page_count),
                        format_func=lambda x: page_options[x],
                        index=min(st.session_state.current_page, page_count-1) if page_count > 0 else 0
                    )
                    st.session_state.current_page = page_selection
            
            with col_next:
                if st.button("Next ▶") and st.session_state.current_page < page_count - 1:
                    st.session_state.current_page += 1
            
            # Get players for current page
            start_idx = st.session_state.current_page * players_per_page
            end_idx = min(start_idx + players_per_page, len(filtered_players))
            current_page_players = filtered_players.iloc[start_idx:end_idx]
            
            # Display players with improved styling and indication if they're already in the lineup
            for _, player in current_page_players.iterrows():
                is_in_lineup = player['player_id'] in st.session_state.selected_players
                
                col_player, col_buttons = st.columns([3, 1])
                
                with col_player:
                    player_name = player['name']
                    player_position = player['position'] if 'position' in player else 'Unknown'
                    player_team = player['team'] if 'team' in player else 'Unknown'
                    
                    if is_in_lineup:
                        st.markdown(f"""
                        <div style='background-color:#e6f7e6;padding:0.5rem;border-radius:0.3rem;border-left:4px solid #28a745;'>
                            <strong>{player_name}</strong> ({player_position}, {player_team})
                            <span style='color:#28a745;'>✓ In Lineup</span>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style='padding:0.5rem;border-radius:0.3rem;'>
                            <strong>{player_name}</strong> ({player_position}, {player_team})
                        </div>
                        """, unsafe_allow_html=True)
                
                with col_buttons:
                    if is_in_lineup:
                        if st.button("Remove", key=f"remove_{player['player_id']}"):
                            st.session_state.selected_players.remove(player['player_id'])
                            st.success(f"Removed {player_name} from lineup")
                            st.rerun()
                    else:
                        if len(st.session_state.selected_players) < 5:
                            if st.button("Add", key=f"add_{player['player_id']}"):
                                st.session_state.selected_players.append(player['player_id'])
                                st.success(f"Added {player_name} to lineup")
                                st.rerun()
                        else:
                            st.warning("Lineup full")
                            
                st.markdown("---")
                
            # Show selected player details
            if 'selected_player_id' in st.session_state and st.session_state.selected_player_id:
                st.subheader("Selected Player Details")
                player_data = players[players['player_id'] == st.session_state.selected_player_id].iloc[0]
                st.write(f"**Name:** {player_data['name']}")
                st.write(f"**Team:** {player_data['team']}")
                st.write(f"**Position:** {player_data['position']}")
                
        else:
            st.warning("No players found with the selected filters.")
            st.markdown("""
            <div style='background-color:#ffe7ba;padding:1rem;border-radius:0.5rem;margin-bottom:1rem;color:#7b341e;'>
            Try adjusting your filters to find players:
            <ul>
                <li>Select "All Teams" to see all teams</li>
                <li>Select "All Positions" to see all positions</li>
                <li>Clear your search term if it's too specific</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if 'player_id' in filtered_players.columns:
            # Current lineup preview at the top
            if st.session_state.selected_players:
                st.subheader("Current Lineup")
                lineup_players = []
                for player_id in st.session_state.selected_players[:5]:
                    player_info = players[players['player_id'] == player_id]
                    if not player_info.empty:
                        lineup_players.append(player_info.iloc[0])
                
                if lineup_players:
                    lineup_df = pd.DataFrame(lineup_players)
                    lineup_display = lineup_df[['name', 'position', 'team']]
                    st.dataframe(lineup_display, use_container_width=True)
                    
                    # Clear lineup button
                    if st.button("Clear Lineup", key="clear_lineup_explorer"):
                        st.session_state.selected_players = []
                        st.rerun()
            
            # Player selection from the list
            if 'filtered_players' in locals() and not filtered_players.empty:
                st.subheader("Select a Player for Detailed Analysis")
                
                # Use a selectbox for quick player selection
                selected_player_name = st.selectbox(
                    "Choose a player to view stats",
                    filtered_players['name'].tolist(),
                    format_func=lambda x: f"🏀 {x}"
                )
                
                if selected_player_name:
                    # Store selected player ID
                    player_id = filtered_players[filtered_players['name'] == selected_player_name]['player_id'].iloc[0]
                    st.session_state.selected_player_id = player_id
                    
                    # Player details
                    player_data = filtered_players[filtered_players['player_id'] == player_id].iloc[0]
                    player_stats = stats[stats['player_id'] == str(player_id)] if 'player_id' in stats.columns else pd.DataFrame()
                    
                    st.subheader(f"Player Analysis: {selected_player_name}")
                    
                    # Player Bio
                    col_bio1, col_bio2 = st.columns(2)
                    with col_bio1:
                        st.write(f"**Team:** {player_data['team'] if 'team' in player_data else 'Unknown'}")
                        st.write(f"**Position:** {player_data['position'] if 'position' in player_data else 'Unknown'}")
                    with col_bio2:
                        st.write(f"**Height:** {player_data['height'] if 'height' in player_data else 'Unknown'}")
                        st.write(f"**Weight:** {player_data['weight'] if 'weight' in player_data else 'Unknown'} kg")
                    
                    # Add/Remove from lineup button
                    if player_id in st.session_state.selected_players:
                        if st.button("⛔ Remove from Lineup", type="primary", key=f"detail_remove_{player_id}"):
                            st.session_state.selected_players.remove(player_id)
                            st.success(f"Removed {selected_player_name} from lineup")
                            st.rerun()
                    else:
                        if len(st.session_state.selected_players) < 5:
                            if st.button("✅ Add to Lineup", type="primary", key=f"detail_add_{player_id}"):
                                st.session_state.selected_players.append(player_id)
                                st.success(f"Added {selected_player_name} to lineup")
                                st.rerun()
                        else:
                            st.error("Your lineup already has 5 players. Remove a player first.")
                    
                    # Player Stats Visualization
                    if not player_stats.empty:
                        # Radar Chart
                        st.subheader("Player Performance Radar")
                        
                        # Calculate key metrics
                        key_stats = ['pts', 'reb', 'ast', 'stl', 'blk']
                        stat_values = []
                        
                        for stat in key_stats:
                            if stat in player_stats.columns:
                                stat_values.append(player_stats[stat].mean(numeric_only=True))
                            else:
                                stat_values.append(0)
                        
                        # Create radar chart with fixed max range based on league averages
                        # This ensures the chart scale stays consistent between players
                        stat_max_values = {
                            'pts': 30,  # Max points per game
                            'reb': 15,  # Max rebounds per game
                            'ast': 12,  # Max assists per game
                            'stl': 4,   # Max steals per game
                            'blk': 4    # Max blocks per game
                        }
                        
                        fig = go.Figure()
                        
                        fig.add_trace(go.Scatterpolar(
                            r=stat_values,
                            theta=key_stats,
                            fill='toself',
                            name=selected_player_name,
                            fillcolor='rgba(0, 123, 255, 0.3)',
                            line=dict(color='rgb(0, 123, 255)')
                        ))
                        
                        # Set a fixed range for better comparison between players
                        fig.update_layout(
                            polar=dict(
                                radialaxis=dict(
                                    visible=True,
                                    range=[0, max([stat_max_values[stat] for stat in key_stats])],
                                    showticklabels=True
                                )
                            ),
                            showlegend=True,
                            title="Player Stats Compared to League Maximums"
                        )
                        
                        st.plotly_chart(fig)
                        
                        # Shooting percentages
                        st.subheader("Shooting Percentages")
                        
                        shooting_stats = ['fg_pct', 'fg3_pct', 'ft_pct']
                        shooting_labels = ['Field Goal %', '3-Point %', 'Free Throw %']
                        shooting_values = []
                        
                        for stat in shooting_stats:
                            if stat in player_stats.columns:
                                shooting_values.append(player_stats[stat].mean() * 100)  # Convert to percentage
                            else:
                                shooting_values.append(0)
                        
                        fig = px.bar(
                            x=shooting_labels,
                            y=shooting_values,
                            labels={'x': 'Shot Type', 'y': 'Percentage (%)'}
                        )
                        
                        st.plotly_chart(fig)
                    else:
                        st.warning("No statistics available for this player.")

# Page: Lineup Builder
elif page == "Lineup Builder":
    st.header("🏀 Lineup Builder")
    st.markdown("""
    <div style='background-color:#f0f2f6;padding:1rem;border-radius:0.5rem;margin-bottom:1rem;color:#333333;'>
    <h4 style='margin-top:0;color:#1e3a8a;'>How to use this page:</h4>
    <ol>
        <li>Select players to add to your custom lineup</li>
        <li>View the combined stats of your selected players</li>
        <li>Compare different lineup combinations</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state for lineup and selected position
    if 'lineup' not in st.session_state:
        st.session_state.lineup = []
    if 'selected_position' not in st.session_state:
        st.session_state.selected_position = "All Positions"
    
    # Load player data
    try:
        players_df = load_nba_players()
        player_stats = load_player_stats()
        
        # Deduplicate player data based on player_id
        players_df = players_df.drop_duplicates(subset=['player_id'])
        
        # Join with player stats for displaying
        if 'player_id' in player_stats.columns:
            player_stats = player_stats.groupby('player_id').mean(numeric_only=True).reset_index()
            avg_player_stats = pd.merge(players_df, player_stats, on='player_id', how='left')
        else:
            avg_player_stats = players_df.copy()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()
    
    # Create columns for page layout
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("Available Players")
        
        # Create filters for selecting players
        position_options = ["All Positions"] + sorted(players_df["position"].unique().tolist())
        selected_position = st.selectbox("Filter by Position", position_options, key="position_filter")
        
        # Player search with autocomplete
        player_search = st.text_input("Search Players", key="player_search")
        
        # Filter players based on position and search term
        filtered_players = players_df.copy()
        
        # Apply position filter
        if selected_position != "All Positions":
            filtered_players = filtered_players[filtered_players["position"] == selected_position]
        
        # Apply search filter
        if player_search:
            filtered_players = filtered_players[
                filtered_players["name"].str.contains(player_search, case=False, na=False)
            ]
        
        # Pagination for player list
        players_per_page = 10
        total_pages = max(1, len(filtered_players) // players_per_page + (1 if len(filtered_players) % players_per_page > 0 else 0))
        
        col_page, col_nav = st.columns([3, 1])
        with col_page:
            page_num = st.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1)
        
        start_idx = (page_num - 1) * players_per_page
        end_idx = min(start_idx + players_per_page, len(filtered_players))
        
        current_page_players = filtered_players.iloc[start_idx:end_idx]
        
        # Show player selection with proper styling
        for _, player in current_page_players.iterrows():
            col_info, col_add = st.columns([4, 1])
            
            with col_info:
                st.markdown(f"""
                <div style='padding:0.5rem;border-radius:0.3rem;background-color:#f8f9fa;'>
                    <strong>{player['name']}</strong><br>
                    <small>{player['position']} | {player['team'] if 'team' in player else 'Team N/A'}</small>
                </div>
                """, unsafe_allow_html=True)
            
            with col_add:
                # Check if player is already in lineup
                is_in_lineup = False
                for lineup_player in st.session_state.lineup:
                    if lineup_player.get('player_id') == player['player_id']:
                        is_in_lineup = True
                        break
                
                if not is_in_lineup and len(st.session_state.lineup) < 5:
                    if st.button("Add", key=f"add_{player['player_id']}"):
                        player_stats_row = player_stats[player_stats['player_id'] == player['player_id']]
                        
                        # Create player object with stats
                        player_with_stats = player.copy()
                        if not player_stats_row.empty:
                            for stat in ['pts', 'reb', 'ast', 'stl', 'blk']:
                                if stat in player_stats_row.columns:
                                    player_with_stats[stat] = player_stats_row[stat].iloc[0]
                        
                        st.session_state.lineup.append(player_with_stats.to_dict())
                        st.rerun()
                elif is_in_lineup:
                    st.markdown("<span style='color:green'>✓ In lineup</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<span style='color:gray'>Lineup full</span>", unsafe_allow_html=True)
    
    with col2:
        st.subheader("Your Lineup")
        
        if st.session_state.lineup:
            # Display current lineup
            for i, player in enumerate(st.session_state.lineup):
                col_player, col_remove = st.columns([3, 1])
                
                with col_player:
                    st.markdown(f"""
                    <div style='padding:0.5rem;background-color:#e6f3ff;border-radius:0.3rem;margin-bottom:0.5rem;'>
                        <strong>{i+1}. {player.get('name', 'Unknown')}</strong><br>
                        <small>{player.get('position', 'N/A')}</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_remove:
                    if st.button("Remove", key=f"remove_{i+1}"):  # Changed from i to i+1
                        st.session_state.lineup.pop(i)
                        st.rerun()
            
            # Calculate lineup statistics if we have stats
            if 'pts' in player_stats.columns:
                st.subheader("Lineup Statistics")
                
                # Extract stats for visualization
                lineup_stats = []
                for player in st.session_state.lineup:
                    player_id = player.get('player_id')
                    if player_id:
                        player_stats_row = player_stats[player_stats['player_id'] == player_id]
                        if not player_stats_row.empty:
                            player_name = player.get('name', 'Unknown')
                            lineup_stats.append({
                                'Player': player_name,
                                'PTS': player_stats_row['pts'].iloc[0] if 'pts' in player_stats_row else 0,
                                'REB': player_stats_row['reb'].iloc[0] if 'reb' in player_stats_row else 0,
                                'AST': player_stats_row['ast'].iloc[0] if 'ast' in player_stats_row else 0,
                                'STL': player_stats_row['stl'].iloc[0] if 'stl' in player_stats_row else 0,
                                'BLK': player_stats_row['blk'].iloc[0] if 'blk' in player_stats_row else 0
                            })
                
                if lineup_stats:
                    # Create DataFrame for display
                    lineup_df = pd.DataFrame(lineup_stats)
                    
                    # Calculate totals and averages
                    totals = lineup_df.drop('Player', axis=1).sum()
                    averages = lineup_df.drop('Player', axis=1).mean()
                    
                    # Display totals and averages
                    col_totals, col_avgs = st.columns(2)
                    
                    with col_totals:
                        st.markdown("**Lineup Totals**")
                        for stat, value in totals.items():
                            st.markdown(f"**{stat}:** {value:.1f}")
                    
                    with col_avgs:
                        st.markdown("**Lineup Averages**")
                        for stat, value in averages.items():
                            st.markdown(f"**{stat}:** {value:.1f}")
                    
                    # Visualization of stats distribution
                    st.subheader("Stats Distribution")
                    
                    # Reshape data for plotting with Plotly
                    plot_data = []
                    for _, row in lineup_df.iterrows():
                        for stat in ['PTS', 'REB', 'AST', 'STL', 'BLK']:
                            plot_data.append({
                                'Player': row['Player'],
                                'Stat': stat,
                                'Value': row[stat]
                            })
                    
                    plot_df = pd.DataFrame(plot_data)
                    
                    # Create grouped bar chart
                    fig = px.bar(
                        plot_df,
                        x='Player',
                        y='Value',
                        color='Stat',
                        barmode='group',
                        title='Player Stats Comparison',
                        labels={'Value': 'Statistic Value', 'Player': 'Player Name'},
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Save lineup button
                    lineup_name = st.text_input("Lineup Name", value="My Custom Lineup")
                    
                    if st.button("Save Lineup"):
                        # Save to session state
                        player_ids = [player.get('player_id') for player in st.session_state.lineup if player.get('player_id')]
                        if len(player_ids) == 5:
                            st.session_state.custom_lineups[lineup_name] = player_ids
                            st.success(f"Lineup '{lineup_name}' saved successfully!")
                        else:
                            st.warning("Please add 5 players to save a complete lineup.")
                
            else:
                st.info("No statistical data available for visualization.")
        else:
            st.info("Your lineup is empty. Add players from the list on the left.")
            st.markdown("""
            <div style='background-color:#f0f2f6;padding:1rem;border-radius:0.5rem;margin-top:1rem;color:#333333;'>
            <strong>Tips for building a lineup:</strong>
            <ul>
                <li>Add a mix of players from different positions for balance</li>
                <li>Consider combining high-scoring players with defensive specialists</li>
                <li>Look for players with complementary skills</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

# Page: Lineup Optimizer
elif page == "Lineup Optimizer":
    st.header("📊 Lineup Optimizer")
    st.markdown("""
    <div style='background-color:#f0f2f6;padding:1rem;border-radius:0.5rem;margin-bottom:1rem;color:#333333;'>
    <h4 style='margin-top:0;color:#1e3a8a;'>How to use this page:</h4>
    <ol>
        <li>Select a lineup from your saved lineups</li>
        <li>Choose an optimization strategy (scoring, defense, or balanced)</li>
        <li>Review the optimized lineup and performance comparison</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if we have any lineups to optimize
    if not st.session_state.custom_lineups:
        st.warning("You don't have any saved lineups. Please build and save a lineup first.")
        st.stop()
    
    # Select a lineup
    lineup_names = list(st.session_state.custom_lineups.keys())
    selected_lineup = st.selectbox("Select Lineup to Optimize", lineup_names)
    
    # Get the selected lineup's player IDs
    player_ids = st.session_state.custom_lineups[selected_lineup]
    
    # Ensure we have 5 players in the lineup
    if len(player_ids) != 5:
        st.warning(f"The selected lineup has {len(player_ids)} players, but we need exactly 5 for optimization.")
        st.stop()
    
    # Load player data if not already loaded
    try:
        players_df = load_nba_players()
        player_stats = load_player_stats()
        
        # Get the stats for the selected players
        lineup_players = []
        lineup_player_stats = []
        
        for player_id in player_ids:
            player_info = players_df[players_df['player_id'] == player_id]
            player_stat = player_stats[player_stats['player_id'] == player_id]
            
            if not player_info.empty and not player_stat.empty:
                lineup_players.append(player_info.iloc[0])
                lineup_player_stats.append(player_stat.iloc[0])
        
        # Create DataFrames
        lineup_df = pd.DataFrame(lineup_players)
        stats_df = pd.DataFrame(lineup_player_stats)
        
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()
    
    # Show the current lineup
    st.subheader("Current Lineup")
    
    # Display players in a table
    if not lineup_df.empty:
        # Join with stats for display
        display_df = pd.merge(
            lineup_df[['player_id', 'name', 'position']],
            stats_df[['player_id', 'pts', 'reb', 'ast', 'stl', 'blk']],
            on='player_id'
        )
        
        st.dataframe(display_df[['name', 'position', 'pts', 'reb', 'ast', 'stl', 'blk']])
    else:
        st.warning("Could not find all players in the lineup.")
        st.stop()
    
    # Select optimization strategy
    st.subheader("Optimization Strategy")
    
    optimization_strategy = st.radio(
        "Select Strategy",
        ["Scoring Focused", "Defense Focused", "Balanced Approach"],
        horizontal=True
    )
    
    # Optimize button
    if st.button("Optimize Lineup"):
        with st.spinner("Optimizing lineup..."):
            try:
                # Get the proper optimization function based on strategy
                if optimization_strategy == "Scoring Focused":
                    optimize_func = optimize_lineup_for_scoring
                elif optimization_strategy == "Defense Focused":
                    optimize_func = optimize_lineup_for_defense
                else:
                    optimize_func = optimize_lineup_for_balanced
                
                # Optimize the lineup
                optimized_player_ids = optimize_func(player_ids, player_stats, players_df)
                
                # Get the stats for the optimized players
                optimized_players = []
                optimized_player_stats = []
                
                for player_id in optimized_player_ids:
                    player_info = players_df[players_df['player_id'] == player_id]
                    player_stat = player_stats[player_stats['player_id'] == player_id]
                    
                    if not player_info.empty and not player_stat.empty:
                        optimized_players.append(player_info.iloc[0])
                        optimized_player_stats.append(player_stat.iloc[0])
                
                # Create DataFrames
                optimized_df = pd.DataFrame(optimized_players)
                optimized_stats_df = pd.DataFrame(optimized_player_stats)
                
                # Show the optimized lineup
                st.subheader("Optimized Lineup")
                
                # Display optimized players in a table
                if not optimized_df.empty:
                    # Join with stats for display
                    optimized_display_df = pd.merge(
                        optimized_df[['player_id', 'name', 'position']],
                        optimized_stats_df[['player_id', 'pts', 'reb', 'ast', 'stl', 'blk']],
                        on='player_id'
                    )
                    
                    st.dataframe(optimized_display_df[['name', 'position', 'pts', 'reb', 'ast', 'stl', 'blk']])
                    
                    # Analyze differences
                    original_totals = stats_df[['pts', 'reb', 'ast', 'stl', 'blk']].sum()
                    optimized_totals = optimized_stats_df[['pts', 'reb', 'ast', 'stl', 'blk']].sum()
                    
                    # Compare lineups
                    st.subheader("Lineup Comparison")
                    
                    # Create comparison data
                    key_metrics = ['pts', 'reb', 'ast', 'stl', 'blk']
                    key_metric_names = ['Points', 'Rebounds', 'Assists', 'Steals', 'Blocks']
                    
                    original_values = [original_totals[metric] for metric in key_metrics]
                    optimized_values = [optimized_totals[metric] for metric in key_metrics]
                    
                    # Calculate improvement percentages
                    improvements = []
                    for i, metric in enumerate(key_metrics):
                        if original_values[i] > 0:
                            pct_change = ((optimized_values[i] - original_values[i]) / original_values[i]) * 100
                            improvements.append(pct_change)
                        else:
                            improvements.append(0)
                    
                    # Create a bar chart with different colors for original and optimized
                    fig = go.Figure()
                    
                    fig.add_trace(go.Bar(
                        x=key_metric_names,
                        y=original_values,
                        name='Original Lineup',
                        marker_color='rgba(58, 71, 180, 0.8)'  # Darker blue
                    ))
                    
                    fig.add_trace(go.Bar(
                        x=key_metric_names,
                        y=optimized_values,
                        name='Optimized Lineup',
                        marker_color='rgba(246, 78, 139, 0.8)'  # Darker pink
                    ))
                    
                    fig.update_layout(
                        title="Lineup Comparison (Team Totals)",
                        xaxis_title="Metrics",
                        yaxis_title="Value",
                        barmode='group',
                        bargap=0.15,
                        bargroupgap=0.1,
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                        )
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Add explanation text below the chart
                    st.markdown("""
                    **Understanding the Comparison Chart:**
                    
                    This bar chart compares the total statistics between your original lineup and the optimized lineup:
                    - **Blue bars** represent the performance metrics of your original lineup
                    - **Pink bars** represent the performance metrics of the optimized lineup
                    
                    The optimization algorithm prioritizes improvements based on your selected strategy:
                    - **Scoring Focused**: Prioritizes points and shooting efficiency
                    - **Defense Focused**: Prioritizes steals, blocks, and defensive rebounds
                    - **Balanced Approach**: Seeks to optimize across all statistical categories
                    """)
                    
                    # Show improvement percentage for each metric
                    st.subheader("Performance Improvement")
                    improvement_data = []
                    
                    for i, metric in enumerate(key_metrics):
                        improvement_data.append({
                            "Metric": key_metric_names[i], 
                            "Original": original_values[i], 
                            "Optimized": optimized_values[i], 
                            "Change %": improvements[i]
                        })
                    
                    if improvement_data:
                        improvement_df = pd.DataFrame(improvement_data)
                        
                        # Style the dataframe to highlight improvements
                        def highlight_improvements(val):
                            if isinstance(val, float) and 'Change' in improvement_df.columns[improvement_df.eq(val).any()]:
                                if val > 1:
                                    return 'background-color: rgba(0, 200, 0, 0.2)'
                                elif val < -1:
                                    return 'background-color: rgba(200, 0, 0, 0.2)'
                            return ''
                        
                        styled_df = improvement_df.style.format({
                            "Original": "{:.1f}",
                            "Optimized": "{:.1f}",
                            "Change %": "{:+.1f}%"
                        }).applymap(highlight_improvements)
                        
                        st.dataframe(styled_df, use_container_width=True)
                    
                    # Save the optimized lineup
                    if st.button("Save Optimized Lineup"):
                        optimized_name = f"{selected_lineup} (Optimized)"
                        st.session_state.custom_lineups[optimized_name] = optimized_player_ids
                        st.success(f"Optimized lineup saved as '{optimized_name}'")
                else:
                    st.warning("Could not create optimized lineup. Please try again.")
            
            except Exception as e:
                st.error(f"Error during optimization: {e}")

# Page: ML Prediction
elif page == "ML Prediction":
    st.title("ML Prediction ⚙️")
    
    st.markdown("""
    ### Train a machine learning model to predict lineup performance
    
    Select five players from different positions to form your lineup. Then train a model to predict 
    how well they would perform together based on their individual statistics.
    
    The model will predict various metrics and show you which player statistics are most important for performance!
    """)
    
    # Load data with type checking for player_id
    try:
        players_df = load_nba_players()
        player_stats = load_player_stats()
        teams_df = load_team_data()
        
        # Force player_id to be string for consistent comparison
        players_df['player_id'] = players_df['player_id'].astype(str)
        if 'player_id' in player_stats.columns:
            player_stats['player_id'] = player_stats['player_id'].astype(str)
        
        # Debug verification of names
        print("Player names check:")
        for idx, player in players_df.head(5).iterrows():
            print(f"ID: {player['player_id']}, Name: {player['name']}")
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()
    
    # Preprocessing player stats - guarantee consistent player names
    try:
        # Group stats by player_id and calculate mean for each numeric column
        avg_player_stats = player_stats.groupby('player_id').mean(numeric_only=True).reset_index()
        
        # Make sure we have required columns
        required_columns = ['pts', 'reb', 'ast', 'stl', 'blk', 'fg_pct', 'fg3_pct', 'ft_pct']
        for col in required_columns:
            if col not in avg_player_stats.columns:
                avg_player_stats[col] = 0.0
        
        # Join with player names from the players_df to ensure consistent naming
        avg_player_stats = pd.merge(
            avg_player_stats,
            players_df[['player_id', 'name']],
            on='player_id',
            how='left'
        )
        
        # Add player_name column if not exists
        if 'player_name' not in avg_player_stats.columns:
            avg_player_stats['player_name'] = avg_player_stats['name']
            
        # Log processed data shape
        print(f"Processed avg_player_stats: {avg_player_stats.shape[0]} rows, columns: {avg_player_stats.columns.tolist()}")
    
    except Exception as e:
        st.error(f"Error preprocessing player stats: {e}")
        st.error(f"Columns in player_stats: {player_stats.columns.tolist() if 'player_stats' in locals() else 'No data'}")
        st.error(f"Columns in players_df: {players_df.columns.tolist() if 'players_df' in locals() else 'No data'}")
        # Create a minimal fallback dataset
        avg_player_stats = pd.DataFrame({
            'player_id': players_df['player_id'],
            'name': players_df['name'],
            'player_name': players_df['name'],
            'pts': np.random.uniform(10, 25, len(players_df)),
            'reb': np.random.uniform(3, 10, len(players_df)),
            'ast': np.random.uniform(2, 8, len(players_df)),
            'stl': np.random.uniform(0.5, 2, len(players_df)),
            'blk': np.random.uniform(0.2, 1.5, len(players_df)),
            'fg_pct': np.random.uniform(0.4, 0.55, len(players_df)),
            'fg3_pct': np.random.uniform(0.3, 0.45, len(players_df)),
            'ft_pct': np.random.uniform(0.7, 0.9, len(players_df))
        })
    
    # Add built-in lineup selector for ML page
    st.subheader("Pre-made Lineups")
    builtin_lineups = list(st.session_state.custom_lineups.keys())
    if builtin_lineups:
        selected_lineup = st.selectbox(
            "Choose a pre-made lineup:",
            options=["None"] + builtin_lineups,
            index=0,
            key="ml_lineup_selector"
        )
        
        if selected_lineup != "None":
            if st.button("Load Selected Lineup", key="ml_load_lineup"):
                st.session_state.selected_players = st.session_state.custom_lineups[selected_lineup].copy()
                st.session_state.current_lineup_name = selected_lineup
                st.success(f"Loaded {selected_lineup}")
                st.rerun()
    else:
        st.info("No built-in lineups available.")
        
    # Player Selection Section
    st.subheader("Player Selection 🏀")
    
    # Get unique positions
    positions = sorted(players_df['position'].unique())
    
    # Create columns for position selection
    cols = st.columns(5)
    
    # Initialize selected players list
    selected_players = []
    position_to_col = {pos: i for i, pos in enumerate(positions[:5])}
    
    # Allow user to select one player from each position
    for i, pos in enumerate(positions[:5]):
        with cols[i]:
            st.markdown(f"**{pos}**")
            players_in_pos = players_df[players_df['position'] == pos]
            if not players_in_pos.empty:
                selected_player = st.selectbox(
                    f"Select {pos}",
                    options=players_in_pos['player_id'].tolist(),
                    format_func=lambda x: players_df[players_df['player_id'] == x]['name'].iloc[0] if not players_df[players_df['player_id'] == x].empty else f"Unknown Player ({x})",
                    key=f"pos_{pos}"
                )
                if selected_player:
                    selected_players.append(selected_player)
            else:
                st.warning(f"No players available for position {pos}")
    
    # Display selected lineup
    if len(selected_players) > 0:
        st.subheader("Your Lineup 👥")
        
        # Get stats for selected players - using direct player lookup rather than merging
        lineup_display = []
        
        for player_id in selected_players:
            # Get player info
            player_info = players_df[players_df['player_id'] == player_id]
            if player_info.empty:
                continue
                
            # Get player stats
            player_stats_row = avg_player_stats[avg_player_stats['player_id'] == player_id]
            
            # Create row for display
            player_row = {
                'player_id': player_id,
                'name': player_info['name'].iloc[0],
                'position': player_info['position'].iloc[0],
                'pts': player_stats_row['pts'].iloc[0] if not player_stats_row.empty and 'pts' in player_stats_row else 0,
                'reb': player_stats_row['reb'].iloc[0] if not player_stats_row.empty and 'reb' in player_stats_row else 0,
                'ast': player_stats_row['ast'].iloc[0] if not player_stats_row.empty and 'ast' in player_stats_row else 0,
                'stl': player_stats_row['stl'].iloc[0] if not player_stats_row.empty and 'stl' in player_stats_row else 0,
                'blk': player_stats_row['blk'].iloc[0] if not player_stats_row.empty and 'blk' in player_stats_row else 0
            }
            lineup_display.append(player_row)
        
        # Create a dataframe for display
        display_df = pd.DataFrame(lineup_display)
        
        # Display the lineup in a table
        if not display_df.empty:
            st.dataframe(
                display_df[['name', 'position', 'pts', 'reb', 'ast', 'stl', 'blk']].sort_values('position'),
                use_container_width=True
            )
        else:
            st.warning("No stats available for selected players")
            # Fallback display with just names
            lineup_players = players_df[players_df['player_id'].isin(selected_players)]
            st.dataframe(lineup_players[['name', 'position']], use_container_width=True)
        
        if len(selected_players) == 5:
            # Training Section
            st.subheader("Train Your Model ⚙️")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                n_estimators = st.slider("Number of Trees", min_value=10, max_value=200, value=100, step=10)
            
            with col2:
                max_depth = st.slider("Max Tree Depth", min_value=3, max_value=20, value=10, step=1)
            
            with col3:
                target_metric = st.selectbox(
                    "Predict Metric",
                    options=["pts", "reb", "ast", "stl", "blk"],
                    format_func=lambda x: {
                        "pts": "Points",
                        "reb": "Rebounds",
                        "ast": "Assists",
                        "stl": "Steals", 
                        "blk": "Blocks"
                    }[x]
                )
            
            if st.button("Train Model"):
                with st.spinner("Training model..."):
                    try:
                        # Verify the data has the necessary columns before training
                        if all(col in avg_player_stats.columns for col in required_columns + ['player_id']):
                            # Train model using the function from src.ml.lineup_prediction
                            model, X_test, y_test, top_features, feature_importances, mse, y_pred = train_lineup_prediction_model(
                                avg_player_stats, 
                                target_metric, 
                                n_estimators=n_estimators, 
                                max_depth=max_depth
                            )
                            
                            st.success(f"Model trained successfully! MSE: {mse:.2f}")
                            
                            # Results Section
                            st.subheader("Model Results 📊")
                            
                            # Store feature importance results in session state to ensure persistence
                            st.session_state.top_features = top_features
                            st.session_state.feature_importances = feature_importances
                            
                            # Display feature importance chart using px.bar
                            fig = px.bar(
                                x=feature_importances,
                                y=top_features,
                                orientation='h',
                                labels={'x': 'Importance', 'y': 'Feature'},
                                title=f'Top Features for Predicting {target_metric.upper()}'
                            )
                            
                            # Make plot larger and more readable
                            fig.update_layout(
                                height=400,
                                xaxis_title="Relative Importance",
                                yaxis_title="Feature",
                                margin=dict(l=40, r=40, t=40, b=40),
                                yaxis={'categoryorder':'total ascending'}  # Sort bars
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Explain feature importance
                            st.markdown("""
                            **What this means**: 
                            The chart above shows which statistics most strongly influence player performance in the selected metric. 
                            Longer bars indicate features that have more impact on the prediction.
                            
                            For example, if points (PTS) has a high importance for predicting rebounds, it suggests that 
                            players who score more points also tend to grab more rebounds, possibly because they're more 
                            involved in the game or have more opportunities near the basket.
                            """)
                            
                            # Add Model Performance Visualization
                            st.subheader("Model Performance")
                            
                            # Create a DataFrame for plotting predictions vs actual
                            performance_df = pd.DataFrame({
                                'Predicted': y_pred,
                                'Actual': y_test
                            })
                            
                            # Scatter plot of predicted vs actual
                            perf_fig = px.scatter(
                                performance_df, 
                                x='Actual', 
                                y='Predicted',
                                title=f"Predicted vs Actual {target_metric.upper()}",
                                labels={'Predicted': f'Predicted {target_metric.upper()}', 
                                       'Actual': f'Actual {target_metric.upper()}'}
                            )
                            
                            # Add a perfect prediction line
                            min_val = min(performance_df['Actual'].min(), performance_df['Predicted'].min())
                            max_val = max(performance_df['Actual'].max(), performance_df['Predicted'].max())
                            
                            perf_fig.add_trace(
                                go.Scatter(
                                    x=[min_val, max_val],
                                    y=[min_val, max_val],
                                    mode='lines',
                                    name='Perfect Prediction',
                                    line=dict(color='red', dash='dash')
                                )
                            )
                            
                            st.plotly_chart(perf_fig, use_container_width=True)
                            
                            # Add explanatory text for model performance
                            st.markdown("""
                            **Understanding the Model Performance Plot:**
                            
                            This scatter plot shows how well our model predicts the actual performance:
                            - Each point represents a lineup's predicted vs actual statistic
                            - Points close to the red dashed line indicate accurate predictions
                            - Points above the line mean the model underestimated performance
                            - Points below the line mean the model overestimated performance
                            
                            The tighter the clustering around the line, the more accurate our model is.
                            """)
                        else:
                            missing_cols = [col for col in required_columns + ['player_id'] if col not in avg_player_stats.columns]
                            st.error(f"Missing required columns for training: {missing_cols}")
                            
                    except Exception as e:
                        st.error(f"Error training model: {e}")
                        st.error("Please try again with different parameters or a different target metric.")
        else:
            st.info("Please select 5 players (one from each position) to train the model.")

# Footer
st.markdown("---")
st.markdown("NBA Lineup Optimizer - Demonstrating Data Science & Machine Learning with Sports Analytics") 