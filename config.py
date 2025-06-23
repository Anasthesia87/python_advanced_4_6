class Server:
    def __init__(self, env):
        self.reqres = {
            "dev": "http://127.0.0.1:8002",
            "beta": "",
            "rc": "",
        }[env]
        self.ninjacats = {
            "dev": "",
            "beta": "",
            "rc": "https://ninjactas.com",
        }[env]