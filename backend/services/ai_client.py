from openai import OpenAI
import os
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError
from openai import (
    APIConnectionError,
    APITimeoutError,
    RateLimitError,
    AuthenticationError,
    BadRequestError             
)

import time
import logging

load_dotenv()
base_url = "https://parley.api.mit.edu/v1"
parley_api_key = os.getenv("PARLEY_API_KEY")
model = "openai/gpt-5"

client = OpenAI(
    api_key=parley_api_key,
    base_url=base_url
)
logger = logging.getLogger(__name__)
def call_model(messages: list[dict], output_schema: type[BaseModel], max_retries: int = 3) -> BaseModel:
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": output_schema.__name__,
                        "schema": output_schema.model_json_schema()
                    }
                }
            )
        except (APIConnectionError, APITimeoutError, RateLimitError) as e:
            logger.warning(f"Retryable error on attempt {attempt + 1}: {e}")
            if attempt == max_retries:
                raise   
            time.sleep(2 ** attempt)  

        except (AuthenticationError, BadRequestError) as e:
            logger.error(f"Non-retryable error: {e}")
            raise 
        content = response.choices[0].message.content
        if not content:
            raise ValueError("No content returned from model")
        try:
            return output_schema.model_validate_json(content)
        except ValidationError as e:
            logger.error(f"Model output didn't match schema: {e}")
            raise
        