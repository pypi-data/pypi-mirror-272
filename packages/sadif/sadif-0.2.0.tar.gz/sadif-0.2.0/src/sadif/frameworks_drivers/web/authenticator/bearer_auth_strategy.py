# Implementação da autenticação por token
from requests import Session

from sadif.interfaces.web.authenticator import AuthStrategy


class BearerAuthStrategy(AuthStrategy):
    def __init__(self, token: str) -> None:
        self.token = token

    def authenticate(self, session: Session) -> Session:
        session.headers.update({"Authorization": f"Bearer {self.token}"})
        return session
