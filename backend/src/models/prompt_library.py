"""
提示词库数据模型
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import relationship

from .base import Base, BaseModel


class PromptCategory(BaseModel):
    """提示词分类表"""
    __tablename__ = "prompt_categories"

    name = Column(String(100), nullable=False, comment="分类名称")
    slug = Column(String(100), unique=True, nullable=False, comment="标识符")
    icon = Column(String(50), comment="图标")
    sort_order = Column(Integer, default=0, comment="排序")
    is_system = Column(Boolean, default=False, comment="系统预设")
    parent_id = Column(PostgreSQLUUID(as_uuid=True), nullable=True, comment="父分类ID")

    def __repr__(self) -> str:
        return f"<PromptCategory(name={self.name})>"


class PromptTag(BaseModel):
    """提示词标签表"""
    __tablename__ = "prompt_tags"

    name = Column(String(50), unique=True, nullable=False, comment="标签名")
    color = Column(String(20), default="default", comment="标签颜色")

    def __repr__(self) -> str:
        return f"<PromptTag(name={self.name})>"


class UserPrompt(BaseModel):
    """用户自定义提示词表"""
    __tablename__ = "user_prompts"

    user_id = Column(PostgreSQLUUID(as_uuid=True), nullable=False, index=True, comment="用户ID")
    category_id = Column(PostgreSQLUUID(as_uuid=True), ForeignKey("prompt_categories.id"), nullable=True, comment="分类ID")
    title = Column(String(200), nullable=False, comment="标题")
    content = Column(Text, nullable=False, comment="提示词内容")
    cover_url = Column(String(500), comment="封面图URL")
    use_case = Column(String(50), nullable=False, comment="用途: text2img/img2img/img2video/tts")
    is_public = Column(Boolean, default=False, comment="是否公开")
    is_featured = Column(Boolean, default=False, comment="是否精选")
    usage_count = Column(Integer, default=0, comment="使用次数")
    source_type = Column(String(20), default="user", comment="来源: github/user/imported")
    source_github_url = Column(String(500), comment="GitHub来源地址")
    sort_order = Column(Integer, default=0, comment="排序")
    is_active = Column(Boolean, default=True, comment="是否有效")

    def __repr__(self) -> str:
        return f"<UserPrompt(title={self.title})>"


class UserPromptFavorite(BaseModel):
    """用户收藏表"""
    __tablename__ = "user_prompt_favorites"

    user_id = Column(PostgreSQLUUID(as_uuid=True), nullable=False, index=True, comment="用户ID")
    prompt_id = Column(PostgreSQLUUID(as_uuid=True), ForeignKey("user_prompts.id"), nullable=False, index=True, comment="提示词ID")

    def __repr__(self) -> str:
        return f"<UserPromptFavorite(user_id={self.user_id}, prompt_id={self.prompt_id})>"


class UserPromptTag(BaseModel):
    """提示词-标签关联表"""
    __tablename__ = "user_prompt_tags"

    prompt_id = Column(PostgreSQLUUID(as_uuid=True), ForeignKey("user_prompts.id"), nullable=False, index=True, comment="提示词ID")
    tag_id = Column(PostgreSQLUUID(as_uuid=True), ForeignKey("prompt_tags.id"), nullable=False, index=True, comment="标签ID")

    def __repr__(self) -> str:
        return f"<UserPromptTag(prompt_id={self.prompt_id}, tag_id={self.tag_id})>"


__all__ = [
    "PromptCategory",
    "PromptTag",
    "UserPrompt",
    "UserPromptFavorite",
    "UserPromptTag",
]
