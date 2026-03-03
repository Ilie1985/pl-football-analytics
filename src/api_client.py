import time
import requests
from typing import Any, Dict, Optional

class FootballDataClient:
    def __init__(self, base_url: str, token: str, min_interval_sec: float = 6.5):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"X-Auth-Token": token})
        self.min_interval_sec = min_interval_sec
        self._last_call_ts = 0.0

    def _throttle(self) -> None:
        now = time.time()
        elapsed = now - self._last_call_ts
        wait = self.min_interval_sec - elapsed
        if wait > 0:
            time.sleep(wait)
        self._last_call_ts = time.time()

    def get(self, path: str, params: Optional[Dict[str, Any]] = None, retries: int = 3) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"

        for attempt in range(retries + 1):
            self._throttle()
            r = self.session.get(url, params=params, timeout=30)

            if r.status_code in (429, 500, 502, 503, 504) and attempt < retries:
                time.sleep(2 * (attempt + 1))
                continue

            if not r.ok:
                # show useful message from API
                try:
                    detail = r.json()
                except Exception:
                    detail = r.text[:500]
                raise requests.HTTPError(
                    f"{r.status_code} for {r.url}\nResponse: {detail}",
                    response=r
                )

            return r.json()

        raise RuntimeError(f"Failed GET {url} after {retries} retries")