from random import randint
from models.reqres import Reqres, ResponseCreateUserData
from schemas.reqres import response_create_user
from pytest_voluptuous import S
from datetime import datetime, timezone


def test_create_user(env):
    expected_response_create_user = ResponseCreateUserData(
        name="morpheus", job="leader", id="506", created_at=str(datetime.now(timezone.utc)))

    result_response_create_user = Reqres(env).create_user(user_id=randint(0, 50))

    assert result_response_create_user.json == expected_response_create_user.json


def test_response_create_user(env, reqresin):
    response = Reqres(env).create_user(user_id=randint(0, 50))
    assert S(response_create_user) == response.json