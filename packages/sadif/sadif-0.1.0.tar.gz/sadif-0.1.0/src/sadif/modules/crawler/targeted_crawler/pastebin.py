from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

from bs4 import BeautifulSoup
from pymongo import MongoClient

from sadif.frameworks_drivers.crawler.base_crawler import BaseCrawler


class PastebinPLCrawler(BaseCrawler):
    """
    A crawler for Pastebin.pl, inheriting from BaseCrawler, to fetch and analyze pastes.

    This crawler navigates through Pastebin.pl lists, extracts pastes, and optionally
    analyzes their content.

    Attributes
    ----------
    base_url : str
        The base URL to start crawling from.
    depth : int
        The maximum depth to crawl.
    proxy : str, optional
        A proxy URL to be used for requests.
    timeout : int
        The timeout for requests in seconds.
    db_client : MongoClient, optional
        The database client for storing crawl results.

    Methods
    -------
    __init__(self, base_url="https://pastebin.pl/lists", depth=1, proxy=None, timeout=10, db_client=None)
        Initializes the crawler with the base URL, crawl depth, proxy, timeout, and database client.

    extract_pastes(self, content, current_url)
        Extracts pastes from a Pastebin.pl list page.

    crawl(self, url, current_depth=0)
        Recursively crawls the given URL to the specified depth, extracts pastes, and analyzes their content.

    analyze_paste(self, paste_url)
        Analyzes the content of a single paste. This method is intended to be overridden by subclasses
        to implement specific analysis logic.
    """

    def __init__(
        self,
        base_url: str = "https://pastebin.pl/lists",
        depth: int = 1,
        proxy: str | None = None,
        timeout: int = 10,
        db_client: MongoClient | None = None,
    ) -> None:
        """
        Initializes the PastebinPLCrawler instance with base URL, crawl depth, proxy,
        timeout, and an optional MongoDB client for storing results.

        Parameters
        ----------
        base_url : str
            The starting URL for the crawl.
        depth : int
            Maximum crawl depth.
        proxy : Optional[str]
            Proxy configuration for requests.
        timeout : int
            Timeout for HTTP requests in seconds.
        db_client : Optional[MongoClient]
            MongoDB client for storing crawl results.
        """
        super().__init__(base_url, depth, proxy, timeout, db_client)

    def extract_pastes(self, content: bytes, current_url: str) -> list[dict[str, str]]:
        """
        Extracts paste URLs and titles from the HTML content of a Pastebin.pl list page.

        Parameters
        ----------
        content : bytes
            The HTML content of the page.
        current_url : str
            The URL of the page being processed.

        Returns
        -------
        List[Dict[str, str]]
            A list of dictionaries, each containing the 'url' and 'title' of a paste.
        """
        soup = BeautifulSoup(content, "html.parser")
        pastes = []
        for paste_link in soup.find_all("a", href=True):
            if "/view/" in paste_link["href"]:  # Identify paste links
                full_url = self.normalize_link(paste_link["href"], current_url)
                title = paste_link.text.strip()
                pastes.append({"url": full_url, "title": title})
        return pastes

    def crawl(self, url: str, current_depth: int = 0) -> None:
        """
        Crawls pages from Pastebin.pl, extracts pastes, and optionally analyzes them.
        This method manages recursion based on the specified depth and keeps track of visited URLs.

        Parameters
        ----------
        url : str
            The URL to crawl.
        current_depth : int
            The current depth of the crawl.

        Notes
        -----
        This method prints the found pastes and their analysis results to the console.
        """
        if current_depth > self.depth or url in self.visited_urls:
            return
        self.visited_urls.add(url)
        try:
            response = self.session.get(
                url, proxies={"http": self.proxy, "https": self.proxy}, timeout=self.timeout
            )
            pastes = self.extract_pastes(response.content, url)
            print(f"Pastes found at {url}: {pastes}")
            # Optionally analyze each paste's content
            with ThreadPoolExecutor(max_workers=10) as executor:
                future_to_paste = {
                    executor.submit(self.analyze_paste, paste["url"]): paste for paste in pastes
                }
                for future in as_completed(future_to_paste):
                    paste = future_to_paste[future]  # Get the paste corresponding to this future
                    try:
                        paste_analysis = future.result()
                        if paste_analysis:  # If there's anything significant found in the analysis
                            print(f"Analysis for {paste['url']}: {paste_analysis}")
                    except Exception as e:
                        print(f"Error in analyzing paste: {paste['url']}, Error: {e}")
        except Exception as e:
            print(f"Error crawling {url}: {e}")

    def analyze_paste(self, paste_url: str) -> Any | None:
        """
        Analyzes the content of a single paste. This method can be overridden to implement
        specific analysis, such as applying Yara rules or keyword searching.

        Parameters
        ----------
        paste_url : str
            The URL of the paste to analyze.

        Returns
        -------
        Optional[Any]
            The result of the analysis, which could be a list of matches, a boolean value,
            or any other data structure depending on the implementation.

        Notes
        -----
        This method currently prints analysis errors to the console and returns None if an
        error occurs.
        """
        try:
            response = self.session.get(paste_url, timeout=self.timeout)
            # Here, we could apply the Yara rules or any other analysis
            match_list = self.analyze_content(response.text, paste_url)
            return match_list
        except Exception as e:
            print(f"Error analyzing paste {paste_url}: {e}")
            return None
