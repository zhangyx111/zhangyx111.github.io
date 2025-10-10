import React, { useState, useEffect } from 'react';
import knowledgeService from '../services/knowledgeService';
import './KnowledgeManagement.css'; // 假设我们会创建这个CSS文件

function KnowledgeManagement() {
  const [knowledgeItems, setKnowledgeItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [tags, setTags] = useState([]);
  const [newTagName, setNewTagName] = useState('');

  useEffect(() => {
    fetchKnowledgeItems();
    fetchTags();
  }, []);

  const fetchKnowledgeItems = async () => {
    try {
      setLoading(true);
      const response = await knowledgeService.getKnowledgeItems();
      if (response.data.success) {
        setKnowledgeItems(response.data.data.items);
      }
    } catch (error) {
      console.error('获取知识库列表失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchTags = async () => {
    try {
      const response = await knowledgeService.getTags();
      if (response.data.success) {
        setTags(response.data.data);
      }
    } catch (error) {
      console.error('获取标签列表失败:', error);
    }
  };

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleAddLocalFile = async () => {
    if (!selectedFile) {
      alert('请选择文件');
      return;
    }

    setUploading(true);
    try {
      const formData = {
        title: selectedFile.name,
        content: '',
        summary: '',
        category: '本地文件',
        tags: []
      };

      const response = await knowledgeService.uploadFile(selectedFile, formData);
      if (response.data.success) {
        alert('文件添加成功');
        setSelectedFile(null);
        fetchKnowledgeItems();
      } else {
        alert('文件添加失败: ' + response.data.message);
      }
    } catch (error) {
      console.error('文件添加失败:', error);
      alert('文件添加失败');
    } finally {
      setUploading(false);
    }
  };

  const handleDeleteItem = async (id) => {
    if (window.confirm('确定要删除此条目吗？')) {
      try {
        const response = await knowledgeService.deleteKnowledgeItem(id);
        if (response.data.success) {
          alert('删除成功');
          fetchKnowledgeItems();
        } else {
          alert('删除失败: ' + response.data.message);
        }
      } catch (error) {
        console.error('删除失败:', error);
        alert('删除失败');
      }
    }
  };

  const handleCreateTag = async () => {
    if (!newTagName.trim()) {
      alert('请输入标签名称');
      return;
    }

    try {
      const response = await knowledgeService.createTag({ name: newTagName });
      if (response.data.success) {
        alert('标签创建成功');
        setNewTagName('');
        fetchTags();
      } else {
        alert('标签创建失败: ' + response.data.message);
      }
    } catch (error) {
      console.error('标签创建失败:', error);
      alert('标签创建失败');
    }
  };

  return (
    <div className="knowledge-management-section">
      <h2>知识库管理</h2>
      
      {/* 文件上传区域 */}
      <div className="file-upload-area">
        <h3>添加文件到知识库</h3>
        <div className="upload-controls">
          <input 
            type="file" 
            onChange={handleFileChange} 
            className="file-input"
            accept=".txt,.pdf,.doc,.docx,.md"
          />
          <button 
            onClick={handleAddLocalFile} 
            disabled={uploading || !selectedFile}
            className="btn btn-primary"
          >
            {uploading ? '上传中...' : '添加到知识库'}
          </button>
        </div>
      </div>

      {/* 标签管理 */}
      <div className="tag-management">
        <h3>标签管理</h3>
        <div className="tag-controls">
          <input
            type="text"
            value={newTagName}
            onChange={(e) => setNewTagName(e.target.value)}
            placeholder="新标签名称"
            className="tag-input"
          />
          <button onClick={handleCreateTag} className="btn btn-secondary">
            创建标签
          </button>
        </div>
        <div className="tag-list">
          {tags.map(tag => (
            <span key={tag.id} className="tag-item">
              {tag.name}
              <span className="tag-color" style={{ backgroundColor: tag.color }}></span>
            </span>
          ))}
        </div>
      </div>

      {/* 知识库列表 */}
      <div className="knowledge-list">
        <h3>知识库列表</h3>
        {loading ? (
          <div className="loading">加载中...</div>
        ) : (
          <div className="items-grid">
            {knowledgeItems.map(item => (
              <div key={item.id} className="knowledge-item">
                <div className="item-header">
                  <h4>{item.title}</h4>
                  <button 
                    onClick={() => handleDeleteItem(item.id)}
                    className="btn btn-danger btn-sm"
                  >
                    删除
                  </button>
                </div>
                <div className="item-meta">
                  <span>类型: {item.file_type || 'text'}</span>
                  <span>大小: {item.file_size ? (item.file_size / 1024).toFixed(2) + ' KB' : 'N/A'}</span>
                  <span>创建时间: {new Date(item.created_at).toLocaleDateString()}</span>
                </div>
                <div className="item-tags">
                  {item.tags.map(tag => (
                    <span key={tag.id} className="tag-item">
                      {tag.name}
                    </span>
                  ))}
                </div>
                {item.summary && (
                  <div className="item-summary">
                    <p>{item.summary}</p>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default KnowledgeManagement;
