"""Behave lifecycle hooks for browser setup, teardown, and diagnostics."""

import logging
import re
from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver

from pages.forms_page import FormsPage
from utils.config import Settings

logger = logging.getLogger(__name__)


def _create_driver(settings: Settings) -> WebDriver:
    if settings.browser == "chrome":
        options = ChromeOptions()
        if settings.headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1440,1000")
        options.add_argument("--disable-background-networking")
        options.add_argument("--no-first-run")
        options.page_load_strategy = "eager"
        driver = webdriver.Chrome(options=options)
    elif settings.browser == "firefox":
        options = FirefoxOptions()
        options.headless = settings.headless
        options.page_load_strategy = "eager"
        driver = webdriver.Firefox(options=options)
    elif settings.browser == "edge":
        options = EdgeOptions()
        if settings.headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1440,1000")
        options.page_load_strategy = "eager"
        driver = webdriver.Edge(options=options)
    else:
        raise ValueError(f"Unsupported browser: {settings.browser}")

    driver.set_page_load_timeout(settings.wait_timeout * 3)
    driver.implicitly_wait(0)
    return driver


def before_all(context) -> None:
    context.settings = Settings.from_environment()
    logging.basicConfig(
        level=getattr(logging, context.settings.log_level),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def before_scenario(context, scenario) -> None:
    context.driver = _create_driver(context.settings)
    context.driver.set_window_size(1440, 1000)
    context.forms_page = FormsPage(context.driver, context.settings.wait_timeout)


def after_step(context, step) -> None:
    if step.status != "failed" or not hasattr(context, "driver"):
        return

    screenshot_dir = Path("reports") / "screenshots"
    safe_name = re.sub(r"[^A-Za-z0-9_-]+", "_", f"{context.scenario.name}_{step.name}")
    safe_name = safe_name[:120].strip("_") or "failed_step"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    screenshot_path = screenshot_dir / f"{safe_name}_{timestamp}.png"

    try:
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        saved = context.driver.save_screenshot(str(screenshot_path))
    except (OSError, WebDriverException):
        logger.exception("Could not capture failure screenshot")
        return
    if not saved:
        logger.warning("WebDriver did not save screenshot to %s", screenshot_path)


def after_scenario(context, scenario) -> None:
    driver = getattr(context, "driver", None)
    if driver is not None:
        try:
            driver.quit()
        except WebDriverException:
            logger.exception("Could not close the browser cleanly")
        finally:
            context.driver = None
