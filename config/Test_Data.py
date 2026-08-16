import os
from pathlib import Path
from typing import Optional


# Project root directory
project_root = Path(__file__).resolve().parent.parent


# Test data paths
test_data_path = {
    "test_module": {
        "test_subModule": {
            "user_data": project_root / "data" / "user_data.json",
            "post_data": project_root / "data" / "post_data.json",
            "comment_data": project_root / "data" / "comment_data.json",
            "basic": project_root / "data" / "module" / "TestFile.csv",
        }
    }
}


def get_test_data_path(
    service: str,
    module: str,
    test_type: str = "basic",
    env_var: Optional[str] = None,
) -> str:

    # Environment variable override
    if env_var:
        custom_path = os.getenv(env_var)

        if custom_path:
            custom_path = Path(custom_path)

            if not custom_path.is_absolute():
                custom_path = project_root / custom_path

            return str(custom_path)

    # Navigate through nested test-data configuration
    try:
        service_path = test_data_path[service]
        module_path = service_path[module]
        related_path = module_path[test_type]

    except KeyError as e:
        raise KeyError(
            f"Test data path not found: "
            f"service={service}, "
            f"module={module}, "
            f"test_type={test_type}, "
            f"missing_key={e}"
        ) from e

    return str(related_path)