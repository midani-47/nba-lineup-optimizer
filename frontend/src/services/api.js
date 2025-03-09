import axios from 'axios';
import { 
  mockPlayers, 
  mockLineups, 
  mockDashboardStats, 
  getPlayerDetail, 
  mockCompareLineups, 
  mockOptimizeLineup 
} from './mockData';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001/api';

// Create a cache for API responses
const apiCache = new Map();

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  // Add timeout to prevent hanging requests
  timeout: 10000,
});

// Add response interceptor for error handling
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error);
    if (error.code === 'ECONNABORTED') {
      console.error('Request timeout');
    }
    return Promise.reject(error);
  }
);

// Helper function to get cached data or fetch from API
const getCachedOrFetch = async (key, fetchFunction) => {
  // Check if we have cached data and it's less than 5 minutes old
  if (apiCache.has(key)) {
    const { data, timestamp } = apiCache.get(key);
    const fiveMinutes = 5 * 60 * 1000;
    if (Date.now() - timestamp < fiveMinutes) {
      return data;
    }
  }
  
  // If no cache or cache is old, fetch new data
  const data = await fetchFunction();
  apiCache.set(key, { data, timestamp: Date.now() });
  return data;
};

// Players
export const getPlayers = async (params = {}) => {
  try {
    const cacheKey = `players-${JSON.stringify(params)}`;
    return await getCachedOrFetch(cacheKey, async () => {
      // For development, always use mock data to ensure data is available
      console.log('Using mock player data');
      
      // Generate additional players if mockPlayers has fewer than 100 players (reduced from 500)
      if (mockPlayers.length < 100) {
        console.log(`Extending mock data from ${mockPlayers.length} to 100 players`);
        const teams = ['ATL', 'BOS', 'BKN', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 
                      'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 
                      'OKC', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS'];
        const positions = ['PG', 'SG', 'SF', 'PF', 'C'];
        const firstNames = ['James', 'John', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Joseph', 'Thomas', 'Charles',
                           'Anthony', 'Kevin', 'Mark', 'Jason', 'Matthew'];
        const lastNames = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor',
                          'Anderson', 'Thomas', 'Jackson', 'White', 'Harris'];
        
        // Create additional players
        const additionalPlayers = [];
        const existingIds = new Set(mockPlayers.map(p => p.player_id));
        
        for (let i = 0; i < 100 - mockPlayers.length; i++) {
          let playerId = Math.floor(Math.random() * 1000000) + 100;
          // Ensure unique ID
          while (existingIds.has(playerId)) {
            playerId = Math.floor(Math.random() * 1000000) + 100;
          }
          existingIds.add(playerId);
          
          const firstName = firstNames[Math.floor(Math.random() * firstNames.length)];
          const lastName = lastNames[Math.floor(Math.random() * lastNames.length)];
          const team = teams[Math.floor(Math.random() * teams.length)];
          const position = positions[Math.floor(Math.random() * positions.length)];
          
          // Use NBA slogan instead of robohash cat images
          const imageUrl = `https://via.placeholder.com/50x50/1a428a/ffffff?text=NBA`;
          
          additionalPlayers.push({
            player_id: playerId,
            name: `${firstName} ${lastName}`,
            team,
            position,
            ppg: +(Math.random() * 20 + 2).toFixed(1),
            rpg: +(Math.random() * 10 + 1).toFixed(1),
            apg: +(Math.random() * 8 + 0.5).toFixed(1),
            spg: +(Math.random() * 2 + 0.1).toFixed(1),
            bpg: +(Math.random() * 1.5 + 0.1).toFixed(1),
            fg_pct: +(Math.random() * 0.2 + 0.4).toFixed(3),
            fg3_pct: +(Math.random() * 0.2 + 0.3).toFixed(3),
            ft_pct: +(Math.random() * 0.2 + 0.7).toFixed(3),
            image_url: imageUrl
          });
        }
        
        // Return combined array of original mock players plus additional players
        return [...mockPlayers, ...additionalPlayers];
      }
      
      return mockPlayers;
      
      // Uncomment for production:
      // const response = await api.get('/players/', { params });
      // return response.data;
    });
  } catch (error) {
    console.error('Error fetching players:', error);
    console.log('Using mock player data as fallback');
    return mockPlayers;
  }
};

