import os
from enum import Enum
from typing import Dict, Any


class Environment(str, Enum):
    LOCAL = "local"
    DEVELOPMENT = "development"
    PRODUCTION = "production"


class EnvironmentConfig:
    config = {
        Environment.LOCAL: {
            # API endpoints
            "DATABASE_URL": "sqlite:///./local.db",
            "API_URL": "https://testwebapp-4bqh.onrender.com/Channel/channels",

            # kafka and RabbitMQ settings can be added here

            # Test configuration
            "precision_percentage": 0.1,
            "timeout_seconds": 30,
            "retry_delay_seconds": 1,
            "retry_attempts": 3,
            "poll_wait_count": 5,
            "poll_wait_seconds": 2,
            "username": "local_user",
            "password": "local_pass"
        },

        Environment.DEVELOPMENT: {
            "DATABASE_URL": "postgresql://dev_user:dev_pass@localhost/dev_db",
            "API_URL": "https://testwebapp-4bqh.onrender.com/Channel/channels",
            "precision_percentage": 0.1,
            "timeout_seconds": 30,
            "retry_delay_seconds": 1,
            "retry_attempts": 3,
            "poll_wait_count": 5,
            "poll_wait_seconds": 2,
            "username": "dev_user",
            "password": "dev_pass"
        },

        Environment.PRODUCTION: {
            "DATABASE_URL": "postgresql://prod_user:prod_pass@localhost/prod_db",
            "API_URL": "https://testwebapp-4bqh.onrender.com/Channel/",
            "precision_percentage": 0.1,
            "timeout_seconds": 30,
            "retry_delay_seconds": 1,
            "retry_attempts": 3,
            "poll_wait_count": 5,
            "poll_wait_seconds": 2,
            "username": "prod_user",
            "password": "prod_pass"
        }
    }

    @classmethod
    def get_config(cls, env: Environment) -> Dict[str, Any]:
        return cls.config.get(
            env,
            cls.config[Environment.LOCAL]
        )  # Default to LOCAL if env not found


class Setting:
    """Global setting instance"""

    def __init__(self):
        env_name = os.getenv("Test_Env", "local").lower()

        try:
            self.env = Environment(env_name)
        except ValueError:
            self.env = Environment.LOCAL  # Default to LOCAL if invalid environment variable

    def get_config(self) -> Dict[str, Any]:
        config = EnvironmentConfig.get_config(self.env)
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