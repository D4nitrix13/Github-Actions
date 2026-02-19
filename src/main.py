from typing import Dict, List
from uuid import uuid4
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr

app: FastAPI = FastAPI()

# -----------------------------
# In-Memory Storage (Fake DB)
# -----------------------------
fake_users_db: Dict[str, dict] = {}


# -----------------------------
# Schemas
# -----------------------------
class UserCreate(BaseModel):
    name: str
    email: EmailStr


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None


class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr


# -----------------------------
# Root
# -----------------------------
@app.get("/")
async def read_root() -> Dict[str, str]:
    return {"Hello": "World"}


# -----------------------------
# CREATE
# -----------------------------
@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    user_id = str(uuid4())

    fake_users_db[user_id] = {
        "id": user_id,
        "name": user.name,
        "email": user.email,
    }

    return fake_users_db[user_id]


# -----------------------------
# READ ALL
# -----------------------------
@app.get("/users", response_model=List[UserResponse])
async def get_users():
    return list(fake_users_db.values())


# -----------------------------
# READ ONE
# -----------------------------
@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    user = fake_users_db.get(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user


# -----------------------------
# UPDATE
# -----------------------------
@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user_update: UserUpdate):
    user = fake_users_db.get(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if user_update.name is not None:
        user["name"] = user_update.name

    if user_update.email is not None:
        user["email"] = user_update.email

    fake_users_db[user_id] = user

    return user


# -----------------------------
# DELETE
# -----------------------------
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    if user_id not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    del fake_users_db[user_id]
