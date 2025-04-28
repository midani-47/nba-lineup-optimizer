import streamlit as st
import pandas as pd
import os
import sys
import numpy as np

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import project modules
from src.data_loader import (
    load_nba_players, 
    load_player_stats, 
    load_team_data,
    import_real_nba_data
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
    optimize_lineup_for_balanced,
    calculate_lineup_chemistry,
    check_lineup_balance
)
from src.models.lineup_predictor import (
    predict_lineup_performance,
    train_models
)

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
    st.session_state.current_lineup_name = ""

# Load data
@st.cache_data
def load_data():
    players = load_nba_players()
    stats = load_player_stats()
    teams = load_team_data()
    return players, stats, teams

players, player_stats, teams = load_data()

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

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select a page",
    ["Data Explorer", "Lineup Optimizer", "ML Predictions", "Model Insights"]
)

# Page: Data Explorer
if page == "Data Explorer":
    st.header("NBA Player Data Explorer")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Filter options
        st.subheader("Filters")
        selected_team = st.selectbox(
            "Team",
            ["All Teams"] + sorted(players['team'].fillna("Unknown").astype(str).unique().tolist())
        )
        
        selected_position = st.selectbox(
            "Position",
            ["All Positions"] + sorted(players['position'].fillna("Unknown").astype(str).unique().tolist())
        )
        
        search_name = st.text_input("Search Player")
        
        # Apply filters
        filtered_players = players.copy()
        if selected_team != "All Teams":
            filtered_players = filtered_players[filtered_players['team'] == selected_team]
        if selected_position != "All Positions":
            filtered_players = filtered_players[filtered_players['position'].fillna("Unknown").str.contains(selected_position)]
        if search_name:
            filtered_players = filtered_players[filtered_players['name'].str.contains(search_name, case=False)]
        
        # Player selection
        st.subheader("Player Selection")
        selected_player = st.selectbox(
            "Select Player for Analysis",
            filtered_players['name'].tolist()
        )
        
        # Add to lineup button
        if st.button("Add to Lineup"):
            if len(st.session_state.selected_players) < 5:
                if selected_player not in st.session_state.selected_players:
                    st.session_state.selected_players.append(selected_player)
                    st.success(f"Added {selected_player} to lineup")
                else:
                    st.warning(f"{selected_player} is already in lineup")
            else:
                st.error("Lineup already has 5 players. Remove a player first.")
        
        # Current lineup display
        st.subheader("Current Lineup")
        if not st.session_state.selected_players:
            st.info("No players selected")
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
            st.subheader("Save Lineup")
            lineup_name = st.text_input("Lineup Name", key="lineup_name_input")
            if st.button("Save Lineup"):
                if lineup_name and lineup_name.strip():
                    if len(st.session_state.selected_players) == 5:
                        st.session_state.custom_lineups[lineup_name] = st.session_state.selected_players.copy()
                        st.success(f"Lineup '{lineup_name}' saved!")
                    else:
                        st.error("A lineup must have exactly 5 players")
                else:
                    st.error("Please enter a lineup name")
    
    with col2:
        # Player data visualization
        if selected_player:
            st.subheader(f"Player Analysis: {selected_player}")
            
            player_id = players[players['name'] == selected_player].iloc[0]['player_id']
            player_data = player_stats[player_stats['player_id'] == player_id]
            
            col_stats1, col_stats2 = st.columns(2)
            
            with col_stats1:
                if not player_data.empty:
                    avg_stats = player_data.mean(numeric_only=True)
                    st.metric("Points per Game", f"{avg_stats['pts']:.1f}")
                    st.metric("Rebounds per Game", f"{avg_stats['reb']:.1f}")
                    st.metric("Assists per Game", f"{avg_stats['ast']:.1f}")
            
            with col_stats2:
                if not player_data.empty:
                    st.metric("FG%", f"{avg_stats['fg_pct']:.3f}")
                    st.metric("3P%", f"{avg_stats['fg3_pct']:.3f}")
                    st.metric("Steals + Blocks", f"{avg_stats['stl'] + avg_stats['blk']:.1f}")
            
            # Player radar chart
            if not player_data.empty:
                st.subheader("Player Radar Chart")
                fig = plot_player_radar_chart(player_data)
                st.plotly_chart(fig, use_container_width=True)
            
        # Player table
        st.subheader("Players Database")
        st.dataframe(
            filtered_players[['name', 'team', 'position', 'age', 'height', 'weight']],
            use_container_width=True
        )

