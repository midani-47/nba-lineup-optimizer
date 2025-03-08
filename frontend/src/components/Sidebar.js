import React, { memo } from 'react';
import { styled } from '@mui/material/styles';
import MuiDrawer from '@mui/material/Drawer';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import DashboardIcon from '@mui/icons-material/Dashboard';
import PeopleIcon from '@mui/icons-material/People';
import SportsSoccerIcon from '@mui/icons-material/SportsSoccer';
import CompareIcon from '@mui/icons-material/Compare';
import AutoFixHighIcon from '@mui/icons-material/AutoFixHigh';
import HomeIcon from '@mui/icons-material/Home';
import { useNavigate, useLocation } from 'react-router-dom';

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

// Memoized menu item component to prevent unnecessary re-renders
const MenuItem = memo(({ item, isSelected, open, onClick }) => (
  <ListItem disablePadding sx={{ display: 'block' }}>
    <ListItemButton
      selected={isSelected}
      onClick={onClick}
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
          color: isSelected ? 'primary.main' : 'inherit',
        }}
      >
        {item.icon}
      </ListItemIcon>
      <ListItemText 
        primary={item.text} 
        sx={{ 
          opacity: open ? 1 : 0,
          '& .MuiTypography-root': {
            fontWeight: isSelected ? 600 : 400,
          }
        }} 
      />
    </ListItemButton>
  </ListItem>
));

const Sidebar = ({ open, toggleDrawer }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const menuItems = [
    { text: 'Home', icon: <HomeIcon />, path: '/' },
    { text: 'Performances', icon: <DashboardIcon />, path: '/performances' },
    { text: 'Players', icon: <PeopleIcon />, path: '/players' },
    { text: 'Lineup Builder', icon: <SportsSoccerIcon />, path: '/lineup-builder' },
    { text: 'Lineup Comparison', icon: <CompareIcon />, path: '/lineup-comparison' },
    { text: 'Lineup Optimizer', icon: <AutoFixHighIcon />, path: '/lineup-optimizer' },
  ];

  const handleNavigation = (path) => {
    // Use navigate with replace option to avoid adding to history stack
    navigate(path, { replace: true });
  };

  return (
    <Drawer variant="permanent" open={open}>
      <Toolbar
        sx={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'flex-end',
          px: [1],
        }}
      >
        <IconButton onClick={toggleDrawer}>
          <ChevronLeftIcon />
        </IconButton>
      </Toolbar>
      <Divider />
      <List component="nav">
        {menuItems.map((item) => (
          <MenuItem
            key={item.text}
            item={item}
            isSelected={location.pathname === item.path}
            open={open}
            onClick={() => handleNavigation(item.path)}
          />
        ))}
      </List>
    </Drawer>
  );
};

export default memo(Sidebar); 