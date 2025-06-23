from http import HTTPStatus

import pytest
import requests
from app.models.User import UserData
from service_tests.models.reqres import Reqres


@pytest.mark.parametrize("user_id", [13])
def test_user_nonexistent_values(env, user_id):
    result_response_get_user = Reqres(env).get_user({user_id})
    assert result_response_get_user.status_code == HTTPStatus.UNPROCESSABLE_ENTITY



