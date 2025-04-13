import { useState, useRef, useEffect } from 'react'
import Live2DDisplay from './components/Live2DModel'
import Login from './components/Login'
import { authService } from './services/authService'
import { chatService } from './services/chatService'
import './App.css'
import LoadingDots from './components/LoadingDots'

function App() {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const live2dRef = useRef(null)
  const [isTracking, setIsTracking] = useState(true)
  const [emotion, setEmotion] = useState('neutral')
  const [emotionIntensity, setEmotionIntensity] = useState(0.5)
  const [user, setUser] = useState(null)
  const messagesEndRef = useRef(null)

  // 檢查用戶登入狀態
  useEffect(() => {
    const currentUser = authService.getCurrentUser()
    if (currentUser) {
      setUser(currentUser)
    }
  }, [])

  // 自動滾動到最新消息
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [messages])

  useEffect(() => {
    const handleKeyPress = (e) => {
      if (e.code === 'Space' && e.target.tagName !== 'INPUT') {
        e.preventDefault()
        setIsTracking(!isTracking)
        if (live2dRef.current) {
          live2dRef.current.setTracking(!isTracking)
        }
      }
    }

    window.addEventListener('keydown', handleKeyPress)
    return () => window.removeEventListener('keydown', handleKeyPress)
  }, [isTracking])

  // 情緒到表情的映射
  const emotionToExpression = {
    'neutral': '咪咪眼',
    'happy': '爱心',
    'excited': '钱钱眼',
    'sad': '泪眼',
    'angry': '生气',
    'shy': '脸红',
    'confident': 'nn眼'
  }

  const handleSubmit = async () => {
    if (!input.trim() || !user) return
    
    const userMessage = { 
      id: Date.now(),
      type: 'user', 
      content: input.trim(), 
      username: user.username 
    }
    
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)
    
    try {
      const response = await chatService.sendMessage(user.userId, input.trim())
      
      // 更新情緒狀態
      if (response.emotion) {
        setEmotion(response.emotion)
        setEmotionIntensity(response.emotion_intensity || 0.5)
      }
      
      // 設置對應的表情
      if (live2dRef.current && response.emotion) {
        const expression = emotionToExpression[response.emotion] || '咪咪眼'
        live2dRef.current.showExpression(expression)
      }
      
      // 更新消息
      const assistantMessage = { 
        id: Date.now(),
        type: 'assistant', 
        content: response.content || response.response,
        emotion: response.emotion,
        emotionIntensity: response.emotion_intensity || 0.5
      }
      
      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Error:', error)
      // 添加錯誤消息
      const errorMessage = {
        id: Date.now(),
        type: 'assistant',
        content: '抱歉，發生了一些錯誤，請稍後再試。',
        emotion: 'sad',
        emotionIntensity: 0.8
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const handleSendMessage = () => {
    handleSubmit()
  }

  const handleLogin = (userData) => {
    setUser(userData)
  }

  const handleLogout = () => {
    authService.logout()
    setUser(null)
    setMessages([])
  }

  // 獲取最後一條助手消息
  const lastAssistantMessage = messages
    .filter(msg => msg.type === 'assistant')
    .at(-1)

  if (!user) {
    return <Login onLogin={handleLogin} />
  }

  return (
    <div className="app">
      <div className="user-info">
        <span className="username">歡迎, {user.username}</span>
        <button onClick={handleLogout} className="logout-button">登出</button>
      </div>

      <div className="live2d-main">
        {process.env.NODE_ENV === 'test' ? (
          <div data-testid="live2d-model">Live2D Model</div>
        ) : (
          <Live2DDisplay ref={live2dRef} />
        )}
        <div className="subtitles">
          {loading ? (
            <div className="subtitle-text loading">
              <LoadingDots />
            </div>
          ) : lastAssistantMessage && (
            <div className="subtitle-text">
              {lastAssistantMessage.content}
            </div>
          )}
        </div>
        <div className="emotion-display">
          <span className={`emotion-badge ${emotion}`}>
            {emotion} ({emotionIntensity.toFixed(2)})
          </span>
        </div>
      </div>

      <div className="chat-container">
        {messages.map((message) => (
          <div key={message.id} className={`message ${message.type}`} data-testid={`message-${message.type}`}>
            {message.type === 'user' ? (
              <>
                <div className="message-username" data-testid="message-username">{message.username}</div>
                <div className="message-content" data-testid="message-content">{message.content}</div>
              </>
            ) : (
              <>
                <div className="message-content" data-testid="bot-message-content">{message.content}</div>
                {message.emotion && (
                  <div className="message-emotion" data-testid="bot-message-emotion">
                    {message.emotion} ({message.emotionIntensity.toFixed(2)})
                  </div>
                )}
              </>
            )}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-container">
        <input
          className="chat-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && handleSendMessage()}
          placeholder="輸入消息..."
          disabled={loading}
        />
        <button
          className="send-button"
          onClick={handleSendMessage}
          disabled={loading}
        >
          發送
        </button>
      </div>
    </div>
  )
}

export default App