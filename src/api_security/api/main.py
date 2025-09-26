from fastapi import APIRouter

from api_security.api.routes import login, notes, users

router = APIRouter()

routes = [
    {"router": login.router, "prefix": "/login", "tags": ["login"]},
    {"router": users.router, "prefix": "/users", "tags": ["users"]},
    {"router": notes.router, "prefix": "/notes", "tags": ["notes"]},
]


for route in routes:
    router.include_router(**route)