export const getPlayerById = async (playerId) => {
  try {
    const cacheKey = `player-${playerId}`;
    return await getCachedOrFetch(cacheKey, async () => {
      // For development, always use mock data
      console.log(`Using mock data for player ${playerId}`);
      
      // First check if the player exists in the original mockPlayers array
      let playerDetail = getPlayerDetail(playerId);
      
      // If not found in original mockPlayers, check if it's a dynamically generated player
      if (!playerDetail) {
        console.log(`Player ${playerId} not found in original mock data, checking dynamic players`);
        
        // Get all players (including dynamically generated ones)
        const allPlayers = await getPlayers();
        
        // Find the player by ID
        const player = allPlayers.find(p => p.player_id === Number(playerId));
        
        if (player) {
          // Create simplified player detail for dynamically generated player
          playerDetail = {
            ...player,
            games_played: Math.floor(Math.random() * 30) + 50, // Random games played between 50-80
            minutes: (Math.random() * 10 + 25).toFixed(1), // Random minutes between 25-35
            efficiency: ((player.ppg + player.rpg + player.apg) / 3).toFixed(1),
            // Simplified recent games data with fewer entries
            recent_games: [
              { date: '2023-11-15', opponent: 'LAC', points: Math.floor(player.ppg * (0.8 + Math.random() * 0.4)), rebounds: Math.floor(player.rpg * (0.8 + Math.random() * 0.4)), assists: Math.floor(player.apg * (0.8 + Math.random() * 0.4)), minutes: Math.floor(Math.random() * 10 + 30) },
              { date: '2023-11-13', opponent: 'DET', points: Math.floor(player.ppg * (0.8 + Math.random() * 0.4)), rebounds: Math.floor(player.rpg * (0.8 + Math.random() * 0.4)), assists: Math.floor(player.apg * (0.8 + Math.random() * 0.4)), minutes: Math.floor(Math.random() * 10 + 30) },
              { date: '2023-11-11', opponent: 'NOP', points: Math.floor(player.ppg * (0.8 + Math.random() * 0.4)), rebounds: Math.floor(player.rpg * (0.8 + Math.random() * 0.4)), assists: Math.floor(player.apg * (0.8 + Math.random() * 0.4)), minutes: Math.floor(Math.random() * 10 + 30) }
            ],
            season_highs: {
              points: Math.floor(player.ppg * 1.5),
              rebounds: Math.floor(player.rpg * 1.5),
              assists: Math.floor(player.apg * 1.5),
              steals: Math.floor(player.spg * 2),
              blocks: Math.floor(player.bpg * 2),
              minutes: Math.floor(Math.random() * 5 + 40)
            }
          };
        }
      }
      
      return playerDetail;
      
      // Uncomment for production:
      // const response = await api.get(`/players/${playerId}/`);
      // return response.data;
    });
  } catch (error) {
    console.error(`Error fetching player ${playerId}:`, error);
    console.log('Using mock player detail data as fallback');
    return getPlayerDetail(playerId);
  }
};

// Lineups
export const getLineups = async () => {
  try {
    // For development, use mock data and localStorage
    console.log('Using mock lineup data and localStorage');
    
    // Try to get lineups from localStorage
    let storedLineups = [];
    try {
      storedLineups = JSON.parse(localStorage.getItem('nba_lineups') || '[]');
      console.log('Retrieved lineups from localStorage:', storedLineups.length);
    } catch (storageError) {
      console.error('Error retrieving lineups from localStorage:', storageError);
    }
    
    // Combine mock lineups with stored lineups, avoiding duplicates
    const combinedLineups = [...mockLineups];
    
    // Add stored lineups that aren't already in mockLineups
    storedLineups.forEach(storedLineup => {
      if (!combinedLineups.some(l => l.id === storedLineup.id)) {
        combinedLineups.push(storedLineup);
      }
    });
    
    console.log('Total lineups available:', combinedLineups.length);
    return combinedLineups;
    
    // Uncomment for production:
    // const response = await api.get('/lineups/');
    // return response.data;
  } catch (error) {
    console.error('Error fetching lineups:', error);
    console.log('Using mock lineup data as fallback');
    
    // Try to get lineups from localStorage as a last resort
    try {
      const storedLineups = JSON.parse(localStorage.getItem('nba_lineups') || '[]');
      return [...mockLineups, ...storedLineups];
    } catch (storageError) {
      console.error('Error retrieving lineups from localStorage:', storageError);
      return mockLineups;
    }
  }
};

