"""API tests for Goals: POST (create + pipeline), GET list, GET by id with tasks and outputs."""
import pytest
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_post_goal_returns_201_and_goal_with_id():
    """POST /api/v1/goals creates a goal and runs the pipeline."""
    response = client.post(
        "/api/v1/goals",
        json={"description": "Demo goal for testing"},
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["description"] == "Demo goal for testing"
    assert data["status"] in ("planned", "in_progress", "completed", "draft")


def test_post_goal_requires_description():
    """POST without or with empty description returns 400."""
    response = client.post("/api/v1/goals", json={})
    assert response.status_code == 400
    response = client.post("/api/v1/goals", json={"description": ""})
    assert response.status_code == 400


def test_get_goals_list_returns_items():
    """GET /api/v1/goals returns items, next_cursor, and total count (for demo: red→green)."""
    response = client.get("/api/v1/goals")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "next_cursor" in data
    assert "total" in data
    assert data["total"] == len(data["items"])
    assert isinstance(data["items"], list)


def test_get_goal_by_id_returns_goal_with_tasks_and_outputs():
    """POST a goal then GET by id returns goal with tasks and per-task output (confidence, routing)."""
    create = client.post("/api/v1/goals", json={"description": "Goal for get-by-id test"})
    assert create.status_code == 201
    goal_id = create.json()["id"]

    response = client.get(f"/api/v1/goals/{goal_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == goal_id
    assert "tasks" in data
    assert isinstance(data["tasks"], list)
    for task in data["tasks"]:
        assert "id" in task and "type" in task and "status" in task
        if task.get("output"):
            assert "confidence_score" in task["output"]
            assert task["output"]["routing"] in ("auto_approved", "review_queue", "rejected")


def test_get_goal_by_id_404_for_unknown():
    """GET /api/v1/goals/{id} returns 404 for unknown id."""
    response = client.get("/api/v1/goals/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
