# XU-News-AI-RAG：个性化新闻智能知识库

## 项目简介

XU-News-AI-RAG 是一个基于人工智能的个性化新闻智能知识库系统，通过结合大语言模型、向量数据库和智能检索技术，为用户提供个性化的新闻信息管理、智能问答和知识发现服务。

### 核心功能

- **智能新闻获取**：通过 RSS 订阅和网页抓取自动获取最新新闻信息
- **知识库管理**：支持上传、编辑、删除和管理新闻文档
- **智能问答**：基于用户提问优先检索知识库内容，结果按相似度排序
- **联网查询**：知识库未匹配时自动触发联网查询，使用大语言模型推理
- **分析报告**：提供知识库数据聚类分析和关键词分布报告
- **用户认证**：安全的用户登录和权限管理

## 技术栈

### 后端
- **框架**：Flask
- **数据库**：MySQL (元数据), FAISS (向量数据)
- **AI 模型**：
  - 大语言模型：qwen2.5::3b (通过 Ollama 部署)
  - 嵌入模型：all-MiniLM-L6-v2
  - 重排模型：ms-marco-MiniLM-L-6-v2
- **其他**：
  - LangChain：支撑知识库构建与检索增强功能
  - JWT：用户身份认证
  - Flask-CORS：跨域资源共享

### 前端
- **框架**：React 18.2.0
- **路由**：React Router DOM 6.8.0
- **HTTP 客户端**：Axios 1.3.0
- **构建工具**：React Scripts 5.0.1

## 项目结构

```
xu-ai-news-rag/
├── app/                    # Flask 后端应用
│   ├── __init__.py        # 应用初始化
│   ├── models.py          # 数据模型
│   ├── api/               # API 路由
│   │   ├── knowledge.py   # 知识库管理 API
│   │   ├── llm_service.py # 大语言模型服务 API
│   │   └── spider.py      # 爬虫 API
│   ├── auth/              # 认证模块
│   ├── main/              # 主页和错误页面
│   ├── services/          # 业务逻辑服务
│   │   ├── faiss_vector.py # FAISS 向量数据库服务
│   │   └── spider.py      # 新闻爬虫服务
│   ├── static/            # 静态文件
│   ├── templates/         # HTML 模板
│   └── utils/             # 工具函数
├── web/                   # React 前端应用
│   ├── public/            # 公共静态文件
│   ├── src/               # 源代码
│   │   ├── components/    # React 组件
│   │   ├── contexts/      # React Context
│   │   ├── pages/         # 页面组件
│   │   └── services/      # API 服务
│   └── build/             # 构建输出目录
├── config.py              # 应用配置
├── run.py                 # 应用启动脚本
├── requirements.txt       # Python 依赖
├── docs/                  # 文档目录
└── README.md              # 项目说明
```

## 安装与部署

### 环境要求

- Python 3.8+
- Node.js 16+
- MySQL 8.0+ 或 SQLite 3.0+
- Ollama (用于运行大语言模型)

### 后端安装

1. 克隆项目
```bash
git clone https://github.com/caslip/xu-ai-news-rag.git
cd xu-ai-news-rag
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置环境变量
创建 `.env` 文件并设置以下变量：
```
FLASK_CONFIG=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
DATABASE_URL=mysql+pymysql://username:password@localhost/dbname
CORS_ORIGINS=http://localhost:3000
```

5. 初始化数据库
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. 启动 Ollama 服务
确保已安装 Ollama 并运行以下命令加载模型：
```bash
ollama pull qwen3:8b
```

7. 启动 Flask 应用
```bash
python run.py
```

后端服务将在 `http://localhost:5000` 启动。

### 前端安装

1. 进入前端目录
```bash
cd web
```

2. 安装依赖
```bash
npm install
```

3. 启动开发服务器
```bash
npm start
```

前端应用将在 `http://localhost:3000` 启动。

### 生产环境部署

1. 构建前端应用
```bash
cd web
npm run build
```

2. 配置 Flask 以服务构建文件
在 `config.py` 中设置 `REACT_BUILD_DIR` 为前端构建目录的绝对路径。

3. 使用 Gunicorn 或类似 WSGI 服务器运行 Flask 应用
```bash
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## 使用指南

### 用户注册与登录

1. 访问 `http://localhost:3000`
2. 点击"注册"创建新账户
3. 使用用户名和密码登录系统

### 知识库管理

1. 登录后，点击顶部导航栏的"知识库"
2. 查看已上传的文档列表
3. 上传新文档：点击"上传"按钮，选择文件（支持 .txt, .pdf, .doc, .docx）
4. 编辑文档元数据：点击文档名称编辑标签和来源
5. 删除文档：选择文档后点击"删除"

### 智能查询

1. 点击顶部导航栏的"智能查询"
2. 在搜索框中输入问题
3. 系统将优先从知识库检索相关信息
4. 如果知识库中没有匹配内容，系统将自动联网查询并使用大语言模型生成答案

### 分析报告

1. 点击顶部导航栏的"分析报告"
2. 点击"生成报告"创建新的分析报告
3. 查看关键词分析和聚类分析结果

## API 文档

### 认证 API

- `POST /auth/login` - 用户登录
- `POST /auth/register` - 用户注册

### 知识库 API

- `GET /api/knowledge/` - 获取知识库列表
- `POST /api/knowledge/upload` - 上传文档到知识库
- `PUT /api/knowledge/<name>` - 更新文档元数据
- `DELETE /api/knowledge/<name>` - 删除文档

### 查询 API

- `POST /api/query` - 执行智能查询

详细的 API 文档请参考 `docs/api/` 目录。

## 开发指南

### 添加新功能

1. 在 `app/api/` 目录下创建新的 API 蓝图
2. 在 `app/services/` 目录下实现业务逻辑
3. 在 `web/src/components/` 或 `web/src/pages/` 目录下添加前端组件
4. 更新 `app/__init__.py` 注册新的 API 蓝图

### 运行测试

```bash
# 运行后端测试
python -m pytest app/tests/

# 运行前端测试
cd web
npm test
```

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 联系方式

如有问题或建议，请通过以下方式联系：

- 项目地址：https://github.com/caslip/xu-ai-news-rag
- 提交问题：[GitHub Issues](https://github.com/caslip/xu-ai-news-rag/issues)

