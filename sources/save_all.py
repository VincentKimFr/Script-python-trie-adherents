# ==============================================================================
# Python 3.9 (64 bits)
# -Vincent Kim-
# V 2.0
# ==============================================================================
import re
from sources.data_processing import ft_save_index_from_name, ft_search_old_data
from sources.files_manipulation import ft_save_and_delete_last
# ==============================================================================
def ft_append_local(array, name, isReg, path, stamp, log, order, dictNames, lenIntroLog) :

    #CONST
    if (isReg == True) :
        idxLoc = ft_save_index_from_name([order], dictNames["itemRegion_Name"])
    else :
        idxLoc = ft_save_index_from_name([order], dictNames["itemDpt_Name"])

    idxStatus = ft_save_index_from_name([order], dictNames["itemStatus_Name"])
    idxAdhID = ft_save_index_from_name([order], dictNames["adhIDName"])
    if (len(log[lenIntroLog -1:lenIntroLog]) != 0)  :
        idxLogChange = ft_save_index_from_name(log[lenIntroLog -1:lenIntroLog], dictNames["itemLogChange_Name"])
        idxLogAdhID = ft_save_index_from_name(log[lenIntroLog -1:lenIntroLog], dictNames["adhIDName"])
        idxLogOldData = ft_save_index_from_name(log[lenIntroLog -1:lenIntroLog], dictNames["itemLogOldData_Name"])
        idxLogNewData = ft_save_index_from_name(log[lenIntroLog -1:lenIntroLog], dictNames["itemLogNewData_Name"])

    #VAR
    loc = []
    logLocal = log[0:lenIntroLog].copy()
    lastReaffect = ""

    loc.append(array[0].copy())

    for i in range(1, len(array)) :

        if (array[i][idxLoc] == name
            and (array[i][idxStatus] == "OK"
                or array[i][idxStatus] == "S"
                or re.search(re.escape(" (actuel)"), array[i][idxStatus]) != None)
        ) :
            loc.append(array[i].copy())

    for i in range(20, len(log)) :

        if (log[i][idxLogChange] == "R" and re.search(re.escape(name), log[i][idxLogOldData]) != None
            and re.search(re.escape(name), log[i][idxLogNewData]) == None) :
            lastReaffect = log[i][idxLogAdhID]

        if (log[i][idxLogChange] != "!P+A+aa") :
            if (re.search(re.escape(name), ft_search_old_data(log[i][idxLogAdhID], array, idxLoc, array[0][idxAdhID])) != None
                or log[i][idxLogAdhID] == lastReaffect
            ) :
                if (ft_search_old_data(log[i][idxLogAdhID], array, idxStatus, array[0][idxAdhID]) == "OK"
                    or ft_search_old_data(log[i][idxLogAdhID], array, idxStatus, array[0][idxAdhID]) == "S"
                    or log[i][idxLogChange] == "!A-"
                    or log[i][idxLogChange] == "!P+C"
                    or log[i][idxLogChange] == "R"
                ):
                    logLocal.append(log[i].copy())
                    if (log[i][idxLogChange] == "R"
                        and re.search(re.escape(name), log[i][idxLogOldData]) != None
                        and re.search(re.escape(name), log[i][idxLogNewData]) == None
                    ) :
                        logLocal[len(logLocal) - 1][idxLogChange] = "R-"
                    elif (log[i][idxLogChange] == "R"
                        and re.search(re.escape(name), log[i][idxLogOldData]) == None
                        and re.search(re.escape(name), log[i][idxLogNewData]) != None
                    ) :
                        logLocal[len(logLocal) - 1][idxLogChange] = "R+"

    ft_save_and_delete_last(loc + logLocal, path, stamp, "_" + name + "_", ".csv")
