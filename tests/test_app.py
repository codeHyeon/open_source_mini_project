from app import app

# 메인 페이지("/")가 정상적으로 열리는지 테스트
def test_index_page():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200

# 메모 추가 페이지("/add")가 정상적으로 열리는지 테스트
def test_add_page():
    client = app.test_client()
    response = client.get("/add")
    assert response.status_code == 200

# 메모 삭제 페이지("/delete")가 정상적으로 열리는지 테스트
def test_delete_page():
    client = app.test_client()
    response = client.get("/delete")
    assert response.status_code == 200

# 메모 추가
def test_add_memo():
    client = app.test_client()

    response = client.post("/add", data={"memo": "hello"})

    # 정상적으로 redirect 되는지 확인
    assert response.status_code == 302

# 메모 목록 보기
def test_memo_appears_in_list():
    client = app.test_client()

    client.post("/add", data={"memo": "hello"})
    response = client.get("/")

    assert b"hello" in response.data

# 메모 삭제
def test_delete_memo():
    client = app.test_client()

    client.post("/add", data={"memo": "bye"})
    client.get("/remove/0")

    response = client.get("/")

    assert b"bye" not in response.data