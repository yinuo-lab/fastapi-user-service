from pydantic import BaseModel, Field

from pydantic import BaseModel, Field, field_validator

class UserCreate(BaseModel):
    username: str = Field(min_length=2, max_length=50)
    password: str = Field(min_length=6, max_length=128)  # 字符长度先不动
    age: int = Field(ge=0, le=150)

    @field_validator("password")
    @classmethod
    def password_must_fit_bcrypt(cls, v: str) -> str:
        # bcrypt 限制是 72 bytes（utf-8 编码后）
        if len(v.encode("utf-8")) > 72:
            raise ValueError("password too long for bcrypt (max 72 bytes in UTF-8). Use a shorter password.")
        return v
class UserOut(BaseModel):
    id: int
    username: str
    age: int

    model_config = {"from_attributes": True}