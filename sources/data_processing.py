# ==============================================================================
# Python 3.9 (64 bits)
# -Vincent Kim-
# V 2.0
# ==============================================================================
import sys #Exit
from datetime import datetime
import re #Regex
from sources.print import ft_print_err, ft_print_err_no_quitt
from sources.convert_text_to_date import ft_convert_text_to_date
# ==============================================================================
def ft_del_duplicates(array, duplicates, dictNames) :

    #CONST
    adhIDName = dictNames["adhIDName"]

    #VAR
    i = 0
    j = 0
    error = False

    print("\n--Recherche des comptes doublons listés--")

    j = 0
    for i in range(len(array[0])) :
        if (array[0][i] == adhIDName) :
            j = i

    for ID in duplicates :
        i = 1
        while (i < len(array)) :
            if (array[i][j] == ID) :
                error = True
                print("[SUPR DBL] Doublon adhérent ID : " + ID + " supprimé")
                array.pop(i)
                i -= 1
            i += 1
# ==============================================================================
def ft_add_column_from_idx_one(array, name, dictNamesOpt) :

    txt = ""

    if (len(dictNamesOpt) > 0)  :
        if (name == dictNamesOpt["itemZipCode_Name"]) :
            ft_print_err_no_quitt("PAS D’ITEM CODE POSTAL DANS LA BASE DE DONNÉES")
            txt = "00000"

        elif (name == dictNamesOpt["itemCity_Name"]) :
            ft_print_err_no_quitt("PAS D’ITEM VILLE DANS LA BASE DE DONNÉES")
            txt = "Inconnu"

        elif (name == dictNamesOpt["itemName_Name"]) :
            ft_print_err_no_quitt("PAS D’ITEM NOM DANS LA BASE DE DONNÉES")
            txt = "Inconnu"

        elif (name == dictNamesOpt["itemFirstName_Name"]) :
            ft_print_err_no_quitt("PAS D’ITEM PRÉNOM DANS LA BASE DE DONNÉES")
            txt = "Inconnu"

    for i in range(1, len(array)) :
        array[i].append(txt)
# ==============================================================================
def ft_save_index_from_name(array, name, dictNamesOpt = []) :

    #VAR
    idx = -1

    for j in range(len(array[0])) :
        if (array[0][j] == name) :
            idx = j

    if (idx == -1) :
        array[0].append(name)
        ft_add_column_from_idx_one(array, name, dictNamesOpt)
        idx = len(array[0]) - 1

    return (idx)
# ==============================================================================
def ft_search_old_data(adhID, array, lastDataIndex, adhIDName) :

    #VAR
    idxAdhID = -1

    if (len(array) == 0) :
        return("")

    for j in range(len(array[0])) :

        if (array[0][j] == adhIDName) :
            idxAdhID = j

    if (idxAdhID == -1) :
        ft_print_err("Erreur, index de \"" + adhIDName + "\" non trouvé depuis ft_search_old_data.")

    for i in range(len(array)) :

        if (array[i][idxAdhID] == adhID) :
            return(array[i][lastDataIndex])

    return("")
