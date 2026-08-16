import os
from typing import Generator

import pytest
from playwright.sync_api import Playwright, APIRequestContext

from services.BaseService import api_request_context


def test_base_service(api_request_context: APIRequestContext) -> None:
    # Example test to verify the API request context is working
    response = api_request_context.get("channels")
    assert response.status == 200
    data = response.json()
    assert isinstance(data, list)  # Assuming the endpoint returns a list of channels