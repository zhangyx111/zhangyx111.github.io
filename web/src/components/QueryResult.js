import React from 'react';
import './QueryResult.css';

const QueryResult = ({ result, index }) => {
  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('zh-CN', options);
  };

  const truncateContent = (content, maxLength = 200) => {
    if (content.length <= maxLength) return content;
    return content.substring(0, maxLength) + '...';
  };

  return (
    <div className="query-result">
      <div className="result-header">
        <span className="result-rank">#{index + 1}</span>
        <div className="result-score">
          <span className="similarity-score">
            相似度: {(result.similarity * 100).toFixed(1)}%
          </span>
        </div>
      </div>
      
      <div className="result-content">
        <h3 className="result-title">{result.title}</h3>
        <p className="result-summary">{truncateContent(result.content)}</p>
        
        <div className="result-meta">
          <span className="result-source">{result.source}</span>
          <span className="result-date">{formatDate(result.publish_date)}</span>
          {result.category && (
            <span className="result-category">{result.category}</span>
          )}
        </div>
        
        {result.tags && result.tags.length > 0 && (
          <div className="result-tags">
            {result.tags.map((tag, tagIndex) => (
              <span key={tagIndex} className="result-tag">
                {tag}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default QueryResult;
