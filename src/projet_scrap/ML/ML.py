import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split

chemin_actuel = os.path.dirname(os.path.abspath(__file__))
chemin_json = os.path.join(chemin_actuel, '..', 'dataset_final.json')

df = pd.read_json(chemin_json)
print(f"✅ Dataset chargé : {df.shape[0]} joueurs, {df.shape[1]} colonnes")


