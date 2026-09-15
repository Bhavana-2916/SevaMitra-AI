from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import chat

app = FastAPI(title="SevaMitra AI Backend")

# Local development CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api")


@app.get("/")
def root():
    return {"status": "SevaMitra backend running"}


@app.get("/health")
def health():
    return {"status": "ok"}