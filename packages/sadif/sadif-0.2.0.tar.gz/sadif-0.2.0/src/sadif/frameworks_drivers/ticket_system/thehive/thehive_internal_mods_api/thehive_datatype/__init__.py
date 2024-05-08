from dataclasses import dataclass, field


@dataclass
class CaseDataType:
    """
    A data class representing information related to a case.

    Attributes:
        _id (str): The unique identifier for the case.
        idd (str): Another identifier for the case.
        createdBy (str): The user who created the case.
        updatedBy (str | None): The user who last updated the case, or None if not updated yet.
        createdAt (int): The timestamp when the case was created.
        updatedAt (int | None): The timestamp when the case was last updated, or None if not updated yet.
        _type (str): The type of the case.
        caseId (int): The numerical identifier for the case.
        title (str): The title or name of the case.
        description (str): A description of the case.
        severity (int): The severity level of the case.
        startDate (int): The timestamp when the case started.
        endDate (int | None): The timestamp when the case ended, or None if ongoing.
        impactStatus (str | None): The impact status of the case, or None if not specified.
        resolutionStatus (str | None): The resolution status of the case, or None if not specified.
        tags (list[str]): A list of tags associated with the case.
        flag (bool): A flag indicating whether the case is flagged or not.
        tlp (int): The Traffic Light Protocol (TLP) level of the case.
        pap (int): The Perceived Attribution Program (PAP) level of the case.
        status (str): The current status of the case (e.g., 'New', 'In Progress', 'Closed').
        extendedStatus (str): Additional status information for the case.
        stage (str): The current stage of the case.
        summary (str): A summary or brief overview of the case.
        owner (str): The owner or responsible person for the case.
        customFields (dict): A dictionary of custom fields and their values.
        stats (dict): A dictionary of statistics or metrics related to the case.
        permissions (list[str]): A list of user permissions for the case.

    Note:
        - This class is designed to represent structured data related to cases.
        - Default values are provided for various attributes to initialize instances
    """

    _id: str = field(default="")
    idd: str = field(default="")
    createdBy: str = field(default="")
    updatedBy: str | None = field(default=None)
    createdAt: int = field(default=0)
    updatedAt: int | None = field(default=None)
    _type: str = field(default="")
    caseId: int = field(default=0)
    title: str = field(default="")
    description: str = field(default="")
    severity: int = field(default=2)
    startDate: int = field(default=0)
    endDate: int | None = field(default=None)
    impactStatus: str | None = field(default=None)
    resolutionStatus: str | None = field(default=None)
    tags: list[str] = field(default_factory=list)
    flag: bool = field(default=False)
    tlp: int = field(default=2)
    pap: int = field(default=2)
    status: str = field(default="New")
    extendedStatus: str = field(default="")
    stage: str = field(default="")
    summary: str = field(default="")
    owner: str = field(default="")
    customFields: dict = field(default_factory=dict)
    stats: dict = field(default_factory=dict)
    permissions: list[str] = field(default_factory=list)
