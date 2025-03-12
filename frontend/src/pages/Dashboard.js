import React, { useState, useEffect, memo, lazy, Suspense } from 'react';
import { 
  Container, 
  Grid, 
  Paper, 
  Typography, 
  Box, 
  Card, 
  CardContent, 
  CardMedia, 
  CircularProgress, 
  Alert, 
  Snackbar,
  Tabs,
  Tab,
  Divider,
  Button,
  Chip
} from '@mui/material';
import { getDashboardStats } from '../services/api';
import { useNavigate } from 'react-router-dom';

// Lazy load the chart components to improve initial load time
const LazyLineChart = lazy(() => import('../components/LineChart'));
const LazyBarChart = lazy(() => import('../components/BarChart'));

// Memoized player card component to prevent unnecessary re-renders
const PlayerCard = memo(({ player, statKey, statLabel, onClick }) => {
  if (!player || typeof player !== 'object') {
    return null;
  }

  return (
    <Card 
      sx={{ 
        display: 'flex', 
        mb: 2, 
        height: 100,
        cursor: 'pointer',
        transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
        '&:hover': {
          transform: 'translateY(-3px)',
          boxShadow: '0 8px 16px rgba(0,0,0,0.1)',
        },
      }} 
      className="player-card"
      onClick={() => onClick(player.player_id)}
    >
      <CardMedia
        component="img"
        sx={{ width: 80, objectFit: 'cover', backgroundColor: '#f0f0f0' }}
        image={player.image_url || `https://cdn.nba.com/headshots/nba/latest/1040x760/${player.player_id}.png`}
        alt={player.name || 'Player'}
        onError={(e) => {
          e.target.src = `https://via.placeholder.com/80x100?text=${player.name ? player.name.charAt(0) : 'N/A'}`;
        }}
      />
      <Box sx={{ display: 'flex', flexDirection: 'column', width: '100%' }}>
        <CardContent sx={{ flex: '1 0 auto', py: 1 }}>
          <Typography component="div" variant="h6" noWrap>
            {player.name || 'Unknown Player'}
          </Typography>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Typography variant="subtitle2" color="text.secondary" component="div">
              {player.team || 'N/A'}
            </Typography>
            <Chip 
              label={`${player[statKey] || '0'} ${statLabel}`} 
              color="primary" 
              size="small"
              sx={{ fontWeight: 'bold' }}
            />
          </Box>
        </CardContent>
      </Box>
    </Card>
  );
});

// Memoized stats section to prevent unnecessary re-renders
const StatsSection = memo(({ title, players, statKey, statLabel, onPlayerClick }) => {
  if (!Array.isArray(players)) {
    return (
      <Grid item xs={12} md={4}>
        <Paper
          sx={{
            p: 2,
            display: 'flex',
            flexDirection: 'column',
            height: 500,
            justifyContent: 'center',
            alignItems: 'center'
          }}
          elevation={3}
          className="card-hover"
        >
          <Typography variant="h6" gutterBottom>
            {title}
          </Typography>
          <Alert severity="warning">No data available</Alert>
        </Paper>
      </Grid>
    );
  }

  return (
    <Grid item xs={12} md={4}>
      <Paper
        sx={{
          p: 2,
          display: 'flex',
          flexDirection: 'column',
          height: 500,
          overflow: 'auto'
        }}
        elevation={3}
        className="card-hover"
      >
        <Typography variant="h6" gutterBottom>
          {title}
        </Typography>
        {players.length > 0 ? (
          players.map((player) => (
            <PlayerCard 
              key={player.player_id} 
              player={player} 
              statKey={statKey} 
              statLabel={statLabel}
              onClick={(playerId) => onPlayerClick(playerId, 'performances')}
            />
          ))
        ) : (
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
            <Typography variant="body1" color="text.secondary">
              No players available
            </Typography>
          </Box>
        )}
      </Paper>
    </Grid>
  );
});

