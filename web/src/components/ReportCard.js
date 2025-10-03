import React from 'react';
import './ReportCard.css';

const ReportCard = ({ report, onClick }) => {
  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleDateString('zh-CN', options);
  };

  const getReportTypeIcon = (type) => {
    switch (type.toLowerCase()) {
      case '关键词分析':
        return '📊';
      case '聚类分析':
        return '🔍';
      case '趋势分析':
        return '📈';
      case '情感分析':
        return '😊';
      default:
        return '📄';
    }
  };

  return (
    <div className="report-card" onClick={onClick}>
      <div className="report-header">
        <div className="report-icon">
          {getReportTypeIcon(report.type)}
        </div>
        <div className="report-title-container">
          <h3 className="report-title">{report.title}</h3>
          <span className="report-type">{report.type}</span>
        </div>
      </div>
      
      <div className="report-meta">
        <span className="report-date">生成时间: {formatDate(report.created_at)}</span>
        <span className="report-status">{report.status || '已完成'}</span>
      </div>
      
      {report.summary && (
        <div className="report-summary">
          <p>{report.summary}</p>
        </div>
      )}
      
      <div className="report-footer">
        <div className="report-stats">
          {report.stats && (
            <>
              <span className="stat-item">
                <span className="stat-label">数据量:</span>
                <span className="stat-value">{report.stats.data_count || 'N/A'}</span>
              </span>
              <span className="stat-item">
                <span className="stat-label">处理时间:</span>
                <span className="stat-value">{report.stats.processing_time || 'N/A'}</span>
              </span>
            </>
          )}
        </div>
        <button className="report-view-btn">
          查看详情
        </button>
      </div>
    </div>
  );
};

export default ReportCard;