# ==============================================================================
def ft_cleaning_order_items(array, toDel, dictNames, order) :

    #CONST
    idxPhone = ft_save_index_from_name([order], dictNames["itemPhone_Name"])
    idxZipCode = ft_save_index_from_name([order], dictNames["itemZipCode_Name"])

    #VAR
    indexes = []
    countDel = 0
    tmp = []
    ret = 0

    #Creating columns
    ft_save_index_from_name(array, dictNames["itemRegion_Name"])
    ft_save_index_from_name(array, dictNames["itemDpt_Name"])

    ft_save_index_from_name(array, dictNames["itemZipCode_Name"], dictNames)
    ft_save_index_from_name(array, dictNames["itemCity_Name"], dictNames)
    ft_save_index_from_name(array, dictNames["itemName_Name"], dictNames)
    ft_save_index_from_name(array, dictNames["itemFirstName_Name"], dictNames)

    for i in range(len(array[0])) :
        for j in range(len(toDel)) :
            if (toDel[j] == array[0][i]) :
                indexes.append(i - countDel)
                countDel += 1
    
    for i in range(len(array)) :
        for j in range(len(indexes)) :
            array[i].pop(indexes[j])

    indexes = []
    for i in range(len(order)) :
        for j in range(len(array[0])) :
            if (order[i] == array[0][j]) :
                indexes.append(j)

    for i in range(len(array)) :
        tmp = []
        for j in range(len(indexes)) :
            tmp.append(array[i][indexes[j]])
        array[i] = tmp

    for i in range(len(array)) :
        array[i][idxZipCode] = array[i][idxZipCode].strip("-")
        if (i > 0 and array[i][idxPhone] != "") :
            array[i][idxPhone] =  "\'" + array[i][idxPhone] + "\'"
# ==============================================================================
def ft_correct_city_code(db, correct_city, only_code, only_Adh_Id, order, dictNames, date) :

    #CONST
    idxAdhID = ft_save_index_from_name([order], dictNames["adhIDName"])
    idxCity = ft_save_index_from_name([order], dictNames["itemCity_Name"])
    idxZipCode = ft_save_index_from_name([order], dictNames["itemZipCode_Name"])

    #VAR
    error = False
    i = 1
    j = 2

    print("\n--CORRECTION DES CODES POSTAUX ET DES VILLES--")

    for i in range(1, len(db)) :

        if (re.search("^[0-9]{5}$", db[i][idxZipCode]) == None) :

            for city in correct_city :
                if (city[0] == db[i][idxCity]) :
                    db[i][idxZipCode] = city[1]

            for code in only_code :
                if (code[0] == db[i][idxZipCode]) :
                    if (db[i][idxCity].strip("-") != "") :
                        ft_print_err_no_quitt("L'ADHERENT ID : " + db[i][idxAdhID] + " A RAJOUTÉ UNE VILLE : \"" + db[i][idxCity].strip("-") +"\"")
                    db[i][idxZipCode] = code[1]
                    db[i][idxCity] = code[2]

            for ID in only_Adh_Id :
                for j in range(2, len(ID)) :
                    if (ID[0] == db[i][idxAdhID]
                        and ft_convert_text_to_date(ID[j][0]) <= ft_convert_text_to_date(date) 
                        and ft_convert_text_to_date(date) < ft_convert_text_to_date(ID[j][1])
                        ) :
                        if (db[i][idxCity].strip("-") != "") :
                            ft_print_err_no_quitt("L'ADHERENT ID : " + db[i][idxAdhID] + " A RAJOUTÉ UNE VILLE : \""
                                + db[i][idxCity].strip("-") +"\"")
                        if (db[i][idxZipCode].strip("-") != "") :
                            ft_print_err_no_quitt("L'ADHERENT ID : " + db[i][idxAdhID] + " A RAJOUTÉ UN CODE POSTAL : \""
                                + db[i][idxZipCode].strip("-") +"\"")
                        db[i][idxZipCode] = ID[1]

            if (re.search("^[0-9]{5}$", db[i][idxZipCode]) == None and re.search("^[A-Z]{2}-", db[i][idxZipCode]) == None) :
                ft_print_err_no_quitt("ERREUR NON ENREGISTRÉE DANS LE CODE POSTAL DE L'ADHÉRENT ID : " + db[i][idxAdhID] + " CODE : \""
                    + db[i][idxZipCode] + "\"")
                error = True

    if (error == True) :
        sys.exit(1)
    else :
        print("[OK] Codes postaux corrigés avec succès.")
