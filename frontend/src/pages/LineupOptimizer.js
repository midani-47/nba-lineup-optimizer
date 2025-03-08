import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Button,
  CircularProgress,
  Divider,
  Card,
  CardContent,
  CardMedia,
  Radio,
  RadioGroup,
  FormControlLabel,
  FormLabel,
  Snackbar,
  Alert,
} from '@mui/material';
import AutoFixHighIcon from '@mui/icons-material/AutoFixHigh';
import SaveIcon from '@mui/icons-material/Save';
import { getLineups, getLineupById, optimizeLineup, createLineup } from '../services/api';

const LineupOptimizer = () => {
  const [loading, setLoading] = useState(true);
  const [lineups, setLineups] = useState([]);
  const [selectedLineupId, setSelectedLineupId] = useState('');
  const [selectedLineup, setSelectedLineup] = useState(null);
  const [optimizationStrategy, setOptimizationStrategy] = useState('balanced');
  const [optimizedLineup, setOptimizedLineup] = useState(null);
  const [optimizing, setOptimizing] = useState(false);
  const [optimizedLineupName, setOptimizedLineupName] = useState('');
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'info',
  });

  useEffect(() => {
    const fetchLineups = async () => {
      try {
        setLoading(true);
        const data = await getLineups();
        setLineups(data);
      } catch (error) {
        console.error('Error fetching lineups:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchLineups();
  }, []);

  const handleLineupChange = async (event) => {
    const lineupId = event.target.value;
    setSelectedLineupId(lineupId);
    setOptimizedLineup(null);
    
    if (lineupId) {
      try {
        const data = await getLineupById(lineupId);
        setSelectedLineup(data);
        setOptimizedLineupName(`${data.name} (Optimized - ${optimizationStrategy.charAt(0).toUpperCase() + optimizationStrategy.slice(1)})`);
      } catch (error) {
        console.error(`Error fetching lineup ${lineupId}:`, error);
      }
    } else {
      setSelectedLineup(null);
      setOptimizedLineupName('');
    }
  };

  const handleStrategyChange = (event) => {
    const strategy = event.target.value;
    setOptimizationStrategy(strategy);
    
    if (selectedLineup) {
      setOptimizedLineupName(`${selectedLineup.name} (Optimized - ${strategy.charAt(0).toUpperCase() + strategy.slice(1)})`);
    }
  };

  const handleOptimize = async () => {
    if (!selectedLineupId) return;

    try {
      setOptimizing(true);
      const data = await optimizeLineup(selectedLineupId, optimizationStrategy);
      setOptimizedLineup(data);
    } catch (error) {
      console.error(`Error optimizing lineup ${selectedLineupId}:`, error);
      setSnackbar({
        open: true,
        message: 'Failed to optimize lineup. Please try again.',
        severity: 'error',
      });
    } finally {
      setOptimizing(false);
    }
  };

  const handleSaveOptimizedLineup = async () => {
    if (!optimizedLineup || !optimizedLineupName.trim()) {
      setSnackbar({
        open: true,
        message: 'Please enter a name for the optimized lineup.',
        severity: 'warning',
      });
      return;
    }

    try {
      const lineupData = {
        name: optimizedLineupName,
        players: optimizedLineup.players.map(player => player.player_id),
      };
      
      await createLineup(lineupData);
      
      setSnackbar({
        open: true,
        message: 'Optimized lineup saved successfully!',
        severity: 'success',
      });
      
      // Refresh lineups
      const data = await getLineups();
      setLineups(data);
    } catch (error) {
      console.error('Error saving optimized lineup:', error);
      setSnackbar({
        open: true,
        message: 'Failed to save optimized lineup. Please try again.',
        severity: 'error',
      });
    }
  };

  const handleCloseSnackbar = () => {
    setSnackbar({
      ...snackbar,
      open: false,
    });
  };

  const getPlayerImageUrl = (playerId) => {
    return `https://cdn.nba.com/headshots/nba/latest/1040x760/${playerId}.png`;
  };

  const getStrategyDescription = () => {
    switch (optimizationStrategy) {
      case 'offense':
        return 'Prioritizes scoring and offensive efficiency. Optimizes for players with high PPG, APG, and shooting percentages.';
      case 'defense':
        return 'Focuses on defensive capabilities. Optimizes for players with high SPG, BPG, and RPG.';
      case 'balanced':
      default:
        return 'Balances offensive and defensive capabilities. Considers all statistical categories equally.';
    }
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
        Lineup Optimizer
      </Typography>
      
      <Paper sx={{ p: 3, mb: 4 }} elevation={3}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <FormControl fullWidth variant="outlined">
              <InputLabel>Select Lineup to Optimize</InputLabel>
              <Select
                value={selectedLineupId}
                onChange={handleLineupChange}
                label="Select Lineup to Optimize"
              >
                <MenuItem value="">
                  <em>Select a lineup</em>
                </MenuItem>
                {lineups.map((lineup) => (
                  <MenuItem key={lineup.id} value={lineup.id}>
                    {lineup.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <FormControl component="fieldset">
              <FormLabel component="legend">Optimization Strategy</FormLabel>
              <RadioGroup
                row
                value={optimizationStrategy}
                onChange={handleStrategyChange}
              >
                <FormControlLabel value="balanced" control={<Radio />} label="Balanced" />
                <FormControlLabel value="offense" control={<Radio />} label="Offense" />
                <FormControlLabel value="defense" control={<Radio />} label="Defense" />
              </RadioGroup>
            </FormControl>
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              {getStrategyDescription()}
            </Typography>
          </Grid>
          
          <Grid item xs={12} sx={{ textAlign: 'center', mt: 2 }}>
            <Button
              variant="contained"
              color="primary"
              startIcon={<AutoFixHighIcon />}
              onClick={handleOptimize}
              disabled={!selectedLineupId || optimizing}
              size="large"
            >
              {optimizing ? 'Optimizing...' : 'Optimize Lineup'}
            </Button>
          </Grid>
        </Grid>
      </Paper>
      
      {optimizing ? (
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="40vh">
          <CircularProgress />
        </Box>
      ) : selectedLineup && optimizedLineup ? (
        <>
          <Grid container spacing={3}>
            {/* Original Lineup */}
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 3, height: '100%' }} elevation={3}>
                <Typography variant="h6" gutterBottom>
                  Original Lineup: {selectedLineup.name}
                </Typography>
                <Divider sx={{ mb: 2 }} />
                
                {selectedLineup.players.map((player) => (
                  <Card key={player.player_id} sx={{ mb: 2, display: 'flex' }}>
                    <CardMedia
                      component="img"
                      sx={{ width: 70, objectFit: 'cover' }}
                      image={player.image_url || getPlayerImageUrl(player.player_id)}
                      alt={player.name}
                      onError={(e) => {
                        e.target.src = `https://via.placeholder.com/70x70?text=${player.name.charAt(0)}`;
                      }}
                    />
                    <Box sx={{ display: 'flex', flexDirection: 'column', width: '100%' }}>
                      <CardContent sx={{ flex: '1 0 auto', py: 1 }}>
                        <Typography component="div" variant="subtitle1">
                          {player.name}
                        </Typography>
                        <Typography variant="body2" color="text.secondary" component="div">
                          {player.position || 'N/A'} | {player.team || 'Free Agent'}
                        </Typography>
                        <Typography variant="body2" component="div">
                          {player.ppg || '0'} PPG, {player.rpg || '0'} RPG, {player.apg || '0'} APG
                        </Typography>
                      </CardContent>
                    </Box>
                  </Card>
                ))}
                
                <Box sx={{ mt: 2 }}>
                  <Typography variant="subtitle1" gutterBottom>
                    Team Statistics
                  </Typography>
                  <Grid container spacing={1}>
                    <Grid item xs={4}>
                      <Typography variant="body2" color="text.secondary">
                        PPG
                      </Typography>
                      <Typography variant="body1" fontWeight="bold">
                        {selectedLineup.total_ppg?.toFixed(1) || '0.0'}
                      </Typography>
                    </Grid>
                    <Grid item xs={4}>
                      <Typography variant="body2" color="text.secondary">
                        RPG
                      </Typography>
                      <Typography variant="body1" fontWeight="bold">
                        {selectedLineup.total_rpg?.toFixed(1) || '0.0'}
                      </Typography>
                    </Grid>
                    <Grid item xs={4}>
                      <Typography variant="body2" color="text.secondary">
                        APG
                      </Typography>
                      <Typography variant="body1" fontWeight="bold">
                        {selectedLineup.total_apg?.toFixed(1) || '0.0'}
                      </Typography>
                    </Grid>
                    <Grid item xs={4}>
                      <Typography variant="body2" color="text.secondary">
                        SPG
                      </Typography>
                      <Typography variant="body1" fontWeight="bold">
                        {selectedLineup.total_spg?.toFixed(1) || '0.0'}
                      </Typography>
                    </Grid>
                    <Grid item xs={4}>
                      <Typography variant="body2" color="text.secondary">
                        BPG
                      </Typography>
                      <Typography variant="body1" fontWeight="bold">
                        {selectedLineup.total_bpg?.toFixed(1) || '0.0'}
                      </Typography>
                    </Grid>
                    <Grid item xs={4}>
                      <Typography variant="body2" color="text.secondary">
                        FG%
                      </Typography>
                      <Typography variant="body1" fontWeight="bold">
                        {(selectedLineup.total_fg_pct * 100)?.toFixed(1) || '0.0'}%
                      </Typography>
                    </Grid>
                  </Grid>
                </Box>
              </Paper>
            </Grid>
            
            {/* Optimized Lineup */}
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 3, height: '100%' }} elevation={3}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                  <Typography variant="h6">
                    Optimized Lineup ({optimizationStrategy.charAt(0).toUpperCase() + optimizationStrategy.slice(1)})
                  </Typography>
                  <AutoFixHighIcon color="primary" />
                </Box>
                <Divider sx={{ mb: 2 }} />
                
                {optimizedLineup.players.map((player) => (
                  <Card key={player.player_id} sx={{ mb: 2, display: 'flex' }}>
                    <CardMedia
                      component="img"
                      sx={{ width: 70, objectFit: 'cover' }}
                      image={player.image_url || getPlayerImageUrl(player.player_id)}
                      alt={player.name}
                      onError={(e) => {
                        e.target.src = `https://via.placeholder.com/70x70?text=${player.name.charAt(0)}`;
                      }}
                    />
                    <Box sx={{ display: 'flex', flexDirection: 'column', width: '100%' }}>
                      <CardContent sx={{ flex: '1 0 auto', py: 1 }}>
                        <Typography component="div" variant="subtitle1">
                          {player.name}
                        </Typography>
                        <Typography variant="body2" color="text.secondary" component="div">
                          {player.position || 'N/A'} | {player.team || 'Free Agent'}
                        </Typography>
                        <Typography variant="body2" component="div">
                          {player.ppg || '0'} PPG, {player.rpg || '0'} RPG, {player.apg || '0'} APG
                        </Typography>
                      </CardContent>
                    </Box>
                  </Card>
                ))}
                
                <Box sx={{ mt: 2 }}>
                  <Typography variant="subtitle1" gutterBottom>
                    Team Statistics
                  </Typography>
                  <Grid container spacing={1}>
                    <Grid item xs={4}>
                      <Typography variant="body2" color="text.secondary">
                        PPG
                      </Typography>
                      <Typography variant="body1" fontWeight="bold">
                        {optimizedLineup.total_ppg?.toFixed(1) || '0.0'}
                      </Typography>
                    </Grid>
                    <Grid item xs={4}>
                      <Typography variant="body2" color="text.secondary">
                        RPG
                      </Typography>
                      <Typography variant="body1" fontWeight="bold">
                        {optimizedLineup.total_rpg?.toFixed(1) || '0.0'}
                      </Typography>
                    </Grid>
                    <Grid item xs={4}>
                      <Typography variant="body2" color="text.secondary">
                        APG
                      </Typography>
                      <Typography variant="body1" fontWeight="bold">
                        {optimizedLineup.total_apg?.toFixed(1) || '0.0'}
                      </Typography>
                    </Grid>
                    <Grid item xs={4}>
                      <Typography variant="body2" color="text.secondary">
                        SPG
                      </Typography>
                      <Typography variant="body1" fontWeight="bold">
                        {optimizedLineup.total_spg?.toFixed(1) || '0.0'}
                      </Typography>
                    </Grid>
                    <Grid item xs={4}>
                      <Typography variant="body2" color="text.secondary">
                        BPG
                      </Typography>
                      <Typography variant="body1" fontWeight="bold">
                        {optimizedLineup.total_bpg?.toFixed(1) || '0.0'}
                      </Typography>
                    </Grid>
                    <Grid item xs={4}>
                      <Typography variant="body2" color="text.secondary">
                        FG%
                      </Typography>
                      <Typography variant="body1" fontWeight="bold">
                        {(optimizedLineup.total_fg_pct * 100)?.toFixed(1) || '0.0'}%
                      </Typography>
                    </Grid>
                  </Grid>
                </Box>
              </Paper>
            </Grid>
          </Grid>
          
          {/* Save Optimized Lineup */}
          <Paper sx={{ p: 3, mt: 3 }} elevation={3}>
            <Typography variant="h6" gutterBottom>
              Save Optimized Lineup
            </Typography>
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={12} sm={8}>
                <FormControl fullWidth variant="outlined">
                  <InputLabel>Lineup Name</InputLabel>
                  <Select
                    value={optimizedLineupName}
                    onChange={(e) => setOptimizedLineupName(e.target.value)}
                    label="Lineup Name"
                    inputProps={{ maxLength: 50 }}
                  >
                    <MenuItem value={`${selectedLineup.name} (Optimized - ${optimizationStrategy.charAt(0).toUpperCase() + optimizationStrategy.slice(1)})`}>
                      {`${selectedLineup.name} (Optimized - ${optimizationStrategy.charAt(0).toUpperCase() + optimizationStrategy.slice(1)})`}
                    </MenuItem>
                    <MenuItem value={`${selectedLineup.name} (${optimizationStrategy.charAt(0).toUpperCase() + optimizationStrategy.slice(1)})`}>
                      {`${selectedLineup.name} (${optimizationStrategy.charAt(0).toUpperCase() + optimizationStrategy.slice(1)})`}
                    </MenuItem>
                    <MenuItem value={`Optimized ${selectedLineup.name}`}>
                      {`Optimized ${selectedLineup.name}`}
                    </MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={4}>
                <Button
                  variant="contained"
                  color="primary"
                  startIcon={<SaveIcon />}
                  onClick={handleSaveOptimizedLineup}
                  disabled={!optimizedLineupName.trim()}
                  fullWidth
                >
                  Save Optimized Lineup
                </Button>
              </Grid>
            </Grid>
          </Paper>
        </>
      ) : selectedLineup ? (
        <Box sx={{ textAlign: 'center', py: 8 }}>
          <Typography variant="h6" color="text.secondary">
            Click "Optimize Lineup" to generate an optimized version
          </Typography>
        </Box>
      ) : (
        <Box sx={{ textAlign: 'center', py: 8 }}>
          <Typography variant="h6" color="text.secondary">
            Select a lineup to optimize
          </Typography>
        </Box>
      )}
      
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={handleCloseSnackbar} severity={snackbar.severity} sx={{ width: '100%' }}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default LineupOptimizer; 