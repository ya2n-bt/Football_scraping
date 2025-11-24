import glob
import json

liste_fichiers = glob.glob("data_*.json")

print(f"Fichiers trouvés : {liste_fichiers}")

tous_les_joueurs = []

# 2. On charge chaque fichier un par un
for fichier in liste_fichiers:
    print(f"Chargement de {fichier}...")
    with open(fichier, "r", encoding="utf-8") as f:
        data = json.load(f)
        tous_les_joueurs.extend(data)