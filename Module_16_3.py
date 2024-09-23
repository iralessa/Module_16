from fastapi import FastAPI, Path
from typing import Annotated
app = FastAPI()

users = {'1': 'Имя: Example, возраст: 18'}

# 1. GET запрос, возвращает всех пользователей
@app.get("/users")
async def get_users()-> dict:
    return users

# 2. POST запрос для добавления нового пользователя
@app.post("/user/{username}/{age}")
async def add_user(username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", example="UrbanUser")],
    age: Annotated[int, Path(ge=18, le=120, description="Enter age", example=24)])-> str:
    new_id = str(max(map(int, users.keys())) + 1)
    users[new_id] = f"Имя: {username}, возраст: {age}"
    return f"User {new_id} is registered"

# 3. PUT запрос для обновления пользователя
@app.put("/user/{user_id}/{username}/{age}")
async def update_user(
    user_id: Annotated[int, Path(ge=1, le=100, description="Enter User ID", example=1)],
    username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", example="UrbanUser")],
    age: Annotated[int, Path(ge=18, le=120, description="Enter age", example=24)]
) -> str:
    if str(user_id) in users:
        users[str(user_id)] = f"Имя: {username}, возраст: {age}"
        return f"User {user_id} has been updated"
    return f"User {user_id} not found"

# 4. DELETE запрос для удаления пользователя
@app.delete("/user/{user_id}")
async def delete_user(user_id: str)-> str:
    if user_id in users:
        del users[user_id]
        return f"User {user_id} has been deleted"
    return f"User {user_id} not found"


