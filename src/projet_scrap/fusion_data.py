import glob
import json

liste_fichiers = glob.glob("data_*.json")

print(f"Fichiers trouvés : {liste_fichiers}")

tous_les_joueurs = []

for fichier in liste_fichiers:
    with open(fichier, "r", encoding="utf-8") as f:
        data = json.load(f)
        tous_les_joueurs.extend(data)

with open("dataset_final.json", "w", encoding="utf-8") as f:
    json.dump(tous_les_joueurs, f, indent=4, ensure_ascii=False)
