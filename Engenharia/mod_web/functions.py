# ############################################################################ #
#                            FUNCTIONS - 2024-10-21                            #
# ############################################################################ #
# ============================================================ #
#              RESET CHROME PROCESS - 2024-06-11               #
# ============================================================ #
def Reset_Chrome_Process():
    import psutil

    for proc in psutil.process_iter():
        if proc.name() in ["chrome.exe", "chromedriver.exe"]:
            try:
                proc.kill()
            except (psutil.NoSuchProcess, ProcessLookupError):
                pass
# ============================================================ #


# ============================================================ #
#                 GET URL DOMAIN - 2023-05-09                  #
# ============================================================ #
def Get_URL_Domain(url):
    import re

    url = re.sub(r"^https?:/+(w{3}\.)?"
                 r"|(?<=\.)\w+/.*"
                 r"|(?<=\.)(com|br|net|gov)", "", url)

    return re.sub(r"\.+", ".", url)
# ============================================================ #


# ============================================================ #
#                    SEND KEYS - 2024-06-12                    #
# ============================================================ #
def Send_Keys(webElm, list_keystrokes, keySpeed=0):
    from time import sleep

    # (ActionChains(driver)
    #  .key_down(Keys.SHIFT)
    #  .send_keys("a")
    #  .key_up(Keys.SHIFT)
    #  .send_keys("b")
    #  .perform())

    for keystroke in list_keystrokes:
        if keySpeed:
            for char in keystroke:
                webElm.send_keys(char)
                sleep(keySpeed / 1000)
        else:
            webElm.send_keys(keystroke)
# ============================================================ #


# ============================================================ #
#                  SELECT OPTION - 2024-06-11                  #
# ============================================================ #
def Select_Option(wbe_select, option, mode=None):
    from selenium.webdriver.support.select import Select

    obj_select = Select(wbe_select)

    if mode == "value":
        obj_select.select_by_value(option)
    elif mode == "index":
        obj_select.select_by_index(option)
    else:
        obj_select.select_by_visible_text(option)
# ============================================================ #


# ============================================================ #
#                  TOGGLE OPTION - 2024-06-13                  #
# ============================================================ #
def Toggle_Option(we_chkElm, toggle: bool):
    from time import sleep

    while we_chkElm.is_selected() != toggle:
        we_chkElm.click()
        sleep(1)
# ============================================================ #


# ============================================================ #
#                  DOWNLOAD FILE - 2024-05-28                  #
# ============================================================ #
def Download_File(url, pth_dest):
    import requests

    obj_resp = requests.get(url, allow_redirects=True)

    with open(pth_dest, "wb") as obj_file:
        obj_file.write(obj_resp.content)
# ============================================================ #
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
################################################################################
