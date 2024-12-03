import os
import traceback

from os import path
from mod_utilities import log
from mod_painelMs import painelMs
from datetime import datetime as dt


obj_log = log(rootModule=True)
dataDir = path.join(os.getcwd(), "Data")
obj_painelMs = painelMs(dataDir, False)
lst_years = list(range(2023, dt.now().year + 1))

# if True:
try:
    obj_painelMs.obj_web.Start_Driver()

    for year in lst_years:
        obj_painelMs.Access_Url()
        obj_painelMs.Write_Update_Date()
        obj_painelMs.Apply_Filters(year)
        obj_painelMs.Export_Data(year)

    obj_painelMs.obj_web.driver.quit()
except Exception:
    obj_log.Write_Log(traceback.format_exc())
finally:
    del obj_log
