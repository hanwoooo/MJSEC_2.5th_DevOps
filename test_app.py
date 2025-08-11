import pytest
from app import app

@pytest.fixture
def client():
    return app.test_client()

def test_index_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"<h1>\xeb\xb0\xa9\uba85\ub85d</h1>" in resp.data  # "방명록" UTF-8 인코딩 확인
    assert b"No messages" in resp.data

def test_post_message(client):
    # 메시지 등록
    resp = client.post("/", data={"name": "hanwoo", "message": "hello"}, follow_redirects=True)
    assert resp.status_code == 200
    # 등록한 내용이 페이지에 표시되는지 확인
    assert b"hanwoo" in resp.data
    assert b"hello" in resp.data