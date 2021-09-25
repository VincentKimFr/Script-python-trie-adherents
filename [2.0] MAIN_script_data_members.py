# ==============================================================================
# Python 3.9 (64 bits)
# -Vincent Kim-
# V 2.0
# ==============================================================================
"""
Cherche un ou plusieurs fichier qui contiennent "admin", "CONFIDENTIEL",
"INTERDIT-DE-PARTAGER-VIA-DISCORD", et termine par .txt, dans un dossier spécifique
 Supprime les anciennes adhésions et trie par région avec histtorique entre chaque mise à jour,
 format des infos :
\"[Précédent]

User Id : 42
Pseudo : pseudo
Email : a@b.c
Date de création : 22/04/1870 à 20h05
Adhérant Id : 32
Adhérant ? : Oui [/ Non]
Compte Activé ? : Oui [/ Non, obligatoirement non si en attente de paiement]
Clé d'activation : 12345
Blocmail : 1
Nombre d'adhésion(s) : 56 [+1 si attente de paiement]
Avatar : https://liendelimage.com
Prénom : Prénom
Nom : Nom
Téléphone : 0611223344
Ville : Bordeaux
Code postal : 33000
Compteur adhésion : 3 [/ Jamais adhéré / Doit être relancé => 0]

[suivant]\"
"""
# ==============================================================================
import sys
import shutil #Copier coller fichiers
from os import makedirs
from os.path import exists

from sources.analyse import ft_analyse, ft_check_db_exist_or_unique_file
from sources.dates import ft_only_members_and_dates_and_count
from sources.files_manipulation import ft_db_to_array, ft_open
from sources.data_processing import ft_correct_city_code, ft_cleaning_order_items, ft_dpt, ft_order_status,\
    ft_check_double, ft_correct_inscr_nb, ft_del_duplicates
from sources.logs import ft_logs
from sources.save_all import ft_save_all
from sources.print import ft_print_err, ft_print_err_no_quitt
from sources.reg_list_dates import ft_choose_dpt
from sources.config import ft_print_success, ft_correct_city, ft_only_code,
    ft_only_Adh_Id, ft_quitt_status, ft_duplicates, ft_failInscription, ft_delSince
# ==============================================================================
def ft_multpl_check_double(arrayDB, dictNames, order) :

    #CONST
    firstName = dictNames["itemFirstName_Name"]
    name = dictNames["itemName_Name"]
    email = dictNames["itemEmail_Name"]
    phone = dictNames["itemPhone_Name"]

    print("\n--RECHERCHE DE duplicates DES DONNÉES--")

    ft_check_double(arrayDB, dictNames, order, firstName, name)
    ft_check_double(arrayDB, dictNames, order, email)
    ft_check_double(arrayDB, dictNames, order, phone)
# ==============================================================================
def ft_last_path(lastFolderPath, natName, quittName) :

    #VAR
    lastNat = []
    lastQuitt = []
    lastNatPathList = []
    lastQuittPathList = []

    if (lastFolderPath != "") :
        print("[INFO] Dernier dossier : " + lastFolderPath)
        lastNatPathList = ft_check_db_exist_or_unique_file(lastFolderPath, False, natName)
        lastNat = ft_open(lastFolderPath + "/" + lastNatPathList[0], False)

        if (len(lastNat) == 0) :
            ft_print_err("ERREUR : FICHIER LAST NAT VIDE")

        lastQuittPathList = ft_check_db_exist_or_unique_file(lastFolderPath, False, quittName)
        lastQuitt = ft_open(lastFolderPath + "/" + lastQuittPathList[0], False)

        if (len(lastQuitt) == 0) :
            ft_print_err("ERREUR : FICHIER LAST QUITT VIDE")
    else :
        print("[INFO] Pas de précédent dossier")

    return(lastNat, lastQuitt)
# ==============================================================================
def ft_manage_generalUpdate(GENERAL_UPDATE) :

    #VAR
    inpt = ""

    if (GENERAL_UPDATE == True) :

        while (inpt.lower() != "o" and inpt.lower() != "n" and inpt.lower() != "q") :
            inpt = input("\n----/!\\ L'OPTION (GENERAL_UPDATE == True) DE REMPLACEMENT AUTOMATIQUE DE TOUT LES ANCIENS DOSSIERS DE RÉSULTATS EST ACTIVÉE DANS LE CODE SOURCE,\
                \nÊTES VOUS SUR DE VOULOIR ÉCRASER TOUT LES ANCIENS DOSSIER DE RÉSULTATS EXISTANTS ? (O : Oui / N : Non / Q : Quitter)\n")

            if (inpt.lower() != "o" and inpt.lower() != "n" and inpt.lower() != "q") :
                print("Entrée inconnue, veuillez recommencer.\n")

        if (inpt.lower() == "q") :
            print("----Arrêt du programme sur demande de l'utilisateur----")
            sys.exit(1)

        elif (inpt.lower() == "n") :
            print("----Réponse négative : Arrêt du programme sur demande de l'utilisateur----")
            sys.exit(1)

        elif (inpt.lower() == "o") :
            ft_print_err_no_quitt("LES DOSSIERS DE RÉSULTATS SERONT REMPLACÉS SANS CONFIRMATION SUPPLÉMENTAIRE")
