import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './HomePage.css';

function HomePage() {
  const { user, isAuthenticated, loading: authLoading, logout, verifyToken } = useAuth();
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('dashboard');
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    const verifyTokenAndFetchUser = async () => {
      try {
        await verifyToken();
      } catch (error) {
        console.error('Token verification failed:', error);
      } finally {
        setLoading(false);
      }
    };

    verifyTokenAndFetchUser();
  }, [isAuthenticated, navigate]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const renderDashboard = () => (
    <div className="dashboard-section">
      <h2>系统概览</h2>
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">📰</div>
          <div className="stat-content">
            <h3>新闻总数</h3>
            <p>1,234</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">🔍</div>
          <div className="stat-content">
            <h3>今日查询</h3>
            <p>56</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">🤖</div>
          <div className="stat-content">
            <h3>AI回答</h3>
            <p>42</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">📊</div>
          <div className="stat-content">
            <h3>分析报告</h3>
            <p>12</p>
          </div>
        </div>
      </div>
    </div>
  );

  const renderNewsManagement = () => (
    <div className="news-management-section">
      <h2>新闻管理</h2>
      <div className="news-controls">
        <button className="btn btn-primary">获取新闻</button>
        <button className="btn btn-secondary">批量导入</button>
        <button className="btn btn-secondary">分类管理</button>
      </div>
      <div className="news-list">
        <div className="news-item">
          <div className="news-title">人工智能技术在新闻行业的应用</div>
          <div className="news-meta">
            <span>科技日报</span>
            <span>2023-10-01</span>
            <span>AI</span>
          </div>
        </div>
        <div className="news-item">
          <div className="news-title">全球气候变化最新研究进展</div>
          <div className="news-meta">
            <span>环球科学</span>
            <span>2023-10-02</span>
            <span>环境</span>
          </div>
        </div>
      </div>
    </div>
  );

  const renderIntelligentQuery = () => (
    <div className="query-section">
      <h2>智能查询</h2>
      <div className="query-container">
        <div className="query-input">
          <input 
            type="text" 
            placeholder="输入您的问题..." 
            className="query-field"
          />
          <button className="btn btn-primary">查询</button>
        </div>
        <div className="query-options">
          <label>
            <input type="checkbox" /> 语义搜索
          </label>
          <label>
            <input type="checkbox" /> 关键词搜索
          </label>
          <label>
            <input type="checkbox" /> 日期范围
          </label>
        </div>
        <div className="query-results">
          <h3>查询结果</h3>
          <div className="result-item">
            <h4>人工智能技术在新闻行业的应用</h4>
            <p>人工智能技术正在改变新闻行业的生产方式...</p>
            <div className="result-meta">
              <span>相似度: 95%</span>
              <span>来源: 科技日报</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

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
            className={`nav-item ${activeTab === 'dashboard' ? 'active' : ''}`}
            onClick={() => setActiveTab('dashboard')}
          >
            系统概览
          </button>
          <button 
            className={`nav-item ${activeTab === 'news' ? 'active' : ''}`}
            onClick={() => setActiveTab('news')}
          >
            新闻管理
          </button>
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
        </nav>
        
        <main className="home-content">
          {activeTab === 'dashboard' && renderDashboard()}
          {activeTab === 'news' && renderNewsManagement()}
          {activeTab === 'query' && renderIntelligentQuery()}
          {activeTab === 'analysis' && renderAnalysisReports()}
          {activeTab === 'settings' && renderUserSettings()}
        </main>
      </div>
    </div>
  );
}

export default HomePage;
