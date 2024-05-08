import concurrent.futures
from typing import List

import requests

from Nexus.exceptions import JackettException, NexusInvalidInfohash
from Nexus.models import Guids, NexusSettings, ScrapeResult


class Jackett:
    def __init__(self, settings: NexusSettings):
        self.settings = settings
        if not self.settings.jackett_url or not self.settings.jackett_apikey:
            raise JackettException("URL and API key are required.")
        self.base_url = self.settings.jackett_url
        self.api_key = self.settings.jackett_apikey
        self.session = requests.Session()

    def _request(self, endpoint, method="GET", params=None, data=None, timeout=60):
        """Private method to handle API requests."""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self.session.request(method, url, params=params, json=data, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ReadTimeout as e:
            raise TimeoutError(f"API request timed out: {e}")
        except requests.exceptions.RequestException as e:
            raise JackettException(f"API request error: {e}")

    def scrape(self, query, media_type="movie", timeout=60) -> List[ScrapeResult]:
        """Method to scrape data based on a query and media type."""
        if not query:
            return []

        category_map = {"movie": "2000", "show": "5000"}
        category = category_map.get(media_type.lower(), "2000,5000")

        params = {"apikey": self.api_key, "q": query, "cat": category}
        data = self._request("api/v2.0/indexers/all/results", params=params, timeout=timeout)

        if not data or "Results" not in data:
            return []

        results = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(self._process_result, result, category): result for result in data["Results"]}
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)

        return results

    def _process_result(self, result, category):
        """Helper method to process each result independently."""
        try:
            return ScrapeResult(
                raw_title=result["Title"],
                infohash=result.get("InfoHash"),
                guids=Guids(),
                media_type=category,
                source="jackett",
                size=result.get("Size", 0),
                seeders=result.get("Seeders", 0),
                leechers=result.get("Peers", 0)
            )
        except NexusInvalidInfohash:
            return None
