// src/components/Login.jsx
import React, { useState } from 'react';
import { Box, TextField, Button, Typography, Container } from '@mui/material';
import { useAuth } from '../context/AuthContext';
import { loginUser } from '../api';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState(''); // For demo, password is not validated
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const userData = await loginUser(username, password);
      login(userData);
      navigate(userData.role === 'admin' ? '/admin' : '/chat');
    } catch (err) {
      setError('Login failed. Try "admin" or "user" as username.');
    }
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 8 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Login
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            label="Username"
            variant="outlined"
            fullWidth
            required
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            sx={{ mb: 2 }}
          />
          <TextField
            label="Password"
            type="password"
            variant="outlined"
            fullWidth
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            sx={{ mb: 2 }}
          />
          {error && (
            <Typography color="error" sx={{ mb: 2 }}>
              {error}
            </Typography>
          )}
          <Button variant="contained" type="submit" fullWidth>
            Login
          </Button>
        </form>
      </Box>
    </Container>
  );
};

export default Login;
