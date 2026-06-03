**This tap is in alpha**. Known issues:
- Products are currently full synced


# tap-plytix

A [Singer](https://www.singer.io/) tap that extracts data from **Plytix**. It is built with [hotglue-singer-sdk](https://github.com/hotgluexyz/HotglueSingerSDK) and speaks the standard Singer message protocol on stdout, so you can pair it with any compatible target.

## Features

- **REST**-style HTTP streams (see `client.py` / `streams.py`).
- API key/password authentication.

- Configurable **`api_url`** and optional **`start_date`** (see [Configuration](#configuration)).
- Incremental sync on **`products`** filters by **`modified`** using the tap **`start_date`** / stream bookmark.

### Streams

| Stream | Endpoint / notes | Primary key | Replication key |
| ------ | ---------------- | ----------- | ----------------- |
| `products` | `POST` `/products/search` (pagination in JSON body) | `id` | `modified` |
| `product_details` | `GET` `/products/{product_id}` (child of `products`) | `id` | — |

Pagination uses `pagination.page` and `pagination.page_size` in the request body (default page size 100). The API returns `data` records and a `pagination` object with `total_count`. Rate limits depend on your Plytix plan (HTTP 429 when exceeded).

## Requirements

- Python **3.10+** (see `requires-python` in `pyproject.toml`).

## Installation

1. **Clone** this repository and `cd` into the project directory.
2. **Create `config.json`** in the project root with your credentials and settings (see [Configuration](#configuration) for the fields and an example).
3. **Create a virtual environment** and activate it:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows, use `.venv\Scripts\activate` instead of `source .venv/bin/activate`.

4. **Install the package** in editable mode:

```bash
pip install -e .
```

5. **Run the tap** (with the venv still activated):

```bash
tap-plytix --help
```

## Configuration

| Setting | Type | Required | Default | Description |
| ------- | ---- | -------- | ------- | ----------- |
| `start_date` | string (datetime) | no | `2000-01-01T00:00:00Z` | Earliest record date to sync. |
| `api_url` | string | no | `https://pim.plytix.com/api/v1` | Base URL for the API. |
| `plytix_api_key` | string | yes | — | Plytix API key. |
| `plytix_api_password` | string | yes | — | Plytix API password. |

Run `tap-plytix --about` (or `tap-plytix --about --format=markdown`) for the authoritative schema for your installed version.

### Example `config.json`

```json
{
  "start_date": "2000-01-01T00:00:00Z",
  "api_url": "https://pim.plytix.com/api/v1",
  "plytix_api_key": "YOUR_API_KEY",
  "plytix_api_password": "YOUR_API_PASSWORD"
}
```

Do not commit real credentials. Prefer environment variables or a secrets manager in production.

### Environment-based config

You can load settings from the process environment using `--config=ENV` (the SDK merges env into config). Env names follow the tap’s setting keys (see `tap-plytix --about`).

## Usage

With your virtual environment **activated** and `config.json` in place:

Discover stream catalog:

```bash
tap-plytix --config config.json --discover > catalog.json
```

Run a sync (with optional state):

```bash
tap-plytix --config config.json --catalog catalog.json --state state.json
```

Pipe to any Singer target:

```bash
tap-plytix --config config.json --catalog catalog.json | target-jsonl
```

Inspect built-in settings and stream metadata:

```bash
tap-plytix --about
```

## API / documentation

TODO: Add your vendor’s base URLs, auth docs, and links (compare to the “API hosts” section in a finished tap README).


## License
Apache 2.0 — see `LICENSE` and `pyproject.toml`.
