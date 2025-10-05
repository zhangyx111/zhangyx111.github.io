# XU-News-AI-RAG 概要设计文档

## 1. 文档概述

### 1.1 文档目的
本文档基于产品需求文档（PRD），为XU-News-AI-RAG系统提供概要设计方案，指导开发团队进行系统架构设计和模块开发。

### 1.2 设计原则
- **模块化设计**：系统采用模块化架构，便于维护和扩展
- **高内聚低耦合**：各模块内部功能高度相关，模块间依赖关系最小化
- **可扩展性**：支持功能扩展和性能扩展
- **安全性**：确保数据安全和系统安全
- **用户体验**：提供友好的用户界面和交互体验

### 1.3 设计范围
- 系统架构设计
- 模块功能设计
- 数据库设计
- 接口设计
- 部署设计
- 安全和性能设计

## 2. 系统架构设计

### 2.1 总体架构
系统采用前后端分离的微服务架构，主要分为以下层次：

```
┌─────────────────────────────────────────────────────────────┐
│                        前端应用层                           │
│          (React/Vue.js + 响应式设计)                        │
├─────────────────────────────────────────────────────────────┤
│                        API网关层                           │
│           (路由转发、负载均衡、认证授权)                     │
├─────────────────────────────────────────────────────────────┤
│                        业务服务层                           │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐   │
│  │信息获取服务 │AI服务      │知识库服务  │用户管理服务 │   │
│  │             │             │             │             │   │
│  └─────────────┴─────────────┴─────────────┴─────────────┘   │
├─────────────────────────────────────────────────────────────┤
│                        数据存储层                           │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐   │
│  │关系型数据库 │向量数据库  │文件存储    │缓存系统    │   │
│  │(MySQL/SQLite)│(FAISS)     │(本地存储)  │(Redis)     │   │
│  └─────────────┴─────────────┴─────────────┴─────────────┘   │
├─────────────────────────────────────────────────────────────┤
│                        基础设施层                           │
│        (Ollama + 大语言模型 + 第三方服务)                   │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 技术栈选择

#### 2.2.1 前端技术栈
- **框架**：React 18+
- **状态管理**：Redux Toolkit 或 Pinia
- **UI组件库**：Ant Design 或 Element Plus
- **构建工具**：Vite 或 Webpack
- **样式方案**：Styled-components 或 CSS-in-JS

#### 2.2.2 后端技术栈
- **主框架**：Flask 3.1.2
- **业务逻辑**：LangChain
- **数据库ORM**：SQLAlchemy
- **API文档**：Swagger/OpenAPI 3.0
- **缓存**：Redis
- **消息队列**：RabbitMQ（可选）

#### 2.2.3 AI服务栈
- **模型部署**：Ollama
- **大语言模型**：qwen3::8b
- **嵌入模型**：all-MiniLM-L6-v2
- **重排模型**：ms-marco-MiniLM-L-6-v2
- **向量数据库**：FAISS

#### 2.2.4 数据存储栈
- **关系型数据库**：MySQL 8.0+ 
- **向量数据库**：FAISS
- **文件存储**：本地文件系统
- **搜索引擎**：Elasticsearch（可选）

## 3. 模块设计

### 3.1 核心模块划分

#### 3.1.1 信息获取模块
**功能描述**：负责从各种来源获取新闻信息
**主要组件**：
- RSS订阅管理器
- 网页爬虫引擎
- 数据清洗处理器
- 定时任务调度器

**接口设计**：
```python
class InformationFetcher:
    def fetch_rss_feeds(self, urls: List[str]) -> List[NewsItem]
    def scrape_web_pages(self, urls: List[str]) -> List[NewsItem]
    def clean_data(self, raw_data: List[NewsItem]) -> List[NewsItem]
    def schedule_tasks(self) -> None
```

#### 3.1.2 AI服务模块
**功能描述**：提供AI相关的服务，包括文本向量化、语义搜索、智能问答等
**主要组件**：
- 模型管理器
- 向量化服务
- 检索服务
- 问答服务

**接口设计**：
```python
class AIService:
    def embed_text(self, text: str) -> np.ndarray
    def search_similar(self, query: str, top_k: int = 10) -> List[SearchResult]
    def generate_answer(self, query: str, context: str) -> str
    def rerank_results(self, query: str, results: List[SearchResult]) -> List[SearchResult]
```

#### 3.1.3 知识库模块
**功能描述**：管理新闻数据的存储、检索和分析
**主要组件**：
- 数据存储管理器
- 向量索引管理器
- 数据分析引擎
- 报表生成器

**接口设计**：
```python
class KnowledgeBase:
    def store_news(self, news_item: NewsItem) -> bool
    def search_news(self, query: str, filters: Dict = None) -> List[NewsItem]
    def analyze_data(self, analysis_type: str) -> AnalysisResult
    def generate_report(self, report_type: str) -> Report
