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
  const [user, setUser] = useState(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      try {
        return typeof storedUser === 'string' ? JSON.parse(storedUser) : storedUser;
      } catch (e) {
        console.error('Error parsing initial user from localStorage:', e);
      }
    }
    return null;
  });

  const [token, setToken] = useState(() => localStorage.getItem('token') || null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkToken = async () => {
      const storedToken = localStorage.getItem('token');
      const storedUser = localStorage.getItem('user');

      if (storedUser) {
        try {
          setUser(typeof storedUser === 'string' ? JSON.parse(storedUser) : storedUser);
        } catch (e) {
          console.error('Error parsing stored user:', e);
        }
      }

      if (storedToken) {
        setToken(storedToken);
        try {
          const res = await authAPI.getMe();
          const userData = res.data?.user || res.data;
          if (userData) {
            setUser(userData);
            localStorage.setItem('user', JSON.stringify(userData));
          }
        } catch (error) {
          console.error('Failed to verify token:', error);
          if (!storedUser) {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            setToken(null);
            setUser(null);
          }
        }
      }
      setLoading(false);
    };

    checkToken();
  }, []);

  const login = async (credentials) => {
    try {
      const res = await authAPI.login(credentials);
      const responseData = res.data;
      const authToken = responseData?.access_token || responseData?.token;
      const userData = responseData?.user;

      if (authToken) {
        localStorage.setItem('token', authToken);
        setToken(authToken);
      }

      if (userData) {
        localStorage.setItem('user', JSON.stringify(userData));
        setUser(userData);
      } else if (authToken) {
        try {
          const meRes = await authAPI.getMe();
          const meUser = meRes.data?.user || meRes.data;
          if (meUser) {
            localStorage.setItem('user', JSON.stringify(meUser));
            setUser(meUser);
          }
        } catch (e) {
          console.error('Failed to fetch user in login:', e);
        }
      }
      return responseData;
    } catch (error) {
      throw error;
    }
  };

  const register = async (userDataInput) => {
    try {
      const res = await authAPI.register(userDataInput);
      const responseData = res.data;
      const authToken = responseData?.access_token || responseData?.token;
      const userData = responseData?.user;

      if (authToken) {
        localStorage.setItem('token', authToken);
        setToken(authToken);
      }

      if (userData) {
        localStorage.setItem('user', JSON.stringify(userData));
        setUser(userData);
      } else if (authToken) {
        try {
          const meRes = await authAPI.getMe();
          const meUser = meRes.data?.user || meRes.data;
          if (meUser) {
            localStorage.setItem('user', JSON.stringify(meUser));
            setUser(meUser);
          }
        } catch (e) {
          console.error('Failed to fetch user in register:', e);
        }
      }
      return responseData;
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
      const updatedUser = res.data?.user || res.data;
      if (updatedUser) {
        setUser(updatedUser);
        localStorage.setItem('user', JSON.stringify(updatedUser));
      }
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
