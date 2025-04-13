import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import { describe, test, expect, beforeEach, vi } from 'vitest';
import Chat from '../Chat';
import { chatService } from '../../services/chatService';

// Mock the chatService
vi.mock('../../services/chatService', () => ({
  chatService: {
    sendMessage: vi.fn(),
    getChatHistory: vi.fn()
  }
}));

describe('Chat Component', () => {
  const mockUser = {
    userId: 'user_123',
    username: 'Test User'
  };

  beforeEach(() => {
    vi.clearAllMocks();
    chatService.getChatHistory.mockResolvedValue([]);
  });

  test('renders chat interface correctly', async () => {
    await act(async () => {
      render(<Chat user={mockUser} />);
    });
    
    expect(screen.getByPlaceholderText('輸入消息...')).toBeInTheDocument();
    expect(screen.getByText('發送')).toBeInTheDocument();
  });

  test('displays chat history', async () => {
    const mockHistory = [
      { id: 1, content: 'Hello!', sender: 'user', timestamp: '2024-01-01T00:00:00Z' },
      { id: 2, content: 'Hi there!', sender: 'bot', timestamp: '2024-01-01T00:00:01Z' }
    ];
    
    chatService.getChatHistory.mockResolvedValue(mockHistory);
    
    await act(async () => {
      render(<Chat user={mockUser} />);
    });
    
    await waitFor(() => {
      expect(screen.getByText('Hello!')).toBeInTheDocument();
      expect(screen.getByText('Hi there!')).toBeInTheDocument();
    });
  });

  test('handles message submission', async () => {
    const userMessage = 'Test message';
    const mockResponse = {
      id: 3,
      content: 'This is a response',
      sender: 'bot',
      timestamp: '2024-01-01T00:00:02Z'
    };
    
    chatService.sendMessage.mockResolvedValue(mockResponse);
    
    await act(async () => {
      render(<Chat user={mockUser} />);
    });
    
    const input = screen.getByPlaceholderText('輸入消息...');
    const sendButton = screen.getByText('發送');
    
    await act(async () => {
      fireEvent.change(input, { target: { value: userMessage } });
      fireEvent.click(sendButton);
    });
    
    await waitFor(() => {
      expect(chatService.sendMessage).toHaveBeenCalledWith('user_123', userMessage);
    });

    await waitFor(() => {
      expect(screen.getByText(mockResponse.content)).toBeInTheDocument();
    });
  });

  test('handles empty message submission', async () => {
    await act(async () => {
      render(<Chat user={mockUser} />);
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
    const userMessage = 'Enter key test';
    const mockResponse = {
      id: 4,
      content: 'Enter key response',
      sender: 'bot',
      timestamp: '2024-01-01T00:00:03Z'
    };
    
    chatService.sendMessage.mockResolvedValue(mockResponse);
    
    await act(async () => {
      render(<Chat user={mockUser} />);
    });
    
    const input = screen.getByPlaceholderText('輸入消息...');
    
    await act(async () => {
      fireEvent.change(input, { target: { value: userMessage } });
      fireEvent.keyDown(input, { key: 'Enter', code: 'Enter' });
    });
    
    await waitFor(() => {
      expect(chatService.sendMessage).toHaveBeenCalledWith('user_123', userMessage);
    });

    await waitFor(() => {
      expect(screen.getByText(mockResponse.content)).toBeInTheDocument();
    });
  });

  test('handles chat service errors', async () => {
    chatService.sendMessage.mockRejectedValue(new Error('Chat service error'));
    
    await act(async () => {
      render(<Chat user={mockUser} />);
    });
    
    const input = screen.getByPlaceholderText('輸入消息...');
    const sendButton = screen.getByText('發送');
    
    await act(async () => {
      fireEvent.change(input, { target: { value: 'Error test' } });
      fireEvent.click(sendButton);
    });
    
    await waitFor(() => {
      expect(screen.getByText('發送消息時發生錯誤')).toBeInTheDocument();
    });
  });
}); 