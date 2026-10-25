"""Environment-based configuration for the BDD test framework."""

import os
from dataclasses import dataclass
from urllib.parse import urlsplit

DEFAULT_BASE_URL = "https://qapracticehub.com/#forms"


def _read_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default

    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"{name} must be a boolean value, got {value!r}")


@dataclass(frozen=True)
class Settings:
    base_url: str
    browser: str
    headless: bool
    wait_timeout: int
    log_level: str

    @classmethod
    def from_environment(cls) -> "Settings":
        browser = os.getenv("BROWSER", "chrome").strip().lower()
        if browser not in {"chrome", "firefox", "edge"}:
            raise ValueError(
                f"Unsupported BROWSER {browser!r}; choose chrome, firefox, or edge"
            )

        try:
            wait_timeout = int(os.getenv("WAIT_TIMEOUT", "10"))
        except ValueError as error:
            raise ValueError("WAIT_TIMEOUT must be a positive integer") from error
        if wait_timeout <= 0:
            raise ValueError("WAIT_TIMEOUT must be a positive integer")

        base_url = os.getenv("BASE_URL", DEFAULT_BASE_URL).strip()
        parsed_url = urlsplit(base_url)
        if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
            raise ValueError("BASE_URL must be an absolute http:// or https:// URL")

        log_level = os.getenv("LOG_LEVEL", "INFO").strip().upper()
        if log_level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
            raise ValueError(
                "LOG_LEVEL must be DEBUG, INFO, WARNING, ERROR, or CRITICAL"
            )

        return cls(
            base_url=base_url,
            browser=browser,
            headless=_read_bool("HEADLESS", True),
            wait_timeout=wait_timeout,
            log_level=log_level,
        )
