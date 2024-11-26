from fastapi import FastAPI
from src.modules.caption.handler.caption_handler import router as caption_router
from src.modules.auth.handler.auth_handler import router as auth_router
from src.config.database_config import Base,engine
from src.modules.profile.handler.profile_handler import router as profile_router
from src.middleware.auth_verify_middleware import AuthVerificationMiddleware
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)
from fastapi.openapi.docs import get_swagger_ui_html
app = FastAPI(
    title="Carla API",
    description="This is a sample API for demonstrating FastAPI",
    version="1.0.0",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,
        "docExpansion": "none"
    }
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific origins for production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Your API",
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1,
            "bearerFormat": "JWT",
            "withCredentials": True
        }
    )
app.include_router(auth_router,prefix="")
app.include_router(caption_router,prefix="/caption")
app.include_router(profile_router,prefix='/profile')
app.add_middleware(AuthVerificationMiddleware)