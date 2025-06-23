
class Server:
    def __init__(self, env):
        self.reqres = {
            "dev": "https://reqres.in",
            "beta": "https://reqres.in",
            "rc": "https://reqres.in",
        }[env]