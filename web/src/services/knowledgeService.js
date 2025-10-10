import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

class KnowledgeService {
  // 获取知识库列表
  getKnowledgeItems(params = {}) {
    return axios.get(`${API_URL}/knowledge`, { params });
  }

  // 创建知识库条目
  createKnowledgeItem(data) {
    return axios.post(`${API_URL}/knowledge`, data);
  }

  // 更新知识库条目
  updateKnowledgeItem(id, data) {
    return axios.put(`${API_URL}/knowledge/${id}`, data);
  }

  // 删除知识库条目
  deleteKnowledgeItem(id) {
    return axios.delete(`${API_URL}/knowledge/${id}`);
  }

  // 批量删除知识库条目
  batchDeleteKnowledgeItems(ids) {
    return axios.delete(`${API_URL}/knowledge/batch`, { data: { ids } });
  }

  // 上传文件到知识库
  uploadFile(file, formData) {
    const form = new FormData();
    form.append('file', file);
    
    // 添加其他表单字段
    Object.keys(formData).forEach(key => {
      form.append(key, formData[key]);
    });

    return axios.post(`${API_URL}/knowledge/upload`, form, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  }

  // 下载知识库文件
  downloadFile(id) {
    return axios.get(`${API_URL}/knowledge/download/${id}`, {
      responseType: 'blob'
    });
  }

  // 获取标签列表
  getTags() {
    return axios.get(`${API_URL}/knowledge/tags`);
  }

  // 创建标签
  createTag(data) {
    return axios.post(`${API_URL}/knowledge/tags`, data);
  }

  // 更新标签
  updateTag(id, data) {
    return axios.put(`${API_URL}/knowledge/tags/${id}`, data);
  }

  // 删除标签
  deleteTag(id) {
    return axios.delete(`${API_URL}/knowledge/tags/${id}`);
  }

  // 添加本地文件到知识库
  addLocalFile(filePath, fileName, options = {}) {
    return axios.post(`${API_URL}/knowledge/local-file`, {
      filePath,
      fileName,
      ...options
    });
  }
}

export default new KnowledgeService();
