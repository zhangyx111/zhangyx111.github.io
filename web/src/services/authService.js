import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  // 不设置默认的Content-Type，让axios在发送FormData时自动设置multipart/form-data
});

// // Add token to requests
// api.interceptors.request.use((config) => {
//   const token = localStorage.getItem('token');
//   if (token) {
//     // 确保Authorization头的格式正确
//     config.headers.Authorization = String(`Bearer ${token}`);
//   }
//   return config;
// }, (error) => {
//   return Promise.reject(error);
// });

// 在请求拦截器中，打印token的payload
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;

    // 调试：解码token
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      console.log('Token payload:', payload);
      console.log('Subject type:', typeof payload.sub);
    } catch (e) {
      console.error('Failed to decode token:', e);
    }
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

// Handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      // 不直接在这里重定向，让调用者处理重定向
      // 这样可以避免在API调用时意外重定向
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
    const response = await api.get('/auth/profile');
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const logout = async () => {
  try {
    // 使用带有token的api实例调用logout
    // 后端需要验证token有效性
    await api.post('/auth/logout');
  } catch (error) {
    console.error('Logout error:', error);
    // 如果是401错误，说明token已经无效，这是正常情况
    if (error.response?.status !== 401) {
      // 对于非401错误，记录详细错误
      console.error('Logout failed with status:', error.response?.status);
    }
  } finally {
    // 无论API调用成功与否，都清除本地数据
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }
};

export default api;
