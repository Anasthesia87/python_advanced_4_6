from models.reqres import Reqres, ResponseUpdateUserData
from schemas.reqres import response_update_user
from pytest_voluptuous import S

def test_update_user(env):

    expected_response_update_user = ResponseUpdateUserData(data=ResponseUpdateUserData(
        name="morpheus",
        job="zion resident"))

    result_response_update_user = Reqres(env).update_user(2)
    assert result_response_update_user.json == expected_response_update_user.json

def test_response_update_user(env, reqresin):
    response = Reqres(env).update_user(2)
    assert S(response_update_user) == response.json