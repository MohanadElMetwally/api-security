from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from api_security.api.main import router
from api_security.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=f"{settings.PROJECT_NAME} Project",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}},
    default_response_class=ORJSONResponse,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(router, prefix=settings.API_V1_STR)
