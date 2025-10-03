import api from './authService';

// 获取关键词分析
export const getKeywordAnalysis = async (params = {}) => {
  try {
    const response = await api.get('/api/v1/analysis/keywords', { params });
    return response.data;
  } catch (error) {
    console.error('获取关键词分析失败:', error);
    throw error;
  }
};

// 获取聚类分析
export const getClusterAnalysis = async (params = {}) => {
  try {
    const response = await api.get('/api/v1/analysis/clusters', { params });
    return response.data;
  } catch (error) {
    console.error('获取聚类分析失败:', error);
    throw error;
  }
};

// 获取趋势分析
export const getTrendAnalysis = async (params = {}) => {
  try {
    const response = await api.get('/api/v1/analysis/trends', { params });
    return response.data;
  } catch (error) {
    console.error('获取趋势分析失败:', error);
    throw error;
  }
};

// 获取情感分析
export const getSentimentAnalysis = async (params = {}) => {
  try {
    const response = await api.get('/api/v1/analysis/sentiment', { params });
    return response.data;
  } catch (error) {
    console.error('获取情感分析失败:', error);
    throw error;
  }
};

// 生成分析报告
export const generateAnalysisReport = async (reportConfig) => {
  try {
    const response = await api.post('/api/v1/analysis/generate', reportConfig);
    return response.data;
  } catch (error) {
    console.error('生成分析报告失败:', error);
    throw error;
  }
};

// 获取报告列表
export const getReportList = async (params = {}) => {
  try {
    const response = await api.get('/api/v1/analysis/reports', { params });
    return response.data;
  } catch (error) {
    console.error('获取报告列表失败:', error);
    throw error;
  }
};

// 获取报告详情
export const getReportDetail = async (reportId) => {
  try {
    const response = await api.get(`/api/v1/analysis/reports/${reportId}`);
    return response.data;
  } catch (error) {
    console.error('获取报告详情失败:', error);
    throw error;
  }
};

// 删除报告
export const deleteReport = async (reportId) => {
  try {
    const response = await api.delete(`/api/v1/analysis/reports/${reportId}`);
    return response.data;
  } catch (error) {
    console.error('删除报告失败:', error);
    throw error;
  }
};

// 导出报告
export const exportReport = async (reportId, format) => {
  try {
    const response = await api.post(`/api/v1/analysis/reports/${reportId}/export`, { format }, {
      responseType: 'blob'
    });
    return response.data;
  } catch (error) {
    console.error('导出报告失败:', error);
    throw error;
  }
};

// 获取数据统计
export const getDataStats = async (params = {}) => {
  try {
    const response = await api.get('/api/v1/analysis/stats', { params });
    return response.data;
  } catch (error) {
    console.error('获取数据统计失败:', error);
    throw error;
  }
};

// 获取来源分析
export const getSourceAnalysis = async (params = {}) => {
  try {
    const response = await api.get('/api/v1/analysis/sources', { params });
    return response.data;
  } catch (error) {
    console.error('获取来源分析失败:', error);
    throw error;
  }
};

// 获取分类分析
export const getCategoryAnalysis = async (params = {}) => {
  try {
    const response = await api.get('/api/v1/analysis/categories', { params });
    return response.data;
  } catch (error) {
    console.error('获取分类分析失败:', error);
    throw error;
  }
};

// 获取时间线分析
export const getTimelineAnalysis = async (params = {}) => {
  try {
    const response = await api.get('/api/v1/analysis/timeline', { params });
    return response.data;
  } catch (error) {
    console.error('获取时间线分析失败:', error);
    throw error;
  }
};

// 获取热点话题
export const getHotTopics = async (params = {}) => {
  try {
    const response = await api.get('/api/v1/analysis/hot-topics', { params });
    return response.data;
  } catch (error) {
    console.error('获取热点话题失败:', error);
    throw error;
  }
};

// 获取实体分析
export const getEntityAnalysis = async (params = {}) => {
  try {
    const response = await api.get('/api/v1/analysis/entities', { params });
    return response.data;
  } catch (error) {
    console.error('获取实体分析失败:', error);
    throw error;
  }
};
