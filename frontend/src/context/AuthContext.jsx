import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from '../services/api';

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
  const [token, setToken] = useState(localStorage.getItem('token') || null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkToken = async () => {
      const storedToken = localStorage.getItem('token');
      if (storedToken) {
        try {
          const res = await authAPI.getMe();
          setUser(res.data);
          setToken(storedToken);
        } catch (error) {
          console.error('Failed to verify token:', error);
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          setToken(null);
          setUser(null);
        }
      }
      setLoading(false);
    };

    checkToken();
  }, []);

  const login = async (credentials) => {
    try {
      const res = await authAPI.login(credentials);
      const authToken = res.data.access_token || res.data.token;
      const userData = res.data.user || res.data;

      localStorage.setItem('token', authToken);
      setToken(authToken);

      if (res.data.user) {
        setUser(res.data.user);
      } else {
        const meRes = await authAPI.getMe();
        setUser(meRes.data);
      }
      return res.data;
    } catch (error) {
      throw error;
    }
  };

  const register = async (userData) => {
    try {
      const res = await authAPI.register(userData);
      const authToken = res.data.access_token || res.data.token;

      if (authToken) {
        localStorage.setItem('token', authToken);
        setToken(authToken);
        if (res.data.user) {
          setUser(res.data.user);
        } else {
          const meRes = await authAPI.getMe();
          setUser(meRes.data);
        }
      }
      return res.data;
    } catch (error) {
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setToken(null);
    setUser(null);
  };

  const updateUser = async (updatedData) => {
    try {
      const res = await authAPI.updateProfile(updatedData);
      setUser(res.data);
      return res.data;
    } catch (error) {
      throw error;
    }
  };

  const value = {
    user,
    token,
    loading,
    isAuthenticated: !!user && !!token,
    login,
    register,
    logout,
    updateUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthContext;
