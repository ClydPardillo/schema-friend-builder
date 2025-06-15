
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import user
from app.routes.donor import router as donor_router
from app.routes.favorite import router as favorite_router
from app.routes.campaign import router as campaign_router

app = FastAPI(
    title="MyCause API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

origins = [o.strip() for o in settings.CORS_ORIGINS.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(donor_router, prefix="/donors", tags=["donors"])
app.include_router(favorite_router, tags=["favorites"])
app.include_router(campaign_router, prefix="/campaigns", tags=["campaigns"])

@app.get("/")
def read_root():
    return {"message": "Backend up!"}
