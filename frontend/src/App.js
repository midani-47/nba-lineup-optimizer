import React, { useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';

// Components
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';

// Pages
import Dashboard from './pages/Dashboard';
import Players from './pages/Players';
import PlayerDetail from './pages/PlayerDetail';
import LineupBuilder from './pages/LineupBuilder';
import LineupComparison from './pages/LineupComparison';
import LineupOptimizer from './pages/LineupOptimizer';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#f50057',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
    ].join(','),
  },
});

function App() {
  const [open, setOpen] = useState(true);
  const toggleDrawer = () => {
    setOpen(!open);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: 'flex' }}>
        <Navbar open={open} toggleDrawer={toggleDrawer} />
        <Sidebar open={open} toggleDrawer={toggleDrawer} />
        <Box
          component="main"
          sx={{
            flexGrow: 1,
            height: '100vh',
            overflow: 'auto',
            pt: 8, // Add padding top to account for the navbar
            px: 2,
          }}
        >
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/players" element={<Players />} />
            <Route path="/players/:playerId" element={<PlayerDetail />} />
            <Route path="/lineup-builder" element={<LineupBuilder />} />
            <Route path="/lineup-comparison" element={<LineupComparison />} />
            <Route path="/lineup-optimizer" element={<LineupOptimizer />} />
          </Routes>
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default App; 