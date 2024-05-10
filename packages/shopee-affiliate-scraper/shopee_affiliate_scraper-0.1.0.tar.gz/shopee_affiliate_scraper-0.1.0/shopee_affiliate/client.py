from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from pydantic import validate_call
from selenium import webdriver
from typing import Optional
import time

DEFAULT_ORIGIN_URL = "https://shopee.com.br"
LIMIT_OF_CUSTOM_URLS_PER_TIME = 5

class ShopeeAffiliate:
    @validate_call
    def __init__(
        self,
        cookies: list[dict],
        origin_url: str = DEFAULT_ORIGIN_URL,
        webdriver_file_path: Optional[str] = None,
        headless = True
    ) -> None:
        options = webdriver.ChromeOptions()

        if webdriver_file_path is None:
            driver_manager = ChromeDriverManager()
            webdriver_file_path = driver_manager.install()

        if headless:
            options.add_argument("--headless")

        service = Service(executable_path = webdriver_file_path)

        self._driver = webdriver.Chrome(
            options = options,
            service = service
        )

        self._driver.get(origin_url)

        for cookie in cookies:
            self._driver.add_cookie(cookie)

    @validate_call
    def _wait_element(self, by: str, selector: str) -> WebElement:
        element = self._driver.find_element(by, selector)
        WebDriverWait(self._driver, 10).until(
            EC.element_to_be_clickable(element)
        )

        return element

    @validate_call
    def create_affiliate_urls(self, original_urls: list[str]) -> list[str]:
        if len(original_urls) > LIMIT_OF_CUSTOM_URLS_PER_TIME:
            raise Exception(f"You cannot create more than {LIMIT_OF_CUSTOM_URLS_PER_TIME} custom URLs at a time!")

        custom_link_creator_url = f"https://affiliate.{DEFAULT_ORIGIN_URL.replace("https://", "").replace("http://", "")}/offer/custom_link"

        self._driver.get(custom_link_creator_url)
        self._driver.implicitly_wait(5)

        original_urls_textarea = self._wait_element(By.CSS_SELECTOR, "#customLink_original_url .ant-input")
        original_urls_textarea.send_keys("\n".join(original_urls))

        get_urls_button = self._driver.find_element(By.CSS_SELECTOR, ".ant-btn-primary")
        get_urls_button.click()

        time.sleep(5)

        custom_urls_textarea = self._driver.find_element(By.CSS_SELECTOR, ".ant-input.ant-input-disabled")
        custom_urls = custom_urls_textarea.text.strip().split("\n")

        return custom_urls

    def close(self) -> None:
        self._driver.close()