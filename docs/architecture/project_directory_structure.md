# XU-News-AI-RAG 项目目录架构

## 项目概述

本文档基于 `Design_docs/design_schema.md` 设计文档，为 XU-News-AI-RAG 系统提供完整的项目目录架构设计。该架构遵循模块化、高内聚低耦合的设计原则，确保系统的可扩展性、可维护性和安全性。

## 目录结构总览

```
xu-ai-news-rag/
├── backend/                    # 后端服务代码
├── frontend/                   # 前端应用代码
├── data/                       # 数据存储目录
├── config/                     # 配置文件目录
├── scripts/                    # 脚本文件目录
├── docs/                       # 文档目录
├── test/                       # 测试目录
├── Design_docs/                # 设计文档目录
├── .gitignore                  # Git忽略文件
└── README.md                   # 项目说明文档
```

## 详细目录结构

### 1. 后端服务目录 (backend/)

```
backend/
├── auth/                       # 用户认证模块
│   ├── __init__.py
│   ├── models.py              # 用户数据模型
│   ├── services.py            # 认证服务
│   ├── utils.py               # 认证工具
│   ├── middleware.py          # 认证中间件
│   └── tests/                 # 认证模块测试
├── information_fetcher/        # 信息获取模块
│   ├── __init__.py
│   ├── rss_fetcher.py         # RSS订阅管理器
│   ├── web_scraper.py         # 网页爬虫引擎
│   ├── data_cleaner.py        # 数据清洗处理器
│   ├── scheduler.py           # 定时任务调度器
│   └── tests/                 # 信息获取模块测试
├── ai_service/                # AI服务模块
│   ├── __init__.py
│   ├── model_manager.py       # 模型管理器
│   ├── embedding_service.py   # 向量化服务
│   ├── search_service.py      # 检索服务
│   ├── qa_service.py          # 问答服务
│   ├── rerank_service.py      # 重排服务
│   └── tests/                 # AI服务模块测试
├── knowledge_base/            # 知识库模块
│   ├── __init__.py
│   ├── storage_manager.py     # 数据存储管理器
│   ├── index_manager.py       # 向量索引管理器
│   ├── data_analyzer.py       # 数据分析引擎
│   ├── report_generator.py    # 报表生成器
│   └── tests/                 # 知识库模块测试
├── content_manager/           # 内容管理模块
│   ├── __init__.py
│   ├── news_manager.py        # 内容管理器
│   ├── tag_manager.py         # 标签管理器
│   ├── category_manager.py    # 分类管理器
│   ├── batch_processor.py     # 批量操作处理器
│   └── tests/                 # 内容管理模块测试
├── intelligent_query/         # 智能查询模块
│   ├── __init__.py
│   ├── query_processor.py     # 查询处理器
│   ├── semantic_searcher.py   # 语义搜索引擎
│   ├── web_searcher.py        # 联网查询服务
│   ├── result_ranker.py       # 结果排序器
│   └── tests/                 # 智能查询模块测试
├── notification/              # 通知模块
│   ├── __init__.py
│   ├── email_service.py       # 邮件服务
│   ├── notification_manager.py # 通知管理器
│   ├── template_engine.py     # 模板引擎
│   ├── scheduler.py           # 发送调度器
│   └── tests/                 # 通知模块测试
├── analysis/                  # 分析报告模块
│   ├── __init__.py
│   ├── cluster_analyzer.py    # 聚类分析引擎
│   ├── keyword_analyzer.py    # 关键词分析引擎
│   ├── visualization_generator.py # 可视化生成器
│   ├── report_template_manager.py # 报表模板管理器
│   ├── export_service.py      # 导出服务
│   └── tests/                 # 分析报告模块测试
├── common/                    # 公共模块
│   ├── __init__.py
│   ├── database.py            # 数据库连接
│   ├── redis_client.py        # Redis客户端
│   ├── config.py              # 配置管理
│   ├── exceptions.py          # 异常定义
│   ├── constants.py           # 常量定义
│   └── models/                # 公共数据模型
│       ├── __init__.py
│       ├── user.py
│       ├── news.py
│       ├── query.py
│       └── base.py
├── utils/                     # 工具模块
│   ├── __init__.py
│   ├── crypto.py              # 加密工具
│   ├── validators.py          # 验证工具
│   ├── formatters.py          # 格式化工具
│   ├── file_utils.py          # 文件工具
│   └── date_utils.py          # 日期工具
├── middleware/                # 中间件模块
│   ├── __init__.py
│   ├── auth_middleware.py     # 认证中间件
│   ├── rate_limit_middleware.py # 限流中间件
│   ├── cors_middleware.py     # CORS中间件
│   ├── security_headers.py    # 安全头中间件
│   └── logging_middleware.py  # 日志中间件
├── tests/                     # 后端测试目录
│   ├── unit/                  # 单元测试
│   ├── integration/           # 集成测试
│   ├── performance/           # 性能测试
│   └── fixtures/              # 测试数据
├── main.py                    # 应用入口文件
├── requirements.txt           # Python依赖
├── config.py                  # 应用配置
└── instance/                  # 实例配置目录
    └── config.py
```

