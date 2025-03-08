import React, { useState, useEffect, memo, lazy, Suspense } from 'react';
import { Container, Grid, Paper, Typography, Box, Card, CardContent, CardMedia, CircularProgress } from '@mui/material';
import { getDashboardStats } from '../services/api';

// Lazy load the chart component to improve initial load time
const LazyLineChart = lazy(() => import('../components/LineChart'));

// Memoized player card component to prevent unnecessary re-renders
const PlayerCard = memo(({ player, statKey, statLabel }) => (
  <Card sx={{ display: 'flex', mb: 2, height: 100 }} className="player-card">
    <CardMedia
      component="img"
      sx={{ width: 80, objectFit: 'cover', backgroundColor: '#f0f0f0' }}
      image={player.image_url || `https://via.placeholder.com/80x100?text=${player.name.charAt(0)}`}
      alt={player.name}
    />
    <Box sx={{ display: 'flex', flexDirection: 'column', width: '100%' }}>
      <CardContent sx={{ flex: '1 0 auto', py: 1 }}>
        <Typography component="div" variant="h6" noWrap>
          {player.name}
        </Typography>
        <Typography variant="subtitle2" color="text.secondary" component="div">
          {player.team}
        </Typography>
        <Typography variant="body1" color="primary" fontWeight="bold">
          {player[statKey]} {statLabel}
        </Typography>
      </CardContent>
    </Box>
  </Card>
));

// Memoized stats section to prevent unnecessary re-renders
const StatsSection = memo(({ title, players, statKey, statLabel }) => (
  <Grid item xs={12} md={4}>
    <Paper
      sx={{
        p: 2,
        display: 'flex',
        flexDirection: 'column',
        height: 500,
      }}
      elevation={3}
      className="card-hover"
    >
      <Typography variant="h6" gutterBottom>
        {title}
      </Typography>
      {players.map((player) => (
        <PlayerCard 
          key={player.player_id} 
          player={player} 
          statKey={statKey} 
          statLabel={statLabel} 
        />
      ))}
    </Paper>
  </Grid>
));

const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    topScorers: [],
    topRebounders: [],
    topAssists: [],
    recentGames: [],
  });

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        const data = await getDashboardStats();
        setStats(data);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        // Use mock data if API fails
        setStats({
          topScorers: [
            { player_id: 1, name: 'Luka Doncic', team: 'DAL', ppg: 33.9, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/1629029.png' },
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
            { player_id: 15, name: 'Luka Doncic', team: 'DAL', apg: 8.4, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/1629029.png' },
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
        });
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

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
        Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        {/* Top Scorers */}
        <StatsSection 
          title="Top Scorers" 
          players={stats.topScorers} 
          statKey="ppg" 
          statLabel="PPG" 
        />
        
        {/* Top Rebounders */}
        <StatsSection 
          title="Top Rebounders" 
          players={stats.topRebounders} 
          statKey="rpg" 
          statLabel="RPG" 
        />
        
        {/* Top Assists */}
        <StatsSection 
          title="Top Assists" 
          players={stats.topAssists} 
          statKey="apg" 
          statLabel="APG" 
        />
        
        {/* Recent Games Chart */}
        <Grid item xs={12}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              height: 400,
            }}
            elevation={3}
            className="card-hover"
          >
            <Typography variant="h6" gutterBottom>
              Recent Games Performance
            </Typography>
            <Box sx={{ height: 300 }}>
              <Suspense fallback={<CircularProgress />}>
                <LazyLineChart data={stats.recentGames} />
              </Suspense>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard; 