import aiohttp
from fastapi import FastAPI, Request, HTTPException
from contextlib import asynccontextmanager

from gemini import AsyncGemini
from models import TextGenerationRequest, TextGenerationResponse
from settings import gcp_settings
from cloud_run_logging import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    # This happens on application startup
    app.aiohttp_session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=1000)) # type: ignore
    app.gemini = await AsyncGemini.create( # type: ignore
        project_id=gcp_settings.PROJECT_ID,
        region=gcp_settings.REGION,
        session=app.aiohttp_session # type: ignore
    ) # type: ignore
    yield

    # This happens on application teardown
    await app.aiohttp_session.close() # type: ignore


app = FastAPI(lifespan=lifespan)

@app.post("/predict")
async def predict(request: Request, generation_request: TextGenerationRequest) -> TextGenerationResponse:
    model: AsyncGemini = request.app.gemini
    try:
        response = await model.predict(request=generation_request)
        return response
    except Exception as e:
        logger.error("Prediction Failed", error=str(e), request=generation_request)
        raise HTTPException(
            status_code=502, 
            detail={"error": {"message": "Gemini prediction failed"}}
        )
