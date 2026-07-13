from types import SimpleNamespace
from uuid import uuid4

import pytest
from pydantic import ValidationError

from src.api.schemas.prompt_library import PromptCreate, PromptUpdate
from src.api.v1 import prompt_library as prompt_library_api


def test_prompt_create_rejects_system_managed_fields():
    with pytest.raises(ValidationError):
        PromptCreate(
            title="测试",
            content="内容",
            use_case="text2img",
            is_featured=True,
        )


def test_prompt_update_rejects_owner_transfer():
    with pytest.raises(ValidationError):
        PromptUpdate(user_id=uuid4())


@pytest.mark.asyncio
async def test_prompt_detail_passes_current_user_to_visibility_check(monkeypatch):
    prompt_id = uuid4()
    user_id = uuid4()
    calls = {}

    class FakeService:
        def __init__(self, db):
            pass

        async def get_visible_prompt_by_id(self, requested_prompt_id, requested_user_id):
            calls["args"] = (requested_prompt_id, requested_user_id)
            return {"id": str(requested_prompt_id)}

    monkeypatch.setattr(prompt_library_api, "PromptLibraryService", FakeService)

    result = await prompt_library_api.get_prompt(
        prompt_id=prompt_id,
        current_user=SimpleNamespace(id=user_id),
        db=object(),
    )

    assert calls["args"] == (prompt_id, user_id)
    assert result == {"id": str(prompt_id)}
