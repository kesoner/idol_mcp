import { render, screen, fireEvent } from '@testing-library/react';
import { describe, test, expect, beforeEach, vi } from 'vitest';
import Login from '../Login';

describe('Login Component', () => {
  const mockOnLogin = vi.fn();

  beforeEach(() => {
    mockOnLogin.mockClear();
  });

  test('renders login form', () => {
    render(<Login onLogin={mockOnLogin} />);
    
    expect(screen.getByText('歡迎來到 IdolMCP')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('請輸入您的名字')).toBeInTheDocument();
    expect(screen.getByText('開始聊天')).toBeInTheDocument();
  });

  test('shows error message when submitting empty form', () => {
    render(<Login onLogin={mockOnLogin} />);
    
    const submitButton = screen.getByText('開始聊天');
    fireEvent.click(submitButton);
    
    expect(screen.getByText('請輸入用戶名')).toBeInTheDocument();
    expect(mockOnLogin).not.toHaveBeenCalled();
  });

  test('calls onLogin with correct data when form is submitted', () => {
    render(<Login onLogin={mockOnLogin} />);
    
    const input = screen.getByPlaceholderText('請輸入您的名字');
    const submitButton = screen.getByText('開始聊天');
    
    fireEvent.change(input, { target: { value: 'Test User' } });
    fireEvent.click(submitButton);
    
    expect(mockOnLogin).toHaveBeenCalledWith({
      userId: expect.stringMatching(/^user_\d+$/),
      username: 'Test User'
    });
  });

  test('handles form submission with Enter key', () => {
    render(<Login onLogin={mockOnLogin} />);
    
    const input = screen.getByPlaceholderText('請輸入您的名字');
    
    fireEvent.change(input, { target: { value: 'Test User' } });
    fireEvent.keyDown(input, { key: 'Enter', code: 'Enter' });
    
    expect(mockOnLogin).toHaveBeenCalledWith({
      userId: expect.stringMatching(/^user_\d+$/),
      username: 'Test User'
    });
  });
}); 