# ==============================================================================
# Python 3.9 (64 bits)
# -Vincent Kim-
# V 2.0
# ==============================================================================
from os import listdir #List or create files in directory
import re #Regex
from os.path import isfile, exists #List files in directory
from sources.print import ft_print_err, ft_print_err_no_quitt
# ==============================================================================
def ft_order_db(listDB, DataFolderName) :

    #VAR
    order = []
    minVal = listDB[0]

    while (len(listDB) > 0) :

        minVal = listDB[0]

        for i in range (len(listDB)) :

            if (listDB[i].replace('.txt', '').split('-')[-1] < minVal.replace('.txt', '').split('-')[-1]
                or (listDB[i].replace('.txt', '').split('-')[-1] == minVal.replace('.txt', '').split('-')[-1] 
                    and listDB[i].replace('.txt', '').split('-')[-2] < minVal.replace('.txt', '').split('-')[-2])
                or (listDB[i].replace('.txt', '').split('-')[-1] == minVal.replace('.txt', '').split('-')[-1]
                    and listDB[i].replace('.txt', '').split('-')[-2] == minVal.replace('.txt', '').split('-')[-2]
                    and listDB[i].replace('.txt', '').split('-')[-3] < minVal.replace('.txt', '').split('-')[-3])
                ) :
                minVal = listDB[i]
        order.append("./" + DataFolderName + "/" + minVal)
        listDB.remove(minVal)
        
    return(order)
# ==============================================================================
def ft_check_db_exist_or_unique_file(folder, db, name = "") :

    #VAR
    pathList = []

    if (db == True) :
        pathList = [f for f in listdir(folder)
            if (isfile(folder + "/"+ f))
                and re.search('(admin)+.*(.txt)$', f)
                and re.search('(CONFIDENTIEL)+.*(.txt)$', f)
                and re.search('(INTERDIT-DE-PARTAGER-VIA-DISCORD)+.*(.txt)$', f)
        ]
        if (len(pathList) == 0) :
            ft_print_err("Erreur : aucun fichier contenant dans son nom \"admin\", \"CONFIDENTIEL\" et \"INTERDIT-DE-PARTAGER-VIA-DISCORD\""\
                + " et terminant par \".txt\" dans le dossier \"" + folder + "\".")

    else :
        pathList = [f for f in listdir(folder)
            if (isfile(folder + "/"+ f))
                and re.search('(CONFIDENTIEL)+.*(.csv)$', f)
                and re.search('(INTERDIT-DE-PARTAGER-VIA-DISCORD)+.*(.csv)$', f)
                and re.search(re.escape(name) + '+.*(.csv)$', f)
        ]
        if (len(pathList) != 1) :
            ft_print_err("Erreur : plus ou moins d'un fichier contenant \"CONFIDENTIEL\" et \"INTERDIT-DE-PARTAGER-VIA-DISCORD\""\
                + " et \"" + name + "\" dans le dossier \"" + folder + "\".")

    return (pathList)
# ==============================================================================
def ft_analyse(dictNames):

    #CONST
    dataFolderName = dictNames["dataFolderName"]
    originelDataFolderName = dictNames["originelDataFolderName"]
    resultFolderName = dictNames["resultFolderName"]
    natName = dictNames["natName"]
    quittName = dictNames["quittName"]
    pathOriginelFolder = "./" + dataFolderName + "/" + originelDataFolderName

    #VAR
    listDB = []
    originelFolder = False

    if (not exists("./" + dataFolderName)):
        ft_print_err("Erreur, le dossier \"./" + dataFolderName + "\" contenant les premiers csv de données n'existe pas.")

    else :
        print("[INFO] Le dossier \"./" + dataFolderName + "\" contenant les données brutes existe.")

    if (exists(pathOriginelFolder)):
        originelFolder = True
        print("[INFO] Le dossier \"" + pathOriginelFolder + "\" contenant les premiers csv de données existe.")

    else :
        print("[INFO] Le dossier \"" + pathOriginelFolder + "\" contenant les premiers csv de données n'existe pas.")

    listDB = ft_check_db_exist_or_unique_file("./" + dataFolderName, True)

    if (originelFolder == True) :

        ft_check_db_exist_or_unique_file(pathOriginelFolder, False, natName)
        ft_check_db_exist_or_unique_file(pathOriginelFolder, False, quittName)

    listDB = ft_order_db(listDB, dataFolderName)

    print("[INFO] " + str(len(listDB)) + " base de données trouvées.")

    for i in range(len(listDB)) :
        print("[INFO] " + listDB[i].replace('.txt', '').split('-')[-3] + "/" + listDB[i].replace('.txt', '').split('-')[-2]\
            + "/" + listDB[i].replace('.txt', '').split('-')[-1])

    if (originelFolder == True) :
        return(pathOriginelFolder, listDB)
    return("", listDB)
# ==============================================================================