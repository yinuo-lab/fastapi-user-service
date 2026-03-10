# FastAPI User Service

一个基于 FastAPI 的用户服务项目，用于学习和实践后端开发。

## 当前功能
- 用户注册
- 用户登录
- JWT 检测
- 获取当前用户信息 `/users/me`
- 基础测试

## 技术栈
- FastAPI
- SQLAlchemy
- Pydantic
- JWT
- Pytest

## 项目结构
- `app/` 应用主代码
- `test/` 测试代码
- `requirements.txt` 依赖文件

## 运行方式
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload