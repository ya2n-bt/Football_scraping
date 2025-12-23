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

print(f"💾 Sauvegarde de {len(tous_les_joueurs)} joueurs dans le fichier final...")

with open("dataset_final.json", "w", encoding="utf-8") as f:
    json.dump(tous_les_joueurs, f, indent=4, ensure_ascii=False)

print("✅ Terminé ! Tu as ton fichier complet.")