```

#### 3.1.4 用户管理模块
**功能描述**：处理用户认证、授权和权限管理
**主要组件**：
- 用户认证服务
- 权限管理服务
- 用户配置管理
- 会话管理

**接口设计**：
```python
class UserService:
    def authenticate(self, username: str, password: str) -> AuthToken
    def authorize(self, token: str, permission: str) -> bool
    def get_user_profile(self, user_id: str) -> UserProfile
    def update_user_settings(self, user_id: str, settings: Dict) -> bool
```

#### 3.1.5 内容管理模块
**功能描述**：管理新闻内容的增删改查操作
**主要组件**：
- 内容管理器
- 标签管理器
- 分类管理器
- 批量操作处理器

**接口设计**：
```python
class ContentManager:
    def create_news(self, news_data: Dict) -> NewsItem
    def update_news(self, news_id: str, news_data: Dict) -> NewsItem
    def delete_news(self, news_id: str) -> bool
    def batch_delete_news(self, news_ids: List[str]) -> bool
    def manage_tags(self, tags: List[str]) -> List[Tag]
```

#### 3.1.6 智能查询模块
**功能描述**：提供智能搜索和问答功能
**主要组件**：
- 查询处理器
- 语义搜索引擎
- 联网查询服务
- 结果排序器

**接口设计**：
```python
class IntelligentQuery:
    def process_query(self, query: str) -> QueryResult
    def semantic_search(self, query: str) -> List[SearchResult]
    def web_search(self, query: str) -> List[WebResult]
    def generate_response(self, query: str, context: str) -> str
```

#### 3.1.7 通知模块
**功能描述**：处理系统通知和邮件发送
**主要组件**：
- 邮件服务
- 通知管理器
- 模板引擎
- 发送调度器

**接口设计**：
```python
class NotificationService:
    def send_email(self, to: str, subject: str, content: str) -> bool
    def send_notification(self, user_id: str, message: str) -> bool
    def schedule_notification(self, notification: Notification) -> bool
    def get_notification_templates(self) -> List[Template]
```

#### 3.1.8 分析报告模块
**功能描述**：生成数据分析和可视化报告
**主要组件**：
- 数据分析引擎
- 可视化生成器
- 报表模板管理器
- 导出服务

**接口设计**：
```python
class AnalysisService:
    def cluster_analysis(self, data: List[NewsItem]) -> ClusterResult
    def keyword_analysis(self, data: List[NewsItem]) -> KeywordResult
    def generate_visualization(self, analysis_result: AnalysisResult) -> Chart
    def export_report(self, report: Report, format: str) -> bytes
```

### 3.2 模块间交互关系

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   信息获取模块   │───→│   知识库模块     │───→│   智能查询模块   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   AI服务模块     │    │   内容管理模块   │    │   通知模块       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   用户管理模块   │
                       └─────────────────┘
```

## 4. 数据库设计

### 4.1 概念设计

#### 4.1.1 实体关系图
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   用户表     │    │   新闻表     │    │   标签表     │
│-------------│    │-------------│    │-------------│
│ user_id     │    │ news_id     │    │ tag_id      │
│ username    │    │ title       │    │ tag_name    │
│ password    │    │ content     │    │ description │
│ email       │    │ source      │    │ created_at  │
│ created_at  │    │ category    │    └─────────────┘
│ last_login  │    │ publish_date│              │
│ status      │    │ created_at  │              │
└─────────────┘    │ updated_at  │              │
        │          └─────────────┘              │
        │                    │                  │
        │                    ▼                  │
        │            ┌─────────────┐            │
        │            │新闻标签关联表│            │
        │            │-------------│            │
        │            │ news_id     │            │
        │            │ tag_id      │            │
        │            └─────────────┘            │
        │                    │                  │
        │                    ▼                  │
        │            ┌─────────────┐            │
        └─────────────│查询记录表   │─────────────┘
                      │-------------│
                      │ query_id    │
                      │ user_id     │
                      │ query_text  │
                      │ results     │
                      │ created_at  │
                      └─────────────┘
