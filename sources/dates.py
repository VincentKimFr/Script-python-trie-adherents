# ==============================================================================
# Python 3.9 (64 bits)
# -Vincent Kim-
# V 2.0
# ==============================================================================
import datetime
import re #Regex
from sources.data_processing import ft_save_index_from_name, ft_search_old_data
from sources.print import ft_print_err, ft_print_err_no_quitt
from sources.convert_text_to_date import ft_convert_text_to_date
# ==============================================================================
def ft_calculing_date(count, date) :

    date = ft_convert_text_to_date(date) \
        - datetime.timedelta(days = 365) \
        + datetime.timedelta(days = int(count))

    date = "{:0>2d}".format(date.day) + "/" + "{:0>2d}".format(date.month) + "/" + str(date.year);

    return(date)
# ==============================================================================
def ft_dates(db, dictNames, lastNat, lastQuitt, date) :

    #CONST
    dateName = dictNames["dateName"]
    oldDatesName = dictNames["oldDatesName"]
    adhIDName = dictNames["adhIDName"]

    if (len(lastQuitt) > 0) :
        lastDB = lastNat + lastQuitt[1:len(lastQuitt)]
    else :
        lastDB = lastNat + lastQuitt

    dateIndex = ft_save_index_from_name(db, dateName)
    oldDatesIndex = ft_save_index_from_name(db, oldDatesName)
    memberDateCountIndex = ft_save_index_from_name(db, dictNames["memberDateCountName"])
    adhIDIndex = ft_save_index_from_name(db, adhIDName)

    #VAR
    counterDays = 0

    lastDBDateIndex = -1
    lastDBOldDatesIndex = -1
    
    for i in range(1, len(db)) :
        if (db[i][memberDateCountIndex] != "Compteur adhésion"
            and db[i][memberDateCountIndex] != "Attente de chèque"
            and db[i][memberDateCountIndex] != "A quitté l'asso"
            and db[i][memberDateCountIndex] != "Jamais adhéré"
            and db[i][memberDateCountIndex] != "Doit être relancé => 0"
            and db[i][memberDateCountIndex] != "Adhésion non-payée"
        ) :
            counterDays = int(db[i][memberDateCountIndex].replace("Doit être relancé =>", "").strip())
            db[i][dateIndex] = ft_calculing_date(counterDays, date)

    if (len(lastDB) != 0) :
        lastDBDateIndex = ft_save_index_from_name(lastDB, dateName)
        lastDBOldDatesIndex = ft_save_index_from_name(lastDB, oldDatesName)

        for i in range(1, len(db)) :
            if (db[i][dateIndex] == "") :
                db[i][dateIndex] = ft_search_old_data(db[i][adhIDIndex], lastDB, lastDBDateIndex, adhIDName)

            if (db[i][oldDatesIndex] == "") :
                db[i][oldDatesIndex] = ft_search_old_data(db[i][adhIDIndex], lastDB, lastDBOldDatesIndex, adhIDName)

    for i in range(1, len(db)) :
        if (db[i][dateIndex] != "" and re.search(re.escape(db[i][dateIndex]), db[i][oldDatesIndex]) == None) :
            if (db[i][oldDatesIndex] == "") :
                db[i][oldDatesIndex] += db[i][dateIndex]
            else :
                db[i][oldDatesIndex] += ", " + db[i][dateIndex]
