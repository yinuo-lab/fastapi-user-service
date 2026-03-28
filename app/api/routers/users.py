from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_current_admin, get_db
from app.core.security import hash_password, verify_password
from app.crud.user import (
    create_task_crud,
    get_task_by_id_and_owner,
    get_task_by_owner_id,
    get_task_detail_by_id_and_owner,
    get_user_by_id,
    get_user_by_username,
    list_users,
    update_active,
    update_task,
    update_user,
    update_user_password, get_tasks_by_owner, delete_task_admin_curd, delete_task_user_curd, delete_task_admin_curd,
    delete_task_user_curd, get_task_admin_curd,
)
from app.models.user import User, Task
from app.schemas.user import (
    PasswordChange,
    TaskCreate,
    TaskDetailOut,
    TaskOut,
    TaskUpdate,
    UserActiveUpdate,
    UserOut,
    UserUpdate,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserOut)
def read_current_user(
    current_user: User = Depends(get_current_active_user),
):
    return current_user


@router.patch("/me", response_model=UserOut)
def update_current_user(
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    update_data = user_in.model_dump(exclude_unset=True)

    if "username" in update_data:
        existing_user = get_user_by_username(db, update_data["username"])
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )

    return update_user(db, current_user, update_data)


@router.patch("/me/password")
def change_password(
    password_change: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    if not verify_password(password_change.old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old password is incorrect",
        )

    if password_change.old_password == password_change.new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be different from old password",
        )

    new_hashed_password = hash_password(password_change.new_password)
    update_user_password(db, current_user, new_hashed_password)
    return {"message": "Password updated successfully"}


@router.post("/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return create_task_crud(
        db=db,
        user=current_user,
        title=payload.title,
        description=payload.description,
    )


from typing import Literal
from fastapi import Query

@router.get("/tasks", response_model=list[TaskOut])
def read_tasks(
    status: Literal["todo", "doing", "done"] | None = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return get_tasks_by_owner(
        db=db,
        owner_id=current_user.id,
        status=status,
        skip=skip,
        limit=limit,
    )
@router.get("/tasks/owner_id", response_model=list[TaskOut])
def read_tasks(
    status: Literal["todo", "doing", "done"] | None = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return get_tasks_by_owner(
        db=db,
        owner_id=current_user.id,
        status=status,
        skip=skip,
        limit=limit,
    )
@router.patch("/tasks/delete/admin/{task_id}",response_model=bool)
def delete_task_admin_router(
    task_id:int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    task =delete_task_admin_curd(db,task_id,current_admin)
    if  not task :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return  True

@router.patch("/tasks/delete/user/{task_id}",response_model=bool)
def delete_task_user_router(
    task_id:int,
    db: Session = Depends(get_db),
    user=Depends(get_current_active_user)
):
    ok =delete_task_user_curd(db,task_id,user)
    if  not ok :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return  True
@router.get("/tasks/admin/read/{task_id}", response_model=TaskOut)
def get_task_admin(
    task_id:int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_admin)
):
    task=get_task_admin_curd(db,task_id)
    if  not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return  task
@router.get("/tasks/admin/read_detail/{task_id}", response_model=TaskDetailOut)
def get_task_admin_detail(
    task_id:int,
    db: Session = Depends(get_db),
    user:User=Depends(get_current_admin)
):
    task=get_task_admin_curd(db,task_id)
    if  not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return  task
@router.get("/tasks/{task_id}", response_model=TaskOut)
def read_task_by_task_id(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    task = get_task_by_id_and_owner(db, task_id, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


@router.get("/tasks/{task_id}/detail", response_model=TaskDetailOut)
def read_task_detail(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    task = get_task_detail_by_id_and_owner(db, task_id, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


@router.patch("/tasks/{task_id}", response_model=TaskOut)
def update_current_task(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    task = get_task_by_id_and_owner(db, task_id, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return update_task(db, task, task_in)


@router.get("", response_model=list[UserOut])
def users(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    return list_users(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserOut)
def user_detail(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.patch("/admin/{user_id}/active")
def change_active(
    user_id: int,
    payload: UserActiveUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    user_to_change = get_user_by_id(db, user_id)
    if not user_to_change:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    update_active(db, user_to_change, payload.is_active)
    return {"message": "User active status changed successfully"}