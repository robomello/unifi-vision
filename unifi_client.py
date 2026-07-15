"""UDM Pro auth + stat/device fetch. Read-only (GET only, no write endpoints).

Uses the UniFi OS cookie-session flow with an X-CSRF-Token and
POST /api/auth/login. Adds a re-login-once-on-401 retry since the poller runs
unattended for long stretches and UniFi sessions expire.
"""
from __future__ import annotations

import logging
from urllib.parse import urljoin

import httpx

logger = logging.getLogger(__name__)


class UniFiClient:
    def __init__(self, host: str, user: str, password: str, site: str, timeout: float = 20.0) -> None:
        self.base = host if host.startswith("http") else f"https://{host}"
        self.user = user
        self.password = password
        self.site = site
        self.client = httpx.Client(verify=False, timeout=timeout)
        self.csrf: str | None = None

    def login(self) -> None:
        try:
            r = self.client.post(
                urljoin(self.base, "/api/auth/login"),
                json={"username": self.user, "password": self.password},
            )
            r.raise_for_status()
            self.csrf = r.headers.get("X-CSRF-Token")
        except httpx.HTTPError as exc:
            raise RuntimeError(f"UniFi login failed against {self.base}: {exc}") from exc

    def _headers(self) -> dict[str, str]:
        return {"X-CSRF-Token": self.csrf} if self.csrf else {}

    def get(self, path: str, **params) -> dict | list:
        """GET with one re-login-and-retry on 401 (expired session)."""
        try:
            r = self.client.get(urljoin(self.base, path), headers=self._headers(), params=params)
            if r.status_code == 401:
                logger.info("UniFi session expired (401 on %s), re-logging in", path)
                self.login()
                r = self.client.get(urljoin(self.base, path), headers=self._headers(), params=params)
            r.raise_for_status()
            return r.json()
        except httpx.HTTPError as exc:
            raise RuntimeError(f"UniFi GET {path} failed: {exc}") from exc

    def stat_device(self) -> list[dict]:
        """GET /proxy/network/api/s/<site>/stat/device -> list of device dicts."""
        data = self.get(f"/proxy/network/api/s/{self.site}/stat/device")
        return data.get("data", []) if isinstance(data, dict) else data

    def close(self) -> None:
        self.client.close()