```

### 4.2 逻辑设计

#### 4.2.1 用户表 (users)
```sql
CREATE TABLE users (
    user_id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    full_name VARCHAR(100),
    avatar_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    status ENUM('active', 'inactive', 'banned') DEFAULT 'active',
    preferences JSON
);
```

#### 4.2.2 新闻表 (news_items)
```sql
CREATE TABLE news_items (
    news_id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    summary TEXT,
    source VARCHAR(100),
    source_url VARCHAR(500),
    category VARCHAR(50),
    publish_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_processed BOOLEAN DEFAULT FALSE,
    embedding_id VARCHAR(36),
    metadata JSON
);
```

#### 4.2.3 标签表 (tags)
```sql
CREATE TABLE tags (
    tag_id VARCHAR(36) PRIMARY KEY,
    tag_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    color VARCHAR(7),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### 4.2.4 新闻标签关联表 (news_tags)
```sql
CREATE TABLE news_tags (
    news_id VARCHAR(36),
    tag_id VARCHAR(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (news_id, tag_id),
    FOREIGN KEY (news_id) REFERENCES news_items(news_id),
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
);
```

#### 4.2.5 查询记录表 (query_records)
```sql
CREATE TABLE query_records (
    query_id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36),
    query_text TEXT NOT NULL,
    query_type ENUM('semantic', 'keyword', 'hybrid') DEFAULT 'semantic',
    results JSON,
    response_time INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
```

#### 4.2.6 系统配置表 (system_config)
```sql
CREATE TABLE system_config (
    config_id VARCHAR(36) PRIMARY KEY,
    config_key VARCHAR(100) NOT NULL UNIQUE,
    config_value TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### 4.3 物理设计

#### 4.3.1 索引设计
```sql
-- 用户表索引
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_status ON users(status);

-- 新闻表索引
CREATE INDEX idx_news_items_title ON news_items(title);
CREATE INDEX idx_news_items_category ON news_items(category);
CREATE INDEX idx_news_items_publish_date ON news_items(publish_date);
CREATE INDEX idx_news_items_created_at ON news_items(created_at);
CREATE INDEX idx_news_items_source ON news_items(source);

-- 标签表索引
CREATE INDEX idx_tags_tag_name ON tags(tag_name);

-- 查询记录表索引
CREATE INDEX idx_query_records_user_id ON query_records(user_id);
CREATE INDEX idx_query_records_created_at ON query_records(created_at);
CREATE INDEX idx_query_records_query_type ON query_records(query_type);
```

#### 4.3.2 向量数据库设计
- **向量索引**：使用FAISS建立HNSW索引
- **向量维度**：all-MiniLM-L6-v2模型输出维度为384
- **索引参数**：
  - HNSW参数：ef=200, M=16
  - 批量大小：1000
  - 索引路径：`./data/faiss_index`

## 5. 接口设计

### 5.1 RESTful API设计

#### 5.1.1 用户管理接口
```yaml
# 用户注册
POST /api/v1/auth/register
Request:
{
  "username": "string",
  "password": "string",
  "email": "string",
  "full_name": "string"
}
Response:
{
  "code": 200,
  "message": "success",
  "data": {
    "user_id": "string",
    "token": "string"
  }
}

# 用户登录
POST /api/v1/auth/login
Request:
{
  "username": "string",
  "password": "string"
}
Response:
{
  "code": 200,
  "message": "success",
  "data": {
    "user_id": "string",
    "token": "string"
  }
}

# 获取用户信息
GET /api/v1/users/profile
Headers:
  Authorization: Bearer <token>
Response:
{
  "code": 200,
  "message": "success",
  "data": {
    "user_id": "string",
    "username": "string",
    "email": "string",
    "full_name": "string",
    "created_at": "timestamp"
  }
}
```

#### 5.1.2 新闻管理接口
```yaml
# 获取新闻列表
GET /api/v1/news
Query Parameters:
  page: integer (default: 1)
  size: integer (default: 10)
  category: string
  source: string
  tags: string
  start_date: date
  end_date: date
Response:
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 100,
    "items": [
      {
        "news_id": "string",
        "title": "string",
        "summary": "string",
        "source": "string",
        "category": "string",
        "publish_date": "timestamp",
        "tags": ["string"]
      }
    ]
  }
}

# 创建新闻
POST /api/v1/news
Headers:
  Authorization: Bearer <token>
Request:
{
  "title": "string",
  "content": "string",
  "source": "string",
  "category": "string",
  "tags": ["string"]
}
Response:
{
  "code": 200,
  "message": "success",
  "data": {
    "news_id": "string",
    "title": "string",
    "created_at": "timestamp"
  }
}

# 删除新闻
DELETE /api/v1/news/{news_id}
Headers:
  Authorization: Bearer <token>
Response:
{
  "code": 200,
  "message": "success"
}
```

#### 5.1.3 智能查询接口
```yaml
# 语义查询
POST /api/v1/query/semantic
Headers:
  Authorization: Bearer <token>
