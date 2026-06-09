import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

export const sendMessage = async (message, chatContext = null) => {
  try {
    const response = await axios.post(`${API_BASE}/chat`, {
      message,
      chat_context: chatContext,
      session_id: localStorage.getItem('sessionId') || Date.now().toString()
    });
    return response.data;
  } catch (error) {
    const detail = error.response?.data?.detail || 'Network error. Please try again.';
    throw new Error(detail);
  }
};