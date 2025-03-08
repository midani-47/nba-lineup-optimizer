import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Players
export const getPlayers = async (params = {}) => {
  try {
    const response = await api.get('/players/', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching players:', error);
    throw error;
  }
};

export const getPlayerById = async (playerId) => {
  try {
    const response = await api.get(`/players/${playerId}/`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching player ${playerId}:`, error);
    throw error;
  }
};

// Lineups
export const getLineups = async () => {
  try {
    const response = await api.get('/lineups/');
    return response.data;
  } catch (error) {
    console.error('Error fetching lineups:', error);
    throw error;
  }
};

export const getLineupById = async (lineupId) => {
  try {
    const response = await api.get(`/lineups/${lineupId}/`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching lineup ${lineupId}:`, error);
    throw error;
  }
};

export const createLineup = async (lineupData) => {
  try {
    const response = await api.post('/lineups/', lineupData);
    return response.data;
  } catch (error) {
    console.error('Error creating lineup:', error);
    throw error;
  }
};

export const updateLineup = async (lineupId, lineupData) => {
  try {
    const response = await api.put(`/lineups/${lineupId}/`, lineupData);
    return response.data;
  } catch (error) {
    console.error(`Error updating lineup ${lineupId}:`, error);
    throw error;
  }
};

export const deleteLineup = async (lineupId) => {
  try {
    const response = await api.delete(`/lineups/${lineupId}/`);
    return response.data;
  } catch (error) {
    console.error(`Error deleting lineup ${lineupId}:`, error);
    throw error;
  }
};

// Lineup Optimization
export const optimizeLineup = async (lineupId, strategy) => {
  try {
    const response = await api.post(`/lineups/${lineupId}/optimize/`, { strategy });
    return response.data;
  } catch (error) {
    console.error(`Error optimizing lineup ${lineupId}:`, error);
    throw error;
  }
};

// Lineup Comparison
export const compareLineups = async (lineup1Id, lineup2Id) => {
  try {
    const response = await api.get(`/lineups/compare/?lineup1=${lineup1Id}&lineup2=${lineup2Id}`);
    return response.data;
  } catch (error) {
    console.error(`Error comparing lineups ${lineup1Id} and ${lineup2Id}:`, error);
    throw error;
  }
};

// Dashboard Stats
export const getDashboardStats = async () => {
  try {
    const response = await api.get('/dashboard/stats/');
    return response.data;
  } catch (error) {
    console.error('Error fetching dashboard stats:', error);
    throw error;
  }
};

export default api; 