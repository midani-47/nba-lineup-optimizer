import React, { useState, memo } from 'react';
import { styled } from '@mui/material/styles';
import MuiAppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import Badge from '@mui/material/Badge';
import NotificationsIcon from '@mui/icons-material/Notifications';
import HomeIcon from '@mui/icons-material/Home';
import { Link, useNavigate } from 'react-router-dom';
import { Tooltip, Menu, MenuItem, Popover, List, ListItem, ListItemText, ListItemIcon, Box, Divider, Avatar } from '@mui/material';
import UpdateIcon from '@mui/icons-material/Update';
import StarIcon from '@mui/icons-material/Star';

const drawerWidth = 240;

const AppBar = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== 'open',
})(({ theme, open }) => ({
  zIndex: theme.zIndex.drawer + 1,
  transition: theme.transitions.create(['width', 'margin'], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  ...(open && {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  }),
}));

// Memoized notification item component
const NotificationItem = memo(({ notification, onClose }) => (
  <React.Fragment>
    <ListItem button alignItems="flex-start" onClick={onClose}>
      <ListItemIcon>
        {notification.type === 'update' ? <UpdateIcon color="primary" /> : <StarIcon color="secondary" />}
      </ListItemIcon>
      <ListItemText 
        primary={notification.message}
        secondary={notification.time}
      />
    </ListItem>
    <Divider />
  </React.Fragment>
));

const Navbar = ({ open, toggleDrawer }) => {
  const navigate = useNavigate();
  const [notificationsAnchorEl, setNotificationsAnchorEl] = useState(null);
  const [userMenuAnchorEl, setUserMenuAnchorEl] = useState(null);
  
  const handleNotificationsClick = (event) => {
    setNotificationsAnchorEl(event.currentTarget);
  };
  
  const handleNotificationsClose = () => {
    setNotificationsAnchorEl(null);
  };
  
  const handleUserMenuClick = (event) => {
    setUserMenuAnchorEl(event.currentTarget);
  };
  
  const handleUserMenuClose = () => {
    setUserMenuAnchorEl(null);
  };
  
  const notificationsOpen = Boolean(notificationsAnchorEl);
  const userMenuOpen = Boolean(userMenuAnchorEl);
  
  // Sample notifications
  const notifications = [
    { id: 1, type: 'update', message: 'Player stats updated', time: '5 min ago' },
    { id: 2, type: 'favorite', message: 'New recommended lineup available', time: '1 hour ago' },
    { id: 3, type: 'update', message: 'NBA games scheduled for today', time: '3 hours ago' },
    { id: 4, type: 'favorite', message: 'Your saved lineup was optimized', time: 'Yesterday' },
  ];

  const handleNavigation = (path) => {
    navigate(path, { replace: true });
  };

  return (
    <AppBar position="fixed" open={open}>
      <Toolbar>
        <IconButton
          edge="start"
          color="inherit"
          aria-label="open drawer"
          onClick={toggleDrawer}
          sx={{
            marginRight: '36px',
            ...(open && { display: 'none' }),
          }}
        >
          <MenuIcon />
        </IconButton>
        <Typography
          component="div"
          variant="h6"
          color="inherit"
          noWrap
          sx={{ 
            flexGrow: 1,
            textDecoration: 'none',
            display: 'flex',
            alignItems: 'center',
            cursor: 'pointer'
          }}
          onClick={() => handleNavigation('/')}
        >
          NBA Lineup Optimizer
        </Typography>
        
        <Tooltip title="Home">
          <IconButton 
            color="inherit" 
            onClick={() => handleNavigation('/')}
            sx={{ mr: 1 }}
          >
            <HomeIcon />
          </IconButton>
        </Tooltip>
        
        <Tooltip title="Notifications">
          <IconButton 
            color="inherit" 
            onClick={handleNotificationsClick}
            aria-describedby="notifications-popover"
          >
            <Badge badgeContent={notifications.length} color="secondary">
              <NotificationsIcon />
            </Badge>
          </IconButton>
        </Tooltip>
        
        <Popover
          id="notifications-popover"
          open={notificationsOpen}
          anchorEl={notificationsAnchorEl}
          onClose={handleNotificationsClose}
          anchorOrigin={{
            vertical: 'bottom',
            horizontal: 'right',
          }}
          transformOrigin={{
            vertical: 'top',
            horizontal: 'right',
          }}
        >
          <Box sx={{ width: 320, maxHeight: 400 }}>
            <Box sx={{ p: 2, bgcolor: 'primary.main', color: 'white' }}>
              <Typography variant="h6">Notifications</Typography>
            </Box>
            <List sx={{ p: 0 }}>
              {notifications.map((notification) => (
                <NotificationItem 
                  key={notification.id} 
                  notification={notification} 
                  onClose={handleNotificationsClose}
                />
              ))}
            </List>
          </Box>
        </Popover>
        
        <Tooltip title="Account">
          <IconButton 
            color="inherit" 
            onClick={handleUserMenuClick}
            aria-controls={userMenuOpen ? 'user-menu' : undefined}
            aria-haspopup="true"
            aria-expanded={userMenuOpen ? 'true' : undefined}
          >
            <Avatar 
              alt="NBA" 
              src="https://cdn.nba.com/logos/nba/nba-logoman-75-word_white.svg"
              sx={{ 
                width: 32, 
                height: 32, 
                bgcolor: 'transparent',
                '& img': {
                  objectFit: 'contain'
                }
              }}
            />
          </IconButton>
        </Tooltip>
        
        <Menu
          id="user-menu"
          anchorEl={userMenuAnchorEl}
          open={userMenuOpen}
          onClose={handleUserMenuClose}
          MenuListProps={{
            'aria-labelledby': 'user-button',
          }}
        >
          <MenuItem onClick={handleUserMenuClose}>Profile</MenuItem>
          <MenuItem onClick={handleUserMenuClose}>My Lineups</MenuItem>
          <MenuItem onClick={handleUserMenuClose}>Settings</MenuItem>
          <Divider />
          <MenuItem onClick={handleUserMenuClose}>Logout</MenuItem>
        </Menu>
      </Toolbar>
    </AppBar>
  );
};

export default memo(Navbar); 