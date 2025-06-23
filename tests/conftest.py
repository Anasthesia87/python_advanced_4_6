import os
import shutil
import pytest
pytest_plugins = ['fixture_sessions']


def pytest_addoption(parser):
    parser.addoption("--env", default="dev")


@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")

@pytest.fixture(scope='session', autouse=True)
def clean_allure_results():
    allure_dir = 'allure-results'
    if os.path.exists(allure_dir):
        shutil.rmtree(allure_dir)
        print(f"Директория '{allure_dir}' очищена.")
    os.makedirs(allure_dir, exist_ok=True)