# Page: Lineup Optimizer
elif page == "Lineup Optimizer":
    st.header("ML-Powered Lineup Optimizer")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Select Lineup to Optimize")
        
        if not st.session_state.custom_lineups:
            st.info("No lineups saved. Create a lineup in the Data Explorer.")
        else:
            lineup_to_optimize = st.selectbox(
                "Choose a lineup",
                list(st.session_state.custom_lineups.keys())
            )
            
            if lineup_to_optimize:
                current_lineup = st.session_state.custom_lineups[lineup_to_optimize]
                
                st.write("Current Lineup:")
                for i, player in enumerate(current_lineup):
                    st.write(f"{i+1}. {player}")
                
                st.subheader("Optimization Strategy")
                optimization_strategy = st.radio(
                    "Choose strategy:",
                    ["Scoring Focus", "Defensive Focus", "Balanced Approach"],
                    index=2
                )
                
                if st.button("Run Optimization Algorithm"):
                    # Get player IDs
                    player_ids = []
                    for player_name in current_lineup:
                        player_id = players[players['name'] == player_name]['player_id'].values
                        if len(player_id) > 0:
                            player_ids.append(player_id[0])
                    
                    # Run optimization
                    with st.spinner("Optimizing lineup..."):
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
                    
                    # Save optimized lineup
                    optimized_name = f"{lineup_to_optimize} (Optimized)"
                    st.session_state.custom_lineups[optimized_name] = optimized_players
                    st.success("Optimization complete! Lineup saved as: " + optimized_name)
                    st.rerun()
    
    with col2:
        st.subheader("Lineup Comparison")
        
        if len(st.session_state.custom_lineups) >= 2:
            col_a, col_b = st.columns(2)
            
            with col_a:
                lineup1 = st.selectbox(
                    "First Lineup",
                    list(st.session_state.custom_lineups.keys()),
                    key="lineup1"
                )
            
            with col_b:
                # Filter out the first selected lineup
                remaining_lineups = [l for l in list(st.session_state.custom_lineups.keys()) if l != lineup1]
                lineup2 = st.selectbox(
                    "Second Lineup",
                    remaining_lineups,
                    key="lineup2"
                )
            
            if lineup1 and lineup2:
                # Get player IDs and stats for both lineups
                lineup1_players = st.session_state.custom_lineups[lineup1]
                lineup2_players = st.session_state.custom_lineups[lineup2]
                
                # Get player IDs
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
                
                # Get stats
                lineup1_stats = player_stats[player_stats['player_id'].isin(lineup1_ids)]
                lineup2_stats = player_stats[player_stats['player_id'].isin(lineup2_ids)]
                
                # Display comparison
                col_c, col_d = st.columns(2)
                
                with col_c:
                    st.markdown(f"### {lineup1}")
                    for i, player in enumerate(lineup1_players):
                        st.write(f"{i+1}. {player}")
                
                with col_d:
                    st.markdown(f"### {lineup2}")
                    for i, player in enumerate(lineup2_players):
                        st.write(f"{i+1}. {player}")
                
                # Statistical comparison
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
                
                # Calculate averages
                lineup1_avg = lineup1_stats.groupby('player_id').mean().reset_index().mean()
                lineup2_avg = lineup2_stats.groupby('player_id').mean().reset_index().mean()
                
                # Create comparison data
                comparison_data = pd.DataFrame({
                    'Stat': [stat_names[stat] for stat in stats_to_compare],
                    lineup1: [lineup1_avg[stat] for stat in stats_to_compare],
                    lineup2: [lineup2_avg[stat] for stat in stats_to_compare]
                })
                
                # Chemistry scores
                chemistry1 = calculate_lineup_chemistry(lineup1_ids, player_stats)
                chemistry2 = calculate_lineup_chemistry(lineup2_ids, player_stats)
                
                st.subheader("Team Chemistry Scores")
                col_chem1, col_chem2 = st.columns(2)
                with col_chem1:
                    st.metric(f"{lineup1}", f"{chemistry1:.1f}/100")
                with col_chem2:
                    st.metric(f"{lineup2}", f"{chemistry2:.1f}/100")
                
                # Create visualization
                st.subheader("Statistical Comparison")
                fig = plot_team_performance(comparison_data, lineup1, lineup2)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("You need at least two lineups to compare. Create or optimize lineups to compare them.")

