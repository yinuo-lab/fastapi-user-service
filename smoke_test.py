import random
import string
import sys
from typing import Any

import requests

BASE_URL = "http://127.0.0.1:8000"


def rand_suffix(n: int = 6) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=n))


def print_step(title: str) -> None:
    print("\n" + "=" * 20, title, "=" * 20)


def show_response(resp: requests.Response) -> None:
    print("status:", resp.status_code)
    try:
        print("json:", resp.json())
    except Exception:
        print("text:", resp.text)


def assert_status(resp: requests.Response, expected: int, step_name: str) -> None:
    if resp.status_code != expected:
        print(f"\n[FAILED] {step_name}")
        show_response(resp)
        sys.exit(1)


def bearer_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def main() -> None:
    username =f"user_{rand_suffix()}"
    password = "abc123456"
    new_password = "new123456"
    age = 24

    print(f"测试用户: {username}")

    # 1) 注册
    print_step("1. register")
    resp = requests.post(
        f"{BASE_URL}/auth/register",
        json={
            "username": username,
            "password": password,
            "age": age,
        },
        timeout=10,
    )
    show_response(resp)
    assert_status(resp, 201, "register")

    # 2) 登录
    print_step("2. login")
    resp = requests.post(
        f"{BASE_URL}/auth/token",
        data={
            "username": username,
            "password": password,
        },
        timeout=10,
    )
    show_response(resp)
    assert_status(resp, 200, "login")

    token = resp.json()["access_token"]
    headers = bearer_headers(token)

    # 3) 读取当前用户
    print_step("3. /users/me")
    resp = requests.get(
        f"{BASE_URL}/users/me",
        headers=headers,
        timeout=10,
    )
    show_response(resp)
    assert_status(resp, 200, "get current user")

    # 4) 修改个人资料
    print_step("4. PATCH /users/me")
    new_age = 25
    resp = requests.patch(
        f"{BASE_URL}/users/me",
        headers=headers,
        json={"age": new_age},
        timeout=10,
    )
    show_response(resp)
    assert_status(resp, 200, "update current user")

    # 5) 修改密码
    print_step("5. PATCH /users/me/password")
    resp = requests.patch(
        f"{BASE_URL}/users/me/password",
        headers=headers,
        json={
            "old_password": password,
            "new_password": new_password,
        },
        timeout=10,
    )
    show_response(resp)
    assert_status(resp, 200, "change password")

    # 6) 用新密码重新登录
    print_step("6. login with new password")
    resp = requests.post(
        f"{BASE_URL}/auth/token",
        data={
            "username": username,
            "password": new_password,
        },
        timeout=10,
    )
    show_response(resp)
    assert_status(resp, 200, "re-login with new password")

    token = resp.json()["access_token"]
    headers = bearer_headers(token)

    # 7) 创建 task
    print_step("7. POST /users/tasks")
    resp = requests.post(
        f"{BASE_URL}/users/tasks",
        headers=headers,
        json={
            "title": f"task_{rand_suffix()}",
            "description": "this is a smoke test task",
        },
        timeout=10,
    )
    show_response(resp)
    assert_status(resp, 201, "create task")

    task_data: dict[str, Any] = resp.json()
    task_id = task_data["id"]

    # 8) 读取 task 列表
    print_step("8. GET /users/tasks")
    resp = requests.get(
        f"{BASE_URL}/users/tasks",
        headers=headers,
        timeout=10,
    )
    show_response(resp)
    assert_status(resp, 200, "list tasks")

    # 9) 读取单个 task
    print_step("9. GET /users/tasks/{task_id}")
    resp = requests.get(
        f"{BASE_URL}/users/tasks/{task_id}",
        headers=headers,
        timeout=10,
    )
    show_response(resp)
    assert_status(resp, 200, "get task by id")

    # 10) 读取 task detail
    print_step("10. GET /users/tasks/{task_id}/detail")
    resp = requests.get(
        f"{BASE_URL}/users/tasks/{task_id}/detail",
        headers=headers,
        timeout=10,
    )
    show_response(resp)
    assert_status(resp, 200, "get task detail")

    # 11) 更新 task
    print_step("11. PATCH /users/tasks/{task_id}")
    resp = requests.patch(
        f"{BASE_URL}/users/tasks/{task_id}",
        headers=headers,
        json={
            "status": "doing",
            "description": "updated by smoke test",
        },
        timeout=10,
    )
    show_response(resp)
    assert_status(resp, 200, "update task")

    print("\n✅ 全部基础接口已跑通")


if __name__ == "__main__":
    main()