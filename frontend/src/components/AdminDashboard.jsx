// src/components/AdminDashboard.jsx
import React, { useState, useEffect } from 'react';
import { 
  Box, Button, Container, Typography, List, ListItem, ListItemText,
  IconButton, Link
} from '@mui/material';
import { Delete, Download } from '@mui/icons-material';
import { uploadDocument, deleteDocument, getDocument } from '../api';
import { useAuth } from '../context/AuthContext';

const AdminDashboard = () => {
  const { user } = useAuth();
  
  // File upload states
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [uploadMessage, setUploadMessage] = useState('');

  // Fetch files on component mount and after changes
  useEffect(() => {
    fetchFiles();
  }, []);

  const fetchFiles = async () => {
    try {
      const response = await getDocument(user.token);
      setUploadedFiles(response.data.files || []);
    } catch (err) {
      setUploadMessage('Failed to fetch documents');
    }
  };

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      await uploadDocument(formData, user.token);
      setUploadMessage('File uploaded successfully');
      await fetchFiles(); // Refresh file list
      setSelectedFile(null);
    } catch (err) {
      setUploadMessage('Upload failed. Please try again.');
    }
  };

  const handleDelete = async (filename) => {
    try {
      await deleteDocument(filename, user.token);
      setUploadMessage('File deleted successfully');
      await fetchFiles(); // Refresh file list
    } catch (err) {
      setUploadMessage('Delete failed. Please try again.');
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
            <input 
              type="file" 
              hidden 
              onChange={handleFileChange}
              accept=".pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx"
            />
          </Button>
          
          {selectedFile && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="body1">
                Selected file: {selectedFile.name}
              </Typography>
              <Button 
                variant="contained" 
                onClick={handleUpload}
                sx={{ mt: 1, mr: 2 }}
              >
                Confirm Upload
              </Button>
              <Button 
                variant="outlined" 
                onClick={() => setSelectedFile(null)}
                sx={{ mt: 1 }}
              >
                Cancel
              </Button>
            </Box>
          )}
          
          {uploadMessage && (
            <Typography 
              variant="body2" 
              color={uploadMessage.includes('failed') ? 'error' : 'success'} 
              sx={{ mt: 2 }}
            >
              {uploadMessage}
            </Typography>
          )}
        </Box>

        {/* Uploaded Documents Section */}
        <Box sx={{ mb: 4 }}>
          <Typography variant="h6" gutterBottom>
            Managed Documents ({uploadedFiles.length})
          </Typography>
          
          <List dense sx={{ maxHeight: 400, overflow: 'auto' }}>
            {uploadedFiles.map((filename) => (
              <ListItem 
                key={filename}
                secondaryAction={
                  <IconButton 
                    edge="end" 
                    onClick={() => handleDelete(filename)}
                    color="error"
                  >
                    <Delete />
                  </IconButton>
                }
              >
                <ListItemText
                  primary={
                    <Link
                      href={`http://localhost:8000/uploads/${filename}`}
                      target="_blank"
                      rel="noopener"
                      sx={{ textDecoration: 'none' }}
                    >
                      {filename}
                    </Link>
                  }
                  secondary={
                    <IconButton 
                      href={`http://localhost:8000/uploads/${filename}`}
                      download
                      size="small"
                    >
                      <Download fontSize="small" />
                    </IconButton>
                  }
                />
              </ListItem>
            ))}
          </List>
        </Box>
      </Box>
    </Container>
  );
};

export default AdminDashboard;