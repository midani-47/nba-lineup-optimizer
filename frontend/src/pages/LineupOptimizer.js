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
        console.log('LineupOptimizer: Fetching lineups...');
        const data = await getLineups();
        // Ensure lineups is always an array
        if (Array.isArray(data)) {
          console.log('LineupOptimizer: Lineups fetched successfully:', data.length);
          setLineups(data);
        } else {
          console.error('Expected lineups to be an array but got:', data);
          setLineups([]);
          setSnackbar({
            open: true,
            message: 'Error loading lineups. Please try again.',
            severity: 'error',
          });
        }
      } catch (error) {
        console.error('Error fetching lineups:', error);
        setLineups([]);
        setSnackbar({
          open: true,
          message: 'Failed to load lineups. Please try again.',
          severity: 'error',
        });
      } finally {
        setLoading(false);
      }
    };

    fetchLineups();
  }, []);

  // Add a function to refresh lineups
  const refreshLineups = async () => {
    try {
      console.log('LineupOptimizer: Refreshing lineups...');
      const data = await getLineups();
      if (Array.isArray(data)) {
        console.log('LineupOptimizer: Lineups refreshed successfully:', data.length);
        setLineups(data);
      }
    } catch (error) {
      console.error('Error refreshing lineups:', error);
    }
  };

  const handleLineupChange = async (event) => {
    const lineupId = event.target.value;
    setSelectedLineupId(lineupId);
    setOptimizedLineup(null);
    
    if (lineupId) {
      try {
        console.log(`LineupOptimizer: Fetching lineup details for ID ${lineupId}`);
        const data = await getLineupById(lineupId);
        if (data && data.players && Array.isArray(data.players)) {
          console.log('LineupOptimizer: Lineup details fetched successfully:', data);
          setSelectedLineup(data);
          setOptimizedLineupName(`${data.name} (Optimized - ${optimizationStrategy.charAt(0).toUpperCase() + optimizationStrategy.slice(1)})`);
        } else {
          console.error('Invalid lineup data:', data);
          setSnackbar({
            open: true,
            message: 'Error loading lineup details. Please try another lineup.',
            severity: 'error',
          });
        }
      } catch (error) {
        console.error(`Error fetching lineup ${lineupId}:`, error);
        setSnackbar({
          open: true,
          message: 'Failed to load lineup details. Please try again.',
          severity: 'error',
        });
      }
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
    if (!selectedLineupId) {
      setSnackbar({
        open: true,
        message: 'Please select a lineup to optimize',
        severity: 'warning',
      });
      return;
    }
    
    try {
      setOptimizing(true);
      const optimizedData = await optimizeLineup(selectedLineupId, optimizationStrategy);
      
      if (optimizedData && optimizedData.players && Array.isArray(optimizedData.players)) {
        setOptimizedLineup(optimizedData);
        setOptimizedLineupName(optimizedData.name || `${selectedLineup.name} (Optimized - ${optimizationStrategy.charAt(0).toUpperCase() + optimizationStrategy.slice(1)})`);
        setSnackbar({
          open: true,
          message: 'Lineup optimized successfully!',
          severity: 'success',
        });
      } else {
        console.error('Invalid optimized lineup data:', optimizedData);
        setSnackbar({
          open: true,
          message: 'Error optimizing lineup. Please try again.',
          severity: 'error',
        });
      }
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
    if (!optimizedLineup || !Array.isArray(optimizedLineup.players) || optimizedLineup.players.length === 0) {
      setSnackbar({
        open: true,
        message: 'No optimized lineup to save',
        severity: 'warning',
      });
      return;
    }
    
    if (!optimizedLineupName.trim()) {
      setSnackbar({
        open: true,
        message: 'Please enter a name for the optimized lineup',
        severity: 'warning',
      });
      return;
    }
    
    try {
      const lineupData = {
        name: optimizedLineupName,
        players: optimizedLineup.players.map(player => player.player_id),
      };
      
      console.log('LineupOptimizer: Saving optimized lineup:', lineupData);
      const savedLineup = await createLineup(lineupData);
      
      if (savedLineup && savedLineup.id) {
        console.log('LineupOptimizer: Optimized lineup saved successfully:', savedLineup);
        
        // Refresh the lineups list
        await refreshLineups();
        
        setSnackbar({
          open: true,
          message: 'Optimized lineup saved successfully!',
          severity: 'success',
        });
      } else {
        console.error('Invalid response from createLineup:', savedLineup);
        setSnackbar({
          open: true,
          message: 'Failed to save optimized lineup. Please try again.',
          severity: 'error',
        });
      }
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
                {Array.isArray(lineups) && lineups.length > 0 ? (
                  lineups.map((lineup) => (
                    <MenuItem key={lineup.id} value={lineup.id}>
                      {lineup.name}
                    </MenuItem>
                  ))
                ) : (
                  <MenuItem disabled>No lineups available</MenuItem>
                )}
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
                  Original Lineup: {selectedLineup?.name || 'N/A'}
                </Typography>
                <Divider sx={{ mb: 2 }} />
                
                {selectedLineup && Array.isArray(selectedLineup.players) ? (
                  selectedLineup.players.map((player) => (
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
                        </CardContent>
                      </Box>
                    </Card>
                  ))
                ) : (
                  <Typography variant="body1" color="text.secondary">
                    No players in this lineup
                  </Typography>
                )}
              </Paper>
            </Grid>
            
            {/* Optimized Lineup */}
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 3, height: '100%' }} elevation={3}>
                <Typography variant="h6" gutterBottom>
                  Optimized Lineup: {optimizedLineupName}
                </Typography>
                <Divider sx={{ mb: 2 }} />
                
                {optimizedLineup && Array.isArray(optimizedLineup.players) ? (
                  optimizedLineup.players.map((player) => (
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
                        </CardContent>
                      </Box>
                    </Card>
                  ))
                ) : (
                  <Typography variant="body1" color="text.secondary">
                    No players in optimized lineup
                  </Typography>
                )}
              </Paper>
            </Grid>
          </Grid>
          
          <Box sx={{ mt: 3, textAlign: 'center' }}>
            <Button
              variant="contained"
              color="secondary"
              startIcon={<SaveIcon />}
              onClick={handleSaveOptimizedLineup}
              disabled={!optimizedLineup || !Array.isArray(optimizedLineup.players) || optimizedLineup.players.length === 0}
              size="large"
            >
              Save Optimized Lineup
            </Button>
          </Box>
        </>
      ) : selectedLineup ? (
        <Paper sx={{ p: 3, textAlign: 'center' }} elevation={3}>
          <Typography variant="h6" gutterBottom>
            Click "Optimize Lineup" to generate an optimized version
          </Typography>
        </Paper>
      ) : (
        <Paper sx={{ p: 3, textAlign: 'center' }} elevation={3}>
          <Typography variant="h6" gutterBottom>
            Select a lineup to optimize
          </Typography>
        </Paper>
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