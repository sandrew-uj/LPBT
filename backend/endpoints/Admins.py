from fastapi import FastAPI, HTTPException
from typing import List, Dict

from Models.admin import AdminDB, Admin

app_admin = FastAPI(
    title="backend_admin"
)


# TODO: добавить эндпоинты

# Endpoint to add an admin
@app_admin.post("/add_admin")
async def add_admin(admin: Admin) -> int:
    admin_dict = admin.dict()
    admin_id = await AdminDB.add_admin(admin_dict)
    return admin_id


# Endpoint to get an admin by admin_id
@app_admin.get("/get_admin/{admin_id}")
async def get_admin(admin_id: int) -> Dict:
    admin = await AdminDB.get_admin_by_id(admin_id)
    if admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    return admin.__dict__


# Endpoint to get all admins
@app_admin.get("/get_all_admins")
async def get_all_admins() -> List[Dict]:
    admins = await AdminDB.get_all_admins()
    return [admin.__dict__ for admin in admins]


# Endpoint to get admin courses by admin_id
@app_admin.get("/get_admin_courses/{admin_id}")
async def get_admin_courses(admin_id: int) -> str:
    courses = await AdminDB.get_admin_courses(admin_id)
    if courses is None:
        raise HTTPException(status_code=404, detail="Admin not found or courses not available")
    return courses


# Endpoint to get admin modules by admin_id
@app_admin.get("/get_admin_modules/{admin_id}")
async def get_admin_modules(admin_id: int) -> str:
    modules = await AdminDB.get_admin_modules(admin_id)
    if modules is None:
        raise HTTPException(status_code=404, detail="Admin not found or modules not available")
    return modules


# Endpoint to get admin groups by admin_id
@app_admin.get("/get_admin_groups/{admin_id}")
async def get_admin_groups(admin_id: int) -> str:
    groups = await AdminDB.get_admin_groups(admin_id)
    if groups is None:
        raise HTTPException(status_code=404, detail="Admin not found or groups not available")
    return groups
