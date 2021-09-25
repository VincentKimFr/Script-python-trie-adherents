# ==============================================================================
# Python 3.9 (64 bits)
# -Vincent Kim-
# V 2.0
# ==============================================================================
import datetime
import re
import sys #Exit
from sources.data_processing import ft_save_index_from_name, ft_search_old_data
from sources.print import ft_print_err_no_quitt
from sources.dates import ft_convert_text_to_date
# ==============================================================================
def ft_statusQuitt(status) :

    switcher = {
        "A quitté l'asso": True,
        "Raisons personelles": True,
        "Départ volontaire": True,
        "Abandon de poste": True,
        "Expulsion": True
    }
    return (switcher.get(status, False))
# ==============================================================================
def ft_member(status) :

    switcher = {
        "OK": True,
        "S": True
    }
    return (switcher.get(status, False))
# ==============================================================================
def ft_logs(lastQuitt, lastNat, array, date, duplicates, delSince, log, order, dictNames) :

    #CONST
    if (len(lastQuitt) > 0) :
        merge = lastNat + lastQuitt[1:len(lastQuitt)]
    else :
        merge = lastNat + lastQuitt
    dateLoc = ft_convert_text_to_date(date)

    idxDate = ft_save_index_from_name([order], dictNames["dateName"])
    idxAdhID = ft_save_index_from_name([order], dictNames["adhIDName"])
    idxPseudo = ft_save_index_from_name([order], dictNames["itemPseudo_Name"])
    idxFirstName = ft_save_index_from_name([order], dictNames["itemFirstName_Name"])
    idxName = ft_save_index_from_name([order], dictNames["itemName_Name"])
    idxEmail = ft_save_index_from_name([order], dictNames["itemEmail_Name"])
    idxPhone = ft_save_index_from_name([order], dictNames["itemPhone_Name"])
    idxCity = ft_save_index_from_name([order], dictNames["itemCity_Name"])
    idxZipCode = ft_save_index_from_name([order], dictNames["itemZipCode_Name"])
    idxRegion = ft_save_index_from_name(array, dictNames["itemRegion_Name"])
    idxDepartement = ft_save_index_from_name(array, dictNames["itemDpt_Name"])
    idxAdhCount = ft_save_index_from_name([order], dictNames["adhCountName"])

    #VAR
    lastStatus = ""
    lastReg = ""
    lastDpt = ""
    lastElem = ""
    dateArr = ""
    elemIndex = 0
    error = False
    dbl = False

    if (len(merge) == 0) :
        log = [[], [], ["Pas d'archives trouvées à analyser"]]
        print("\n--ANALYSE DES ARCHIVES--")
        print("[/!\\] ANNULATION DE LA CRÉATION D'UN HISTORIQUE, ARCHIVES MANQUANTES")
        return(log)

    print("\n--ANALYSE DES ARCHIVES--")

    for i in range(1, len(array)) :

        lastStatus = ft_search_old_data(array[i][idxAdhID], merge, 0, array[0][idxAdhID])
        elemIndex = 0
        if (lastStatus != array[i][elemIndex]) :

            if (lastStatus == "OK" and array[i][elemIndex] == "S") :
                log.append(["!S+", array[i][idxAdhID], array[i][idxPseudo], array[i][idxFirstName], array[i][idxName]])

            elif (lastStatus == "S" and array[i][elemIndex] == "OK") :
                log.append(["S-", array[i][idxAdhID], array[i][idxPseudo], array[i][idxFirstName], array[i][idxName]])

            elif (ft_member(lastStatus) == True and re.search(re.escape(" (actuel)"), array[i][elemIndex]) != None) :
                log.append(["!P+C", array[i][idxAdhID], array[i][idxPseudo], array[i][idxFirstName], array[i][idxName]])

            elif (lastStatus == "" and array[i][elemIndex] == "OK") :
                log.append(["A+", array[i][idxAdhID], array[i][idxPseudo], array[i][idxFirstName], array[i][idxName]])

            elif (lastStatus == "" and array[i][elemIndex] == "S") :
                log.append(["A+", array[i][idxAdhID], array[i][idxPseudo], array[i][idxFirstName], array[i][idxName]])
                ft_print_err_no_quitt("VÉRIFICATION HUMAINE REQUISE : NOUVEL ADHÉRANT EN SURSIS")
                error = True

            elif (ft_member(lastStatus) == True and ft_statusQuitt(array[i][elemIndex]) == True) :
                log.append(["!A-", array[i][idxAdhID], array[i][idxPseudo], array[i][idxFirstName], array[i][idxName], array[0][elemIndex], lastStatus,
                    array[i][elemIndex]])

            elif (re.search(re.escape(" (actuel)"), lastStatus) != None and array[i][elemIndex] == "OK") :
                log.append(["P-", array[i][idxAdhID], array[i][idxPseudo], array[i][idxFirstName], array[i][idxName]])

            elif (re.search(re.escape(" (actuel)"), lastStatus) != None and array[i][elemIndex] == "S") :
                log.append(["P-", array[i][idxAdhID], array[i][idxPseudo], array[i][idxFirstName], array[i][idxName],
                    array[0][idxAdhCount] + " : " + array[i][idxAdhCount],
                    ft_search_old_data(array[i][idxAdhID], merge, idxDate, array[0][idxAdhID]),
                    array[i][idxDate]])
                ft_print_err_no_quitt("VÉRIFICATION HUMAINE REQUISE : RÉHADÉSION EN SURSIS")
                error = True

            elif (ft_statusQuitt(lastStatus) == True and re.search(re.escape(" (réadhésion)"), array[i][elemIndex]) != None) :
                log.append(["!P+A+aa", array[i][idxAdhID], array[i][idxPseudo], array[i][idxFirstName], array[i][idxName]])

            elif ((re.search(re.escape(" (réadhésion)"), lastStatus) != None or ft_statusQuitt(lastStatus) == True)
                    and array[i][elemIndex] == "OK") :
                log.append(["A+aa", array[i][idxAdhID], array[i][idxPseudo], array[i][idxFirstName], array[i][idxName],
                    "Ancien status : " + lastStatus, array[0][idxAdhCount] + " : " + array[i][idxAdhCount],
                    "Anciennes dates : " + ft_search_old_data(array[i][idxAdhID], merge, idxDate, array[0][idxAdhID]), "Nouvelle date : "
                    + array[i][idxDate]])

            elif ((re.search(re.escape(" (réadhésion)"), lastStatus) != None or ft_statusQuitt(lastStatus) == True)
                    and array[i][elemIndex] == "S") :
                log.append(["A+aa", array[i][idxAdhID], array[i][idxPseudo], array[i][idxFirstName], array[i][idxName],
                    array[0][idxAdhCount] + " : " + array[i][idxAdhCount], ft_search_old_data(array[i][idxAdhID], merge, idxDate, array[0][idxAdhID]),
                        array[i][idxDate]])
                ft_print_err_no_quitt("VÉRIFICATION HUMAINE REQUISE : RÉHADÉSION (D'ANCIEN) EN SURSIS")
                error = True

            elif (lastStatus == "" and re.search(re.escape(" (primo)"), array[i][elemIndex]) != None) :
                log.append(["!P+A+", array[i][idxAdhID], array[i][idxPseudo], array[i][idxFirstName], array[i][idxName]])

            elif (lastStatus == "" and ft_statusQuitt(array[i][elemIndex]) == True) :
                print("--DÉPART ÉCLAIR DE L'ADHÉRENT NUMERO : " + array[i][idxAdhID])

            elif (
                (re.search(re.escape(" (primo)"), lastStatus) != None and array[i][elemIndex] == "OK")
                or (re.search(re.escape(" (réadhésion)"), lastStatus) != None and ft_statusQuitt(array[i][elemIndex]) == True)
                ) :
                elemIndex = elemIndex

            else :
                ft_print_err_no_quitt("ERREUR, MODIFICATION DE STATUS IMPRÉVUE, ADH ID : " + array[i][idxAdhID] + " DE \""\
                    + lastStatus + "\" VERS \"" + array[i][elemIndex] + "\"")
                error = True

        elif (ft_search_old_data(array[i][idxAdhID], merge, idxDate, array[0][idxAdhID]) != "") :
            if (lastStatus == "OK" and array[i][idxDate] != ft_search_old_data(array[i][idxAdhID], merge, idxDate, array[0][idxAdhID])) :
                log.append(["C", array[i][idxAdhID], array[i][idxPseudo], array[i][idxFirstName], array[i][idxName], 
                    array[0][idxAdhCount] + " : " + array[i][idxAdhCount],
                    ft_search_old_data(array[i][idxAdhID], merge, idxDate, array[0][idxAdhID]), array[i][idxDate]])
            elif (lastStatus == "S" and array[i][idxDate] != ft_search_old_data(array[i][idxAdhID], merge, idxDate, array[0][idxAdhID])) :
                log.append(["C", array[i][idxAdhID], array[i][idxPseudo], array[i][idxFirstName], array[i][idxName],
                    array[0][idxAdhCount] + " : " + array[i][idxAdhCount],
                    ft_search_old_data(array[i][idxAdhID], merge, idxDate, array[0][idxAdhID]), array[i][idxDate]])
                ft_print_err_no_quitt("VÉRIFICATION HUMAINE REQUISE : RÉHADÉSION SANS SURSIS TERMINE EN SURSIS")
                error = True

        if (lastStatus != "") :

            lastReg = ft_search_old_data(array[i][idxAdhID], merge, idxRegion, array[0][idxAdhID])
            lastDpt = ft_search_old_data(array[i][idxAdhID], merge, idxDepartement, array[0][idxAdhID])

            if (
                (lastReg != array[i][idxRegion]
                    and (re.search(re.escape("["), lastReg) != None
                        or re.search(re.escape("["), array[i][idxRegion]) != None))
                or (lastDpt != array[i][idxDepartement]
                    and (re.search(re.escape("["), lastDpt) != None
                        or re.search(re.escape("["), array[i][idxDepartement]) != None))
            ) :
                log.append(["R", array[i][idxAdhID], array[i][idxPseudo], array[i][idxFirstName], array[i][idxName],
                    array[0][idxRegion] + " / " + array[0][idxDepartement], lastReg + " / " + lastDpt, array[i][idxRegion]
                    + " / " + array[i][idxDepartement]])


            for elemIndex in range(3, 10) : #Data indexes

                lastElem = ft_search_old_data(array[i][idxAdhID], merge, elemIndex, array[0][idxAdhID])

                if (lastElem != array[i][elemIndex]) :
                    if (
                        (elemIndex == idxPhone 
                            and lastElem.strip("'").lstrip("0+ ").strip() != array[i][elemIndex].strip("'").lstrip("0+ ").strip())
                        or ((elemIndex == idxPseudo or elemIndex == idxFirstName or elemIndex == idxName
                                or elemIndex == idxCity or elemIndex == idxZipCode) 
                            and lastElem.strip("'").lstrip(" ,0").strip().lower() 
                            != array[i][elemIndex].strip("'").lstrip(" ,0").strip().lower())
                        or (elemIndex == idxEmail and lastElem.strip() != array[i][elemIndex].strip())
                    ) :
                        log.append(["D", array[i][idxAdhID], array[i][idxPseudo], array[i][idxFirstName], array[i][idxName],
                            array[0][elemIndex], lastElem, array[i][elemIndex]])


    for i in range (1, len(merge)) :
        if (ft_search_old_data(merge[i][idxAdhID], array, idxAdhID, merge[0][idxAdhID]) == "") :
            dbl = False
            for ID in duplicates :
                if (merge[i][idxAdhID] == ID) :
                    dbl = True

            for datas in delSince :
                dateArr = ft_convert_text_to_date(datas[0])
                if (dateLoc >= dateArr and merge[i][idxAdhID] == datas[1]) :
                    dbl = True
            if (dbl == False) :
                ft_print_err_no_quitt("ERREUR : SUPRESSION DE L'ADHÉRENT " + merge[i][idxAdhID] + " DANS LA MISE À JOUR")
                error = True

    if (error == True) :
#        if (
#            (date != "23/06/2020")
#        ) :
        sys.exit(1)
    elif (error == False) :
        print("[OK] Analyse des archives terminées avec succès")

    return(log)
# ==============================================================================