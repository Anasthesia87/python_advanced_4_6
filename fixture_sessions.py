import pytest

from config import Server
from utils import BaseSession


@pytest.fixture(scope='session')
def reqresin(env):
    with BaseSession(base_url=Server(env).reqres) as session:
        return session