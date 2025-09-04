from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.config import get_settings
from backend.app.routers import auth as auth_router
from backend.app.routers import users as users_router
from backend.app.routers import plants as plants_router
from pydantic import Field

settings = get_settings()

app = FastAPI(title=settings.APP_NAME, version=settings.VERSION)

# CORS for mobile app dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health & Version
@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


@app.get("/version")
async def version():
    return {"version": settings.VERSION}

# Mount API v1
api = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)  # sub-app (optional)
app.mount(settings.API_V1_PREFIX, api)  # type: ignore[attr-defined]


api.include_router(auth_router.router)
api.include_router(users_router.router)
api.include_router(plants_router.router)
