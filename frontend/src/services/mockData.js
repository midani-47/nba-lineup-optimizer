// Mock data for the NBA lineup optimizer app
// This provides fallback data when the API is unavailable

// Mock Players
export const mockPlayers = [
  { player_id: 1, name: 'LeBron James', team: 'LAL', position: 'SF', ppg: 25.7, rpg: 7.3, apg: 7.8, spg: 1.1, bpg: 0.6, fg_pct: 0.538, fg3_pct: 0.365, ft_pct: 0.731, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/2544.png' },
  { player_id: 2, name: 'Kevin Durant', team: 'PHX', position: 'SF', ppg: 27.3, rpg: 6.8, apg: 5.0, spg: 0.7, bpg: 1.2, fg_pct: 0.525, fg3_pct: 0.384, ft_pct: 0.873, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/201142.png' },
  { player_id: 3, name: 'Stephen Curry', team: 'GSW', position: 'PG', ppg: 26.4, rpg: 5.2, apg: 6.3, spg: 1.3, bpg: 0.4, fg_pct: 0.473, fg3_pct: 0.428, ft_pct: 0.915, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/201939.png' },
  { player_id: 4, name: 'Giannis Antetokounmpo', team: 'MIL', position: 'PF', ppg: 29.7, rpg: 11.5, apg: 5.7, spg: 1.1, bpg: 1.3, fg_pct: 0.553, fg3_pct: 0.276, ft_pct: 0.688, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/203507.png' },
  { player_id: 5, name: 'Nikola Jokic', team: 'DEN', position: 'C', ppg: 24.5, rpg: 11.8, apg: 9.8, spg: 1.3, bpg: 0.7, fg_pct: 0.583, fg3_pct: 0.337, ft_pct: 0.822, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/203999.png' },
  { player_id: 6, name: 'Joel Embiid', team: 'PHI', position: 'C', ppg: 33.1, rpg: 10.2, apg: 4.2, spg: 1.0, bpg: 1.7, fg_pct: 0.546, fg3_pct: 0.345, ft_pct: 0.857, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/203954.png' },
  { player_id: 7, name: 'Luka Doncic', team: 'DAL', position: 'PG', ppg: 32.4, rpg: 8.6, apg: 8.0, spg: 1.4, bpg: 0.5, fg_pct: 0.495, fg3_pct: 0.345, ft_pct: 0.745, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/1629029.png' },
  { player_id: 8, name: 'Jayson Tatum', team: 'BOS', position: 'SF', ppg: 26.9, rpg: 8.1, apg: 4.3, spg: 1.0, bpg: 0.7, fg_pct: 0.466, fg3_pct: 0.351, ft_pct: 0.854, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/1628369.png' },
  { player_id: 9, name: 'Ja Morant', team: 'MEM', position: 'PG', ppg: 24.6, rpg: 5.6, apg: 8.1, spg: 1.1, bpg: 0.3, fg_pct: 0.474, fg3_pct: 0.304, ft_pct: 0.749, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/1629630.png' },
  { player_id: 10, name: 'Damian Lillard', team: 'MIL', position: 'PG', ppg: 26.3, rpg: 4.4, apg: 7.0, spg: 0.9, bpg: 0.3, fg_pct: 0.441, fg3_pct: 0.371, ft_pct: 0.907, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/203081.png' },
  { player_id: 11, name: 'Anthony Davis', team: 'LAL', position: 'PF', ppg: 25.9, rpg: 12.5, apg: 2.6, spg: 1.1, bpg: 2.0, fg_pct: 0.552, fg3_pct: 0.254, ft_pct: 0.783, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/203076.png' },
  { player_id: 12, name: 'Devin Booker', team: 'PHX', position: 'SG', ppg: 27.1, rpg: 4.6, apg: 5.5, spg: 1.0, bpg: 0.3, fg_pct: 0.485, fg3_pct: 0.355, ft_pct: 0.859, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/1626164.png' },
  { player_id: 13, name: 'Trae Young', team: 'ATL', position: 'PG', ppg: 26.1, rpg: 3.0, apg: 10.8, spg: 1.1, bpg: 0.1, fg_pct: 0.426, fg3_pct: 0.361, ft_pct: 0.886, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/1629027.png' },
  { player_id: 14, name: 'Jimmy Butler', team: 'MIA', position: 'SF', ppg: 20.8, rpg: 5.5, apg: 5.0, spg: 1.3, bpg: 0.3, fg_pct: 0.495, fg3_pct: 0.345, ft_pct: 0.854, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/202710.png' },
  { player_id: 15, name: 'Kawhi Leonard', team: 'LAC', position: 'SF', ppg: 23.8, rpg: 6.5, apg: 3.9, spg: 1.6, bpg: 0.5, fg_pct: 0.524, fg3_pct: 0.416, ft_pct: 0.879, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/202695.png' },
  { player_id: 16, name: 'Donovan Mitchell', team: 'CLE', position: 'SG', ppg: 27.4, rpg: 5.2, apg: 6.1, spg: 1.8, bpg: 0.4, fg_pct: 0.466, fg3_pct: 0.366, ft_pct: 0.861, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/1628378.png' },
  { player_id: 17, name: 'Jaylen Brown', team: 'BOS', position: 'SG', ppg: 23.6, rpg: 5.5, apg: 3.5, spg: 1.1, bpg: 0.5, fg_pct: 0.491, fg3_pct: 0.335, ft_pct: 0.713, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/1627759.png' },
  { player_id: 18, name: 'Bam Adebayo', team: 'MIA', position: 'C', ppg: 19.3, rpg: 10.4, apg: 3.9, spg: 1.1, bpg: 0.9, fg_pct: 0.541, fg3_pct: 0.000, ft_pct: 0.803, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/1628389.png' },
  { player_id: 19, name: 'Kyrie Irving', team: 'DAL', position: 'PG', ppg: 25.6, rpg: 5.1, apg: 5.2, spg: 1.3, bpg: 0.4, fg_pct: 0.499, fg3_pct: 0.412, ft_pct: 0.904, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/202681.png' },
  { player_id: 20, name: 'Zion Williamson', team: 'NOP', position: 'PF', ppg: 22.9, rpg: 6.8, apg: 4.9, spg: 1.1, bpg: 0.7, fg_pct: 0.594, fg3_pct: 0.333, ft_pct: 0.699, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/1629627.png' },
  { player_id: 21, name: 'Victor Wembanyama', team: 'SAS', position: 'C', ppg: 21.4, rpg: 10.6, apg: 3.9, spg: 1.2, bpg: 3.6, fg_pct: 0.467, fg3_pct: 0.328, ft_pct: 0.802, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/1641705.png' },
  { player_id: 22, name: 'Chet Holmgren', team: 'OKC', position: 'C', ppg: 16.5, rpg: 7.9, apg: 2.4, spg: 0.7, bpg: 2.3, fg_pct: 0.530, fg3_pct: 0.372, ft_pct: 0.787, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/1631096.png' },
  { player_id: 23, name: 'Paolo Banchero', team: 'ORL', position: 'PF', ppg: 22.6, rpg: 6.9, apg: 5.4, spg: 0.9, bpg: 0.6, fg_pct: 0.459, fg3_pct: 0.338, ft_pct: 0.756, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/1631094.png' },
  { player_id: 24, name: 'Anthony Edwards', team: 'MIN', position: 'SG', ppg: 25.9, rpg: 5.4, apg: 5.1, spg: 1.3, bpg: 0.5, fg_pct: 0.461, fg3_pct: 0.352, ft_pct: 0.833, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/1630162.png' },
  { player_id: 25, name: 'Shai Gilgeous-Alexander', team: 'OKC', position: 'PG', ppg: 30.1, rpg: 5.5, apg: 6.2, spg: 2.0, bpg: 0.9, fg_pct: 0.534, fg3_pct: 0.355, ft_pct: 0.874, image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/1628983.png' },
];

// Mock Lineups
export const mockLineups = [
  {
    id: 1,
    name: 'All-Star Team',
    players: mockPlayers.slice(0, 5),
    total_ppg: 133.6,
    total_rpg: 42.3,
    total_apg: 34.6,
    total_spg: 5.5,
    total_bpg: 4.2,
    total_fg_pct: 0.534,
    total_fg3_pct: 0.358,
    total_ft_pct: 0.806
  },
  {
    id: 2,
    name: 'Dream Team',
    players: mockPlayers.slice(5, 10),
    total_ppg: 143.3,
    total_rpg: 36.9,
    total_apg: 31.6,
    total_spg: 5.9,
    total_bpg: 3.7,
    total_fg_pct: 0.504,
    total_fg3_pct: 0.349,
    total_ft_pct: 0.822
  },
  {
    id: 3,
    name: 'Young Guns',
    players: [mockPlayers[6], mockPlayers[7], mockPlayers[8], mockPlayers[11], mockPlayers[16]],
    total_ppg: 134.1,
    total_rpg: 32.0,
    total_apg: 30.2,
    total_spg: 5.6,
    total_bpg: 2.6,
    total_fg_pct: 0.482,
    total_fg3_pct: 0.339,
    total_ft_pct: 0.804
  }
];

// Mock Dashboard Stats
export const mockDashboardStats = {
  topScorers: [
    mockPlayers[6], // Luka
    mockPlayers[5], // Embiid
    mockPlayers[3], // Giannis
    mockPlayers[1], // Durant
    mockPlayers[15] // Mitchell
  ],
  topRebounders: [
    mockPlayers[10], // Davis
    mockPlayers[4], // Jokic
    mockPlayers[3], // Giannis
    mockPlayers[5], // Embiid
    mockPlayers[17] // Adebayo
  ],
  topAssists: [
    mockPlayers[12], // Trae
    mockPlayers[4], // Jokic
    mockPlayers[8], // Morant
    mockPlayers[0], // LeBron
    mockPlayers[6] // Luka
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
  topPerformances: [
    { player_id: 1, name: 'LeBron James', team: 'LAL', points: 45, rebounds: 12, assists: 8, date: '2023-11-15', opponent: 'LAC', image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/2544.png' },
    { player_id: 6, name: 'Luka Doncic', team: 'DAL', points: 42, rebounds: 15, assists: 5, date: '2023-11-14', opponent: 'DET', image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/1629029.png' },
    { player_id: 4, name: 'Nikola Jokic', team: 'DEN', points: 35, rebounds: 14, assists: 12, date: '2023-11-13', opponent: 'NOP', image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/203999.png' },
    { player_id: 3, name: 'Giannis Antetokounmpo', team: 'MIL', points: 40, rebounds: 16, assists: 7, date: '2023-11-12', opponent: 'PHX', image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/203507.png' },
    { player_id: 5, name: 'Joel Embiid', team: 'PHI', points: 38, rebounds: 9, assists: 12, date: '2023-11-11', opponent: 'BKN', image_url: 'https://cdn.nba.com/headshots/nba/latest/1040x760/203954.png' },
  ]
};

// Mock Player Detail
export const getPlayerDetail = (playerId) => {
  const player = mockPlayers.find(p => p.player_id === Number(playerId));
  if (!player) return null;
  
  return {
    ...player,
    games_played: 82,
    minutes: 34.6,
    efficiency: ((player.ppg + player.rpg + player.apg) / 3).toFixed(1),
    recent_games: [
      { date: '2023-11-15', opponent: 'LAC', points: 32, rebounds: 8, assists: 7, minutes: 36 },
      { date: '2023-11-13', opponent: 'DET', points: 28, rebounds: 6, assists: 9, minutes: 34 },
      { date: '2023-11-11', opponent: 'NOP', points: 25, rebounds: 7, assists: 8, minutes: 35 },
      { date: '2023-11-09', opponent: 'PHX', points: 30, rebounds: 9, assists: 6, minutes: 37 },
      { date: '2023-11-07', opponent: 'BKN', points: 27, rebounds: 5, assists: 10, minutes: 33 },
    ],
    season_highs: {
      points: 45,
      rebounds: 15,
      assists: 12,
      steals: 4,
      blocks: 3,
      minutes: 42
    }
  };
};

// Mock Lineup Comparison
export const mockCompareLineups = (lineup1Id, lineup2Id) => {
  const lineup1 = mockLineups.find(l => l.id === Number(lineup1Id));
  const lineup2 = mockLineups.find(l => l.id === Number(lineup2Id));
  
  if (!lineup1 || !lineup2) return null;
  
  return {
    lineup1,
    lineup2,
    stat_diff: {
      ppg: lineup1.total_ppg - lineup2.total_ppg,
      rpg: lineup1.total_rpg - lineup2.total_rpg,
      apg: lineup1.total_apg - lineup2.total_apg,
      spg: lineup1.total_spg - lineup2.total_spg,
      bpg: lineup1.total_bpg - lineup2.total_bpg,
      fg_pct: lineup1.total_fg_pct - lineup2.total_fg_pct,
      fg3_pct: lineup1.total_fg3_pct - lineup2.total_fg3_pct,
      ft_pct: lineup1.total_ft_pct - lineup2.total_ft_pct,
    }
  };
};

// Mock Optimize Lineup
export const mockOptimizeLineup = (lineupId, strategy) => {
  const lineup = mockLineups.find(l => l.id === Number(lineupId));
  if (!lineup) return null;
  
  // Simulate optimization by selecting different players based on strategy
  let optimizedPlayers;
  switch (strategy) {
    case 'scoring':
      optimizedPlayers = mockPlayers.sort((a, b) => b.ppg - a.ppg).slice(0, 5);
      break;
    case 'defense':
      optimizedPlayers = mockPlayers.sort((a, b) => (b.spg + b.bpg) - (a.spg + a.bpg)).slice(0, 5);
      break;
    case 'balanced':
    default:
      optimizedPlayers = mockPlayers.sort((a, b) => {
        const aScore = a.ppg + a.rpg + a.apg + a.spg + a.bpg;
        const bScore = b.ppg + b.rpg + b.apg + b.spg + b.bpg;
        return bScore - aScore;
      }).slice(0, 5);
  }
  
  return {
    original_lineup: lineup,
    optimized_lineup: {
      name: `${lineup.name} (Optimized - ${strategy})`,
      players: optimizedPlayers,
      total_ppg: optimizedPlayers.reduce((sum, p) => sum + p.ppg, 0),
      total_rpg: optimizedPlayers.reduce((sum, p) => sum + p.rpg, 0),
      total_apg: optimizedPlayers.reduce((sum, p) => sum + p.apg, 0),
      total_spg: optimizedPlayers.reduce((sum, p) => sum + p.spg, 0),
      total_bpg: optimizedPlayers.reduce((sum, p) => sum + p.bpg, 0),
      total_fg_pct: optimizedPlayers.reduce((sum, p) => sum + p.fg_pct, 0) / 5,
      total_fg3_pct: optimizedPlayers.reduce((sum, p) => sum + p.fg3_pct, 0) / 5,
      total_ft_pct: optimizedPlayers.reduce((sum, p) => sum + p.ft_pct, 0) / 5,
    },
    improvement: {
      ppg: optimizedPlayers.reduce((sum, p) => sum + p.ppg, 0) - lineup.total_ppg,
      rpg: optimizedPlayers.reduce((sum, p) => sum + p.rpg, 0) - lineup.total_rpg,
      apg: optimizedPlayers.reduce((sum, p) => sum + p.apg, 0) - lineup.total_apg,
    }
  };
}; 