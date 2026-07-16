# gpt-image-2 / video-v1 交付审计（2026-07-13）

## 实用链路结果

- gpt-image-2：真实上游生成成功，结果上传 MinIO，SSE 返回成功，画布预览与历史记录可见，刷新后仍可恢复。
- video-v1：真实上游任务完成，MP4 下载并上传 MinIO，生成记录完成，刷新后视频节点仍可恢复。
- 浏览器视频证据：HTMLVideoElement readyState=4，1280×720，时长 5.05 秒，无媒体错误；实际播放后 currentTime 从 0 推进到 0.90 秒。
- 浏览器最新刷新控制台：0 error、0 warning；当前画布/API 请求为 200/204，视频 Range 请求为 206。

## 自动化回归

- 前端 Vitest：17 个文件、76 项全部通过。
- 前端生产构建：Vite 5.4.21 构建通过（1850 modules）。
- 后端现行测试：90 项全部通过（含认证、画布 API、画布助手及供应商契约）。
- 图片/视频供应商契约和画布关键集成路径已定向验证。
- 前端生产依赖 `npm audit --omit=dev`：0 项漏洞。

## 历史测试基线说明

以下 11 个测试模块引用已删除的 pre-v1 架构或过期 T048 项目/文件响应契约（如 src.api.upload、src.tasks.task、FileProcessingStatus、SupportedFileType、ProjectStatus.DRAFT），无法测试当前产品代码，已在 tests/conftest.py 明确列入 collect_ignore：

- test_async_file_processing.py
- integration/test_database_integration.py
- integration/test_file_upload_workflow.py
- integration/test_projects.py（旧 T048 非 UUID/mock 响应契约）
- integration/test_upload.py（旧 T048 文件管理 mock 契约）
- unit/test_file_handlers.py
- unit/test_files_api.py
- unit/test_projects_api.py
- unit/test_upload_api.py
- unit/test_project_service.py
- unit/test_storage.py

测试数据库引擎已在 session 结束时显式 dispose；全套现行测试可正常完成并退出。

## 已知非阻塞项

- Vite 提示 Element Plus 分包超过 500 kB；不影响当前功能和构建产物。
- SQLAlchemy 关系 overlaps 警告仍存在；不影响当前测试与图片/视频链路，本次未扩展为模型关系重构。
- 开发依赖仍有 Vite 5/esbuild 审计提示；修复需要升级到 Vite 8（破坏性主版本），生产依赖审计为 0。
- Vitest 提示旧 `poolOptions` 配置已弃用；不影响 76 项测试通过。

## 2026-07-16 本地验收续检

- 本地后端 `http://127.0.0.1:8000/health` 与前端 `http://127.0.0.1:3001/` 已重新启动并返回 200，PostgreSQL 与 MinIO 保持 healthy。
- Playwright 从根路径走未登录重定向时，复现登录卡片空白：页面 DOM 中输入框、按钮和表单数均为 0。
- 根因是鉴权跳转使用了父布局路由名 `Login` / `Dashboard`，只挂载布局而没有挂载默认子页；已将守卫、会话过期和通用鉴权组件的跳转统一指向 `LoginPage` / `RegisterPage` / `DashboardPage`。
- 新增 2 项路由守卫回归测试；修复前均失败，修复后前端全量为 18 个文件、78 项全部通过。
- Vite 5.4.21 生产构建再次通过；Playwright 再次从根路径验证后，登录页已显示 2 个输入框、登录按钮和注册入口，注册页也能正常挂载。
- 已配置的 `gpt-image-2`、`GPT-5.5` 与 `video-v1` 模型信息保持在本地数据库；本次未重写或输出任何模型密钥。
