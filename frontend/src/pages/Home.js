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
    }
  ];

  const testimonials = [
    {
      name: "Michael J.",
      role: "Fantasy Basketball Manager",
      avatar: "M",
      content: "This tool has completely transformed how I build my fantasy lineups. The optimization feature is a game-changer!"
    },
    {
      name: "Sarah L.",
      role: "Basketball Analyst",
      avatar: "S",
      content: "The statistical comparisons and visualizations make my analysis so much more effective. Highly recommended for any serious NBA fan."
    },
    {
      name: "David K.",
      role: "Basketball Coach",
      avatar: "D",
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
              height: { xs: 200, md: 300 },
              maxWidth: 800,
              mx: 'auto',
              mb: 10,
              mt: 5
            }}
          >
            <Box 
              sx={{ 
                position: 'absolute',
                top: 0,
                left: '50%',
                transform: 'translateX(-50%)',
                width: '100%',
                height: '100%',
                borderRadius: '50% 50% 0 0',
                border: '4px solid rgba(255,255,255,0.3)',
                borderBottom: 'none',
                '&::after': {
                  content: '""',
                  position: 'absolute',
                  top: '50%',
                  left: '50%',
                  transform: 'translate(-50%, -50%)',
                  width: '30%',
                  height: '30%',
                  borderRadius: '50%',
                  border: '4px solid rgba(255,255,255,0.3)'
                }
              }}
            />
            <Box 
              sx={{ 
                position: 'absolute',
                bottom: 0,
                left: 0,
                width: '100%',
                height: '2px',
                backgroundColor: 'rgba(255,255,255,0.3)'
              }}
            />
            <Box 
              sx={{ 
                position: 'absolute',
                bottom: '10%',
                left: '10%',
                width: '80%',
                height: '2px',
                backgroundColor: 'rgba(255,255,255,0.2)'
              }}
            />
            <Box 
              sx={{ 
                position: 'absolute',
                bottom: 0,
                left: '15%',
                width: '70%',
                height: '40%',
                border: '4px solid rgba(255,255,255,0.2)',
                borderBottom: 'none',
                borderTopLeftRadius: 100,
                borderTopRightRadius: 100
              }}
            />
            <Box 
              component="img"
              src="/basketball-icon.svg"
              alt="Basketball"
              sx={{ 
                position: 'absolute',
                width: 80,
                height: 80,
                bottom: '20%',
                left: '50%',
                transform: 'translateX(-50%)',
                filter: 'drop-shadow(0 4px 8px rgba(0,0,0,0.3))',
                animation: 'bounce 2s infinite ease-in-out',
                '@keyframes bounce': {
                  '0%, 100%': { transform: 'translateX(-50%) translateY(0)' },
                  '50%': { transform: 'translateX(-50%) translateY(-20px)' }
                }
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
      </Container>
    </Box>
  );
};

export default Home; 