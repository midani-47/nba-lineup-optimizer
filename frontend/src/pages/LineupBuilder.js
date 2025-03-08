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
        const playersData = await getPlayers();
        setPlayers(playersData);
        setFilteredPlayers(playersData);
        
        const lineupsData = await getLineups();
        setSavedLineups(lineupsData);
        
        // Check if a player was passed from another page
        if (location.state?.selectedPlayer) {
          const selectedPlayer = location.state.selectedPlayer;
          if (!lineup.some(p => p.player_id === selectedPlayer.player_id)) {
            setLineup(prev => [...prev, selectedPlayer].slice(0, 5));
          }
        }
      } catch (error) {
        console.error('Error fetching data:', error);
        setSnackbar({
          open: true,
          message: 'Failed to load data. Please try again.',
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

  const handleLoadLineup = (savedLineup) => {
    setLineup(savedLineup.players);
    setLineupName(savedLineup.name + ' (Copy)');
    setSnackbar({
      open: true,
      message: `Loaded lineup: ${savedLineup.name}`,
      severity: 'success',
    });
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

  const handleSaveLineup = async () => {
    if (lineup.length !== 5) {
      setSnackbar({
        open: true,
        message: 'A lineup must contain exactly 5 players.',
        severity: 'warning',
      });
      return;
    }

    if (!lineupName.trim()) {
      setSnackbar({
        open: true,
        message: 'Please enter a lineup name.',
        severity: 'warning',
      });
      return;
    }

    // Check if lineup name already exists
    const lineupNameExists = savedLineups.some(
      savedLineup => savedLineup.name.toLowerCase() === lineupName.toLowerCase()
    );
    
    if (lineupNameExists) {
      setSnackbar({
        open: true,
        message: 'A lineup with this name already exists. Please choose a different name.',
        severity: 'warning',
      });
      return;
    }

    // Check if exact same players already exist in a saved lineup
    const lineupPlayerIds = lineup.map(player => player.player_id).sort().join(',');
    const duplicateLineup = savedLineups.find(savedLineup => {
      const savedPlayerIds = savedLineup.players.map(player => player.player_id).sort().join(',');
      return savedPlayerIds === lineupPlayerIds;
    });
    
    if (duplicateLineup) {
      setSnackbar({
        open: true,
        message: `This exact lineup already exists as "${duplicateLineup.name}".`,
        severity: 'warning',
      });
      return;
    }

    try {
      const lineupData = {
        name: lineupName,
        players: lineup.map(player => player.player_id),
      };
      
      await createLineup(lineupData);
      await fetchSavedLineups();
      
      setSnackbar({
        open: true,
        message: 'Lineup saved successfully!',
        severity: 'success',
      });
      
      // Reset form
      setLineupName('');
      setLineup([]);
    } catch (error) {
      console.error('Error saving lineup:', error);
      setSnackbar({
        open: true,
        message: 'Failed to save lineup. Please try again.',
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
      stats.fg_pct = stats.fg_pct / lineup.length;
      stats.fg3_pct = stats.fg3_pct / lineup.length;
      stats.ft_pct = stats.ft_pct / lineup.length;
    }
    
    return stats;
  };

  const handleRemovePlayer = (playerId) => {
    setLineup(lineup.filter(player => player.player_id !== playerId));
  };

  const handleAddPlayer = (player) => {
    if (lineup.length >= 5) {
      setSnackbar({
        open: true,
        message: 'A lineup can have a maximum of 5 players.',
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
    
    setLineup([...lineup, player]);
  };

  const lineupStats = calculateLineupStats();

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
        Lineup Builder
      </Typography>
      
      <Grid container spacing={3}>
        {/* Available Players */}
        <Grid item xs={12} md={7}>
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
              Available Players
            </Typography>
            <Box sx={{ mb: 2, display: 'flex' }}>
              <TextField
                fullWidth
                label="Search Players"
                variant="outlined"
                value={searchTerm}
                onChange={(e) => {
                  setSearchTerm(e.target.value);
                  handleSearchPlayers(e.target.value);
                }}
                sx={{ mr: 1 }}
              />
              <Button
                variant="contained"
                color="primary"
                startIcon={<SearchIcon />}
                onClick={() => handleSearchPlayers(searchTerm)}
              >
                Search
              </Button>
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
            <TextField
              fullWidth
              label="Lineup Name"
              variant="outlined"
              value={lineupName}
              onChange={(e) => setLineupName(e.target.value)}
              sx={{ mb: 2 }}
            />
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
            
            <Button
              variant="contained"
              color="primary"
              startIcon={<SaveIcon />}
              onClick={handleSaveLineup}
              disabled={lineup.length !== 5 || !lineupName.trim()}
              fullWidth
            >
              Save Lineup
            </Button>
          </Paper>
        </Grid>
        
        {/* Saved Lineups */}
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
                          {savedLineup.players.map((player) => (
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
                        <Button
                          variant="outlined"
                          color="primary"
                          size="small"
                          onClick={() => handleLoadLineup(savedLineup)}
                          sx={{ mt: 2, width: '100%' }}
                        >
                          Load Lineup
                        </Button>
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