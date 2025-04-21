import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

def plot_team_performance(comparison_data, team1_name, team2_name):
    """
    Create a radar chart comparing two teams or lineups.
    
    Args:
        comparison_data (pandas.DataFrame): DataFrame with comparison statistics
        team1_name (str): Name of the first team/lineup
        team2_name (str): Name of the second team/lineup
    
    Returns:
        plotly.graph_objects.Figure: Radar chart comparing team statistics
    """
    # Get data in the right format for radar chart
    categories = comparison_data['Stat'].tolist()
    team1_values = comparison_data[team1_name].tolist()
    team2_values = comparison_data[team2_name].tolist()
    
    # For radar chart, we need to close the loop by repeating the first value
    categories.append(categories[0])
    team1_values.append(team1_values[0])
    team2_values.append(team2_values[0])
    
    # Create radar chart
    fig = go.Figure()
    
    # Add traces for each team
    fig.add_trace(go.Scatterpolar(
        r=team1_values,
        theta=categories,
        fill='toself',
        name=team1_name,
        line=dict(color='blue')
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=team2_values,
        theta=categories,
        fill='toself',
        name=team2_name,
        line=dict(color='red')
    ))
    
    # Update layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                showticklabels=False
            )
        ),
        showlegend=True,
        title="Team Comparison",
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    return fig

def plot_team_bar_comparison(comparison_data, team1_name, team2_name):
    """
    Create a bar chart comparing two teams or lineups.
    
    Args:
        comparison_data (pandas.DataFrame): DataFrame with comparison statistics
        team1_name (str): Name of the first team/lineup
        team2_name (str): Name of the second team/lineup
    
    Returns:
        plotly.graph_objects.Figure: Bar chart comparing team statistics
    """
    # Prepare data for visualization
    categories = comparison_data['Stat'].tolist()
    team1_values = comparison_data[team1_name].tolist()
    team2_values = comparison_data[team2_name].tolist()
    
    # Create figure
    fig = go.Figure()
    
    # Add traces for each team
    fig.add_trace(go.Bar(
        x=categories,
        y=team1_values,
        name=team1_name,
        marker_color='blue'
    ))
    
    fig.add_trace(go.Bar(
        x=categories,
        y=team2_values,
        name=team2_name,
        marker_color='red'
    ))
    
    # Update layout
    fig.update_layout(
        title="Team Comparison",
        xaxis_title="Statistic",
        yaxis_title="Value",
        legend_title="Team",
        barmode='group'
    )
    
    return fig

def plot_win_probability_chart(home_team, away_team, home_prob):
    """
    Create a gauge chart showing win probability.
    
    Args:
        home_team (str): Name of the home team
        away_team (str): Name of the away team
        home_prob (float): Probability of home team winning (0-1)
    
    Returns:
        plotly.graph_objects.Figure: Gauge chart showing win probability
    """
    # Create figure
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=home_prob * 100,
        title={'text': f"{home_team} vs. {away_team}"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 100], 'color': "gray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 50
            }
        }
    ))
    
    # Update layout
    fig.update_layout(
        title=f"Win Probability: {home_team}",
        annotations=[
            dict(
                x=0.5,
                y=0.25,
                text=f"{home_prob:.1%} chance to win",
                showarrow=False
            )
        ]
    )
    
    return fig

def plot_team_stat_comparison(team_stats, stat='pts'):
    """
    Create a horizontal bar chart comparing all teams on a specific statistic.
    
    Args:
        team_stats (pandas.DataFrame): DataFrame with team statistics
        stat (str): The statistic to compare (default: 'pts')
    
    Returns:
        plotly.graph_objects.Figure: Horizontal bar chart comparing teams
    """
    # Sort teams by the statistic
    sorted_teams = team_stats.sort_values(stat, ascending=False)
    
    # Create figure
    fig = px.bar(
        sorted_teams,
        y='name',
        x=stat,
        orientation='h',
        title=f"NBA Teams Ranked by {stat.upper()}",
        labels={stat: stat.upper(), 'name': 'Team'}
    )
    
    # Update layout
    fig.update_layout(
        yaxis={'categoryorder': 'array', 'categoryarray': sorted_teams['name']}
    )
    
    return fig 