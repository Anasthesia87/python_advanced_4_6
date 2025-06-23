from http import HTTPStatus

import pytest

from schemas.reqres import response_get_user
from pytest_voluptuous import S
from models.reqres import Reqres, ResponseGetUserData, ResponseUserData

def test_get_user(env):
    expected_response_get_user = ResponseGetUserData(data=ResponseUserData(
        id=2,
        email="janet.weaver@reqres.in",
        first_name="Janet",
        last_name="Weaver",
        avatar="https://reqres.in/img/faces/2-image.jpg"
    ))

    result_response_get_user = Reqres(env).get_user(2)

    assert result_response_get_user.support_url == expected_response_get_user.support_url
    assert result_response_get_user.json == expected_response_get_user.json

def test_response_get_user(env, reqresin):
    response = Reqres(env).get_user(2)
    assert S(response_get_user) == response.json

@pytest.mark.parametrize("user_id", [-1, 0, "fafaf"])
def test_user_invalid_values(env, user_id):
    result_response_get_user = Reqres(env).get_user({user_id})
    assert result_response_get_user.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

@pytest.mark.parametrize("user_id", [99])
def test_user_nonexistent_values(env, user_id):
    result_response_user_nonexistent_values = Reqres(env).get_user({user_id})
    assert result_response_user_nonexistent_values.status_code == HTTPStatus.NOT_FOUND