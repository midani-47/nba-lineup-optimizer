import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  TextField,
  Button,
  Card,
  CardContent,
  CardMedia,
  IconButton,
  Divider,
  CircularProgress,
  Snackbar,
  Alert,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
  ListItemSecondaryAction,
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import SaveIcon from '@mui/icons-material/Save';
import SearchIcon from '@mui/icons-material/Search';
import { getPlayers, createLineup, getLineups } from '../services/api';

const LineupBuilder = () => {
  const location = useLocation();
  const [loading, setLoading] = useState(true);
  const [players, setPlayers] = useState([]);
  const [filteredPlayers, setFilteredPlayers] = useState([]);
  const [lineup, setLineup] = useState([]);
  const [lineupName, setLineupName] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [savedLineups, setSavedLineups] = useState([]);
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'info',
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [playersData, lineupsData] = await Promise.all([
          getPlayers(),
          getLineups()
        ]);
        
        // Validate players data
        if (Array.isArray(playersData)) {
          setPlayers(playersData);
          setFilteredPlayers(playersData);
        } else {
          console.error('Expected players data to be an array but got:', playersData);
          setPlayers([]);
          setFilteredPlayers([]);
          setSnackbar({
            open: true,
            message: 'Failed to load players data. Please try refreshing the page.',
            severity: 'error',
          });
        }
        
        // Validate lineups data
        if (Array.isArray(lineupsData)) {
          setSavedLineups(lineupsData);
        } else {
          console.error('Expected lineups data to be an array but got:', lineupsData);
          setSavedLineups([]);
          setSnackbar({
            open: true,
            message: 'Failed to load saved lineups. Please try refreshing the page.',
            severity: 'warning',
          });
        }
        
        // Check if a player was passed from another page
        if (location.state?.selectedPlayer) {
          const selectedPlayer = location.state.selectedPlayer;
          if (!lineup.some(p => p.player_id === selectedPlayer.player_id)) {
            setLineup(prev => [...prev, selectedPlayer].slice(0, 5));
          }
        }
      } catch (error) {
        console.error('Error fetching data:', error);
        setPlayers([]);
        setFilteredPlayers([]);
        setSavedLineups([]);
        setSnackbar({
          open: true,
          message: 'Error loading data. Please try refreshing the page.',
          severity: 'error',
        });
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [location.state]);

  const fetchSavedLineups = async () => {
    try {
      const lineupsData = await getLineups();
      setSavedLineups(lineupsData);
    } catch (error) {
      console.error('Error fetching saved lineups:', error);
    }
  };

  const handleSearchPlayers = (searchTerm) => {
    if (!searchTerm.trim()) {
      setFilteredPlayers(players);
      return;
    }
    
    const filtered = players.filter(player => 
      player.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (player.team && player.team.toLowerCase().includes(searchTerm.toLowerCase())) ||
      (player.position && player.position.toLowerCase().includes(searchTerm.toLowerCase()))
    );
    
    setFilteredPlayers(filtered);
  };

  const handleAddPlayer = (player) => {
    if (lineup.length >= 5) {
      setSnackbar({
        open: true,
        message: 'Maximum 5 players allowed in a lineup.',
        severity: 'warning',
      });
      return;
    }
    
    if (lineup.some(p => p.player_id === player.player_id)) {
      setSnackbar({
        open: true,
        message: 'This player is already in your lineup.',
        severity: 'warning',
      });
      return;
    }
    
    setLineup(prev => [...prev, player]);
  };

  const handleRemovePlayer = (playerId) => {
    setLineup(prev => prev.filter(player => player.player_id !== playerId));
  };

  const handleSaveLineup = async () => {
    // Validate lineup
    if (!Array.isArray(lineup) || lineup.length === 0) {
      setSnackbar({
        open: true,
        message: 'Please add players to your lineup before saving.',
        severity: 'warning',
      });
      return;
    }
    
    // Validate lineup name
    if (!lineupName.trim()) {
      setSnackbar({
        open: true,
        message: 'Please enter a name for your lineup.',
        severity: 'warning',
      });
      return;
    }

    try {
      // Create lineup data object
      const lineupData = {
        name: lineupName,
        players: lineup.map(player => player.player_id)
      };

      console.log('Saving lineup with data:', lineupData);

      // Save lineup
      const response = await createLineup(lineupData);
      
      // Validate response
      if (response && response.id) {
        console.log('Lineup saved successfully:', response);
        
        // Fetch all lineups again to ensure we have the latest data
        const updatedLineups = await getLineups();
        setSavedLineups(updatedLineups);
        
        // Reset lineup and name
        setLineup([]);
        setLineupName('');
        
        setSnackbar({
          open: true,
          message: 'Lineup saved successfully!',
          severity: 'success',
        });
      } else {
        console.error('Invalid response from createLineup:', response);
        setSnackbar({
          open: true,
          message: 'Failed to save lineup. Please try again.',
          severity: 'error',
        });
      }
    } catch (error) {
      console.error('Error saving lineup:', error);
      setSnackbar({
        open: true,
        message: 'Error saving lineup. Please try again.',
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

  const calculateLineupStats = () => {
    if (lineup.length === 0) {
      return {
        ppg: 0,
        rpg: 0,
        apg: 0,
        spg: 0,
        bpg: 0,
        fg_pct: 0,
        fg3_pct: 0,
        ft_pct: 0,
      };
    }
    
    const stats = lineup.reduce((acc, player) => {
      return {
        ppg: acc.ppg + (player.ppg || 0),
        rpg: acc.rpg + (player.rpg || 0),
        apg: acc.apg + (player.apg || 0),
        spg: acc.spg + (player.spg || 0),
        bpg: acc.bpg + (player.bpg || 0),
        fg_pct: acc.fg_pct + (player.fg_pct || 0),
        fg3_pct: acc.fg3_pct + (player.fg3_pct || 0),
        ft_pct: acc.ft_pct + (player.ft_pct || 0),
      };
    }, {
      ppg: 0,
      rpg: 0,
      apg: 0,
      spg: 0,
      bpg: 0,
      fg_pct: 0,
      fg3_pct: 0,
      ft_pct: 0,
    });
    
    // Calculate averages for percentages
    if (lineup.length > 0) {
      stats.fg_pct /= lineup.length;
      stats.fg3_pct /= lineup.length;
      stats.ft_pct /= lineup.length;
    }
    
    return stats;
  };
  
  const lineupStats = calculateLineupStats();

  if (loading) {
    return (
      <Container sx={{ mt: 4, mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  return (
    <Container sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Lineup Builder
      </Typography>
      <Typography variant="subtitle1" gutterBottom>
        Create your dream NBA lineup by selecting players from the available list.
      </Typography>
      
      <Grid container spacing={3}>
        {/* Available Players */}
        <Grid item xs={12} md={7}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
            }}
            elevation={3}
          >
            <Typography variant="h6" gutterBottom>
              Available Players
            </Typography>
            <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
              <form onSubmit={(e) => {
                e.preventDefault();
                handleSearchPlayers(searchTerm);
              }} style={{ display: 'flex', gap: '8px', width: '100%' }}>
                <TextField
                  fullWidth
                  variant="outlined"
                  placeholder="Search players..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
                <Button
                  type="submit"
                  variant="contained"
                  color="primary"
                  startIcon={<SearchIcon />}
                >
                  Search
                </Button>
              </form>
            </Box>
            <Typography variant="body2" sx={{ mb: 2 }}>
              Search and add players to your lineup. Click the Add button to add a player.
            </Typography>
            <Box sx={{ flexGrow: 1, overflow: 'auto', maxHeight: 500 }}>
              <List>
                {filteredPlayers.map((player) => (
                  <ListItem key={player.player_id} divider>
                    <ListItemAvatar>
                      <Avatar
                        src={player.image_url || getPlayerImageUrl(player.player_id)}
                        alt={player.name}
                        sx={{ width: 50, height: 50 }}
                        variant="rounded"
                      />
                    </ListItemAvatar>
                    <ListItemText
                      primary={player.name}
                      secondary={
                        <>
                          {player.position || 'N/A'} | {player.team || 'Free Agent'}
                          <br />
                          {player.ppg || '0'} PPG, {player.rpg || '0'} RPG, {player.apg || '0'} APG
                        </>
                      }
                    />
                    <ListItemSecondaryAction>
                      <IconButton
                        edge="end"
                        color="primary"
                        onClick={() => handleAddPlayer(player)}
                        disabled={lineup.some(p => p.player_id === player.player_id) || lineup.length >= 5}
                      >
                        <AddIcon />
                      </IconButton>
                    </ListItemSecondaryAction>
                  </ListItem>
                ))}
                {filteredPlayers.length === 0 && (
                  <ListItem>
                    <ListItemText primary="No players found matching your search." />
                  </ListItem>
                )}
              </List>
            </Box>
          </Paper>
        </Grid>
        
        {/* Current Lineup */}
        <Grid item xs={12} md={5}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              minHeight: 500,
            }}
            elevation={3}
          >
            <Typography variant="h6" gutterBottom>
              Current Lineup ({lineup.length}/5)
            </Typography>
            
            <Box sx={{ flexGrow: 1, mb: 2 }}>
              {lineup.length > 0 ? (
                lineup.map((player) => (
                  <Card key={player.player_id} sx={{ mb: 2, display: 'flex' }}>
                    <CardMedia
                      component="img"
                      sx={{ width: 80, objectFit: 'cover' }}
                      image={player.image_url || getPlayerImageUrl(player.player_id)}
                      alt={player.name}
                      onError={(e) => {
                        e.target.src = `https://via.placeholder.com/80x80?text=${player.name.charAt(0)}`;
                      }}
                    />
                    <Box sx={{ display: 'flex', flexDirection: 'column', width: '100%' }}>
                      <CardContent sx={{ flex: '1 0 auto', py: 1 }}>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <Typography component="div" variant="subtitle1">
                            {player.name}
                          </Typography>
                          <IconButton
                            size="small"
                            color="error"
                            onClick={() => handleRemovePlayer(player.player_id)}
                          >
                            <DeleteIcon />
                          </IconButton>
                        </Box>
                        <Typography variant="body2" color="text.secondary" component="div">
                          {player.position || 'N/A'} | {player.team || 'Free Agent'}
                        </Typography>
                        <Typography variant="body2" component="div">
                          {player.ppg || '0'} PPG, {player.rpg || '0'} RPG, {player.apg || '0'} APG
                        </Typography>
                      </CardContent>
                    </Box>
                  </Card>
                ))
              ) : (
                <Box sx={{ textAlign: 'center', py: 4 }}>
                  <Typography variant="body1">
                    Your lineup is empty. Add players from the available players list.
                  </Typography>
                </Box>
              )}
            </Box>
            
            {/* Lineup Stats */}
            <Box sx={{ mb: 2 }}>
              <Typography variant="subtitle1" gutterBottom>
                Lineup Statistics
              </Typography>
              <Grid container spacing={1}>
                <Grid item xs={4}>
                  <Typography variant="body2" color="text.secondary">
                    PPG
                  </Typography>
                  <Typography variant="body1" fontWeight="bold">
                    {lineupStats.ppg.toFixed(1)}
                  </Typography>
                </Grid>
                <Grid item xs={4}>
                  <Typography variant="body2" color="text.secondary">
                    RPG
                  </Typography>
                  <Typography variant="body1" fontWeight="bold">
                    {lineupStats.rpg.toFixed(1)}
                  </Typography>
                </Grid>
                <Grid item xs={4}>
                  <Typography variant="body2" color="text.secondary">
                    APG
                  </Typography>
                  <Typography variant="body1" fontWeight="bold">
                    {lineupStats.apg.toFixed(1)}
                  </Typography>
                </Grid>
                <Grid item xs={4}>
                  <Typography variant="body2" color="text.secondary">
                    SPG
                  </Typography>
                  <Typography variant="body1" fontWeight="bold">
                    {lineupStats.spg.toFixed(1)}
                  </Typography>
                </Grid>
                <Grid item xs={4}>
                  <Typography variant="body2" color="text.secondary">
                    BPG
                  </Typography>
                  <Typography variant="body1" fontWeight="bold">
                    {lineupStats.bpg.toFixed(1)}
                  </Typography>
                </Grid>
                <Grid item xs={4}>
                  <Typography variant="body2" color="text.secondary">
                    FG%
                  </Typography>
                  <Typography variant="body1" fontWeight="bold">
                    {(lineupStats.fg_pct * 100).toFixed(1)}%
                  </Typography>
                </Grid>
              </Grid>
            </Box>
            <Box>
              <form onSubmit={(e) => {
                e.preventDefault();
                handleSaveLineup();
              }}>
                <TextField
                  fullWidth
                  label="Lineup Name"
                  variant="outlined"
                  value={lineupName}
                  onChange={(e) => setLineupName(e.target.value)}
                  sx={{ mb: 2 }}
                />
                <Button
                  type="submit"
                  variant="contained"
                  color="primary"
                  startIcon={<SaveIcon />}
                  disabled={lineup.length !== 5 || !lineupName.trim()}
                  fullWidth
                >
                  Save Lineup
                </Button>
              </form>
            </Box>
          </Paper>
        </Grid>
        
        {/* Saved Lineups Section - Display Only */}
        <Grid item xs={12}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
            }}
            elevation={3}
          >
            <Typography variant="h6" gutterBottom>
              Saved Lineups
            </Typography>
            <Divider sx={{ mb: 2 }} />
            
            {savedLineups.length > 0 ? (
              <Grid container spacing={2}>
                {savedLineups.map((savedLineup) => (
                  <Grid item key={savedLineup.id} xs={12} sm={6} md={4}>
                    <Card className="lineup-card">
                      <CardContent>
                        <Typography variant="h6" component="div">
                          {savedLineup.name}
                        </Typography>
                        <Typography variant="body2" color="text.secondary" gutterBottom>
                          {savedLineup.created_at ? new Date(savedLineup.created_at).toLocaleDateString() : 'N/A'}
                        </Typography>
                        <Box sx={{ mt: 1 }}>
                          {Array.isArray(savedLineup.players) && savedLineup.players.map((player) => (
                            <Typography key={player.player_id} variant="body2" component="div">
                              • {player.name} ({player.position || 'N/A'})
                            </Typography>
                          ))}
                        </Box>
                        <Box sx={{ mt: 2, display: 'flex', justifyContent: 'space-between' }}>
                          <Typography variant="body2">
                            PPG: {savedLineup.total_ppg?.toFixed(1) || '0.0'}
                          </Typography>
                          <Typography variant="body2">
                            RPG: {savedLineup.total_rpg?.toFixed(1) || '0.0'}
                          </Typography>
                          <Typography variant="body2">
                            APG: {savedLineup.total_apg?.toFixed(1) || '0.0'}
                          </Typography>
                        </Box>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            ) : (
              <Box sx={{ textAlign: 'center', py: 4 }}>
                <Typography variant="body1">
                  You haven't saved any lineups yet. Create and save a lineup to see it here.
                </Typography>
              </Box>
            )}
          </Paper>
        </Grid>
      </Grid>
      
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

export default LineupBuilder; 