### 2. 前端应用目录 (frontend/)

```
frontend/
├── src/                       # 源代码目录
│   ├── components/            # React组件
│   │   ├── common/            # 通用组件
│   │   │   ├── Layout.js
│   │   │   ├── Header.js
│   │   │   ├── Footer.js
│   │   │   ├── Sidebar.js
│   │   │   └── Loading.js
│   │   ├── auth/              # 认证组件
│   │   │   ├── Login.js
│   │   │   ├── Register.js
│   │   │   ├── ForgotPassword.js
│   │   │   └── ResetPassword.js
│   │   ├── news/              # 新闻组件
│   │   │   ├── NewsList.js
│   │   │   ├── NewsCard.js
│   │   │   ├── NewsDetail.js
│   │   │   ├── NewsSearch.js
│   │   │   └── NewsFilter.js
│   │   ├── query/             # 查询组件
│   │   │   ├── SemanticSearch.js
│   │   │   ├── ChatInterface.js
│   │   │   ├── QueryHistory.js
│   │   │   └── ResultDisplay.js
│   │   ├── analysis/          # 分析组件
│   │   │   ├── Dashboard.js
│   │   │   ├── Charts.js
│   │   │   ├── Reports.js
│   │   │   └── Statistics.js
│   │   ├── user/              # 用户组件
│   │   │   ├── Profile.js
│   │   │   ├── Settings.js
│   │   │   ├── Preferences.js
│   │   │   └── Notifications.js
│   │   └── ui/                # UI组件
│   │       ├── Button.js
│   │       ├── Input.js
│   │       ├── Modal.js
│   │       ├── Table.js
│   │       ├── Form.js
│   │       └── Pagination.js
│   ├── pages/                 # 页面组件
│   │   ├── Auth/              # 认证页面
│   │   │   ├── Login.js
│   │   │   ├── Register.js
│   │   │   └── ForgotPassword.js
│   │   ├── News/              # 新闻页面
│   │   │   ├── NewsList.js
│   │   │   ├── NewsDetail.js
│   │   │   ├── NewsCreate.js
│   │   │   ├── NewsEdit.js
│   │   │   └── NewsManagement.js
│   │   ├── Query/             # 查询页面
│   │   │   ├── SemanticSearch.js
│   │   │   ├── ChatInterface.js
│   │   │   ├── QueryHistory.js
│   │   │   └── AdvancedSearch.js
│   │   ├── Analysis/          # 分析页面
│   │   │   ├── Dashboard.js
│   │   │   ├── KeywordAnalysis.js
│   │   │   ├── ClusterAnalysis.js
│   │   │   ├── TrendAnalysis.js
│   │   │   └── Reports.js
│   │   ├── User/              # 用户页面
│   │   │   ├── Profile.js
│   │   │   ├── Settings.js
│   │   │   └── Notifications.js
│   │   └── Error/             # 错误页面
│   │       ├── 404.js
│   │       ├── 500.js
│   │       └── Forbidden.js
│   ├── services/              # API服务
│   │   ├── api.js             # API客户端
│   │   ├── auth.js            # 认证服务
│   │   ├── news.js            # 新闻服务
│   │   ├── query.js           # 查询服务
│   │   ├── analysis.js        # 分析服务
│   │   └── upload.js          # 上传服务
│   ├── utils/                 # 工具函数
│   │   ├── helpers.js         # 通用助手函数
│   │   ├── validators.js      # 验证函数
│   │   ├── formatters.js      # 格式化函数
│   │   ├── storage.js         # 存储工具
│   │   └── constants.js       # 前端常量
│   ├── hooks/                 # 自定义Hooks
│   │   ├── useAuth.js         # 认证Hook
│   │   ├── useNews.js         # 新闻Hook
│   │   ├── useQuery.js        # 查询Hook
│   │   ├── useAnalysis.js     # 分析Hook
│   │   ├── useWebSocket.js    # WebSocket Hook
│   │   └── useLocalStorage.js # 本地存储Hook
│   ├── contexts/              # React Context
│   │   ├── AuthContext.js     # 认证上下文
│   │   ├── NewsContext.js     # 新闻上下文
│   │   ├── QueryContext.js    # 查询上下文
│   │   ├── AnalysisContext.js # 分析上下文
│   │   └── ThemeContext.js    # 主题上下文
│   ├── types/                 # TypeScript类型定义
│   │   ├── auth.ts
│   │   ├── news.ts
│   │   ├── query.ts
│   │   ├── analysis.ts
│   │   ├── api.ts
│   │   └── common.ts
│   ├── assets/                # 静态资源
│   │   ├── images/            # 图片资源
│   │   ├── icons/             # 图标资源
│   │   ├── fonts/             # 字体资源
│   │   └── styles/            # 样式资源
│   ├── styles/                # 样式文件
│   │   ├── globals.css        # 全局样式
│   │   ├── variables.css      # CSS变量
│   │   ├── components.css     # 组件样式
│   │   └── themes/            # 主题样式
│   │       ├── light.css
│   │       └── dark.css
│   ├── i18n.js                # 国际化配置
│   ├── App.js                 # 应用主组件
│   ├── index.js               # 应用入口
│   └── setupTests.js          # 测试配置
├── public/                    # 公共资源
│   ├── index.html             # HTML模板
│   ├── favicon.ico            # 网站图标
│   ├── manifest.json          # PWA配置
│   ├── robots.txt             # 搜索引擎配置
│   └── static/                # 静态文件
│       ├── images/
│       ├── fonts/
│       └── icons/
├── docs/                      # 前端文档
│   ├── API.md                 # API文档
│   ├── Components.md          # 组件文档
│   └── Styling.md             # 样式指南
├── package.json               # 项目配置
├── package-lock.json          # 依赖锁定
├── README.md                  # 项目说明
├── .env.local                # 环境变量
├── .env.development          # 开发环境变量
├── .env.production           # 生产环境变量
├── vite.config.js            # Vite配置
├── tailwind.config.js        # Tailwind配置
├── tsconfig.json             # TypeScript配置
└── .eslintrc.js              # ESLint配置
```

