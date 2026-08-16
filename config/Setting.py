import os
from enum import Enum
from typing import Dict, Any


class Environment(str, Enum):
    LOCAL = "local"
    QA = "qa"
    PRODUCTION = "production"


class EnvironmentConfig:

    config = {

        Environment.LOCAL: {
            "DATABASE_URL": "sqlite:///./local.db",
            "API_URL": "http://127.0.0.1:8000/Channel/",

            "precision_percentage": 0.1,
            "timeout_seconds": 30,
            "retry_delay_seconds": 1,
            "retry_attempts": 3,
            "poll_wait_count": 5,
            "poll_wait_seconds": 2,
        },

        Environment.QA: {
            "DATABASE_URL": "",
            "API_URL": "https://testwebapp-qa-4bqh.onrender.com/Channel/",

            "precision_percentage": 0.1,
            "timeout_seconds": 30,
            "retry_delay_seconds": 1,
            "retry_attempts": 3,
            "poll_wait_count": 5,
            "poll_wait_seconds": 2,
        },

        Environment.PRODUCTION: {
            "DATABASE_URL": "",
            "API_URL": "https://testwebapp-4bqh.onrender.com/Channel/",

            "precision_percentage": 0.1,
            "timeout_seconds": 30,
            "retry_delay_seconds": 1,
            "retry_attempts": 3,
            "poll_wait_count": 5,
            "poll_wait_seconds": 2,
        },
    }

    @classmethod
    def get_config(cls, env: Environment) -> Dict[str, Any]:
        return cls.config.get(
            env,
            cls.config[Environment.LOCAL]
        )


class Setting:

    def __init__(self):
        env_name = os.getenv("Test_Env", "local").lower()

        try:
            self.env = Environment(env_name)
        except ValueError:
            self.env = Environment.LOCAL

    def get_config(self) -> Dict[str, Any]:

        config = EnvironmentConfig.get_config(self.env).copy()

        config["auth_token"] = os.getenv(
            "AUTH_TOKEN",
            os.getenv("Auth_bearer")
        )

        config["client_id"] = os.getenv(
            "CLIENT_ID",
            os.getenv("Client_id")
        )

        return config


settings = Setting()