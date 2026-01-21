import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error, r2_score

# --- PRÉPARATION DES DONNÉES ---
chemin_actuel = os.path.dirname(os.path.abspath(__file__))
chemin_json = os.path.join(chemin_actuel, '..', 'data', 'dataset_final.json')

df = pd.read_json(chemin_json)
cols_a_convertir = ['taille', 'valeur', 'fin_contrat'] 
for col in cols_a_convertir:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df_train = df.dropna(subset=['valeur']).copy()

target = 'valeur'
variable_num = [
    'age', 'taille', 'fin_contrat', 'selections_inter', 'minutes_25_26',
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
cols_utiles = cols_num_reelles + cols_cat_reelles

X = df_train[cols_utiles]
y = df_train[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

# --- PRÉPROCESSEUR ---
preprocessor = ColumnTransformer(
    transformers=[
        ('num', Pipeline([('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())]), cols_num_reelles),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cols_cat_reelles)
    ])

# --- CONFIGURATION DES GRIDS ---
models_config = {
    "Random Forest": {
        "model": RandomForestRegressor(random_state=42),
        "grid": {
            'regressor__n_estimators': [300, 500, 800],
            'regressor__max_depth': [15, 25, None],
            'regressor__min_samples_split': [2, 5, 10],
            'regressor__min_samples_leaf': [1, 2],
            'regressor__max_features': ['sqrt', None]
        }
    },
    "Gradient Boosting": {
        "model": GradientBoostingRegressor(random_state=42),
        "grid": {
            'regressor__n_estimators': [500, 1000],
            'regressor__learning_rate': [0.01, 0.05, 0.1],
            'regressor__max_depth': [3, 5, 7],
            'regressor__subsample': [0.8, 1.0]
        }
    },
    "XGBoost": {
        "model": XGBRegressor(random_state=42),
        "grid": {
            'regressor__n_estimators': [500, 1000],
            'regressor__learning_rate': [0.01, 0.05, 0.1],
            'regressor__max_depth': [6, 8, 10],
            'regressor__colsample_bytree': [0.8, 1.0],
            'regressor__gamma': [0, 0.1]
        }
    }
}

best_overall_score = -np.inf
best_model = None
comparison_results = []

print(f"🚀 Démarrage de l'optimisation profonde (10-fold CV)... Prévoyez du temps.")

for name, config in models_config.items():
    print(f"\n🔎 Recherche intensive pour : {name}")
    pipe = Pipeline(steps=[('preprocessor', preprocessor), ('regressor', config["model"])])
    
    grid_search = GridSearchCV(pipe, config["grid"], cv=10, scoring='r2', n_jobs=-1, verbose=1)
    grid_search.fit(X_train, y_train)
    
    y_pred = grid_search.best_estimator_.predict(X_test)
    test_r2 = r2_score(y_test, y_pred)
    test_mae = mean_absolute_error(y_test, y_pred)
    
    comparison_results.append({
        "Modèle": name,
        "Meilleur R² (CV)": grid_search.best_score_,
        "R² (Test)": test_r2,
        "MAE (€)": test_mae,
        "Params": grid_search.best_params_
    })
    
    if test_r2 > best_overall_score:
        best_overall_score = test_r2
        best_model = grid_search.best_estimator_
        winner_name = name

# --- AFFICHAGE DU TABLEAU COMPARATIF ---
df_res = pd.DataFrame(comparison_results).sort_values(by="R² (Test)", ascending=False)
print("\n" + "="*60)
print("📊 RÉSULTATS DE L'OPTIMISATION")
print("="*60)
print(df_res[["Modèle", "Meilleur R² (CV)", "R² (Test)", "MAE (€)"]])
print(f"\n🏆 MEILLEUR MODÈLE RETENU : {winner_name}")

# --- SAUVEGARDE DU MODÈLE ---
joblib.dump(best_model, 'modele_2.pkl')
print(f"\n💾 Modèle sauvegardé sous 'modele_2.pkl'")

# ---  PRÉDICTIONS SUR LE DF COMPLET ---
df_complet = df.copy()

print("\nLancement des prédictions pour tous les joueurs...")

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

print("Application des statuts...")
df_complet['statut'] = df_complet.apply(definir_statut, axis=1)

df_complet.to_csv('dataset_avec_predictions_2.csv', index=False)
print("✅ Données complètes sauvegardées sous 'dataset_avec_predictions.csv'")
