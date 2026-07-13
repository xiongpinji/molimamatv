"""
提示词库 API 路由
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import get_current_user_optional, get_current_user_required, get_db
from src.api.schemas.prompt_library import PromptCreate, PromptUpdate
from src.models.user import User
from src.services.prompt_library import PromptLibraryService

router = APIRouter()


@router.get("/")
async def get_prompts(
    use_case: Optional[str] = Query(None, description="用途类型: text2img/img2img/img2video/tts"),
    category_id: Optional[UUID] = Query(None, description="分类ID"),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db),
):
    """获取提示词列表"""
    service = PromptLibraryService(db)
    user_id = current_user.id if current_user else None
    return await service.get_prompts(
        user_id=user_id,
        use_case=use_case,
        category_id=category_id,
        keyword=keyword,
        page=page,
        page_size=page_size,
    )


@router.get("/favorites")
async def get_favorites(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user_required),
    db: AsyncSession = Depends(get_db),
):
    """获取收藏列表"""
    service = PromptLibraryService(db)
    return await service.get_favorites(
        user_id=current_user.id,
        page=page,
        page_size=page_size,
    )


@router.get("/categories")
async def get_categories(db: AsyncSession = Depends(get_db)):
    """获取分类列表"""
    service = PromptLibraryService(db)
    return await service.get_categories()


@router.get("/tags")
async def get_tags(db: AsyncSession = Depends(get_db)):
    """获取标签列表"""
    service = PromptLibraryService(db)
    return await service.get_tags()


@router.get("/{prompt_id}")
async def get_prompt(
    prompt_id: UUID,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db),
):
    """获取单个提示词"""
    service = PromptLibraryService(db)
    user_id = current_user.id if current_user else None
    prompt = await service.get_visible_prompt_by_id(prompt_id, user_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="提示词不存在")
    return prompt


@router.post("/")
async def create_prompt(
    data: PromptCreate,
    current_user: User = Depends(get_current_user_required),
    db: AsyncSession = Depends(get_db),
):
    """创建提示词"""
    service = PromptLibraryService(db)
    values = data.model_dump()
    values["user_id"] = current_user.id
    return await service.create_prompt(values)


@router.put("/{prompt_id}")
async def update_prompt(
    prompt_id: UUID,
    data: PromptUpdate,
    current_user: User = Depends(get_current_user_required),
    db: AsyncSession = Depends(get_db),
):
    """更新提示词"""
    service = PromptLibraryService(db)
    user_id = current_user.id if current_user else None
    prompt = await service.get_visible_prompt_by_id(prompt_id, user_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="提示词不存在")
    if str(prompt["user_id"]) != str(current_user.id):
        raise HTTPException(status_code=403, detail="无权修改此提示词")
    return await service.update_prompt(prompt_id, data.model_dump(exclude_unset=True))


@router.delete("/{prompt_id}")
async def delete_prompt(
    prompt_id: UUID,
    current_user: User = Depends(get_current_user_required),
    db: AsyncSession = Depends(get_db),
):
    """删除提示词"""
    service = PromptLibraryService(db)
    user_id = current_user.id if current_user else None
    prompt = await service.get_visible_prompt_by_id(prompt_id, user_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="提示词不存在")
    if str(prompt["user_id"]) != str(current_user.id):
        raise HTTPException(status_code=403, detail="无权删除此提示词")
    success = await service.delete_prompt(prompt_id)
    return {"success": success}


@router.post("/{prompt_id}/favorite")
async def toggle_favorite(
    prompt_id: UUID,
    current_user: User = Depends(get_current_user_required),
    db: AsyncSession = Depends(get_db),
):
    """收藏/取消收藏"""
    service = PromptLibraryService(db)
    is_favorited = await service.toggle_favorite(current_user.id, prompt_id)
    return {"is_favorited": is_favorited}


@router.post("/{prompt_id}/use")
async def use_prompt(
    prompt_id: UUID,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db),
):
    """使用提示词（增加使用次数）"""
    service = PromptLibraryService(db)
    await service.increment_usage(prompt_id)
    return {"success": True}
