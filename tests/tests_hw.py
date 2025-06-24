from app.models.UserService import UserService


def test_api_create_user(env):
    # Подготовка данных
    body = {
        "email": "valid@example.com",
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "avatar": "https://example.com/avatar.jpg"
    }

    # Инициализация сервиса
    user_service = UserService(env)

    # Создание пользователя
    create_response = user_service.create_user(body)
    assert create_response.status_code == 201, f"Не удалось создать пользователя: {create_response.text}"

    new_user = create_response.json()

    # Проверка, что данные пользователя соответствуют переданным
    values_equal = all(new_user[key] == body[key]
                       for key in body
                       if key in new_user)
    assert values_equal, "Данные пользователя не совпадают с ожидаемыми"

    # Удаление пользователя (используем метод сервиса, а не requests)
    delete_response = user_service.delete_user(new_user["id"])
    assert delete_response.status_code == 200, f"Не удалось удалить пользователя: {delete_response.text}"
