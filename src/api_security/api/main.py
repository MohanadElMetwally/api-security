from fastapi import APIRouter

from api_security.api.routes import login, notes, users, utils

router = APIRouter()

routes = [
    {"router": login.router, "tags": ["login"]},
    {"router": users.router, "prefix": "/users", "tags": ["users"]},
    {"router": notes.router, "prefix": "/notes", "tags": ["notes"]},
    {"router": utils.router, "prefix": "/utils", "tags": ["utils"]},
]


for route in routes:
    router.include_router(**route)
