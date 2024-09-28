from fastapi import FastAPI, status, Body, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Пустой список для хранения пользователей
users = []

class User(BaseModel):
    id: int
    username: str
    age: int

# 1. GET запрос, возвращает всех пользователей
@app.get("/users")
def get_all_messages() -> List[User]:
    return users

# 2. POST запрос для добавления нового пользователя
@app.post("/user/{username}/{age}")
async def add_user(username: str, age: int) -> users:
    # Вычисляем ID для нового пользователя
    if len(users) > 0:  # Проверяем, есть ли пользователи в списке
        last_user = users[-1]  # Берем последнего пользователя
        new_id = last_user.id + 1  # Увеличиваем его ID на 1
    else:
        new_id = 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user

# 3. PUT запрос для обновления пользователя
@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: int, username: str, age: int):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    #  Если пользователя не нашли, выбрасываем ошибку
    raise HTTPException(status_code=404, detail="User was not found")

# 4. DELETE запрос для удаления пользователя
@app.delete("/user/{user_id}")
async def delete_user(user_id: int):
    # Проходим по списку пользователей
    for user in users:
        # Если нашли пользователя с нужным id, удаляем его из списка
        if user.id == user_id:
            users.remove(user)
            return user
    # Если пользователя не нашли, выбрасываем ошибку
    raise HTTPException(status_code=404, detail="User was not found")

