"""
茉莉妈妈短剧工作台 - FastAPI应用入口
"""

import time

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

from src.api.health import router as health_router
from src.middleware import (
    error_handler_middleware,
    logging_middleware,
    security_middleware,
    performance_monitoring_middleware,
)
from src.api.v1 import api_router
from src.api.websocket import router as websocket_router
from src.core.config import settings
from src.core.exceptions import AICGException
from src.core.logging import logger, setup_logging

# 设置日志
setup_logging()

# 创建FastAPI应用实例
app = FastAPI(
    title="茉莉妈妈短剧工作台",
    description="AI驱动的短剧创作与内容分发平台",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加受信任主机中间件
if settings.ENVIRONMENT == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS,
    )

# 添加自定义中间件 (顺序重要)
# 注意：中间件的执行顺序是注册的逆序
app.middleware("http")(error_handler_middleware)          # 最外层，处理所有异常
app.middleware("http")(performance_monitoring_middleware) # 性能监控
app.middleware("http")(logging_middleware)                # 日志记录
app.middleware("http")(security_middleware)               # 安全检查


# 添加请求处理时间中间件
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """添加请求处理时间头"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# 注册路由
app.include_router(api_router, prefix=settings.API_V1_PREFIX)
app.include_router(health_router, prefix="/health")
app.include_router(websocket_router, prefix="/ws")


@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    # 使用标准库日志避免JSON编码
    import logging
    app_logger = logging.getLogger(__name__)

    app_logger.info("🚀 茉莉妈妈短剧工作台正在启动...")
    app_logger.info(f"📝 环境: {settings.ENVIRONMENT}")
    app_logger.info(f"🌐 调试模式: {settings.DEBUG}")
    app_logger.info(f"🔗 API地址: http://0.0.0.0:8000")
    app_logger.info(f"📖 API文档: http://0.0.0.0:8000/docs")

    # 这里可以添加其他启动逻辑
    # 例如: 检查数据库连接、预热缓存等


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    import logging
    app_logger = logging.getLogger(__name__)
    app_logger.info("🛑 茉莉妈妈短剧工作台正在关闭...")
    # 这里可以添加清理逻辑


@app.exception_handler(AICGException)
async def aicg_exception_handler(request: Request, exc: AICGException):
    """自定义异常处理"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "code": exc.error_code,
            "message": exc.message,
            "details": exc.details,
            "timestamp": time.time(),
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """通用异常处理"""
    logger.error(f"未处理的异常: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "code": "INTERNAL_SERVER_ERROR",
            "message": "服务器内部错误" if not settings.DEBUG else str(exc),
            "timestamp": time.time(),
        },
    )


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "欢迎使用茉莉妈妈短剧工作台",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/info")
async def app_info():
    """应用信息"""
    return {
        "name": "茉莉妈妈短剧工作台",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
        "api_prefix": settings.API_V1_PREFIX,
        "monitoring": {
            "structured_logging": settings.STRUCTURED_LOGGING,
        },
    }


def main():
    """主函数入口"""
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True,
        use_colors=True,
    )


if __name__ == "__main__":
    main()
