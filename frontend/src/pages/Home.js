import React, { useEffect, useState } from 'react';
import { 
  Container, 
  Box, 
  Typography, 
  Button, 
  Grid, 
  Card, 
  CardContent,
  Paper,
  useTheme,
  Fade,
  Grow,
  Divider,
  Avatar,
  Chip
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import DashboardIcon from '@mui/icons-material/Dashboard';
import PeopleIcon from '@mui/icons-material/People';
import CompareArrowsIcon from '@mui/icons-material/CompareArrows';
import AutoFixHighIcon from '@mui/icons-material/AutoFixHigh';
import BuildIcon from '@mui/icons-material/Build';
import SportsSoccerIcon from '@mui/icons-material/SportsSoccer';
import StarIcon from '@mui/icons-material/Star';

const Home = () => {
  const navigate = useNavigate();
  const theme = useTheme();
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    // Trigger animations after component mounts
    setLoaded(true);
  }, []);

  const features = [
    {
      title: 'Dashboard',
      description: 'View top performers and quick stats from around the league',
      icon: <DashboardIcon fontSize="large" />,
      path: '/',
      color: '#1976d2',
      delay: 100
    },
    {
      title: 'Players',
      description: 'Browse and filter NBA players by name, position, and team',
      icon: <PeopleIcon fontSize="large" />,
      path: '/players',
      color: '#2e7d32',
      delay: 200
    },
    {
      title: 'Lineup Builder',
      description: 'Create custom lineups with search and add functionality',
      icon: <SportsSoccerIcon fontSize="large" />,
      path: '/lineup-builder',
      color: '#ed6c02',
      delay: 300
    },
    {
      title: 'Lineup Comparison',
      description: 'Compare two lineups side by side with statistical charts',
      icon: <CompareArrowsIcon fontSize="large" />,
      path: '/lineup-comparison',
      color: '#9c27b0',
      delay: 400
    },
    {
      title: 'Lineup Optimizer',
      description: 'Optimize lineups based on criteria like offense or defense',
      icon: <AutoFixHighIcon fontSize="large" />,
      path: '/lineup-optimizer',
      color: '#d32f2f',
      delay: 500
    },
    {
      title: 'Performances',
      description: 'Analyze team and player performances with detailed stats',
      icon: <DashboardIcon fontSize="large" />,
      path: '/performances',
      color: '#1976d2',
      delay: 600
    }
  ];

  const testimonials = [
    {
      name: "Abed Midani",
      role: "Fantasy Basketball Analyst",
      avatar: "A",
      content: "This tool has completely transformed how I build my fantasy lineups. The optimization feature is a game-changer!"
    },
    {
      name: "Olivia S.",
      role: "Basketball Player",
      avatar: "O",
      content: "The statistical comparisons and visualizations make my analysis so much more effective. Highly recommended for any serious NBA fan."
    },
    {
      name: "Nevron J.",
      role: "Basketball Fan",
      avatar: "N",
      content: "I use this to explore different lineup combinations for my team. The interface is intuitive and the insights are valuable."
    }
  ];

  return (
    <Box sx={{ 
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #0d253f 0%, #1e3c72 100%)',
      overflow: 'hidden',
      position: 'relative'
    }}>
      {/* Animated basketball elements */}
      <Box sx={{
        position: 'absolute',
        width: '100%',
        height: '100%',
        overflow: 'hidden',
        zIndex: 0
      }}>
        {[...Array(8)].map((_, i) => (
          <Box
            key={i}
            sx={{
              position: 'absolute',
              width: '80px',
              height: '80px',
              borderRadius: '50%',
              background: 'radial-gradient(circle, rgba(255,109,0,0.2) 0%, rgba(255,109,0,0.1) 70%, rgba(255,109,0,0) 100%)',
              border: '2px dashed rgba(255,109,0,0.3)',
              top: `${Math.random() * 100}%`,
              left: `${Math.random() * 100}%`,
              transform: 'translate(-50%, -50%)',
              animation: `float${i % 3 + 1} ${10 + i * 2}s infinite ease-in-out`,
              opacity: 0.7,
              zIndex: 0,
              '@keyframes float1': {
                '0%, 100%': { transform: 'translate(-50%, -50%) translateY(-20px) rotate(0deg)' },
                '50%': { transform: 'translate(-50%, -50%) translateY(20px) rotate(180deg)' }
              },
              '@keyframes float2': {
                '0%, 100%': { transform: 'translate(-50%, -50%) translateX(-20px) rotate(0deg)' },
                '50%': { transform: 'translate(-50%, -50%) translateX(20px) rotate(-180deg)' }
              },
              '@keyframes float3': {
                '0%, 100%': { transform: 'translate(-50%, -50%) translate(-20px, -20px) rotate(0deg)' },
                '50%': { transform: 'translate(-50%, -50%) translate(20px, 20px) rotate(90deg)' }
              }
            }}
          />
        ))}
      </Box>

      <Container maxWidth="lg" sx={{ position: 'relative', zIndex: 1, pt: 8, pb: 10 }}>
        {/* Hero Section */}
        <Fade in={loaded} timeout={1000}>
          <Box sx={{ textAlign: 'center', mb: 8, mt: 4 }}>
            <Typography 
              variant="h1" 
              component="h1" 
              sx={{ 
                fontSize: { xs: '2.5rem', md: '4rem' },
                fontWeight: 800,
                color: 'white',
                textShadow: '0 4px 8px rgba(0,0,0,0.3)',
                mb: 2,
                letterSpacing: '-0.02em'
              }}
            >
              NBA Lineup Optimizer
            </Typography>
            <Typography 
              variant="h5" 
              sx={{ 
                color: 'rgba(255,255,255,0.8)', 
                mb: 4,
                maxWidth: '800px',
                mx: 'auto',
                lineHeight: 1.5
              }}
            >
              Build, compare, and optimize your dream NBA lineups with powerful analytics and real-time player data
            </Typography>
            <Box sx={{ display: 'flex', gap: 3, justifyContent: 'center', flexWrap: 'wrap' }}>
              <Button 
                variant="contained" 
                size="large" 
                onClick={() => navigate('/lineup-builder')}
                sx={{ 
                  px: 4, 
                  py: 1.5,
                  fontSize: '1.1rem',
                  fontWeight: 600,
                  backgroundColor: '#ff6d00',
                  '&:hover': {
                    backgroundColor: '#ff8f00',
                  },
                  borderRadius: '30px',
                  boxShadow: '0 4px 20px rgba(255,109,0,0.5)'
                }}
              >
                Build Your Lineup
              </Button>
              <Button 
                variant="outlined" 
                size="large" 
                onClick={() => navigate('/players')}
                sx={{ 
                  px: 4, 
                  py: 1.5,
                  fontSize: '1.1rem',
                  fontWeight: 600,
                  borderColor: 'rgba(255,255,255,0.5)',
                  color: 'white',
                  '&:hover': {
                    borderColor: 'white',
                    backgroundColor: 'rgba(255,255,255,0.1)',
                  },
                  borderRadius: '30px'
                }}
              >
                Explore Players
              </Button>
            </Box>
          </Box>
        </Fade>

        {/* Basketball court illustration */}
        <Fade in={loaded} timeout={1500}>
          <Box 
            sx={{ 
              position: 'relative',
              height: { xs: 350, md: 450 },
              maxWidth: 1000,
              mx: 'auto',
              mb: 10,
              mt: 5,
              perspective: '1200px'
            }}
          >
            {/* Half Court - Facing the Net - Upside Down */}
            <Box 
              sx={{ 
                position: 'absolute',
                top: 0,
                left: '50%',
                width: '90%',
                height: '100%',
                transform: 'translateX(-50%) rotateX(25deg)',
                borderRadius: '16px',
                border: '5px solid rgba(255,255,255,0.6)',
                background: 'linear-gradient(to top, rgba(30,60,114,0.7), rgba(21,101,192,0.6))',
                boxShadow: '0 20px 50px rgba(0,0,0,0.4), inset 0 0 100px rgba(0,0,0,0.2)',
                overflow: 'hidden',
                transformStyle: 'preserve-3d'
              }}
            >
              {/* Center court line */}
              <Box 
                sx={{ 
                  position: 'absolute',
                  top: '0%',
                  left: '0',
                  width: '100%',
                  height: '5px',
                  backgroundColor: 'rgba(255,255,255,0.9)'
                }}
              />
              
              {/* Free throw line */}
              <Box 
                sx={{ 
                  position: 'absolute',
                  top: '30%',
                  left: '0',
                  width: '100%',
                  height: '4px',
                  backgroundColor: 'rgba(255,255,255,0.9)'
                }}
              />
              
              {/* Free throw semicircle */}
              <Box 
                sx={{ 
                  position: 'absolute',
                  top: '30%',
                  left: '25%',
                  width: '50%',
                  height: '15%',
                  borderTopLeftRadius: '100px',
                  borderTopRightRadius: '100px',
                  border: '4px solid rgba(255,255,255,0.8)',
                  borderBottom: 'none'
                }}
              />
              
              {/* Three-point line */}
              <Box 
                sx={{ 
                  position: 'absolute',
                  top: '5%',
                  left: '10%',
                  width: '80%',
                  height: '50%',
                  border: '4px solid rgba(255,255,255,0.8)',
                  borderBottomLeftRadius: '200px',
                  borderBottomRightRadius: '200px',
                  borderTop: 'none'
                }}
              />
              
              {/* Paint area */}
              <Box 
                sx={{ 
                  position: 'absolute',
                  top: '0%',
                  left: '30%',
                  width: '40%',
                  height: '30%',
                  backgroundColor: 'rgba(30,60,114,0.6)',
                  borderBottom: '4px solid rgba(255,255,255,0.8)',
                  borderLeft: '4px solid rgba(255,255,255,0.8)',
                  borderRight: '4px solid rgba(255,255,255,0.8)'
                }}
              />
              
              {/* Lane markers on free throw line */}
              {[...Array(6)].map((_, i) => (
                <React.Fragment key={`lane-marker-${i}`}>
                  <Box
                    sx={{
                      position: 'absolute',
                      top: `${5 + i * 5}%`,
                      left: '30%',
                      width: '3px',
                      height: '15px',
                      backgroundColor: 'rgba(255,255,255,0.9)'
                    }}
                  />
                  <Box
                    sx={{
                      position: 'absolute',
                      top: `${5 + i * 5}%`,
                      left: '70%',
                      width: '3px',
                      height: '15px',
                      backgroundColor: 'rgba(255,255,255,0.9)'
                    }}
                  />
                </React.Fragment>
              ))}
              
              {/* Center court circle */}
              <Box 
                sx={{ 
                  position: 'absolute',
                  top: '-15%',
                  left: '25%',
                  width: '50%',
                  height: '30%',
                  borderBottomLeftRadius: '100px',
                  borderBottomRightRadius: '100px',
                  border: '4px solid rgba(255,255,255,0.8)',
                  borderTop: 'none'
                }}
              />
              
              {/* Court texture overlay */}
              <Box
                sx={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  width: '100%',
                  height: '100%',
                  backgroundImage: 'url("data:image/svg+xml,%3Csvg width=\'100\' height=\'100\' viewBox=\'0 0 100 100\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cpath d=\'M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z\' fill=\'%23ffffff\' fill-opacity=\'0.05\' fill-rule=\'evenodd\'/%3E%3C/svg%3E")',
                  backgroundSize: '100px 100px',
                  opacity: 0.7
                }}
              />
              
              {/* Glossy reflection */}
              <Box
                sx={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  width: '100%',
                  height: '100%',
                  background: 'linear-gradient(to bottom, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 40%)',
                  pointerEvents: 'none'
                }}
              />
            </Box>
            
            {/* Basketball Hoop and Net */}
            <Box
              sx={{
                position: 'absolute',
                top: '0%',
                left: '50%',
                transform: 'translateX(-50%)',
                width: '140px',
                height: '120px',
                zIndex: 2
              }}
            >
              {/* Backboard */}
              <Box
                sx={{
                  position: 'absolute',
                  top: '0',
                  left: '50%',
                  transform: 'translateX(-50%)',
                  width: '90px',
                  height: '60px',
                  backgroundColor: 'rgba(255,255,255,0.95)',
                  borderRadius: '4px',
                  boxShadow: '0 5px 15px rgba(0,0,0,0.3)'
                }}
              >
                {/* Backboard square */}
                <Box
                  sx={{
                    position: 'absolute',
                    bottom: '5px',
                    left: '50%',
                    transform: 'translateX(-50%)',
                    width: '35px',
                    height: '30px',
                    border: '3px solid rgba(255,109,0,0.8)',
                    borderRadius: '2px'
                  }}
                />
              </Box>
              
              {/* Rim */}
              <Box
                sx={{
                  position: 'absolute',
                  top: '60px',
                  left: '50%',
                  transform: 'translateX(-50%)',
                  width: '45px',
                  height: '6px',
                  border: '4px solid #ff6d00',
                  borderRadius: '20px',
                  boxShadow: '0 3px 10px rgba(0,0,0,0.4)'
                }}
              />
              
              {/* Net - simplified and more natural */}
              <Box
                component="svg"
                viewBox="0 0 45 45"
                sx={{
                  position: 'absolute',
                  top: '65px',
                  left: '50%',
                  transform: 'translateX(-50%)',
                  width: '45px',
                  height: '45px'
                }}
              >
                {/* Vertical net lines */}
                {[...Array(8)].map((_, i) => (
                  <path
                    key={`net-v-${i}`}
                    d={`M${5 + i * 5},0 Q${5 + i * 5},20 ${3 + i * 6},45`}
                    fill="none"
                    stroke="rgba(255,255,255,0.9)"
                    strokeWidth="0.8"
                  />
                ))}
                
                {/* Horizontal net lines */}
                {[...Array(6)].map((_, i) => (
                  <path
                    key={`net-h-${i}`}
                    d={`M0,${7 + i * 7} Q22.5,${10 + i * 7} 45,${7 + i * 7}`}
                    fill="none"
                    stroke="rgba(255,255,255,0.8)"
                    strokeWidth="0.8"
                  />
                ))}
              </Box>
              
              {/* Rim support */}
              <Box
                sx={{
                  position: 'absolute',
                  top: '40px',
                  left: '50%',
                  transform: 'translateX(-50%)',
                  width: '10px',
                  height: '20px',
                  backgroundColor: '#d32f2f',
                  zIndex: -1
                }}
              />
            </Box>
            
            {/* Bouncing Basketball with improved animation */}
            <Box 
              sx={{ 
                position: 'absolute',
                width: 60,
                height: 60,
                top: '60%',
                left: '50%',
                borderRadius: '50%',
                background: 'radial-gradient(circle at 30% 30%, #f57c00 0%, #e65100 70%)',
                boxShadow: '0 5px 15px rgba(0,0,0,0.4)',
                transform: 'translate(-50%, -50%)',
                animation: 'bounce-and-rotate 2s infinite ease-in-out',
                zIndex: 3,
                '&::before': {
                  content: '""',
                  position: 'absolute',
                  top: '0',
                  left: '0',
                  width: '100%',
                  height: '100%',
                  borderRadius: '50%',
                  background: 'linear-gradient(to right, transparent 45%, rgba(0,0,0,0.1) 50%, transparent 55%), linear-gradient(to bottom, transparent 45%, rgba(0,0,0,0.1) 50%, transparent 55%)',
                  transform: 'rotate(30deg)'
                },
                '&::after': {
                  content: '""',
                  position: 'absolute',
                  top: '0',
                  left: '0',
                  width: '100%',
                  height: '100%',
                  borderRadius: '50%',
                  background: 'linear-gradient(to right, transparent 48%, rgba(0,0,0,0.1) 50%, transparent 52%), linear-gradient(to bottom, transparent 48%, rgba(0,0,0,0.1) 50%, transparent 52%)',
                  transform: 'rotate(60deg)'
                },
                '@keyframes bounce-and-rotate': {
                  '0%': { 
                    transform: 'translate(-50%, -80%) rotate(0deg)', 
                    animationTimingFunction: 'cubic-bezier(0.17, 0.67, 0.83, 0.67)' 
                  },
                  '50%': { 
                    transform: 'translate(-50%, 0%) rotate(180deg) scale(0.95)', 
                    animationTimingFunction: 'cubic-bezier(0.17, 0.67, 0.83, 0.67)' 
                  },
                  '100%': { 
                    transform: 'translate(-50%, -80%) rotate(360deg)', 
                    animationTimingFunction: 'cubic-bezier(0.17, 0.67, 0.83, 0.67)' 
                  }
                }
              }}
            />
            
            {/* Court shadow */}
            <Box 
              sx={{ 
                position: 'absolute',
                bottom: '-20px',
                left: '50%',
                transform: 'translateX(-50%)',
                width: '85%',
                height: '25px',
                borderRadius: '50%',
                background: 'radial-gradient(ellipse at center, rgba(0,0,0,0.4) 0%, rgba(0,0,0,0) 70%)',
                zIndex: 1
              }}
            />
            
            {/* Spotlight effect */}
            <Box
              sx={{
                position: 'absolute',
                top: '-50px',
                left: '50%',
                transform: 'translateX(-50%)',
                width: '300px',
                height: '300px',
                background: 'radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%)',
                zIndex: 0
              }}
            />
          </Box>
        </Fade>

        {/* Features Section */}
        <Box sx={{ mb: 12 }}>
          <Fade in={loaded} timeout={1000}>
            <Typography 
              variant="h3" 
              component="h2" 
              align="center" 
              gutterBottom
              sx={{ 
                color: 'white',
                mb: 6,
                fontWeight: 700,
                textShadow: '0 2px 4px rgba(0,0,0,0.3)'
              }}
            >
              Powerful Features
            </Typography>
          </Fade>
          
          <Grid container spacing={4}>
            {features.map((feature, index) => (
              <Grid item xs={12} sm={6} md={4} key={index}>
                <Grow 
                  in={loaded} 
                  style={{ transformOrigin: '0 0 0' }}
                  timeout={1000 + feature.delay}
                >
                  <Card 
                    sx={{ 
                      height: '100%', 
                      display: 'flex', 
                      flexDirection: 'column',
                      transition: 'all 0.3s ease-in-out',
                      background: 'rgba(255,255,255,0.9)',
                      backdropFilter: 'blur(10px)',
                      borderRadius: '16px',
                      overflow: 'hidden',
                      boxShadow: '0 10px 30px rgba(0,0,0,0.2)',
                      '&:hover': {
                        transform: 'translateY(-10px)',
                        boxShadow: '0 15px 35px rgba(0,0,0,0.3)',
                      },
                    }}
                    onClick={() => navigate(feature.path)}
                  >
                    <Box sx={{ 
                      height: 8, 
                      backgroundColor: feature.color,
                      width: '100%'
                    }} />
                    <CardContent sx={{ flexGrow: 1, p: 4 }}>
                      <Box sx={{ 
                        color: 'white', 
                        mb: 3,
                        p: 2,
                        borderRadius: '50%',
                        width: 60,
                        height: 60,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        backgroundColor: feature.color,
                        boxShadow: `0 4px 20px ${feature.color}80`
                      }}>
                        {feature.icon}
                      </Box>
                      <Typography variant="h5" component="h3" gutterBottom fontWeight="bold" color="text.primary">
                        {feature.title}
                      </Typography>
                      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
                        {feature.description}
                      </Typography>
                      <Button 
                        variant="text" 
                        sx={{ 
                          color: feature.color,
                          '&:hover': {
                            backgroundColor: `${feature.color}10`,
                          },
                          alignSelf: 'flex-start',
                          mt: 'auto'
                        }}
                        onClick={(e) => {
                          e.stopPropagation();
                          navigate(feature.path);
                        }}
                      >
                        Explore {feature.title}
                      </Button>
                    </CardContent>
                  </Card>
                </Grow>
              </Grid>
            ))}
          </Grid>
        </Box>

        {/* Testimonials */}
        <Fade in={loaded} timeout={2000}>
          <Box sx={{ mb: 10 }}>
            <Typography 
              variant="h3" 
              component="h2" 
              align="center" 
              gutterBottom
              sx={{ 
                color: 'white',
                mb: 6,
                fontWeight: 700,
                textShadow: '0 2px 4px rgba(0,0,0,0.3)'
              }}
            >
              What Users Say
            </Typography>
            
            <Grid container spacing={4}>
              {testimonials.map((testimonial, index) => (
                <Grid item xs={12} md={4} key={index}>
                  <Paper
                    sx={{
                      p: 4,
                      height: '100%',
                      display: 'flex',
                      flexDirection: 'column',
                      borderRadius: 4,
                      background: 'rgba(255,255,255,0.8)',
                      backdropFilter: 'blur(10px)',
                      boxShadow: '0 10px 30px rgba(0,0,0,0.15)',
                    }}
                  >
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                      <Avatar 
                        sx={{ 
                          bgcolor: theme.palette.primary.main,
                          width: 56,
                          height: 56,
                          mr: 2,
                          boxShadow: '0 4px 8px rgba(0,0,0,0.2)'
                        }}
                      >
                        {testimonial.avatar}
                      </Avatar>
                      <Box>
                        <Typography variant="h6" fontWeight="bold">{testimonial.name}</Typography>
                        <Chip 
                          label={testimonial.role} 
                          size="small" 
                          sx={{ 
                            backgroundColor: 'rgba(25, 118, 210, 0.1)',
                            color: theme.palette.primary.main
                          }} 
                        />
                      </Box>
                    </Box>
                    <Typography variant="body1" sx={{ fontStyle: 'italic', color: 'text.secondary', flexGrow: 1 }}>
                      "{testimonial.content}"
                    </Typography>
                    <Box sx={{ display: 'flex', mt: 2 }}>
                      {[...Array(5)].map((_, i) => (
                        <StarIcon key={i} sx={{ color: '#ff9800', fontSize: 20 }} />
                      ))}
                    </Box>
                  </Paper>
                </Grid>
              ))}
            </Grid>
          </Box>
        </Fade>

        {/* Call to Action */}
        <Fade in={loaded} timeout={2500}>
          <Paper
            sx={{
              p: { xs: 4, md: 6 },
              borderRadius: 4,
              background: 'linear-gradient(135deg, #ff6d00 0%, #ff9100 100%)',
              boxShadow: '0 15px 50px rgba(255,109,0,0.3)',
              textAlign: 'center',
              mb: 8
            }}
          >
            <Typography 
              variant="h4" 
              component="h2" 
              sx={{ 
                color: 'white',
                mb: 2,
                fontWeight: 700
              }}
            >
              Ready to Build Your Dream Lineup?
            </Typography>
            <Typography 
              variant="h6" 
              sx={{ 
                color: 'rgba(255,255,255,0.9)', 
                mb: 4,
                maxWidth: '800px',
                mx: 'auto'
              }}
            >
              Start optimizing your NBA lineups today and gain the competitive edge
            </Typography>
            <Button 
              variant="contained" 
              size="large" 
              onClick={() => navigate('/lineup-builder')}
              sx={{ 
                px: 5, 
                py: 1.5,
                fontSize: '1.1rem',
                fontWeight: 600,
                backgroundColor: 'white',
                color: '#ff6d00',
                '&:hover': {
                  backgroundColor: 'rgba(255,255,255,0.9)',
                },
                borderRadius: '30px',
                boxShadow: '0 4px 20px rgba(0,0,0,0.2)'
              }}
            >
              Get Started Now
            </Button>
          </Paper>
        </Fade>

        {/* Footer */}
        <Divider sx={{ borderColor: 'rgba(255,255,255,0.1)', mb: 4 }} />
        <Box sx={{ 
          textAlign: 'center',
          color: 'rgba(255,255,255,0.6)'
        }}>
          <Typography variant="body2">
            © {new Date().getFullYear()} NBA Lineup Optimizer | All NBA statistics and player data are property of their respective owners
          </Typography>
        </Box>

        {/* Quick Access Links */}
        <Fade in={loaded} timeout={1800}>
          <Box sx={{ mb: 12 }}>
            <Typography 
              variant="h4" 
              component="h2" 
              align="center" 
              gutterBottom
              sx={{ 
                color: 'white',
                mb: 4,
                fontWeight: 700,
                textShadow: '0 2px 4px rgba(0,0,0,0.3)'
              }}
            >
              Quick Access
            </Typography>
            
            <Grid container spacing={2} justifyContent="center">
              {[
                { text: 'Performances Dashboard', path: '/performances', color: '#1976d2', icon: '📊' },
                { text: 'Player Stats', path: '/players', color: '#2e7d32', icon: '👤' },
                { text: 'Build Lineup', path: '/lineup-builder', color: '#ed6c02', icon: '🏀' },
                { text: 'Compare Lineups', path: '/lineup-comparison', color: '#9c27b0', icon: '⚖️' },
                { text: 'Optimize Lineup', path: '/lineup-optimizer', color: '#d32f2f', icon: '✨' }
              ].map((link, index) => (
                <Grid item key={index}>
                  <Button
                    variant="contained"
                    onClick={() => navigate(link.path)}
                    sx={{
                      backgroundColor: link.color,
                      '&:hover': {
                        backgroundColor: `${link.color}dd`,
                      },
                      px: 3,
                      py: 1.5,
                      borderRadius: '30px',
                      fontWeight: 600,
                      boxShadow: '0 4px 10px rgba(0,0,0,0.2)'
                    }}
                    startIcon={<Box component="span" sx={{ fontSize: '1.2rem' }}>{link.icon}</Box>}
                  >
                    {link.text}
                  </Button>
                </Grid>
              ))}
            </Grid>
          </Box>
        </Fade>
      </Container>
    </Box>
  );
};

export default Home; 