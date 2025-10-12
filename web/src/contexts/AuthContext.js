import React, { createContext, useContext, useState, useEffect } from 'react';
import { login as loginService, logout as logoutService, getUserProfile } from '../services/authService';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    
    if (token && userData) {
      try {
        const parsedUser = JSON.parse(userData);
        setUser(parsedUser);
        setIsAuthenticated(true);
      } catch (e) {
        console.error('Error parsing user data:', e);
        localStorage.removeItem('user');
        localStorage.removeItem('token');
      }
    }
    
    setLoading(false);
  }, []);

  const login = async (username, password) => {
    try {
      const response = await loginService(username, password);
      
      if (!response || !response.token || !response.user) {
        throw new Error('Invalid login response');
      }
      
      localStorage.setItem('token', response.token);
      localStorage.setItem('user', JSON.stringify(response.user));
      
      setUser(response.user);
      setIsAuthenticated(true);
      
      return response;
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  };

  const logout = async () => {
    try {
      await logoutService();
    } catch (error) {
      console.error('Logout error:', error);
      // 即使API调用失败，也要清除本地状态
    } finally {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      setUser(null);
      setIsAuthenticated(false);
    }
  };

  const verifyToken = async () => {
    try {
      const userData = await getUserProfile();
      setUser(userData);
      localStorage.setItem('user', JSON.stringify(userData));
      return userData;
    } catch (error) {
      console.error('Token verification error:', error);
      if (error.response?.status === 401) {
        logout();
      }
      throw error;
    }
  };

  const value = {
    user,
    isAuthenticated,
    loading,
    login,
    logout,
    verifyToken
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