Request:
{
  "query": "string",
  "top_k": integer (default: 10),
  "filters": {
    "category": "string",
    "source": "string",
    "date_range": {
      "start": "date",
      "end": "date"
    }
  }
}
Response:
{
  "code": 200,
  "message": "success",
  "data": {
    "query_id": "string",
    "results": [
      {
        "news_id": "string",
        "title": "string",
        "content": "string",
        "similarity": 0.95,
        "source": "string",
        "publish_date": "timestamp"
      }
    ],
    "response_time": 1500
  }
}

# 智能问答
POST /api/v1/query/chat
Headers:
  Authorization: Bearer <token>
Request:
{
  "question": "string",
  "context": "string"
}
Response:
{
  "code": 200,
  "message": "success",
  "data": {
    "answer": "string",
    "sources": [
      {
        "news_id": "string",
        "title": "string",
        "relevance": 0.9
      }
    ],
    "response_time": 2500
  }
}
```

#### 5.1.4 数据分析接口
```yaml
# 获取关键词分析
GET /api/v1/analysis/keywords
Query Parameters:
  time_range: string (default: "7d")
  category: string
Response:
{
  "code": 200,
  "message": "success",
  "data": {
    "keywords": [
      {
        "keyword": "string",
        "frequency": 100,
        "trend": "up|down|stable"
      }
    ],
    "total": 50
  }
}

# 获取聚类分析
GET /api/v1/analysis/clusters
Query Parameters:
  algorithm: string (default: "kmeans")
  n_clusters: integer (default: 5)
Response:
{
  "code": 200,
  "message": "success",
  "data": {
    "clusters": [
      {
        "cluster_id": 0,
        "size": 25,
        "keywords": ["string"],
        "news_items": ["string"]
      }
    ]
  }
}
```

### 5.2 WebSocket接口

#### 5.2.1 实时通知
```javascript
// 客户端连接
const socket = new WebSocket('ws://localhost:8080/ws/notifications');

// 接收通知
socket.onmessage = function(event) {
  const notification = JSON.parse(event.data);
  console.log('收到通知:', notification);
};

// 发送心跳
setInterval(() => {
  socket.send(JSON.stringify({ type: 'heartbeat' }));
}, 30000);
```

## 6. 部署设计

### 6.1 部署架构

#### 6.1.1 单机部署架构
```
┌─────────────────────────────────────────────────────────────┐
│                        负载均衡器                           │
│                        (Nginx)                             │
├─────────────────────────────────────────────────────────────┤
│                        Web服务器                           │
│                        (Nginx)                             │
├─────────────────────────────────────────────────────────────┤
│                        应用服务器                           │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐   │
│  │前端应用     │后端API      │AI服务      │定时任务     │   │
│  │(React)     │(SpringBoot) │(Ollama)    │(Cron)      │   │
│  └─────────────┴─────────────┴─────────────┴─────────────┘   │
├─────────────────────────────────────────────────────────────┤
│                        数据存储                           │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐   │
│  │MySQL/SQLite │FAISS       │Redis       │文件存储     │   │
│  └─────────────┴─────────────┴─────────────┴─────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

#### 6.1.2 Docker容器化部署
```dockerfile
# Docker Compose配置
version: '3.8'

services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://backend:8080
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "8080:8080"
    environment:
      - SPRING_PROFILES_ACTIVE=prod
      - DATABASE_URL=jdbc:mysql://mysql:3306/xu_news
    depends_on:
      - mysql
      - redis
      - ollama

  mysql:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=root
      - MYSQL_DATABASE=xu_news
    volumes:
      - mysql_data:/var/lib/mysql
    ports:
      - "3306:3306"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0

  faiss:
    build: ./faiss
    volumes:
      - faiss_data:/data/faiss

volumes:
  mysql_data:
  redis_data:
  ollama_data:
  faiss_data:
```

### 6.2 环境配置

#### 6.2.1 开发环境
```yaml
# application-dev.yml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/xu_news_dev
    username: dev_user
    password: dev_password
    driver-class-name: com.mysql.cj.jdbc.Driver
  
  redis:
    host: localhost
    port: 6379
    database: 0
  
  ai:
    ollama:
      base-url: http://localhost:11434
      model: qwen2.5:3b
      embedding-model: all-MiniLM-L6-v2
      rerank-model: ms-marco-MiniLM-L-6-v2
  
  file:
    upload-path: ./uploads/dev
```

