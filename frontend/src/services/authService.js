// 用戶認證服務
const AUTH_KEY = 'idolmcp_auth';

export const authService = {
  // 獲取當前用戶
  getCurrentUser: () => {
    const userData = localStorage.getItem(AUTH_KEY);
    return userData ? JSON.parse(userData) : null;
  },

  // 登入
  login: (userId, username) => {
    const userData = {
      userId,
      username,
      timestamp: new Date().toISOString()
    };
    localStorage.setItem(AUTH_KEY, JSON.stringify(userData));
    return userData;
  },

  // 登出
  logout: () => {
    localStorage.removeItem(AUTH_KEY);
  },

  // 檢查是否已登入
  isAuthenticated: () => {
    return !!localStorage.getItem(AUTH_KEY);
  }
}; 