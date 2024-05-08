from abc import ABC, abstractmethod

from requests import Session


class AuthStrategy(ABC):
    """
    An abstract base class defining the interface for authentication strategies.

    This interface requires implementing classes to provide a method for
    authenticating HTTP sessions.

    Methods
    -------
    authenticate(session: Session) -> Session
        Authenticates an HTTP session and returns the authenticated session.
    """

    @abstractmethod
    def authenticate(self, session: Session) -> Session:
        """
        Abstract method to be implemented by concrete authentication strategies.
        This method should handle the authentication process and modify the
        provided session object as necessary.

        Parameters
        ----------
        session : Session
            The requests session object to be authenticated.

        Returns
        -------
        Session
            The authenticated requests session object.

        Raises
        ------
        NotImplementedError
            If the child class does not implement this method.
        """