### 3. 数据存储目录 (data/)

```
data/
├── raw/                       # 原始数据
│   ├── rss_feeds/            # RSS原始数据
│   ├── web_scraped/          # 爬取原始数据
│   ├── uploads/              # 用户上传数据
│   └── external/             # 外部数据源
├── processed/                 # 处理后数据
│   ├── cleaned/              # 清洗后的数据
│   ├── vectorized/           # 向量化数据
│   ├── indexed/              # 索引数据
│   └── archived/             # 归档数据
├── faiss_index/              # FAISS向量索引
│   ├── news_index/           # 新闻向量索引
│   ├── semantic_index/       # 语义向量索引
│   ├── backup/               # 索引备份
│   └── metadata/             # 索引元数据
├── uploads/                  # 文件上传目录
│   ├── avatars/              # 用户头像
│   ├── documents/            # 文档文件
│   ├── images/               # 图片文件
│   └── temp/                 # 临时文件
├── logs/                     # 日志文件
│   ├── application/          # 应用日志
│   ├── access/               # 访问日志
│   ├── error/                # 错误日志
│   ├── ai_service/           # AI服务日志
│   └── backup/               # 日志备份
└── temp/                     # 临时文件
    ├── processing/           # 处理中文件
    ├── downloads/            # 下载文件
    └── cache/                # 缓存文件
```

