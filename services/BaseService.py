from typing import Generator
import os
import pytest
from playwright.sync_api import (
    Playwright,
    APIRequestContext,
)

from config.Setting import settings


@pytest.fixture(scope="session")
def api_request_context(
    playwright: Playwright,
) -> Generator[APIRequestContext, None, None]:

    config = settings.get_config()

    api_token = config.get("auth_token")
    client_id = config.get("client_id")

    base_url = config.get("API_URL")

    headers = {
        "Accept": "application/json",
    }

    if api_token:
        if api_token.startswith("Bearer "):
            headers["Authorization"] = api_token
        else:
            headers["Authorization"] = f"Bearer {api_token}"


    if client_id:
        headers["client-id"] = client_id

    request_context = playwright.request.new_context(
        base_url=base_url,
        extra_http_headers=headers,
        ignore_https_errors=True,
    )

    print(f"Environment: {settings.env.value}")
    print(f"Base URL: {base_url}")
    print(f"Headers: {headers}")

    yield request_context

    request_context.dispose()