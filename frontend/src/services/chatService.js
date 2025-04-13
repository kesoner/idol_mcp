const CHAT_HISTORY_KEY = 'idolmcp_chat_history';
const API_BASE_URL = 'http://localhost:8002';

class ChatService {
  constructor() {
    this.loadChatHistory();
  }

  loadChatHistory() {
    try {
      const storedHistory = localStorage.getItem(CHAT_HISTORY_KEY);
      this.chatHistory = storedHistory ? JSON.parse(storedHistory) : {};
    } catch (error) {
      console.error('Error loading chat history:', error);
      this.chatHistory = {};
    }
  }

  saveChatHistory() {
    try {
      localStorage.setItem(CHAT_HISTORY_KEY, JSON.stringify(this.chatHistory));
    } catch (error) {
      console.error('Error saving chat history:', error);
    }
  }

  async getChatHistory(userId) {
    try {
      const response = await fetch(`${API_BASE_URL}/chat/history/${userId}`);
      if (!response.ok) {
        throw new Error('Failed to fetch chat history');
      }
      const data = await response.json();
      return data.messages || [];
    } catch (error) {
      console.error('Error fetching chat history:', error);
      return this.chatHistory[userId] || [];
    }
  }

  async sendMessage(userId, content) {
    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          message: content,
          platform: 'web'
        })
      });

      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      const data = await response.json();
      return {
        id: Date.now(),
        content: data.response,
        sender: 'bot',
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      console.error('Error sending message:', error);
      // 在 API 調用失敗時使用本地存儲作為備份
      const botResponse = {
        id: Date.now(),
        content: `你說: "${content}"`,
        sender: 'bot',
        timestamp: new Date().toISOString()
      };

      if (!this.chatHistory[userId]) {
        this.chatHistory[userId] = [];
      }

      const userMessage = {
        id: Date.now() - 1,
        content,
        sender: 'user',
        timestamp: new Date().toISOString()
      };

      this.chatHistory[userId].push(userMessage, botResponse);
      this.saveChatHistory();

      return botResponse;
    }
  }
}

export const chatService = new ChatService(); 