### 4. 配置文件目录 (config/)

```
config/
├── dev/                      # 开发环境配置
│   ├── database.yml          # 数据库配置
│   ├── redis.yml             # Redis配置
│   ├── ai_service.yml        # AI服务配置
│   ├── logging.yml           # 日志配置
│   ├── security.yml          # 安全配置
│   └── app.yml               # 应用配置
├── prod/                     # 生产环境配置
│   ├── database.yml
│   ├── redis.yml
│   ├── ai_service.yml
│   ├── logging.yml
│   ├── security.yml
│   ├── performance.yml       # 性能配置
│   └── app.yml
├── test/                     # 测试环境配置
│   ├── database.yml
│   ├── redis.yml
│   ├── ai_service.yml
│   ├── logging.yml
│   └── app.yml
├── environment/              # 环境变量模板
│   ├── .env.example
│   ├── .env.development
│   └── .env.production
└── nginx/                    # Nginx配置
    ├── nginx.conf
    ├── ssl.conf
    └── upstream.conf
```

### 5. 脚本文件目录 (scripts/)

```
scripts/
├── deployment/               # 部署脚本
│   ├── deploy.sh            # 部署脚本
│   ├── rollback.sh          # 回滚脚本
│   ├── health_check.sh      # 健康检查脚本
│   ├── backup.sh            # 备份脚本
│   └── migrate.sh           # 数据迁移脚本
├── migration/               # 数据迁移脚本
│   ├── create_tables.sql     # 创建表脚本
│   ├── seed_data.sql        # 初始化数据脚本
│   ├── migrations/          # 迁移文件
│   │   ├── 001_initial.sql
│   │   ├── 002_add_indexes.sql
│   │   └── 003_update_schema.sql
│   └── rollback/            # 回滚脚本
├── backup/                  # 备份脚本
│   ├── backup_db.sh         # 数据库备份
│   ├── backup_files.sh      # 文件备份
│   ├── backup_ai_models.sh  # AI模型备份
│   └── restore.sh           # 恢复脚本
├── setup/                   # 安装脚本
│   ├── setup_env.sh         # 环境设置
│   ├── install_deps.sh      # 依赖安装
│   ├── setup_db.sh          # 数据库设置
│   └── setup_ai_models.sh   # AI模型设置
└── utilities/               # 实用脚本
    ├── cleanup.sh           # 清理脚本
    ├── monitor.sh           # 监控脚本
    ├── logrotate.sh         # 日志轮转
    └── status.sh            # 状态检查
```

### 6. 文档目录 (docs/)

```
docs/
├── api/                      # API文档
│   ├── authentication.md     # 认证API
│   ├── news.md              # 新闻API
│   ├── query.md             # 查询API
│   ├── analysis.md          # 分析API
│   ├── upload.md            # 上传API
│   └── webhooks.md          # Webhook文档
├── architecture/            # 架构文档
│   ├── system_architecture.md # 系统架构
│   ├── module_design.md     # 模块设计
│   ├── data_flow.md         # 数据流设计
│   ├── security_design.md   # 安全设计
│   └── performance_design.md # 性能设计
├── deployment/              # 部署文档
│   ├── deployment_guide.md  # 部署指南
│   ├── docker_guide.md      # Docker部署
│   ├── kubernetes_guide.md  # Kubernetes部署
│   ├── monitoring.md        # 监控配置
│   └── troubleshooting.md   # 故障排除
├── development/             # 开发文档
│   ├── setup_guide.md       # 环境搭建
│   ├── coding_standards.md  # 编码规范
│   ├── testing_guide.md     # 测试指南
│   ├── contribution.md      # 贡献指南
│   └── release_notes.md     # 发布说明
├── user_guides/             # 用户指南
│   ├── getting_started.md   # 快速开始
│   ├── user_manual.md       # 用户手册
│   ├── faq.md               # 常见问题
│   └── tutorials/           # 教程
│       ├── basic_search.md
│       ├── advanced_query.md
│       └── analysis_features.md
└── assets/                  # 文档资源
    ├── diagrams/            # 架构图
    ├── screenshots/         # 截图
    └── templates/           # 模板
```

