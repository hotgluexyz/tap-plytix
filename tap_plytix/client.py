"""HTTP API client (REST or GraphQL), including PlytixStream base class."""

from __future__ import annotations

import requests
from hotglue_singer_sdk.authenticators import BearerTokenAuthenticator
from hotglue_singer_sdk.streams import RESTStream
from typing_extensions import override


class PlytixStream(RESTStream):
    """Plytix stream class."""

    records_jsonpath = "$.data[*]"

    @override
    @property
    def url_base(self) -> str:
        return self.config.get("api_url", "https://pim.plytix.com/api/v1")

    @property
    def access_token(self) -> str:
        token = getattr(self, "_access_token", None)
        if token is None:
            response = requests.post(
                "https://auth.plytix.com/auth/api/get-token",
                json={
                    "api_key": self.config["plytix_api_key"],
                    "api_password": self.config["plytix_api_password"],
                },
                timeout=30,
            )
            response.raise_for_status()
            token = response.json()["data"][0]["access_token"]
            self._access_token = token
        return token

    @override
    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        return BearerTokenAuthenticator(stream=self, token=self.access_token)

    @override
    @property
    def http_headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
