import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import knowledgeService from '../services/knowledgeService';
import KnowledgeManagement from '../components/KnowledgeManagement';
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

  const renderIntelligentQuery = () => {
    const [query, setQuery] = useState('');
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState([]);
    const [searchType, setSearchType] = useState('semantic');
    const [topK, setTopK] = useState(5);
    const [error, setError] = useState(null);

    const handleSearch = async () => {
      if (!query.trim()) {
        setError('请输入查询内容');
        return;
      }

      setLoading(true);
      setError(null);
      setResults([]);

      try {
        const response = await fetch('/api/llm_service/search', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify({
            query: query.trim(),
            top_k: topK
          })
        });

        const data = await response.json();

        if (data.success) {
          setResults(data.data.results);
        } else {
          setError(data.message || '查询失败');
        }
      } catch (err) {
        console.error('查询失败:', err);
        setError('网络错误，请稍后重试');
      } finally {
        setLoading(false);
      }
    };

    const handleKeyPress = (e) => {
      if (e.key === 'Enter') {
        handleSearch();
      }
    };

    return (
      <div className="query-section">
        <h2>智能查询</h2>
        <div className="query-container">
          <div className="query-input">
            <input 
              type="text" 
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="输入您的问题..." 
              className="query-field"
              disabled={loading}
            />
            <button 
              onClick={handleSearch} 
              disabled={loading || !query.trim()}
              className="btn btn-primary"
            >
              {loading ? '查询中...' : '查询'}
            </button>
          </div>
          
          <div className="query-options">
            <div className="option-group">
              <label>搜索类型:</label>
              <select 
                value={searchType}
                onChange={(e) => setSearchType(e.target.value)}
                className="select-input"
              >
                <option value="semantic">语义搜索</option>
                <option value="keyword">关键词搜索</option>
                <option value="hybrid">混合搜索</option>
              </select>
            </div>
            
            <div className="option-group">
              <label>返回结果数:</label>
              <select 
                value={topK}
                onChange={(e) => setTopK(parseInt(e.target.value))}
                className="select-input"
              >
                <option value="3">3</option>
                <option value="5">5</option>
                <option value="10">10</option>
                <option value="20">20</option>
              </select>
            </div>
          </div>

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          <div className="query-results">
            <h3>查询结果 ({results.length})</h3>
            {results.length === 0 && !loading && !error && (
              <div className="no-results">
                请输入查询内容并点击查询按钮
              </div>
            )}
            {results.map((result) => (
              <div key={result.id} className="result-item">
                <h4>结果 #{result.id}</h4>
                <div className="result-content">
                  <p>{result.content}</p>
                </div>
                {result.metadata && Object.keys(result.metadata).length > 0 && (
                  <div className="result-metadata">
                    {Object.entries(result.metadata).map(([key, value]) => (
                      <span key={key} className="meta-item">
                        <strong>{key}:</strong> {String(value)}
                      </span>
                    ))}
                  </div>
                )}
                <div className="result-meta">
                  <span className="similarity">相似度: {(result.similarity * 100).toFixed(1)}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
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
          <button 
            className={`nav-item ${activeTab === 'knowledge' ? 'active' : ''}`}
            onClick={() => setActiveTab('knowledge')}
          >
            知识库
          </button>
        </nav>
        
        <main className="home-content">
          {activeTab === 'dashboard' && renderDashboard()}
          {activeTab === 'news' && renderNewsManagement()}
          {activeTab === 'query' && renderIntelligentQuery()}
          {activeTab === 'analysis' && renderAnalysisReports()}
          {activeTab === 'settings' && renderUserSettings()}
          {activeTab === 'knowledge' && <KnowledgeManagement />}
        </main>
      </div>
    </div>
  );
}

export default HomePage;
