import React from 'react';
import { Link } from 'react-router-dom';
import { styled } from '@mui/material/styles';
import MuiDrawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import HomeIcon from '@mui/icons-material/Home';
import PeopleIcon from '@mui/icons-material/People';
import SportsMmaIcon from '@mui/icons-material/SportsMma';
import TuneIcon from '@mui/icons-material/Tune';
import GitHubIcon from '@mui/icons-material/GitHub';
import InfoIcon from '@mui/icons-material/Info';
import Tooltip from '@mui/material/Tooltip';

const drawerWidth = 240;

const Drawer = styled(MuiDrawer, { shouldForwardProp: (prop) => prop !== 'open' })(
  ({ theme, open }) => ({
    '& .MuiDrawer-paper': {
      position: 'relative',
      whiteSpace: 'nowrap',
      width: drawerWidth,
      transition: theme.transitions.create('width', {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.enteringScreen,
      }),
      boxSizing: 'border-box',
      ...(!open && {
        overflowX: 'hidden',
        transition: theme.transitions.create('width', {
          easing: theme.transitions.easing.sharp,
          duration: theme.transitions.duration.leavingScreen,
        }),
        width: theme.spacing(7),
        [theme.breakpoints.up('sm')]: {
          width: theme.spacing(9),
        },
      }),
    },
  }),
);

// Simplified navigation items - removed redundant items
const mainNavItems = [
  { name: 'Home', icon: <HomeIcon />, path: '/', description: 'Dashboard and overview' },
  { name: 'Players', icon: <PeopleIcon />, path: '/players', description: 'Browse and analyze players' },
  { name: 'Lineup Builder', icon: <SportsMmaIcon />, path: '/lineup-builder', description: 'Create and manage lineups' },
  { name: 'Lineup Optimizer', icon: <TuneIcon />, path: '/lineup-optimizer', description: 'Optimize lineups with AI' },
];

const secondaryNavItems = [
  { name: 'About', icon: <InfoIcon />, path: '/about', description: 'About this project' },
  { name: 'GitHub', icon: <GitHubIcon />, path: 'https://github.com/username/nba-lineup-optimizer', description: 'View source code', external: true },
];

function Sidebar({ open, toggleDrawer }) {
  return (
    <Drawer variant="permanent" open={open}>
      <List component="nav">
        {/* Drawer header with close button */}
        <ListItemButton
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'flex-end',
            px: 1,
          }}
          onClick={toggleDrawer}
        >
          <IconButton>
            <ChevronLeftIcon />
          </IconButton>
        </ListItemButton>
        <Divider />
        
        {/* Main navigation items */}
        {mainNavItems.map((item) => (
          <Tooltip 
            key={item.name} 
            title={item.description} 
            placement="right" 
            arrow 
            disableHoverListener={open}
          >
            <ListItemButton
              component={Link}
              to={item.path}
              sx={{
                minHeight: 48,
                justifyContent: open ? 'initial' : 'center',
                px: 2.5,
              }}
            >
              <ListItemIcon
                sx={{
                  minWidth: 0,
                  mr: open ? 3 : 'auto',
                  justifyContent: 'center',
                }}
              >
                {item.icon}
              </ListItemIcon>
              <ListItemText primary={item.name} sx={{ opacity: open ? 1 : 0 }} />
            </ListItemButton>
          </Tooltip>
        ))}
        
        <Divider sx={{ my: 1 }} />
        
        {/* Secondary navigation items */}
        {secondaryNavItems.map((item) => (
          <Tooltip 
            key={item.name} 
            title={item.description} 
            placement="right" 
            arrow 
            disableHoverListener={open}
          >
            <ListItemButton
              component={item.external ? 'a' : Link}
              to={!item.external ? item.path : undefined}
              href={item.external ? item.path : undefined}
              target={item.external ? '_blank' : undefined}
              rel={item.external ? 'noopener noreferrer' : undefined}
              sx={{
                minHeight: 48,
                justifyContent: open ? 'initial' : 'center',
                px: 2.5,
              }}
            >
              <ListItemIcon
                sx={{
                  minWidth: 0,
                  mr: open ? 3 : 'auto',
                  justifyContent: 'center',
                }}
              >
                {item.icon}
              </ListItemIcon>
              <ListItemText primary={item.name} sx={{ opacity: open ? 1 : 0 }} />
            </ListItemButton>
          </Tooltip>
        ))}
      </List>
    </Drawer>
  );
}

export default Sidebar; 