# ==============================================================================
def ft_manage_forceUpdate(resultPath, DBPath, FORCE_UPDATE, GENERAL_UPDATE, date) :

    #VAR
    inpt = ""

    if (not exists(resultPath)):
        print("\n[INFO] Création du dossier \"" + resultPath + "\".")
        makedirs(resultPath, exist_ok=True)
        shutil.copy(DBPath, resultPath)

    elif (FORCE_UPDATE == False) :
            print("\n[INFO] Le dossier de résultats \"" + resultPath + "\" existe déjà. "\
                + "Exécution de la base de donnée suivante.\n")
            return("return")

    elif (FORCE_UPDATE == True and GENERAL_UPDATE == False) :

        while (inpt.lower() != "o" and inpt.lower() != "n" and inpt.lower() != "q") :
            inpt = input("\n----/!\\ L'OPTION (FORCE_UPDATE == True) DE REMPLACEMENT AUTOMATIQUE DES ANCIENS DOSSIERS DE RÉSULTATS EST ACTIVÉE DANS LE CODE SOURCE,\
                \nÊTES VOUS SUR DE VOULOIR ÉCRASER L'ANCIEN DOSSIER DE RÉSULTATS DU " + date + " ? (O : Oui / N : Non / Q : Quitter)\n")

            if (inpt.lower() != "o" and inpt.lower() != "n" and inpt.lower() != "q") :
                print("Entrée inconnue, veuillez recommencer.\n")

        if (inpt.lower() == "q") :
            print("----Arrêt du programme sur demande de l'utilisateur----")
            sys.exit(1)

        elif (inpt.lower() == "n") :
            print("\n[INFO] Exécution de la base de donnée suivante.\n")
            return("return")

        elif (inpt.lower() == "o") :
            ft_print_err_no_quitt("[INFO] LE DOSSIER " + date + " SERA REMPLACÉ\n")
            shutil.copy(DBPath, resultPath)

# ==============================================================================
def ft_run_db(lastFolderPath, DBPath, dictNames, order, GENERAL_UPDATE) :

    #CONST
    #FORCE_UPDATE = True
    FORCE_UPDATE = False

    correct_city = ft_correct_city() #[["City", "Correct zip code"],["City2", "Correct zip code2"]…]
    only_code = ft_only_code() #[["Zip Code", "Correct/standard zip code", "Correct city"],[…]…]
    only_Adh_Id = ft_only_Adh_Id() #[["AdhId", "New zip code", ], […]]
    quitt_status = ft_quitt_status() #[["AdhId", "special reason to quitt (fired, banned, resign…)",
                                        #["date begin", "date end or empty string"], [Others begin-end dates if exists]], […]]
    duplicates = ft_duplicates() #[ADH ID to del]
    failInscription = ft_failInscription() #[["Date min", "ADH ID", "adh count (-1)", "date end"],[…]]
    delSince = ft_delSince() #[["date since adh is deleted", "AdhId"], […]]

    to_del = ["User Id",
        "Date de création",
        "Adhérant ?",
        "Compte Activé ?",
        "Clé d'activation",
        "Blocmail",
        "Avatar",
        "Compteur adhésion"]

    date = DBPath.replace('.txt', '').split('-')[-3] + "/" + DBPath.replace('.txt', '').split('-')[-2]\
        + "/" + DBPath.replace('.txt', '').split('-')[-1]

    dpt = ft_choose_dpt(date)

    nameFolder = date.split("/")[2] + "-" + date.split("/")[1] + "-" + date.split("/")[0]
    resultPath = "./" + dictNames["resultFolderName"] + "/" + nameFolder

    natName = dictNames["natName"]
    quittName = dictNames["quittName"]
    

    #VAR
    lastNat = []
    lastQuitt = []

    arrayDB = []
    countTxt = ""
    logs = [
        [],
        [],
        [],
        [],
        ["Modifications depuis la dernière mise à jour :"],
        [],
        ["!A-", "N'est plus adhérent"],
        ["A+", "Nouvel adhérent"],
        ["A+aa", "Retour d'un ancien adhérent"],
        ["R+", "Réaffectation entrante"],
        ["R-", "Réaffectation sortante"],
        ["!S+", "Est passé en sursis"],
        ["S-", "À renouvelé sa cotisation et est sortit de sursis datant d'au moins une mise à jour"],
        ["C", "Est passé en sursis et à renouvelé sa cotisation entre les deux mises à jour"],
        ["!P+C", "Est passé en statut de cotisation impayée lors du renouvellement ou sortit de sursis"],
        ["!P+A+aa", "Est passé en statut de cotisation impayée lors de la réhadésion"],
        ["P-", "Est sortit du statut de cotisation impayée lors du renouvellement ou sortit de sursis"],
        ["D", "Autre changement de données"],
        [],
        [dictNames["itemLogChange_Name"], dictNames["adhIDName"], dictNames["itemPseudo_Name"], dictNames["itemFirstName_Name"],
            dictNames["itemName_Name"], dictNames["itemLogData_Name"], dictNames["itemLogOldData_Name"],
            dictNames["itemLogNewData_Name"]
            ]
    ]
    lenLogs = len(logs)

    if (ft_manage_forceUpdate(resultPath, DBPath, FORCE_UPDATE, GENERAL_UPDATE,date) == "return") :
        return(resultPath)

    print("\n[DÉBUT]------------------------" + date + "------------------------\n")

    lastNat, lastQuitt = ft_last_path(lastFolderPath, natName, quittName)

    arrayDB = ft_db_to_array(DBPath)
    ft_del_duplicates(arrayDB, duplicates, dictNames)
    ft_correct_inscr_nb(arrayDB, failInscription, date, dictNames)
    countTxt = ft_only_members_and_dates_and_count(arrayDB,dictNames, lastNat, lastQuitt, date, quitt_status)
    ft_cleaning_order_items(arrayDB, to_del, dictNames, order)
    ft_multpl_check_double(arrayDB, dictNames, order)
    ft_correct_city_code(arrayDB, correct_city, only_code, only_Adh_Id, order, dictNames, date)
    ft_dpt(arrayDB, dpt, order, dictNames)
    arrayDB = ft_order_status(arrayDB, dpt, order, dictNames)
    logs = ft_logs(lastQuitt, lastNat, arrayDB, date, duplicates, delSince, logs, order, dictNames)
    ft_save_all(arrayDB, logs, countTxt, date, dictNames, order, lenLogs, FORCE_UPDATE)
    return(resultPath)
