import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Typography,
  TextField,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress,
  Pagination,
  Chip,
  Button,
  Alert,
  Snackbar,
} from '@mui/material';
import { getPlayers, getPlayerImageUrl } from '../services/api';

const Players = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [players, setPlayers] = useState([]);
  const [filteredPlayers, setFilteredPlayers] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [positionFilter, setPositionFilter] = useState('');
  const [teamFilter, setTeamFilter] = useState('');
  const [page, setPage] = useState(1);
  const [teams, setTeams] = useState([]);
  const [positions, setPositions] = useState([]);
  const [error, setError] = useState(null);
  const playersPerPage = 12;

  useEffect(() => {
    const fetchPlayers = async () => {
      try {
        setLoading(true);
        const data = await getPlayers();
        
        // Ensure data is an array
        if (Array.isArray(data)) {
          setPlayers(data);
          setFilteredPlayers(data);
          
          // Extract unique teams for filter
          const uniqueTeams = [...new Set(data.map(player => player.team))].filter(Boolean).sort();
          setTeams(uniqueTeams);
          
          // Extract unique positions for filter
          const uniquePositions = [...new Set(data.map(player => player.position))].filter(Boolean).sort();
          setPositions(uniquePositions);
        } else {
          console.error('Expected players data to be an array but got:', data);
          setPlayers([]);
          setFilteredPlayers([]);
          setError('Failed to load players data. Please try again.');
        }
      } catch (error) {
        console.error('Error fetching players:', error);
        setPlayers([]);
        setFilteredPlayers([]);
        setError('Error loading players. Please try refreshing the page.');
      } finally {
        setLoading(false);
      }
    };

    fetchPlayers();
  }, []);

  useEffect(() => {
    // Apply filters
    if (!Array.isArray(players)) {
      setFilteredPlayers([]);
      return;
    }
    
    let result = [...players];
    
    if (searchTerm) {
      result = result.filter(player => 
        player.name && player.name.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
    
    if (positionFilter) {
      result = result.filter(player => 
        player.position === positionFilter
      );
    }
    
    if (teamFilter) {
      result = result.filter(player => 
        player.team === teamFilter
      );
    }
    
    setFilteredPlayers(result);
    setPage(1); // Reset to first page when filters change
  }, [searchTerm, positionFilter, teamFilter, players]);

  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value);
  };
  
  const handlePositionChange = (event) => {
    setPositionFilter(event.target.value);
  };
  
  const handleTeamChange = (event) => {
    setTeamFilter(event.target.value);
  };
  
  const handlePageChange = (event, value) => {
    setPage(value);
  };
  
  const handlePlayerClick = (playerId) => {
    navigate(`/players/${playerId}`);
  };
  
  const clearFilters = () => {
    setSearchTerm('');
    setPositionFilter('');
    setTeamFilter('');
  };
  
  const handleCloseError = () => {
    setError(null);
  };

  // Calculate pagination
  const indexOfLastPlayer = page * playersPerPage;
  const indexOfFirstPlayer = indexOfLastPlayer - playersPerPage;
  const currentPlayers = Array.isArray(filteredPlayers) 
    ? filteredPlayers.slice(indexOfFirstPlayer, indexOfLastPlayer) 
    : [];
  const totalPages = Math.ceil((Array.isArray(filteredPlayers) ? filteredPlayers.length : 0) / playersPerPage);

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
        Players
      </Typography>
      
      {/* Filters */}
      <Box sx={{ mb: 4 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} sm={4}>
            <TextField
              fullWidth
              label="Search Players"
              variant="outlined"
              value={searchTerm}
              onChange={handleSearchChange}
            />
          </Grid>
          <Grid item xs={12} sm={3}>
            <FormControl fullWidth>
              <InputLabel>Position</InputLabel>
              <Select
                value={positionFilter}
                label="Position"
                onChange={handlePositionChange}
              >
                <MenuItem value="">All Positions</MenuItem>
                {Array.isArray(positions) && positions.map((position) => (
                  <MenuItem key={position} value={position}>
                    {position}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={3}>
            <FormControl fullWidth>
              <InputLabel>Team</InputLabel>
              <Select
                value={teamFilter}
                label="Team"
                onChange={handleTeamChange}
              >
                <MenuItem value="">All Teams</MenuItem>
                {Array.isArray(teams) && teams.map((team) => (
                  <MenuItem key={team} value={team}>
                    {team}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={2}>
            <Button 
              variant="outlined" 
              onClick={clearFilters}
              fullWidth
            >
              Clear Filters
            </Button>
          </Grid>
        </Grid>
      </Box>
      
      {/* Results count */}
      <Box sx={{ mb: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="body1">
          Showing {Array.isArray(filteredPlayers) ? filteredPlayers.length : 0} players
        </Typography>
        {filteredPlayers.length === 0 && !loading && (
          <Typography variant="body1" color="error">
            No players found matching your filters
          </Typography>
        )}
      </Box>
      
      {/* Players Grid */}
      <Grid container spacing={3}>
        {Array.isArray(currentPlayers) && currentPlayers.length > 0 ? (
          currentPlayers.map((player) => (
            <Grid item xs={12} sm={6} md={4} lg={3} key={player.player_id}>
              <Card 
                sx={{ 
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  cursor: 'pointer',
                  transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
                  '&:hover': {
                    transform: 'translateY(-5px)',
                    boxShadow: '0 8px 16px rgba(0,0,0,0.1)',
                  },
                }}
                onClick={() => handlePlayerClick(player.player_id)}
                className="player-card"
              >
                <CardMedia
                  component="img"
                  height="140"
                  image={player.image_url || getPlayerImageUrl(player.player_id)}
                  alt={`${player.first_name} ${player.last_name}`}
                  onError={(e) => {
                    // Fall back to NBA logo if player image is unavailable
                    e.target.src = `https://cdn.nba.com/logos/nba/nba-logoman-75-word_black.svg`;
                  }}
                  sx={{ 
                    objectFit: 'contain', 
                    backgroundColor: '#f8f8f8',
                    padding: '8px'
                  }}
                />
                <CardContent>
                  <Typography variant="h6" component="div" gutterBottom noWrap>
                    {player.name || 'Unknown Player'}
                  </Typography>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Chip 
                      label={player.position || 'N/A'} 
                      size="small" 
                      sx={{ backgroundColor: 'rgba(25, 118, 210, 0.1)', color: 'primary.main' }}
                    />
                    <Chip 
                      label={player.team || 'Free Agent'} 
                      size="small"
                      sx={{ backgroundColor: 'rgba(46, 125, 50, 0.1)', color: 'success.main' }}
                    />
                  </Box>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 2 }}>
                    <Typography variant="body2" color="text.secondary">
                      PPG: <strong>{player.ppg || '0.0'}</strong>
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      RPG: <strong>{player.rpg || '0.0'}</strong>
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      APG: <strong>{player.apg || '0.0'}</strong>
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))
        ) : (
          <Grid item xs={12}>
            <Box sx={{ textAlign: 'center', py: 5 }}>
              <Typography variant="h6" color="text.secondary">
                No players found matching your criteria
              </Typography>
              <Button 
                variant="contained" 
                onClick={clearFilters}
                sx={{ mt: 2 }}
              >
                Clear Filters
              </Button>
            </Box>
          </Grid>
        )}
      </Grid>
      
      {/* Pagination */}
      {totalPages > 1 && (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
          <Pagination 
            count={totalPages} 
            page={page} 
            onChange={handlePageChange} 
            color="primary" 
            size="large"
          />
        </Box>
      )}
      
      {/* Error Snackbar */}
      <Snackbar open={!!error} autoHideDuration={6000} onClose={handleCloseError}>
        <Alert onClose={handleCloseError} severity="error" sx={{ width: '100%' }}>
          {error}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default Players; 