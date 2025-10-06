import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // 只有在不是登录请求的情况下才清除token并重定向
      if (!error.config.url.includes('/auth/login')) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export const login = async (username, password) => {
  try {
    const response = await api.post('/auth/login', { username, password });
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const register = async (username, email, password) => {
  try {
    const response = await api.post('/auth/register', { username, email, password });
    return response.data;
  } catch (error) {
    console.log(error)
    throw error;
  }
};

export const getUserProfile = async () => {
  try {
    const token = localStorage.getItem('token');
    if (!token) {
      // 如果没有令牌，可以立即抛出错误或返回特定的错误状态
      throw new Error('No authentication token found');
    }    

    verifyToken();

    const response = await api.get('/auth/profile');
    return response.data;
  } catch (error) {
    throw error;
  }
};

    const verifyToken = async () => {
        try {
          const response = await axios.get('http://localhost:5000/api/protected');
          // 如果token有效，可以在这里获取用户信息
          setUser({ id: response.data.user_id });
          setLoading(false);
        } catch (error) {
          // token无效，尝试刷新
          await refreshToken();
        }
      };

export const logout = async () => {
  try {
    await api.post('/auth/logout');
  } catch (error) {
    console.error('Logout error:', error);
  } finally {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }
};

export default api;
