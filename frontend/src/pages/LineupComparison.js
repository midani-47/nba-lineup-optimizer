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

  const handleCompare = async () => {
    if (!lineup1 || !lineup2) {
      return;
    }

    try {
      setComparisonLoading(true);
      const data = await compareLineups(lineup1, lineup2);
      setComparisonData(data);
    } catch (error) {
      console.error('Error comparing lineups:', error);
    } finally {
      setComparisonLoading(false);
    }
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
    if (!comparisonData) return [];

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
        id: comparisonData.lineup1.name,
        color: '#1976d2',
        data: stats.map(stat => {
          let value = comparisonData.lineup1[`total_${stat}`];
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
        id: comparisonData.lineup2.name,
        color: '#f50057',
        data: stats.map(stat => {
          let value = comparisonData.lineup2[`total_${stat}`];
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
                {lineups.map((lineup) => (
                  <MenuItem key={`lineup1-${lineup.id}`} value={lineup.id}>
                    {lineup.name}
                  </MenuItem>
                ))}
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
                {lineups.map((lineup) => (
                  <MenuItem key={`lineup2-${lineup.id}`} value={lineup.id}>
                    {lineup.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          
          <Grid item xs={12} sx={{ textAlign: 'center', mt: 2 }}>
            <Button
              variant="contained"
              color="primary"
              onClick={handleCompare}
              disabled={!lineup1 || !lineup2 || lineup1 === lineup2}
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
                tooltip={({ point }) => {
                  return (
                    <div
                      style={{
                        background: 'rgba(0, 0, 0, 0.8)',
                        color: '#fff',
                        padding: '9px 12px',
                        border: '1px solid #ccc',
                        borderRadius: '4px',
                      }}
                    >
                      <div>{point.serieId}: {point.data.y.toFixed(1)}</div>
                      <div>{point.data.x}</div>
                    </div>
                  );
                }}
              />
            </Box>
          </Paper>
          
          {/* Detailed Stats Comparison */}
          <Paper sx={{ p: 3, mb: 4 }} elevation={3}>
            <Typography variant="h6" gutterBottom>
              Team Statistics Comparison
            </Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Stat</TableCell>
                    <TableCell align="right" sx={{ color: '#1976d2' }}>
                      {comparisonData.lineup1.name}
                    </TableCell>
                    <TableCell align="right" sx={{ color: '#f50057' }}>
                      {comparisonData.lineup2.name}
                    </TableCell>
                    <TableCell align="right">Difference</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  <TableRow>
                    <TableCell component="th" scope="row">Points Per Game</TableCell>
                    <TableCell align="right">{comparisonData.lineup1.total_ppg.toFixed(1)}</TableCell>
                    <TableCell align="right">{comparisonData.lineup2.total_ppg.toFixed(1)}</TableCell>
                    <TableCell align="right" sx={{ color: getStatDiffColor(comparisonData.stat_diff.ppg) }}>
                      {formatStatDiff(comparisonData.stat_diff.ppg)}
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell component="th" scope="row">Rebounds Per Game</TableCell>
                    <TableCell align="right">{comparisonData.lineup1.total_rpg.toFixed(1)}</TableCell>
                    <TableCell align="right">{comparisonData.lineup2.total_rpg.toFixed(1)}</TableCell>
                    <TableCell align="right" sx={{ color: getStatDiffColor(comparisonData.stat_diff.rpg) }}>
                      {formatStatDiff(comparisonData.stat_diff.rpg)}
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell component="th" scope="row">Assists Per Game</TableCell>
                    <TableCell align="right">{comparisonData.lineup1.total_apg.toFixed(1)}</TableCell>
                    <TableCell align="right">{comparisonData.lineup2.total_apg.toFixed(1)}</TableCell>
                    <TableCell align="right" sx={{ color: getStatDiffColor(comparisonData.stat_diff.apg) }}>
                      {formatStatDiff(comparisonData.stat_diff.apg)}
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell component="th" scope="row">Steals Per Game</TableCell>
                    <TableCell align="right">{comparisonData.lineup1.total_spg.toFixed(1)}</TableCell>
                    <TableCell align="right">{comparisonData.lineup2.total_spg.toFixed(1)}</TableCell>
                    <TableCell align="right" sx={{ color: getStatDiffColor(comparisonData.stat_diff.spg) }}>
                      {formatStatDiff(comparisonData.stat_diff.spg)}
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell component="th" scope="row">Blocks Per Game</TableCell>
                    <TableCell align="right">{comparisonData.lineup1.total_bpg.toFixed(1)}</TableCell>
                    <TableCell align="right">{comparisonData.lineup2.total_bpg.toFixed(1)}</TableCell>
                    <TableCell align="right" sx={{ color: getStatDiffColor(comparisonData.stat_diff.bpg) }}>
                      {formatStatDiff(comparisonData.stat_diff.bpg)}
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell component="th" scope="row">Field Goal %</TableCell>
                    <TableCell align="right">{(comparisonData.lineup1.total_fg_pct * 100).toFixed(1)}%</TableCell>
                    <TableCell align="right">{(comparisonData.lineup2.total_fg_pct * 100).toFixed(1)}%</TableCell>
                    <TableCell align="right" sx={{ color: getStatDiffColor(comparisonData.stat_diff.fg_pct * 100) }}>
                      {formatStatDiff(comparisonData.stat_diff.fg_pct * 100)}%
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell component="th" scope="row">Three Point %</TableCell>
                    <TableCell align="right">{(comparisonData.lineup1.total_fg3_pct * 100).toFixed(1)}%</TableCell>
                    <TableCell align="right">{(comparisonData.lineup2.total_fg3_pct * 100).toFixed(1)}%</TableCell>
                    <TableCell align="right" sx={{ color: getStatDiffColor(comparisonData.stat_diff.fg3_pct * 100) }}>
                      {formatStatDiff(comparisonData.stat_diff.fg3_pct * 100)}%
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell component="th" scope="row">Free Throw %</TableCell>
                    <TableCell align="right">{(comparisonData.lineup1.total_ft_pct * 100).toFixed(1)}%</TableCell>
                    <TableCell align="right">{(comparisonData.lineup2.total_ft_pct * 100).toFixed(1)}%</TableCell>
                    <TableCell align="right" sx={{ color: getStatDiffColor(comparisonData.stat_diff.ft_pct * 100) }}>
                      {formatStatDiff(comparisonData.stat_diff.ft_pct * 100)}%
                    </TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
          
          {/* Lineup Details */}
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 3, height: '100%' }} elevation={3}>
                <Typography variant="h6" gutterBottom sx={{ color: '#1976d2' }}>
                  {comparisonData.lineup1.name}
                </Typography>
                <Divider sx={{ mb: 2, borderColor: '#1976d2' }} />
                {comparisonData.lineup1.players.map((player) => (
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
              </Paper>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 3, height: '100%' }} elevation={3}>
                <Typography variant="h6" gutterBottom sx={{ color: '#f50057' }}>
                  {comparisonData.lineup2.name}
                </Typography>
                <Divider sx={{ mb: 2, borderColor: '#f50057' }} />
                {comparisonData.lineup2.players.map((player) => (
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
              </Paper>
            </Grid>
          </Grid>
        </>
      ) : (
        <Box sx={{ textAlign: 'center', py: 8 }}>
          <Typography variant="h6" color="text.secondary">
            Select two lineups to compare
          </Typography>
        </Box>
      )}
    </Container>
  );
};

export default LineupComparison; 