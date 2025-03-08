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
      // In production, this would try the API first
      console.log('Using mock player data');
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
      return getPlayerDetail(playerId);
      
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
    // For development, always use mock data
    console.log('Using mock lineup data');
    return mockLineups;
    
    // Uncomment for production:
    // const response = await api.get('/lineups/');
    // return response.data;
  } catch (error) {
    console.error('Error fetching lineups:', error);
    console.log('Using mock lineup data as fallback');
    return mockLineups;
  }
};

export const getLineupById = async (lineupId) => {
  try {
    // For development, always use mock data
    console.log(`Using mock data for lineup ${lineupId}`);
    const lineup = mockLineups.find(l => l.id === Number(lineupId));
    if (!lineup) {
      throw new Error(`Lineup with ID ${lineupId} not found`);
    }
    return lineup;
    
    // Uncomment for production:
    // const response = await api.get(`/lineups/${lineupId}/`);
    // return response.data;
  } catch (error) {
    console.error(`Error fetching lineup ${lineupId}:`, error);
    console.log('Using mock lineup data as fallback');
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
    // Create a mock lineup with a new ID
    const newId = Math.max(...mockLineups.map(l => l.id)) + 1;
    const newLineup = {
      id: newId,
      name: lineupData.name,
      players: lineupData.players.map(id => mockPlayers.find(p => p.player_id === id)).filter(Boolean),
      total_ppg: 0,
      total_rpg: 0,
      total_apg: 0,
      total_spg: 0,
      total_bpg: 0,
      total_fg_pct: 0,
      total_fg3_pct: 0,
      total_ft_pct: 0
    };
    
    // Calculate totals
    if (newLineup.players.length > 0) {
      newLineup.total_ppg = newLineup.players.reduce((sum, p) => sum + p.ppg, 0);
      newLineup.total_rpg = newLineup.players.reduce((sum, p) => sum + p.rpg, 0);
      newLineup.total_apg = newLineup.players.reduce((sum, p) => sum + p.apg, 0);
      newLineup.total_spg = newLineup.players.reduce((sum, p) => sum + p.spg, 0);
      newLineup.total_bpg = newLineup.players.reduce((sum, p) => sum + p.bpg, 0);
      newLineup.total_fg_pct = newLineup.players.reduce((sum, p) => sum + p.fg_pct, 0) / newLineup.players.length;
      newLineup.total_fg3_pct = newLineup.players.reduce((sum, p) => sum + p.fg3_pct, 0) / newLineup.players.length;
      newLineup.total_ft_pct = newLineup.players.reduce((sum, p) => sum + p.ft_pct, 0) / newLineup.players.length;
    }
    
    // Add to mock lineups (in memory only)
    mockLineups.push(newLineup);
    
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
    
    const lineupIndex = mockLineups.findIndex(l => l.id === Number(lineupId));
    if (lineupIndex === -1) return null;
    
    const updatedLineup = {
      ...mockLineups[lineupIndex],
      name: lineupData.name,
      players: lineupData.players.map(id => mockPlayers.find(p => p.player_id === id)).filter(Boolean)
    };
    
    // Recalculate totals
    if (updatedLineup.players.length > 0) {
      updatedLineup.total_ppg = updatedLineup.players.reduce((sum, p) => sum + p.ppg, 0);
      updatedLineup.total_rpg = updatedLineup.players.reduce((sum, p) => sum + p.rpg, 0);
      updatedLineup.total_apg = updatedLineup.players.reduce((sum, p) => sum + p.apg, 0);
      updatedLineup.total_spg = updatedLineup.players.reduce((sum, p) => sum + p.spg, 0);
      updatedLineup.total_bpg = updatedLineup.players.reduce((sum, p) => sum + p.bpg, 0);
      updatedLineup.total_fg_pct = updatedLineup.players.reduce((sum, p) => sum + p.fg_pct, 0) / updatedLineup.players.length;
      updatedLineup.total_fg3_pct = updatedLineup.players.reduce((sum, p) => sum + p.fg3_pct, 0) / updatedLineup.players.length;
      updatedLineup.total_ft_pct = updatedLineup.players.reduce((sum, p) => sum + p.ft_pct, 0) / updatedLineup.players.length;
    }
    
    // Update in mock lineups (in memory only)
    mockLineups[lineupIndex] = updatedLineup;
    
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
    
    const lineupIndex = mockLineups.findIndex(l => l.id === Number(lineupId));
    if (lineupIndex === -1) return { success: false };
    
    // Remove from mock lineups (in memory only)
    mockLineups.splice(lineupIndex, 1);
    
    return { success: true };
  }
};

// Lineup Optimization
export const optimizeLineup = async (lineupId, strategy) => {
  try {
    const response = await api.post(`/lineups/${lineupId}/optimize/`, { strategy });
    return response.data;
  } catch (error) {
    console.error(`Error optimizing lineup ${lineupId}:`, error);
    console.log('Using mock lineup optimization as fallback');
    return mockOptimizeLineup(lineupId, strategy);
  }
};

// Lineup Comparison
export const compareLineups = async (lineup1Id, lineup2Id) => {
  try {
    const response = await api.get(`/lineups/compare/?lineup1=${lineup1Id}&lineup2=${lineup2Id}`);
    return response.data;
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