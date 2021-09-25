# Scrip de trie d’utilisateurs

Ce script prends en entrée au moins une base de donées d’utilisateurs au format texte. En option un dossier antérieur aux bases de données qui contient un premier résultat.

Il tranforme le texte en tableau por trier, ordonner, corriger ou déduire des données (date d’adhésion selon un compteur), effectuer des vérifications (comptes en double, code postal invalide…), trier les adhésions expirées, avant de faire un historique selon les fichiers précédants. Pour enfin enregistrer un csv national puis par secrétaire départemental ou régional, ainsi que des statistiques générales, dans un dossier par base de données.

Par défaut, si un dosser de résultat pour une date donnée existe déjà il est ignorée, mais en modifiant une variable il est possible de lui faire demander confirmation de l’écrasement des données, et avec une autre variable en plus, de tout remplacer sans deander. Et pour une dernière, de prendre d’autres noms de dossiers de données et résultats.
