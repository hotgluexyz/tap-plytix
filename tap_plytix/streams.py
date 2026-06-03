"""Stream type classes for tap-plytix."""

from __future__ import annotations

from typing import Any

import requests
from hotglue_singer_sdk import typing as th
from typing_extensions import override

from tap_plytix.client import PlytixStream

PAGE_SIZE = 100

_PRODUCT_SCHEMA_PROPERTIES = [
    th.Property("id", th.StringType),
    th.Property("sku", th.StringType),
    th.Property("label", th.StringType),
    th.Property("status", th.StringType),
    th.Property("modified", th.DateTimeType),
    th.Property("created", th.DateTimeType),
    th.Property("num_variations", th.IntegerType),
    th.Property("_parent_id", th.StringType),
    th.Property("product_family_id", th.StringType),
    th.Property("product_family_model_id", th.StringType),
    th.Property("modified_user_audit", th.CustomType({"type": "object"})),
    th.Property("overwritten_attributes", th.CustomType({"type": "object"})),
    th.Property("categories", th.CustomType({"type": "array"})),
    th.Property(
        "thumbnail",
        th.ObjectType(th.Property("id", th.StringType)),
    ),
    th.Property("attributes", th.CustomType({"type": "object"})),
]


class ProductsStream(PlytixStream):
    """Products via POST ``/products/search``."""

    name = "products"
    path = "/products/search"
    rest_method = "POST"
    primary_keys = ["id"]
    replication_key = None

    schema = th.PropertiesList(*_PRODUCT_SCHEMA_PROPERTIES).to_dict()

    @override
    def get_child_context(self, record: dict, context: dict | None) -> dict:
        return {"product_id": record["id"]}

    @override
    def prepare_request_payload(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict:
        page = 1 if next_page_token is None else int(next_page_token)
        payload: dict[str, Any] = {
            "pagination": {
                "page": page,
                "page_size": PAGE_SIZE,
                "order": "modified",
            },
        }
        return payload

    @override
    def get_next_page_token(
        self,
        response: requests.Response,
        previous_token: Any | None,
    ) -> Any | None:
        pagination = response.json().get("pagination") or {}
        page = int(pagination.get("page") or 1)
        page_size = int(pagination.get("page_size") or PAGE_SIZE)
        total_count = int(pagination.get("total_count") or 0)
        if page * page_size >= total_count:
            return None
        return page + 1


class ProductDetailsStream(PlytixStream):
    name = "product_details"
    path = "/products/{product_id}"
    parent_stream_type = ProductsStream
    ignore_parent_replication_key = True
    primary_keys = ["id"]
    replication_key = None

    schema = th.PropertiesList(
        th.Property("product_id", th.StringType),
        *_PRODUCT_SCHEMA_PROPERTIES,
        th.Property("gtin", th.StringType),
        th.Property("assets", th.CustomType({"type": "array"})),
    ).to_dict()

    @override
    def get_next_page_token(
        self,
        response: requests.Response,
        previous_token: Any | None,
    ) -> Any | None:
        return None
