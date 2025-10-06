import api from './authService';

// 获取新闻总数
export const getNewsCount = async () => {
  try {
    const response = await api.get('/api/news/count');
    return response.data;
  } catch (error) {
    console.error('获取新闻总数失败:', error);
    throw error;
  }
};

// 获取新闻列表
export const getNewsList = async (params = {}) => {
  try {
    const response = await api.get('/api/v1/news', { params });
    return response.data;
  } catch (error) {
    console.error('获取新闻列表失败:', error);
    throw error;
  }
};

// 获取单个新闻详情
export const getNewsDetail = async (newsId) => {
  try {
    const response = await api.get(`/api/v1/news/${newsId}`);
    return response.data;
  } catch (error) {
    console.error('获取新闻详情失败:', error);
    throw error;
  }
};

// 创建新闻
export const createNews = async (newsData) => {
  try {
    const response = await api.post('/api/v1/news', newsData);
    return response.data;
  } catch (error) {
    console.error('创建新闻失败:', error);
    throw error;
  }
};

// 更新新闻
export const updateNews = async (newsId, newsData) => {
  try {
    const response = await api.put(`/api/v1/news/${newsId}`, newsData);
    return response.data;
  } catch (error) {
    console.error('更新新闻失败:', error);
    throw error;
  }
};

// 删除新闻
export const deleteNews = async (newsId) => {
  try {
    const response = await api.delete(`/api/v1/news/${newsId}`);
    return response.data;
  } catch (error) {
    console.error('删除新闻失败:', error);
    throw error;
  }
};

// 批量删除新闻
export const batchDeleteNews = async (newsIds) => {
  try {
    const response = await api.post('/api/v1/news/batch-delete', { news_ids: newsIds });
    return response.data;
  } catch (error) {
    console.error('批量删除新闻失败:', error);
    throw error;
  }
};

// 获取新闻分类
export const getNewsCategories = async () => {
  try {
    const response = await api.get('/api/v1/news/categories');
    return response.data;
  } catch (error) {
    console.error('获取新闻分类失败:', error);
    throw error;
  }
};

// 获取新闻标签
export const getNewsTags = async () => {
  try {
    const response = await api.get('/api/v1/news/tags');
    return response.data;
  } catch (error) {
    console.error('获取新闻标签失败:', error);
    throw error;
  }
};

// 获取RSS源列表
export const getRSSSources = async () => {
  try {
    const response = await api.get('/api/v1/rss/sources');
    return response.data;
  } catch (error) {
    console.error('获取RSS源失败:', error);
    throw error;
  }
};

// 添加RSS源
export const addRSSSource = async (sourceData) => {
  try {
    const response = await api.post('/api/v1/rss/sources', sourceData);
    return response.data;
  } catch (error) {
    console.error('添加RSS源失败:', error);
    throw error;
  }
};

// 删除RSS源
export const deleteRSSSource = async (sourceId) => {
  try {
    const response = await api.delete(`/api/v1/rss/sources/${sourceId}`);
    return response.data;
  } catch (error) {
    console.error('删除RSS源失败:', error);
    throw error;
  }
};

// 手动获取新闻
export const fetchNewsManually = async (sourceIds = []) => {
  try {
    const response = await api.post('/api/v1/news/fetch', { source_ids: sourceIds });
    return response.data;
  } catch (error) {
    console.error('手动获取新闻失败:', error);
    throw error;
  }
};

// 搜索新闻
export const searchNews = async (query, filters = {}) => {
  try {
    const response = await api.post('/api/v1/news/search', { query, filters });
    return response.data;
  } catch (error) {
    console.error('搜索新闻失败:', error);
    throw error;
  }
};

// 导出新闻
export const exportNews = async (format, filters = {}) => {
  try {
    const response = await api.post('/api/v1/news/export', { format, filters }, {
      responseType: 'blob'
    });
    return response.data;
  } catch (error) {
    console.error('导出新闻失败:', error);
    throw error;
  }
};
