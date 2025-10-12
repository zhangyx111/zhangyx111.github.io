import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import knowledgeService from '../services/knowledgeService';
import KnowledgeManagement from '../components/KnowledgeManagement';
import IntelligentQuery from '../components/IntelligentQuery';
import './HomePage.css';

function HomePage() {
  const { user, isAuthenticated, loading: authLoading, logout } = useAuth();
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('query');
  const navigate = useNavigate();

  useEffect(() => {
    // 不需要在这里验证token，因为ProtectedRoute已经确保用户已认证
    // 只需要设置loading状态
    setLoading(false);
  }, [isAuthenticated]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };



  const renderAnalysisReports = () => (
    <div className="analysis-section">
      <h2>分析报告</h2>
      <div className="report-controls">
        <button className="btn btn-primary">生成报告</button>
        <button className="btn btn-secondary">关键词分析</button>
        <button className="btn btn-secondary">聚类分析</button>
      </div>
      <div className="report-list">
        <div className="report-item">
          <div className="report-title">本周热门话题分析</div>
          <div className="report-meta">
            <span>生成时间: 2023-10-03</span>
            <span>类型: 关键词分析</span>
          </div>
        </div>
        <div className="report-item">
          <div className="report-title">新闻主题聚类报告</div>
          <div className="report-meta">
            <span>生成时间: 2023-10-02</span>
            <span>类型: 聚类分析</span>
          </div>
        </div>
      </div>
    </div>
  );

  const renderUserSettings = () => (
    <div className="settings-section">
      <h2>用户设置</h2>
      <div className="settings-form">
        <div className="form-group">
          <label>用户名</label>
          <input type="text" value={user?.username || ''} readOnly />
        </div>
        <div className="form-group">
          <label>邮箱</label>
          <input type="email" value={user?.email || ''} readOnly />
        </div>
        <div className="form-group">
          <label>通知设置</label>
          <div className="checkbox-group">
            <label>
              <input type="checkbox" /> 邮件通知
            </label>
            <label>
              <input type="checkbox" /> 系统通知
            </label>
          </div>
        </div>
        <div className="form-group">
          <label>查询偏好</label>
          <select>
            <option>语义优先</option>
            <option>关键词优先</option>
            <option>混合模式</option>
          </select>
        </div>
        <button className="btn btn-primary">保存设置</button>
      </div>
    </div>
  );


  if (loading || authLoading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="home-page">
      <div className="home-container">
        <header className="home-header">
          <div className="logo">
            <h1>XU-News-AI-RAG</h1>
            <p>智能新闻检索与问答系统</p>
          </div>
          <div className="header-actions">
            {user && (
              <div className="user-info">
                <span>欢迎, {user.username}!</span>
                <button onClick={handleLogout} className="btn btn-secondary">
                  退出
                </button>
              </div>
            )}
          </div>
        </header>
        
        <nav className="main-nav">
          <button 
            className={`nav-item ${activeTab === 'query' ? 'active' : ''}`}
            onClick={() => setActiveTab('query')}
          >
            智能查询
          </button>
          <button 
            className={`nav-item ${activeTab === 'analysis' ? 'active' : ''}`}
            onClick={() => setActiveTab('analysis')}
          >
            分析报告
          </button>
          <button 
            className={`nav-item ${activeTab === 'settings' ? 'active' : ''}`}
            onClick={() => setActiveTab('settings')}
          >
            用户设置
          </button>
          <button 
            className={`nav-item ${activeTab === 'knowledge' ? 'active' : ''}`}
            onClick={() => setActiveTab('knowledge')}
          >
            知识库
          </button>
        </nav>
        
        <main className="home-content">
          {activeTab === 'query' && <IntelligentQuery />}
          {activeTab === 'analysis' && renderAnalysisReports()}
          {activeTab === 'settings' && renderUserSettings()}
          {activeTab === 'knowledge' && <KnowledgeManagement />}
        </main>
      </div>
    </div>
  );
}

export default HomePage;
