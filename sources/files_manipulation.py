# ==============================================================================
# Python 3.9 (64 bits)
# -Vincent Kim-
# V 2.0
# ==============================================================================
from os import listdir, remove #List or create files in directory
import re #Regex
from datetime import datetime
from os.path import isfile #List files in directory
# ==============================================================================
def ft_save_csv(content, path, name, ext) :

    #VAR
    txt = ""
    finalName = ""

    if (ext == ".csv") :
        for i in range(len(content)) :
            for j in range(len(content[i])) :
                txt += content[i][j] + ";"
            txt += "\n"

    elif (ext == ".txt") :
        txt = content

    finalName = name + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")).replace(":", "-") + ext
    
    fd = open(path + "/" + finalName, encoding = 'utf-8',mode = 'w')
    fd.write(txt)
    fd.close()

    return(finalName)
# ==============================================================================
def ft_formating_db_to_array(array) :

    #VAR
    items = []

    items = array[0].split("\n")

    for i in range(len(items)) :
        items[i] = items[i].split(":")[0].strip()

    for i in range(len(array)) :
        array[i] = array[i].split("\n")
        for j in range(len(array[i])) :
            if (len(array[i][j].split(":")) > 1) :
                array[i][j] = array[i][j].split(":")[1].strip()

    array.insert(0, items)
# ==============================================================================
def ft_open(path, db) :

    #VAR
    array = []
    fileDescriptor = ""
    i = 0

    fileDescriptor = open(path, encoding = 'utf-8',mode = 'r')

    if (db == True) :
        array = fileDescriptor.read().replace(";", "").split('\n\n')
        fileDescriptor.close()

        while (i < len(array)) :
            if (array[i] == ""):
                del array[i]
                i -= 1
            i += 1
    else :
        array = fileDescriptor.read().split("\n")

        i = 0
        while (i < len(array)) :
            if (array[i].split(";")[0].strip().lower() != 'a quitté l\'asso'\
            and array[i].split(";")[0].strip().lower() != 'abandon de poste'\
            and array[i].split(";")[0].strip().lower() != 'adhésion non-payée'\
            and array[i].split(";")[0].strip().lower() != 'adhésion non-payée (actuel)'\
            and array[i].split(";")[0].strip().lower() != 'adhésion non-payée (réadhésion)'\
            and array[i].split(";")[0].strip().lower() != 'adhésion non-payée (primo)'\
            and array[i].split(";")[0].strip().lower() != 'adhésion non-payée (retour d\'expulsion)'\
            and array[i].split(";")[0].strip().lower() != 'attente de chèque'\
            and array[i].split(";")[0].strip().lower() != 'attente de chèque (actuel)'\
            and array[i].split(";")[0].strip().lower() != 'attente de chèque (réadhésion)'\
            and array[i].split(";")[0].strip().lower() != 'attente de chèque (primo)'\
            and array[i].split(";")[0].strip().lower() != 'attente de chèque (retour d\'expulsion)'\
            and array[i].split(";")[0].strip().lower() != 'départ volontaire'\
            and array[i].split(";")[0].strip().lower() != 'expulsion'\
            and array[i].split(";")[0].strip().lower() != 'raisons personelles'\
            and array[i].split(";")[0].strip().upper() != 'STATUS'\
            and array[i].split(";")[0].strip().upper() != '?'\
            and array[i].split(";")[0].strip().upper() != 'OK'\
            and array[i].split(";")[0].strip().upper() != 'S'\
            ) :
                array.pop(i);
                i -= 1
            else :
                array[i] = array[i].split(";")
            i += 1

    return(array)
# ==============================================================================
def ft_db_to_array(path) :

    #VAR
    arrayDB = []

    arrayDB = ft_open(path, True)
    ft_formating_db_to_array(arrayDB)

    return(arrayDB)
# ==============================================================================
def ft_save_and_delete_last(content, path, stamp, name, ext) :

    #VAR
    lastFileArr = []
    nameFile = ""

    nameFile = ft_save_csv(content, path,  stamp + name, ext)

    lastFileArr = [f for f in listdir(path)
            if (isfile(path + "/"+ f))
                and re.search(re.escape(name) + '+.*(' + ext + ')$', f)
            ]
    if (len(lastFileArr) > 2) :
        ft_print_err("ERREUR : PLUS D'UN FICHIER A SUPPRIMÉ")
        
    elif (len(lastFileArr) == 2) :
        for file in lastFileArr :
            if (file != nameFile) :
                remove(path + "/" + file)
# ==============================================================================