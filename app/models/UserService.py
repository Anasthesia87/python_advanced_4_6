from fastapi import HTTPException

from app.models.User import UserDataCreateBody, UserDataUpdateBody
from config import Server
from utils.base_session import BaseSession


class UserService:
    def __init__(self, env):
        self.session = BaseSession(base_url=Server(env).service)

    def get_status(self):
        return self.session.get(f"status")

    def get_users(self):
        return self.session.get(f"users")

    def get_user_id(self, user_id: int):
        return self.session.get(f"users/{user_id}")

    def create_user(self, user: UserDataCreateBody):
        if user:
            return self.session.post(f"users", json=user)
        else:
            raise HTTPException(status_code=400, detail="Invalid user")

    def update_user(self, user_id: int, user: UserDataUpdateBody):
        return self.session.patch(f"users/{user_id}", json=user)

    def delete_user(self, user_id: int):
        return self.session.delete(f"users/{user_id}")