### 7. 测试目录 (test/)

```
test/
├── unit/                     # 单元测试
│   ├── backend/             # 后端单元测试
│   │   ├── test_auth.py
│   │   ├── test_ai_service.py
│   │   ├── test_knowledge_base.py
│   │   └── test_models.py
│   └── frontend/            # 前端单元测试
│       ├── __tests__/
│       ├── components/
│       ├── services/
│       └── utils/
├── integration/              # 集成测试
│   ├── api_tests/           # API集成测试
│   ├── database_tests/      # 数据库集成测试
│   ├── ai_service_tests/    # AI服务集成测试
│   └── e2e_tests/           # 端到端测试
├── performance/             # 性能测试
│   ├── load_tests/          # 负载测试
│   ├── stress_tests/        # 压力测试
│   ├── benchmark_tests/     # 基准测试
│   └── profiling/           # 性能分析
├── fixtures/                # 测试数据
│   ├── data/                # 测试数据文件
│   ├── models/              # 测试模型
│   └── mocks/               # 模拟对象
├── config/                  # 测试配置
│   ├── pytest.ini
│   ├── jest.config.js
│   └── test.env
└── reports/                 # 测试报告
    ├── unit_reports/
    ├── integration_reports/
    └── performance_reports/
```

## 核心模块说明

### 1. 用户认证模块 (auth/)
- **功能**: 处理用户注册、登录、权限管理
- **技术栈**: JWT、OAuth2.0、RBAC
- **主要文件**:
  - `models.py`: 用户、角色、权限数据模型
  - `services.py`: 认证、授权服务
  - `middleware.py`: JWT认证中间件

### 2. 信息获取模块 (information_fetcher/)
- **功能**: 从RSS、网页等来源获取新闻信息
- **技术栈**: Feedparser、BeautifulSoup、Scrapy
- **主要文件**:
  - `rss_fetcher.py`: RSS订阅管理
  - `web_scraper.py`: 网页爬虫引擎
  - `data_cleaner.py`: 数据清洗处理

### 3. AI服务模块 (ai_service/)
- **功能**: 提供文本向量化、语义搜索、智能问答
- **技术栈**: Ollama、LangChain、FAISS
- **主要文件**:
  - `embedding_service.py`: 文本向量化
  - `search_service.py`: 语义搜索
  - `qa_service.py`: 智能问答

### 4. 知识库模块 (knowledge_base/)
- **功能**: 新闻数据存储、检索、分析
- **技术栈**: SQLAlchemy、FAISS、Pandas
- **主要文件**:
  - `storage_manager.py`: 数据存储管理
  - `index_manager.py`: 向量索引管理
  - `data_analyzer.py`: 数据分析引擎

### 5. 内容管理模块 (content_manager/)
- **功能**: 新闻内容的增删改查操作
- **技术栈**: Flask-RESTful、SQLAlchemy
- **主要文件**:
  - `news_manager.py`: 新闻内容管理
  - `tag_manager.py`: 标签管理
  - `batch_processor.py`: 批量操作处理

### 6. 智能查询模块 (intelligent_query/)
- **功能**: 提供智能搜索和问答功能
- **技术栈**: 向量搜索、自然语言处理
- **主要文件**:
  - `query_processor.py`: 查询处理
  - `semantic_searcher.py`: 语义搜索
  - `result_ranker.py`: 结果排序