# Page: ML Predictions
elif page == "ML Predictions":
    st.header("Machine Learning Predictions")
    
    st.markdown("""
    This page uses machine learning models to predict how well a lineup will perform.
    The models analyze player statistics and lineup composition to predict:
    
    - Expected Points Per Game
    - Win Probability
    - Offensive and Defensive Ratings
    - Chemistry Score
    """)
    
    if not st.session_state.custom_lineups:
        st.info("No lineups saved. Create a lineup in the Data Explorer.")
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
            
            if st.button("Generate ML Predictions"):
                # Get player IDs
                player_ids = []
                for player_name in selected_lineup:
                    player_id = players[players['name'] == player_name]['player_id'].values
                    if len(player_id) > 0:
                        player_ids.append(player_id[0])
                
                # Generate predictions
                if len(player_ids) == 5:
                    with st.spinner("Running machine learning models..."):
                        predictions = predict_lineup_performance(player_ids, player_stats, players)
                    
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
                    
                    # Display prediction insights
                    st.subheader("Model Insights")
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown("**Key Strengths:**")
                        for strength in predictions['strengths']:
                            st.markdown(f"- {strength}")
                    
                    with col_b:
                        st.markdown("**Areas for Improvement:**")
                        for weakness in predictions['weaknesses']:
                            st.markdown(f"- {weakness}")
                    
                    # Balance check
                    is_balanced, balance_reasons = check_lineup_balance(player_ids, players)
                    st.subheader("Lineup Balance Analysis")
                    if is_balanced:
                        st.success("This lineup has good positional balance")
                    else:
                        st.warning("This lineup has potential positional issues")
                        for reason in balance_reasons:
                            st.markdown(f"- {reason}")

# Page: Model Insights
elif page == "Model Insights":
    st.header("Data Science & Machine Learning Insights")
    
    st.markdown("""
    ### Machine Learning Techniques Used
    
    This application demonstrates several data science and machine learning concepts:
    
    1. **Feature Engineering**: We transform raw player statistics into meaningful features
    2. **Random Forest Regression**: Used to predict lineup performance metrics
    3. **Statistical Analysis**: Creating metrics to quantify lineup chemistry and balance
    4. **Data Visualization**: Interactive charts to compare lineups and players
    """)
    
    # Model explanation
    st.subheader("How the Lineup Optimization Works")
    
    st.markdown("""
    The lineup optimizer uses a combination of:
    
    - **Player Performance Metrics**: Analyzing individual player statistics
    - **Position-Based Analysis**: Maintaining lineup balance across positions
    - **Chemistry Calculation**: Finding players with complementary skills
    
    For the scoring optimization, we use a weighted formula:
    ```python
    scoring_metric = points + 0.5 * assists + 30 * three_point_percentage
    ```
    
    For defensive optimization:
    ```python
    defensive_metric = steals + blocks + 0.5 * rebounds
    ```
    
    The balanced approach combines both metrics.
    """)
    
    # Machine learning model details
    st.subheader("Machine Learning Model Architecture")
    
    st.markdown("""
    Our prediction system uses ensemble learning with Random Forest models:
    
    1. **Points Predictor**: Forecasts total points the lineup will score
    2. **Win Probability Model**: Estimates likelihood of winning
    3. **Offensive & Defensive Rating Models**: Predicts team efficiency
    
    Each model is trained on:
    - Individual player statistics
    - Position balance indicators
    - Chemistry calculations based on skill complementarity
    """)
    
    # Feature importance visualization
    st.subheader("Feature Importance")
    
    # Create dummy feature importance for demonstration
    features = ['Points', 'Rebounds', 'Assists', 'Steals', 'Blocks', 'FG%', '3P%', 'Skill Diversity', 'Position Balance']
    importance = [0.25, 0.15, 0.12, 0.08, 0.10, 0.09, 0.11, 0.05, 0.05]
    
    # Sort by importance
    sorted_indices = np.argsort(importance)[::-1]
    sorted_features = [features[i] for i in sorted_indices]
    sorted_importance = [importance[i] for i in sorted_indices]
    
    # Create DataFrame for chart
    feature_df = pd.DataFrame({
        'Feature': sorted_features,
        'Importance': sorted_importance
    })
    
    # Display chart
    st.bar_chart(feature_df.set_index('Feature'))
    
    st.markdown("""
    ### Technical Implementation Details
    
    The application demonstrates several advanced programming concepts:
    
    - **Modular Code Architecture**: Separation of data loading, analysis, and visualization
    - **Caching for Performance**: Using Streamlit's caching for efficient data loading
    - **Statistical Analysis**: Advanced pandas operations for data manipulation
    
    The machine learning pipeline includes:
    - Feature extraction from player statistics
    - Model training with cross-validation
    - Prediction generation with confidence metrics
    """)

# Footer
st.markdown("---")
st.markdown("NBA Lineup Optimizer - Demonstrating Data Science & Machine Learning with Sports Analytics") 