#### 6.2.2 生产环境
```yaml
# application-prod.yml
spring:
  datasource:
    url: jdbc:mysql://${DB_HOST}:3306/xu_news_prod
    username: ${DB_USERNAME}
    password: ${DB_PASSWORD}
    driver-class-name: com.mysql.cj.jdbc.Driver
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5
      connection-timeout: 30000
  
  redis:
    host: ${REDIS_HOST}
    port: ${REDIS_PORT}
    password: ${REDIS_PASSWORD}
    database: 0
    timeout: 3000
  
  ai:
    ollama:
      base-url: http://${OLLAMA_HOST}:11434
      model: qwen2.5:3b
      embedding-model: all-MiniLM-L-6-v2
      rerank-model: ms-marco-MiniLM-L-6-v2
  
  file:
    upload-path: /data/uploads/prod
```

### 6.3 监控和日志

#### 6.3.1 监控配置
```yaml
# 监控配置
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
  endpoint:
    health:
      show-details: always
  metrics:
    export:
      prometheus:
        enabled: true
  
  # 健康检查
  health:
    redis:
      enabled: true
    db:
      enabled: true
    ollama:
      enabled: true
```

#### 6.3.2 日志配置
```yaml
# 日志配置
logging:
  level:
    root: INFO
    com.xu.news: DEBUG
  pattern:
    console: "%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n"
    file: "%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n"
  file:
    name: logs/xu-news.log
    max-size: 100MB
    max-history: 30
```

## 7. 安全设计

### 7.1 安全架构

