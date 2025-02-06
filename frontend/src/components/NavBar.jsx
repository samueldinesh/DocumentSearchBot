// src/components/NavBar.jsx
import React from 'react';
import { AppBar, Toolbar, Typography, Button } from '@mui/material';
import { useAuth } from '../context/AuthContext';
import { Link, useNavigate } from 'react-router-dom';

const NavBar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Document Search Bot
        </Typography>
        {user && (
          <>
            {user.role === 'admin' && (
              <>
              <Button color="inherit" component={Link} to="/admin">
                Admin Dashboard
              </Button>
              <Button color="inherit" component={Link} to="/chat">
              Chat
            </Button>
            </>
            )}
            {user.role === 'user' && (
              <Button color="inherit" component={Link} to="/chat">
                Chat
              </Button>
            )}
            <Button color="inherit" onClick={handleLogout}>
              Logout
            </Button>
          </>
        )}
      </Toolbar>
    </AppBar>
  );
};

export default NavBar;
