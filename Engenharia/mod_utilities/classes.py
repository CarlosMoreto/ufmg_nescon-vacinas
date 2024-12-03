# ############################################################################ #
#                        UTILITIES MODULE - 2024-09-06                         #
# ############################################################################ #
import os
import inspect
import logging

from threading import Thread
from .functions import Get_Time
from datetime import datetime as dt

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
#                           LOG - 2024-09-06                           #
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
class log(object):
    rootModule = False
    dirLog = os.path.join(os.getcwd(), "Logs")
    logFileName = f"log_{dt.now().strftime('%y%m%d')}.log"
    dt_start = dt.now()
    dt_call = dt.now()

    # ============================================================ #
    #                      INIT - 2024-09-09                       #
    # ============================================================ #
    def __init__(self, logFileName=None, rootModule=None, dic_logger=None):
        self.logFileName = logFileName or self.logFileName
        self.rootModule = rootModule or self.rootModule
        self.callTime = 0
        self.totalTime = 0
        pthLog = os.path.join(self.dirLog, self.logFileName)

        if not os.path.exists(self.dirLog):
            os.mkdir(self.dirLog)

        logging.basicConfig(filename=pthLog,
                            filemode="a",
                            level=logging.INFO)

        if self.rootModule:
            self.Write_Log("Script start")

        if dic_logger:
            logging.getLogger(dic_logger["name"]).setLevel(dic_logger["level"])
    # ============================================================ #

    # # ============================================================ #
    # #                       DEL - 2024-06-18                       #
    # # ============================================================ #
    # def __del__(self):
    #     if self.rootModule:
    #         self.Write_Log("Script end")
    # # ============================================================ #


    # ============================================================ #
    #                GET SOURCE CALLER - 2024-09-06                #
    # ============================================================ #
    @staticmethod
    def __Get_Source_Caller__():
        obj_stack = inspect.stack()
        mainIdx = [obj.function for obj in obj_stack].index("<module>") + 1

        if mainIdx == 3:
            return "Main", None

        frm_source = obj_stack[mainIdx - 1]
        frm_caller = obj_stack[mainIdx - 2]
        source = frm_source.function
        caller = frm_caller.function

        if caller in ["__init__", "__del__"]:
            source = frm_caller.frame.f_locals["self"].__class__.__name__

        if source == "<module>":
            source = "Main"

        return source, caller
    # ============================================================ #


    # ============================================================ #
    #                    WRITE LOG - 2024-09-06                    #
    # ============================================================ #
    def Write_Log(self, text=""):
        self.callTime = Get_Time(td_diff=dt.now() - self.dt_call)
        self.totalTime = Get_Time(td_diff=dt.now() - self.dt_start)
        timeNow = Get_Time(dt.now())
        timeStamp = f"{timeNow}: +{self.callTime} --> {self.totalTime}"

        source, caller = self.__Get_Source_Caller__()

        if caller:
            msg = f"{timeStamp}: {source} --> {caller} --> {text}"
        else:
            msg = f"{timeStamp}: {source} --> {text}"

        self.dt_call = dt.now()

        logging.info(msg)
        print(msg)

        return self.callTime
    # ============================================================ #
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #


# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
#                    PROPAGATINGTHREAD - 2024-03-21                    #
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
class PropagatingThread(Thread):
    """
    From URL https://stackoverflow.com/questions/2829329/catch-a-threads-exception-in-the-caller-thread
    By ArtOfWarfare, 2021-07-06 17:22
    """

    def run(self):
        self.exc = None

        try:
            if hasattr(self, '_Thread__target'):
                # Thread uses name mangling prior to Python 3.
                self.ret = self._Thread__target(*self._Thread__args,
                                                **self._Thread__kwargs)
            else:
                self.ret = self._target(*self._args, **self._kwargs)
        except BaseException as e:
            self.exc = e

    def join(self, timeout=None):
        super(PropagatingThread, self).join(timeout)
        if self.exc:
            raise self.exc
        return self.ret
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
# ############################################################################ #