export const getLineupById = async (lineupId) => {
  try {
    console.log(`Fetching lineup with ID ${lineupId}`);
    
    // First check mock lineups
    let lineup = mockLineups.find(l => l.id === Number(lineupId));
    
    // If not found in mock lineups, check localStorage
    if (!lineup) {
      try {
        const storedLineups = JSON.parse(localStorage.getItem('nba_lineups') || '[]');
        lineup = storedLineups.find(l => l.id === Number(lineupId));
        console.log(`Lineup ${lineupId} found in localStorage:`, !!lineup);
      } catch (storageError) {
        console.error('Error retrieving lineups from localStorage:', storageError);
      }
    }
    
    if (!lineup) {
      throw new Error(`Lineup with ID ${lineupId} not found`);
    }
    
    return lineup;
    
    // Uncomment for production:
    // const response = await api.get(`/lineups/${lineupId}/`);
    // return response.data;
  } catch (error) {
    console.error(`Error fetching lineup ${lineupId}:`, error);
    
    // Last attempt to find the lineup in localStorage
    try {
      const storedLineups = JSON.parse(localStorage.getItem('nba_lineups') || '[]');
      const lineup = storedLineups.find(l => l.id === Number(lineupId));
      if (lineup) return lineup;
    } catch (storageError) {
      console.error('Error in last attempt to retrieve from localStorage:', storageError);
    }
    
    // If all else fails, check mock lineups again
    return mockLineups.find(l => l.id === Number(lineupId)) || null;
  }
};

export const createLineup = async (lineupData) => {
  try {
    const response = await api.post('/lineups/', lineupData);
    return response.data;
  } catch (error) {
    console.error('Error creating lineup:', error);
    console.log('Using mock lineup creation as fallback');
    
    // Get all players to ensure we have the complete data
    const allPlayers = await getPlayers();
    
    // Create a mock lineup with a new ID
    let storedLineups = [];
    try {
      storedLineups = JSON.parse(localStorage.getItem('nba_lineups') || '[]');
    } catch (storageError) {
      console.error('Error retrieving lineups from localStorage:', storageError);
    }
    
    const mockIds = mockLineups.map(l => l.id);
    const storedIds = storedLineups.map(l => l.id);
    const allIds = [...mockIds, ...storedIds];
    const newId = allIds.length > 0 ? Math.max(...allIds) + 1 : 1;
    
    // Find full player objects for each player ID
    const playerObjects = lineupData.players.map(id => 
      allPlayers.find(p => p.player_id === Number(id))
    ).filter(Boolean);
    
    // Calculate totals first to ensure they're set correctly
    let total_ppg = 0;
    let total_rpg = 0;
    let total_apg = 0;
    let total_spg = 0;
    let total_bpg = 0;
    let total_fg_pct = 0;
    let total_fg3_pct = 0;
    let total_ft_pct = 0;
    
    if (playerObjects.length > 0) {
      total_ppg = playerObjects.reduce((sum, p) => sum + (p.ppg || 0), 0);
      total_rpg = playerObjects.reduce((sum, p) => sum + (p.rpg || 0), 0);
      total_apg = playerObjects.reduce((sum, p) => sum + (p.apg || 0), 0);
      total_spg = playerObjects.reduce((sum, p) => sum + (p.spg || 0), 0);
      total_bpg = playerObjects.reduce((sum, p) => sum + (p.bpg || 0), 0);
      total_fg_pct = playerObjects.reduce((sum, p) => sum + (p.fg_pct || 0), 0) / playerObjects.length;
      total_fg3_pct = playerObjects.reduce((sum, p) => sum + (p.fg3_pct || 0), 0) / playerObjects.length;
      total_ft_pct = playerObjects.reduce((sum, p) => sum + (p.ft_pct || 0), 0) / playerObjects.length;
    }
    
    const newLineup = {
      id: newId,
      name: lineupData.name,
      players: playerObjects,
      total_ppg,
      total_rpg,
      total_apg,
      total_spg,
      total_bpg,
      total_fg_pct,
      total_fg3_pct,
      total_ft_pct,
      created_at: new Date().toISOString() // Add timestamp
    };
    
    // Add to mock lineups (in memory only)
    mockLineups.push(newLineup);
    
    // Store in localStorage for persistence
    try {
      storedLineups.push(newLineup);
      localStorage.setItem('nba_lineups', JSON.stringify(storedLineups));
      console.log('Lineup saved to localStorage:', newLineup);
    } catch (storageError) {
      console.error('Error storing lineup in localStorage:', storageError);
    }
    
    return newLineup;
  }
};

