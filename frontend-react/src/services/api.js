import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const chatService = {
  // Send message to chatbot
  sendMessage: async (message) => {
    try {
      const response = await api.post('/chat', { message });
      return response.data;
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  },

  // Send feedback
  sendFeedback: async (feedback, answer, question) => {
    try {
      const response = await api.post('/feedback', {
        feedback,
        answer,
        question,
      });
      return response.data;
    } catch (error) {
      console.error('Error sending feedback:', error);
      throw error;
    }
  },

  // Check health
  checkHealth: async () => {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      console.error('Error checking health:', error);
      throw error;
    }
  },

  // Get stats
  getStats: async () => {
    try {
      const response = await api.get('/stats');
      return response.data;
    } catch (error) {
      console.error('Error getting stats:', error);
      throw error;
    }
  },

  // Get live analytics
  getLiveAnalytics: async () => {
    try {
      const response = await api.get('/analytics/live');
      return response.data;
    } catch (error) {
      console.error('Error getting live analytics:', error);
      throw error;
    }
  },
};

// Research & Evaluation APIs
export const generateResearchReport = async () => {
  try {
    const response = await api.get('/analytics/report');
    return response.data;
  } catch (error) {
    console.error('Error generating research report:', error);
    throw error;
  }
};

export const exportAnalytics = async () => {
  try {
    const response = await api.get('/analytics/export');
    return response.data;
  } catch (error) {
    console.error('Error exporting analytics:', error);
    throw error;
  }
};

export default api;
