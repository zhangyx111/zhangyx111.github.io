import React, { useState } from 'react';
import QueryResult from './QueryResult';
import api from '../services/authService';

const IntelligentQuery = () => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
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
      const params = new URLSearchParams({
        query: query.trim()
      });
      const response = await api.get(`/api/llm_service/search?${params.toString()}`);

      const data = response.data;
      console.log(typeof data)

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
            <QueryResult key={result.id} result={result} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default IntelligentQuery;
