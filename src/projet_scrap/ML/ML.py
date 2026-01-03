import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

pd.options.display.float_format = '{:,.0f}'.format

# --- PRÉPARATION DES DONNÉES ---

chemin_actuel = os.path.dirname(os.path.abspath(__file__))
chemin_json = os.path.join(chemin_actuel, '..', '..', '..', 'data', 'dataset_final.json')

df = pd.read_json(chemin_json)

cols_a_convertir = ['taille', 'valeur', 'fin_contrat'] 

for col in cols_a_convertir:
        df[col] = pd.to_numeric(df[col], errors='coerce')

df_train = df.dropna(subset=['valeur']).copy()

# --- SÉLECTION DES VARIABLES ---

target = 'valeur'

variable_num = [
    'age', 'taille', 
    'fin_contrat', 'selections_inter', 'minutes_25_26',
    'matchs_25_26', 'entrees_25_26', 'titularisations_25_26', 'buts_25_26',
    'penaltys_25_26', 'passes_d_25_26', 'clean_sheets_25_26','buts_encaisses_25_26', 
    'minutes_24_25', 'matchs_24_25', 'entrees_24_25', 'titularisations_24_25', 
    'buts_24_25', 'penaltys_24_25', 'passes_d_24_25', 'clean_sheets_24_25', 
    'buts_encaisses_24_25', 'minutes_23_24', 'matchs_23_24', 'entrees_23_24', 
    'titularisations_23_24', 'buts_23_24', 'penaltys_23_24',
    'passes_d_23_24', 'clean_sheets_23_24', 'buts_encaisses_23_24', 
    'nb_blessures_3ans', 'matchs_manques_3ans', 'jours_blessures', 'nb_trophees_3ans'
]

variable_cat = ['position', 'nationalite', 'pied_fort'] 

cols_num_reelles = [c for c in variable_num if c in df_train.columns]
cols_cat_reelles = [c for c in variable_cat if c in df_train.columns]

X = df_train[cols_num_reelles + cols_cat_reelles]
y = df_train[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

# --- PRÉPARATION DU PIPELINE ---
preprocessor = ColumnTransformer(
    transformers=[
        ('num', SimpleImputer(strategy='median'), cols_num_reelles),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cols_cat_reelles)
    ])

pipeline_base = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(random_state=42)) 
])

# --- OPTIMISATION ---

param_grid = {
    'regressor__n_estimators': [100, 200, 300, 500], 
    'regressor__max_depth': [10, 15, 20, 25, 30, None], 
    'regressor__min_samples_split': [2, 5, 10], 
    'regressor__min_samples_leaf': [1, 2, 4]    
}

print("Démarrage de l'optimisation des hyperparamètres...")

grid_search = GridSearchCV(pipeline_base,
                            param_grid, cv=10,
                            scoring='r2',
                            n_jobs=-1,
                            verbose=1)

grid_search.fit(X_train, y_train)

# --- RÉSULTATS ---
best_model = grid_search.best_estimator_ 

print("Optimisation terminée :")
print(f"Meilleurs paramètres : {grid_search.best_params_}")
print(f"Score de la validation croisée (R²) : {grid_search.best_score_:.3f}")

final_score = best_model.score(X_test, y_test)
print(f"Score Final sur les données test (R²) : {final_score:.2f}")


# --- ANALYSE VARIABLES IMPORTANTES ---

rf_model_opti = best_model.named_steps['regressor']
preprocessor_opti = best_model.named_steps['preprocessor']

variables_names_cat = preprocessor_opti.named_transformers_['cat'].get_feature_names_out(cols_cat_reelles)
toutes_les_cols = np.concatenate([cols_num_reelles, variables_names_cat])

importances = rf_model_opti.feature_importances_
df_importances = pd.DataFrame({'Variable': toutes_les_cols, 'Importance': importances})
df_importances = df_importances.sort_values(by='Importance', ascending=False)

print("TOP 10 des facteurs déterminants :")
print(df_importances.head(10))

# --- 8. FONCTION DE PRÉDICTION ---

def predire_joueur(nom_joueur):
    joueur = df[df['nom'].str.contains(nom_joueur, case=False, na=False)]
    if len(joueur) == 0:
        print(f"Joueur '{nom_joueur}' introuvable.")
        return
    
    joueur_data = joueur.iloc[[0]]
    valeur_reelle = joueur_data['valeur'].values[0]
    
    estimation = best_model.predict(joueur_data[cols_num_reelles + cols_cat_reelles])[0]
    
    print(f"{joueur_data['nom'].values[0]} ({joueur_data['club'].values[0]})")
    print(f"Valeur réelle : {valeur_reelle:,.0f} €" if not pd.isna(valeur_reelle) else "   Valeur réelle : Inconnu")
    print(f"Valeur estimée : {estimation:,.0f} €")

# --- PÉPITES ---

print("TOP 10 des joueurs sous-cotés) :")
predictions_test = best_model.predict(X_test)
df_resultats = X_test.copy()
df_resultats['nom'] = df.loc[X_test.index, 'nom']
df_resultats['club'] = df.loc[X_test.index, 'club']
df_resultats['valeur_reelle'] = y_test
df_resultats['valeur_estimee'] = predictions_test
df_resultats['diff_argent'] = df_resultats['valeur_estimee'] - df_resultats['valeur_reelle']

df_pépites = df_resultats[df_resultats['valeur_reelle'] > 1000000]
print(df_pépites.sort_values(by='diff_argent', ascending=False).head(10)[['nom', 'club', 'valeur_reelle', 'valeur_estimee', 'diff_argent']])

while True:
    nom = input("\n⚽ Nom du joueur (ou 'q') : ")
    if nom.lower() == 'q': break
    predire_joueur(nom)

# --- SAUVEGARDE DU MODÈlE ET DES DONNÉES ---

print("Sauvegarde du modèle et des données...")

joblib.dump(best_model, 'modele.pkl')
print("Modèle sauvegardé sous 'modele.pkl'")

df_complet = df.copy()
cols_utiles = cols_num_reelles + cols_cat_reelles

print("Lancement des prédictions pour tous les joueurs...")

df_complet['valeur_estimee'] = best_model.predict(df_complet[cols_utiles])
df_complet['valeur_estimee'] = df_complet['valeur_estimee'].round(0)

df_complet['diff_valeur'] = df_complet['valeur_estimee'] - df_complet['valeur']
df_complet['diff_valeur'] = df_complet['diff_valeur'].round(0)

def definir_statut(row):
    if pd.isna(row['valeur']):
        return "À découvrir"  

    if pd.isna(row['valeur_estimee']):
        return "Erreur Données"

    if row['diff_valeur'] > 0:
        return "Sous-coté"
    else:
        return "Sur-coté"

df_complet['statut'] = df_complet.apply(definir_statut, axis=1)

df_complet.to_csv('dataset_avec_predictions.csv', index=False)
print("Données complètes sauvegardées sous 'dataset_avec_predictions.csv'")

nb_decouvertes = len(df_complet[df_complet['statut'] == 'À découvrir'])
print(f"Le modèle à estimé la valeur de {nb_decouvertes} joueurs sans valeur connue.")