import React, { useState } from 'react';
import { authService } from '../services/authService';
import './Login.css';

const Login = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e?.preventDefault();
    if (!username.trim()) {
      setError('請輸入用戶名');
      return;
    }

    // 生成用戶ID（實際應用中應該由後端生成）
    const userId = `user_${Date.now()}`;
    authService.login(userId, username.trim());
    onLogin({ userId, username: username.trim() });
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>歡迎來到 IdolMCP</h2>
        <form onSubmit={handleSubmit} className="login-form">
          <div className="input-group">
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="請輸入您的名字"
              className="login-input"
            />
            {error && <div className="error-message">{error}</div>}
          </div>
          <button type="submit" className="login-button">
            開始聊天
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login; 