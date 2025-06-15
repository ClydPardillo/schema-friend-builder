
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import user, campaign, donation

app = FastAPI(title="ClearCause API", version="1.0.0")

origins = [o.strip() for o in settings.CORS_ORIGINS.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(campaign.router, prefix="/campaigns", tags=["campaigns"])
app.include_router(donation.router, prefix="/donations", tags=["donations"])

@app.get("/")
def root():
    return {"message": "ClearCause API running!"}
