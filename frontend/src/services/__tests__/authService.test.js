import { authService } from '../authService';

describe('authService', () => {
  beforeEach(() => {
    // 清除 localStorage
    localStorage.clear();
  });

  test('getCurrentUser should return null when no user is logged in', () => {
    expect(authService.getCurrentUser()).toBeNull();
  });

  test('login should store user data in localStorage', () => {
    const userId = 'test_user_123';
    const username = 'Test User';
    
    const userData = authService.login(userId, username);
    
    expect(userData).toEqual({
      userId,
      username,
      timestamp: expect.any(String)
    });
    
    expect(localStorage.getItem('idolmcp_auth')).toBe(JSON.stringify(userData));
  });

  test('getCurrentUser should return logged in user data', () => {
    const userId = 'test_user_123';
    const username = 'Test User';
    
    authService.login(userId, username);
    const currentUser = authService.getCurrentUser();
    
    expect(currentUser).toEqual({
      userId,
      username,
      timestamp: expect.any(String)
    });
  });

  test('logout should remove user data from localStorage', () => {
    authService.login('test_user_123', 'Test User');
    authService.logout();
    
    expect(localStorage.getItem('idolmcp_auth')).toBeNull();
    expect(authService.getCurrentUser()).toBeNull();
  });

  test('isAuthenticated should return correct authentication status', () => {
    expect(authService.isAuthenticated()).toBe(false);
    
    authService.login('test_user_123', 'Test User');
    expect(authService.isAuthenticated()).toBe(true);
    
    authService.logout();
    expect(authService.isAuthenticated()).toBe(false);
  });
}); 