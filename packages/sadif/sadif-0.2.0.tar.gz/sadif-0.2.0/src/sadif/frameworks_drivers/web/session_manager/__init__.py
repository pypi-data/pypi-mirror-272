from requests import Session

from sadif.interfaces.web.authenticator import AuthStrategy


class SessionManager:
    def __init__(self) -> None:
        self.sessions: list[Session] = []

    def create_session(self, auth_strategy: AuthStrategy | None = None) -> Session:
        """
        Create a new HTTP session, optionally authenticated using the provided auth_strategy.

        Parameters
        ----------
        auth_strategy : AuthStrategy, optional
            Strategy to use for session authentication. If None, the session is created without authentication.

        Returns
        -------
        Session
            The newly created (and possibly authenticated) session.
        """
        session = Session()
        if auth_strategy:
            session = auth_strategy.authenticate(session)
        self.sessions.append(session)
        return session

    def close_session(self, session: Session) -> None:
        """
        Close and remove a specified session.

        Parameters
        ----------
        session : Session
            The session to close and remove.
        """
        session.close()
        self.sessions.remove(session)

    def close_all_sessions(self) -> None:
        """
        Close all active sessions and clear the list.
        """
        for session in self.sessions:
            session.close()
        self.sessions.clear()
