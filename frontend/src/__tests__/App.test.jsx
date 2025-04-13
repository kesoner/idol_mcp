import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import { describe, test, expect, beforeEach, vi } from 'vitest';
import App from '../App';
import { authService } from '../services/authService';
import { chatService } from '../services/chatService';

// Mock the authService
vi.mock('../services/authService', () => ({
  authService: {
    getCurrentUser: vi.fn(),
    login: vi.fn(),
    logout: vi.fn(),
    isAuthenticated: vi.fn()
  }
}));

// Mock the chatService
vi.mock('../services/chatService', () => ({
  chatService: {
    sendMessage: vi.fn(),
    getChatHistory: vi.fn()
  }
}));

// Mock the Live2DModel component
vi.mock('../components/Live2DModel', () => ({
  default: function DummyLive2DModel() {
    return <div data-testid="live2d-model">Live2D Model</div>;
  }
}));

describe('App Component', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    vi.clearAllMocks();
  });

  test('renders login form when user is not authenticated', async () => {
    authService.isAuthenticated.mockReturnValue(false);
    authService.getCurrentUser.mockReturnValue(null);

    await act(async () => {
      render(<App />);
    });
    
    expect(screen.getByText('歡迎來到 IdolMCP')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('請輸入您的名字')).toBeInTheDocument();
  });

  test('renders chat interface when user is authenticated', async () => {
    authService.isAuthenticated.mockReturnValue(true);
    authService.getCurrentUser.mockReturnValue({
      userId: 'user_123',
      username: 'Test User'
    });

    await act(async () => {
      render(<App />);
    });
    
    expect(screen.getByText('歡迎, Test User')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('輸入消息...')).toBeInTheDocument();
    expect(screen.getByTestId('live2d-model')).toBeInTheDocument();
  });

  test('handles user login', async () => {
    authService.isAuthenticated.mockReturnValue(false);
    authService.getCurrentUser.mockReturnValue(null);
    authService.login.mockImplementation((user) => {
      authService.getCurrentUser.mockReturnValue(user);
      authService.isAuthenticated.mockReturnValue(true);
    });

    await act(async () => {
      render(<App />);
    });
    
    const input = screen.getByPlaceholderText('請輸入您的名字');
    const submitButton = screen.getByText('開始聊天');
    
    await act(async () => {
      fireEvent.change(input, { target: { value: 'Test User' } });
      fireEvent.click(submitButton);
    });
    
    await waitFor(() => {
      expect(screen.getByText('歡迎, Test User')).toBeInTheDocument();
    });
  });

  test('handles user logout', async () => {
    authService.isAuthenticated.mockReturnValue(true);
    authService.getCurrentUser.mockReturnValue({
      userId: 'user_123',
      username: 'Test User'
    });
    authService.logout.mockImplementation(() => {
      authService.getCurrentUser.mockReturnValue(null);
      authService.isAuthenticated.mockReturnValue(false);
    });

    await act(async () => {
      render(<App />);
    });
    
    const logoutButton = screen.getByText('登出');
    
    await act(async () => {
      fireEvent.click(logoutButton);
    });
    
    await waitFor(() => {
      expect(screen.getByText('歡迎來到 IdolMCP')).toBeInTheDocument();
    });
  });

  test('handles chat message submission', async () => {
    authService.isAuthenticated.mockReturnValue(true);
    authService.getCurrentUser.mockReturnValue({
      userId: 'user_123',
      username: 'Test User'
    });
    
    chatService.getChatHistory.mockResolvedValue([]);
    const mockResponse = {
      response: 'Hello!',
      emotion: 'happy',
      emotion_intensity: 0.8
    };
    chatService.sendMessage.mockResolvedValue(mockResponse);

    render(<App />);
    
    const input = screen.getByPlaceholderText('輸入消息...');
    const sendButton = screen.getByText('發送');
    
    fireEvent.change(input, { target: { value: 'Hello!' } });
    
    await act(async () => {
      fireEvent.click(sendButton);
    });
    
    expect(chatService.sendMessage).toHaveBeenCalledWith('user_123', 'Hello!');
    
    await waitFor(() => {
      expect(screen.getByText('Test User')).toBeInTheDocument();
    }, { timeout: 2000 });
    
    await waitFor(() => {
      expect(screen.getByText('Hello!')).toBeInTheDocument();
    }, { timeout: 2000 });
    
    await waitFor(() => {
      expect(screen.getByText(`${mockResponse.emotion} (${mockResponse.emotion_intensity.toFixed(2)})`)).toBeInTheDocument();
    }, { timeout: 2000 });
  });
}); 