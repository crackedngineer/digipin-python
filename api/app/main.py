from app.routes.v1.routes import router as v1_routers
from fastapi import FastAPI

app = FastAPI(
    title="Digipin Pro API",
    version="1.0.0",
    description="API for encoding/decoding DIGIPINs using the digipin-python library.",
)
app.include_router(v1_routers, prefix="/api/v1")


@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Welcome to the DIGIPIN API. Go to /docs for API documentation."}


@app.get("/healthz", summary="Health check endpoint", tags=["Health"])
async def healthz():
    """
    Health check endpoint to indicate if the application is running.
    Returns a 200 OK status with a simple message.
    """
    return {"status": "healthy"}


@app.get("/readz", summary="Readiness check endpoint", tags=["Health"])
async def readz():
    """
    Readiness check endpoint to indicate if the application is ready to serve requests.
    Returns a 200 OK status with a simple message.
    """
    return {"status": "ready"}
