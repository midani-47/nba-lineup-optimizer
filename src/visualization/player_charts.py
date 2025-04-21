import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

def plot_player_radar_chart(player_data):
    """
    Create a radar chart for a player's key statistics.
    
    Args:
        player_data (pandas.DataFrame): DataFrame containing player statistics
    
    Returns:
        plotly.graph_objects.Figure: Radar chart of player statistics
    """
    # Compute average statistics
    avg_stats = player_data.mean(numeric_only=True)
    
    # Select key statistics for the radar chart
    stats = ['pts', 'reb', 'ast', 'stl', 'blk']
    values = [avg_stats[stat] for stat in stats]
    
    # Normalize values for better visualization
    max_values = {'pts': 30, 'reb': 15, 'ast': 10, 'stl': 3, 'blk': 3}
    normalized_values = [min(100 * values[i] / max_values[stats[i]], 100) for i in range(len(stats))]
    
    # Create radar chart
    categories = ['Points', 'Rebounds', 'Assists', 'Steals', 'Blocks']
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=normalized_values,
        theta=categories,
        fill='toself',
        name=player_data['player_name'].iloc[0],
        marker=dict(color='rgba(31, 119, 180, 0.8)')
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False,
        title=f"{player_data['player_name'].iloc[0]} - Performance Metrics"
    )
    
    # Add annotations showing actual values
    for i, (cat, val) in enumerate(zip(categories, values)):
        angle = i * 2 * np.pi / len(categories)
        # Adjust radius for annotation placement
        radius = normalized_values[i] + 5
        x = 0.5 * radius * np.cos(angle - np.pi/2) / 100
        y = 0.5 * radius * np.sin(angle - np.pi/2) / 100
        
        # Adjust text position
        x_text = 0.5 + x
        y_text = 0.5 + y
        
        fig.add_annotation(
            x=x_text,
            y=y_text,
            text=f"{val:.1f}",
            showarrow=False,
            font=dict(
                size=10,
                color="black"
            )
        )
    
    return fig

def plot_player_comparison(player_stats_df):
    """
    Create a comparison chart for multiple players.
    
    Args:
        player_stats_df (pandas.DataFrame): DataFrame containing statistics for multiple players
    
    Returns:
        plotly.graph_objects.Figure: Bar chart comparing player statistics
    """
    # Select key statistics for comparison
    stats_to_compare = ['pts', 'reb', 'ast', 'stl', 'blk']
    
    # Prepare data for visualization
    player_names = player_stats_df['name'].tolist()
    
    # Create figure
    fig = go.Figure()
    
    # Define colors for bars
    colors = px.colors.qualitative.Plotly[:len(player_names)]
    
    # Add traces for each statistic
    for i, stat in enumerate(stats_to_compare):
        y_values = player_stats_df[stat].tolist()
        
        fig.add_trace(go.Bar(
            x=player_names,
            y=y_values,
            name=stat.upper(),
            marker_color=colors[i % len(colors)]
        ))
    
    # Update layout
    fig.update_layout(
        title="Player Comparison",
        xaxis_title="Player",
        yaxis_title="Value",
        legend_title="Statistic",
        barmode='group'
    )
    
    return fig

def plot_player_stat_history(player_data, stat='pts'):
    """
    Create a line chart showing a player's statistic over time.
    
    Args:
        player_data (pandas.DataFrame): DataFrame containing player statistics
        stat (str): The statistic to plot (default: 'pts')
    
    Returns:
        plotly.graph_objects.Figure: Line chart of player statistic over time
    """
    # Sort data by date
    player_data = player_data.sort_values('game_date')
    
    # Create figure
    fig = px.line(
        player_data, 
        x='game_date', 
        y=stat,
        title=f"{player_data['player_name'].iloc[0]} - {stat.upper()} Over Time"
    )
    
    # Add rolling average
    window_size = min(5, len(player_data))
    if window_size > 1:
        rolling_avg = player_data[stat].rolling(window=window_size).mean()
        
        fig.add_trace(
            go.Scatter(
                x=player_data['game_date'],
                y=rolling_avg,
                mode='lines',
                name=f'{window_size}-Game Average',
                line=dict(color='red', dash='dash')
            )
        )
    
    # Update layout
    fig.update_layout(
        xaxis_title="Game Date",
        yaxis_title=stat.upper(),
        legend_title="Metric"
    )
    
    return fig

def plot_player_shooting_percentages(player_data):
    """
    Create a chart showing a player's shooting percentages.
    
    Args:
        player_data (pandas.DataFrame): DataFrame containing player statistics
    
    Returns:
        plotly.graph_objects.Figure: Chart of player shooting percentages
    """
    # Compute average percentages
    avg_percentages = player_data[['fg_pct', 'fg3_pct', 'ft_pct']].mean()
    
    # Create labels
    labels = ['Field Goal %', '3-Point %', 'Free Throw %']
    
    # Create figure
    fig = go.Figure()
    
    # Add bar chart
    fig.add_trace(go.Bar(
        x=labels,
        y=avg_percentages.values,
        marker_color=['blue', 'green', 'orange'],
        text=[f'{val:.1%}' for val in avg_percentages.values],
        textposition='auto'
    ))
    
    # Update layout
    fig.update_layout(
        title=f"{player_data['player_name'].iloc[0]} - Shooting Percentages",
        yaxis=dict(
            title='Percentage',
            tickformat='.0%',
            range=[0, 1]
        ),
        showlegend=False
    )
    
    return fig 