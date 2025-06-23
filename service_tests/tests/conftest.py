import json
from pathlib import Path

import dotenv
import pytest
from sqlmodel import Session, select, SQLModel
from service_tests.app.database import engine
import requests
from service_tests.app.models.User import UserData
import os
import shutil

BASE_URL = "http://127.0.0.1:8002"


@pytest.fixture(scope="session", autouse=True)
def envs():
    dotenv.load_dotenv()


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

@pytest.fixture(scope="session", autouse=True)
def create_tables():
    SQLModel.metadata.create_all(engine)

@pytest.fixture
def test_data_users():
    return [
        {
            "id": 1,
            "email": "george.bluth@reqres.in",
            "first_name": "George",
            "last_name": "Bluth",
            "avatar": "https://reqres.in/img/faces/1-image.jpg"
        },
        {
            "id": 2,
            "email": "janet.weaver@reqres.in",
            "first_name": "Janet",
            "last_name": "Weaver",
            "avatar": "https://reqres.in/img/faces/2-image.jpg"
        },
        {
            "id": 3,
            "email": "emma.wong@reqres.in",
            "first_name": "Emma",
            "last_name": "Wong",
            "avatar": "https://reqres.in/img/faces/3-image.jpg"
        },
        {
            "id": 4,
            "email": "eve.holt@reqres.in",
            "first_name": "Eve",
            "last_name": "Holt",
            "avatar": "https://reqres.in/img/faces/4-image.jpg"
        },
        {
            "id": 5,
            "email": "charles.morris@reqres.in",
            "first_name": "Charles",
            "last_name": "Morris",
            "avatar": "https://reqres.in/img/faces/5-image.jpg"
        },
        {
            "id": 6,
            "email": "tracey.ramos@reqres.in",
            "first_name": "Tracey",
            "last_name": "Ramos",
            "avatar": "https://reqres.in/img/faces/6-image.jpg"
        },
        {
            "id": 7,
            "email": "michael.lawson@reqres.in",
            "first_name": "Michael",
            "last_name": "Lawson",
            "avatar": "https://reqres.in/img/faces/7-image.jpg"
        },
        {
            "id": 8,
            "email": "lindsay.ferguson@reqres.in",
            "first_name": "Lindsay",
            "last_name": "Ferguson",
            "avatar": "https://reqres.in/img/faces/8-image.jpg"
        },
        {
            "id": 9,
            "email": "tobias.funke@reqres.in",
            "first_name": "Tobias",
            "last_name": "Funke",
            "avatar": "https://reqres.in/img/faces/9-image.jpg"
        },
        {
            "id": 10,
            "email": "byron.fields@reqres.in",
            "first_name": "Byron",
            "last_name": "Fields",
            "avatar": "https://reqres.in/img/faces/10-image.jpg"
        },
        {
            "id": 11,
            "email": "george.edwards@reqres.in",
            "first_name": "George",
            "last_name": "Edwards",
            "avatar": "https://reqres.in/img/faces/11-image.jpg"
        },
        {
            "id": 12,
            "email": "rachel.howell@reqres.in",
            "first_name": "Rachel",
            "last_name": "Howell",
            "avatar": "https://reqres.in/img/faces/12-image.jpg"
        }
    ]


@pytest.fixture(scope='module', autouse=False)
def clear_database():
    with Session(engine) as session:
        statement = select(UserData)
        users = session.exec(statement).all()
        for user in users:
            session.delete(user)
        session.commit()


@pytest.fixture(scope="module")
def fill_test_data(reqresin, clear_database):
    clear_database
    with open(Path(__file__).parent.parent.parent.joinpath("users.json").absolute()) as f:
        test_data_users = json.load(f)
    api_users = []
    for user in test_data_users:
        api_users.append(UserData(**reqresin.post(f"/api/users", json=user).json()))
    user_ids = [user.id for user in api_users]

    yield user_ids

    for user_id in user_ids:
        requests.delete(f"{base_url}/api/users/{user_id}")


@pytest.fixture
def users(reqresin):
    response = reqresin.get("/api/users/")
    return response.json()


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
