from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PromptCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    use_case: Literal["text2img", "img2img", "img2video", "tts"]
    category_id: Optional[UUID] = None
    cover_url: Optional[str] = Field(default=None, max_length=500)
    is_public: bool = False


class PromptUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    content: Optional[str] = Field(default=None, min_length=1)
    use_case: Optional[Literal["text2img", "img2img", "img2video", "tts"]] = None
    category_id: Optional[UUID] = None
    cover_url: Optional[str] = Field(default=None, max_length=500)
    is_public: Optional[bool] = None
