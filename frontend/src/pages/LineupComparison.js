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
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Alert,
  Snackbar
} from '@mui/material';
import { ResponsiveLine } from '@nivo/line';
import { getLineups, compareLineups } from '../services/api';

const LineupComparison = () => {
  const [loading, setLoading] = useState(true);
  const [lineups, setLineups] = useState([]);
  const [lineup1, setLineup1] = useState('');
  const [lineup2, setLineup2] = useState('');
  const [comparisonData, setComparisonData] = useState(null);
  const [comparisonLoading, setComparisonLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLineups = async () => {
      try {
        setLoading(true);
        const data = await getLineups();
        
        // Validate that data is an array
        if (Array.isArray(data)) {
          setLineups(data);
        } else {
          console.error('Expected lineups data to be an array but got:', data);
          setLineups([]);
          setError('Failed to load lineups data. Please try again.');
        }
      } catch (error) {
        console.error('Error fetching lineups:', error);
        setLineups([]);
        setError('Error loading lineups. Please try refreshing the page.');
      } finally {
        setLoading(false);
      }
    };

    fetchLineups();
  }, []);

  const handleCompare = async () => {
    if (!lineup1 || !lineup2) {
      setError('Please select two lineups to compare');
      return;
    }

    if (lineup1 === lineup2) {
      setError('Please select different lineups to compare');
      return;
    }

    try {
      setComparisonLoading(true);
      const data = await compareLineups(lineup1, lineup2);
      
      // Validate comparison data
      if (data && data.lineup1 && data.lineup2) {
        setComparisonData(data);
      } else {
        console.error('Invalid comparison data received:', data);
        setError('Failed to compare lineups. Please try again with different lineups.');
        setComparisonData(null);
      }
    } catch (error) {
      console.error('Error comparing lineups:', error);
      setError('Error comparing lineups. Please try again.');
      setComparisonData(null);
    } finally {
      setComparisonLoading(false);
    }
  };

  const handleCloseError = () => {
    setError(null);
  };

  const getPlayerImageUrl = (playerId) => {
    return `https://cdn.nba.com/headshots/nba/latest/1040x760/${playerId}.png`;
  };

  const getStatDiffColor = (diff) => {
    if (diff > 0) return 'success.main';
    if (diff < 0) return 'error.main';
    return 'text.primary';
  };

  const formatStatDiff = (diff) => {
    if (diff > 0) return `+${diff.toFixed(1)}`;
    return diff.toFixed(1);
  };

  const getChartData = () => {
    if (!comparisonData || !comparisonData.lineup1 || !comparisonData.lineup2) return [];

    const stats = ['ppg', 'rpg', 'apg', 'spg', 'bpg', 'fg_pct', 'fg3_pct', 'ft_pct'];
    const statLabels = {
      ppg: 'Points',
      rpg: 'Rebounds',
      apg: 'Assists',
      spg: 'Steals',
      bpg: 'Blocks',
      fg_pct: 'FG%',
      fg3_pct: '3P%',
      ft_pct: 'FT%',
    };

    return [
      {
        id: comparisonData.lineup1.name || 'Lineup 1',
        color: '#1976d2',
        data: stats.map(stat => {
          let value = comparisonData.lineup1[`total_${stat}`] || 0;
          if (stat.includes('pct')) {
            value = value * 100;
          }
          return {
            x: statLabels[stat],
            y: value,
          };
        }),
      },
      {
        id: comparisonData.lineup2.name || 'Lineup 2',
        color: '#f50057',
        data: stats.map(stat => {
          let value = comparisonData.lineup2[`total_${stat}`] || 0;
          if (stat.includes('pct')) {
            value = value * 100;
          }
          return {
            x: statLabels[stat],
            y: value,
          };
        }),
      },
    ];
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
        Lineup Comparison
      </Typography>
      
      <Paper sx={{ p: 3, mb: 4 }} elevation={3}>
        <Grid container spacing={3} alignItems="center">
          <Grid item xs={12} sm={5}>
            <FormControl fullWidth variant="outlined">
              <InputLabel>First Lineup</InputLabel>
              <Select
                value={lineup1}
                onChange={(e) => setLineup1(e.target.value)}
                label="First Lineup"
              >
                <MenuItem value="">
                  <em>Select a lineup</em>
                </MenuItem>
                {Array.isArray(lineups) && lineups.length > 0 ? (
                  lineups.map((lineup) => (
                    <MenuItem key={`lineup1-${lineup.id}`} value={lineup.id}>
                      {lineup.name || `Lineup ${lineup.id}`}
                    </MenuItem>
                  ))
                ) : (
                  <MenuItem disabled>No lineups available</MenuItem>
                )}
              </Select>
            </FormControl>
          </Grid>
          
          <Grid item xs={12} sm={2} sx={{ textAlign: 'center' }}>
            <Typography variant="h6">VS</Typography>
          </Grid>
          
          <Grid item xs={12} sm={5}>
            <FormControl fullWidth variant="outlined">
              <InputLabel>Second Lineup</InputLabel>
              <Select
                value={lineup2}
                onChange={(e) => setLineup2(e.target.value)}
                label="Second Lineup"
              >
                <MenuItem value="">
                  <em>Select a lineup</em>
                </MenuItem>
                {Array.isArray(lineups) && lineups.length > 0 ? (
                  lineups.map((lineup) => (
                    <MenuItem key={`lineup2-${lineup.id}`} value={lineup.id}>
                      {lineup.name || `Lineup ${lineup.id}`}
                    </MenuItem>
                  ))
                ) : (
                  <MenuItem disabled>No lineups available</MenuItem>
                )}
              </Select>
            </FormControl>
          </Grid>
          
          <Grid item xs={12} sx={{ textAlign: 'center', mt: 2 }}>
            <Button
              variant="contained"
              color="primary"
              onClick={handleCompare}
              disabled={!lineup1 || !lineup2 || lineup1 === lineup2 || !Array.isArray(lineups) || lineups.length < 2}
              size="large"
            >
              Compare Lineups
            </Button>
          </Grid>
        </Grid>
      </Paper>
      
      {comparisonLoading ? (
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="40vh">
          <CircularProgress />
        </Box>
      ) : comparisonData ? (
        <>
          {/* Comparison Chart */}
          <Paper sx={{ p: 3, mb: 4, height: 400 }} elevation={3}>
            <Typography variant="h6" gutterBottom>
              Statistical Comparison
            </Typography>
            <Box sx={{ height: 320 }}>
              <ResponsiveLine
                data={getChartData()}
                margin={{ top: 50, right: 110, bottom: 50, left: 60 }}
                xScale={{ type: 'point' }}
                yScale={{
                  type: 'linear',
                  min: 'auto',
                  max: 'auto',
                  stacked: false,
                  reverse: false,
                }}
                yFormat=" >-.1f"
                axisTop={null}
                axisRight={null}
                axisBottom={{
                  tickSize: 5,
                  tickPadding: 5,
                  tickRotation: 0,
                  legend: 'Category',
                  legendOffset: 36,
                  legendPosition: 'middle',
                }}
                axisLeft={{
                  tickSize: 5,
                  tickPadding: 5,
                  tickRotation: 0,
                  legend: 'Value',
                  legendOffset: -40,
                  legendPosition: 'middle',
                }}
                pointSize={10}
                pointColor={{ theme: 'background' }}
                pointBorderWidth={2}
                pointBorderColor={{ from: 'serieColor' }}
                pointLabelYOffset={-12}
                useMesh={true}
                legends={[
                  {
                    anchor: 'bottom-right',
                    direction: 'column',
                    justify: false,
                    translateX: 100,
                    translateY: 0,
                    itemsSpacing: 0,
                    itemDirection: 'left-to-right',
                    itemWidth: 80,
                    itemHeight: 20,
                    itemOpacity: 0.75,
                    symbolSize: 12,
                    symbolShape: 'circle',
                    symbolBorderColor: 'rgba(0, 0, 0, .5)',
                    effects: [
                      {
                        on: 'hover',
                        style: {
                          itemBackground: 'rgba(0, 0, 0, .03)',
                          itemOpacity: 1,
                        },
                      },
                    ],
                  },
                ]}
              />
            </Box>
          </Paper>
          
          {/* Lineups Comparison */}
          <Grid container spacing={3}>
            {/* Lineup 1 */}
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 2 }} elevation={3}>
                <Typography variant="h6" gutterBottom>
                  {comparisonData.lineup1?.name || 'Lineup 1'}
                </Typography>
                <Divider sx={{ mb: 2 }} />
                
                {Array.isArray(comparisonData.lineup1?.players) && comparisonData.lineup1.players.length > 0 ? (
                  comparisonData.lineup1.players.map((player) => (
                    <Card key={player.player_id} sx={{ mb: 2, display: 'flex' }}>
                      <CardMedia
                        component="img"
                        sx={{ width: 80, height: 80, objectFit: 'cover' }}
                        image={player.image_url || getPlayerImageUrl(player.player_id)}
                        alt={player.name}
                        onError={(e) => {
                          e.target.src = `https://via.placeholder.com/80x80?text=${player.name ? player.name.charAt(0) : 'N/A'}`;
                        }}
                      />
                      <CardContent sx={{ flex: '1 1 auto' }}>
                        <Typography variant="subtitle1">{player.name || 'Unknown Player'}</Typography>
                        <Typography variant="body2" color="text.secondary">
                          {player.position || 'N/A'} | {player.team || 'N/A'}
                        </Typography>
                        <Box sx={{ display: 'flex', mt: 1 }}>
                          <Typography variant="body2" sx={{ mr: 2 }}>
                            {player.ppg || '0'} PPG
                          </Typography>
                          <Typography variant="body2" sx={{ mr: 2 }}>
                            {player.rpg || '0'} RPG
                          </Typography>
                          <Typography variant="body2">
                            {player.apg || '0'} APG
                          </Typography>
                        </Box>
                      </CardContent>
                    </Card>
                  ))
                ) : (
                  <Alert severity="info">No player data available for this lineup</Alert>
                )}
              </Paper>
            </Grid>
            
            {/* Lineup 2 */}
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 2 }} elevation={3}>
                <Typography variant="h6" gutterBottom>
                  {comparisonData.lineup2?.name || 'Lineup 2'}
                </Typography>
                <Divider sx={{ mb: 2 }} />
                
                {Array.isArray(comparisonData.lineup2?.players) && comparisonData.lineup2.players.length > 0 ? (
                  comparisonData.lineup2.players.map((player) => (
                    <Card key={player.player_id} sx={{ mb: 2, display: 'flex' }}>
                      <CardMedia
                        component="img"
                        sx={{ width: 80, height: 80, objectFit: 'cover' }}
                        image={player.image_url || getPlayerImageUrl(player.player_id)}
                        alt={player.name}
                        onError={(e) => {
                          e.target.src = `https://via.placeholder.com/80x80?text=${player.name ? player.name.charAt(0) : 'N/A'}`;
                        }}
                      />
                      <CardContent sx={{ flex: '1 1 auto' }}>
                        <Typography variant="subtitle1">{player.name || 'Unknown Player'}</Typography>
                        <Typography variant="body2" color="text.secondary">
                          {player.position || 'N/A'} | {player.team || 'N/A'}
                        </Typography>
                        <Box sx={{ display: 'flex', mt: 1 }}>
                          <Typography variant="body2" sx={{ mr: 2 }}>
                            {player.ppg || '0'} PPG
                          </Typography>
                          <Typography variant="body2" sx={{ mr: 2 }}>
                            {player.rpg || '0'} RPG
                          </Typography>
                          <Typography variant="body2">
                            {player.apg || '0'} APG
                          </Typography>
                        </Box>
                      </CardContent>
                    </Card>
                  ))
                ) : (
                  <Alert severity="info">No player data available for this lineup</Alert>
                )}
              </Paper>
            </Grid>
            
            {/* Stats Comparison Table */}
            <Grid item xs={12}>
              <Paper sx={{ p: 2 }} elevation={3}>
                <Typography variant="h6" gutterBottom>
                  Statistical Breakdown
                </Typography>
                <TableContainer>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Stat</TableCell>
                        <TableCell align="right">{comparisonData.lineup1?.name || 'Lineup 1'}</TableCell>
                        <TableCell align="right">{comparisonData.lineup2?.name || 'Lineup 2'}</TableCell>
                        <TableCell align="right">Difference</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {comparisonData && (
                        <>
                          <TableRow>
                            <TableCell component="th" scope="row">Points Per Game</TableCell>
                            <TableCell align="right">{comparisonData.lineup1?.total_ppg?.toFixed(1) || '0.0'}</TableCell>
                            <TableCell align="right">{comparisonData.lineup2?.total_ppg?.toFixed(1) || '0.0'}</TableCell>
                            <TableCell align="right" sx={{ color: getStatDiffColor((comparisonData.lineup1?.total_ppg || 0) - (comparisonData.lineup2?.total_ppg || 0)) }}>
                              {formatStatDiff((comparisonData.lineup1?.total_ppg || 0) - (comparisonData.lineup2?.total_ppg || 0))}
                            </TableCell>
                          </TableRow>
                          <TableRow>
                            <TableCell component="th" scope="row">Rebounds Per Game</TableCell>
                            <TableCell align="right">{comparisonData.lineup1?.total_rpg?.toFixed(1) || '0.0'}</TableCell>
                            <TableCell align="right">{comparisonData.lineup2?.total_rpg?.toFixed(1) || '0.0'}</TableCell>
                            <TableCell align="right" sx={{ color: getStatDiffColor((comparisonData.lineup1?.total_rpg || 0) - (comparisonData.lineup2?.total_rpg || 0)) }}>
                              {formatStatDiff((comparisonData.lineup1?.total_rpg || 0) - (comparisonData.lineup2?.total_rpg || 0))}
                            </TableCell>
                          </TableRow>
                          <TableRow>
                            <TableCell component="th" scope="row">Assists Per Game</TableCell>
                            <TableCell align="right">{comparisonData.lineup1?.total_apg?.toFixed(1) || '0.0'}</TableCell>
                            <TableCell align="right">{comparisonData.lineup2?.total_apg?.toFixed(1) || '0.0'}</TableCell>
                            <TableCell align="right" sx={{ color: getStatDiffColor((comparisonData.lineup1?.total_apg || 0) - (comparisonData.lineup2?.total_apg || 0)) }}>
                              {formatStatDiff((comparisonData.lineup1?.total_apg || 0) - (comparisonData.lineup2?.total_apg || 0))}
                            </TableCell>
                          </TableRow>
                          <TableRow>
                            <TableCell component="th" scope="row">Steals Per Game</TableCell>
                            <TableCell align="right">{comparisonData.lineup1?.total_spg?.toFixed(1) || '0.0'}</TableCell>
                            <TableCell align="right">{comparisonData.lineup2?.total_spg?.toFixed(1) || '0.0'}</TableCell>
                            <TableCell align="right" sx={{ color: getStatDiffColor((comparisonData.lineup1?.total_spg || 0) - (comparisonData.lineup2?.total_spg || 0)) }}>
                              {formatStatDiff((comparisonData.lineup1?.total_spg || 0) - (comparisonData.lineup2?.total_spg || 0))}
                            </TableCell>
                          </TableRow>
                          <TableRow>
                            <TableCell component="th" scope="row">Blocks Per Game</TableCell>
                            <TableCell align="right">{comparisonData.lineup1?.total_bpg?.toFixed(1) || '0.0'}</TableCell>
                            <TableCell align="right">{comparisonData.lineup2?.total_bpg?.toFixed(1) || '0.0'}</TableCell>
                            <TableCell align="right" sx={{ color: getStatDiffColor((comparisonData.lineup1?.total_bpg || 0) - (comparisonData.lineup2?.total_bpg || 0)) }}>
                              {formatStatDiff((comparisonData.lineup1?.total_bpg || 0) - (comparisonData.lineup2?.total_bpg || 0))}
                            </TableCell>
                          </TableRow>
                          <TableRow>
                            <TableCell component="th" scope="row">Field Goal %</TableCell>
                            <TableCell align="right">{((comparisonData.lineup1?.total_fg_pct || 0) * 100).toFixed(1)}%</TableCell>
                            <TableCell align="right">{((comparisonData.lineup2?.total_fg_pct || 0) * 100).toFixed(1)}%</TableCell>
                            <TableCell align="right" sx={{ color: getStatDiffColor((comparisonData.lineup1?.total_fg_pct || 0) - (comparisonData.lineup2?.total_fg_pct || 0)) }}>
                              {formatStatDiff(((comparisonData.lineup1?.total_fg_pct || 0) - (comparisonData.lineup2?.total_fg_pct || 0)) * 100)}%
                            </TableCell>
                          </TableRow>
                          <TableRow>
                            <TableCell component="th" scope="row">Three Point %</TableCell>
                            <TableCell align="right">{((comparisonData.lineup1?.total_fg3_pct || 0) * 100).toFixed(1)}%</TableCell>
                            <TableCell align="right">{((comparisonData.lineup2?.total_fg3_pct || 0) * 100).toFixed(1)}%</TableCell>
                            <TableCell align="right" sx={{ color: getStatDiffColor((comparisonData.lineup1?.total_fg3_pct || 0) - (comparisonData.lineup2?.total_fg3_pct || 0)) }}>
                              {formatStatDiff(((comparisonData.lineup1?.total_fg3_pct || 0) - (comparisonData.lineup2?.total_fg3_pct || 0)) * 100)}%
                            </TableCell>
                          </TableRow>
                          <TableRow>
                            <TableCell component="th" scope="row">Free Throw %</TableCell>
                            <TableCell align="right">{((comparisonData.lineup1?.total_ft_pct || 0) * 100).toFixed(1)}%</TableCell>
                            <TableCell align="right">{((comparisonData.lineup2?.total_ft_pct || 0) * 100).toFixed(1)}%</TableCell>
                            <TableCell align="right" sx={{ color: getStatDiffColor((comparisonData.lineup1?.total_ft_pct || 0) - (comparisonData.lineup2?.total_ft_pct || 0)) }}>
                              {formatStatDiff(((comparisonData.lineup1?.total_ft_pct || 0) - (comparisonData.lineup2?.total_ft_pct || 0)) * 100)}%
                            </TableCell>
                          </TableRow>
                        </>
                      )}
                    </TableBody>
                  </Table>
                </TableContainer>
              </Paper>
            </Grid>
          </Grid>
        </>
      ) : (
        <Box sx={{ textAlign: 'center', py: 5 }}>
          <Typography variant="h6" color="text.secondary" gutterBottom>
            Select two lineups to compare their statistics
          </Typography>
          <Typography variant="body1" color="text.secondary">
            The comparison will show detailed stats and player information for both lineups
          </Typography>
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

export default LineupComparison; 