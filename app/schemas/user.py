from pydantic import BaseModel, ConfigDict, Field, field_validator


class UserCreate(BaseModel):
    username: str = Field(min_length=2, max_length=50)
    password: str = Field(min_length=6, max_length=128)
    age: int = Field(ge=0, le=150)


class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=2, max_length=50)
    age: int | None = Field(default=None, ge=0, le=150)


class PasswordChange(BaseModel):
    old_password: str = Field(min_length=6, max_length=128)
    new_password: str = Field(min_length=6, max_length=128)


class UserActiveUpdate(BaseModel):
    is_active: bool


class UserOut(BaseModel):
    id: int
    username: str
    age: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class sorted(arr, key=lambda x: x[0])UserSimpleOut(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)


class TaskOut(BaseModel):
    id: int
    title: str
    description: str | None
    status: str
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class TaskDetailOut(BaseModel):
    id: int
    title: str
    description: str | None
    status: str
    owner_id: int
    owner: UserSimpleOut

    model_config = ConfigDict(from_attributes=True)


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    status: str | None = Field(default=None, max_length=20)

    @field_validator("status")
    @classmethod
    def status_must_fit_menu(cls, value: str | None) -> str | None:
        if value is None:
            return value
        if value not in ["todo", "doing", "done"]:
            raise ValueError("status must be one of: todo, doing, done")
        return value