# ==============================================================================
def ft_dpt(db, dpt, order, dictNames) :

    #CONST
    idxZipCode = ft_save_index_from_name([order], dictNames["itemZipCode_Name"])
    idxRegion = ft_save_index_from_name([order], dictNames["itemRegion_Name"])
    idxDepartement = ft_save_index_from_name([order], dictNames["itemDpt_Name"])

    #VAR
    i = 0
    j = 1

    for line in db :
        i = 0
        while (i < len(dpt)) :
            j = 1
            while (j < len(dpt[i])) :
                if (re.search("^" + re.escape(dpt[i][j][0]), line[idxZipCode]) != None) :
                    line[idxRegion] = dpt[i][0]
                    line[idxDepartement] = dpt[i][j][1]
                    j = len(dpt[i])
                j += 1
            i += 1
            if (line[idxRegion] != "") :
                i = len(dpt)

        if (line[idxRegion] == "") :
            line[idxRegion] = "Étranger et inclassables"

    for i in range(1, len(db)) :
        db[i][idxZipCode] =  "\'" + db[i][idxZipCode] + "\'"
# ==============================================================================
def ft_order_status(array, dpt, order, dictNames) :

    #CONST
    idxStatus = ft_save_index_from_name(array, dictNames["itemStatus_Name"])

    #VAR
    nat = []
    quitt = []

    for line in array :
        if (line[0] == "OK" or line[0] == "S" or line[0] == array[0][0]) :
            nat.append(line)

    for line in array :
        if ((line[0] != "OK" and line[0] != "S") or line[0] == array[0][0]) :
            quitt.append(line)

    nat = ft_order_by_dpt_and_ID(nat, dpt, order, dictNames)
    quitt = ft_order_by_X_and_ID(quitt, idxStatus, order, dictNames)

    if (len(quitt) > 0) :
        return(nat + quitt[1:len(quitt)])
    else :
        return (nat + quitt)
# ==============================================================================
def ft_order_by_X_and_ID(array, idx, order, dictNames) :

    #CONST
    idxAdhID = ft_save_index_from_name([order], dictNames["adhIDName"])

    #VAR
    minIdx = 1
    sortedArr = []

    sortedArr.append(array[0])

    while (len(array) > 1) :
        minIdx = 1

        for i in range(1, len(array)) :
            if (array[i][idx] < array[minIdx][idx]) :
                minIdx = i
            elif (array[i][idx] == array[minIdx][idx] and int(array[i][idxAdhID]) < int(array[minIdx][idxAdhID])) :
                minIdx = i

        sortedArr.append(array[minIdx])
        array.pop(minIdx)
    return (sortedArr)
# ==============================================================================
def ft_order_by_dpt_and_ID(array, dpt, order, dictNames) :

    #CONST
    idxZipCode = ft_save_index_from_name([order], dictNames["itemZipCode_Name"])
    idxRegion = ft_save_index_from_name([order], dictNames["itemRegion_Name"])

    #VAR
    minIdx = 1
    sortedArr = []
    nameRegion = ""

    sortedArr.append(array[0])

    while (len(array) > 1) :

        for i in range(len(dpt)) :
            nameRegion = dpt[i][0]
            minIdx  = 1

            while (minIdx != 0) :

                minIdx = 0
                for j in range(1, len(array)) :
                    if (array[j][idxRegion] == nameRegion) :
                        minIdx = j

                if (minIdx != 0) :
                    for j in range(1, len(array)) :
                        if (nameRegion != dpt[-1][0] and array[j][idxRegion] == nameRegion and int(array[j][2]) < int(array[minIdx][2])) :
                            minIdx = j
                        elif (nameRegion == dpt[-1][0] and array[j][idxRegion] == nameRegion
                                and array[j][idxZipCode][1:4] < array[minIdx][idxZipCode][1:4]) :
                            minIdx = j

                    sortedArr.append(array[minIdx])
                    array.pop(minIdx)

    return (sortedArr)
# ==============================================================================
def ft_email(email) :

    if (re.search(re.escape("gmail"), email.strip().lower()) != None) :
        return(email[0 : email.find("@")].strip().lower().replace(".", ""))
    else :
        return (email[0 : email.find("@")].strip().lower())
