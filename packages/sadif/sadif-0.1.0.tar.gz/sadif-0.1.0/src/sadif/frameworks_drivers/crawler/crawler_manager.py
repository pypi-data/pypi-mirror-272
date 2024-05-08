import json
import re
from pathlib import Path
from urllib.parse import urlparse

from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

from sadif.config.soar_config import SadifConfiguration
from sadif.frameworks_drivers.gitmanager import GitManager
from sadif.frameworks_drivers.log_manager.soar_log import LogManager


class CrawlerManager:
    """
    Manages the crawling process, including interactions with the database, logging, and
    handling of Git repositories for crawler configurations.

    Attributes
    ----------
    db_client : MongoClient, optional
        The MongoDB client used for database interactions. If not provided, a new client
        will be instantiated with default settings.

    Methods
    -------
    __init__(self, db_client=None) -> None
        Initializes the CrawlerManager with optional database client.

    _create_unique_indexes(self)
        Creates unique indexes for URL fields in all managed collections to avoid duplicate
        entries.

    process_document(self, document: dict, overwrite: bool=False) -> Union[ObjectId, int, None]
        Processes a single document (web page data), determining the appropriate collection
        based on the document's URL and whether it requires credentials for access. Handles
        insertion or updating of documents based on the `overwrite` flag.

    _determine_collection(self, url: str, document: dict) -> Collection
        Determines the appropriate MongoDB collection for a document based on its URL and
        whether it contains credentials for access.

    get_all_documents_by_collection(self, collection_name: str=None) -> dict
        Fetches documents from specified collection or all documents from all collections
        if no specific collection is named.

    export_collections(self, export_dir: str)
        Exports all documents from all collections into JSON files, organized by collection
        name within the specified directory.

    import_collections(self, overwrite: bool=False)
        Imports documents into their respective collections from JSON files located in the
        cloned Git repository directory. Overwrites existing documents if `overwrite` is True.
    """

    def __init__(self, db_client=None) -> None:
        """
        Initializes the CrawlerManager instance. Sets up logging, loads configurations from
        the SoarConfiguration, clones the necessary Git repository for crawler monitoring,
        and initializes the database connections based on provided or default MongoDB client.

        Parameters
        ----------
        db_client : MongoClient, optional
            A pre-configured instance of MongoClient for database operations. If not provided,
            a default MongoClient instance will be created and used.

        Raises
        ------
        Exception
            If initialization of any component (logging, configuration loading, Git repository
            cloning, or database connection) fails, an exception is raised with an appropriate
            error message.
        """
        self.log_manager = LogManager()
        init_msg = "Initializing CrawlerManager"
        self.log_manager.log("info", init_msg, category="crawler_manager", task_state="running")

        try:
            self.soar_internal_config = SadifConfiguration()
            self.git_url = self.soar_internal_config.get_configuration(
                "GIT_REPO_CLIENT_CRAWLER_MONITORING"
            )
            self.git_token = self.soar_internal_config.get_configuration("GIT_REPO_TOKEN")
            self.git_manager = GitManager(self.git_url, self.git_token)  # Initialize GitManager
            cloned_dir = self.git_manager.clone_repo()
            if cloned_dir:
                self.directory = cloned_dir
            else:
                self.log_manager.log("error", "Error in cloning the Git repository")
            self.db_client = db_client or MongoClient()
            self.db = self.db_client[
                self.soar_internal_config.get_configuration("MONGODB_DATABASE_CRAWLER")
            ]
            self.collection_with_credential_web = self.db[
                self.soar_internal_config.get_configuration(
                    "MONGODB_COLLECTION_CRAWLER_WEB_WITH_CREDENTIAL"
                )
            ]
            self.collection_without_credential_web = self.db[
                self.soar_internal_config.get_configuration(
                    "MONGODB_COLLECTION_CRAWLER_WEB_WITHOUT_CREDENTIAL"
                )
            ]
            self.collection_with_credential_onion = self.db[
                self.soar_internal_config.get_configuration(
                    "MONGODB_COLLECTION_CRAWLER_ONION_WITH_CREDENTIAL"
                )
            ]
            self.collection_without_credential_onion = self.db[
                self.soar_internal_config.get_configuration(
                    "MONGODB_COLLECTION_CRAWLER_ONION_WITHOUT_CREDENTIAL"
                )
            ]
            self._create_unique_indexes()
            init_success_msg = "CrawlerManager initialized successfully"
            self.log_manager.log(
                "info", init_success_msg, category="crawler_manager", task_state="success"
            )
        except Exception as e:
            init_fail_msg = "Failed to initialize CrawlerManager"
            self.log_manager.capture_exception(e, init_fail_msg, category="crawler_manager")

    def _create_unique_indexes(self):
        """
        Creates unique indexes on the 'url' field for all collections managed by the CrawlerManager.
        This ensures that each URL can only be stored once in each collection, preventing duplicate
        entries.

        Raises
        ------
        Exception
            If creating a unique index for any collection fails, an exception is captured and logged.
        """
        try:
            collections = [
                self.collection_with_credential_web,
                self.collection_without_credential_web,
                self.collection_with_credential_onion,
                self.collection_without_credential_onion,
            ]

            for collection in collections:
                collection.create_index("url", unique=True)

            indexes_msg = "Unique indexes created for all collections"
            self.log_manager.log(
                "info", indexes_msg, category="crawler_manager", task_state="success"
            )
        except Exception as e:
            index_fail_msg = "Failed to create unique indexes"
            self.log_manager.capture_exception(e, index_fail_msg, category="crawler_manager")

    def process_document(self, document: dict, overwrite: bool = False) -> ObjectId | int | None:  # noqa: FBT001
        """
        Processes a given document by determining the appropriate collection based on the URL
        and credentials information within the document. Inserts the document into the database
        or updates an existing document based on the 'overwrite' flag.

        Parameters
        ----------
        document : dict
            The document (e.g., web page data) to be processed and stored in the database.
        overwrite : bool, optional
            If True, the document will update an existing entry with the same URL if found. If False,
            the document will only be inserted if the URL does not already exist in the database.

        Returns
        -------
        ObjectId, int, or None
            The ObjectId of the inserted document if a new document was inserted, the number
            of documents matched for update if an existing document was updated, or None
            if the document was skipped due to duplication and 'overwrite' is False.

        Raises
        ------
        ValueError
            If the 'url' key is missing from the document.
        Exception
            For any other failures during the process, an exception is raised.
        """
        task_state = "running"
        process_msg = "Processing document"
        self.log_manager.log("info", process_msg, category="crawler_manager", task_state=task_state)
        try:
            url = document.get("url")
            if not url:
                msg = "URL is missing from the document"
                raise ValueError(msg)

            collection = self._determine_collection(url, document)

            if overwrite:
                result = collection.update_one({"url": url}, {"$set": document}, upsert=True)
                action = "inserted" if result.upserted_id is not None else "updated"
                doc_msg = f"Document with URL '{url}' {action}."
                self.log_manager.log(
                    "info", doc_msg, category="crawler_manager", task_state="success"
                )
                return result.upserted_id or result.matched_count
            else:
                try:
                    inserted_id = collection.insert_one(document).inserted_id
                    insert_msg = f"Document with URL '{url}' inserted."
                    self.log_manager.log(
                        "info", insert_msg, category="crawler_manager", task_state="success"
                    )
                    return inserted_id
                except DuplicateKeyError:
                    dup_msg = f"Document ignored: Document with URL '{url}' already exists."
                    self.log_manager.log(
                        "warning", dup_msg, category="crawler_manager", task_state="skipped"
                    )
                    return None
        except Exception as e:
            fail_msg = "Failed to process document"
            self.log_manager.capture_exception(e, fail_msg, category="crawler_manager")

    def _determine_collection(self, url: str, document: dict) -> Collection:
        """
        Determines the appropriate MongoDB collection for storing the document based on the
        document's URL and whether it requires credentials for access.

        Parameters
        ----------
        url : str
            The URL of the document being processed.
        document : dict
            The document being processed, which may contain authentication type information
            indicating if credentials are required for access.

        Returns
        -------
        Collection
            The MongoDB collection object where the document should be stored.

        Raises
        ------
        Exception
            If there is any issue in determining the appropriate collection, an exception
            is raised.
        """
        task_state = "running"
        determ_msg = "Determining collection for URL"
        self.log_manager.log("info", determ_msg, category="crawler_manager", task_state=task_state)
        parsed_url = urlparse(url)
        has_credentials = "auth_type" in document and bool(document["auth_type"])

        if parsed_url.hostname.endswith(".onion"):
            return (
                self.collection_with_credential_onion
                if has_credentials
                else self.collection_without_credential_onion
            )
        else:
            return (
                self.collection_with_credential_web
                if has_credentials
                else self.collection_without_credential_web
            )

    def get_all_documents_by_collection(self, collection_name: str = None) -> dict:
        """
        Retrieves documents from a specific collection or all documents from all collections
        managed by the CrawlerManager, depending on the 'collection_name' parameter.

        Parameters
        ----------
        collection_name : str, optional
            The name of a specific collection from which to fetch documents. If not provided,
            documents will be fetched from all collections.

        Returns
        -------
        dict
            A dictionary with collection names as keys and lists of documents as values. If
            a specific collection name is provided, the dictionary will contain a single entry.

        Raises
        ------
        Exception
            If fetching documents fails for any reason, an exception is raised and logged.
        """
        try:
            self.log_manager.log(
                "info",
                "Fetching documents from collections",
                category="crawler_manager",
                task_state="running",
            )
            collections = {
                "crawler_with_credential_web": self.collection_with_credential_web,
                "crawler_without_credential_web": self.collection_without_credential_web,
                "crawler_with_credential_onion": self.collection_with_credential_onion,
                "crawler_without_credential_onion": self.collection_without_credential_onion,
            }

            # Verifica se um nome de coleção específico foi fornecido
            if collection_name and collection_name in collections:
                # Retorna documentos apenas da coleção especificada
                documents = list(collections[collection_name].find({}, {"_id": 0}))
                self.log_manager.log(
                    "info",
                    f"Documents fetched from {collection_name}",
                    category="crawler_manager",
                    task_state="running",
                )
                return {collection_name: documents}
            else:
                # Caso nenhum nome específico seja fornecido, retorna todos os documentos
                all_documents = {}
                for collection_name, collection in collections.items():
                    documents = list(collection.find({}, {"_id": 0}))
                    all_documents[collection_name] = documents
                    self.log_manager.log(
                        "info",
                        f"Documents fetched from {collection_name}",
                        category="crawler_manager",
                        task_state="running",
                    )

                self.log_manager.log(
                    "info",
                    "Successfully fetched all documents",
                    category="crawler_manager",
                    task_state="success",
                )
                return all_documents
        except Exception as e:
            self.log_manager.capture_exception(
                e, "Failed to fetch documents", category="crawler_manager"
            )

    def export_collections(self, export_dir: str):
        """
        Exports all documents from the database into JSON files organized by collection name
        within the specified directory.

        Parameters
        ----------
        export_dir : str
            The directory path where the collection documents should be exported as JSON files.

        Raises
        ------
        Exception
            If there are any issues during the export process, such as problems creating directories
            or writing to files, an exception is raised and logged.
        """
        task_state = "running"
        try:
            self.log_manager.log(
                "info",
                "Starting export of collections",
                category="crawler_manager",
                task_state=task_state,
            )
            all_documents = self.get_all_documents_by_collection()

            export_dir_path = Path(export_dir)
            export_dir_path.mkdir(parents=True, exist_ok=True)

            for collection_name, documents in all_documents.items():
                collection_dir = export_dir_path / collection_name
                collection_dir.mkdir(parents=True, exist_ok=True)

                for document in documents:
                    url = document.get("url", "unknown")
                    # Removendo protocolos e 'www' da URL
                    simplified_url = re.sub(r"https?://", "", url)
                    simplified_url = re.sub(r"www\.", "", simplified_url)
                    # Substituindo caracteres não permitidos em nomes de arquivos
                    filename = (
                        simplified_url.replace(".", "_").replace("/", "_").replace(":", "_")
                        + ".json"
                    )
                    with (collection_dir / filename).open("w") as file:
                        json.dump(document, file)

                self.log_manager.log(
                    "info",
                    f"Documents exported for collection {collection_name}",
                    category="crawler_manager",
                    task_state="running",
                )

            self.log_manager.log(
                "info",
                "Export completed successfully",
                category="crawler_manager",
                task_state="success",
            )
        except Exception as e:
            self.log_manager.capture_exception(
                e, "Failed to export collections", category="crawler_manager"
            )

    def import_collections(self, meta_update: bool = False):  # noqa: FBT001
        """
        Imports documents into the database from JSON files located within the cloned Git repository
        directory. Existing documents can be overwritten based on the 'overwrite' flag. If 'meta_update'
        is set to True, the entire database is dropped and recreated from the imported JSON files.
        """
        imported_urls = []
        ignored_urls = []  # Esta lista agora conterá tuplas de (nome do arquivo, motivo)

        try:
            if meta_update:
                self.db_client.drop_database(self.db.name)
                self.log_manager.log(
                    level="info",
                    message=f"Database '{self.db.name}' dropped for meta update.",
                    category="crawler_manager",
                    task_state="running",
                )

            import_dir_path = Path(self.directory)

            for collection_dir in import_dir_path.iterdir():
                if not collection_dir.is_dir() or not collection_dir.name.startswith("crawler_"):
                    continue

                collection_name = collection_dir.name
                collection = self.db[collection_name]

                if meta_update:
                    self.log_manager.log(
                        level="info",
                        message=f"Collection '{collection_name}' deleted for meta update.",
                        category="crawler_manager",
                        task_state="running",
                    )

                for file_path in collection_dir.iterdir():
                    if file_path.is_file():
                        with file_path.open() as file:
                            document = json.load(file)
                            url = document.get("url", None)
                            if not url:
                                ignored_urls.append(
                                    (file_path.name, "URL is needed to import file.")
                                )
                                continue

                            try:
                                collection.replace_one({"url": url}, document, upsert=True)
                                imported_urls.append(url)
                                self.log_manager.log(
                                    level="info",
                                    message=f"Monitoring url {url} inserted in {collection_name}.",
                                    category="crawler_manager",
                                    task_state="success",
                                )
                            except Exception as e:
                                ignored_urls.append((file_path.name, str(e)))
                                self.log_manager.log(
                                    level="error",
                                    message=f"Error inserting url {url} in {collection_name}: {e}",
                                    category="crawler_manager",
                                    task_state="failed",
                                    exc_info=e,
                                )

            self.log_manager.log(
                level="info",
                message="Import completed successfully",
                category="crawler_manager",
                task_state="success",
            )
            if ignored_urls:
                for ignored_url in ignored_urls:
                    self.log_manager.log(
                        level="warning",
                        message=f"Ignored URL from file '{ignored_url[0]}': {ignored_url[1]}",
                        category="crawler_manager",
                        task_state="skipped",
                    )
            self.log_manager.log(
                level="info",
                message=f"Imported URLs: {len(imported_urls)}. Ignored URLs: {len(ignored_urls)}.",
                category="crawler_manager",
                task_state="skipped",
            )
        except FileNotFoundError as e:
            self.log_manager.log(
                level="error",
                message="Cloned repository directory not found: " + str(e),
                category="crawler_manager",
                task_state="failed",
                exc_info=e,
            )
        except Exception as e:
            self.log_manager.log(
                level="error",
                message="Failed to import collections: " + str(e),
                category="crawler_manager",
                task_state="failed",
                exc_info=e,
            )
