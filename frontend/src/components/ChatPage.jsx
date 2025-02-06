// src/components/ChatPage.jsx
import React, { useState } from 'react';
import { Box, Container, TextField, Button, Typography, Paper, List, ListItem, ListItemText } from '@mui/material';
import { chatWithBot } from '../api';
import { useAuth } from '../context/AuthContext';

const ChatPage = () => {
  const { user } = useAuth();
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);

  const handleSend = async () => {
    if (!message.trim()) return;
    // Append user message to chat history
    setChatHistory((prev) => [...prev, { sender: 'user', text: message }]);
    try {
      const res = await chatWithBot(message, user.token);
      setChatHistory((prev) => [...prev, { sender: 'bot', text: res.data.response }]);
      setMessage('');
    } catch (err) {
      setChatHistory((prev) => [...prev, { sender: 'bot', text: 'Error: could not get a response.' }]);
    }
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ mt: 4 }}>
        <Typography variant="h4" gutterBottom>
          Chat with Document Bot
        </Typography>
        <Paper sx={{ p: 2, height: '60vh', overflowY: 'auto', mb: 2 }}>
          <List>
            {chatHistory.map((entry, index) => (
              <ListItem key={index}>
                <ListItemText
                  primary={entry.sender === 'user' ? `You: ${entry.text}` : `Bot: ${entry.text}`}
                />
              </ListItem>
            ))}
          </List>
        </Paper>
        <Box sx={{ display: 'flex' }}>
          <TextField
            fullWidth
            label="Your Message"
            variant="outlined"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
          />
          <Button variant="contained" onClick={handleSend} sx={{ ml: 2 }}>
            Send
          </Button>
        </Box>
      </Box>
    </Container>
  );
};

export default ChatPage;
