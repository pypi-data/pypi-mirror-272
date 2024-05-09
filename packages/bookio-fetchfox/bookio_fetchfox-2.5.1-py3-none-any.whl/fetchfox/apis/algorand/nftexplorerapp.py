import logging
import os
from functools import lru_cache
from typing import Iterable, Tuple

from fetchfox import rest
from fetchfox.checks import check_str

API_KEY = os.getenv("NFTEXPLORER_API_KEY")

BASE_URL = os.getenv(
    "NFTEXPLORER_API_BASE_URL",
    "https://api.nftexplorer.app",
)

logger = logging.getLogger(__name__)


def get(service: str, params: dict = None, version: int = 1, api_key: str = None) -> Tuple[dict, int]:
    api_key = api_key or API_KEY
    check_str(api_key, "nftexplorerapp.api_key")

    return rest.get(
        url=f"{BASE_URL}/v{version}/{service}",
        headers={
            "Authorization": api_key,
        },
        params=params,
        sleep=0.5,
    )


@lru_cache(maxsize=None)
def get_collection_id(creator_address: str, api_key: str) -> str:
    check_str(creator_address, "nftexplorerapp.creator_address")
    creator_address = creator_address.strip().upper()

    response, status_code = get(
        service="collections/search",
        params={
            "q": creator_address,
        },
        api_key=api_key,
    )

    if response.get("error"):
        logger.error("error fetching sales on algorand: %s", response["error"])
        return

    verified = response["results"].get("verified", [])

    if verified:
        return verified[0]["collectionId"]

    recognized = response["results"].get("recognized", [])

    if recognized:
        return recognized[0]["collectionId"]

    return None


def get_collection_sales(creator_address: str, api_key: str = None) -> Iterable[dict]:
    check_str(creator_address, "nftexplorerapp.creator_address")
    creator_address = creator_address.strip().upper()

    collection_id = get_collection_id(creator_address, api_key)

    if not collection_id:
        return

    next_token = ""

    while True:
        response, status_code = get(
            service="/collections/salesHistory",
            params={
                "collectionId": collection_id,
                "nextToken": next_token,
            },
            api_key=api_key,
        )

        if response.get("error"):
            logger.error("error fetching sales on algorand: %s", response["error"])
            return

        yield from response["sales"]

        next_token = response.get("nextToken")

        if not next_token:
            break
