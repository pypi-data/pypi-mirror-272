import requests

from Nexus.exceptions import ApibayException
from Nexus.models import Guids, ScrapeResult


class Apibay:
    """`Apibay` scraper class."""

    def __init__(self):
        self.url = "https://apibay.org"
        self.session = requests.Session()
        self.session.headers.update({'Connection': 'keep-alive'})
        self.timeout = 10  # seconds

    def scrape(self, query: str, **kwargs) -> list[ScrapeResult]:
        """Search torrents from `Apibay`."""
        if not query:
            raise ApibayException("Query cannot be empty")
        
        query_type = 'imdb' if query.startswith('tt') else 'q'
        url = f"{self.url}/q.php?{query_type}={query}"
        results = []
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            torrents = response.json()
        except requests.RequestException as e:
            raise ApibayException(f"Failed to fetch data from Apibay: {str(e)}")

        if not torrents or torrents[0].get("name") == "No results returned":
            return results

        for torrent in filter(lambda x: len(x.get("info_hash", "")) == 40, torrents):
            results.append(ScrapeResult(
                raw_title=torrent["name"],
                infohash=torrent["info_hash"],
                guids=Guids(
                    imdb_id=torrent.get("imdb") if torrent.get("imdb") else None,
                    tmdb_id=None,
                    tvdb_id=None
                ),
                media_type=None,
                source="apibay",
                size=torrent["size"],
                seeders=int(torrent["seeders"]),
                leechers=int(torrent["leechers"]),
            ))

        return results
