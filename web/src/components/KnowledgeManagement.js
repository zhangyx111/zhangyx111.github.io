import React, { useState, useEffect } from 'react';
import knowledgeService from '../services/knowledgeService';
import KnowledgeItem from './KnowledgeItem';
import './KnowledgeManagement.css'; // 假设我们会创建这个CSS文件

function KnowledgeManagement() {
  const [knowledgeItems, setKnowledgeItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    fetchKnowledgeItems();
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
      // 只发送文件，不发送额外的表单数据
      const response = await knowledgeService.uploadFile(selectedFile);
      if (response.data.success) {
        alert('文件添加成功');
        
        // 创建新文件对象并直接添加到列表中
        const newItem = {
          id: Date.now().toString(), // 临时ID，后端应该返回真实的ID
          name: selectedFile.name,
          is_activate: true, // 默认激活状态
          file_type: 'text', // 默认文件类型
          created_at: new Date().toISOString() // 当前时间
        };
        
        // 将新项目添加到列表开头
        setKnowledgeItems(prevItems => [newItem, ...prevItems]);
        setSelectedFile(null);
        
        // 仍然调用fetchKnowledgeItems来获取完整列表并更新临时ID
        fetchKnowledgeItems();
      } else {
        alert('文件添加失败: ' + response.data.message);
      }
    } catch (error) {
      console.error('文件添加失败:', error);
      if (error.response && error.response.data && error.response.data.message) {
        alert('文件添加失败: ' + error.response.data.message);
      } else {
        alert('文件添加失败');
      }
    } finally {
      setUploading(false);
    }
  };

  const handleDeleteItem = async (id) => {
    if (window.confirm('确定要删除此条目吗？')) {
      const itemToDelete = knowledgeItems.find(item => item.id === id);
      if (!itemToDelete) {
        alert('未找到要删除的条目');
        return;
      }

      // 直接从前端状态中删除
      setKnowledgeItems(prevItems => prevItems.filter(item => item.id !== id));

      try {
        const response = await knowledgeService.deleteKnowledgeItem(itemToDelete.name);
        if (response.data.success) {
          alert('删除成功');
        } else {
          // 如果后端删除失败，回滚前端状态
          setKnowledgeItems(prevItems => [...prevItems, itemToDelete]);
          alert('删除失败: ' + response.data.message);
        }
      } catch (error) {
        console.error('删除失败:', error);
        // 如果后端删除失败，回滚前端状态
        setKnowledgeItems(prevItems => [...prevItems, itemToDelete]);
        alert('删除失败');
      }
    }
  };

  const handleToggleActivate = async (id) => {
    try {
      // 获取当前知识库项
      const currentItems = [...knowledgeItems];
      const itemIndex = currentItems.findIndex(item => item.id === id);
      if (itemIndex === -1) return;

      const currentItem = currentItems[itemIndex];
      const newActivateStatus = !currentItem.is_activate;

      // 更新本地状态以立即反映更改
      currentItems[itemIndex] = { ...currentItem, is_activate: newActivateStatus };
      setKnowledgeItems(currentItems);

      // 调用API更新后端
      const response = await knowledgeService.updateKnowledgeItem(id, { 
        is_activate: newActivateStatus 
      });
      
      if (!response.data.success) {
        // 如果API更新失败，回滚本地状态
        currentItems[itemIndex] = { ...currentItem, is_activate: !newActivateStatus };
        setKnowledgeItems(currentItems);
        alert('更新状态失败: ' + response.data.message);
      }
    } catch (error) {
      console.error('更新状态失败:', error);
      // 发生错误时，重新获取数据以确保状态正确
      fetchKnowledgeItems();
      alert('更新状态失败');
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


      {/* 知识库列表 */}
      <div className="knowledge-list">
        <h3>知识库列表</h3>
        {loading ? (
          <div className="loading">加载中...</div>
        ) : (
          <div className="items-grid">
            {knowledgeItems.map(item => (
              <KnowledgeItem 
                key={item.id} 
                item={item} 
                onToggleActivate={handleToggleActivate}
                onDelete={handleDeleteItem}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default KnowledgeManagement;
