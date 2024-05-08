# Classe que utiliza uma estratégia de autenticação
from requests import Session

from sadif.interfaces.web.authenticator import AuthStrategy


class Authenticator:
    def __init__(self, strategy: AuthStrategy) -> None:
        self.strategy = strategy

    def authenticate(self, session: Session) -> Session:
        return self.strategy.authenticate(session)
