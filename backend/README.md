# 茉莉妈妈短剧工作台 - 后端服务

基于 FastAPI 的 AI 短剧创作平台后端服务。

## 功能特性

- 🎬 短剧制作工作流引擎
- 🖼️ 无限画布节点系统
- 📝 图文说批量生成
- 🎨 提示词库管理
- 📤 多平台内容发布

## 快速开始

### 1. 安装依赖

```bash
cd backend
uv sync
```

### 2. 数据库迁移

```bash
alembic upgrade head
```

### 3. 启动服务

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## API 文档

启动后访问: http://localhost:8000/docs

## 技术栈

- FastAPI
- SQLAlchemy (异步)
- Alembic
- PostgreSQL
- Redis
- Celery
- MinIO
