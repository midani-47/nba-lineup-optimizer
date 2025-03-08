import React, { useState, lazy, Suspense } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import CircularProgress from '@mui/material/CircularProgress';

// Components
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';

// Lazy load pages for better performance
const Home = lazy(() => import('./pages/Home'));
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Players = lazy(() => import('./pages/Players'));
const PlayerDetail = lazy(() => import('./pages/PlayerDetail'));
const LineupBuilder = lazy(() => import('./pages/LineupBuilder'));
const LineupComparison = lazy(() => import('./pages/LineupComparison'));
const LineupOptimizer = lazy(() => import('./pages/LineupOptimizer'));

// Loading component for suspense fallback
const LoadingFallback = () => (
  <Box 
    sx={{ 
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center', 
      height: '100vh',
      background: 'linear-gradient(135deg, #0d253f 0%, #1e3c72 100%)'
    }}
  >
    <CircularProgress size={60} sx={{ color: '#ff6d00' }} />
  </Box>
);

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
      <Suspense fallback={<LoadingFallback />}>
        <Routes>
          {/* Make Home the default landing page */}
          <Route path="/" element={<Home />} />
          
          {/* Dashboard and other app pages with navigation */}
          <Route path="/dashboard" element={
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
                <Dashboard />
              </Box>
            </Box>
          } />
          
          <Route path="/players" element={
            <Box sx={{ display: 'flex' }}>
              <Navbar open={open} toggleDrawer={toggleDrawer} />
              <Sidebar open={open} toggleDrawer={toggleDrawer} />
              <Box
                component="main"
                sx={{
                  flexGrow: 1,
                  height: '100vh',
                  overflow: 'auto',
                  pt: 8,
                  px: 2,
                }}
              >
                <Players />
              </Box>
            </Box>
          } />
          
          <Route path="/players/:playerId" element={
            <Box sx={{ display: 'flex' }}>
              <Navbar open={open} toggleDrawer={toggleDrawer} />
              <Sidebar open={open} toggleDrawer={toggleDrawer} />
              <Box
                component="main"
                sx={{
                  flexGrow: 1,
                  height: '100vh',
                  overflow: 'auto',
                  pt: 8,
                  px: 2,
                }}
              >
                <PlayerDetail />
              </Box>
            </Box>
          } />
          
          <Route path="/lineup-builder" element={
            <Box sx={{ display: 'flex' }}>
              <Navbar open={open} toggleDrawer={toggleDrawer} />
              <Sidebar open={open} toggleDrawer={toggleDrawer} />
              <Box
                component="main"
                sx={{
                  flexGrow: 1,
                  height: '100vh',
                  overflow: 'auto',
                  pt: 8,
                  px: 2,
                }}
              >
                <LineupBuilder />
              </Box>
            </Box>
          } />
          
          <Route path="/lineup-comparison" element={
            <Box sx={{ display: 'flex' }}>
              <Navbar open={open} toggleDrawer={toggleDrawer} />
              <Sidebar open={open} toggleDrawer={toggleDrawer} />
              <Box
                component="main"
                sx={{
                  flexGrow: 1,
                  height: '100vh',
                  overflow: 'auto',
                  pt: 8,
                  px: 2,
                }}
              >
                <LineupComparison />
              </Box>
            </Box>
          } />
          
          <Route path="/lineup-optimizer" element={
            <Box sx={{ display: 'flex' }}>
              <Navbar open={open} toggleDrawer={toggleDrawer} />
              <Sidebar open={open} toggleDrawer={toggleDrawer} />
              <Box
                component="main"
                sx={{
                  flexGrow: 1,
                  height: '100vh',
                  overflow: 'auto',
                  pt: 8,
                  px: 2,
                }}
              >
                <LineupOptimizer />
              </Box>
            </Box>
          } />
          
          {/* Redirect /home to / */}
          <Route path="/home" element={<Navigate to="/" replace />} />
          
          {/* Catch all other routes and redirect to home */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Suspense>
    </ThemeProvider>
  );
}

export default App; 