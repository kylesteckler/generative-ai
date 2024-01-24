import os
import aiohttp
import json
from typing import Optional, Dict, Any
from gcloud.aio.auth import Token

from cloud_run_logging import logger
from models import TextGenerationRequest, TextGenerationResponse


class AsyncGemini:
    project_id: str
    region: str
    model_id: str
    session: aiohttp.ClientSession
    url: str
    token: Token
    timeout: float

    @classmethod
    async def create(cls,
        project_id: str,
        session: aiohttp.ClientSession,
        region: str = "us-central1",
        model_id: str = "gemini-pro",
        timeout: float = 60.0
    ) -> "AsyncGemini":
        self = cls()
        self.model_id = model_id
        self.session = session
        self.timeout = timeout
        self.url = cls.full_url(
            root_url=cls.root_url(project_id, region),
            model_path=cls.model_path(model_id)
        )
        self.token = Token(session=self.session, scopes=["https://www.googleapis.com/auth/cloud-platform"])
        return self

    @staticmethod
    def full_url(root_url: str, model_path: str) -> str:
        return os.path.join(root_url, model_path)

    @staticmethod
    def root_url(project_id: str, region: str) -> str:
        return f"https://{region}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{region}"

    @staticmethod
    def model_path(model_id: str):
        return f"publishers/google/models/{model_id}:streamGenerateContent"

    async def _headers(self) -> Dict[str, str]:
        headers = {
            'Content-Type': 'application/json',
        }
        token = await self.token.get()
        headers['Authorization'] = f'Bearer {token}'
        return headers

    async def predict(self, request: TextGenerationRequest) -> TextGenerationResponse:
        headers = await self._headers()
        response = await self.session.post(
            url=self.url,
            json={
                "contents": [{
                    "role": "USER",
                    "parts": [{"text": request.prompt}]
                    }],
                "generationConfig": request.generation_config.model_dump(),
                "safetySettings": [
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": request.safety_settings.sexually_explicit
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": request.safety_settings.hate_speech
                    },
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": request.safety_settings.harassment
                    },
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": request.safety_settings.dangerous_content
                    },
                    ]
            },
            headers=headers,
            timeout=self.timeout
        )

        response_bytes = bytes()
        # Streaming response so iterate through chunks
        async for data, _ in response.content.iter_chunks():
            response_bytes += data

        # Loads byte chunks into list of JSON objects
        response_json_chunks = json.loads(response_bytes)

        response_text = str()
        # Iterate through JSON objects and put together full model response
        for chunk in response_json_chunks:
            candidate = chunk["candidates"][0]
            response_text += candidate["content"]["parts"][0]["text"]

        # Usage metadata is in the last chunk
        return TextGenerationResponse(
            text=response_text,
            input_chars=len(request.prompt),
            output_chars=len(response_text)
        )
