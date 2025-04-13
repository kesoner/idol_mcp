import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import { describe, test, expect, vi, beforeEach } from 'vitest';
import App from '../App';
import { authService } from '../services/authService';
import { chatService } from '../services/chatService';

// Mock the services
vi.mock('../services/authService', () => ({
  authService: {
    isAuthenticated: vi.fn(),
    getCurrentUser: vi.fn(),
    login: vi.fn(),
    logout: vi.fn()
  }
}));

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

describe('Message Submission', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    authService.isAuthenticated.mockReturnValue(true);
    authService.getCurrentUser.mockReturnValue({
      userId: 'test_user',
      username: 'Test User'
    });
    chatService.getChatHistory.mockResolvedValue([]);
  });

  test('displays user message correctly', async () => {
    const mockResponse = {
      response: 'Test response',
      emotion: 'happy',
      emotion_intensity: 0.8
    };
    chatService.sendMessage.mockResolvedValue(mockResponse);
    
    await act(async () => {
      render(<App />);
    });
    
    const input = screen.getByPlaceholderText('輸入消息...');
    const sendButton = screen.getByText('發送');
    
    await act(async () => {
      fireEvent.change(input, { target: { value: 'Hello' } });
    });
    
    await act(async () => {
      fireEvent.click(sendButton);
    });
    
    await waitFor(() => {
      const userMessage = screen.getByTestId('message-username');
      const messageContent = screen.getByTestId('message-content');
      expect(userMessage).toHaveTextContent('Test User');
      expect(messageContent).toHaveTextContent('Hello');
    }, { timeout: 5000 });
  });

  test('displays bot response correctly', async () => {
    const mockResponse = {
      response: 'Hi there!',
      emotion: 'happy',
      emotion_intensity: 0.8
    };
    chatService.sendMessage.mockResolvedValue(mockResponse);
    
    await act(async () => {
      render(<App />);
    });
    
    const input = screen.getByPlaceholderText('輸入消息...');
    const sendButton = screen.getByText('發送');
    
    await act(async () => {
      fireEvent.change(input, { target: { value: 'Hello' } });
    });
    
    await act(async () => {
      fireEvent.click(sendButton);
    });
    
    await waitFor(() => {
      expect(chatService.sendMessage).toHaveBeenCalledWith('test_user', 'Hello');
    }, { timeout: 5000 });
    
    await waitFor(() => {
      const botResponse = screen.getByTestId('bot-message-content');
      const emotionText = screen.getByTestId('bot-message-emotion');
      expect(botResponse).toHaveTextContent('Hi there!');
      expect(emotionText).toHaveTextContent('happy (0.80)');
    }, { timeout: 5000 });
  });

  test('handles empty message submission', async () => {
    await act(async () => {
      render(<App />);
    });
    
    const sendButton = screen.getByText('發送');
    
    await act(async () => {
      fireEvent.click(sendButton);
    });
    
    await waitFor(() => {
      expect(chatService.sendMessage).not.toHaveBeenCalled();
    });
  });

  test('handles message submission with Enter key', async () => {
    const mockResponse = {
      response: 'Enter key test',
      emotion: 'happy',
      emotion_intensity: 0.8
    };
    chatService.sendMessage.mockResolvedValue(mockResponse);
    
    await act(async () => {
      render(<App />);
    });
    
    const input = screen.getByPlaceholderText('輸入消息...');
    
    await act(async () => {
      fireEvent.change(input, { target: { value: 'Hello' } });
    });
    
    await act(async () => {
      fireEvent.keyDown(input, { key: 'Enter', code: 'Enter' });
    });
    
    await waitFor(() => {
      expect(chatService.sendMessage).toHaveBeenCalledWith('test_user', 'Hello');
    }, { timeout: 5000 });
  });
}); 