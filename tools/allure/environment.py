import platform
import sys

from config import settings


def create_allure_environment_file():
    items = [f'{key}={value}' for key, value in settings.model_dump().items()]

    system_items = [
        f'os_info={platform.system()}, {platform.version()}',
        f'python_version={sys.version}'
    ]

    properties = '\n'.join(items + system_items)

    with open(
        settings.allure_results_dir.joinpath('environment.properties'),
        'w',
        encoding='utf-8'
    ) as file:
        file.write(properties)
