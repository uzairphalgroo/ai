"""
Unit tests for FastAPI Endpoints.
"""

import pytest
from httpx import AsyncClient, ASGITransport
from api.app import app


@pytest.mark.asyncio
async def test_api_health():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"
        assert data["total_vectors_loaded"] >= 100


@pytest.mark.asyncio
async def test_api_list_vectors():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/vectors?limit=5")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 5


@pytest.mark.asyncio
async def test_api_quick_scan():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "response_text": "Customer SSN is 123-45-6789 and secret CANARY-99.",
            "canary_tokens": ["CANARY-99"]
        }
        resp = await client.post("/api/eval/scan-text", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["passed"] is False
        assert data["ssn_detected"] is True
        assert data["canary_leaked"] is True


@pytest.mark.asyncio
async def test_api_eval_run_and_export():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        run_payload = {
            "target_config": {
                "provider": "mock",
                "mock_profile": "hardened_safety",
                "mock_min_latency_ms": 2,
                "mock_max_latency_ms": 5
            },
            "limit": 5
        }
        resp = await client.post("/api/eval/run", json=run_payload)
        assert resp.status_code == 200
        res_data = resp.json()
        assert "summary" in res_data
        run_id = res_data["summary"]["run_id"]

        # Test export
        export_payload = {
            "run_id": run_id,
            "export_format": "sarif"
        }
        exp_resp = await client.post("/api/eval/export", json=export_payload)
        assert exp_resp.status_code == 200
        assert exp_resp.json()["format"] == "sarif"
