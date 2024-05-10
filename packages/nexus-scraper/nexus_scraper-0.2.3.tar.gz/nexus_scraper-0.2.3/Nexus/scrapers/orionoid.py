from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

from Nexus.exceptions import NexusInvalidInfohash, OrionoidException
from Nexus.models import Guids, NexusSettings, ScrapeResult


class Orionoid:
    """Orionoid class for Orionoid API operations."""

    def __init__(self, settings: NexusSettings):
        if not settings.orionoid_client or not settings.orionoid_apikey:
            return

        self.base_url = "https://api.orionoid.com"
        self.client_id = settings.orionoid_client
        self.api_key = settings.orionoid_apikey
        self.is_premium = False
        self.is_initialized = False
        self.session = requests.Session()
        self.check_api_key_validity()

    def check_api_key_validity(self):
        """Validate the API key and initialize parameters based on the account type."""
        url = f"{self.base_url}?keyapp={self.client_id}&keyuser={self.api_key}&mode=user&action=retrieve"
        try:
            response = self.session.get(url, timeout=60)
        except requests.exceptions.ReadTimeout as e:
            raise requests.exceptions.ReadTimeout(f"API request timed out: {str(e)}")
        except requests.exceptions.ConnectTimeout as e:
            raise requests.exceptions.ConnectTimeout(f"API request timed out: {str(e)}")
        if response.status_code != 200:
            raise OrionoidException(f"API key validation failed with status code {response.status_code}")

        data = response.json()
        if data.get('result', {}).get('status') == 'success' and data.get('data', {}).get('status') == 'active':
            self.is_premium = data['data']['subscription']['package']['premium']
            self.is_initialized = True
        else:
            raise OrionoidException("Failed to initialize Orionoid due to invalid API key or account status.")

    def scrape(self, query: str, media_type: str = "movie", season=None, episode=None, timeout=60) -> list[ScrapeResult]:
        """Scrape Orionoid for a given media type and ID."""
        if not self.is_initialized:
            raise OrionoidException("Orionoid API not initialized.")

        if media_type not in ["movie", "show"]:
            raise OrionoidException("Invalid media type. Must be 'movie' or 'show'.")

        url = self.construct_url(query, media_type, season, episode)
        try:
            response = self.session.get(url, timeout=timeout)
        except requests.exceptions.ReadTimeout as e:
            raise OrionoidException(f"API request timed out: {str(e)}")

        if response.status_code != 200:
            raise OrionoidException(f"API request failed with status code {response.status_code}")

        if 'application/json' not in response.headers.get('Content-Type', ''):
            raise OrionoidException("Expected JSON response but received a different format.")

        data = response.json()
        streams = data["data"]["streams"]
        return self.parse_response(streams, query, media_type)

    def construct_url(self, query, media_type, season=None, episode=None) -> str:
        """Construct the URL for the Orionoid API based on media type and identifiers."""
        params = {
            "keyapp": self.client_id,
            "keyuser": self.api_key,
            "mode": "stream",
            "action": "retrieve",
            "type": media_type,
            "streamtype": "torrent",
            "filename": "true",
            "limitcount": 200 if self.is_premium else 5,
            "sortorder": "descending",
            "sortvalue": "best" if self.is_premium else "popularity",
        }
        if season and episode:
            params.update({"numberseason": season, "numberepisode": episode})
        elif season:
            params.update({"numberseason": season})
        if query.startswith("tt"):
            params.update({"idimdb": query})
        else:
            params.update({"query": query})
        return f"{self.base_url}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"

    def parse_response(self, streams, imdb_id, media_type) -> list[ScrapeResult]:
        """Parse the response from Orionoid and create ScrapeResult objects using concurrency."""
        if not streams:
            return []

        results = []
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(self.create_scrape_result, stream, imdb_id, media_type): stream for stream in streams}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)
        return results

    def create_scrape_result(self, stream, imdb_id, media_type):
        """Helper function to create a ScrapeResult object."""
        try:
            guids = Guids(
                imdb_id=imdb_id if imdb_id.startswith("tt") else None,
                tmdb_id=None,
                tvdb_id=None
            )
            return ScrapeResult(
                raw_title=stream["file"]["name"],
                infohash=stream["file"]["hash"],
                guids=guids,
                media_type=media_type,
                source="orionoid"
            )
        except NexusInvalidInfohash:
            return None
