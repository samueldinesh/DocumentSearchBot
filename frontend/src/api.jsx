import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000'; // update to your backend URL

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Example login function (mock)
export const loginUser = async (username, password) => {
  // In production, you'd call your login endpoint
  // For demo, we simply resolve with role based on username
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (username === 'admin' && password === 'adminpass') {
        resolve({ token: 'admin-token', role: 'admin' });
      } else if (username === 'user' && password === 'userpass') {
        resolve({ token: 'user-token', role: 'user' });
      } else {
        reject(new Error('Invalid credentials'));
      }
    }, 500);
  });
};

export const uploadDocument = async (formData, token) => {
  return api.post('/documents/upload', formData, {
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'multipart/form-data' },
  });
};

export const deleteDocument = async (filename, token) => {
  return api.delete(`/documents/${filename}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
};

export const getDocument = async (token) => {
  return api.get('/documents/getfile', {  // Updated endpoint
    headers: { Authorization: `Bearer ${token}` },
  });
};

export const chatWithBot = async (message, token) => {
  return api.post('/chat', { user_message: message }, {
    headers: { Authorization: `Bearer ${token}` },
  });
};

export default api;