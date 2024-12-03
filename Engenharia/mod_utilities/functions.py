# ############################################################################ #
#                         GENERAL MODULE - 2024-10-18                          #
# ############################################################################ #
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
#                         IMPORT - 2024-10-22                          #
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
import os
import re
import pandas as pd

from os import path
from dateutil.parser import parse, ParserError
from datetime import datetime as dt, timedelta as td
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #


# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
#                    STATIC FUNCTIONS - 2024-10-18                     #
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
# ============================================================ #
#                         FLATTEN LIST                         #
# ============================================================ #
def Flatten_List(nested_list):
    flat_list = []

    for item in nested_list:
        if isinstance(item, list):
            flat_list.extend(Flatten_List(item))
        else:
            flat_list.append(item)
    return flat_list
# ============================================================ #


# ============================================================ #
#                    TEXT FIND - 2024-03-21                    #
# ============================================================ #
def Text_Find(sourceTxt, searchTxt, getIdx=False):
    """
    Args:
        sourceTxt (str): source text to be analysed
        searchTxt (str): search text to be found
        getIdx (bool): should the found index be returned?
    Return:
        True if searchTxt is found within sourceTxt. False otherwise.
    """

    result = sourceTxt.find(searchTxt)

    if result != -1:
        return True if not getIdx else result

    return False if not getIdx else result
# ============================================================ #


# ============================================================ #
#                     GET DIR - 2024-05-16                     #
# ============================================================ #
def Get_Dir(fileDir):
    match fileDir:
        case None:
            return os.getcwd()
        case False:
            return ""
        case _:
            return fileDir
# ============================================================ #


# ============================================================ #
#                   FILE CHECK - 2024-05-16                    #
# ============================================================ #
def File_Check(fileName, fileDir = None):
    fileDir = Get_Dir(fileDir)
    pth_file = os.path.join(fileDir, fileName)

    if os.path.exists(pth_file):
        return True

    return False
# ============================================================ #


# ============================================================ #
#                    FILE LIST - 2024-10-22                    #
# ============================================================ #
def File_List(srcDir, rgxFilt, flags=re.I, fullPath=True, sort=True):
    list_files = []

    for item in os.listdir(srcDir):
        if re.search(rgxFilt, item, flags) is not None:
            if fullPath:
                list_files.append(path.join(srcDir, item))
            else:
                list_files.append(item)

    if sort:
        list_files.sort()

    return list_files
# ============================================================ #


# ============================================================ #
#                 FILE LIST CHECK - 2024-05-16                 #
# ============================================================ #
def File_List_Check(lst_files, fileDir = None, mode="all"):
    if mode not in ["all", "any"]:
        raise Exception('Error: mode must be either "all" or "any"')

    fileDir = Get_Dir(fileDir)
    lst_check = [File_Check(file, fileDir) for file in lst_files]

    return eval(f"{mode}({lst_check}) and len({lst_check})")
# ============================================================ #


# ============================================================ #
#                   FILE DELETE - 2024-10-22                   #
# ============================================================ #
def File_Delete(srcDir, rgxFilt, flags=re.I, fullPath=True):
    [os.remove(file)
     for file in File_List(srcDir, rgxFilt, flags, fullPath)]
# ============================================================ #


# ============================================================ #
#                    GET TIME - 2024-08-30                     #
# ============================================================ #
def Get_Time(dt_var=None, td_diff=td(), timeFormat="%H:%M:%S"):
    if dt_var:
        return (dt_var + td_diff).strftime(timeFormat)

    return re.sub(r"\.\d+$", "", str(td_diff))
# ============================================================ #


# ============================================================ #
#                   FILTER LIST - 2024-07-15                   #
# ============================================================ #
def Filter_List(lst_items, pattern, regex=False):
    if not regex:
        lst_filtered = [item for item in lst_items if item.find(pattern) != -1]
    else:
        rgx_filter = re.compile(pattern)
        lst_filtered = list(filter(rgx_filter.search, lst_items))

    return lst_filtered
# ============================================================ #


# ============================================================ #
#                   CAMEL CASE - 2024-09-13                    #
# ============================================================ #
def Camel_Case(txt):
    for word in re.findall(r"_\w", txt):
        uWord = word.upper()[-1]
        txt = txt.replace(word, uWord)

    return txt
# ============================================================ #


# ============================================================ #
#               GET ESTIMATED TIME - 2024-09-17                #
# ============================================================ #
def Get_Estimated_Time(dtm_loopStart, loopIdx, remainingLoops):
    totalTime = (dt.now() - dtm_loopStart).seconds
    loopTime = totalTime / loopIdx
    estimatedSeconds = loopTime * remainingLoops
    td_diff = td(seconds=estimatedSeconds)

    return Get_Time(td_diff=td_diff)
# ============================================================ #


# ============================================================ #
#               GET INCREMENT DATA - 2024-10-20                #
# ============================================================ #
def Get_Increment_Data(dtf_a, dtf_b, idVar=None):
    if idVar:
        return dtf_a[~dtf_a[idVar].isin(dtf_b[idVar])]

    return dtf_a[~dtf_a.apply(tuple, 1).isin(dtf_b.apply(tuple, 1))]
# ============================================================ #


