"""Page object for the QA Practice Hub Forms section."""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.ui import Select, WebDriverWait


class FormsPage:
    FORMS_HEADING = (By.CSS_SELECTOR, "#forms h2")
    COOKIE_BANNER = (By.ID, "cookie-banner")
    COOKIE_ACCEPT = (By.ID, "cookie-accept")

    LOGIN_USERNAME = (By.ID, "login-username")
    LOGIN_PASSWORD = (By.ID, "login-password")
    LOGIN_SUBMIT = (By.ID, "login-submit")
    LOGIN_MESSAGE = (By.ID, "login-message")

    FIRST_NAME = (By.ID, "reg-firstname")
    LAST_NAME = (By.ID, "reg-lastname")
    EMAIL = (By.ID, "reg-email")
    COUNTRY = (By.ID, "reg-country")
    REGISTER_SUBMIT = (By.ID, "register-submit")
    REGISTER_MESSAGE = (By.ID, "register-message")
    REGISTER_CLEAR = (By.ID, "register-clear")

    def __init__(self, driver: WebDriver, timeout: int) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def visible(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(expected.visibility_of_element_located(locator))

    def clickable(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(expected.element_to_be_clickable(locator))

    def click(self, locator: tuple[str, str]) -> None:
        self.clickable(locator).click()

    def enter_text(self, locator: tuple[str, str], value: str) -> None:
        element = self.clickable(locator)
        element.clear()
        if value:
            element.send_keys(value)

    def text_contains(self, locator: tuple[str, str], text: str) -> bool:
        return bool(
            self.wait.until(expected.text_to_be_present_in_element(locator, text))
        )

    def value(self, locator: tuple[str, str]) -> str:
        return self.visible(locator).get_attribute("value") or ""

    def is_visible(self, locator: tuple[str, str]) -> bool:
        elements = self.driver.find_elements(*locator)
        return bool(elements and elements[0].is_displayed())

    def open(self, url: str) -> None:
        self.driver.get(url)
        self.accept_cookies_if_present()
        self.visible(self.FORMS_HEADING)

    def accept_cookies_if_present(self) -> None:
        banners = self.driver.find_elements(*self.COOKIE_BANNER)
        if banners and banners[0].is_displayed():
            self.click(self.COOKIE_ACCEPT)

    def fill_login(self, username: str, password: str) -> None:
        self.enter_text(self.LOGIN_USERNAME, username)
        self.enter_text(self.LOGIN_PASSWORD, password)

    def submit_login(self) -> None:
        self.click(self.LOGIN_SUBMIT)

    def login_message_contains(self, text: str) -> bool:
        return self.text_contains(self.LOGIN_MESSAGE, text)

    def login_values(self) -> tuple[str, str]:
        return self.value(self.LOGIN_USERNAME), self.value(self.LOGIN_PASSWORD)

    def submit_registration(self) -> None:
        self.click(self.REGISTER_SUBMIT)

    def fill_registration(
        self,
        first_name: str,
        last_name: str,
        email: str,
        country: str,
    ) -> None:
        self.enter_text(self.FIRST_NAME, first_name)
        self.enter_text(self.LAST_NAME, last_name)
        self.enter_text(self.EMAIL, email)
        Select(self.clickable(self.COUNTRY)).select_by_value(country)

    def clear_registration(self) -> None:
        self.click(self.REGISTER_CLEAR)

    def registration_message_contains(self, text: str) -> bool:
        return self.text_contains(self.REGISTER_MESSAGE, text)

    def registration_message_is_visible(self) -> bool:
        return self.is_visible(self.REGISTER_MESSAGE)

    def registration_values(self) -> tuple[str, str, str, str]:
        return (
            self.value(self.FIRST_NAME),
            self.value(self.LAST_NAME),
            self.value(self.EMAIL),
            self.value(self.COUNTRY),
        )
