import os
from pathlib import Path

project_root = Path(__file__).parent.parent

test_data_path = {
    'test_module': {
        'test_subModule': {
            "user_data": project_root / "data" / "user_data.json",
            "post_data": project_root / "data" / "post_data.json",
            "comment_data": project_root / "data" / "comment_data.json",
            "basic": project_root / "data" / "module" / "TestFile.csv",
        }
    }
}


def get_test_data_path(service: str, module: str, test_type: str = 'basic', env_var: str = None) -> str:

    if env_var and os.getenv(env_var):
        # use env variable override
        custom_path = os.getenv(env_var)

        if not Path(custom_path).is_absolute():
            return str(project_root / custom_path)

        return custom_path

    # Navigate through nested directory
    try:
        service_path = test_data_path[service]
        module_path = service_path[module]
        related_path = module_path[test_type]

    except KeyError as e:
        raise KeyError(
            f"Test data path not found services = {service}, "
            f"module= {module}, test_type= {test_type}"
            f"Missing key:{e}"
        )

    return str(project_root / related_path)