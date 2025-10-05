import React from 'react';
import './NewsCard.css';

const NewsCard = ({ news, onClick }) => {
  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('zh-CN', options);
  };

  return (
    <div className="news-card" onClick={onClick}>
      <div className="news-content">
        <h3 className="news-title">{news.title}</h3>
        <p className="news-summary">{news.summary || news.content.substring(0, 150) + '...'}</p>
        <div className="news-meta">
          <span className="news-source">{news.source}</span>
          <span className="news-date">{formatDate(news.publish_date)}</span>
          {news.category && (
            <span className="news-category">{news.category}</span>
          )}
        </div>
        {news.tags && news.tags.length > 0 && (
          <div className="news-tags">
            {news.tags.map((tag, index) => (
              <span key={index} className="news-tag">
                {tag}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default NewsCard;