### 7. 通知模块 (notification/)
- **功能**: 系统通知和邮件发送
- **技术栈**: SMTP、WebSocket、Celery
- **主要文件**:
  - `email_service.py`: 邮件服务
  - `notification_manager.py`: 通知管理
  - `template_engine.py`: 模板引擎

### 8. 分析报告模块 (analysis/)
- **功能**: 数据分析和可视化报告
- **技术栈**: Matplotlib、Plotly、Jinja2
- **主要文件**:
  - `cluster_analyzer.py`: 聚类分析
  - `keyword_analyzer.py`: 关键词分析
  - `visualization_generator.py`: 可视化生成

## 技术栈配置

### 后端技术栈
- **主框架**: Flask 3.1.2
- **数据库**: MySQL 8.0+ / SQLite 3.0+
- **ORM**: SQLAlchemy
- **缓存**: Redis
- **AI服务**: Ollama + LangChain
- **向量数据库**: FAISS
- **认证**: JWT + OAuth2.0
- **API文档**: Swagger/OpenAPI 3.0

### 前端技术栈
- **框架**: React 18+
- **状态管理**: Redux Toolkit
- **UI组件库**: Ant Design
- **构建工具**: Vite
- **样式方案**: Styled-components
- **类型检查**: TypeScript
- **HTTP客户端**: Axios
- **图表库**: ECharts / Recharts

### 部署技术栈
- **容器化**: Docker + Docker Compose
- **反向代理**: Nginx
- **进程管理**: PM2
- **监控**: Prometheus + Grafana
- **日志**: ELK Stack (Elasticsearch, Logstash, Kibana)
- **CI/CD**: GitHub Actions / Jenkins

## 开发规范

### 代码组织
- **模块化**: 每个功能模块独立，职责明确
- **分层架构**: 控制器 → 服务 → 数据访问层
- **依赖注入**: 使用依赖注入降低耦合度

### 命名规范
- **Python**: 使用下划线命名法 (snake_case)
- **JavaScript/TypeScript**: 使用驼峰命名法 (camelCase)
- **文件名**: 使用小写字母，多词用下划线分隔
- **类名**: 使用帕斯卡命名法 (PascalCase)

### 代码风格
- **Python**: 遵循 PEP 8 规范
- **JavaScript**: 遵循 ESLint + Prettier 规范
- **注释**: 使用清晰的文档字符串和注释
- **文档**: 每个模块和函数都有详细的文档说明

### 版本控制
- **Git Flow**: 使用 Git Flow 工作流
- **分支管理**: main、develop、feature、release、hotfix
- **提交规范**: 使用 Conventional Commits 规范
- **代码审查**: 所有代码都需要经过审查

## 安全考虑

### 数据安全
- **加密存储**: 敏感数据加密存储
- **传输安全**: 使用 HTTPS 加密传输
- **访问控制**: 基于角色的访问控制 (RBAC)
- **审计日志**: 记录所有重要操作日志

### 应用安全
- **输入验证**: 所有输入数据都进行验证
- **XSS防护**: 防止跨站脚本攻击
- **CSRF防护**: 防止跨站请求伪造
- **SQL注入防护**: 使用参数化查询

### 网络安全
- **防火墙**: 配置网络防火墙
- **入侵检测**: 部署入侵检测系统
- **DDoS防护**: 配置DDoS防护
- **安全头**: 设置适当的安全HTTP头

## 性能优化

### 缓存策略
- **多级缓存**: L1内存缓存 + L2 Redis缓存 + L3文件缓存
- **缓存失效**: 基于时间和事件的缓存失效策略
- **缓存预热**: 系统启动时预加载热点数据

### 数据库优化
- **索引优化**: 为常用查询字段创建索引
- **连接池**: 使用数据库连接池
- **查询优化**: 优化SQL查询语句
- **分库分表**: 大数据量时考虑分库分表

### AI服务优化
- **模型缓存**: 缓存常用查询结果
- **批量处理**: 批量处理向量化请求
- **负载均衡**: 分布式AI服务部署
- **模型压缩**: 使用模型压缩技术

