# ############################################################################ #
#                         MODULE PAINELMS - 2024-12-03                         #
# ############################################################################ #
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
#                         IMPORT - 2024-12-03                          #
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
import os
import re
import shutil
import pandas as pd

from .vars import *
from os import path
from time import time, sleep
from datetime import datetime as dt
from dateutil.parser import parse
from mod_web import webCrawler, Send_Keys
from mod_utilities import log, File_Delete, File_List
from selenium.common.exceptions import (TimeoutException,
                                        StaleElementReferenceException,
                                        MoveTargetOutOfBoundsException,
                                        ElementClickInterceptedException,
                                        ElementNotInteractableException,
                                        NoSuchElementException)
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #


# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
#                        PAINELMS - 2024-11-08                         #
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
class painelMs(object):
    # ============================================================ #
    #                      INIT - 2024-10-22                       #
    # ============================================================ #
    def __init__(self, dataDir, hidden=True):
        self.obj_log = log()
        self.dataDir = dataDir
        self.obj_web = webCrawler(hidden=hidden)
    # ============================================================ #


    # ============================================================ #
    #                   ACCESS URL - 2024-10-22                    #
    # ============================================================ #
    def Access_Url(self):
        self.obj_log.Write_Log("Accessing website")

        wbe_divLoad = self.obj_web.Get_URL(url, fltDivLoad)

        self.obj_web.Wait_Element_Disappear(wbe_divLoad)
        self.obj_web.Safe_Click(self.obj_web.Find_Element(fltBtnData))
    # ============================================================ #


    # ============================================================ #
    #                WRITE UPDATE DATE - 2024-12-03                #
    # ============================================================ #
    def Write_Update_Date(self):
        rgx_date = re.compile(r"\b\d+/\d+/\d+\b")

        while True:
            self.obj_log.Write_Log("Writing update file")

            wbe_txtUpdate = self.obj_web.Find_Element(fltTxtUpdate)

            if wbe_txtUpdate is not None:
                filePth = path.join(self.dataDir, "painelMs_datas.csv")
                lst_dates = rgx_date.findall(wbe_txtUpdate.text)
                lst_dates = [parse(d, dayfirst=True) for d in lst_dates]
                dtf_update = pd.DataFrame({"dte_atual": [lst_dates[0]],
                                           "dte_ref": [lst_dates[1]]})

                dtf_update.to_csv(filePth, sep=";",
                                  index=False, encoding="utf-8-sig")

                break
            else:
                sleep(1)
    # ============================================================ #


    # ============================================================ #
    #                  VERIFY FILTER - 2024-11-07                  #
    # ============================================================ #
    def Verify_Filter(self, tagVal, tagFilt):
        wbe_tag = self.obj_web.Find_Element(tagVal, timeout=5)
    
        try:
            if wbe_tag is not None:
                return re.search(tagFilt, wbe_tag.text) is not None
        except StaleElementReferenceException:
            return False
    # ============================================================ #


    # ============================================================ #
    #                  APPLY FILTERS - 2024-11-10                  #
    # ============================================================ #
    def Apply_Filters(self, year):
        for key, dic_filterInfo in dic_filters.items():
            filtVal = dic_filterInfo["flt"]["val"]
            tagFilt = dic_filterInfo["tag"]["flt"]
            tagVal = dic_filterInfo["tag"]["val"]

            if key == "year":
                tagFilt = tagFilt.replace("{year}", str(year))

            while not self.Verify_Filter(tagVal, tagFilt):
                self.obj_log.Write_Log(f"Filtering {key}")

                if key == "year":
                    filtVal = filtVal.replace("{year}", str(year))

                    try:
                        self.obj_web.Find_Element(filtVal).click()
                    except StaleElementReferenceException:
                        sleep(3)
                else:
                    self.obj_web.Safe_Click(self.obj_web.Find_Element(filtVal))

                sleep(1)
    # ============================================================ #


    # ============================================================ #
    #                   EXPORT DATA - 2024-11-07                   #
    # ============================================================ #
    def Export_Data(self, year):
        self.obj_log.Write_Log(f"{year}: exporting data")

        File_Delete(self.obj_web.downloadDir, r"\.xlsx$")

        tries = 0
        maxTries = 3
        waitTime = 45
        fileName = None

        while not fileName and tries < maxTries:
            self.obj_web.Safe_Click(self.obj_web.Find_Element(fltLnkExport))

            tries += 1
            tme_start = time()

            while time() - tme_start < tries*waitTime:
                try:
                    fileName = File_List(self.obj_web.downloadDir,
                                         r"\.xlsx$", fullPath=False)[0]

                    break
                except IndexError:
                    sleep(1)

        if not fileName:
            raise Exception(f"Unable to extract data for {year}")

        shutil.move(path.join(self.obj_web.downloadDir, fileName),
                    path.join(self.dataDir, f"ms_doses_imuno_{year}.xlsx"))
    # ============================================================ #
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
# ############################################################################ #