import time
from typing import List

import requests

from Nexus.exceptions import AnnatarException
from Nexus.models import Guids, NexusSettings, ScrapeResult


class Annatar:
    def __init__(self, settings: NexusSettings):
        self.base_url = settings.annatar_url
        self.session = requests.Session()

    def _request(self, endpoint: str, params: dict = {}) -> dict:
        url = f"{self.base_url}/{endpoint}"
        params.update({"limit": 200})
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise AnnatarException(f"API request error: {e}")

    def scrape(self, query, media_type = "movie", season = 9999, episode = 9999) -> List[ScrapeResult]:
        if not query:
            return []
        
        if not query.startswith("tt"):
            raise AnnatarException("Invalid IMDB ID.")
        
        if not media_type:
            raise AnnatarException("Media type is required.")
        
        if media_type not in ["movie", "show"]:
            raise AnnatarException("Invalid media type. Must be 'movie' or 'show'.")
        
        # de-normalize media type
        if media_type.lower() == "show":
            media_type = "series"
        
        if media_type.lower() == "series" and season != 9999 and episode != 9999:
            endpoint = f"search/imdb/series/{query}"
            params = {"season": season, "episode": episode}
        elif media_type.lower() == "series" and season != 9999 and episode == 9999:
            endpoint = f"search/imdb/series/{query}"
            params = {"season": season}
        else:
            endpoint = f"search/imdb/movie/{query}"
            params = {}

        res = self._request(endpoint, params)
        if not res or "media" not in res:
            time.sleep(3) # start a cold search
            res = self._request(endpoint, params)
            if not res or "media" not in res:
                return []

        results = []
        for result in res.get("media", []):
            results.append(
                ScrapeResult(
                    raw_title=result.get("title"),
                    infohash=result.get("hash"),
                    guids=Guids(
                        imdb_id=query,
                        tmdb_id=None,
                        tvdb_id=None
                    ),
                    media_type=media_type.lower(),
                    source="annatar",
                    size=None,
                    seeders=None,
                    leechers=None
                )
            )
        return results