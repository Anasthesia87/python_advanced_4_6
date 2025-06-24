import json
from http import HTTPStatus
import time

from app.models.UserService import UserService
from utils.base_session import BaseSession
from config import Server

import dotenv
import pytest
from sqlmodel import Session, select, SQLModel
from app.database.engine import engine
from app.models.User import UserData
import logging

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


@pytest.fixture(scope="class")
def fill_test_data(env, clear_database):
    clear_database
    with open("tests/users.json") as f:
        test_data_users = json.load(f)
    api_users = []
    for user in test_data_users:
        response = UserService(env).create_user(user)
        api_users.append(response.json())

    print(api_users)
    yield api_users

    for user in api_users:
        response = UserService(env).delete_user(user['id'])


@pytest.fixture
def users(env):
    response = UserService(env).get_users()
    assert response.status_code == HTTPStatus.OK
    return response.json()

def pytest_addoption(parser):
    parser.addoption("--env", default="dev")
    logging.info("parser")

@pytest.fixture(scope="session")
def env(request):
    e = request.config.getoption("--env", default="dev")
    logging.info(f"env : {e}")
    return e

@pytest.fixture(scope='session')
def servicein(env):
    print(f"🔍 Передаём в Server: {env}")
    time.sleep(5)
    with BaseSession(base_url=Server(env).service) as session:
        yield session
