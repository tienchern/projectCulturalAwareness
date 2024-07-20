class Person:
    _country = None
    _name = None
    _model = None

    def __init__(self, country: str, name: str):
        self._country = country
        self._name = name

    def __str__(self) -> str:
        return self._name

    def say_hi() -> str:
        return "Hi there!"

    def respond(user_input: str) -> str:
        return f"You said {user_input}" 