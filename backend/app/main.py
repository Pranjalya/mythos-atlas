"""
MythosAtlas Dynamic Comparative Backend.
FastAPI service orchestrating motif vector retrieval, syncretic graph traversal,
and AI-driven structural comparative synthesis.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes.myths import router as myths_router
from app.routes.compare import router as compare_router

app = FastAPI(
    title="MythosAtlas API",
    description="Dynamic Spatio-Temporal Folklore Atlas & Comparative Knowledge Engine",
    version="1.0.0",
)

# CORS configuration for client origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:4173",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "https://mythos-atlas.pages.dev",
        "https://mythos-atlas-three.vercel.app",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(myths_router)
app.include_router(compare_router)


@app.get("/health", tags=["system"])
def health_check():
    return {
        "status": "healthy",
        "service": "MythosAtlas Dynamic Knowledge Engine",
        "version": "1.0.0",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
