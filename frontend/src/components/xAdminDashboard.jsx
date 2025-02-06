// src/components/AdminDashboard.jsx
import React, { useState } from 'react';
import { 
  Box, Button, Container, Typography, List, ListItem, ListItemText, TextField, Paper, ListItemButton 
} from '@mui/material';
import { uploadDocument, deleteDocument, getDocument, chatWithBot } from '../api';
import { useAuth } from '../context/AuthContext';

const AdminDashboard = () => {
  const { user } = useAuth();
  
  // File upload states
  const [selectedFile, setSelectedFile] = useState(null);
  console.log(selectedFile);
  const [uploadedFiles, setUploadedFiles] = useState([]); // list of filenames
  console.log(uploadedFiles);
  const [uploadMessage, setUploadMessage] = useState('');
  console.log(uploadMessage);
  // Chat states
  const [chatInput, setChatInput] = useState('');
  console.log(chatInput);
  const [chatHistory, setChatHistory] = useState([]);
  console.log(chatHistory);

    // Fetch files on component mount
    useEffect(() => {
      fetchFiles();
    }, []);
    
  // Handle file selection
  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  // Handle file upload
  const handleUpload = async () => {
    if (!selectedFile) return;
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const res = await uploadDocument(formData, user.token);
      setUploadMessage(res.data.message);
      setUploadedFiles(prev => [...prev, selectedFile.name]);
      setSelectedFile(null);
    } catch (err) {
      setUploadMessage('Upload failed.');
    }
  };

  // Handle file deletion
  const handleDelete = async (filename) => {
    try {
      const res = await deleteDocument(filename, user.token);
      setUploadMessage(res.data.message);
      setUploadedFiles(prev => prev.filter(f => f !== filename));
    } catch (err) {
      setUploadMessage('Delete failed.');
    }
  };

   // Handle file deletion
   const fetchFiles = async () => {
    try {
      const res = await getDocument(user.token);
      setUploadedFiles(res.data.files);
      //setUploadedFiles(prev => prev.filter(f => f !== filename));
    } catch (err) {
      setUploadMessage('fetch failed.');
    }
  };

  // Handle sending chat message
  const handleSendChat = async () => {
    if (!chatInput.trim()) return;
    
    // Append admin's message
    setChatHistory(prev => [...prev, { sender: 'You', text: chatInput }]);
    try {
      const res = await chatWithBot({ user_message: chatInput }, user.token);
      setChatHistory(prev => [...prev, { sender: 'Bot', text: res.data.response }]);
      setChatInput('');
    } catch (err) {
      setChatHistory(prev => [...prev, { sender: 'Bot', text: 'Error: Could not get response.' }]);
    }
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ mt: 4 }}>
        <Typography variant="h4" gutterBottom>
          Admin Dashboard
        </Typography>
        
        {/* Upload Section */}
        <Box sx={{ mb: 4 }}>
          <Button variant="contained" component="label">
            Upload Document
            <input type="file" hidden onChange={handleFileChange} />
          </Button>
          {selectedFile && (
            <Box sx={{ mt: 1 }}>
              <Typography variant="body1">{selectedFile.name}</Typography>
              <Button variant="outlined" onClick={handleUpload} sx={{ mt: 1 }}>
                Upload
              </Button>
            </Box>
          )}
          {uploadMessage && (
            <Typography variant="body2" color="primary" sx={{ mt: 2 }}>
              {uploadMessage}
            </Typography>
          )}
        </Box>

        {/* View/Delete Section */}
        <Box sx={{ mb: 4 }}>
          <Typography variant="h6">Uploaded Documents</Typography>
          <List>
            {uploadedFiles.map((filename) => (
              <ListItem 
                key={filename}
                secondaryAction={
                  <Button color="error" onClick={() => handleDelete(filename)}>
                    Delete
                  </Button>
                }
              >
                <ListItemText primary={filename} />
              </ListItem>
            ))}
          </List>
        </Box>
      </Box>
    </Container>
  );
};

export default AdminDashboard;
