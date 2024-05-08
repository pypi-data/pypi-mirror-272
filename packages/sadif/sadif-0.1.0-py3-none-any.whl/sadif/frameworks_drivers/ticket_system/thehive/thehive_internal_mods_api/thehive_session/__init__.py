import requests
from requests.auth import HTTPBasicAuth  # This import is used, so we keep it.


class SessionThehive:
    """
    A client to interact with TheHive API.
    ...
    """

    def __init__(self, base_url: str = "http://localhost:9000/api/"):
        """
        Initialize a SessionThehive instance.
        ...
        """
        self.base_url = base_url
        self.headers: dict[str, str] = {}  # Use built-in dict instead of typing.Dict
        self.cookies: dict[str, str] = {}  # Use built-in dict instead of typing.Dict
        self.auth: HTTPBasicAuth | None = None  # Keep using HTTPBasicAuth from requests

    def _reset_auth(self) -> None:
        """Reset the authentication information (both headers and cookies)."""

        self.headers.pop("Authorization", None)
        self.cookies.pop("THEHIVE-SESSION", None)
        self.auth = None

    def set_api_key(self, api_key: str) -> None:
        """
        Set the API key for authentication.

        Parameters
        ----------
        api_key : str
            The API key.
        """
        self._reset_auth()
        self.headers["Authorization"] = f"Bearer {api_key}"

    def set_basic_auth(self, login: str, password: str) -> None:
        self._reset_auth()
        from requests.auth import HTTPBasicAuth

        self.auth = HTTPBasicAuth(login, password)

    def set_session(self, session_id: str) -> None:
        self._reset_auth()
        self.cookies["THEHIVE-SESSION"] = session_id

    def set_organisation(self, org_name: str) -> None:
        self.headers["X-Organisation"] = org_name

    def request(
        self, endpoint: str, method: str = "GET", json_data: dict | None = None
    ) -> tuple[dict | str, int]:
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.request(
                method,
                url,
                headers=self.headers,
                cookies=self.cookies,
                json=json_data,
                auth=self.auth,
            )
            response.raise_for_status()
            status_code_request = (
                response.status_code
            )  # Assuming 'response' is an instance of a request's Response object
            try:
                json_data = response.json()
                return json_data, status_code_request
            except ValueError:  # Raised when the response isn't a valid JSON
                return response.text, status_code_request

        except requests.RequestException as e:
            print(f"Request error: {e}")
        except ValueError:
            print(f"Error decoding JSON from response. URL: {url}")

    def get_status(self) -> tuple[dict | str, int]:
        return self.request("status")

    def create_alert(self, data: dict) -> tuple[dict | str, int]:
        return self.request("alert", method="POST", json_data=data)
