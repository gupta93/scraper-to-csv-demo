from __future__ import annotations

import time
from typing import Protocol

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

DEFAULT_USER_AGENT = (
    "ScraperToCsvDemo/1.0 (+https://github.com/gupta93/scraper-to-csv-demo; portfolio demo)"
)


class PageFetcher(Protocol):
    def get(self, url: str) -> str: ...


class HttpClient:
    def __init__(
        self,
        *,
        user_agent: str = DEFAULT_USER_AGENT,
        timeout: float = 30.0,
        delay_seconds: float = 0.25,
    ) -> None:
        self.timeout = timeout
        self.delay_seconds = delay_seconds
        self._session = requests.Session()
        self._session.headers.update({"User-Agent": user_agent})
        retry = Retry(
            total=5,
            backoff_factor=0.5,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=("GET",),
        )
        adapter = HTTPAdapter(max_retries=retry)
        self._session.mount("https://", adapter)
        self._session.mount("http://", adapter)

    def get(self, url: str) -> str:
        if self.delay_seconds > 0:
            time.sleep(self.delay_seconds)
        response = self._session.get(url, timeout=self.timeout)
        response.raise_for_status()
        response.encoding = "utf-8"
        return response.text
