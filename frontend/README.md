# 茉莉妈妈短剧工作台 - 前端应用

基于 Vue 3 + Element Plus 构建的现代化 AI 短剧创作平台。

## 🌟 核心功能

### 1. 📦 项目管理
- **多项目支持**: 轻松管理多个短剧创作项目
- **智能导入**: 支持 TXT/EPUB 格式导入，自动解析章节
- **角色管理**: 统一管理项目角色，设定角色画像和音色

### 2. 🎬 短剧制作工作流
- **脚本编辑**: 结构化编辑视频脚本，管理分镜内容
- **素材生成**:
  - **AI 绘图**: 一键生成场景图，支持 Prompt 优化
  - **AI 配音**: 句子级语音合成，支持试听和调整
- **实时预览**: 即时查看生成的图片和音频效果

### 3. 🖼️ 无限画布创作
- **可视化节点编排**: 自由组织创作流程
- **AI 助手引导**: 从剧本到成片一键生成
- **多人协作**: 支持多人协作与版本管理

### 4. 🎨 提示词库
- **专业模板**: 电影级提示词模板库
- **全流程覆盖**: 文生图、图生图、图转视频
- **自定义管理**: 支持自定义提示词管理

## 🛠️ 技术栈

- **核心框架**: Vue 3 (Composition API)
- **构建工具**: Vite 5
- **UI 组件库**: Element Plus
- **状态管理**: Pinia
- **路由管理**: Vue Router 4
- **HTTP 客户端**: Axios
- **样式预处理**: SCSS

## 🚀 开发指南

### 安装依赖
```bash
npm install
```

### 启动开发服务器
```bash
npm run dev
```

### 构建生产版本
```bash
npm run build
```

### 代码规范
```bash
# Lint 检查
npm run lint

# 格式化
npm run format
```

## 📁 目录结构

```
frontend/
├── src/
│   ├── api/              # API 接口定义
│   ├── assets/           # 静态资源
│   ├── components/       # 公共组件
│   │   ├── business/     # 业务组件 (如 ProjectCard)
│   │   ├── canvas/       # 画布节点组件
│   │   └── common/       # 通用 UI 组件
│   ├── composables/      # 组合式函数 (Hooks)
│   ├── router/           # 路由配置
│   ├── stores/           # Pinia 状态存储
│   ├── views/            # 页面视图
│   │   ├── project/      # 项目管理页面
│   │   ├── studio/       # 内容工坊页面
│   │   └── video/        # 视频任务页面
│   └── App.vue           # 根组件
├── .env.development      # 开发环境变量
└── vite.config.js        # Vite 配置
```

## 🔌 环境变量

在 `.env` 文件中配置后端 API 地址：

```ini
VITE_API_BASE_URL=http://localhost:8000/api/v1
```
