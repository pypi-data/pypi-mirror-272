import shutil
import tempfile
from pathlib import Path

from git import GitCommandError, Repo

from sadif.frameworks_drivers.log_manager.soar_log import LogManager


class GitManager:
    """
    Manages Git operations including cloning, pulling, committing, and pushing changes
    to a repository. It uses a temporary directory for repository operations and supports
    authentication via a personal access token.

    Attributes
    ----------
    repo_url : str
        The URL of the Git repository to manage.
    token : Optional[str]
        The personal access token for repository authentication; defaults to None.
    repo_dir : str
        The path to the temporary directory where the repository is cloned.
    repo : Optional[Repo]
        The GitPython Repo object for the cloned repository; initially None.
    log_manager : LogManager
        The LogManager instance for logging operations within the GitManager.

    Methods
    -------
    configure_authentication()
        Configures repository authentication using the token, if provided.
    clone_repo() -> Optional[str]
        Clones the repository into a temporary directory, returning the directory path.
    pull_changes(branch: str = 'master')
        Pulls changes from the given branch into the cloned repository.
    commit_changes(commit_message: str)
        Commits all current changes in the cloned repository with the given commit message.
    push_changes(branch: str = 'main')
        Pushes committed changes from the cloned repository to the specified branch.
    cleanup()
        Removes the temporary directory and cleans up resources.
    """

    def __init__(self, repo_url: str, token: str | None = None):
        """
        Initializes the GitManager with the repository URL and an optional authentication token.

        Parameters
        ----------
        repo_url : str
            The URL of the Git repository.
        token : Optional[str], optional
            The personal access token for authentication, by default None.
        """
        self.repo_url = repo_url
        self.token = token
        self.repo_dir = tempfile.mkdtemp()
        self.repo = None
        self.log_manager = LogManager()
        self.log_manager.log("info", "Initializing GitManager", "git")
        self.configure_authentication()

    def configure_authentication(self):
        """Configures repository authentication using the personal access token, if provided."""
        if self.token:
            self.repo_url = self.repo_url.replace(
                "https://", f"https://x-access-token:{self.token}@"
            )
            self.log_manager.log(
                "info", "Authentication configuration completed", "git", task_state="success"
            )

    def clone_repo(self) -> str | None:
        """
        Clones the Git repository into a temporary directory and returns the directory path.

        Returns
        -------
        Optional[str]
            The path to the temporary directory containing the cloned repository, or None if cloning fails.
        """
        try:
            self.repo = Repo.clone_from(self.repo_url, self.repo_dir)
            self.log_manager.log(
                "info",
                f"Repository successfully cloned to {self.repo_dir}",
                "git",
                task_state="success",
            )
            return self.repo_dir
        except GitCommandError as e:
            self.log_manager.log(
                "error", f"Error cloning repository: {e}", "git", exc_info=e, task_state="failed"
            )
            return None

    def pull_changes(self, branch: str = "main"):
        """
        Pulls changes from the specified branch into the cloned repository.

        Parameters
        ----------
        branch : str
            The branch from which to pull changes, default is 'main'.
        """
        self.log_manager.log(
            "info", f"Attempting to pull from branch {branch}", "git", task_state="running"
        )
        try:
            self.repo.git.pull("origin", branch)
            self.log_manager.log("info", "Pull successful", "git", task_state="success")
        except GitCommandError as e:
            self.log_manager.log(
                "error", f"Error during pull: {e}", "git", exc_info=e, task_state="failed"
            )

    def commit_changes(self, commit_message: str):
        """
        Commits all current changes in the cloned repository with the provided commit message.

        Parameters
        ----------
        commit_message : str
            The commit message to use for the commit.
        """
        self.log_manager.log("info", "Attempting to commit changes", "git", task_state="running")
        try:
            self.repo.git.add(A=True)
            self.repo.index.commit(commit_message)
            self.log_manager.log("info", "Commit successful", "git", task_state="success")
        except GitCommandError as e:
            self.log_manager.log(
                "error", f"Error during commit: {e}", "git", exc_info=e, task_state="failed"
            )

    def push_changes(self, branch: str = "main"):
        """
        Pushes committed changes from the cloned repository to the specified branch.

        Parameters
        ----------
        branch : str
            The branch to which the changes should be pushed, default is 'main'.
        """
        self.log_manager.log(
            "info", f"Attempting to push to branch {branch}", "git", task_state="running"
        )
        try:
            origin = self.repo.remote(name="origin")
            origin.push(branch)
            self.log_manager.log("info", "Push successful", "git", task_state="success")
        except GitCommandError as e:
            self.log_manager.log(
                "error", f"Error during push: {e}", "git", exc_info=e, task_state="failed"
            )

    def cleanup(self):
        """
        Removes the temporary directory used for the cloned repository and cleans up resources.
        """
        self.log_manager.log(
            "info", "Starting cleanup of temporary directory", "git", task_state="running"
        )
        try:
            if self.repo:
                self.repo.close()

            if Path(self.repo_dir).exists():
                shutil.rmtree(self.repo_dir)
                self.log_manager.log(
                    "info", "Temporary directory successfully removed", "git", task_state="success"
                )
        except OSError as e:
            self.log_manager.log(
                "error",
                f"Error removing temporary directory: {e}",
                "git",
                exc_info=e,
                task_state="failed",
            )
