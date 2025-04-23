from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.claims import router as claim_router

app = FastAPI(title="SDI Claim Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(claim_router, prefix="/api/claims")
