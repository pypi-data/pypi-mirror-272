import logging
import os
import time
from typing import Tuple

from cachetools.func import ttl_cache

from fetchfox import rest
from fetchfox.constants.currencies import ALGO, ADA, BOOK, ETH, MATIC

IDS = {
    ALGO: "algorand",
    ADA: "cardano",
    BOOK: "book-2",
    ETH: "ethereum",
    MATIC: "matic-network",
}


BASE_URL = os.environ.get(
    "COINGECKOC_API_BASE_URL",
    "https://api.coingecko.com/api/v3",
)

API_KEY = os.environ.get("COINGECKO_API_KEY")

logger = logging.getLogger(__name__)


def get(service: str, params: dict = None, api_key: str = None) -> Tuple[dict, int]:
    api_key = api_key or API_KEY

    if api_key:
        rate_limit = 30
        headers = {
            "x-cg-demo-api-key": api_key,
        }
    else:
        rate_limit = 5
        headers = {}

    time.sleep(60 / rate_limit)

    return rest.get(
        url=f"{BASE_URL}/{service}",
        headers=headers,
        params=params,
    )


@ttl_cache(ttl=60 * 60)
def get_currency_usd_exchange(currency: str, api_key: str = None):
    currency = currency.strip().upper()
    id = IDS[currency]

    logger.info("fetching exchange for %s (%s)", currency, id)

    response, status_code = get(
        service="simple/price",
        params={
            "ids": id,
            "vs_currencies": "usd",
        },
        api_key=api_key,
    )

    return response[id]["usd"]


@ttl_cache(ttl=60 * 60)
def get_currency_ath_usd(currency: str, api_key: str = None):
    currency = currency.strip().upper()
    id = IDS[currency]

    logger.info("fetching ath for %s (%s)", currency, id)

    response, status_code = get(
        service=f"coins/{id}",
        api_key=api_key,
    )

    return response["market_data"]["ath"]["usd"]


def get_currency_exchange_history(currency: str, days: int = 7, api_key: str = None):
    id = IDS[currency]

    logger.info("fetching exchange history of %s (%s)", currency, id)

    response, status_code = get(
        service=f"coins/{id}/market_chart",
        params={
            "vs_currency": "usd",
            "days": days,
        },
        api_key=api_key,
    )

    return response["prices"]


get_currency_history = get_currency_exchange_history
