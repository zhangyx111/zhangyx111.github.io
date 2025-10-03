import api from './authService';

// 语义查询
export const semanticSearch = async (query, options = {}) => {
  try {
    const response = await api.post('/api/v1/query/semantic', {
      query,
      top_k: options.top_k || 10,
      filters: options.filters || {}
    });
    return response.data;
  } catch (error) {
    console.error('语义查询失败:', error);
    throw error;
  }
};

// 关键词查询
export const keywordSearch = async (query, options = {}) => {
  try {
    const response = await api.post('/api/v1/query/keyword', {
      query,
      top_k: options.top_k || 10,
      filters: options.filters || {}
    });
    return response.data;
  } catch (error) {
    console.error('关键词查询失败:', error);
    throw error;
  }
};

// 混合查询
export const hybridSearch = async (query, options = {}) => {
  try {
    const response = await api.post('/api/v1/query/hybrid', {
      query,
      top_k: options.top_k || 10,
      filters: options.filters || {},
      semantic_weight: options.semantic_weight || 0.7,
      keyword_weight: options.keyword_weight || 0.3
    });
    return response.data;
  } catch (error) {
    console.error('混合查询失败:', error);
    throw error;
  }
};

// 智能问答
export const intelligentQA = async (question, context = '') => {
  try {
    const response = await api.post('/api/v1/query/chat', {
      question,
      context: context || ''
    });
    return response.data;
  } catch (error) {
    console.error('智能问答失败:', error);
    throw error;
  }
};

// 获取查询历史
export const getQueryHistory = async (params = {}) => {
  try {
    const response = await api.get('/api/v1/query/history', { params });
    return response.data;
  } catch (error) {
    console.error('获取查询历史失败:', error);
    throw error;
  }
};

// 保存查询
export const saveQuery = async (queryData) => {
  try {
    const response = await api.post('/api/v1/query/save', queryData);
    return response.data;
  } catch (error) {
    console.error('保存查询失败:', error);
    throw error;
  }
};

// 获取热门查询
export const getPopularQueries = async (limit = 10) => {
  try {
    const response = await api.get('/api/v1/query/popular', { params: { limit } });
    return response.data;
  } catch (error) {
    console.error('获取热门查询失败:', error);
    throw error;
  }
};

// 获取查询建议
export const getQuerySuggestions = async (partialQuery) => {
  try {
    const response = await api.get('/api/v1/query/suggestions', { 
      params: { query: partialQuery } 
    });
    return response.data;
  } catch (error) {
    console.error('获取查询建议失败:', error);
    throw error;
  }
};

// 联网查询
export const webSearch = async (query, options = {}) => {
  try {
    const response = await api.post('/api/v1/query/web', {
      query,
      top_k: options.top_k || 10,
      time_range: options.time_range || 'all',
      language: options.language || 'zh'
    });
    return response.data;
  } catch (error) {
    console.error('联网查询失败:', error);
    throw error;
  }
};

// 获取查询分析
export const getQueryAnalysis = async (queryId) => {
  try {
    const response = await api.get(`/api/v1/query/analysis/${queryId}`);
    return response.data;
  } catch (error) {
    console.error('获取查询分析失败:', error);
    throw error;
  }
};

// 反馈查询结果
export const feedbackQuery = async (queryId, feedback) => {
  try {
    const response = await api.post(`/api/v1/query/feedback/${queryId}`, feedback);
    return response.data;
  } catch (error) {
    console.error('反馈查询结果失败:', error);
    throw error;
  }
};

// 获取查询统计
export const getQueryStats = async (params = {}) => {
  try {
    const response = await api.get('/api/v1/query/stats', { params });
    return response.data;
  } catch (error) {
    console.error('获取查询统计失败:', error);
    throw error;
  }
};
