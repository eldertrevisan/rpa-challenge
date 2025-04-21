from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
from src.resources.config import CHROME_HEADLESS, CHROME_DOWNLOAD_DIR


class RoboSelenium:
    # Class attributes should be instance attributes
    service = Service()
    chrome_options = Options()

    def __init__(self):
        """
        Initializes the Selenium bot, configuring options and required directories.
        """
        self.current_dir = os.path.dirname(__file__)
        self.chrome_dir = os.path.join(self.current_dir, 'chrome')
        self.selenium_dir = os.path.join(self.current_dir, self.chrome_dir, 'selenium')

        if CHROME_DOWNLOAD_DIR is None:
            self.download_dir = os.path.join(self.current_dir, self.chrome_dir, self.selenium_dir, 'download')
            os.makedirs(self.download_dir, exist_ok=True)  # Create the download directory if it doesn't exist
        else:
            self.download_dir = CHROME_DOWNLOAD_DIR
            os.makedirs(self.selenium_dir, exist_ok=True)

        self.service = Service()  # Moved inside __init__
        self.chrome_options = Options()  # Moved inside __init__
        self.options_selenium()

        if CHROME_HEADLESS:
            self.chrome_options.add_argument("--headless=new")  # Runs in headless mode if enabled

        try:
            self.driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize WebDriver: {e}")

    def options_selenium(self):
        """
        Configures Selenium options for Chrome.
        """
        # Sets experimental options for Chrome, adjusting preferences related to downloads and security.
        self.chrome_options.add_experimental_option("prefs", {
            'profile.default_content_setting_values.automatic_downloads': 1, # Allows automatic downloads without asking for confirmation.
            'download.default_directory': self.download_dir,  # Sets the default directory for downloads.
            'download.prompt_for_download': False,  # Disables the download prompt, forcing automatic downloads.
            'download.directory_upgrade': True,  # Allows upgrading the download directory without user interaction.
            'safebrowsing.enabled': True,  # Enables Safe Browsing to prevent malware downloads.
            'credentials_enable_service': False,  # Disables credential storage services.
            'profile': {
                'password_manager_enabled': False  # Disables Chrome's built-in password manager.
            }
        })

        # Prevents Chrome from displaying automation-related warnings in the browser.
        self.chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])

        # Additional Chrome settings:
        self.chrome_options.add_argument("--start-maximized")  # Starts Chrome maximized.
        self.chrome_options.add_argument("--lang=pt")  # Sets the browser language to Portuguese.
        self.chrome_options.add_argument("--disable-webgl")  # Disables WebGL to reduce fingerprinting risks.
        self.chrome_options.add_argument("--window-size=1920x1080")  # Sets the browser window size explicitly.
        self.chrome_options.add_argument(
            "--no-sandbox")  # Disables the sandbox mode (useful for running in containers).
        self.chrome_options.add_argument(
            "--disable-gpu")  # Disables GPU acceleration (helps with compatibility issues).
        self.chrome_options.add_argument('--log-level=3')  # Reduces Chrome's logging output to only display errors.

        # Defines a local directory to store Chrome's user profile data, avoiding the creation of a new session every run.
        local_profile = os.path.join(self.chrome_dir, 'scope_dir')
        os.makedirs(local_profile, exist_ok=True)  # Creates the profile directory if it doesn't exist.
        self.chrome_options.add_argument(
            f"user-data-dir={local_profile}")  # Uses the specified directory as the Chrome profile.
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled") # prevents sites from detecting automated behavior

    def open_url(self, url: str):
        """Opens the specified URL in the browser."""
        self.driver.get(url)

    def close_browser(self):
        """Closes the current browser window."""
        self.driver.close()

    def quit_driver(self):
        """Completely shuts down the Selenium driver."""
        self.driver.quit()

    def document_ready_state(self, timeout: int = 30):
        """Waits until the document's ready state is 'complete'."""
        return WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def find_by_attribute(self, attribute: str, element: str, timeout: int = 10):
        """Finds an element by a given attribute with explicit wait."""
        atrib = None
        if attribute == "id":
            atrib = By.ID
        elif attribute == "xpath":
            atrib = By.XPATH
        elif attribute == "class":
            atrib = By.CLASS_NAME
        elif attribute == "tag":
            atrib = By.TAG_NAME
        else:
            raise ValueError(f"Invalid attribute: {attribute}")

        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((atrib, element)))

    def find_by_label(self, label, timeout=10):
        return WebDriverWait(label, timeout).until(
            EC.presence_of_element_located((By.XPATH, "./following-sibling::input"))
        )

    def send_key(self, element, text: str):
        """Sends text to an input field."""
        element.send_keys(text)

    def click_xpath(self, xpath: str, timeout: int = 10):
        """Waits until an element is clickable and clicks it."""
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))

    def check_title(self, title: str, timeout: int = 10):
        """Checks if the page title matches the expected title."""
        return WebDriverWait(self.driver, timeout).until(EC.title_is(title))

    def mouse_click(self, element: str):
        """Performs a JavaScript click on an element found by XPath."""
        try:
            element_found = self.find_by_attribute('xpath', element)
            self.driver.execute_script("arguments[0].click();", element_found)
        except Exception as e:
            raise RuntimeError(f"Error clicking element {element}: {e}")

    def scroll_to_element(self, element: str):
        """Scrolls the screen to a specific element."""
        element_found = self.find_by_attribute('xpath', element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element_found)

    def exec_javascript(self, script: str):
        """Executes a JavaScript script in the context of the loaded page."""
        self.driver.execute_script(script)
