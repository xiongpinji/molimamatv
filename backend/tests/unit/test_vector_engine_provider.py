import pytest

from src.services.provider.vector_engine_provider import VectorEngineProvider


@pytest.mark.asyncio
async def test_custom_open_api_uses_documented_video_job_contract(monkeypatch):
    captured = {}

    class Response:
        def raise_for_status(self):
            return None

        def json(self):
            return {"data": {"id": "video-task-1", "status": "queued"}}

    class Client:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *_args):
            return None

        async def post(self, url, *, headers, json):
            captured.update(url=url, headers=headers, json=json)
            return Response()

    monkeypatch.setattr("src.services.provider.vector_engine_provider.httpx.AsyncClient", lambda **_kwargs: Client())

    provider = VectorEngineProvider("secret", "https://example.test/v1", open_api=True)
    result = await provider.create_video(prompt="a butterfly", model="video-v1", aspect_ratio="16:9")

    assert result["id"] == "video-task-1"
    assert captured["url"] == "https://example.test/api/v1/video-jobs"
    assert captured["headers"]["api-key"] == "secret"
    assert "Authorization" not in captured["headers"]
    assert captured["json"]["api_key"] == "secret"
    assert captured["json"]["prompt"] == "a butterfly"
    assert captured["json"]["task_type"] == "video"
    assert '"model": "video-v1"' in captured["json"]["extra_params"]
    assert '"aspect_ratio": "16:9"' in captured["json"]["extra_params"]
    assert '"duration": 5' in captured["json"]["extra_params"]


@pytest.mark.asyncio
async def test_custom_open_api_unwraps_status_response(monkeypatch):
    class Response:
        def raise_for_status(self):
            return None

        def json(self):
            return {"code": 0, "data": {"task_id": 79755, "status": "success", "video_url": "https://example.test/video.mp4"}}

    class Client:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *_args):
            return None

        async def get(self, *_args, **_kwargs):
            return Response()

    monkeypatch.setattr("src.services.provider.vector_engine_provider.httpx.AsyncClient", lambda **_kwargs: Client())
    provider = VectorEngineProvider("secret", "https://example.test/v1", open_api=True)

    result = await provider.get_task_status(79755)

    assert result["status"] == "success"
    assert result["video_url"] == "https://example.test/video.mp4"