export const updateLineup = async (lineupId, lineupData) => {
  try {
    const response = await api.put(`/lineups/${lineupId}/`, lineupData);
    return response.data;
  } catch (error) {
    console.error(`Error updating lineup ${lineupId}:`, error);
    console.log('Using mock lineup update as fallback');
    
    // Get all players to ensure we have the complete data
    const allPlayers = await getPlayers();
    
    // Check mock lineups first
    const lineupIndex = mockLineups.findIndex(l => l.id === Number(lineupId));
    let updatedLineup = null;
    let inMockLineups = false;
    
    if (lineupIndex !== -1) {
      inMockLineups = true;
      
      // Find full player objects for each player ID
      const playerObjects = lineupData.players.map(id => 
        allPlayers.find(p => p.player_id === Number(id))
      ).filter(Boolean);
      
      updatedLineup = {
        ...mockLineups[lineupIndex],
        name: lineupData.name,
        players: playerObjects
      };
      
      // Recalculate totals
      if (updatedLineup.players.length > 0) {
        updatedLineup.total_ppg = updatedLineup.players.reduce((sum, p) => sum + (p.ppg || 0), 0);
        updatedLineup.total_rpg = updatedLineup.players.reduce((sum, p) => sum + (p.rpg || 0), 0);
        updatedLineup.total_apg = updatedLineup.players.reduce((sum, p) => sum + (p.apg || 0), 0);
        updatedLineup.total_spg = updatedLineup.players.reduce((sum, p) => sum + (p.spg || 0), 0);
        updatedLineup.total_bpg = updatedLineup.players.reduce((sum, p) => sum + (p.bpg || 0), 0);
        updatedLineup.total_fg_pct = updatedLineup.players.reduce((sum, p) => sum + (p.fg_pct || 0), 0) / updatedLineup.players.length;
        updatedLineup.total_fg3_pct = updatedLineup.players.reduce((sum, p) => sum + (p.fg3_pct || 0), 0) / updatedLineup.players.length;
        updatedLineup.total_ft_pct = updatedLineup.players.reduce((sum, p) => sum + (p.ft_pct || 0), 0) / updatedLineup.players.length;
      }
      
      // Update in mock lineups (in memory only)
      mockLineups[lineupIndex] = updatedLineup;
    }
    
    // Now check localStorage
    try {
      let storedLineups = JSON.parse(localStorage.getItem('nba_lineups') || '[]');
      const storedIndex = storedLineups.findIndex(l => l.id === Number(lineupId));
      
      if (storedIndex !== -1) {
        // If we already updated in mock lineups, use that updated lineup
        if (inMockLineups && updatedLineup) {
          storedLineups[storedIndex] = updatedLineup;
        } else {
          // Otherwise create a new updated lineup
          const playerObjects = lineupData.players.map(id => 
            allPlayers.find(p => p.player_id === Number(id))
          ).filter(Boolean);
          
          updatedLineup = {
            ...storedLineups[storedIndex],
            name: lineupData.name,
            players: playerObjects
          };
          
          // Recalculate totals
          if (updatedLineup.players.length > 0) {
            updatedLineup.total_ppg = updatedLineup.players.reduce((sum, p) => sum + (p.ppg || 0), 0);
            updatedLineup.total_rpg = updatedLineup.players.reduce((sum, p) => sum + (p.rpg || 0), 0);
            updatedLineup.total_apg = updatedLineup.players.reduce((sum, p) => sum + (p.apg || 0), 0);
            updatedLineup.total_spg = updatedLineup.players.reduce((sum, p) => sum + (p.spg || 0), 0);
            updatedLineup.total_bpg = updatedLineup.players.reduce((sum, p) => sum + (p.bpg || 0), 0);
            updatedLineup.total_fg_pct = updatedLineup.players.reduce((sum, p) => sum + (p.fg_pct || 0), 0) / updatedLineup.players.length;
            updatedLineup.total_fg3_pct = updatedLineup.players.reduce((sum, p) => sum + (p.fg3_pct || 0), 0) / updatedLineup.players.length;
            updatedLineup.total_ft_pct = updatedLineup.players.reduce((sum, p) => sum + (p.ft_pct || 0), 0) / updatedLineup.players.length;
          }
          
          storedLineups[storedIndex] = updatedLineup;
        }
      } else if (updatedLineup) {
        // If not found in localStorage but we have an updated lineup from mock lineups, add it
        storedLineups.push(updatedLineup);
      }
      
      // Save back to localStorage
      localStorage.setItem('nba_lineups', JSON.stringify(storedLineups));
      console.log('Updated lineup saved to localStorage:', updatedLineup);
    } catch (storageError) {
      console.error('Error updating lineup in localStorage:', storageError);
    }
    
    return updatedLineup;
  }
};

