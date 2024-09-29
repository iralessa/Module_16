from fastapi import FastAPI, status, Body, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from fastapi.templating import Jinja2Templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Пустой список для хранения пользователей
users = []

class User(BaseModel):
    id: int = None
    username: str
    age: int

# Главная страница со всеми пользователями
@app.get("/")
def get_all_messages(request: Request)-> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

# Получить одного пользователя по ID
@app.get("/users/{user_id}")
def get_user(request: Request, user_id: int):
    if user_id < 0 or user_id >= len(users):
        raise HTTPException(status_code=404, detail="User not found")
    user = users[user_id]
    return templates.TemplateResponse("users.html", {"request": request, "user": user})

# Добавление нового пользователя
@app.post("/user")
async def add_user(request: Request, username: str = Form(), age: int = Form())-> HTMLResponse:
    # Вычисляем ID для нового пользователя
    if len(users) > 0:
        last_user = users[-1]
        new_id = last_user.id + 1
    else:
        new_id = 1

    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

# Обновление информации о пользователе
@app.put("/user/{user_id}/{username}/{age}")
async def update_user(request: Request, user_id: int, username: str, age: int)-> HTMLResponse:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return templates.TemplateResponse("users.html", {"request": request, "users": users})

    raise HTTPException(status_code=404, detail="User was not found")

# Удаление пользователя
@app.delete("/user/{user_id}")
async def delete_user(request: Request, user_id: int)-> HTMLResponse:
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return templates.TemplateResponse("users.html", {"request": request, "users": users})

    raise HTTPException(status_code=404, detail="User was not found")

