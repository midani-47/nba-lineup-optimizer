import React, { useState, lazy, Suspense } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import CircularProgress from '@mui/material/CircularProgress';

// Components - Only import what's needed for initial render
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';

// Lazy load pages with prefetch priority
// Home is loaded immediately as it's the landing page
const Home = lazy(() => import('./pages/Home'));

// Other pages are loaded with lower priority
const Performances = lazy(() => 
  import(/* webpackChunkName: "performances" */ './pages/Dashboard')
);
const Players = lazy(() => 
  import(/* webpackChunkName: "players" */ './pages/Players')
);
const PlayerDetail = lazy(() => 
  import(/* webpackChunkName: "player-detail" */ './pages/PlayerDetail')
);
const LineupBuilder = lazy(() => 
  import(/* webpackChunkName: "lineup-builder" */ './pages/LineupBuilder')
);
const LineupComparison = lazy(() => 
  import(/* webpackChunkName: "lineup-comparison" */ './pages/LineupComparison')
);
const LineupOptimizer = lazy(() => 
  import(/* webpackChunkName: "lineup-optimizer" */ './pages/LineupOptimizer')
);

// Simpler loading component for faster initial render
const LoadingFallback = () => (
  <Box 
    sx={{ 
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center', 
      height: '100vh',
      background: '#f5f5f5'
    }}
  >
    <CircularProgress size={40} />
  </Box>
);

// Simplified theme with fewer customizations
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#f50057',
    }
  }
});

function App() {
  const [open, setOpen] = useState(false); // Start with sidebar closed for faster initial render
  const toggleDrawer = () => {
    setOpen(!open);
  };

  // Layout component to avoid repetition
  const AppLayout = ({ children }) => (
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
        {children}
      </Box>
    </Box>
  );

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Suspense fallback={<LoadingFallback />}>
        <Routes>
          {/* Make Home the default landing page */}
          <Route path="/" element={<Home />} />
          
          {/* Performances page (formerly Dashboard) */}
          <Route path="/performances" element={
            <AppLayout>
              <Suspense fallback={<LoadingFallback />}>
                <Performances />
              </Suspense>
            </AppLayout>
          } />
          
          <Route path="/players" element={
            <AppLayout>
              <Suspense fallback={<LoadingFallback />}>
                <Players />
              </Suspense>
            </AppLayout>
          } />
          
          <Route path="/players/:playerId" element={
            <AppLayout>
              <Suspense fallback={<LoadingFallback />}>
                <PlayerDetail />
              </Suspense>
            </AppLayout>
          } />
          
          <Route path="/lineup-builder" element={
            <AppLayout>
              <Suspense fallback={<LoadingFallback />}>
                <LineupBuilder />
              </Suspense>
            </AppLayout>
          } />
          
          <Route path="/lineup-comparison" element={
            <AppLayout>
              <Suspense fallback={<LoadingFallback />}>
                <LineupComparison />
              </Suspense>
            </AppLayout>
          } />
          
          <Route path="/lineup-optimizer" element={
            <AppLayout>
              <Suspense fallback={<LoadingFallback />}>
                <LineupOptimizer />
              </Suspense>
            </AppLayout>
          } />
          
          {/* Redirect /home to / */}
          <Route path="/home" element={<Navigate to="/" replace />} />
          
          {/* Redirect old dashboard path to performances */}
          <Route path="/dashboard" element={<Navigate to="/performances" replace />} />
          
          {/* Catch all other routes and redirect to home */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Suspense>
    </ThemeProvider>
  );
}

export default App; 