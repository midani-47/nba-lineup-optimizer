import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Button,
  CircularProgress,
  Divider,
  Card,
  CardContent,
  CardMedia,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { getPlayerById } from '../services/api';

const PlayerDetail = () => {
  const { playerId } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [player, setPlayer] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPlayerData = async () => {
      try {
        setLoading(true);
        const data = await getPlayerById(playerId);
        setPlayer(data);
      } catch (error) {
        console.error(`Error fetching player ${playerId}:`, error);
        setError('Failed to load player data. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchPlayerData();
  }, [playerId]);

  const handleGoBack = () => {
    navigate('/players');
  };

  const getPlayerImageUrl = (playerId) => {
    return `https://cdn.nba.com/headshots/nba/latest/1040x760/${playerId}.png`;
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

  if (error) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={handleGoBack}
          sx={{ mb: 2 }}
        >
          Back to Players
        </Button>
        <Paper sx={{ p: 3, textAlign: 'center' }}>
          <Typography variant="h6" color="error">
            {error}
          </Typography>
          <Button
            variant="contained"
            color="primary"
            onClick={() => window.location.reload()}
            sx={{ mt: 2 }}
          >
            Retry
          </Button>
        </Paper>
      </Container>
    );
  }

  if (!player) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={handleGoBack}
          sx={{ mb: 2 }}
        >
          Back to Players
        </Button>
        <Paper sx={{ p: 3, textAlign: 'center' }}>
          <Typography variant="h6">
            Player not found
          </Typography>
        </Paper>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Button
        startIcon={<ArrowBackIcon />}
        onClick={handleGoBack}
        sx={{ mb: 2 }}
      >
        Back to Players
      </Button>
      
      {/* Player Header */}
      <Card sx={{ mb: 4 }}>
        <Grid container>
          <Grid item xs={12} md={4}>
            <CardMedia
              component="img"
              sx={{ height: 300, objectFit: 'contain', backgroundColor: '#f0f0f0' }}
              image={player.image_url || getPlayerImageUrl(player.player_id)}
              alt={player.name}
              onError={(e) => {
                e.target.src = `https://via.placeholder.com/300x300?text=${player.name.charAt(0)}`;
              }}
            />
          </Grid>
          <Grid item xs={12} md={8}>
            <CardContent sx={{ height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
              <Typography variant="h4" component="h1" gutterBottom>
                {player.name}
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={6} md={3}>
                  <Typography variant="body2" color="text.secondary">
                    Team
                  </Typography>
                  <Typography variant="body1" fontWeight="bold">
                    {player.team || 'Free Agent'}
                  </Typography>
                </Grid>
                <Grid item xs={6} md={3}>
                  <Typography variant="body2" color="text.secondary">
                    Position
                  </Typography>
                  <Typography variant="body1" fontWeight="bold">
                    {player.position || 'N/A'}
                  </Typography>
                </Grid>
                <Grid item xs={6} md={3}>
                  <Typography variant="body2" color="text.secondary">
                    Height
                  </Typography>
                  <Typography variant="body1" fontWeight="bold">
                    {player.height || 'N/A'}
                  </Typography>
                </Grid>
                <Grid item xs={6} md={3}>
                  <Typography variant="body2" color="text.secondary">
                    Weight
                  </Typography>
                  <Typography variant="body1" fontWeight="bold">
                    {player.weight ? `${player.weight} lbs` : 'N/A'}
                  </Typography>
                </Grid>
                <Grid item xs={6} md={3}>
                  <Typography variant="body2" color="text.secondary">
                    Age
                  </Typography>
                  <Typography variant="body1" fontWeight="bold">
                    {player.age || 'N/A'}
                  </Typography>
                </Grid>
                <Grid item xs={6} md={3}>
                  <Typography variant="body2" color="text.secondary">
                    Draft
                  </Typography>
                  <Typography variant="body1" fontWeight="bold">
                    {player.draft_year ? `${player.draft_year} (${player.draft_round}/${player.draft_number})` : 'Undrafted'}
                  </Typography>
                </Grid>
                <Grid item xs={6} md={3}>
                  <Typography variant="body2" color="text.secondary">
                    Country
                  </Typography>
                  <Typography variant="body1" fontWeight="bold">
                    {player.country || 'N/A'}
                  </Typography>
                </Grid>
                <Grid item xs={6} md={3}>
                  <Typography variant="body2" color="text.secondary">
                    Experience
                  </Typography>
                  <Typography variant="body1" fontWeight="bold">
                    {player.experience ? `${player.experience} years` : 'Rookie'}
                  </Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Grid>
        </Grid>
      </Card>
      
      {/* Season Stats */}
      <Typography variant="h5" gutterBottom>
        Season Statistics
      </Typography>
      <Paper sx={{ mb: 4, overflow: 'hidden' }}>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
                <TableCell>PPG</TableCell>
                <TableCell>RPG</TableCell>
                <TableCell>APG</TableCell>
                <TableCell>SPG</TableCell>
                <TableCell>BPG</TableCell>
                <TableCell>FG%</TableCell>
                <TableCell>3P%</TableCell>
                <TableCell>FT%</TableCell>
                <TableCell>MPG</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              <TableRow>
                <TableCell>{player.ppg || '0.0'}</TableCell>
                <TableCell>{player.rpg || '0.0'}</TableCell>
                <TableCell>{player.apg || '0.0'}</TableCell>
                <TableCell>{player.spg || '0.0'}</TableCell>
                <TableCell>{player.bpg || '0.0'}</TableCell>
                <TableCell>{player.fg_pct ? `${(player.fg_pct * 100).toFixed(1)}%` : '0.0%'}</TableCell>
                <TableCell>{player.fg3_pct ? `${(player.fg3_pct * 100).toFixed(1)}%` : '0.0%'}</TableCell>
                <TableCell>{player.ft_pct ? `${(player.ft_pct * 100).toFixed(1)}%` : '0.0%'}</TableCell>
                <TableCell>{player.mpg || '0.0'}</TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
      
      {/* Advanced Stats */}
      <Typography variant="h5" gutterBottom>
        Advanced Statistics
      </Typography>
      <Paper sx={{ mb: 4, overflow: 'hidden' }}>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
                <TableCell>PER</TableCell>
                <TableCell>TS%</TableCell>
                <TableCell>USG%</TableCell>
                <TableCell>ORTG</TableCell>
                <TableCell>DRTG</TableCell>
                <TableCell>WS</TableCell>
                <TableCell>BPM</TableCell>
                <TableCell>VORP</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              <TableRow>
                <TableCell>{player.per || 'N/A'}</TableCell>
                <TableCell>{player.ts_pct ? `${(player.ts_pct * 100).toFixed(1)}%` : 'N/A'}</TableCell>
                <TableCell>{player.usg_pct ? `${(player.usg_pct * 100).toFixed(1)}%` : 'N/A'}</TableCell>
                <TableCell>{player.ortg || 'N/A'}</TableCell>
                <TableCell>{player.drtg || 'N/A'}</TableCell>
                <TableCell>{player.ws || 'N/A'}</TableCell>
                <TableCell>{player.bpm || 'N/A'}</TableCell>
                <TableCell>{player.vorp || 'N/A'}</TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
      
      {/* Add to Lineup Button */}
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <Button
          variant="contained"
          color="primary"
          size="large"
          onClick={() => navigate('/lineup-builder', { state: { selectedPlayer: player } })}
        >
          Add to Lineup
        </Button>
      </Box>
    </Container>
  );
};

export default PlayerDetail; 