#### 7.1.1 分层安全策略
```
┌─────────────────────────────────────────────────────────────┐
│                        应用层安全                           │
│           (输入验证、XSS防护、CSRF防护)                     │
├─────────────────────────────────────────────────────────────┤
│                        认证层安全                           │
│           (JWT认证、OAuth2.0、多因素认证)                   │
├─────────────────────────────────────────────────────────────┤
│                        授权层安全                           │
│           (RBAC权限控制、API访问控制)                       │
├─────────────────────────────────────────────────────────────┤
│                        数据层安全                           │
│           (数据加密、访问控制、审计日志)                     │
├─────────────────────────────────────────────────────────────┤
│                        网络层安全                           │
│           (防火墙、入侵检测、DDoS防护)                       │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 认证和授权

#### 7.2.1 JWT认证实现
```python
# JWT工具类
class JWTUtil:
    SECRET_KEY = "your-secret-key"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_DAYS = 7

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, JWTUtil.SECRET_KEY, algorithm=JWTUtil.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str):
        try:
            payload = jwt.decode(token, JWTUtil.SECRET_KEY, algorithms=[JWTUtil.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            return username
        except JWTError:
            raise credentials_exception
```

#### 7.2.2 权限控制实现
```python
# 权限装饰器
def require_permission(permission: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                raise HTTPException(status_code=401, detail="Missing authentication token")
            
            user_id = JWTUtil.verify_token(token)
            user = await UserService.get_user_by_id(user_id)
            
            if not user or not user.has_permission(permission):
                raise HTTPException(status_code=403, detail="Insufficient permissions")
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator
```

### 7.3 数据安全

#### 7.3.1 数据加密
```python
# 数据加密工具类
class CryptoUtil:
    SECRET_KEY = "your-encryption-key"
    ALGORITHM = "AES-256-CBC"

    @staticmethod
    def encrypt(data: str) -> str:
        key = hashlib.sha256(CryptoUtil.SECRET_KEY.encode()).digest()
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        padded_data = data.encode() + b'\x00' * (16 - len(data.encode()) % 16)
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        return base64.b64encode(iv + encrypted_data).decode()

    @staticmethod
    def decrypt(encrypted_data: str) -> str:
        key = hashlib.sha256(CryptoUtil.SECRET_KEY.encode()).digest()
        data = base64.b64decode(encrypted_data)
        iv = data[:16]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(data[16:]) + decryptor.finalize()
        return decrypted_data.rstrip(b'\x00').decode()
```

#### 7.3.2 敏感数据保护
```python
# 敏感数据处理
class SensitiveDataHandler:
    @staticmethod
    def mask_email(email: str) -> str:
        if '@' not in email:
            return email
        username, domain = email.split('@', 1)
        return f"{username[:2]}...@{domain}"

    @staticmethod
    def mask_phone(phone: str) -> str:
        if len(phone) < 4:
            return phone
        return f"{phone[:2]}...{phone[-2:]}"

    @staticmethod
    def hash_sensitive_data(data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()
```

### 7.4 网络安全

#### 7.4.1 API安全
```python
# API安全中间件
class APISecurityMiddleware:
    def __init__(self, app):
        self.app = app
        self.setup_security()

    def setup_security(self):
        # CORS配置
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["https://yourdomain.com"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # 请求限流
        self.app.add_middleware(RateLimitMiddleware, 
                              rate_limit="100/minute", 
                              error_response=self.rate_limit_response)

        # 安全头
        self.app.add_middleware(
            SecurityHeadersMiddleware,
            content_security_policy="default-src 'self'",
            strict_transport_security="max-age=31536000; includeSubDomains",
            x_content_type_options="nosniff",
            x_frame_options="DENY",
            x_xss_protection="1; mode=block"
        )

    def rate_limit_response(self, request):
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded"}
        )
```

## 8. 性能设计

### 8.1 性能优化策略

#### 8.1.1 缓存策略
```python
# 多级缓存实现
class MultiLevelCache:
    def __init__(self):
        self.l1_cache = {}  # 内存缓存
        self.l2_cache = RedisCache()  # Redis缓存
        self.l3_cache = FileCache()  # 文件缓存

    def get(self, key: str):
        # L1缓存
        if key in self.l1_cache:
            return self.l1_cache[key]
        
        # L2缓存
        value = self.l2_cache.get(key)
        if value is not None:
            self.l1_cache[key] = value  # 回填L1缓存
            return value
        
        # L3缓存
        value = self.l3_cache.get(key)
        if value is not None:
            self.l2_cache.set(key, value, ttl=3600)  # 回填L2缓存
            self.l1_cache[key] = value  # 回填L1缓存
            return value
        
        return None

    def set(self, key: str, value: any, ttl: int = 3600):
        self.l1_cache[key] = value
        self.l2_cache.set(key, value, ttl)
        self.l3_cache.set(key, value, ttl * 24)  # 文件缓存时间更长
```

#### 8.1.2 数据库优化
```python
# 数据库连接池配置
HikariConfig config = new HikariConfig();
config.setJdbcUrl("jdbc:mysql://localhost:3306/xu_news");
config.setUsername("username");
config.setPassword("password");
config.setDriverClassName("com.mysql.cj.jdbc.Driver");

# 连接池参数
config.setMaximumPoolSize(20);
config.setMinimumIdle(5);
config.setConnectionTimeout(30000);
config.setIdleTimeout(600000);
config.setMaxLifetime(1800000);
config.setLeakDetectionThreshold(15000);

# 性能优化
config.addDataSourceProperty("cachePrepStmts", "true");
config.addDataSourceProperty("prepStmtCacheSize", "250");
config.addDataSourceProperty("prepStmtCacheSqlLimit", "2048");
config.addDataSourceProperty("useServerPrepStmts", "true");
config.addDataSourceProperty("useLocalSessionState", "true");
config.addDataSourceProperty("rewriteBatchedStatements", "true");
config.addDataSourceProperty("cacheResultSetMetadata", "true");
config.addDataSourceProperty("cacheServerConfiguration", "true");
config.addDataSourceProperty("elideSetAutoCommits", "true");
config.addDataSourceProperty("maintainTimeStats", "false");
```

#### 8.1.3 AI服务优化
```python
# AI服务性能优化
class AIServiceOptimizer:
    def __init__(self):
        self.model_pool = ModelPool()
        self.request_queue = RequestQueue()
        self.result_cache = ResultCache()

    async def process_request(self, request: AIRequest):
        # 检查缓存
        cache_key = self.generate_cache_key(request)
        cached_result = self.result_cache.get(cache_key)
        if cached_result:
            return cached_result

        # 请求队列处理
        future = await self.request_queue.submit(request)
        try:
            result = await future
            # 缓存结果
            self.result_cache.set(cache_key, result, ttl=3600)
            return result
        except Exception as e:
            raise AIServiceException(f"AI服务处理失败: {str(e)}")

    def generate_cache_key(self, request: AIRequest) -> str:
        # 基于请求内容生成缓存键
        content = f"{request.type}:{request.query}:{request.timestamp}"
        return hashlib.md5(content.encode()).hexdigest()
```

### 8.2 性能监控

#### 8.2.1 性能指标收集
```python
# 性能监控装饰器
def monitor_performance(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            duration = time.time() - start_time
            
            # 记录性能指标
            metrics = {
                "function": func.__name__,
                "duration": duration,
                "success": True,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # 发送到监控系统
            await MetricsCollector.collect(metrics)
            
            return result
        except Exception as e:
            duration = time.time() - start_time
            
            # 记录错误指标
            metrics = {
                "function": func.__name__,
                "duration": duration,
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            await MetricsCollector.collect(metrics)
            raise
    
    return wrapper
```

#### 8.2.2 性能告警配置
```yaml
# 性能告警配置
performance_alerts:
  - name: "high_response_time"
    condition: "avg_response_time > 2000"
    threshold: 5
    action: "send_alert"
    
  - name: "high_error_rate"
    condition: "error_rate > 0.05"
    threshold: 3
    action: "send_alert"
    
  - name: "high_memory_usage"
    condition: "memory_usage > 0.8"
    threshold: 3
    action: "send_alert"
    
  - name: "high_cpu_usage"
    condition: "cpu_usage > 0.8"
    threshold: 3
    action: "send_alert"
```

## 9. 扩展性设计

### 9.1 模块化扩展

#### 9.1.1 插件架构
```python
# 插件接口定义
class PluginInterface:
    def initialize(self, config: dict):
        raise NotImplementedError
    
    def execute(self, data: any) -> any:
        raise NotImplementedError
    
    def cleanup(self):
        raise NotImplementedError

# 插件管理器
class PluginManager:
    def __init__(self):
        self.plugins = {}
        self.plugin_configs = {}

    def register_plugin(self, name: str, plugin_class: type, config: dict):
        if name in self.plugins:
            raise PluginAlreadyExistsError(f"Plugin {name} already exists")
        
        plugin_instance = plugin_class()
        plugin_instance.initialize(config)
        self.plugins[name] = plugin_instance
        self.plugin_configs[name] = config

    def execute_plugin(self, name: str, data: any) -> any:
        if name not in self.plugins:
            raise PluginNotFoundError(f"Plugin {name} not found")
        
        return self.plugins[name].execute(data)

    def unregister_plugin(self, name: str):
        if name in self.plugins:
            self.plugins[name].cleanup()
            del self.plugins[name]
            del self.plugin_configs[name]
```

#### 9.1.2 数据源扩展
```python
# 数据源接口
class DataSourceInterface:
    def connect(self, config: dict):
        raise NotImplementedError
    
    def fetch_data(self, query: dict) -> list:
        raise NotImplementedError
    
    def disconnect(self):
        raise NotImplementedError

# 数据源工厂
class DataSourceFactory:
    _data_sources = {
        'rss': RSSDataSource,
        'web': WebDataSource,
        'api': APIDataSource,
        'file': FileDataSource
    }

    @classmethod
    def create_data_source(cls, source_type: str, config: dict) -> DataSourceInterface:
        if source_type not in cls._data_sources:
            raise DataSourceNotFoundError(f"Data source {source_type} not found")
        
        data_source_class = cls._data_sources[source_type]
        return data_source_class(config)
    
    @classmethod
    def register_data_source(cls, source_type: str, data_source_class: type):
        cls._data_sources[source_type] = data_source_class
```

### 9.2 水平扩展

#### 9.2.1 微服务架构
```yaml
# 微服务配置
services:
  - name: user-service
    image: xu-news/user-service:latest
    ports:
      - "8081:8080"
    environment:
      - SPRING_PROFILES_ACTIVE=prod
      - DATABASE_URL=jdbc:mysql://mysql:3306/xu_news_users
    depends_on:
      - mysql
      - redis

  - name: news-service
    image: xu-news/news-service:latest
    ports:
      - "8082:8080"
    environment:
      - SPRING_PROFILES_ACTIVE=prod
      - DATABASE_URL=jdbc:mysql://mysql:3306/xu_news_news
    depends_on:
      - mysql
      - redis
      - ai-service

  - name: ai-service
    image: xu-news/ai-service:latest
    ports:
      - "8083:8080"
    environment:
      - SPRING_PROFILES_ACTIVE=prod
      - OLLAMA_URL=http://ollama:11434
    depends_on:
      - ollama
      - faiss

  - name: search-service
    image: xu-news/search-service:latest
    ports:
      - "8084:8080"
    environment:
      - SPRING_PROFILES_ACTIVE=prod
      - FAISS_PATH=/data/faiss
    depends_on:
      - faiss
```

#### 9.2.2 负载均衡配置
```nginx
# Nginx负载均衡配置
upstream xu_news_backend {
    least_conn;
    server user-service:8080 weight=1;
    server news-service:8080 weight=2;
    server ai-service:8080 weight=3;
    server search-service:8080 weight=2;
    
    # 健康检查
    health_check interval=30s fails=3 passes=2;
}

server {
    listen 80;
    server_name your-domain.com;

    # 前端应用
    location / {
        proxy_pass http://frontend:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # API网关
    location /api/ {
        proxy_pass http://xu_news_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 负载均衡策略
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
        proxy_next_upstream_tries 3;
        proxy_next_upstream_timeout 10s;
        
        # 缓存配置
        proxy_cache api_cache;
        proxy_cache_valid 200 302 10m;
        proxy_cache_valid 404 1m;
    }

    # WebSocket支持
    location /ws/ {
        proxy_pass http://xu_news_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

### 9.3 数据扩展

#### 9.3.1 数据库分片策略
```python
# 数据库分片管理
class DatabaseShardManager:
    def __init__(self, shard_configs: list):
        self.shards = {}
        self.shard_configs = shard_configs
        self.initialize_shards()

    def initialize_shards(self):
        for config in self.shard_configs:
            shard_id = config['shard_id']
            self.shards[shard_id] = DatabaseShard(config)

    def get_shard(self, key: str) -> DatabaseShard:
        # 基于键选择分片
        shard_id = self.hash_key(key) % len(self.shards)
        return self.shards[shard_id]

    def hash_key(self, key: str) -> int:
        # 一致性哈希算法
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def add_shard(self, config: dict):
        # 动态添加分片
        shard_id = config['shard_id']
        if shard_id in self.shards:
            raise ShardAlreadyExistsError(f"Shard {shard_id} already exists")
        
        self.shards[shard_id] = DatabaseShard(config)
        self.rebalance_data()

    def remove_shard(self, shard_id: str):
        # 动态移除分片
        if shard_id not in self.shards:
            raise ShardNotFoundError(f"Shard {shard_id} not found")
        
        del self.shards[shard_id]
        self.rebalance_data()

    def rebalance_data(self):
        # 数据重平衡
        # 实现数据迁移逻辑
        pass
```

#### 9.3.2 向量数据库扩展
```python
# 向量数据库分片
class VectorDatabaseShard:
    def __init__(self, shard_id: str, config: dict):
        self.shard_id = shard_id
        self.index = self.create_index(config)
        self.metadata_store = MetadataStore(config)

    def create_index(self, config: dict):
        # 创建FAISS索引
        dimension = config.get('dimension', 384)
        index_type = config.get('index_type', 'HNSW')
        
        if index_type == 'HNSW':
            index = faiss.IndexHNSWFlat(dimension, config.get('M', 16))
            index.hnsw.ef = config.get('ef', 200)
        elif index_type == 'IVF':
            nlist = config.get('nlist', 100)
            quantizer = faiss.IndexHNSWFlat(dimension, 16)
            index = faiss.IndexIVFFlat(quantizer, dimension, nlist)
        
        return index

    def add_vectors(self, vectors: np.ndarray, metadata: list):
        # 添加向量到索引
        self.index.add(vectors)
        self.metadata_store.add_metadata(metadata)

    def search_vectors(self, query_vector: np.ndarray, k: int = 10):
        # 搜索相似向量
        distances, indices = self.index.search(query_vector.reshape(1, -1), k)
        return self.metadata_store.get_metadata(indices[0])
```

## 10. 总结

### 10.1 设计要点总结

1. **架构设计**：采用前后端分离的微服务架构，确保系统的可扩展性和可维护性
2. **模块化设计**：系统划分为8个核心模块，每个模块职责明确，接口清晰
3. **数据存储**：采用关系型数据库+向量数据库的混合存储方案，满足结构化和非结构化数据需求
4. **AI服务**：基于Ollama部署大语言模型，提供智能问答和语义搜索功能
5. **安全设计**：多层次的安全防护，包括认证、授权、数据加密等
6. **性能优化**：采用多级缓存、数据库优化、AI服务优化等策略
7. **扩展性**：支持插件架构、微服务扩展、数据库分片等扩展方式

### 10.2 实施建议

1. **分阶段实施**：建议按照核心功能→辅助功能→高级功能的顺序分阶段实施
2. **技术选型**：根据团队技术栈和项目需求选择合适的技术框架
3. **测试策略**：建立完善的测试体系，包括单元测试、集成测试、性能测试
4. **监控运维**：建立完善的监控和运维体系，确保系统稳定运行
5. **文档维护**：保持技术文档的更新，确保团队协作效率

### 10.3 风险评估

1. **技术风险**：AI模型性能可能不达预期，需要充分的测试和优化
2. **性能风险**：随着数据量增长，系统性能可能下降，需要做好扩展准备
3. **安全风险**：系统面临各种安全威胁，需要建立完善的安全防护体系
4. **运维风险**：系统复杂度增加，运维难度加大，需要建立完善的运维体系

### 10.4 后续优化

1. **性能优化**：持续监控系统性能，进行针对性优化
2. **功能扩展**：根据用户反馈和业务需求，持续扩展系统功能
3. **技术升级**：关注新技术发展，适时进行技术升级
4. **用户体验**：持续优化用户体验，提升用户满意度

---

*本文档基于PRD.md需求文档编制，如有疑问请参考PRD文档或联系产品团队。*
