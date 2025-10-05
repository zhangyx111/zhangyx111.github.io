import api from './authService';

// 获取用户配置
export const getUserSettings = async () => {
  try {
    const response = await api.get('/api/v1/users/settings');
    return response.data;
  } catch (error) {
    console.error('获取用户配置失败:', error);
    throw error;
  }
};

// 更新用户配置
export const updateUserSettings = async (settings) => {
  try {
    const response = await api.put('/api/v1/users/settings', settings);
    return response.data;
  } catch (error) {
    console.error('更新用户配置失败:', error);
    throw error;
  }
};

// 获取通知设置
export const getNotificationSettings = async () => {
  try {
    const response = await api.get('/api/v1/users/notifications/settings');
    return response.data;
  } catch (error) {
    console.error('获取通知设置失败:', error);
    throw error;
  }
};

// 更新通知设置
export const updateNotificationSettings = async (settings) => {
  try {
    const response = await api.put('/api/v1/users/notifications/settings', settings);
    return response.data;
  } catch (error) {
    console.error('更新通知设置失败:', error);
    throw error;
  }
};

// 获取查询偏好
export const getQueryPreferences = async () => {
  try {
    const response = await api.get('/api/v1/users/query/preferences');
    return response.data;
  } catch (error) {
    console.error('获取查询偏好失败:', error);
    throw error;
  }
};

// 更新查询偏好
export const updateQueryPreferences = async (preferences) => {
  try {
    const response = await api.put('/api/v1/users/query/preferences', preferences);
    return response.data;
  } catch (error) {
    console.error('更新查询偏好失败:', error);
    throw error;
  }
};

// 获取界面主题
export const getThemeSettings = async () => {
  try {
    const response = await api.get('/api/v1/users/theme');
    return response.data;
  } catch (error) {
    console.error('获取界面主题失败:', error);
    throw error;
  }
};

// 更新界面主题
export const updateThemeSettings = async (theme) => {
  try {
    const response = await api.put('/api/v1/users/theme', theme);
    return response.data;
  } catch (error) {
    console.error('更新界面主题失败:', error);
    throw error;
  }
};

// 获取语言设置
export const getLanguageSettings = async () => {
  try {
    const response = await api.get('/api/v1/users/language');
    return response.data;
  } catch (error) {
    console.error('获取语言设置失败:', error);
    throw error;
  }
};

// 更新语言设置
export const updateLanguageSettings = async (language) => {
  try {
    const response = await api.put('/api/v1/users/language', { language });
    return response.data;
  } catch (error) {
    console.error('更新语言设置失败:', error);
    throw error;
  }
};

// 获取数据导出设置
export const getExportSettings = async () => {
  try {
    const response = await api.get('/api/v1/users/export/settings');
    return response.data;
  } catch (error) {
    console.error('获取数据导出设置失败:', error);
    throw error;
  }
};

// 更新数据导出设置
export const updateExportSettings = async (settings) => {
  try {
    const response = await api.put('/api/v1/users/export/settings', settings);
    return response.data;
  } catch (error) {
    console.error('更新数据导出设置失败:', error);
    throw error;
  }
};

// 获取隐私设置
export const getPrivacySettings = async () => {
  try {
    const response = await api.get('/api/v1/users/privacy');
    return response.data;
  } catch (error) {
    console.error('获取隐私设置失败:', error);
    throw error;
  }
};

// 更新隐私设置
export const updatePrivacySettings = async (settings) => {
  try {
    const response = await api.put('/api/v1/users/privacy', settings);
    return response.data;
  } catch (error) {
    console.error('更新隐私设置失败:', error);
    throw error;
  }
};

// 获取API密钥
export const getAPIKeys = async () => {
  try {
    const response = await api.get('/api/v1/users/api-keys');
    return response.data;
  } catch (error) {
    console.error('获取API密钥失败:', error);
    throw error;
  }
};

// 创建API密钥
export const createAPIKey = async (keyData) => {
  try {
    const response = await api.post('/api/v1/users/api-keys', keyData);
    return response.data;
  } catch (error) {
    console.error('创建API密钥失败:', error);
    throw error;
  }
};

// 删除API密钥
export const deleteAPIKey = async (keyId) => {
  try {
    const response = await api.delete(`/api/v1/users/api-keys/${keyId}`);
    return response.data;
  } catch (error) {
    console.error('删除API密钥失败:', error);
    throw error;
  }
};

// 获取使用统计
export const getUsageStats = async (params = {}) => {
  try {
    const response = await api.get('/api/v1/users/stats', { params });
    return response.data;
  } catch (error) {
    console.error('获取使用统计失败:', error);
    throw error;
  }
};

// 更新用户资料
export const updateUserProfile = async (profileData) => {
  try {
    const response = await api.put('/api/v1/users/profile', profileData);
    return response.data;
  } catch (error) {
    console.error('更新用户资料失败:', error);
    throw error;
  }
};

// 更改密码
export const changePassword = async (passwordData) => {
  try {
    const response = await api.put('/api/v1/users/password', passwordData);
    return response.data;
  } catch (error) {
    console.error('更改密码失败:', error);
    throw error;
  }
};
