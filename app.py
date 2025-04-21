import streamlit as st
import pandas as pd
import os
import sys

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import project modules
from src.data_loader import (
    load_nba_players, 
    load_player_stats, 
    load_team_data
)
from src.visualization.player_charts import (
    plot_player_radar_chart, 
    plot_player_comparison
)
from src.visualization.team_charts import (
    plot_team_performance
)
from src.optimizer.lineup_optimizer import (
    optimize_lineup_for_scoring,
    optimize_lineup_for_defense,
    optimize_lineup_for_balanced
)
from src.models.lineup_predictor import predict_lineup_performance

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
    This application helps you create, analyze, and optimize NBA lineups using 
    statistical analysis and machine learning.
    """
)

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select a page",
    ["Browse Players", "Create Lineup", "Optimize Lineup", "Compare Lineups", "ML Predictions"]
)

# Initialize session state for user selections
if 'selected_players' not in st.session_state:
    st.session_state.selected_players = []
if 'custom_lineups' not in st.session_state:
    st.session_state.custom_lineups = {}
if 'current_lineup_name' not in st.session_state:
    st.session_state.current_lineup_name = ""
if 'optimization_strategy' not in st.session_state:
    st.session_state.optimization_strategy = "balanced"

# Load data
@st.cache_data
def load_data():
    players = load_nba_players()
    stats = load_player_stats()
    teams = load_team_data()
    return players, stats, teams

players, player_stats, teams = load_data()

# Page: Browse Players
if page == "Browse Players":
    st.header("Browse NBA Players")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_team = st.selectbox(
            "Filter by Team",
            ["All Teams"] + sorted(players['team'].unique().tolist())
        )
    
    with col2:
        selected_position = st.selectbox(
            "Filter by Position",
            ["All Positions"] + sorted(players['position'].unique().tolist())
        )
    
    with col3:
        search_name = st.text_input("Search by Name")
    
    # Apply filters
    filtered_players = players.copy()
    if selected_team != "All Teams":
        filtered_players = filtered_players[filtered_players['team'] == selected_team]
    if selected_position != "All Positions":
        filtered_players = filtered_players[filtered_players['position'].str.contains(selected_position)]
    if search_name:
        filtered_players = filtered_players[filtered_players['name'].str.contains(search_name, case=False)]
    
    # Display players table
    st.dataframe(
        filtered_players[['name', 'team', 'position', 'age', 'height', 'weight']],
        use_container_width=True
    )
    
    # Player details
    st.subheader("Player Details")
    selected_player = st.selectbox(
        "Select a player to view details",
        filtered_players['name'].tolist()
    )
    
    if selected_player:
        player_id = players[players['name'] == selected_player].iloc[0]['player_id']
        player_data = player_stats[player_stats['player_id'] == player_id]
        
        col1, col2 = st.columns([1, 2])
        with col1:
            player_info = players[players['name'] == selected_player].iloc[0]
            st.markdown(f"**Team:** {player_info['team']}")
            st.markdown(f"**Position:** {player_info['position']}")
            st.markdown(f"**Age:** {player_info['age']}")
            st.markdown(f"**Height:** {player_info['height']}")
            st.markdown(f"**Weight:** {player_info['weight']} lbs")
            
            # Add button to select player for lineup
            if st.button(f"Add {selected_player} to lineup"):
                if len(st.session_state.selected_players) < 5:
                    if selected_player not in st.session_state.selected_players:
                        st.session_state.selected_players.append(selected_player)
                        st.success(f"Added {selected_player} to your lineup!")
                    else:
                        st.warning(f"{selected_player} is already in your lineup!")
                else:
                    st.error("You can only have 5 players in a lineup. Remove a player first.")
        
        with col2:
            # Display radar chart of player's key stats
            if not player_data.empty:
                fig = plot_player_radar_chart(player_data)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No detailed stats available for this player")

# Page: Create Lineup
elif page == "Create Lineup":
    st.header("Create Your Custom Lineup")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Your Current Lineup")
        
        # Display currently selected players
        if not st.session_state.selected_players:
            st.info("You haven't selected any players yet. Go to 'Browse Players' to add players to your lineup.")
        else:
            for i, player_name in enumerate(st.session_state.selected_players):
                col_a, col_b = st.columns([4, 1])
                with col_a:
                    st.write(f"{i+1}. {player_name}")
                with col_b:
                    if st.button("✕", key=f"remove_{i}"):
                        st.session_state.selected_players.pop(i)
                        st.rerun()
        
        # Save lineup
        if len(st.session_state.selected_players) > 0:
            st.subheader("Save This Lineup")
            lineup_name = st.text_input("Lineup Name", st.session_state.current_lineup_name)
            if st.button("Save Lineup"):
                if lineup_name and lineup_name.strip():
                    if len(st.session_state.selected_players) == 5:
                        st.session_state.custom_lineups[lineup_name] = st.session_state.selected_players.copy()
                        st.session_state.current_lineup_name = lineup_name
                        st.success(f"Lineup '{lineup_name}' saved successfully!")
                    else:
                        st.error("A valid lineup must have exactly 5 players.")
                else:
                    st.error("Please enter a name for your lineup.")
    
    with col2:
        st.subheader("Lineup Analysis")
        if len(st.session_state.selected_players) > 0:
            # Get stats for selected players
            selected_player_ids = []
            for player_name in st.session_state.selected_players:
                player_id = players[players['name'] == player_name]['player_id'].values
                if len(player_id) > 0:
                    selected_player_ids.append(player_id[0])
            
            # Show lineup stats
            if selected_player_ids:
                selected_stats = player_stats[player_stats['player_id'].isin(selected_player_ids)]
                
                if not selected_stats.empty:
                    # Display average statistics for the lineup
                    avg_stats = selected_stats.groupby('player_id').mean().reset_index()
                    avg_stats = avg_stats.merge(players[['player_id', 'name']], on='player_id')
                    
                    # Display positions for lineup balance check
                    positions = []
                    for player_name in st.session_state.selected_players:
                        pos = players[players['name'] == player_name]['position'].values[0]
                        positions.append(pos)
                    
                    st.markdown("### Lineup Composition")
                    st.markdown(f"**Positions:** {', '.join(positions)}")
                    
                    # Display lineup stats summary
                    st.markdown("### Lineup Statistics")
                    stats_cols = ['pts', 'reb', 'ast', 'stl', 'blk', 'fg_pct', 'fg3_pct', 'ft_pct']
                    avg_lineup_stats = avg_stats[stats_cols].mean()
                    
                    col_a, col_b, col_c, col_d = st.columns(4)
                    with col_a:
                        st.metric("Points", f"{avg_lineup_stats['pts']:.1f}")
                        st.metric("Rebounds", f"{avg_lineup_stats['reb']:.1f}")
                    with col_b:
                        st.metric("Assists", f"{avg_lineup_stats['ast']:.1f}")
                        st.metric("Steals", f"{avg_lineup_stats['stl']:.1f}")
                    with col_c:
                        st.metric("Blocks", f"{avg_lineup_stats['blk']:.1f}")
                        st.metric("FG%", f"{avg_lineup_stats['fg_pct']:.3f}")
                    with col_d:
                        st.metric("3P%", f"{avg_lineup_stats['fg3_pct']:.3f}")
                        st.metric("FT%", f"{avg_lineup_stats['ft_pct']:.3f}")
                    
                    # Display player comparison chart
                    st.markdown("### Player Comparison")
                    fig = plot_player_comparison(avg_stats)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No statistical data available for the selected players")
        else:
            st.info("Select players to see lineup analysis")

# Page: Optimize Lineup
elif page == "Optimize Lineup":
    st.header("Optimize Your Lineup")
    
    # Select optimization strategy
    st.subheader("Optimization Strategy")
    optimization_strategy = st.radio(
        "Choose optimization strategy:",
        ["Scoring Focus", "Defensive Focus", "Balanced Approach"],
        index=2
    )
    
    # Display saved lineups for optimization
    st.subheader("Select Lineup to Optimize")
    if not st.session_state.custom_lineups:
        st.info("You haven't saved any lineups yet. Go to 'Create Lineup' to create and save a lineup first.")
    else:
        lineup_to_optimize = st.selectbox(
            "Choose a saved lineup",
            list(st.session_state.custom_lineups.keys())
        )
        
        if lineup_to_optimize:
            current_lineup = st.session_state.custom_lineups[lineup_to_optimize]
            
            st.write("Current Lineup:")
            for i, player in enumerate(current_lineup):
                st.write(f"{i+1}. {player}")
            
            if st.button("Optimize This Lineup"):
                # Get player IDs for current lineup
                player_ids = []
                for player_name in current_lineup:
                    player_id = players[players['name'] == player_name]['player_id'].values
                    if len(player_id) > 0:
                        player_ids.append(player_id[0])
                
                # Apply optimization based on selected strategy
                if optimization_strategy == "Scoring Focus":
                    optimized_ids = optimize_lineup_for_scoring(player_ids, player_stats, players)
                elif optimization_strategy == "Defensive Focus":
                    optimized_ids = optimize_lineup_for_defense(player_ids, player_stats, players)
                else:  # Balanced
                    optimized_ids = optimize_lineup_for_balanced(player_ids, player_stats, players)
                
                # Get optimized player names
                optimized_players = []
                for player_id in optimized_ids:
                    player_name = players[players['player_id'] == player_id]['name'].values
                    if len(player_name) > 0:
                        optimized_players.append(player_name[0])
                
                st.success("Lineup optimized successfully!")
                
                # Display optimized lineup
                st.subheader("Optimized Lineup")
                for i, player in enumerate(optimized_players):
                    st.write(f"{i+1}. {player}")
                
                # Option to save optimized lineup
                save_optimized = st.checkbox("Save optimized lineup")
                if save_optimized:
                    optimized_name = st.text_input("Name for optimized lineup", 
                                                  value=f"{lineup_to_optimize} (Optimized)")
                    if st.button("Save Optimized Lineup"):
                        if optimized_name and optimized_name.strip():
                            st.session_state.custom_lineups[optimized_name] = optimized_players
                            st.success(f"Optimized lineup saved as '{optimized_name}'!")

# Page: Compare Lineups
elif page == "Compare Lineups":
    st.header("Compare Lineups")
    
    if len(st.session_state.custom_lineups) < 2:
        st.info("You need at least two saved lineups to compare. Go to 'Create Lineup' to create and save lineups.")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            lineup1 = st.selectbox(
                "Select first lineup",
                list(st.session_state.custom_lineups.keys()),
                key="lineup1"
            )
        
        with col2:
            lineup2 = st.selectbox(
                "Select second lineup",
                list(st.session_state.custom_lineups.keys()),
                key="lineup2"
            )
        
        if lineup1 and lineup2:
            if lineup1 == lineup2:
                st.warning("Please select two different lineups to compare.")
            else:
                lineup1_players = st.session_state.custom_lineups[lineup1]
                lineup2_players = st.session_state.custom_lineups[lineup2]
                
                # Get player IDs for both lineups
                lineup1_ids = []
                for player_name in lineup1_players:
                    player_id = players[players['name'] == player_name]['player_id'].values
                    if len(player_id) > 0:
                        lineup1_ids.append(player_id[0])
                
                lineup2_ids = []
                for player_name in lineup2_players:
                    player_id = players[players['name'] == player_name]['player_id'].values
                    if len(player_id) > 0:
                        lineup2_ids.append(player_id[0])
                
                # Get stats for both lineups
                lineup1_stats = player_stats[player_stats['player_id'].isin(lineup1_ids)]
                lineup2_stats = player_stats[player_stats['player_id'].isin(lineup2_ids)]
                
                # Display comparison
                st.subheader("Lineup Comparison")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"### {lineup1}")
                    for i, player in enumerate(lineup1_players):
                        st.write(f"{i+1}. {player}")
                
                with col2:
                    st.markdown(f"### {lineup2}")
                    for i, player in enumerate(lineup2_players):
                        st.write(f"{i+1}. {player}")
                
                # Calculate average stats for both lineups
                lineup1_avg = lineup1_stats.groupby('player_id').mean().reset_index().mean()
                lineup2_avg = lineup2_stats.groupby('player_id').mean().reset_index().mean()
                
                # Compare key statistics
                stats_to_compare = ['pts', 'reb', 'ast', 'stl', 'blk', 'fg_pct', 'fg3_pct', 'ft_pct']
                stat_names = {
                    'pts': 'Points', 
                    'reb': 'Rebounds', 
                    'ast': 'Assists',
                    'stl': 'Steals', 
                    'blk': 'Blocks', 
                    'fg_pct': 'FG%',
                    'fg3_pct': '3P%', 
                    'ft_pct': 'FT%'
                }
                
                # Create comparison chart
                comparison_data = pd.DataFrame({
                    'Stat': [stat_names[stat] for stat in stats_to_compare],
                    lineup1: [lineup1_avg[stat] for stat in stats_to_compare],
                    lineup2: [lineup2_avg[stat] for stat in stats_to_compare]
                })
                
                st.markdown("### Statistical Comparison")
                
                # Display side-by-side metrics
                for i, stat in enumerate(stats_to_compare):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        value1 = lineup1_avg[stat]
                        if stat in ['fg_pct', 'fg3_pct', 'ft_pct']:
                            formatted_value = f"{value1:.3f}"
                        else:
                            formatted_value = f"{value1:.1f}"
                        st.metric(stat_names[stat], formatted_value)
                    
                    with col_b:
                        value2 = lineup2_avg[stat]
                        if stat in ['fg_pct', 'fg3_pct', 'ft_pct']:
                            formatted_value = f"{value2:.3f}"
                        else:
                            formatted_value = f"{value2:.1f}"
                        
                        delta = value2 - value1
                        if stat in ['fg_pct', 'fg3_pct', 'ft_pct']:
                            delta_formatted = f"{delta:.3f}"
                        else:
                            delta_formatted = f"{delta:.1f}"
                        
                        st.metric(stat_names[stat], formatted_value, delta=delta_formatted)
                
                # Create comparison visualization
                st.markdown("### Visual Comparison")
                fig = plot_team_performance(comparison_data, lineup1, lineup2)
                st.plotly_chart(fig, use_container_width=True)

# Page: ML Predictions
elif page == "ML Predictions":
    st.header("Machine Learning Predictions")
    
    st.markdown("""
    This page uses machine learning models to predict how well your lineup will perform.
    Select a saved lineup to get predictions on:
    
    - Expected Points Per Game
    - Win Probability
    - Offensive and Defensive Ratings
    """)
    
    if not st.session_state.custom_lineups:
        st.info("You haven't saved any lineups yet. Go to 'Create Lineup' to create and save a lineup first.")
    else:
        lineup_to_predict = st.selectbox(
            "Select a lineup for prediction",
            list(st.session_state.custom_lineups.keys())
        )
        
        if lineup_to_predict:
            selected_lineup = st.session_state.custom_lineups[lineup_to_predict]
            
            st.write("Selected Lineup:")
            for i, player in enumerate(selected_lineup):
                st.write(f"{i+1}. {player}")
            
            if st.button("Generate Predictions"):
                # Get player IDs
                player_ids = []
                for player_name in selected_lineup:
                    player_id = players[players['name'] == player_name]['player_id'].values
                    if len(player_id) > 0:
                        player_ids.append(player_id[0])
                
                # Generate predictions
                if len(player_ids) == 5:
                    predictions = predict_lineup_performance(player_ids, player_stats, players)
                    
                    st.success("Predictions generated successfully!")
                    
                    # Display predictions
                    st.subheader("Lineup Performance Predictions")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Predicted Points", f"{predictions['points_per_game']:.1f}")
                    with col2:
                        st.metric("Win Probability", f"{predictions['win_probability']:.1%}")
                    with col3:
                        st.metric("Team Chemistry", f"{predictions['chemistry_score']:.0f}/100")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Offensive Rating", f"{predictions['offensive_rating']:.1f}")
                    with col2:
                        st.metric("Defensive Rating", f"{predictions['defensive_rating']:.1f}")
                    
                    # Display prediction confidence and factors
                    st.subheader("Prediction Insights")
                    st.markdown(f"**Confidence Level:** {predictions['confidence_level']}")
                    
                    st.markdown("**Key Strengths:**")
                    for strength in predictions['strengths']:
                        st.markdown(f"- {strength}")
                    
                    st.markdown("**Areas for Improvement:**")
                    for weakness in predictions['weaknesses']:
                        st.markdown(f"- {weakness}")
                    
                    # Prediction disclaimer
                    st.info(
                        "Note: These predictions are based on historical data and simulated games. "
                        "Actual performance may vary due to many factors not captured in the model."
                    )
                else:
                    st.error("A valid lineup must have exactly 5 players.")

# Display footer
st.markdown("---")
st.markdown("NBA Lineup Optimizer - Created for educational purposes") 