const Performances = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [chartTab, setChartTab] = useState(0);
  const [stats, setStats] = useState({
    topScorers: [],
    topRebounders: [],
    topAssists: [],
    recentGames: [],
    topPerformances: []
  });

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        const data = await getDashboardStats();
        
        // Validate the data structure
        if (data && typeof data === 'object') {
          // Ensure all expected properties exist with default values if missing
          const validatedData = {
            topScorers: Array.isArray(data.topScorers) ? data.topScorers : [],
            topRebounders: Array.isArray(data.topRebounders) ? data.topRebounders : [],
            topAssists: Array.isArray(data.topAssists) ? data.topAssists : [],
            recentGames: Array.isArray(data.recentGames) ? data.recentGames : [],
            // Add new top performances data
            topPerformances: Array.isArray(data.topPerformances) ? data.topPerformances : [
              { player_id: 1, name: 'Luka Doncic', team: 'LAL', points: 45, rebounds: 12, assists: 8, date: '2023-11-15', opponent: 'LAC' },
              { player_id: 2, name: 'Joel Embiid', team: 'PHI', points: 42, rebounds: 15, assists: 5, date: '2023-11-14', opponent: 'DET' },
              { player_id: 3, name: 'Nikola Jokic', team: 'DEN', points: 35, rebounds: 14, assists: 12, date: '2023-11-13', opponent: 'NOP' },
              { player_id: 4, name: 'LeBron James', team: 'LAL', points: 38, rebounds: 9, assists: 12, date: '2023-11-12', opponent: 'PHX' },
              { player_id: 5, name: 'Giannis Antetokounmpo', team: 'MIL', points: 40, rebounds: 16, assists: 7, date: '2023-11-11', opponent: 'BKN' },
            ]
          };
          
          setStats(validatedData);
        } else {
          console.error('Invalid data format received:', data);
          setError('Failed to load performance data. Please try again.');
          // Use mock data as fallback
          setDefaultMockData();
        }
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        setError('Error loading performance data. Please try refreshing the page.');
        // Use mock data if API fails
        setDefaultMockData();
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const setDefaultMockData = () => {
        setStats({
          topScorers: [
            { player_id: 1, name: 'Luka Doncic', team: 'LAL', ppg: 33.9, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/1629029.png' },
            { player_id: 2, name: 'Joel Embiid', team: 'PHI', ppg: 33.1, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/203954.png' },
            { player_id: 3, name: 'Kevin Durant', team: 'PHX', ppg: 29.1, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/201142.png' },
            { player_id: 4, name: 'LeBron James', team: 'LAL', ppg: 28.9, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/2544.png' },
            { player_id: 5, name: 'Trae Young', team: 'ATL', ppg: 28.4, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/1629027.png' },
          ],
          topRebounders: [
            { player_id: 6, name: 'Domantas Sabonis', team: 'SAC', rpg: 13.7, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/1627734.png' },
            { player_id: 7, name: 'Rudy Gobert', team: 'MIN', rpg: 12.9, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/203497.png' },
            { player_id: 8, name: 'Nikola Jokic', team: 'DEN', rpg: 12.4, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/203999.png' },
            { player_id: 9, name: 'Giannis Antetokounmpo', team: 'MIL', rpg: 11.5, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/203507.png' },
            { player_id: 10, name: 'Anthony Davis', team: 'LAL', rpg: 11.3, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/203076.png' },
          ],
          topAssists: [
            { player_id: 11, name: 'Tyrese Haliburton', team: 'IND', apg: 10.9, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/1630169.png' },
            { player_id: 12, name: 'Trae Young', team: 'ATL', apg: 10.8, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/1629027.png' },
            { player_id: 13, name: 'Nikola Jokic', team: 'DEN', apg: 9.0, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/203999.png' },
            { player_id: 14, name: 'James Harden', team: 'LAC', apg: 8.5, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/201935.png' },
            { player_id: 15, name: 'Luka Doncic', team: 'LAL', apg: 8.4, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/1629029.png' },
          ],
          recentGames: [
            {
              id: 'Points',
              data: [
                { x: 'Game 1', y: 105 },
                { x: 'Game 2', y: 118 },
                { x: 'Game 3', y: 98 },
                { x: 'Game 4', y: 112 },
                { x: 'Game 5', y: 124 },
              ],
            },
            {
              id: 'Assists',
              data: [
                { x: 'Game 1', y: 24 },
                { x: 'Game 2', y: 28 },
                { x: 'Game 3', y: 19 },
                { x: 'Game 4', y: 26 },
                { x: 'Game 5', y: 30 },
              ],
            },
            {
              id: 'Rebounds',
              data: [
                { x: 'Game 1', y: 42 },
                { x: 'Game 2', y: 45 },
                { x: 'Game 3', y: 38 },
                { x: 'Game 4', y: 44 },
                { x: 'Game 5', y: 47 },
              ],
            },
          ],
      topPerformances: [
        { player_id: 1, name: 'Luka Doncic', team: 'LAL', points: 45, rebounds: 12, assists: 8, date: '2023-11-15', opponent: 'LAC' },
        { player_id: 2, name: 'Joel Embiid', team: 'PHI', points: 42, rebounds: 15, assists: 5, date: '2023-11-14', opponent: 'DET' },
        { player_id: 3, name: 'Nikola Jokic', team: 'DEN', points: 35, rebounds: 14, assists: 12, date: '2023-11-13', opponent: 'NOP' },
        { player_id: 4, name: 'LeBron James', team: 'LAL', points: 38, rebounds: 9, assists: 12, date: '2023-11-12', opponent: 'PHX' },
        { player_id: 5, name: 'Giannis Antetokounmpo', team: 'MIL', points: 40, rebounds: 16, assists: 7, date: '2023-11-11', opponent: 'BKN' },
      ]
    });
  };

  const handleCloseError = () => {
    setError(null);
  };

  const handleChartTabChange = (event, newValue) => {
    setChartTab(newValue);
  };

  const handlePlayerClick = (playerId, source = 'players') => {
    navigate(`/players/${playerId}`, { state: { from: source } });
  };

  // Prepare data for top performances bar chart
  const getTopPerformancesChartData = () => {
    if (!Array.isArray(stats.topPerformances) || stats.topPerformances.length === 0) {
      return [];
    }

    return [
      {
        id: 'Points',
        data: stats.topPerformances.map(perf => ({
          x: perf.name ? perf.name.split(' ')[1] || perf.name : 'Unknown',
          y: perf.points || 0
        }))
      },
      {
        id: 'Rebounds',
        data: stats.topPerformances.map(perf => ({
          x: perf.name ? perf.name.split(' ')[1] || perf.name : 'Unknown',
          y: perf.rebounds || 0
        }))
      },
      {
        id: 'Assists',
        data: stats.topPerformances.map(perf => ({
          x: perf.name ? perf.name.split(' ')[1] || perf.name : 'Unknown',
          y: perf.assists || 0
        }))
      }
    ];
  };

  // Render the chart section with improved chart
  const renderChartSection = () => {
    if (!Array.isArray(stats.recentGames) || stats.recentGames.length === 0) {
      return (
        <Paper
          sx={{
            p: 3,
            display: 'flex',
            flexDirection: 'column',
            height: 400,
            justifyContent: 'center',
            alignItems: 'center'
          }}
          elevation={3}
        >
          <Alert severity="info">No recent game data available</Alert>
        </Paper>
      );
    }

    return (
      <Box>
        {/* Bar Chart */}
        <Paper
          sx={{
            p: 3,
            display: 'flex',
            flexDirection: 'column',
            height: 400,
            mb: 4
          }}
          elevation={3}
        >
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6">
              Team Performance - Bar Chart
            </Typography>
          </Box>
          
          <Box sx={{ height: 300, mt: 2 }}>
            <Suspense fallback={<Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}><CircularProgress /></Box>}>
              <LazyBarChart 
                data={stats.recentGames.map(series => ({
                  ...series,
                  data: series.data.map(point => ({
                    ...point,
                    indexValue: point.x,
                    value: point.y
                  }))
                }))}
                keys={['value']}
                indexBy="indexValue"
                title="Team Stats by Game"
                tooltipFormat={(value) => `${value}`}
              />
            </Suspense>
          </Box>
          
          {/* Chart Legend and Explanation */}
          {/*<Box sx={{ mt: 2, display: 'flex', justifyContent: 'center', flexWrap: 'wrap', gap: 2 }}>
            {stats.recentGames.map((series, index) => (
              <Chip 
                key={index}
                label={series.id}
                sx={{ 
                  backgroundColor: index === 0 ? '#ff6d00' : index === 1 ? '#2196f3' : '#4caf50',
                  color: 'white',
                  fontWeight: 'bold'
                }}
              />
            ))}
          </Box>*/}
        </Paper>
        
        {/* Line Chart */}
        <Paper
          sx={{
            p: 3,
            display: 'flex',
            flexDirection: 'column',
            height: 400,
            mb: 4
          }}
          elevation={3}
        >
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6">
              Team Performance - Line Chart
          </Typography>
          </Box>
          
          <Box sx={{ height: 300, mt: 2 }}>
            <Suspense fallback={<Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}><CircularProgress /></Box>}>
              <LazyLineChart 
                data={stats.recentGames}
                xLegend="Game"
                yLegend="Value"
                title="Team Stats by Game"
                tooltipTitle="Game Performance"
                tooltipFormat={(value) => `${value}`}
              />
            </Suspense>
          </Box>
          
          {/* Chart Legend and Explanation */}
{/*          <Box sx={{ mt: 2, display: 'flex', justifyContent: 'center', flexWrap: 'wrap', gap: 2 }}>
            {stats.recentGames.map((series, index) => (
              <Chip 
                key={index}
                label={series.id}
                sx={{ 
                  backgroundColor: index === 0 ? '#ff6d00' : index === 1 ? '#2196f3' : '#4caf50',
                  color: 'white',
                  fontWeight: 'bold'
                }}
              />
            ))}
          </Box>*/}
        </Paper>
        
        <Typography variant="body2" color="text.secondary" sx={{ mb: 4, textAlign: 'center' }}>
          These charts show the team's performance metrics over the last 5 games. 
          Points represent scoring efficiency, Assists show team playmaking, and Rebounds indicate defensive presence.
          </Typography>
      </Box>
  );
  };

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom className="page-title">
        Performance Dashboard
      </Typography>
      
      {/* Top Performers */}
      <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
        Top Performers
      </Typography>
      <Grid container spacing={3}>
        <StatsSection 
          title="Top Scorers" 
          players={stats.topScorers} 
          statKey="ppg" 
          statLabel="PPG"
          onPlayerClick={handlePlayerClick}
        />
        <StatsSection 
          title="Top Rebounders" 
          players={stats.topRebounders} 
          statKey="rpg" 
          statLabel="RPG"
          onPlayerClick={handlePlayerClick}
        />
        <StatsSection 
          title="Top Playmakers" 
          players={stats.topAssists} 
          statKey="apg" 
          statLabel="APG"
          onPlayerClick={handlePlayerClick}
        />
        </Grid>
        
        {/* Recent Games Chart */}
      <Typography variant="h5" gutterBottom sx={{ mt: 4, mb: 2 }}>
        Recent Team Performance
      </Typography>
      {renderChartSection()}
      
      {/* Top Individual Performances */}
      <Typography variant="h5" gutterBottom sx={{ mt: 6 }}>
        Top Individual Performances
      </Typography>
      <Grid container spacing={3}>
        {Array.isArray(stats.topPerformances) && stats.topPerformances.length > 0 ? (
          stats.topPerformances.map((performance, index) => (
            <Grid item xs={12} sm={6} md={4} key={index}>
              <Card 
            sx={{
                  height: '100%',
                  cursor: 'pointer',
                  transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
                  '&:hover': {
                    transform: 'translateY(-5px)',
                    boxShadow: '0 8px 16px rgba(0,0,0,0.1)',
                  },
                }}
                onClick={() => handlePlayerClick(performance.player_id, 'performances')}
              >
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <CardMedia
                      component="img"
                      sx={{ width: 60, height: 60, borderRadius: '50%', mr: 2, objectFit: 'cover' }}
                      image={performance.image_url || `https://cdn.nba.com/headshots/nba/latest/260x190/${performance.player_id}.png`}
                      alt={performance.name}
                      onError={(e) => {
                        e.target.src = `https://via.placeholder.com/60x60/1a428a/ffffff?text=NBA`;
                      }}
                    />
                    <Box>
                      <Typography variant="h6" component="div">
                        {performance.name}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {performance.team} vs {performance.opponent} • {performance.date}
                      </Typography>
                    </Box>
                  </Box>
                  <Box sx={{ display: 'flex', justifyContent: 'space-around', mt: 2 }}>
                    <Box sx={{ textAlign: 'center' }}>
                      <Typography variant="h5" color="primary">
                        {performance.points}
                      </Typography>
                      <Typography variant="body2">PTS</Typography>
                    </Box>
                    <Box sx={{ textAlign: 'center' }}>
                      <Typography variant="h5" color="primary">
                        {performance.rebounds}
                      </Typography>
                      <Typography variant="body2">REB</Typography>
                    </Box>
                    <Box sx={{ textAlign: 'center' }}>
                      <Typography variant="h5" color="primary">
                        {performance.assists}
                      </Typography>
                      <Typography variant="body2">AST</Typography>
                    </Box>
            </Box>
                </CardContent>
              </Card>
            </Grid>
          ))
        ) : (
          <Grid item xs={12}>
            <Paper sx={{ p: 3, textAlign: 'center' }}>
              <Typography variant="body1">No top performances available</Typography>
          </Paper>
        </Grid>
        )}
      </Grid>
      
      {/* Error Snackbar */}
      <Snackbar open={!!error} autoHideDuration={6000} onClose={() => setError(null)}>
        <Alert onClose={() => setError(null)} severity="error" sx={{ width: '100%' }}>
          {error}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default Performances; 