# ==============================================================================
def ft_only_members_and_dates_and_count(arrayDB, dictNames, lastNat, lastQuitt, date, quittStatusArray) :

    #CONST
    countAdhIndex = ft_save_index_from_name(arrayDB, dictNames["adhCountName"])
    memberDateCountIndex = ft_save_index_from_name(arrayDB, dictNames["memberDateCountName"])
    membershipCountIndex = ft_save_index_from_name(arrayDB, dictNames["adhCountName"])
    adhIDIndex = ft_save_index_from_name(arrayDB, dictNames["adhIDName"])
    idxStatus = ft_save_index_from_name(arrayDB, dictNames["itemStatus_Name"])
    if (len(lastNat) != 0) :
        idxlastNatStatus = ft_save_index_from_name(lastNat, dictNames["itemStatus_Name"])
    if (len(lastQuitt) != 0) :
        idxlastQuittStatus = ft_save_index_from_name(lastQuitt, dictNames["itemStatus_Name"])
    

    #VAR
    i = 1
    j = 0
    k = 2
    txt = date + "\n";
    quittStatus = ""
    natStatus = ""

    accounts = len(arrayDB) - 1
    accountsNoMembers = 0

    primoNoPaid = 0
    ancientsNoPaid = 0
    actualNoPaid = 0

    joinAgain = 0
    warn = 0
    quitt = 0
    members = 0

    volontary = 0
    desertion = 0
    fired = 0
    personnal_reasons = 0

    known_cases = 0
    unpaid = 0
    printed = False

    print("\n--ANALYSE DES STATUS DES MEMBRES--")

    i = 1
    while (i < len(arrayDB)) :
        if (int(arrayDB[i][countAdhIndex]) == 0) :
            accountsNoMembers += 1
            arrayDB.pop(i)
            i -= 1
        i += 1

    ft_dates(arrayDB, dictNames, lastNat, lastQuitt, date)
    
    for i in range(1, len(arrayDB)) :

        if (len(lastQuitt) != 0) :
            quittStatus = ft_search_old_data(arrayDB[i][adhIDIndex], lastQuitt, idxlastQuittStatus, dictNames["adhIDName"])

        if (len(lastNat) != 0) :
            natStatus = ft_search_old_data(arrayDB[i][adhIDIndex], lastNat, idxlastNatStatus, dictNames["adhIDName"])

        if (arrayDB[i][memberDateCountIndex] == "A quitté l'asso") :
            quitt += 1
            arrayDB[i][idxStatus] = "A quitté l'asso"
            for j in range(len(quittStatusArray)) :
                for k in range(2, len(quittStatusArray[j])) :
                    if (arrayDB[i][adhIDIndex] == quittStatusArray[j][0]
                        and ft_convert_text_to_date(quittStatusArray[j][k][0]) <= ft_convert_text_to_date(date) 
                        and ft_convert_text_to_date(date) < ft_convert_text_to_date(quittStatusArray[j][k][1])
                        ) :
                        arrayDB[i][idxStatus] = quittStatusArray[j][1]
                        if (arrayDB[i][idxStatus] == "Abandon de poste") :
                            desertion += 1
                            quitt -= 1
                        elif (arrayDB[i][idxStatus] == "Raisons personelles") :
                            personnal_reasons += 1
                            quitt -= 1
                        elif (arrayDB[i][idxStatus] == "Expulsion") :
                            fired += 1
                            quitt -= 1
                        elif (arrayDB[i][idxStatus] == "Départ volontaire") :
                            volontary += 1
                            quitt -= 1
        
        elif (arrayDB[i][memberDateCountIndex] == "Adhésion non-payée"
            or arrayDB[i][memberDateCountIndex] == "Attente de chèque") :

            if (len(lastQuitt) == 0 and len(lastNat) == 0 and int(arrayDB[i][membershipCountIndex]) > 1) :
                ancientsNoPaid += 1
                arrayDB[i][idxStatus] = arrayDB[i][memberDateCountIndex] + " (réadhésion)"
                ft_print_err_no_quitt("IMPAYÉ SANS HISTORIQUE DE L'ANCIEN MEMBRE ADHÉRENT ID : " + arrayDB[i][adhIDIndex]
                        + " HYPOTHÈSE AUTOATIQUE : RÉADHÉSION")
                printed = True

            elif (int(arrayDB[i][membershipCountIndex]) == 1) :
                primoNoPaid += 1
                arrayDB[i][idxStatus] = arrayDB[i][memberDateCountIndex] + " (primo)"

            elif (natStatus != "" or quittStatus.find(" (actuel)") != -1) :
                actualNoPaid += 1
                arrayDB[i][idxStatus] = arrayDB[i][memberDateCountIndex] + " (actuel)"

            elif (quittStatus == "A quitté l'asso"
                or quittStatus == "Raisons personelles"
                or quittStatus == "Départ volontaire"
                or quittStatus == "Abandon de poste"
                or quittStatus.find(" (réadhésion)") != -1
            ) :
                ancientsNoPaid += 1
                arrayDB[i][idxStatus] = arrayDB[i][memberDateCountIndex] + " (réadhésion)"
                if (quittStatus.find(" (réadhésion)") == -1) :
                    ft_print_err_no_quitt("RETOUR (NON PAYÉ) DE L'ADHÉRENT ID : " + arrayDB[i][adhIDIndex]
                        + " RAISON DU DÉPART : " + quittStatus)
                    printed = True

            elif (quittStatus == "Expulsion"
                or quittStatus.find(" (retour d'expulsion)") != -1) :
                ancientsNoPaid += 1
                arrayDB[i][idxStatus] = arrayDB[i][memberDateCountIndex] + " (retour d'expulsion)"
                if (quittStatus.find(" (retour d'expulsion)") == -1) :
                    ft_print_err_no_quitt("RETOUR D'EXPULSION DE L'ADHÉRENT ID : " + arrayDB[i][adhIDIndex])
                    printed = True

            else :
                primoNoPaid += 1
                arrayDB[i][idxStatus] = arrayDB[i][memberDateCountIndex] + " (primo)"
                ft_print_err_no_quitt("ERREUR : ADHÉRENT ID : " + arrayDB[i][adhIDIndex] + " IMPAYÉ, ADH > 1, MAIS INTROUVABLE EN ARCHIVES")
                printed = True

        elif (arrayDB[i][memberDateCountIndex] == "Doit être relancé => 0") :
            warn += 1
            arrayDB[i][idxStatus] = "S"

        elif (quittStatus == "A quitté l'asso"
            or quittStatus == "Raisons personelles"
            or quittStatus == "Départ volontaire"
            or quittStatus == "Abandon de poste"
            or quittStatus.find(" (réadhésion)") != -1
        ) :
            joinAgain += 1
            arrayDB[i][idxStatus] = "OK"
            if (quittStatus.find(" (réadhésion)") == -1) :
                ft_print_err_no_quitt("RETOUR DE L'ADHÉRENT ID : " + arrayDB[i][adhIDIndex] + " RAISON DU DÉPART : " + quittStatus)
                printed = True
            elif (quittStatus == "Raisons personelles") :
                ft_print_err_no_quitt("RETOUR DE L'ADHÉRENT ID : " + arrayDB[i][adhIDIndex] + " RAISON DU DÉPART : " + quittStatus)
                printed = True
            elif (quittStatus == "Départ volontaire") :
                ft_print_err_no_quitt("RETOUR DE L'ADHÉRENT ID : " + arrayDB[i][adhIDIndex] + " RAISON DU DÉPART : " + quittStatus)
                printed = True
            elif (quittStatus == "Abandon de poste") :
                ft_print_err_no_quitt("RETOUR DE L'ADHÉRENT ID : " + arrayDB[i][adhIDIndex] + " RAISON DU DÉPART : " + quittStatus)
                printed = True


        elif (quittStatus == "Expulsion"
            or quittStatus.find(" (retour d'expulsion)") != -1) :
            joinAgain += 1
            arrayDB[i][idxStatus] = "OK"
            if (quittStatus.find(" (retour d'expulsion)") == -1) :
                    ft_print_err_no_quitt("RETOUR D'EXPULSION DE L'ADHÉRENT ID : " + arrayDB[i][adhIDIndex])
                    printed = True

        else :
            arrayDB[i][idxStatus] = "OK"
            members += 1

    known_cases = desertion + fired + volontary + personnal_reasons
    unpaid = primoNoPaid + ancientsNoPaid + actualNoPaid

    txt += str(accounts) + " comptes.\n"
    txt += str(accountsNoMembers) + " non membres, reste " + str(accounts - accountsNoMembers) + "\n"
    txt += str(primoNoPaid) + " primo-impayés, reste " + str(accounts - accountsNoMembers - primoNoPaid) + "\n"
    txt += str(ancientsNoPaid) + " ex-abandons impayés, reste " + str(accounts - accountsNoMembers - primoNoPaid - ancientsNoPaid) + "\n"
    txt += str(actualNoPaid) + " renouvellements impayés, reste " + str(accounts - accountsNoMembers - unpaid) + "\n"
    txt += str(desertion) + " abandons de poste, " + str(fired) + " expulsions, "\
        + str(volontary) + " départs volontaires, " + str(personnal_reasons) + " raisons personnelles, total "\
        + str(known_cases)\
        + " reste " + str(accounts - accountsNoMembers - unpaid - known_cases) + "\n"
    txt += str(quitt) + " abandons, reste " + str(accounts - accountsNoMembers - unpaid - known_cases - quitt) + "\n"
    txt += str(warn) + " adhérents en sursis\n"
    txt += str(accounts - accountsNoMembers - unpaid - known_cases - quitt - warn) + " adhérents hors sursis (" + str(members + joinAgain) + ")\n"
    txt += "Dont " + str(joinAgain) + " réadhésion\n"
    
    if (accounts - accountsNoMembers - unpaid - known_cases - quitt - warn != members + joinAgain) :
        ft_print_err("ERREUR : DEUX CALCULS DIFFÉRENTS DU NOMBRE D'ADHÉRENTS : "
            + str(accounts - accountsNoMembers - unpaid - known_cases - quitt - warn) + " / " + str(members + joinAgain))

    if (printed == False) :
        print("[OK] Analyse des status terminée.")

    return(txt)
# ==============================================================================