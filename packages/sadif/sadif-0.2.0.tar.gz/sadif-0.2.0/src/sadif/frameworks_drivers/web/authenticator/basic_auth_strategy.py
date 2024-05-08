# Implementação da autenticação básica
from requests import Session

from sadif.interfaces.web.authenticator import AuthStrategy


class BasicAuthStrategy(AuthStrategy):
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def authenticate(self, session: Session) -> Session:
        session.auth = (self.username, self.password)
        return session
