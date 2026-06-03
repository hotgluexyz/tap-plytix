"""Plytix tap class."""

from __future__ import annotations

from hotglue_singer_sdk import Stream, Tap
from hotglue_singer_sdk import typing as th  # JSON schema typing helpers
from typing_extensions import override

from tap_plytix.streams import (
    ProductDetailsStream,
    ProductsStream,
)

STREAM_TYPES = [
    ProductsStream,
    ProductDetailsStream,
]


class TapPlytix(Tap):
    """Singer tap for Plytix."""

    name = "tap-plytix"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
            default="2000-01-01T00:00:00Z",
        ),
        th.Property(
            "api_url",
            th.StringType,
            description="Base URL for the Plytix API",
            default="https://pim.plytix.com/api/v1",
        ),
        th.Property(
            "plytix_api_key",
            th.StringType,
            required=True,
            description="Plytix API key",
        ),
        th.Property(
            "plytix_api_password",
            th.StringType,
            required=True,
            description="Plytix API password",
        ),
    ).to_dict()

    @override
    def discover_streams(self) -> list[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]


if __name__ == "__main__":
    TapPlytix.cli()
