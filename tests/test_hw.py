from pydantic import ValidationError

from app.models.User import UserData
from app.models.UserService import UserService
from http import HTTPStatus
import pytest


def test_api_create_user(env):
    body = {
        "email": "valid@example.com",
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "avatar": "https://example.com/avatar.jpg"
    }

    user_service = UserService(env)

    create_response = user_service.create_user(body)
    assert create_response.status_code == 201, f"Не удалось создать пользователя: {create_response.text}"

    new_user = create_response.json()

    values_equal = all(new_user[key] == body[key]
                       for key in body
                       if key in new_user)
    assert values_equal, "Данные пользователя не совпадают с ожидаемыми"

    delete_response = user_service.delete_user(new_user["id"])
    assert delete_response.status_code == 200, f"Не удалось удалить пользователя: {delete_response.text}"


def test_api_get_user_after_create_user(env):
    body = {
        "email": "valid@example.com",
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "avatar": "https://example.com/avatar.jpg"
    }

    user_service = UserService(env)

    create_response = user_service.create_user(body)
    assert create_response.status_code == 201, f"Не удалось создать пользователя: {create_response.text}"
    new_user = create_response.json()

    get_response = user_service.get_user_id(new_user["id"])
    assert get_response.status_code == 200, f"Не удалось получить пользователя: {get_response.text}"
    user_from_api = get_response.json()

    values_equal = all(
        new_user[key] == user_from_api[key]
        for key in new_user
        if key in user_from_api
    )
    assert values_equal, "Данные пользователя не совпадают с ожидаемыми"

    delete_response = user_service.delete_user(new_user["id"])
    assert delete_response.status_code == 200, f"Не удалось удалить пользователя: {delete_response.text}"


def test_api_get_list_users_after_create_user(env, fill_test_data, clear_database):
    user_service = UserService(env)

    response = user_service.get_users()
    assert response.status_code == 200, f"Не удалось получить список пользователей: {response.text}"
    initial_users = response.json()

    body = {
        "email": "valid@example.com",
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "avatar": "https://example.com/avatar.jpg"
    }
    create_response = user_service.create_user(body)
    assert create_response.status_code == 201, f"Не удалось создать пользователя: {create_response.text}"
    new_user = create_response.json()

    response = user_service.get_users()
    users_list_from_api = response.json()
    users = users_list_from_api
    new_user_found = any(user['id'] == new_user['id'] for user in users)

    assert new_user_found, "Новый пользователь не найден в списке"

    all_users_found = all(
        any(
            all(
                test_user[key] == api_user.get(key)
                for key in test_user
                if key in api_user
            )
            for api_user in users_list_from_api
        )
        for test_user in fill_test_data
    )

    assert all_users_found, "Не все тестовые пользователи найдены в ответе API"

    assert len(users_list_from_api) == len(initial_users) + 1

    delete_response = user_service.delete_user(new_user["id"])
    assert delete_response.status_code == 200, f"Не удалось удалить пользователя: {delete_response.text}"


def test_api_update_patch_user_all_data(env, fill_test_data, clear_database):
    user_service = UserService(env)

    body = {
        "email": "valid@example.com",
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "avatar": "https://example.com/avatar.jpg"
    }
    create_response = user_service.create_user(body)
    assert create_response.status_code == 201, f"Не удалось создать пользователя: {create_response.text}"
    new_user = create_response.json()

    update_body = {
        "email": "new_valid@example.com",
        "first_name": "new_test_first_name",
        "last_name": "new_test_last_name",
        "avatar": "https://newexample.com/avatar.jpg"
    }

    update_response = user_service.update_user(new_user["id"], update_body)
    assert update_response.status_code == 200, f"Не удалось обновить пользователя: {update_response.text}"

    get_response = user_service.get_user_id(new_user["id"])
    updated_user = get_response.json()

    for field, value in update_body.items():
        assert updated_user[field] == value, f"Поле {field} не обновилось"

    delete_response = user_service.delete_user(new_user["id"])
    assert delete_response.status_code == 200, f"Не удалось удалить пользователя: {delete_response.text}"


