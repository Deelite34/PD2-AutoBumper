from time import sleep
from re import match
import os
from sys import exit
import getpass
import configparser

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys


class BumpAutomator:
    """
    Automatically bumps the trades on project diablo 2 website.\n
    Possible contribution ideas below.
    TODO:
        - Fix bugs
        - Upgrade code quality
        - Add support for 2 remaining supported by selenium webdrivers
        - Better handling of bugs and exceptions - display helpful message to user, and do not close the window
          (example - handling of WebDriverException)
        - Launched browser window should be smaller, with help of launch parameters(if possible with current browser)
    """
    def __init__(self):
        self.browser_options = None
        self.browser_name = None
        self.browser_path = None
        self.driver_name = ""
        self.browser_options = None
        self.load_settings()

        # Gets webdriver file from local directory
        self.driver_path = f"{os.getcwd()}/{self.driver_name}.exe".replace('/', '\\')

        if self.driver_name == "chromedriver":
            try:
                self.browser = webdriver.Chrome(executable_path=self.driver_path, options=self.browser_options)
            except WebDriverException:
                input("Error: Unable to launch browser. Did you add correct browser name and path, and did you add the " +
                      "webdriver to the same folder as AutoBumper.exe? You can close this window.")
            else:
                pass
        elif self.driver_name == "geckodriver":
            try:
                self.browser = webdriver.Firefox(executable_path=self.driver_path)
            except WebDriverException:
                input("Error: Unable to launch browser. Did you add correct browser name, path to the .exe file of that browser, " +
                      "and did you add the webdriver to the same folder as AutoBumper.exe? " +
                      "You can close this window.")
            else:
                pass

        self.browser.get("https://www.projectdiablo2.com/login")
        self.__name = None
        self.__password = None
        # Proceed as soon as password field is loaded and usable
        WebDriverWait(self.browser, 10).until(
            ec.presence_of_element_located((By.XPATH, "//input[@type='password']"))
        )

    def load_settings(self):
        """
        Detects if settings file is present and loads it.
        If file is not present, one will be created, user will receive message.
        """
        files = [f for f in os.listdir(os.getcwd()) if os.path.isfile(f)]
        config = configparser.ConfigParser()

        if "settings.ini" in files:
            config.read('settings.ini')
            self.browser_name = config['SETTINGS']['BrowserName']
            self.browser_path = config['SETTINGS']['BrowserPath']
            possible_drivers = {
                'chrome': "chromedriver",
                'firefox': 'geckodriver',
            }
            if self.browser_name in possible_drivers.keys():
                self.driver_name = possible_drivers[self.browser_name.lower()]
                if self.browser_name.lower() == "chrome":
                    self.browser_options = webdriver.ChromeOptions()
                    self.browser_options.binary_location = self.browser_path
                    if config['SETTINGS']['OptionalChromeMuteSound'].lower() == "true":
                        self.browser_options.add_argument("--mute-audio")
                    if config['SETTINGS']['OptionalChromeIgnoreLogs'].lower() == "true":
                        self.browser_options.add_argument('log-level=3')
        else:
            config['SETTINGS'] = {'BrowserName': 'chrome',
                                  'BrowserPath': 'C:/example/exampleFolder/browserfolder/filename.exe',
                                  'OptionalChromeMuteSound': 'False',
                                  'OptionalChromeIgnoreLogs': 'True', }
            with open("settings.ini", "w") as configfile:
                config.write(configfile)
            input("Config file created, please add used browser name and path to the config. Remember to download " +
                  "and add webdriver file to the application directory, otherwise it will not work. " +
                  "You can close this window.")

    def login(self):
        """
        Logs into the website, and moves to manage trades page.
        """
        username_field = self.browser.find_element_by_xpath("//input[@type='text']")
        password_field = self.browser.find_element_by_xpath("//input[@type='password']")
        log_in_button = self.browser.find_element_by_xpath("//button[@form='login-form']")

        # Wait until we get correct credentials from user
        while True:
            try:
                self.__get_credentials()
                username_field.send_keys(self.__name)
                password_field.send_keys(self.__password)

                sleep(1)  # Wait for button to activate
                print("Attempting to log in...")
                log_in_button.click()

                # Wait until main page of website is loaded
                WebDriverWait(self.browser, 7).until(ec.element_to_be_clickable((
                    By.XPATH, "//a[@class='v-btn v-btn--router v-btn--text theme--dark v-size--default']"))
                )
            except TimeoutException:
                print("Login or password incorrect.")
                username_field.send_keys(Keys.CONTROL + "a")
                username_field.send_keys(Keys.DELETE)
                password_field.send_keys(Keys.CONTROL + "a")
                password_field.send_keys(Keys.DELETE)
                username_field.send_keys("")  # Get focus back on username field to not confuse user
                pass
            else:
                print("Logging in..")
                break
        self.browser.get("https://www.projectdiablo2.com/manageTrades")

    def bump_trades(self):
        """
        Handles bumping the trades. Iterates trought all visible divs
        containing items data, and clicks bump button for each one then scrolsl down.
        Respecting site request frequency tolerance with help of sleep()
        """
        self.wait_until_div_is_gone(sleep_time=5)

        show_inactive_button = self.browser.find_element_by_xpath("//div[@class='v-input--selection-controls__ripple primary--text']")
        show_inactive_button.click()
        previous_visible_items = []  # Items visible in previous iteration
        current_visible_items = []   # Currently visible items detected by program
        current_scroll_height = 600  # Scroll height in trades div to be used when there's need to scroll down

        visible_items_divs = self.browser.find_elements_by_xpath("//div[@class='v-virtual-scroll__item']")
        scroll_container = self.browser.find_element_by_xpath("//div[@class='v-virtual-scroll']")
        sleep(3)

        # First iteration. Having it outside while True loop allows us to detect later when end of item list is reached
        for i in visible_items_divs:
            item_text = match('[^\n]*', str(i.text)).group()
            current_visible_items.append(item_text)
        if len(current_visible_items) == 0:
            print("No items detected, ending..")
            return

        print(f"First 6 items: {', '.join(current_visible_items)}", end="\n\n")
        bumped_items_count = 1
        sleep(0.5)
        for index, item in enumerate(current_visible_items):
            print(f"Selected item #{bumped_items_count}: {item}")
            sleep(0.5)
            bump_buttons_to_click = self.browser.find_elements_by_xpath(
                "//button[@class='v-btn v-btn--icon v-btn--round theme--dark v-size--default primary--text']")
            sleep(0.5)
            print(f"Bumping item #{bumped_items_count}", end="\n\n")
            bump_buttons_to_click[index].click()
            self.wait_until_div_is_gone(sleep_time=5)
            bumped_items_count += 1

        print(f'Attempting to move to scroll height: {current_scroll_height}')
        self.browser.execute_script(f"arguments[0].scrollTop = {current_scroll_height}", scroll_container)
        sleep(1)

        while True:
            visible_items_divs = self.browser.find_elements_by_xpath("//div[@class='v-virtual-scroll__item']")
            scroll_container = self.browser.find_element_by_xpath("//div[@class='v-virtual-scroll']")
            previous_visible_items = current_visible_items
            current_visible_items = []
            for i in visible_items_divs:
                item_text = match('[^\n]*', str(i.text)).group()
                current_visible_items.append(item_text)
            if current_visible_items == previous_visible_items:
                print(f"No more items to bump. Last 6 items: {', '.join(current_visible_items)}")
                break

            for index, item in enumerate(current_visible_items):
                print(f"Selected item #{bumped_items_count}: {item}", end="")
                bump_buttons_to_click = self.browser.find_elements_by_xpath(
                    "//button[@class='v-btn v-btn--icon v-btn--round theme--dark v-size--default primary--text']")
                while True:
                    try:
                        sleep(8)
                        print(".", end="\n")
                        WebDriverWait(self.browser, 2).until(
                            ec.element_to_be_clickable(
                                (By.XPATH,
                                 "//button[@class='v-btn v-btn--icon v-btn--round theme--dark v-size--default primary--text'][0]")))
                    except TimeoutException:
                        break
                sleep(0.5)
                print(f"Bumping item #{bumped_items_count}", end="\n\n")
                bump_buttons_to_click[index].click()
                self.wait_until_div_is_gone(sleep_time=8)
                bumped_items_count += 1

            current_scroll_height += 600
            print(f'Attempting to move to scroll height: {current_scroll_height}')
            sleep(2)
            self.browser.execute_script(f"arguments[0].scrollTop = {current_scroll_height}", scroll_container)

    def wait_until_div_is_gone(self, class_name: str = "v-overlay__content", sleep_time: int = 6):
        """
        Hold program until div with specified class name appears, then dissapears,
        after that program can continue.
        With default parameters it will wait until pd2 website loading overlay is gone.
        :param str class_name: contains class name of div to be detected. Default value is v-overlay__content
        :param int sleep_time: Decides how long to wait after div dissapears
        """
        print("Waiting for overlay...")
        sleep(0.2)
        overlay_appeared = False
        while True:
            try:
                sleep(0.5)
                if overlay_appeared is False:
                    overlay_detected = WebDriverWait(self.browser, 0.5).until(
                        ec.presence_of_element_located((By.CLASS_NAME, class_name)))
                    if overlay_detected:
                        overlay_appeared = True
                elif overlay_appeared is True:
                    overlay_dissapeared = WebDriverWait(self.browser, 0.5).until_not(
                        ec.presence_of_element_located((By.CLASS_NAME, class_name)))
                    if overlay_dissapeared:
                        sleep(sleep_time)
                        return
            except TimeoutException:
                continue

    def __get_credentials(self):
        """
        Private method handling getting login and password from user
        """
        self.__name = input("Login: ")
        sleep(0.5)
        self.__password = getpass.getpass()  # gets pass without displaying inputed letters

    def run(self):
        """
        Initiates other functions, specifies things to do before, between, after
        they are called
        """
        self.load_settings()
        self.login()
        self.bump_trades()
        input("Bumping finished, you can quit now..")


if __name__ == "__main__":
    print('Auto Bumper by Blaze#1663 / deelite34\n' +
          'You can report bugs and contribute at https://github.com/Deelite34')
    auto_bumps = BumpAutomator()
    auto_bumps.run()
