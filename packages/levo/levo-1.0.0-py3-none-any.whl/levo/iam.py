class User:
    name: str
    username: str
    password: str

    def __init__(self, *, name: str, username: str, password: str) -> None:
        self.name = name
        self.username = username
        self.password = password
