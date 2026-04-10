import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
from app.app import app, memo_service

# ============== FIXTURE ==============
# 모든 테스트 실행 전에 memos 초기화
@pytest.fixture(autouse=True)
def clear_memos():
    """Clear memos before each test."""
    memo_service.memos.clear()


# ============== HTML TEST ==============
def test_index_page():
    """Test that the index page renders successfully."""
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


def test_add_page():
    """Test that the add memo page renders successfully."""
    client = app.test_client()
    response = client.get("/add")
    assert response.status_code == 200


def test_delete_page():
    """Test that the delete memo page renders successfully."""
    client = app.test_client()
    response = client.get("/delete")
    assert response.status_code == 200


def test_add_memo():
    """Test memo creation via POST request."""
    client = app.test_client()
    response = client.post("/add", data={"memo": "hello"})
    
    # Check that redirect occurs
    assert response.status_code == 302


def test_memo_appears_in_list():
    """Test that a newly added memo appears in the list."""
    client = app.test_client()
    
    client.post("/add", data={"memo": "hello"})
    response = client.get("/")
    
    assert b"hello" in response.data


def test_delete_memo():
    """Test memo deletion."""
    client = app.test_client()
    
    client.post("/add", data={"memo": "bye"})
    client.get("/remove/1")
    
    response = client.get("/")
    
    assert b"bye" not in response.data