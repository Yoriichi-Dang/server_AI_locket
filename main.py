from fastapi import FastAPI
from src.modules.caption.handler.caption_handler import router as caption_router
from src.config.database_config import Base,engine

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Carla API",
    description="This is a sample API for demonstrating FastAPI",
    version="1.0.0"
)
app.include_router(caption_router,prefix="/caption")