import logging
from typing import Any

class RateLimiterFilter(logging.Filter):
    def filter(self, record: Any): ...