# ==============================================================================
def ft_check_double(array, dictNames, order, name, arg2 = "") :

    #CONST
    idxAdhID = ft_save_index_from_name([order], dictNames["adhIDName"])
    idx = ft_save_index_from_name(array, name)
    idx2 = 0
    if (arg2 != "") :
        idx2 = ft_save_index_from_name(array, arg2)

    #VAR
    test = ""
    test2 = ""
    error = False

    for i in range(1, len(array)) :
        test = array[i][idx]

        if (arg2 != "") :
            test2 = array[i][idx2]

        if (i + 1 < len(array) and test != "") :

            for j in range(i + 1, len(array)):

                if (arg2 != "" and test.strip().lower() ==  array[j][idx].strip().lower()
                    and test2.strip().lower() == array[j][idx2].strip().lower()
                    and test != "Inconnu" and array[j][idx] != "Inconnu" and test2 != "Inconnu" and array[j][idx2] != "Inconnu") :
                    ft_print_err_no_quitt("ERREUR, MÊME NOM PRÉNOM, ADH ID : " + array[i][idxAdhID] + " ET ID : " + array[j][idxAdhID]
                        + " <" + test + " ; " + test2 + ">")
                    error = True

                elif (name == "Téléphone" and test.strip("'").lstrip("0+ ") == array[j][idx].strip("'").lstrip("0+ ")) :
                    ft_print_err_no_quitt("ERREUR, MÊME " + name + " ADH ID : " + array[i][idxAdhID]
                        + " ET ID : " + array[j][idxAdhID] + " <" + test + ">")
                    error = True

                elif (name == "Email" and ft_email(test) == ft_email(array[j][idx])) :
                    ft_print_err_no_quitt("ERREUR, MÊME " + name + " ADH ID : " + array[i][idxAdhID]
                        + " ET ID : " + array[j][idxAdhID] + " <" + test + ">")
                    error = True

                elif (arg2 == "" and test.strip("'").lstrip(" ,0").strip().lower()
                    == array[j][idx].strip("'").lstrip(" ,0").strip().lower()) :
                    ft_print_err_no_quitt("ERREUR, MÊME " + name + " ADH ID : " + array[i][idxAdhID]
                        + " ET ID : " + array[j][idxAdhID] + " <" + test + ">")
                    error = True

    if (error == False) :
        if (arg2 != "") :
            print("[OK] Pas de doublons repérés dans les " + name + " " + arg2 + ".")
        else :
            print("[OK] Pas de doublons repérés dans les " + name + ".")
# ==============================================================================
def ft_correct_inscr_nb(array, correct, date, dictNames) :

    #CONST
    idxAdhID =  ft_save_index_from_name(array, dictNames["adhIDName"])
    idxAdhCount = ft_save_index_from_name(array, dictNames["adhCountName"])
    dateLoc = date.split("/")
    dateLoc = datetime(int(dateLoc[2]), int(dateLoc[1]), int(dateLoc[0]))

    #VAR
    dateArr = ""
    dateMax = ""
    correc = False

    print("\n--CORRECTION DES COMPTEURS D'ADHÉSIONS LISTÉS--")

    for i in range(1, len(array)): 
        for datas in correct :
            dateArr = datas[0].split("/")
            dateArr = datetime(int(dateArr[2]), int(dateArr[1]), int(dateArr[0]))
            dateMax = datas[3].split("/")
            dateMax = datetime(int(dateMax[2]), int(dateMax[1]), int(dateMax[0]))
            if (dateArr <= dateLoc and dateLoc < dateMax and array[i][idxAdhID] == datas[1]) :
                array[i][idxAdhCount] = str(int(array[i][idxAdhCount]) + datas[2])
                print("[CORR ADH COUNT] CORRECTION DU NOMBRE D'ADHÉSIONS, ID : " + array[i][idxAdhID] + " COMPTE FINAL : "
                    + array[i][idxAdhCount])
                correc = True
    if (correc == False) :
        print("[OK] Correction terminée sans effets.")
# ==============================================================================