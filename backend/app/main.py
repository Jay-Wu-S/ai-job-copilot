from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_match import router as match_router
from app.api.routes_rag import router as rag_router
from app.api.routes_upload import router as upload_router
from app.api.routes_classifier import router as classifier_router

app = FastAPI(
    title="AI Job Copilot API",
    version="0.5.0",
    description="Backend API for resume-job matching, PDF resume upload, Wikipedia-based Q&A, and TensorFlow skill classification."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(match_router, prefix="/api")
app.include_router(rag_router, prefix="/api")
app.include_router(upload_router, prefix="/api")
app.include_router(classifier_router, prefix="/api")


@app.get("/")
def root():
    return {"message": "AI Job Copilot backend is running"}