# ==============================================================================
def ft_run_main (GENERAL_UPDATE, dictNames, order):

    #CONST
    resultFolderName = "./" + dictNames["resultFolderName"]

    #VAR
    lastFolderPath = ""
    listDB = []

    ft_manage_generalUpdate(GENERAL_UPDATE)
    
    print("--ANALYSE PRÉLIMINAIRE DES DOSSIERS--")

    lastFolderPath, listDB = ft_analyse(dictNames)

    if (not exists(resultFolderName)):
        print("[INFO] Création du dossier \"" + resultFolderName + "\".")
        makedirs(resultFolderName, exist_ok=True)
    else :
        print("[INFO] Le dossier \"" + resultFolderName + "\" existe déjà.")

    for i in range(len(listDB)) :
        lastFolderPath = ft_run_db(lastFolderPath, listDB[i], dictNames, order, GENERAL_UPDATE)

# ==============================================================================
def main ():
    #CONST
    GENERAL_UPDATE = False
    AG = False
    REGULAR = True

    dictNames = {
        "dataFolderName" : "datas/AG",
        "resultFolderName" : "results/AG",
        "originelDataFolderName" : "originel",

        "natName" : "_national-script_",
        "quittName" : "_national-quitt_",

        "dateName" : "Date dernière adhésion",
        "oldDatesName" : "Dates anciennes adhésions",
        "memberDateCountName" : "Compteur adhésion",
        "adhIDName" : "Adhérant Id",
        "adhCountName" : "Nombre d'adhésion(s)",

        "itemFirstName_Name" : "Prénom",
        "itemName_Name" : "Nom",
        "itemEmail_Name" : "Email",
        "itemPhone_Name" : "Téléphone",
        "itemStatus_Name" : "Status",
        "itemPseudo_Name" : "Pseudo",
        "itemCity_Name" : "Ville",
        "itemZipCode_Name" : "Code postal",
        "itemRegion_Name" : "Région",
        "itemDpt_Name" : "Département",

        "itemLogChange_Name" : "Changement",
        "itemLogData_Name" : "Donnée",
        "itemLogOldData_Name" : "De",
        "itemLogNewData_Name" : "Vers",

        "stamp" : "CONFIDENTIEL-INTERDIT-DE-PARTAGER-VIA-DISCORD"
    }

    order = [
        dictNames["itemStatus_Name"], dictNames["dateName"], dictNames["adhIDName"], dictNames["itemPseudo_Name"],
        dictNames["itemFirstName_Name"], dictNames["itemName_Name"], dictNames["itemEmail_Name"], dictNames["itemPhone_Name"],
        dictNames["itemCity_Name"], dictNames["itemZipCode_Name"], dictNames["itemRegion_Name"], dictNames["itemDpt_Name"],
        dictNames["adhCountName"], dictNames["oldDatesName"]
    ]

    print("\n---DÉBUT DU SCRIPT---\n")

    if (AG == True) :
        print("\n---ANALYSE AG---\n")
        ft_run_main(GENERAL_UPDATE, dictNames, order)

    if (REGULAR == True) :
        dictNames["dataFolderName"] = "datas/regular"
        dictNames["resultFolderName"] = "results/regular"
        print("\n---ANALYSE RÉGULIÈRE---\n")
        ft_run_main(GENERAL_UPDATE, dictNames, order)

    ft_print_success()
    sys.exit(0)
#-------------------------------------------------------------------------------
if __name__ == "__main__" :
    main()