# ==============================================================================
def ft_save_all(array, log, countTxt, date, dictNames, order, lenIntroLog, FORCE_UPDATE) :

    #CONST
    nameFolder = date.split("/")[2] + "-" + date.split("/")[1] + "-" + date.split("/")[0]
    path = "./" + dictNames["resultFolderName"] + "/" + nameFolder
    stamp = dictNames["stamp"]

    idxStatus = ft_save_index_from_name([order], dictNames["itemStatus_Name"])
    idxAdhID = ft_save_index_from_name([order], dictNames["adhIDName"])
    idxRegion = ft_save_index_from_name([order], dictNames["itemRegion_Name"])
    idxDepartement = ft_save_index_from_name([order], dictNames["itemDpt_Name"])
    if (len(log[lenIntroLog -1:lenIntroLog]) != 0) :
        idxLogChange = ft_save_index_from_name(log[lenIntroLog -1:lenIntroLog], dictNames["itemLogChange_Name"])
        idxLogAdhID = ft_save_index_from_name(log[lenIntroLog -1:lenIntroLog], dictNames["adhIDName"])
        idxLogOldData = ft_save_index_from_name(log[lenIntroLog -1:lenIntroLog], dictNames["itemLogOldData_Name"])
        idxLogNewData = ft_save_index_from_name(log[lenIntroLog -1:lenIntroLog], dictNames["itemLogNewData_Name"])

    #VAR
    nat = []
    logNat = log[0:lenIntroLog].copy()

    quitt = []
    logQuitt = log[0:lenIntroLog].copy()

    notAttrib = []
    logNotAttrib = log[0:lenIntroLog].copy()

    lastReg = ""
    lastDpt = ""

    lastReaffect = ""
    
    ft_save_and_delete_last(countTxt, path, stamp, "_comptage_", ".txt")
    
    nat.append(array[0].copy())
    quitt.append(array[0].copy())
    notAttrib.append(array[0].copy())

    for i in range(1, len(array)) :

        if (array[i][idxStatus] == "OK" or array[i][idxStatus] == "S") :
            nat.append(array[i].copy())
            
        else :
            quitt.append(array[i].copy())

        if ((array[i][idxStatus] == "OK" or array[i][idxStatus] == "S" or re.search(re.escape(" (actuel)"), array[i][idxStatus]) != None)
            and re.search(re.escape("["), array[i][idxRegion]) == None
            and re.search(re.escape("["), array[i][idxDepartement]) == None
        ) :
            notAttrib.append(array[i].copy())

        elif (array[i][idxStatus] == "OK" or array[i][idxStatus] == "S" or re.search(re.escape(" (actuel)"), array[i][idxStatus]) != None) :
            if (re.search(re.escape("["), array[i][idxRegion]) != None and array[i][idxRegion] != lastReg) :
                lastReg = array[i][idxRegion]
                ft_append_local(array, lastReg, True, path, stamp, log, order, dictNames, lenIntroLog)
            if (re.search(re.escape("["), array[i][idxDepartement]) != None and array[i][idxDepartement] != lastDpt) :
                lastDpt = array[i][idxDepartement]
                ft_append_local(array, lastDpt, False, path, stamp, log, order, dictNames, lenIntroLog)


    for i in range(lenIntroLog, len(log)) :

        if (log[i][idxLogChange] != "!P+A+aa") :
            logNat.append(log[i].copy())

        if (log[i][idxLogChange] == "!A-"
            or log[i][idxLogChange] == "A+aa"
            or log[i][idxLogChange] == "!P+C"
            or log[i][idxLogChange] == "!P+A+aa"
            or log[i][idxLogChange] == "P-"
            or (log[i][idxLogChange] == "D" and ft_search_old_data(log[i][idxLogAdhID], array, idxStatus, array[0][idxAdhID]) != "OK"
                and ft_search_old_data(log[i][idxLogAdhID], array, idxStatus, array[0][idxAdhID]) != "S")
        ) :
            logQuitt.append(log[i].copy())

        if (log[i][idxLogChange] == "R" and re.search(re.escape("["), log[i][idxLogOldData]) == None
                and re.search(re.escape("["), log[i][idxLogNewData]) != None) :
            lastReaffect = log[i][idxLogAdhID]

        if (log[i][idxLogChange] != "!P+A+aa") :
            if (
                (re.search(re.escape("["), ft_search_old_data(log[i][idxLogAdhID], array, idxRegion, array[0][idxAdhID])) == None
                    and re.search(re.escape("["), ft_search_old_data(log[i][idxLogAdhID], array, idxDepartement, array[0][idxAdhID])) == None)
                or log[i][idxLogAdhID] == lastReaffect

            ) :
                if (ft_search_old_data(log[i][idxLogAdhID], array, idxStatus, array[0][idxAdhID]) == "OK"
                    or ft_search_old_data(log[i][idxLogAdhID], array, idxStatus, array[0][idxAdhID]) == "S"
                    or log[i][idxLogChange] == "!A-"
                    or log[i][idxLogChange] == "!P+C"
                    or log[i][idxLogChange] == "R"
                ):
                    logNotAttrib.append(log[i].copy())
                    if (log[i][idxLogChange] == "R"
                        and re.search(re.escape("["), log[i][idxLogOldData]) == None
                        and re.search(re.escape("["), log[i][idxLogNewData]) != None
                    ) :
                        logNotAttrib[len(logNotAttrib) - 1][idxLogChange] = "R-"
                    elif (log[i][idxLogChange] == "R"
                        and re.search(re.escape("["), log[i][idxLogOldData]) != None
                        and re.search(re.escape("["), log[i][idxLogNewData]) == None
                    ) :
                        logNotAttrib[len(logNotAttrib) - 1][idxLogChange] = "R+"


    ft_save_and_delete_last(nat + logNat, path, stamp, dictNames["natName"], ".csv")
    ft_save_and_delete_last(quitt + logQuitt, path, stamp, dictNames["quittName"], ".csv")
    ft_save_and_delete_last(notAttrib + logNotAttrib, path, stamp, "_pas-attribués_", ".csv")
# ==============================================================================