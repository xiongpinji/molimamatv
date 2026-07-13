#!/bin/bash

# 茉莉妈妈短剧工作台 - 启动脚本
# 启动PostgreSQL、Redis、MinIO基础设施服务

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查Docker和Docker Compose
check_dependencies() {
    log_info "检查依赖..."

    if ! command -v docker &> /dev/null; then
        log_error "Docker 未安装，请先安装Docker"
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose 未安装，请先安装Docker Compose"
        exit 1
    fi

    log_success "依赖检查通过"
}

# 创建环境变量文件
setup_env() {
    if [ ! -f .env ]; then
        log_info "创建 .env 文件..."
        cp .env.example .env
        log_warning "请编辑 .env 文件配置相关参数"
    else
        log_info ".env 文件已存在"
    fi
}

# 启动基础设施服务
start_infrastructure() {
    log_info "启动基础设施服务 (PostgreSQL, Redis, MinIO)..."

    # 尝试启动基础服务，如果网络冲突则自动清理
    if ! docker-compose up -d postgres redis minio 2>/dev/null; then
        log_warning "检测到网络冲突，正在自动清理..."

        # 自动清理冲突的网络
        docker-compose down --remove-orphans 2>/dev/null || true
        docker network prune -f 2>/dev/null || true

        log_info "重新启动服务..."
        if ! docker-compose up -d postgres redis minio; then
            log_error "服务启动失败，请手动清理Docker网络："
            echo "   docker network prune -f"
            exit 1
        fi
    fi

    # 等待服务健康检查
    log_info "等待服务启动..."
    sleep 10

    log_success "基础设施服务启动完成"
}

# 显示服务信息
show_services_info() {
    echo ""
    log_success "🎉 基础设施启动成功！"
    echo ""
    echo "📋 服务地址："
    echo "   • PostgreSQL: localhost:5432"
    echo "   • Redis:      localhost:6379"
    echo "   • MinIO:      http://localhost:9000 / http://localhost:9001"
    echo ""
    echo "🚀 本地开发："
    echo "   cd backend && uv sync && alembic upgrade head"
    echo "   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000"
    echo ""
    echo "📖 API文档: http://localhost:8000/docs"
    echo ""
}

# 主函数
main() {
    echo "🐳 AICG平台启动"
    echo "=================="

    check_dependencies
    setup_env
    start_infrastructure
    show_services_info

    log_success "启动完成！开始本地开发~ 🎨"
}

# 脚本入口
main "$@"