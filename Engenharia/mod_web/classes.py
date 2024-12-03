# ############################################################################ #
#                            FUNCTIONS - 2024-11-07                            #
# ############################################################################ #
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
#                     IMPORT MODULES - 2024-10-21                      #
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
import os
import re
import winreg
import zipfile
import requests
import pyperclip
import pandas as pd

from .vars import *
from .functions import *
from time import time, sleep
from mod_utilities import log
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from undetected_chromedriver.patcher import Patcher
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium_recaptcha_solver import RecaptchaSolver, RecaptchaException
from selenium.common.exceptions import (TimeoutException,
                                        StaleElementReferenceException,
                                        MoveTargetOutOfBoundsException,
                                        ElementClickInterceptedException,
                                        ElementNotInteractableException,
                                        NoSuchElementException)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#


# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
#                       WEBCRAWLER - 2024-11-07                        #
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
class webCrawler(object):
    # ============================================================ #
    #                      INIT - 2024-11-07                       #
    # ============================================================ #
    def __init__(self, osVer=None, profileDir=None,
                 profile=None, downloadDir=None, hidden=None):
        self.obj_log = log()
        self.osVer = osVer or 32
        self.profileDir = profileDir or defProfileDir
        self.profile = profile or "Default"
        self.downloadDir = downloadDir or defDownloadDir
        self.hidden = hidden if hidden is not None else True
        self.driver = None
        self.mainTab = None
        self.obj_elmLoc = None
        self.dic_chromeVersion = {
            "browser": self.Get_Chrome_Version("browser"),
            "driver": self.Get_Chrome_Version("driver")
        }
        self.driverPth = path.join(os.getcwd(),
                                   f"chromedriver-win{self.osVer}",
                                   "chromedriver.exe")

        self.Update_Chrome_Driver()
    # ============================================================ #


    # ============================================================ #
    #                       DEL - 2024-06-18                       #
    # ============================================================ #
    def __del__(self):
        try:
            self.driver.quit()
        except AttributeError:
            pass
    # ============================================================ #


    # ============================================================ #
    #               GET CHROME VERSION - 2024-06-11                #
    # ============================================================ #
    def Get_Chrome_Version(self, mode):
        chromeVersion = None

        if mode == "browser":
            obj_regCon = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            obj_regKey = winreg.OpenKey(obj_regCon,
                                        r"Software\Google\Chrome\BLBeacon")
            chromeVersion = winreg.EnumValue(obj_regKey, 0)[1]
        elif mode == "driver":
            pth_chromeDriver = os.path.join(os.getcwd(),
                                            f"chromedriver-win{self.osVer}",
                                            "chromedriver.exe")

            if os.path.exists(pth_chromeDriver):
                osResp = os.popen(f'"{pth_chromeDriver}" -v').read()

                if len(osResp):
                    chromeVersion = re.findall(r"\d+\.\d+\.\d+\.\d+", osResp)[0]

        return chromeVersion
    # ============================================================ #


    # ============================================================ #
    #              UPDATE CHROME DRIVER - 2024-09-13               #
    # ============================================================ #
    def Update_Chrome_Driver(self):
        browserVersion = self.dic_chromeVersion["browser"]
        driverVersion = self.dic_chromeVersion["driver"] or ""

        if browserVersion[:-3] == driverVersion[:-3]:
            return

        url_src = "https://googlechromelabs.github.io/chrome-for-testing/"
        list_tables = pd.read_html(url_src)
        chromeVersion = None
        df_stable = None

        for table in list_tables:
            if df_stable is not None:
                break

            if any(table.columns == "Channel") and chromeVersion is None:
                chromeVersion = table.Version[table.Channel == "Stable"].item()

            if any(table.columns == "URL") and chromeVersion is not None:
                if any(table.URL.str.contains(chromeVersion)):
                    df_stable = table

                    break

        url_chrome = df_stable.URL[(df_stable.Binary == "chromedriver") &
                                   (df_stable.Platform == f"win{self.osVer}")]
        resp = requests.get(url_chrome.item(), allow_redirects=True)
        pth_chromeDriver = os.path.join(os.getcwd(), "../chromedriver.zip")

        with open(pth_chromeDriver, "wb") as file_chrome:
            file_chrome.write(resp.content)

        with zipfile.ZipFile(pth_chromeDriver, "r") as zip_chrome:
            zip_chrome.extractall(os.getcwd())
    # ============================================================ #


    # ============================================================ #
    #                  START DRIVER - 2024-10-21                   #
    # ============================================================ #
    def Start_Driver(self):
        Reset_Chrome_Process()

        # test_ua = ('Mozilla/5.0 (Windows NT 4.0; WOW64) '
        #            'AppleWebKit/537.36 (KHTML, like Gecko) '
        #            'Chrome/37.0.2049.0 Safari/537.36')

        Patcher(self.driverPth, True)

        obj_ua = UserAgent()
        test_ua = obj_ua.random  # "Chrome/37.0.2049.0"
        options = webdriver.ChromeOptions()
        prefs = {"credentials_enable_service": False,
                 "profile.password_manager_enabled": False,
                 "download.default_directory": self.downloadDir}

        # options.add_argument('--no-sandbox')
        # options.add_argument('--ignore-certificate-errors')
        # options.add_argument('--disable-dev-shm-usage')
        # options.add_argument("--disable-notifications")
        # options.add_argument('--disable-extensions')
        # options.add_argument('--disable-gpu')
        options.add_argument(f"--user-data-dir={self.profileDir}")
        options.add_argument(f"--profile-directory={self.profile}")
        options.add_argument("--log-level=3")
        options.add_argument('--hide-crash-restore-bubble')
        # options.add_argument("--page-load-strategy=none")
        # options.add_argument("--remote-debugging-port=9222")
        options.add_experimental_option("prefs", prefs)

        # ++++++++++++ DETECTION EVASION +++++++++++++ #
        options.add_argument("--disable-cache")
        options.add_argument("--start-maximized")
        # options.add_argument(f'--user-agent={test_ua}')
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches",
                                        ["enable-automation"])
        # ++++++++++++++++++++++++++++++++++++++++++++ #

        if self.hidden:
            options.add_argument("--headless=new")

        self.driver = Chrome(self.driverPth, chrome_options=options)

        assert len(self.driver.window_handles) == 1

        dic_userAgents = {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/83.0.4103.53 Safari/537.36'
        }
        cmdSetNavigator = ("Object.defineProperty("
                           "navigator, 'webdriver', {get: () => undefined})")

        self.driver.execute_cdp_cmd('Network.setUserAgentOverride',
                                    dic_userAgents)
        self.driver.execute_script(cmdSetNavigator)
        self.driver.delete_all_cookies()
        # self.driver.maximize_window()

        self.mainTab = self.driver.current_window_handle
        self.obj_elmLoc = Element_Locator(self.driver)
    # ============================================================ #


    # ============================================================ #
    #                  FIND ELEMENT - 2024-09-12                   #
    # ============================================================ #
    def Find_Element(self, filt: str, wbe_ref=None, findAll=None,
                     timeout=None, maxTry=None):
        return self.obj_elmLoc.Find_Element(filt, wbe_ref,
                                            findAll, timeout, maxTry)
    # ============================================================ #


    # ============================================================ #
    #                 CHECK PAGE LOAD - 2024-06-11                 #
    # ============================================================ #
    def Wait_Page_Load(self, timeout=0):
        readyState = 'return document.readyState'
        time_start = time()

        while self.driver.execute_script(readyState) != "complete":
            if 0 < timeout < (time() - time_start):
                return False

        return True
    # ============================================================ #


    # ============================================================ #
    #                     GET URL - 2024-10-21                     #
    # ============================================================ #
    def Get_URL(self, url, filt=None, timeout=15, maxRetries=5):
        for tryCount in range(0, maxRetries):
            self.driver.implicitly_wait(0)
            self.driver.set_page_load_timeout(10 + 2 * tryCount)

            try:
                self.driver.execute_script(f"window.location.href = '{url}';")

                readyState = 'return document.readyState'

                WebDriverWait(self.driver, timeout).until(
                    lambda drv: drv.execute_script(readyState) == 'complete')

                if filt is not None:
                    return self.Find_Element(filt, timeout=timeout)
            except TimeoutException:
                if tryCount >= maxRetries:
                    self.obj_log.Write_Log("Page element load reference fail")

                    return False
    # ============================================================ #


    # ============================================================ #
    #               WAIT ELEMENT APPEAR - 2024-09-12               #
    # ============================================================ #
    def Wait_Element_Appear(self, wbe_ref: any, timeout=0,
                            waitDisplay=True, waitEnable=False):
        if isinstance(wbe_ref, str):
            wbe_ref = self.Find_Element(wbe_ref, timeout=10)

        if waitDisplay or waitEnable:
            time_start = time()

            while True:
                if 0 < timeout < (time() - time_start):
                    return None

                try:
                    bol_display = waitDisplay == wbe_ref.is_displayed()
                    bol_enable = waitDisplay == wbe_ref.is_enabled()

                    if waitDisplay and bol_display or waitEnable and bol_enable:
                        break

                except (StaleElementReferenceException, AttributeError):
                    pass

        return wbe_ref
    # ============================================================ #


    # ============================================================ #
    #             WAIT ELEMENT DISAPPEAR - 2024-09-12              #
    # ============================================================ #
    def Wait_Element_Disappear(self, wbe_ref: any, timeout=0):
        if isinstance(wbe_ref, str):
            wbe_ref = self.Find_Element(wbe_ref, timeout=10)

        time_start = time()

        while wbe_ref.is_displayed():
            if 0 < timeout < (time() - time_start):
                return wbe_ref

        return None
    # ============================================================ #


    # ============================================================ #
    #                 CENTER ELEMENT - 2024-06-17                  #
    # ============================================================ #
    def Center_Element(self, wbe_ref):
        action_chains = ActionChains(self.driver)
        scriptCenterElement = ("arguments[0].scrollIntoView({behavior: 'auto', "
                               "block: 'center', inline: 'center'});")

        try:
            self.driver.execute_script(scriptCenterElement, wbe_ref)
            (action_chains.move_to_element(wbe_ref).perform())
        except MoveTargetOutOfBoundsException:
            pass
    # ============================================================ #


    # ============================================================ #
    #                   SAFE CLICK - 2024-06-11                    #
    # ============================================================ #
    def Safe_Click(self, webElm, timeout=10,
                   lst_popups=None, waitTime=3, maxTry=3):
        if webElm is None:
            return False

        self.driver.maximize_window()

        try:
            if lst_popups is not None:
                self.Close_Popups(lst_popups, 2)

            time_start = time()

            while not timeout or (time() - time_start) < timeout:
                try:
                    webElm = WebDriverWait(self.driver, 1).until(
                        EC.element_to_be_clickable(webElm))

                    break
                except TimeoutException:
                    pass

            if not (webElm.is_displayed() and webElm.is_enabled()):
                raise Exception("Unable to click element")

            for _ in range(0, maxTry):
                self.Center_Element(webElm)

                try:
                    webElm.click()
                    break
                except ElementClickInterceptedException:
                    pass
                finally:
                    sleep(waitTime)
        except StaleElementReferenceException:
            return False

        return True
    # ============================================================ #


    # ============================================================ #
    #                  CLOSE POPUPS - 2024-09-12                   #
    # ============================================================ #
    def Close_Popups(self, lst_popups, waitTime=0):
        for popup in lst_popups:
            sleep(waitTime)

            webElm_popups = self.Find_Element(popup, findAll=True)

            if webElm_popups is not None:
                for webElm in webElm_popups:
                    try:
                        webElm.click()
                    except ElementNotInteractableException:
                        pass
    # ============================================================ #


    # ============================================================ #
    #                  SOLVE CAPTCHA - 2024-09-13                  #
    # ============================================================ #
    def Solve_Captcha(self, wbe_captcha):
        obj_solver = RecaptchaSolver(driver=self.driver)

        try:
            obj_solver.click_recaptcha_v2(iframe=wbe_captcha)

            return True
        except RecaptchaException:
            return False
    # ============================================================ #


    # ============================================================ #
    #                   ISOLATE TAB - 2024-06-11                   #
    # ============================================================ #
    def Isolate_Tab(self, tabHandle=None):
        tabHandle = tabHandle or self.mainTab

        if tabHandle != self.mainTab:
            self.mainTab = tabHandle

        for tab in self.driver.window_handles:
            if tab != tabHandle:
                self.driver.switch_to.window(tab)
                self.driver.close()

        self.driver.switch_to.window(tabHandle)
    # ============================================================ #


    # ============================================================ #
    #                   PASTE CLIP - 2024-06-11                    #
    # ============================================================ #
    def Paste_Clip(self, text):
        pyperclip.copy(text.strip())
        (ActionChains(self.driver)
         .key_down(Keys.CONTROL)
         .send_keys("v")
         .key_up(Keys.CONTROL)
         .perform())
    # ============================================================ #


    # ============================================================ #
    #                REGEX FILTER HTML - 2023-05-15                #
    # ============================================================ #
    def RegEx_Filter_HTML(self, dic_urlFilt):
        from mod_utilities import Flatten_List

        for _ in range(0, 3):
            try:
                fullHTML = [self.driver.page_source]
                urlName = Get_URL_Domain(self.driver.current_url)

                for filtURL, list_dic_filt in dic_urlFilt.items():
                    if f'|{urlName}' in filtURL or filtURL == '*':
                        for dic_filt in list_dic_filt:
                            mode = dic_filt['mode']
                            list_filt = dic_filt['filt']

                            for filt in list_filt:
                                if mode == 'sub':
                                    fullHTML = [
                                        re.sub(filt, '', html, flags=re.S)
                                        for html in fullHTML]
                                elif mode == 'find':
                                    fullHTML = [
                                        re.findall(filt, html, flags=re.S)
                                        for html in fullHTML]
                                elif mode == 'search':
                                    try:
                                        fullHTML = [
                                            re.search(filt, html, re.S)[0]
                                            for html in fullHTML]
                                    except TypeError:
                                        fullHTML = []

                                fullHTML = Flatten_List(fullHTML)

                return fullHTML
            except TimeoutException:
                pass

        return []
    # ============================================================ #
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#


# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
#                     ELEMENT LOCATOR - 2024-11-07                     #
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
class Element_Locator(object):
    # ============================================================ #
    #                      INIT - 2024-10-07                       #
    # ============================================================ #
    def __init__(self, driver):
        self.driver = driver
        self.mode = By.XPATH
        self.findAll = False
        self.maxTry = 1
        self.timeout = 5
        self._wbe_found = None
    # ============================================================ #


    # ============================================================ #
    #                    WBE FOUND - 2024-11-07                    #
    # ============================================================ #
    @property
    def wbe_found(self):
        return self._wbe_found

    @wbe_found.setter
    def wbe_found(self, wbe_found):
        self._wbe_found = wbe_found
    # ============================================================ #


    # ============================================================ #
    #                  FIND ELEMENT - 2024-11-07                   #
    # ============================================================ #
    def Find_Element(self, filt: str, wbe_ref=None, findAll=None,
                     timeout=None, maxTry=None):
        self.findAll = self.findAll if findAll is None else findAll
        self.timeout = timeout or self.timeout
        self.maxTry = maxTry or self.maxTry
        self.wbe_found = None

        wbe_ref = wbe_ref or self.driver
        obj_rgx = re.search(r"(?P<codMode>^\w+(?=:))", filt)

        if obj_rgx is not None:
            if obj_rgx["codMode"] == "css":
                self.mode = By.CSS_SELECTOR
            elif obj_rgx["codMode"] == "scr":
                self.mode = "script"
            else:
                self.mode = By.XPATH
        else:
            self.mode = By.XPATH

        if self.mode == By.XPATH:
            if hasattr(wbe_ref, "get"):
                filt = "//" + re.sub(r"^\.?/+", "", filt)
            else:
                filt = "./" + re.sub(r"^\.?/+", "", filt)

        for _ in range(0, self.maxTry):
            try:
                if self.mode == By.XPATH and filt.find("rgx(") != -1:
                    self.wbe_found = self.Find_Element_By_Regex(filt, wbe_ref)
                elif self.mode == "script":
                    filt = re.sub(r"^scr:\s*", "", filt)
                    time_start = time()

                    while (time() - time_start) < self.timeout:
                        self.wbe_found = self.driver.execute_script(filt)

                        if self.wbe_found is not None:
                            break
                elif self.findAll:
                    self.wbe_found = WebDriverWait(wbe_ref,
                                                    self.timeout).until(
                        EC.presence_of_all_elements_located((self.mode, filt)))
                else:
                    self.wbe_found = WebDriverWait(wbe_ref,
                                                    self.timeout).until(
                        EC.presence_of_element_located((self.mode, filt)))
            except (NoSuchElementException, TimeoutException):
                pass

        return self.wbe_found
    # ============================================================ #


    # ============================================================ #
    #              FIND ELEMENT BY REGEX - 2024-06-13              #
    # ============================================================ #
    def Find_Element_By_Regex(self, webFilt: str, wbe_ref=None):
        wbe_ref = wbe_ref or self.driver
        webFilt = re.sub(r"^\.?/+", "", webFilt)
        lst_search = webFilt.split("/")
        node = re.findall(r"^.+?(?=\[)", webFilt)[0]
        attr = re.findall(r"(?<=rgx\()@?(.+?(?=,))", webFilt)[0].strip()
        rgxFilt = re.findall(r"(?<=rgx\().+?,\s*\'(.+?)(?=\'\s*\))",
                             webFilt.replace(attr, ""))[0].strip()
        lst_children = lst_search[1 - len(lst_search):]
        filtChildren = "/".join(lst_children)

        if hasattr(wbe_ref, "get"):
            lst_elms = wbe_ref.find_elements(By.XPATH, f"//{node}")
        else:
            lst_elms = wbe_ref.find_elements(By.XPATH, f"./{node}")

        lst_matches = None

        for elm in lst_elms:
            if attr == "text":
                attrCont = elm.text
            else:
                attrCont = elm.get_attribute(attr)

            if re.search(rgxFilt, attrCont) is not None:
                if self.findAll:
                    if lst_matches is None:
                        lst_matches = []

                    if len(filtChildren):
                        lst_matches.append(self.Find_Element(filtChildren, elm))
                    else:
                        lst_matches.append(elm)
                else:
                    if len(filtChildren):
                        return self.Find_Element(filtChildren, elm)
                    else:
                        return elm

        return lst_matches
    # ============================================================ #
################################################################################
