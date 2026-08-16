from typing import Generator
import pytest
from playwright.sync_api import Playwright, APIRequestContext
from config.Setting import settings, EnvironmentConfig

config = settings.get_config()

API_TOKEN = config.get('auth_token')
CLIENT_ID = config.get('client_id')
Base_URL = EnvironmentConfig.get_config(settings.env)


@pytest.fixture(scope="session")
def api_request_context(
    playwright: Playwright,
) -> Generator[APIRequestContext, None, None]:

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {API_TOKEN}",
        "Client_id": CLIENT_ID
    }

    request_context = playwright.request.new_context(
        base_url=Base_URL["API_URL"],
        ignore_https_errors=True
    )

    print(Base_URL["API_URL"])
    yield request_context
    request_context.dispose()