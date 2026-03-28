from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.security import hash_password
from app.models.user import Task, User
from app.schemas.user import TaskUpdate


def get_user_by_username(db: Session, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    return db.execute(stmt).scalar_one_or_none()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def list_users(db: Session, skip: int = 0, limit: int = 50) -> list[User]:
    stmt = select(User).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())


def create_user(db: Session, username: str, password: str, age: int) -> User:
    user = User(
        username=username,
        hashed_password=hash_password(password),
        age=age,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user: User, update_data: dict) -> User:
    for field, value in update_data.items():
        setattr(user, field, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user_password(db: Session, user: User, hashed_password: str) -> User:
    user.hashed_password = hashed_password
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_active(db: Session, user: User, is_active: bool) -> User:
    user.is_active = is_active
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_task_crud(
    db: Session,
    user: User,
    title: str,
    description: str | None = None,
) -> Task:
    task = Task(
        title=title,
        description=description,
        status="todo",
        owner_id=user.id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_task_by_owner_id(db: Session, owner_id: int) -> list[Task]:
    stmt = select(Task).where(Task.owner_id == owner_id)
    return list(db.execute(stmt).scalars().all())
from typing import Literal
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.user import Task

from typing import Literal
from sqlalchemy import select

def get_tasks_by_owner(
    db: Session,
    owner_id: int,
    status: Literal["todo", "doing", "done"] | None = None,
    skip: int = 0,
    limit: int = 10,
) -> list[Task]:
    stmt = select(Task).where(Task.owner_id == owner_id)

    if status is not None:
        stmt = stmt.where(Task.status == status)

    stmt = stmt.offset(skip).limit(limit)

    return list(db.execute(stmt).scalars().all())

def get_task_by_id_and_owner(db: Session, task_id: int, owner_id: int) -> Task | None:
    stmt = select(Task).where(Task.id == task_id, Task.owner_id == owner_id)
    return db.execute(stmt).scalar_one_or_none()


def get_task_detail_by_id_and_owner(db: Session, task_id: int, owner_id: int) -> Task | None:
    stmt = (
        select(Task)
        .options(selectinload(Task.owner))
        .where(Task.id == task_id, Task.owner_id == owner_id)
    )
    return db.execute(stmt).scalar_one_or_none()


def delete_task_user_curd(db: Session, task_id: int, current_user: User)->bool:
    task=get_task_by_id_and_owner(db,task_id,current_user.id)
    if task:
        db.delete(task)
        db.commit()
        return True
    else:
        return False

def delete_task_admin_curd(db: Session, task_id: int, current_user: User) ->bool:
    task = db.get(Task, task_id)
    if task:
        db.delete(task)
        db.commit()
        return True
    else:
        return False

def get_task_admin_curd(db: Session, task_id: int)-> type[Task] | None:
    return db.get(Task, task_id)
def update_task(db: Session, task: Task, task_update: TaskUpdate) -> Task:
    update_data = task_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(task, field, value)

    db.add(task)
    db.commit()
    db.refresh(task)
    return task