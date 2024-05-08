# Implementação da autenticação digest
from requests import Session
from requests.auth import HTTPDigestAuth

from sadif.interfaces.web.authenticator import AuthStrategy


class DigestAuthStrategy(AuthStrategy):
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def authenticate(self, session: Session) -> Session:
        session.auth = HTTPDigestAuth(self.username, self.password)
        return session
