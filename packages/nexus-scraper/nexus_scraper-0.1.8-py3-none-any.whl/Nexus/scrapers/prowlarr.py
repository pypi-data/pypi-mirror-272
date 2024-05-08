import concurrent.futures

import requests

from Nexus.exceptions import NexusInvalidInfohash, ProwlarrException
from Nexus.models import Guids, NexusSettings, ScrapeResult


class Prowlarr:
    """Prowlarr class for Prowlarr API operations."""

    def __init__(self, settings: NexusSettings):
        if not settings.prowlarr_url or not settings.prowlarr_apikey:
            raise ProwlarrException("URL and API key are required.")
        if len(settings.prowlarr_apikey) != 32:
            raise ProwlarrException("API key must be 32 characters long.")

        self.base_url = settings.prowlarr_url
        self.api_key = settings.prowlarr_apikey
        self.session = requests.Session()
        self.session.headers.update({"X-Api-Key": settings.prowlarr_apikey})

    def _request(self, endpoint, method="GET", params=None, timeout=60):
        url = f"{self.base_url}{endpoint if endpoint.startswith('/') else '/api/v1/' + endpoint}"
        try:
            response = self.session.request(method, url, params=params, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ReadTimeout as e:
            raise ProwlarrException(f"API request timed out: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise ProwlarrException(f"API request error: {str(e)}")

    def scrape(self, query, media_type="", timeout=60) -> list[ScrapeResult]:
        """Scrape Prowlarr for a given query."""
        if query.startswith("tt"):
            return []

        params = {
            "query": query,
            "limit": 1000,
            "offset": 0
        }

        match media_type:
            case "movie":
                params.update({"categories": 2000, "type": "movie-search"})
            case "show":
                params.update({"categories": 5000, "type": "tv-search"})
            case _:
                params.update({"categories": [2000, 5000], "type": "search"})

        data = self._request("search", params=params, timeout=timeout)
        if not data:
            return []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(self._get_rarbg_hash, result["guid"]): result for result in data if "guid" in result}
            results = []
            for future in concurrent.futures.as_completed(futures):
                result = futures[future]
                infohash = future.result()
                if infohash:
                    try:
                        guids = Guids(
                            imdb_id=result.get("imdbId"),
                            tmdb_id=result.get("tmdbId"),
                            tvdb_id=result.get("tvdbId")
                        )
                        scrape_result = ScrapeResult(
                            raw_title=result["title"],
                            infohash=infohash,
                            guids=guids,
                            media_type=media_type if media_type else None,
                            source="prowlarr",
                            size=result.get("size", 0),
                            seeders=result.get("seeders", 0),
                            leechers=result.get("leechers", 0)
                        )
                        results.append(scrape_result)
                    except NexusInvalidInfohash:
                        continue
        return results

    def _get_rarbg_hash(self, guid_url: str) -> str:
        try:
            response = self.session.get(guid_url, timeout=15)
            response.raise_for_status()  # Ensure proper handling of HTTP errors.
            return response.json().get("info_hash", "")
        except Exception:
            return ""

    def ping(self):
        """Ping the Prowlarr API."""
        return self._request("/ping")
