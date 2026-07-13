"""
提示词库业务逻辑
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.prompt_library import (
    PromptCategory,
    PromptTag,
    UserPrompt,
    UserPromptFavorite,
    UserPromptTag,
)


class PromptLibraryService:
    """提示词库服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_prompts(
        self,
        user_id: Optional[UUID] = None,
        use_case: Optional[str] = None,
        category_id: Optional[UUID] = None,
        keyword: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """获取提示词列表"""
        query = select(UserPrompt).where(UserPrompt.is_active == True)

        if user_id:
            query = query.where(
                or_(UserPrompt.user_id == user_id, UserPrompt.is_public == True)
            )
        else:
            query = query.where(UserPrompt.is_public == True)

        if use_case:
            query = query.where(UserPrompt.use_case == use_case)

        if category_id:
            query = query.where(UserPrompt.category_id == category_id)

        if keyword:
            query = query.where(
                or_(
                    UserPrompt.title.ilike(f"%{keyword}%"),
                    UserPrompt.content.ilike(f"%{keyword}%")
                )
            )

        # 总数
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()

        # 分页
        query = query.order_by(UserPrompt.sort_order.desc(), UserPrompt.created_at.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)

        result = await self.db.execute(query)
        items = result.scalars().all()

        return {
            "items": [item.to_dict() for item in items],
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    async def get_prompt_by_id(self, prompt_id: UUID) -> Optional[Dict]:
        """获取单个提示词"""
        query = select(UserPrompt).where(UserPrompt.id == prompt_id)
        result = await self.db.execute(query)
        prompt = result.scalar_one_or_none()
        return prompt.to_dict() if prompt else None

    async def get_visible_prompt_by_id(
        self, prompt_id: UUID, user_id: Optional[UUID] = None
    ) -> Optional[Dict]:
        """仅返回公开提示词或当前用户自己的提示词。"""
        visibility = UserPrompt.is_public == True
        if user_id:
            visibility = or_(visibility, UserPrompt.user_id == user_id)
        query = select(UserPrompt).where(
            UserPrompt.id == prompt_id,
            UserPrompt.is_active == True,
            visibility,
        )
        result = await self.db.execute(query)
        prompt = result.scalar_one_or_none()
        return prompt.to_dict() if prompt else None

    async def create_prompt(self, data: Dict) -> Dict:
        """创建提示词"""
        prompt = UserPrompt(**data)
        self.db.add(prompt)
        await self.db.commit()
        await self.db.refresh(prompt)
        return prompt.to_dict()

    async def update_prompt(self, prompt_id: UUID, data: Dict) -> Optional[Dict]:
        """更新提示词"""
        query = select(UserPrompt).where(UserPrompt.id == prompt_id)
        result = await self.db.execute(query)
        prompt = result.scalar_one_or_none()

        if not prompt:
            return None

        for key, value in data.items():
            if hasattr(prompt, key):
                setattr(prompt, key, value)

        await self.db.commit()
        await self.db.refresh(prompt)
        return prompt.to_dict()

    async def delete_prompt(self, prompt_id: UUID) -> bool:
        """删除提示词（软删除）"""
        query = select(UserPrompt).where(UserPrompt.id == prompt_id)
        result = await self.db.execute(query)
        prompt = result.scalar_one_or_none()

        if not prompt:
            return False

        prompt.is_active = False
        await self.db.commit()
        return True

    async def toggle_favorite(self, user_id: UUID, prompt_id: UUID) -> bool:
        """收藏/取消收藏"""
        query = select(UserPromptFavorite).where(
            and_(
                UserPromptFavorite.user_id == user_id,
                UserPromptFavorite.prompt_id == prompt_id
            )
        )
        result = await self.db.execute(query)
        favorite = result.scalar_one_or_none()

        if favorite:
            await self.db.delete(favorite)
            await self.db.commit()
            return False
        else:
            new_favorite = UserPromptFavorite(user_id=user_id, prompt_id=prompt_id)
            self.db.add(new_favorite)
            await self.db.commit()
            return True

    async def get_favorites(self, user_id: UUID, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """获取收藏列表"""
        query = (
            select(UserPrompt)
            .join(UserPromptFavorite, UserPromptFavorite.prompt_id == UserPrompt.id)
            .where(
                and_(
                    UserPromptFavorite.user_id == user_id,
                    UserPrompt.is_active == True
                )
            )
        )

        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()

        query = query.order_by(UserPromptFavorite.created_at.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)

        result = await self.db.execute(query)
        items = result.scalars().all()

        return {
            "items": [item.to_dict() for item in items],
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    async def get_categories(self) -> List[Dict]:
        """获取分类列表"""
        query = select(PromptCategory).order_by(PromptCategory.sort_order)
        result = await self.db.execute(query)
        categories = result.scalars().all()
        return [cat.to_dict() for cat in categories]

    async def get_tags(self) -> List[Dict]:
        """获取标签列表"""
        query = select(PromptTag).order_by(PromptTag.name)
        result = await self.db.execute(query)
        tags = result.scalars().all()
        return [tag.to_dict() for tag in tags]

    async def increment_usage(self, prompt_id: UUID) -> None:
        """增加使用次数"""
        query = select(UserPrompt).where(UserPrompt.id == prompt_id)
        result = await self.db.execute(query)
        prompt = result.scalar_one_or_none()
        if prompt:
            prompt.usage_count = (prompt.usage_count or 0) + 1
            await self.db.commit()
