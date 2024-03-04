from fastapi import FastAPI, HTTPException
from typing import List, Dict

from Models.user import UserDB, User

app_user = FastAPI(
    title="backend_user"
)


# Endpoint to add a user
@app_user.post("/add_user")
async def add_user(user: User) -> int:
    user_dict = user.dict()
    user_id = await UserDB.add_user(user_dict)
    return user_id


# Endpoint to get a user by user_id
@app_user.get("/get_user/{user_id}")
async def get_user(user_id: int) -> Dict:
    user = await UserDB.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user.__dict__


# Endpoint to get all users
@app_user.get("/get_all_users")
async def get_all_users() -> List[Dict]:
    users = await UserDB.get_all_users()
    return [user.__dict__ for user in users]


# Endpoint to get a user by name and surname
@app_user.get("/get_user_by_name_surname")
async def get_user_by_name_surname(name: str, surname: str) -> Dict:
    user = await UserDB.get_user_by_name_surname(name, surname)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user.__dict__