def test_delete_user_after_create(env, fill_test_data):
    user_service = UserService(env)

    body = {
        "email": "valid@example.com",
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "avatar": "https://example.com/avatar.jpg"
    }
    create_response = user_service.create_user(body)
    assert create_response.status_code == 201, f"Не удалось создать пользователя: {create_response.text}"
    new_user = create_response.json()

    delete_response = user_service.delete_user(new_user["id"])
    assert delete_response.status_code == 200, f"Не удалось удалить пользователя: {delete_response.text}"

    response_get_after_delete = user_service.get_user_id(new_user["id"])
    assert response_get_after_delete.status_code == 404

    response_delete_after_delete = user_service.delete_user(new_user["id"])
    assert response_delete_after_delete.status_code in [404, 500]


def test_api_create_user_with_invalid_data(env, fill_test_data, clear_database):
    user_service = UserService(env)

    body = {
        "email": "invalid_email",
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "avatar": "https://example.com/avatar.jpg"
    }
    create_response = user_service.create_user(body)
    assert create_response.status_code == 500, f"Ожидается ошибка 500, но получен статус: {create_response.status_code}"


def test_api_create_user_without_email(env, fill_test_data, clear_database):
    user_service = UserService(env)

    body = {
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "avatar": "https://example.com/avatar.jpg"
    }
    create_response = user_service.create_user(body)
    assert create_response.status_code == 500, f"Ожидается ошибка 500, но получен статус: {create_response.status_code}"


@pytest.mark.usefixtures("clear_database")
def test_clear_database(env):
    user_service = UserService(env)

    response = user_service.get_users()
    data = response.json()
    user_list = data if isinstance(data, list) else data.get('items', [])
    assert len(user_list) == 0, (
        f"База даных не пуста. Найдено пользователей: {len(user_list)}\n"
        f"Содержимое: {user_list}"
    )


@pytest.mark.usefixtures("fill_test_data")
def test_users_no_duplicates(users):
    assert isinstance(users, list), "Параметр users должен быть списком"

    assert len(users) > 0, "Список пользователей пуст"

    try:
        users_ids = [user["id"] for user in users]
    except KeyError:
        pytest.fail("У некоторых пользователей отсутствует поле 'id'")

    unique_ids = set(users_ids)
    assert len(users_ids) == len(unique_ids), (
        f"Найдены дубликаты ID. Всего элементов: {len(users_ids)}, "
        f"уникальных: {len(unique_ids)}. Дубликаты: {[id for id in unique_ids if users_ids.count(id) > 1]}"
    )


def test_user(env, fill_test_data):
    user_service = UserService(env)

    test_user_ids = [fill_test_data[0]['id'], fill_test_data[-1]['id']]

    for user_id in test_user_ids:
        response = user_service.get_user_id(user_id)

        assert response.status_code == HTTPStatus.OK, (
            f"Для пользователя {user_id} получен статус {response.status_code}, ожидался {HTTPStatus.OK}"
        )

        try:
            user_data = response.json()
            UserData.model_validate(user_data)
        except ValidationError as e:
            pytest.fail(f"Ошибка валидации данных пользователя {user_id}: {str(e)}")
        except ValueError:
            pytest.fail(f"Невалидный JSON в ответе для пользователя {user_id}")


@pytest.mark.parametrize("user_id", [99])
def test_user_nonexistent_values(env, user_id):
    user_service = UserService(env)

    response = user_service.get_user_id(user_id)

    assert response.status_code == HTTPStatus.NOT_FOUND, (
        f"Для несуществующего пользователя {user_id} получен статус {response.status_code}, "
        f"ожидался {HTTPStatus.NOT_FOUND}"
    )


@pytest.mark.parametrize("user_id", [-1, 0, "fafaf"])
def test_user_invalid_values(env, user_id):
    user_service = UserService(env)

    response = user_service.get_user_id(user_id)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, (
        f"Для невалидного ID {user_id!r} получен статус {response.status_code}, "
        f"ожидался {HTTPStatus.UNPROCESSABLE_ENTITY}\n"
        f"Ответ сервера: {response.text}"
    )
