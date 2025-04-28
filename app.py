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

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import project modules
from src.data_loader import (
    load_nba_players, 
    load_player_stats, 
    load_team_data
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
from src.ml.lineup_prediction import LineupPredictor

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
    # Get some star players for example lineups
    stars = players[players['name'].str.contains('LeBron|Curry|Giannis|Jokic|Doncic', case=False, na=False)]
    
    # Create example lineups if we have enough star players
    if len(stars) >= 5:
        example_lineup1 = stars.iloc[0:5]['name'].tolist()
        st.session_state.custom_lineups["All-Star Lineup"] = example_lineup1
        
        # Create a second lineup with different players
        remaining_players = players[~players['name'].isin(example_lineup1)]
        if len(remaining_players) >= 5:
            example_lineup2 = remaining_players.iloc[0:5]['name'].tolist()
            st.session_state.custom_lineups["Backup Lineup"] = example_lineup2

# Sidebar navigation
st.sidebar.title("NBA Lineup Optimizer")
st.sidebar.image("https://cdn.nba.com/logos/nba/nba-logoman-75-word_white.svg", width=200)
st.sidebar.markdown("---")

# Navigation with icons and descriptions
st.sidebar.header("Navigation")

page = st.sidebar.radio(
    "Select a page",
    options=["Player Explorer", "Lineup Builder", "Lineup Optimizer", "ML Prediction"],
    format_func=lambda x: {
        "Player Explorer": "👤 Player Explorer",
        "Lineup Builder": "🏀 Lineup Builder",
        "Lineup Optimizer": "⚙️ Lineup Optimizer",
        "ML Prediction": "🧠 ML Prediction"
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
        
        # Player selection with improved UI
        st.markdown("<h3 style='color:#1e3a8a;background-color:#f0f2f6;padding:10px;border-radius:5px;'>Player Selection</h3>", unsafe_allow_html=True)
        if not filtered_players.empty:
            # Show count of filtered players
            st.info(f"Found {len(filtered_players)} players matching your filters")
            
            # Use a more prominent selectbox for player selection
            selected_player = st.selectbox(
                "Select Player for Analysis",
                filtered_players['name'].tolist(),
                format_func=lambda x: f"🏀 {x}"
            )
        
            # Add to lineup button - use primary button style
            if st.button("✨ Add to Lineup", type="primary"):
                player_id = filtered_players[filtered_players['name'] == selected_player]['player_id'].iloc[0]
                if len(st.session_state.selected_players) < 5:
                    if player_id not in st.session_state.selected_players:
                        st.session_state.selected_players.append(player_id)
                        st.success(f"Added {selected_player} to lineup")
                    else:
                        st.warning(f"{selected_player} is already in lineup")
                else:
                    st.error("Lineup already has 5 players. Remove a player first.")
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
        if 'selected_player' in locals() and not filtered_players.empty:
            # Player details
            player_data = filtered_players[filtered_players['name'] == selected_player].iloc[0]
            player_id = player_data['player_id']
            player_stats = stats[stats['player_id'] == player_id]
            
            st.subheader(f"Player Analysis: {selected_player}")
            
            # Player Bio
            col_bio1, col_bio2 = st.columns(2)
            with col_bio1:
                st.write(f"**Team:** {player_data['team']}")
                st.write(f"**Position:** {player_data['position']}")
            with col_bio2:
                st.write(f"**Height:** {player_data['height']} cm")
                st.write(f"**Weight:** {player_data['weight']} kg")
            
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
                    name=selected_player,
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
        <li>Review and manage your current lineup</li>
        <li>Analyze the position distribution and team balance</li>
        <li>View team-level statistics projected from player averages</li>
    </ol>
    <p><b>Tip:</b> A balanced lineup typically includes 2 guards, 2 forwards, and 1 center.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Current Lineup")
        
        # Show current lineup
        if st.session_state.selected_players:
            st.write(f"Lineup Name: {st.session_state.current_lineup_name}")
            
            # Allow user to modify lineup name
            new_name = st.text_input("Change Lineup Name", value=st.session_state.current_lineup_name)
            if new_name != st.session_state.current_lineup_name:
                st.session_state.current_lineup_name = new_name
            
            # Display players in lineup
            for i, player_id in enumerate(st.session_state.selected_players):
                player = players[players['player_id'] == player_id].iloc[0]
                col_p1, col_p2, col_p3 = st.columns([3, 1, 1])
                
                with col_p1:
                    st.write(f"{i+1}. {player['name']} ({player['position']}, {player['team']})")
                
                with col_p3:
                    if st.button(f"Remove {i}", key=f"remove_{i}"):
                        st.session_state.selected_players.pop(i)
                        st.rerun()
            
            # Clear lineup button
            if st.button("Clear Lineup"):
                st.session_state.selected_players = []
                st.rerun()
        else:
            st.info("No players selected. Use the Player Explorer to add players to your lineup.")
    
    with col2:
        st.subheader("Lineup Analysis")
        
        if len(st.session_state.selected_players) > 0:
            # Position distribution
            position_counts = {}
            for player_id in st.session_state.selected_players:
                player = players[players['player_id'] == player_id].iloc[0]
                position = player['position']
                if position in position_counts:
                    position_counts[position] += 1
                else:
                    position_counts[position] = 1
            
            # Display position distribution
            st.write("**Position Distribution:**")
            fig = px.pie(
                values=list(position_counts.values()),
                names=list(position_counts.keys()),
                title="Position Distribution"
            )
            st.plotly_chart(fig)
            
            # Calculate and display team stats
            if len(st.session_state.selected_players) > 0:
                st.write("**Team Statistics:**")
                
                lineup_stats = stats[stats['player_id'].isin(st.session_state.selected_players)]
                if not lineup_stats.empty:
                    # Calculate average stats
                    avg_stats = lineup_stats.mean(numeric_only=True)
                    
                    key_stats = {
                        'pts': 'Points',
                        'reb': 'Rebounds',
                        'ast': 'Assists',
                        'stl': 'Steals',
                        'blk': 'Blocks'
                    }
                    
                    stat_values = []
                    stat_names = []
                    
                    for key, name in key_stats.items():
                        if key in avg_stats:
                            stat_values.append(avg_stats[key] * 5)  # Multiply by 5 for team total
                            stat_names.append(name)
                    
                    fig = px.bar(
                        x=stat_names,
                        y=stat_values,
                        labels={'x': 'Statistic', 'y': 'Value (Team Total)'}
                    )
                    
                    st.plotly_chart(fig)
                else:
                    st.warning("No statistics available for the selected players.")
        else:
            st.info("Add players to your lineup to see the analysis.")

# Page: Lineup Optimizer
elif page == "Lineup Optimizer":
    st.header("⚙️ Lineup Optimizer")
    st.markdown("""
    <div style='background-color:#f0f2f6;padding:1rem;border-radius:0.5rem;margin-bottom:1rem;color:#333333;'>
    <h4 style='margin-top:0;color:#1e3a8a;'>How to use this page:</h4>
    <ol>
        <li>Select an optimization strategy that matches your team's needs</li>
        <li>Click "Optimize Lineup" to generate the best combination of players</li>
        <li>Review the optimized lineup and its projected performance</li>
        <li>Apply the changes if you're satisfied with the result</li>
    </ol>
    <p><b>Note:</b> You need at least 5 players in your lineup to use the optimizer.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if len(st.session_state.selected_players) < 5:
        st.warning("You need at least 5 players in your lineup to use the optimizer. Please add more players in the Lineup Builder.")
    else:
        optimization_method = st.selectbox(
            "Select Optimization Method",
            ["Scoring", "Defense", "Balanced"]
        )
        
        if st.button("Optimize Lineup"):
            with st.spinner("Optimizing lineup..."):
                if optimization_method == "Scoring":
                    optimized_lineup = optimize_lineup_for_scoring(
                        st.session_state.selected_players, 
                        stats, 
                        players
                    )
                elif optimization_method == "Defense":
                    optimized_lineup = optimize_lineup_for_defense(
                        st.session_state.selected_players, 
                        stats, 
                        players
                    )
                else:  # Balanced
                    optimized_lineup = optimize_lineup_for_balanced(
                        st.session_state.selected_players, 
                        stats, 
                        players
                    )
                
                # Display optimized lineup
                st.subheader(f"Optimized Lineup ({optimization_method})")
                
                # Show before and after comparison
                col_before, col_after = st.columns(2)
                
                with col_before:
                    st.write("**Original Lineup:**")
                    for player_id in st.session_state.selected_players[:5]:
                        player = players[players['player_id'] == player_id].iloc[0]
                        st.write(f"- {player['name']} ({player['position']}, {player['team']})")
                
                with col_after:
                    st.write("**Optimized Lineup:**")
                    for player_id in optimized_lineup:
                        player = players[players['player_id'] == player_id].iloc[0]
                        st.write(f"- {player['name']} ({player['position']}, {player['team']})")
                
                # Calculate chemistry score
                chemistry_score = calculate_lineup_chemistry(optimized_lineup, players)
                st.write(f"**Lineup Chemistry Score:** {chemistry_score:.2f}/100")
                
                # Check lineup balance
                is_balanced, position_coverage = check_lineup_balance(optimized_lineup, players)
                if is_balanced:
                    st.success("This lineup has good position balance.")
                else:
                    missing_positions = [pos for pos, covered in position_coverage.items() if not covered]
                    st.warning(f"This lineup may lack coverage in: {', '.join(missing_positions)}")
                
                # Visualize key metrics comparison
                st.subheader("Lineup Comparison")
                
                # Calculate metrics for both lineups
                original_stats = stats[stats['player_id'].isin(st.session_state.selected_players[:5])]
                optimized_stats = stats[stats['player_id'].isin(optimized_lineup)]
                
                key_metrics = ['pts', 'reb', 'ast', 'stl', 'blk']
                original_values = []
                optimized_values = []
                
                for metric in key_metrics:
                    if metric in original_stats.columns and metric in optimized_stats.columns:
                        original_values.append(original_stats[metric].mean(numeric_only=True) * 5)  # Team total
                        optimized_values.append(optimized_stats[metric].mean(numeric_only=True) * 5)  # Team total
                
                # Create comparison chart
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    x=key_metrics,
                    y=original_values,
                    name='Original Lineup'
                ))
                
                fig.add_trace(go.Bar(
                    x=key_metrics,
                    y=optimized_values,
                    name='Optimized Lineup'
                ))
                
                fig.update_layout(
                    title="Lineup Comparison (Team Totals)",
                    xaxis_title="Metrics",
                    yaxis_title="Value",
                    barmode='group'
                )
                
                st.plotly_chart(fig)
                
                # Option to update current lineup
                if st.button("Update Current Lineup with Optimized Result"):
                    st.session_state.selected_players = optimized_lineup + st.session_state.selected_players[5:]
                    st.success("Lineup updated successfully!")
                    st.rerun()

# Page: ML Prediction
elif page == "ML Prediction":
    st.header("🧠 Machine Learning Prediction")
    st.markdown("""
    <div style='background-color:#f0f2f6;padding:1rem;border-radius:0.5rem;margin-bottom:1rem;color:#333333;'>
    <h4 style='margin-top:0;color:#1e3a8a;'>How to use this page:</h4>
    <ol>
        <li>First, train a new model or load an existing one</li>
        <li>View feature importance to understand what factors influence performance</li>
        <li>Predict the performance of your current lineup</li>
        <li>Explore suggested lineup improvements based on ML predictions</li>
    </ol>
    <p><b>Advanced:</b> The model uses Random Forest Regression to predict offensive and defensive ratings.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize predictor
    predictor = LineupPredictor()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Train Model")
        
        if st.button("Train New Prediction Model"):
            with st.spinner("Training model... This may take a minute..."):
                try:
                    # Create directory for models if it doesn't exist
                    os.makedirs('data/models/lineup_predictor', exist_ok=True)
                    
                    # Generate training data
                    lineups, offensive_ratings, defensive_ratings = predictor.generate_training_data(stats)
                    
                    # Train model
                    training_metrics = predictor.train(lineups, offensive_ratings, defensive_ratings, stats)
                    
                    # Update session state
                    st.session_state.model_trained = True
                    
                    # Show training metrics
                    st.success("Model trained successfully!")
                    st.write("**Training Metrics:**")
                    st.write(f"- Samples: {training_metrics.get('n_samples', 'N/A')}")
                    st.write(f"- Features: {training_metrics.get('n_features', 'N/A')}")
                    st.write(f"- Offensive Model R²: {training_metrics.get('offense_r2', 'N/A'):.4f}")
                    st.write(f"- Defensive Model R²: {training_metrics.get('defense_r2', 'N/A'):.4f}")
                except Exception as e:
                    st.error(f"Error training model: {e}")
        
        # Load existing model
        if os.path.exists('data/models/lineup_predictor/offense_model.pkl'):
            if st.button("Load Existing Model"):
                with st.spinner("Loading model..."):
                    try:
                        success = predictor.load_models()
                        if success:
                            st.session_state.model_trained = True
                            st.success("Model loaded successfully!")
                        else:
                            st.error("Failed to load model.")
                    except Exception as e:
                        st.error(f"Error loading model: {e}")
        
        # Feature importance
        if st.session_state.model_trained:
            st.subheader("Feature Importance")
            
            try:
                feature_importance = predictor.get_feature_importance()
                
                # Display feature importance
                if not feature_importance.empty:
                    # Show top 10 features for offense and defense
                    st.write("**Top Features for Offensive Rating:**")
                    offense_importance = feature_importance.sort_values('Offense Importance', ascending=False).head(10)
                    
                    fig = px.bar(
                        offense_importance,
                        x='Offense Importance',
                        y='Feature',
                        orientation='h',
                        title="Top Features for Offense"
                    )
                    st.plotly_chart(fig)
                    
                    st.write("**Top Features for Defensive Rating:**")
                    defense_importance = feature_importance.sort_values('Defense Importance', ascending=False).head(10)
                    
                    fig = px.bar(
                        defense_importance,
                        x='Defense Importance',
                        y='Feature',
                        orientation='h',
                        title="Top Features for Defense"
                    )
                    st.plotly_chart(fig)
            except Exception as e:
                st.error(f"Error displaying feature importance: {e}")
    
    with col2:
        st.subheader("Lineup Performance Prediction")
        
        if len(st.session_state.selected_players) < 5:
            st.warning("You need at least 5 players in your lineup to make a prediction.")
        else:
            lineup_to_predict = st.session_state.selected_players[:5]
            
            if st.button("Predict Performance"):
                with st.spinner("Predicting lineup performance..."):
                    try:
                        # Predict lineup performance
                        off_rating, def_rating = predictor.predict(lineup_to_predict, stats)
                        
                        # Display prediction results
                        st.success("Prediction complete!")
                        
                        col_rating1, col_rating2 = st.columns(2)
                        
                        with col_rating1:
                            st.metric("Offensive Rating", f"{off_rating:.1f}/100")
                        
                        with col_rating2:
                            st.metric("Defensive Rating", f"{def_rating:.1f}/100")
                        
                        # Overall rating (simple average)
                        overall_rating = (off_rating + def_rating) / 2
                        
                        # Create gauge chart for overall rating
                        fig = go.Figure(go.Indicator(
                            mode = "gauge+number",
                            value = overall_rating,
                            title = {'text': "Overall Rating"},
                            gauge = {
                                'axis': {'range': [0, 100]},
                                'bar': {'color': "darkblue"},
                                'steps': [
                                    {'range': [0, 40], 'color': "red"},
                                    {'range': [40, 70], 'color': "yellow"},
                                    {'range': [70, 100], 'color': "green"}
                                ],
                                'threshold': {
                                    'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75,
                                    'value': 80
                                }
                            }
                        ))
                        
                        st.plotly_chart(fig)
                        
                        # Display lineup
                        st.subheader("Lineup Players")
                        for player_id in lineup_to_predict:
                            player = players[players['player_id'] == player_id].iloc[0]
                            st.write(f"- {player['name']} ({player['position']}, {player['team']})")
                        
                        # Performance analysis
                        st.subheader("Performance Analysis")
                        
                        if off_rating > 70:
                            st.success("This lineup has excellent offensive potential.")
                        elif off_rating > 50:
                            st.info("This lineup has good offensive capabilities.")
                        else:
                            st.warning("This lineup may struggle offensively.")
                            
                        if def_rating > 70:
                            st.success("This lineup has excellent defensive potential.")
                        elif def_rating > 50:
                            st.info("This lineup has good defensive capabilities.")
                        else:
                            st.warning("This lineup may struggle defensively.")
                            
                        if overall_rating > 70:
                            st.success("Overall, this looks like a strong lineup!")
                        elif overall_rating > 50:
                            st.info("This lineup has good potential but could be improved.")
                        else:
                            st.warning("This lineup may need significant improvements.")
                            
                    except Exception as e:
                        st.error(f"Error making prediction: {e}")
            
            # Suggestion for lineup improvement
            if st.session_state.model_trained and len(st.session_state.selected_players) >= 5:
                if st.button("Suggest Lineup Improvement"):
                    with st.spinner("Analyzing lineup for possible improvements..."):
                        try:
                            # Get all available players not in the lineup
                            all_player_ids = players['player_id'].tolist()
                            bench_players = [pid for pid in all_player_ids if pid not in lineup_to_predict]
                            
                            # Find best substitution
                            suggestions = predictor.predict_best_substitution(
                                lineup_to_predict, 
                                bench_players, 
                                stats
                            )
                            
                            if suggestions:
                                st.success("Substitution analysis complete!")
                                
                                st.subheader("Recommended Substitution")
                                
                                replace_id = suggestions['replace_player_id']
                                with_id = suggestions['with_player_id']
                                
                                replace_player = players[players['player_id'] == replace_id].iloc[0]
                                with_player = players[players['player_id'] == with_id].iloc[0]
                                
                                st.write(f"Replace: **{replace_player['name']}** ({replace_player['position']}, {replace_player['team']})")
                                st.write(f"With: **{with_player['name']}** ({with_player['position']}, {with_player['team']})")
                                
                                # Show improvement
                                st.write(f"**Expected Improvement:**")
                                st.write(f"- Offensive Rating: {suggestions['offense_improvement']:+.2f}")
                                st.write(f"- Defensive Rating: {suggestions['defense_improvement']:+.2f}")
                                st.write(f"- Overall Rating: {suggestions['overall_improvement']:+.2f}")
                                
                                # Button to apply suggestion
                                if st.button("Apply This Substitution"):
                                    # Find index of player to replace
                                    idx = lineup_to_predict.index(replace_id)
                                    # Make the substitution
                                    new_lineup = lineup_to_predict.copy()
                                    new_lineup[idx] = with_id
                                    
                                    # Update session state
                                    st.session_state.selected_players = new_lineup + st.session_state.selected_players[5:]
                                    st.success("Lineup updated with suggested substitution!")
                                    st.rerun()
                            else:
                                st.warning("No improvement suggestions found.")
                        except Exception as e:
                            st.error(f"Error generating improvement suggestions: {e}")

# Footer
st.markdown("---")
st.markdown("NBA Lineup Optimizer - Demonstrating Data Science & Machine Learning with Sports Analytics") 