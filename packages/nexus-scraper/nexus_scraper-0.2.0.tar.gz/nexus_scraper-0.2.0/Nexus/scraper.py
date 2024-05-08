import concurrent.futures
from typing import List

from Nexus.exceptions import NexusException, NexusInvalidInfohash
from Nexus.models import NexusSettings, ScrapeResult
from Nexus.scrapers.annatar import Annatar
from Nexus.scrapers.jackett import Jackett
from Nexus.scrapers.orionoid import Orionoid
from Nexus.scrapers.prowlarr import Prowlarr
from Nexus.scrapers.torbox import TorBox
from Nexus.scrapers.torrentio import Torrentio


class NexusScrapers:
    def __init__(self, settings: NexusSettings):
        self.settings = settings
        self.scrapers = {
            "torrentio": Torrentio(settings),
            "orionoid": Orionoid(settings),
            "prowlarr": Prowlarr(settings),
            "jackett": Jackett(settings),
            "annatar": Annatar(settings),
            "torbox": TorBox()
        }
        self.imdb_scrapers = {
            "torrentio": self.scrapers["torrentio"],
            "orionoid": self.scrapers["orionoid"],
            "jackett": self.scrapers["jackett"],
            "annatar": self.scrapers["annatar"],
            "prowlarr": self.scrapers["prowlarr"],
        }
        self.raw_scrapers = {
            "jackett": self.scrapers["jackett"],
            "prowlarr": self.scrapers["prowlarr"],
            "orionoid": self.scrapers["orionoid"],
            "torbox": self.scrapers["torbox"],
        }

    def scrape(self, query: str = "", source: str = "torrentio", **kwargs) -> List[ScrapeResult]:
        """
        Scrape a source for a query. 

        Parameters:
        - `query` (str): The search query.
        - `source` (str): The source to scrape.
        - `kwargs`: Additional keyword arguments to pass to the scraper.

        Returns:
        - A list of `ScrapeResult` objects.
        """
        if not query:
            raise NexusException("Query cannot be empty")

        if source not in self.scrapers:
            if query.startswith("tt"):
                return self.imdb_scrapers["torrentio"].scrape(query, **kwargs)
            else:
                return self.raw_scrapers["torbox"].scrape(query, **kwargs)
        if query.startswith("tt"):
            return self.imdb_scrapers[source].scrape(query, **kwargs)
        return self.raw_scrapers[source].scrape(query, **kwargs)

    def scrape_raw(self, query="", **kwargs) -> List[ScrapeResult]:
        """
        Scrape all sources for a query.

        Parameters:
        - `query` (str): The search query.
        - `kwargs`: Additional keyword arguments to pass to the scraper.

        Returns:
        - A list of `ScrapeResult` objects.
        """
        if query.startswith("tt"):
            raise NexusException("IMDB ID not supported")
        if not query:
            raise NexusException("Query cannot be empty")

        results = []
        workers = len(self.raw_scrapers)
        with concurrent.futures.ThreadPoolExecutor(thread_name_prefix="Nexus Raw Scrape", max_workers=workers) as executor:
            scrape_tasks = {executor.submit(self.scrape, query, source, **kwargs): source for source in self.raw_scrapers if not None}
            for future in concurrent.futures.as_completed(scrape_tasks):
                source = scrape_tasks[future]
                try:
                    result = future.result()
                    results.extend(result)
                    # print(f"Scraped {len(result)} items from {source}")
                except NexusInvalidInfohash:
                    continue
                except Exception as e:
                    raise NexusException(f"Error scraping from {source.title()}: {str(e)}")
        return results

    def imdb_scrape(self, query="", **kwargs) -> List[ScrapeResult]:
        """
        Scrape all IMDB sources for a query.

        Parameters:
        - `query` (str): The IMDB ID.
        - `kwargs`: Additional keyword arguments to pass to the scraper.

        Returns:
        - A list of `ScrapeResult` objects.
        """
        results = []
        workers = len(self.imdb_scrapers)
        with concurrent.futures.ThreadPoolExecutor(thread_name_prefix="Nexus IMDB Scrape", max_workers=workers) as executor:
            scrape_tasks = {executor.submit(self.scrape, query, source, **kwargs): source for source in self.imdb_scrapers if not None}
            for future in concurrent.futures.as_completed(scrape_tasks):
                source = scrape_tasks[future]
                try:
                    result = future.result()
                    results.extend(result)
                    # print(f"Scraped {len(result)} items from {source}")
                except Exception as e:
                    raise NexusException(f"Error scraping from {source}: {str(e)}")
        return results

    def get_sources(self):
        """Get a list of available sources."""
        return list(self.scrapers.keys())

    def get_scraper(self, source):
        """Get a scraper by source."""
        if source not in self.scrapers:
            return self.scrapers["torrentio"]
        return self.scrapers[source]
