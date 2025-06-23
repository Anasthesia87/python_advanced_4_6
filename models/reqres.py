from config import Server
from utils.base_session import BaseSession


class User:
    def __init__(self, **kwargs):
        json_ = kwargs.pop("json", {})
        self._id = kwargs.pop("id", None)
        self._email = kwargs.pop("email", None)
        self._first_name = kwargs.pop("first_name", None)
        self._last_name = kwargs.pop("last_name", None)
        self._avatar = kwargs.pop("avatar", None)
        self._json = json_ if json_ else {
            "id": self._id,
            "email": self._email,
            "first_name": self._first_name,
            "last_name": self._last_name,
            "avatar": self._avatar,
        }

    @property
    def id(self):
        return self._json['id']

    @property
    def email(self):
        return self._json['email']

    @property
    def first_name(self):
        return self._json['first_name']

    @property
    def last_name(self):
        return self._json['last_name']

    @property
    def avatar(self):
        return self._json['avatar']

    @property
    def json(self):
        return self._json


class ResponseUser:
    def __init__(self, **kwargs):
        json_ = kwargs.pop("json", {})
        self._id = kwargs.pop("id", 2)
        self._email = kwargs.pop("email", "janet.weaver@reqres.in")
        self._first_name = kwargs.pop("first_name", "Janet")
        self._last_name = kwargs.pop("last_name", "Weaver")
        self._avatar = kwargs.pop("avatar", "https://reqres.in/img/faces/2-image.jpg")
        self._json = json_ if json_ else {
            "id": self._id,
            "email": self._email,
            "first_name": self._first_name,
            "last_name": self._last_name,
            "avatar": self._avatar,
        }

    @property
    def json(self):
        return self._json


class ResponseListUsers:
    def __init__(self, **kwargs):
        json_ = kwargs.pop("json", {})

        self._json = json_ if json_ else {
            "page": 2,
            "per_page": 6,
            "total": 12,
            "total_pages": 2,
            "data": []
        }

    def add_user(self, user: ResponseUser):
        self._json['data'].append(user.json)
        return self

    @property
    def json(self):
        return self._json


class Reqres:
    def __init__(self, env):
        self.session = BaseSession(base_url=Server(env).reqres)

    def get_user(self, user_id: int):
        return ResponseUser(response=self.session.get(f"/api/users/{user_id}"))

    def get_users(self):
        return ResponseListUsers(response=self.session.get("/api/users"))