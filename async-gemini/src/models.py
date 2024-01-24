from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, Dict, Any


class SafetyThresholdEnum(str, Enum):
    BLOCK_NONE = "BLOCK_NONE"
    BLOCK_LOW_AND_ABOVE = "BLOCK_LOW_AND_ABOVE"
    BLOCK_MEDIUM_AND_ABOVE = "BLOCK_MEDIUM_AND_ABOVE"
    BLOCK_ONLY_HIGH = "BLOCK_ONLY_HIGH"

class SafetySettings(BaseModel):
    sexually_explicit: SafetyThresholdEnum = SafetyThresholdEnum.BLOCK_MEDIUM_AND_ABOVE
    hate_speech: SafetyThresholdEnum = SafetyThresholdEnum.BLOCK_MEDIUM_AND_ABOVE
    harassment: SafetyThresholdEnum = SafetyThresholdEnum.BLOCK_MEDIUM_AND_ABOVE
    dangerous_content: SafetyThresholdEnum = SafetyThresholdEnum.BLOCK_MEDIUM_AND_ABOVE

class GenerationConfig(BaseModel):
    temperature: float = Field(default=0.9, ge=0.0, le=1.0, serialization_alias='temperature')
    max_output_tokens: int = Field(default=8192, ge=0, le=8192, serialization_alias='maxOutputTokens')
    top_k: int = Field(default=32, ge=0, le=40, serialization_alias='topK')
    top_p: float = Field(default=1.0, ge=0.0, le=1.0, serialization_alias='topP')

class TextGenerationRequest(BaseModel):
    prompt: str
    generation_config: GenerationConfig = GenerationConfig()
    safety_settings: SafetySettings = SafetySettings()

class TextGenerationResponse(BaseModel):
    # Number of input/output characters included in response because gemini is priced per 1k chars
    text: str
    input_chars: int # num input chars
    output_chars: int # num output chars