## 监控和运维

### 系统监控
- **性能监控**: CPU、内存、磁盘、网络使用率
- **应用监控**: 响应时间、错误率、吞吐量
- **业务监控**: 用户活跃度、查询成功率
- **AI服务监控**: 模型响应时间、准确率

### 日志管理
- **结构化日志**: 使用结构化日志格式
- **日志级别**: DEBUG、INFO、WARNING、ERROR、CRITICAL
- **日志轮转**: 定期清理和归档日志
- **日志分析**: 使用ELK Stack进行日志分析

### 告警机制
- **阈值告警**: 设置性能和错误阈值告警
- **邮件通知**: 通过邮件发送告警信息
- **短信通知**: 重要告警通过短信通知
- **自动恢复**: 自动恢复故障服务

## 扩展性设计

### 水平扩展
- **微服务架构**: 支持微服务部署
- **负载均衡**: 使用Nginx进行负载均衡
- **容器化**: Docker容器化部署
- **编排工具**: Kubernetes容器编排

### 垂直扩展
- **资源优化**: 优化CPU和内存使用
- **数据库扩展**: 读写分离和分库分表
- **缓存扩展**: 分布式缓存集群
- **AI服务扩展**: 分布式AI推理服务

### 功能扩展
- **插件系统**: 支持插件化功能扩展
- **API网关**: 统一的API网关管理
- **消息队列**: 使用消息队列处理异步任务
- **事件驱动**: 基于事件驱动的架构

## 部署架构

### 单机部署
```
┌─────────────────────────────────────────────────────────────┐
│                        负载均衡器 (Nginx)                    │
├─────────────────────────────────────────────────────────────┤
│                        Web服务器 (Nginx)                     │
├─────────────────────────────────────────────────────────────┤
│                        应用服务器                           │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐   │
│  │前端应用     │后端API      │AI服务      │定时任务     │   │
│  │(React)     │(Flask)      │(Ollama)    │(Celery)     │   │
│  └─────────────┴─────────────┴─────────────┴─────────────┘   │
├─────────────────────────────────────────────────────────────┤
│                        数据存储                           │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐   │
│  │MySQL/SQLite │FAISS       │Redis       │文件存储     │   │
│  └─────────────┴─────────────┴─────────────┴─────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 容器化部署
```yaml
# docker-compose.yml
version: '3.8'

services:
  frontend:
    build: ./frontend
    ports: ["3000:3000"]
    environment: ["REACT_APP_API_URL=http://backend:8080"]
    depends_on: [backend]

  backend:
    build: ./backend
    ports: ["8080:8080"]
    environment: ["FLASK_ENV=production"]
    depends_on: [mysql, redis, ollama]

  mysql:
    image: mysql:8.0
    environment: ["MYSQL_ROOT_PASSWORD=root", "MYSQL_DATABASE=xu_news"]
    volumes: ["mysql_data:/var/lib/mysql"]
    ports: ["3306:3306"]

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]
    volumes: ["redis_data:/data"]

  ollama:
    image: ollama/ollama
    ports: ["11434:11434"]
    volumes: ["ollama_data:/root/.ollama"]

  faiss:
    build: ./faiss
    volumes: ["faiss_data:/data/faiss"]

volumes:
  mysql_data:
  redis_data:
  ollama_data:
  faiss_data:
```

## 总结

本目录架构设计基于 XU-News-AI-RAG 系统的设计文档，充分考虑了系统的可扩展性、可维护性、安全性和性能要求。通过模块化的设计，每个功能模块都有明确的职责和接口，便于团队协作和后续功能扩展。

该架构支持多种部署方式，包括单机部署、容器化部署和微服务部署，可以根据实际需求选择合适的部署方案。同时，完善的监控、日志和告警机制确保了系统的稳定运行。

建议在项目实施过程中，严格按照本架构设计进行开发，并保持良好的代码质量和文档维护，以确保项目的长期可持续发展。
