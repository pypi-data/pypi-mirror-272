from sadif.frameworks_drivers.ticket_system.thehive.thehive_internal_mods_api.thehive_session import (
    SessionThehive,
)


class CaseComment:
    """
    A utility class to manage comments related to cases and alerts in TheHive.

    Attributes
    ----------
    session : SessionThehive
        An active session to interact with TheHive's API.

    Methods
    -------
    create_for_case(case_id, message):
        Create a comment for a specific case.

    create_for_alert(alert_id, message):
        Create a comment for a specific alert.

    delete(comment_id):
        Delete a specific comment.

    update(comment_id, message):
        Update the message of a specific comment.

    """

    def __init__(self, session: SessionThehive):
        """
        Initialize the CaseComment object.

        Parameters
        ----------
        session : SessionThehive
            An active session to interact with TheHive's API.
        """
        self.session = session

    def create_for_case(self, case_id, message):
        """
        Create a comment for a specific case.

        Parameters
        ----------
        case_id : str
            The ID of the case to which the comment will be added.
        message : str
            The message of the comment.

        Returns
        -------
        tuple
            The response and status code of the create request.
        """
        endpoint = f"v1/case/{case_id}/comment"
        data = {"message": message}
        return self.session.request(endpoint, method="POST", json_data=data)

    def create_for_alert(self, alert_id, message):
        """
        Create a comment for a specific alert.

        Parameters
        ----------
        alert_id : str
            The ID of the alert to which the comment will be added.
        message : str
            The message of the comment.

        Returns
        -------
        tuple
            The response and status code of the create request.
        """
        endpoint = f"v1/alert{alert_id}/comment"
        data = {"message": message}
        return self.session.request(endpoint, method="POST", json_data=data)

    def delete(self, comment_id):
        """
        Delete a specific comment.

        Parameters
        ----------
        comment_id : str
            The ID of the comment to be deleted.

        Returns
        -------
        tuple
            The response and status code of the delete request.
        """
        endpoint = f"v1/comment/{comment_id}"
        return self.session.request(endpoint, method="DELETE")

    def update(self, comment_id, message):
        """
        Update the message of a specific comment

        Parameters
        ----------
        comment_id : str
            The ID of the comment to be updated.
        message : str
            The updated message of the comment.

        Returns
        -------
        tuple
            The response and status code of the update request
        """
        endpoint = f"v1/comment/{comment_id}"
        data = {"message": message}
        return self.session.request(endpoint, method="PATCH", json_data=data)
