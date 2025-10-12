import React from 'react';
import './KnowledgeManagement.css'; // 复用KnowledgeManagement的样式

function KnowledgeItem({ item, onToggleActivate, onDelete }) {
  return (
    <div className="knowledge-item full-width">
      <div className="item-header">
        <h4>{item.name}</h4>
        <div className="item-actions">
          <div className="switch-container">
            <span className="switch-label">{item.is_activate ? '已激活' : '已停用'}</span>
            <label className="switch">
              <input 
                type="checkbox" 
                checked={item.is_activate}
                onChange={() => onToggleActivate(item.id)}
              />
              <span className="slider round"></span>
            </label>
          </div>
          <button 
            onClick={() => onDelete(item.id)}
            className="btn btn-danger btn-sm"
          >
            删除
          </button>
        </div>
      </div>
    </div>
  );
}

export default KnowledgeItem;
