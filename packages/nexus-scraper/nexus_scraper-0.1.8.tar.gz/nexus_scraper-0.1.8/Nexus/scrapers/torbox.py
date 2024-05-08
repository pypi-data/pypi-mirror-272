import time
from types import SimpleNamespace
from typing import List

import requests

from Nexus.exceptions import TorBoxException
from Nexus.models import Guids, ScrapeResult


class TorBox:
    def __init__(self):
        self.base_url = "https://api.torbox.app/v1/api"
        self.session = requests.Session()

    def _request(self, endpoint, method = "GET", params = None, data = None, timeout = 30):
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method, url, params=params, json=data, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ReadTimeout as e:
            raise TorBoxException(f"API request timed out: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise TorBoxException(f"API request error: {str(e)}")

    def scrape(self, query = "", media_type = None, timeout = 30) -> List[ScrapeResult]:
        if not query:
            return []

        data = self._request(f"/torrents/search?query={query}", timeout=timeout)
        if not data:
            request = self.add_search_request(query, timeout=timeout)
            if request.get("detail") == "Torrent search stored for searching successfully.":
                time.sleep(5)
                data = self._request(f"/torrents/search?query={query}")
                if not data:
                    return []
        
        items = SimpleNamespace(**data)
        if not items.data:
            return []

        return [ScrapeResult(
            raw_title=item.get("name"),
            infohash=item.get("hash"),
            guids=Guids(
                imdb_id=None,
                tmdb_id=None,
                tvdb_id=None
            ),
            media_type=media_type,
            source="torbox",
            size=item.get("size"),
            seeders=item.get("seeders"),
            leechers=item.get("peers"),
        ) for item in items.data if item.get("hash")]

    def add_search_request(self, query: str, timeout: int = 30):
        return self._request(f"/torrents/storesearch?query={query}", method="PUT", timeout=timeout)
