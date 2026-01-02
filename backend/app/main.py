from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import get_settings
from .routers import auth, resources, dashboard, timesheets, ai, teams

settings = get_settings()

app = FastAPI(title=settings.app_name)

origins = [origin.strip() for origin in settings.cors_origins.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(resources.router)
app.include_router(dashboard.router)
app.include_router(timesheets.router)
app.include_router(ai.router)
app.include_router(teams.router)


@app.get("/")
def health():
    return {"status": "ok"}
