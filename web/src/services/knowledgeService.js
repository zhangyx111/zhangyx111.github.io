import api from './authService';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

class KnowledgeService {
  // 获取知识库列表
  getKnowledgeItems(params = {}) {
    return api.get(`${API_URL}/knowledge/`, { params });
  }

  // 创建知识库条目
  createKnowledgeItem(data) {
    return api.post(`${API_URL}/knowledge`, data);
  }

  // 更新知识库条目
  updateKnowledgeItem(id, data) {
    return api.put(`${API_URL}/knowledge/${id}`, data);
  }

  // 删除知识库条目
  deleteKnowledgeItem(name) {
    return api.delete(`${API_URL}/knowledge/${name}`);
  }

  // 批量删除知识库条目
  batchDeleteKnowledgeItems(ids) {
    return api.delete(`${API_URL}/knowledge/batch`, { data: { ids } });
  }

  // 上传文件到知识库
  uploadFile(file, data = {}) {
    const form = new FormData();
    form.append('file', file);

    // 如果有额外的数据，添加到FormData中
    Object.entries(data).forEach(([key, value]) => {
      form.append(key, value);
    });

    // 不需要手动设置Content-Type，axios会自动处理FormData
    return api.post(`${API_URL}/knowledge/upload`, form);
  }

  // 下载知识库文件
  downloadFile(id) {
    return api.get(`${API_URL}/knowledge/download/${id}`, {
      responseType: 'blob'
    });
  }

  // 添加本地文件到知识库
  addLocalFile(filePath, fileName, options = {}) {
    return api.post(`${API_URL}/knowledge/local-file`, {
      filePath,
      fileName,
      ...options
    });
  }
}

export default new KnowledgeService();
