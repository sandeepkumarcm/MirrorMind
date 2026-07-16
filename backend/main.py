from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ADD THESE IMPORTS
from backend.routes import video_routes, audio_routes

app = FastAPI(title="MirrorMind API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this later for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ADD THESE TWO LINES
app.include_router(video_routes.router)
app.include_router(audio_routes.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
