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
} from '@mui/material';
import { getPlayers } from '../services/api';

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
  const playersPerPage = 12;

  useEffect(() => {
    const fetchPlayers = async () => {
      try {
        setLoading(true);
        const data = await getPlayers();
        setPlayers(data);
        setFilteredPlayers(data);
        
        // Extract unique teams for filter
        const uniqueTeams = [...new Set(data.map(player => player.team))].filter(Boolean).sort();
        setTeams(uniqueTeams);
      } catch (error) {
        console.error('Error fetching players:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchPlayers();
  }, []);

  useEffect(() => {
    // Apply filters
    let result = players;
    
    if (searchTerm) {
      result = result.filter(player => 
        player.name.toLowerCase().includes(searchTerm.toLowerCase())
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

  const getPlayerImageUrl = (playerId) => {
    return `https://cdn.nba.com/headshots/nba/latest/1040x760/${playerId}.png`;
  };

  // Calculate pagination
  const indexOfLastPlayer = page * playersPerPage;
  const indexOfFirstPlayer = indexOfLastPlayer - playersPerPage;
  const currentPlayers = filteredPlayers.slice(indexOfFirstPlayer, indexOfLastPlayer);
  const totalPages = Math.ceil(filteredPlayers.length / playersPerPage);

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
        NBA Players
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
            <FormControl fullWidth variant="outlined">
              <InputLabel>Position</InputLabel>
              <Select
                value={positionFilter}
                onChange={handlePositionChange}
                label="Position"
              >
                <MenuItem value="">All Positions</MenuItem>
                <MenuItem value="PG">Point Guard (PG)</MenuItem>
                <MenuItem value="SG">Shooting Guard (SG)</MenuItem>
                <MenuItem value="SF">Small Forward (SF)</MenuItem>
                <MenuItem value="PF">Power Forward (PF)</MenuItem>
                <MenuItem value="C">Center (C)</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={3}>
            <FormControl fullWidth variant="outlined">
              <InputLabel>Team</InputLabel>
              <Select
                value={teamFilter}
                onChange={handleTeamChange}
                label="Team"
              >
                <MenuItem value="">All Teams</MenuItem>
                {teams.map((team) => (
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
              color="secondary" 
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
          Showing {filteredPlayers.length} players
        </Typography>
        {(searchTerm || positionFilter || teamFilter) && (
          <Box>
            {searchTerm && (
              <Chip 
                label={`Search: ${searchTerm}`} 
                onDelete={() => setSearchTerm('')}
                sx={{ mr: 1 }}
              />
            )}
            {positionFilter && (
              <Chip 
                label={`Position: ${positionFilter}`} 
                onDelete={() => setPositionFilter('')}
                sx={{ mr: 1 }}
              />
            )}
            {teamFilter && (
              <Chip 
                label={`Team: ${teamFilter}`} 
                onDelete={() => setTeamFilter('')}
              />
            )}
          </Box>
        )}
      </Box>
      
      {/* Players Grid */}
      <Grid container spacing={3}>
        {currentPlayers.length > 0 ? (
          currentPlayers.map((player) => (
            <Grid item key={player.player_id} xs={12} sm={6} md={4} lg={3}>
              <Card 
                className="player-card" 
                onClick={() => handlePlayerClick(player.player_id)}
                sx={{ cursor: 'pointer' }}
              >
                <CardMedia
                  component="img"
                  height="200"
                  image={player.image_url || getPlayerImageUrl(player.player_id)}
                  alt={player.name}
                  onError={(e) => {
                    e.target.src = `https://via.placeholder.com/200x200?text=${player.name.charAt(0)}`;
                  }}
                />
                <CardContent>
                  <Typography gutterBottom variant="h6" component="div" noWrap>
                    {player.name}
                  </Typography>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="body2" color="text.secondary">
                      {player.position || 'N/A'}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {player.team || 'Free Agent'}
                    </Typography>
                  </Box>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography variant="body2">
                      {player.ppg || '0'} PPG
                    </Typography>
                    <Typography variant="body2">
                      {player.rpg || '0'} RPG
                    </Typography>
                    <Typography variant="body2">
                      {player.apg || '0'} APG
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))
        ) : (
          <Grid item xs={12}>
            <Box sx={{ textAlign: 'center', py: 4 }}>
              <Typography variant="h6">No players found matching your filters</Typography>
              <Button 
                variant="contained" 
                color="primary" 
                onClick={clearFilters}
                sx={{ mt: 2 }}
              >
                Clear All Filters
              </Button>
            </Box>
          </Grid>
        )}
      </Grid>
      
      {/* Pagination */}
      {filteredPlayers.length > 0 && (
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
    </Container>
  );
};

export default Players; 