# ============================================================ #
#                  GET VAR TYPE - 2024-10-19                   #
# ============================================================ #
def Get_Var_Type(ser_var):
    if any([x for x in ["DT_", "DATA_"] if ser_var.name.startswith(x)]):
        return "DATE", "dte_"

    ser_var = ser_var.replace("0", pd.NA)
    ser_var = ser_var.dropna()
    ser_varValues = ser_var.value_counts()
    lst_varValues = ser_varValues.to_dict().keys()
    numericVar = all([re.search(r"^\d+$", str(x).strip())
                      for x in lst_varValues])
    bitVar = min(lst_varValues) == 0 and max(lst_varValues) == 1

    if not len(ser_var):
        return "TEXT", "txt_"

    if len(ser_varValues) == 2 and numericVar and bitVar:
        return "BIT", "bol_"

    minCharCount = min(ser_var.str.len())
    maxCharCount = max(ser_var.str.len())
    charCountDiff = maxCharCount - minCharCount
    alphaNumericVar = all([re.search(r"\d", str(x).strip())
                           for x in ser_varValues.to_dict().keys()])

    if alphaNumericVar and (charCountDiff < 5 or maxCharCount < 20):
        return f"VARCHAR({maxCharCount})", "cod_"

    return "TEXT", "txt_"
# ============================================================ #


# ============================================================ #
#                  CONVERT DATE - 2024-10-19                   #
# ============================================================ #
def Convert_Date(dateString, lst_dateFormats=None):
    if not isinstance(dateString, str):
        return dateString

    if not lst_dateFormats:
        try:
            return parse(dateString)
        except ParserError:
            return pd.NA

    for dateFormat in lst_dateFormats:
        try:
            return dt.strptime(dateString, dateFormat)
        except ValueError:
            pass
# ============================================================ #


# ============================================================ #
#                 TRANSFORM DATA - 2024-10-20                  #
# ============================================================ #
def Transform_Data(dtf_data, dic_rules):
    if "trim" in dic_rules:
        if "cols" in dic_rules["trim"]:
            lst_cols = dic_rules["trim"]["cols"]
        else:
            lst_cols = dtf_data.columns

        if all([col in dtf_data.columns for col in lst_cols]):
            dtf_data[lst_cols] = dtf_data[lst_cols].apply(
                lambda x: x.str.strip())

    if "noSymbol" in dic_rules:
        if "cols" in dic_rules["noSymbol"]:
            lst_cols = dic_rules["noSymbol"]["cols"]
        else:
            lst_cols = dtf_data.columns

        if all([col in dtf_data.columns for col in lst_cols]):
            dtf_data[lst_cols] = dtf_data[lst_cols].replace(r"\W", "",
                                                            regex=True)

    if "replace" in dic_rules:
        if isinstance(dic_rules["replace"], dict):
            dic_rules["replace"] = [dic_rules["replace"]]

        for dic_replace in dic_rules["replace"]:
            if "cols" in dic_replace:
                lst_cols = dic_replace["cols"]
            else:
                lst_cols = dtf_data.columns

            if all([col in dtf_data.columns for col in lst_cols]):
                old = dic_replace["old"]
                new = dic_replace["new"]
                rgx = dic_replace["rgx"]

                dtf_data[lst_cols] = dtf_data[lst_cols].apply(
                    lambda x: x.str.replace(old, new, regex=rgx))

    if "truncate" in dic_rules:
        if isinstance(dic_rules["truncate"], dict):
            dic_rules["truncate"] = [dic_rules["truncate"]]

        for dic_trunc in dic_rules["truncate"]:
            if "cols" in dic_trunc:
                lst_cols = dic_trunc["cols"]
            else:
                lst_cols = dtf_data.columns

            if all([col in dtf_data.columns for col in lst_cols]):
                start = dic_trunc["start"] if "start" in dic_trunc else None
                stop = dic_trunc["stop"] if "stop" in dic_trunc else None

                dtf_data[lst_cols] = dtf_data[lst_cols].apply(
                    lambda x: x.str.slice(start=start, stop=stop))

    if "fillBlank" in dic_rules:
        for mode in dic_rules["fillBlank"]:
            if "cols" in dic_rules["fillBlank"][mode]:
                lst_cols = dic_rules["fillBlank"][mode]["cols"]
            else:
                lst_cols = dtf_data.columns

            value = dic_rules["fillBlank"][mode]["value"]

            if all([col in dtf_data.columns for col in lst_cols]):
                dtf_data[lst_cols] = dtf_data[lst_cols].replace(r"^\s*$", value,
                                                                regex=True)

    if "fillNa" in dic_rules:
        for mode in dic_rules["fillNa"]:
            if "cols" in dic_rules["fillNa"][mode]:
                lst_cols = dic_rules["fillNa"][mode]["cols"]
            else:
                lst_cols = dtf_data.columns

            value = dic_rules["fillNa"][mode]["value"]

            if all([col in dtf_data.columns for col in lst_cols]):
                dtf_data[lst_cols] = dtf_data[lst_cols].fillna(value)

    if "convert" in dic_rules:
        if "date" in dic_rules["convert"]:
            if "cols" in dic_rules["convert"]["date"]:
                lst_cols = dic_rules["convert"]["date"]["cols"]
            else:
                lst_cols = dtf_data.columns

            if all([col in dtf_data.columns for col in lst_cols]):
                for dateCol in lst_cols:
                    dtf_data[dateCol] = dtf_data[dateCol].apply(
                        lambda x: Convert_Date(x)
                    )
# ============================================================ #


# ============================================================ #
#                  CALCULATE AGE - 2024-10-19                  #
# ============================================================ #
def Calculate_Age(dte_start, dte_end):
    return int((dte_end - dte_start).days / 365.25)
# ============================================================ #
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
# ############################################################################ #
