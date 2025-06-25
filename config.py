
class Server:
    def __init__(self, env):
        self.service = {
            "dev": "http://localhost:8002/api/",
            "beta": "",
            "rc": "",
        }[env]