export const deleteLineup = async (lineupId) => {
  try {
    const response = await api.delete(`/lineups/${lineupId}/`);
    return response.data;
  } catch (error) {
    console.error(`Error deleting lineup ${lineupId}:`, error);
    console.log('Using mock lineup deletion as fallback');
    
    let success = false;
    
    // Remove from mock lineups (in memory)
    const lineupIndex = mockLineups.findIndex(l => l.id === Number(lineupId));
    if (lineupIndex !== -1) {
      mockLineups.splice(lineupIndex, 1);
      success = true;
    }
    
    // Remove from localStorage
    try {
      let storedLineups = JSON.parse(localStorage.getItem('nba_lineups') || '[]');
      const initialLength = storedLineups.length;
      storedLineups = storedLineups.filter(l => l.id !== Number(lineupId));
      
      if (storedLineups.length !== initialLength) {
        success = true;
      }
      
      localStorage.setItem('nba_lineups', JSON.stringify(storedLineups));
      console.log(`Lineup ${lineupId} removed from localStorage`);
    } catch (storageError) {
      console.error('Error removing lineup from localStorage:', storageError);
    }
    
    return { success };
  }
};

// Lineup Optimization
export const optimizeLineup = async (lineupId, strategy) => {
  try {
    // For development, use mock data
    console.log(`Optimizing lineup ${lineupId} with strategy ${strategy}`);
    
    // Get all lineups (including user-created ones)
    const allLineups = await getLineups();
    
    // Find the lineup by ID
    const lineup = allLineups.find(l => l.id === Number(lineupId));
    
    if (!lineup) {
      console.error(`Lineup with ID ${lineupId} not found`);
      throw new Error(`Lineup with ID ${lineupId} not found`);
    }
    
    // Get all players for optimization
    const allPlayers = await getPlayers();
    
    // Simulate optimization based on strategy
    let optimizedPlayers;
    switch (strategy) {
      case 'scoring':
        optimizedPlayers = allPlayers.sort((a, b) => b.ppg - a.ppg).slice(0, 5);
        break;
      case 'defense':
        optimizedPlayers = allPlayers.sort((a, b) => (b.spg + b.bpg) - (a.spg + a.bpg)).slice(0, 5);
        break;
      case 'balanced':
      default:
        optimizedPlayers = allPlayers.sort((a, b) => {
          const aScore = a.ppg + a.rpg + a.apg + a.spg + a.bpg;
          const bScore = b.ppg + b.rpg + b.apg + b.spg + b.bpg;
          return bScore - aScore;
        }).slice(0, 5);
    }
    
    // Calculate totals for optimized lineup
    const total_ppg = optimizedPlayers.reduce((sum, p) => sum + p.ppg, 0);
    const total_rpg = optimizedPlayers.reduce((sum, p) => sum + p.rpg, 0);
    const total_apg = optimizedPlayers.reduce((sum, p) => sum + p.apg, 0);
    const total_spg = optimizedPlayers.reduce((sum, p) => sum + p.spg, 0);
    const total_bpg = optimizedPlayers.reduce((sum, p) => sum + p.bpg, 0);
    const total_fg_pct = optimizedPlayers.reduce((sum, p) => sum + p.fg_pct, 0) / 5;
    const total_fg3_pct = optimizedPlayers.reduce((sum, p) => sum + p.fg3_pct, 0) / 5;
    const total_ft_pct = optimizedPlayers.reduce((sum, p) => sum + p.ft_pct, 0) / 5;
    
    // Create optimized lineup object
    const optimizedLineup = {
      name: `${lineup.name} (Optimized - ${strategy})`,
      players: optimizedPlayers,
      total_ppg,
      total_rpg,
      total_apg,
      total_spg,
      total_bpg,
      total_fg_pct,
      total_fg3_pct,
      total_ft_pct
    };
    
    return optimizedLineup;
    
    // Uncomment for production:
    // const response = await api.post(`/lineups/${lineupId}/optimize/`, { strategy });
    // return response.data;
  } catch (error) {
    console.error(`Error optimizing lineup ${lineupId}:`, error);
    console.log('Using mock lineup optimization as fallback');
    
    // Create a safer fallback that won't cause errors
    try {
      // Get mock players for fallback
      const topPlayers = mockPlayers.slice(0, 5);
      
      // Calculate totals
      const total_ppg = topPlayers.reduce((sum, p) => sum + p.ppg, 0);
      const total_rpg = topPlayers.reduce((sum, p) => sum + p.rpg, 0);
      const total_apg = topPlayers.reduce((sum, p) => sum + p.apg, 0);
      const total_spg = topPlayers.reduce((sum, p) => sum + p.spg, 0);
      const total_bpg = topPlayers.reduce((sum, p) => sum + p.bpg, 0);
      const total_fg_pct = topPlayers.reduce((sum, p) => sum + p.fg_pct, 0) / 5;
      const total_fg3_pct = topPlayers.reduce((sum, p) => sum + p.fg3_pct, 0) / 5;
      const total_ft_pct = topPlayers.reduce((sum, p) => sum + p.ft_pct, 0) / 5;
      
      return {
        name: `Optimized Lineup (${strategy})`,
        players: topPlayers,
        total_ppg,
        total_rpg,
        total_apg,
        total_spg,
        total_bpg,
        total_fg_pct,
        total_fg3_pct,
        total_ft_pct
      };
    } catch (fallbackError) {
      console.error('Error in optimization fallback:', fallbackError);
      throw new Error('Failed to optimize lineup');
    }
  }
};

