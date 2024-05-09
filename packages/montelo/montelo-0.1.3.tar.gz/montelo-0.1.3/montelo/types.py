from typing import Optional, Dict, Any, Union

import httpx
from httpx import Timeout
from pydantic import BaseModel, Field, HttpUrl


class OpenAIClientConfig(BaseModel):
    api_key: Optional[str] = None
    organization: Optional[str] = None
    project: Optional[str] = None
    base_url: Union[str, HttpUrl, None] = None
    timeout: Union[
        float, Timeout, None] = None
    max_retries: int | None = None
    default_headers: Optional[Dict[str, str]] = None
    default_query: Optional[Dict[str, Any]] = None
    http_client: Optional[httpx.Client] = None
    _strict_response_validation: bool = False

    model_config = {
        "arbitrary_types_allowed": True
    }


class MonteloClientOptions(BaseModel):
    api_key: Optional[str] = Field(None)
    base_url: Optional[str] = Field(None)


class TraceParams(BaseModel):
    name: str
    user_id: Optional[str] = Field(None)
    extra: Optional[Dict[str, Any]] = None
