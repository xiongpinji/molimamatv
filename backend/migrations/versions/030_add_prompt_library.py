"""添加提示词库表

Revision ID: 030
Revises: 029
Create Date: 2026-07-12
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers
revision = '030'
down_revision = '029'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 创建分类表
    op.create_table(
        'prompt_categories',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('slug', sa.String(100), unique=True, nullable=False),
        sa.Column('icon', sa.String(50)),
        sa.Column('sort_order', sa.Integer, default=0),
        sa.Column('is_system', sa.Boolean, default=False),
        sa.Column('parent_id', UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    # 创建标签表
    op.create_table(
        'prompt_tags',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(50), unique=True, nullable=False),
        sa.Column('color', sa.String(20), default='default'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    # 创建用户提示词表
    op.create_table(
        'user_prompts',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('category_id', UUID(as_uuid=True), sa.ForeignKey('prompt_categories.id'), nullable=True),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('cover_url', sa.String(500)),
        sa.Column('use_case', sa.String(50), nullable=False),
        sa.Column('is_public', sa.Boolean, default=False),
        sa.Column('is_featured', sa.Boolean, default=False),
        sa.Column('usage_count', sa.Integer, default=0),
        sa.Column('source_type', sa.String(20), default='user'),
        sa.Column('source_github_url', sa.String(500)),
        sa.Column('sort_order', sa.Integer, default=0),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    # 创建收藏表
    op.create_table(
        'user_prompt_favorites',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('prompt_id', UUID(as_uuid=True), sa.ForeignKey('user_prompts.id'), nullable=False, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    # 创建标签关联表
    op.create_table(
        'user_prompt_tags',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('prompt_id', UUID(as_uuid=True), sa.ForeignKey('user_prompts.id'), nullable=False, index=True),
        sa.Column('tag_id', UUID(as_uuid=True), sa.ForeignKey('prompt_tags.id'), nullable=False, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    # 插入系统预设分类
    op.execute("""
        INSERT INTO prompt_categories (id, name, slug, icon, sort_order, is_system, created_at, updated_at)
        VALUES
            (gen_random_uuid(), '文生图', 'text2img', 'Picture', 1, true, NOW(), NOW()),
            (gen_random_uuid(), '图生图', 'img2img', 'PictureFilled', 2, true, NOW(), NOW()),
            (gen_random_uuid(), '图转视频', 'img2video', 'VideoCamera', 3, true, NOW(), NOW()),
            (gen_random_uuid(), '音频/TTS', 'tts', 'Headset', 4, true, NOW(), NOW());
    """)


def downgrade() -> None:
    op.drop_table('user_prompt_tags')
    op.drop_table('user_prompt_favorites')
    op.drop_table('user_prompts')
    op.drop_table('prompt_tags')
    op.drop_table('prompt_categories')