// Lineup Comparison
export const compareLineups = async (lineup1Id, lineup2Id) => {
  try {
    // For development, use mock data
    console.log(`Comparing lineups ${lineup1Id} and ${lineup2Id}`);
    
    // Get all lineups (including user-created ones)
    const allLineups = await getLineups();
    
    // Find the lineups by ID
    const lineup1 = allLineups.find(l => l.id === Number(lineup1Id));
    const lineup2 = allLineups.find(l => l.id === Number(lineup2Id));
    
    if (!lineup1 || !lineup2) {
      console.error(`One or both lineups not found: ${lineup1Id}, ${lineup2Id}`);
      return null;
    }
    
    // Calculate stat differences
    const statDiff = {
      ppg: lineup1.total_ppg - lineup2.total_ppg,
      rpg: lineup1.total_rpg - lineup2.total_rpg,
      apg: lineup1.total_apg - lineup2.total_apg,
      spg: lineup1.total_spg - lineup2.total_spg,
      bpg: lineup1.total_bpg - lineup2.total_bpg,
      fg_pct: lineup1.total_fg_pct - lineup2.total_fg_pct,
      fg3_pct: lineup1.total_fg3_pct - lineup2.total_fg3_pct,
      ft_pct: lineup1.total_ft_pct - lineup2.total_ft_pct,
    };
    
    return {
      lineup1,
      lineup2,
      stat_diff: statDiff
    };
    
    // Uncomment for production:
    // const response = await api.get(`/lineups/compare/?lineup1=${lineup1Id}&lineup2=${lineup2Id}`);
    // return response.data;
  } catch (error) {
    console.error(`Error comparing lineups ${lineup1Id} and ${lineup2Id}:`, error);
    console.log('Using mock lineup comparison as fallback');
    return mockCompareLineups(lineup1Id, lineup2Id);
  }
};

// Dashboard Stats
export const getDashboardStats = async () => {
  try {
    // For development, always use mock data
    console.log('Using mock dashboard stats');
    return mockDashboardStats;
    
    // Uncomment for production:
    // const response = await api.get('/dashboard/stats/');
    // return response.data;
  } catch (error) {
    console.error('Error fetching dashboard stats:', error);
    console.log('Using mock dashboard stats as fallback');
    return mockDashboardStats;
  }
};

export default api; 