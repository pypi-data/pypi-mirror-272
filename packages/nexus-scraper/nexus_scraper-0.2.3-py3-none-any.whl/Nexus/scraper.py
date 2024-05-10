import concurrent.futures
from typing import List

from Nexus.exceptions import NexusException, NexusInvalidInfohash
from Nexus.models import NexusSettings, ScrapeResult
from Nexus.scrapers.annatar import Annatar
from Nexus.scrapers.apibay import Apibay
from Nexus.scrapers.jackett import Jackett
from Nexus.scrapers.orionoid import Orionoid
from Nexus.scrapers.prowlarr import Prowlarr
from Nexus.scrapers.torbox import TorBox
from Nexus.scrapers.torrentio import Torrentio


class Nexus:
    def __init__(self, settings: NexusSettings):
        self.settings = settings
        self.scrapers = {
            "torrentio": Torrentio(settings),
            "orionoid": Orionoid(settings),
            "prowlarr": Prowlarr(settings),
            "jackett": Jackett(settings),
            "annatar": Annatar(settings),
            "torbox": TorBox(),
            "apibay": Apibay(),
        }

        self.imdb_scrapers = {k: v for k, v in self.scrapers.items() if k not in ["torbox"]}
        self.raw_scrapers = {k: v for k, v in self.scrapers.items() if k not in ["torrentio", "annatar"]}

    def scrape(self, query: str = "", source: str = "torrentio", **kwargs) -> List[ScrapeResult]:
        """
        Scrape a source for a query.

        Args:
            query (str): The search query.
            source (str): The source to scrape.

        Returns:
            List[ScrapeResult]: A list of `ScrapeResult` objects.
        """
        if not query:
            raise NexusException("Query cannot be empty")
        if source not in self.scrapers:
            raise NexusException("Invalid source")
        
        if source in ["torrentio", "annatar"] and not query.startswith("tt"):
            raise NexusException("IMDB ID not supported for the selected source")
        
        return self.scrapers[source].scrape(query, **kwargs)

    def scrape_raw(self, query: str = "", **kwargs) -> List[ScrapeResult]:
        """
        Scrape all non-ID-based sources for a query.

        Args:
            query (str): The search query.

        Returns:
            List[ScrapeResult]: A list of `ScrapeResult` objects.
        """
        if not query:
            raise NexusException("Query cannot be empty")
        if query.startswith("tt"):
            raise NexusException("IMDB ID not supported in raw scrape")

        return self._execute_concurrent_scrape(self.raw_scrapers, query, **kwargs)

    def imdb_scrape(self, query: str = "", **kwargs) -> List[ScrapeResult]:
        """
        Scrape all ID-based sources with a valid IMDB ID.

        Args:
            query (str): The IMDB ID.

        Returns:
            List[ScrapeResult]: A list of `ScrapeResult` objects.
        """
        if not query:
            raise NexusException("Query cannot be empty")
        if not query.startswith("tt"):
            raise NexusException("Invalid IMDB ID")

        return self._execute_concurrent_scrape(self.imdb_scrapers, query, **kwargs)

    def _execute_concurrent_scrape(self, scrapers, query, **kwargs) -> List[ScrapeResult]:
        results = []
        workers = len(scrapers)
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers, thread_name_prefix="Nexus Scrape") as executor:
            scrape_tasks = {executor.submit(scraper.scrape, query, **kwargs): scraper for scraper in scrapers.values()}
            for future in concurrent.futures.as_completed(scrape_tasks):
                try:
                    results.extend(future.result())
                except NexusInvalidInfohash:
                    continue
                except Exception as e:
                    scraper_name = type(scrape_tasks[future]).__name__
                    raise NexusException(f"Error scraping from {scraper_name}: {str(e)}")
        return results

    def get_sources(self) -> List[str]:
        """Return a list of available sources."""
        return list(self.scrapers.keys())

    def get_scraper(self, source: str):
        """Get a scraper by source. Defaults to 'torrentio' if not found."""
        return self.scrapers.get(source, self.scrapers["torrentio"])
