import os
from typing import Iterable

from fetchfox import rest

BASE_URL = os.getenv(
    "BOOKIO_BASE_URL",
    "https://api.book.io",
)


def get_campaigns() -> Iterable[dict]:
    response, status_code = rest.get_stream(
        url=f"{BASE_URL}/treasury/v2/campaigns/all.ndjson",
    )

    yield from response
