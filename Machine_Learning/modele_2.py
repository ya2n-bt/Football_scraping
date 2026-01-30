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
from sklearn.model_selection import cross_val_score

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
    'nb_blessures_3ans', 'matchs_manques_3ans', 'jours_blessures', 'nb_trophees_3ans', 'classement_club', 'valeur_club'
]
variable_cat = ['position', 'nationalite', 'pied_fort', 'club', 'ligue'] 

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

best_overall_cv_score = -np.inf 
meilleur_modele = ""
comparison_results = []

for name, config in models_config.items():
    print(f"Modèle : {name}")
    pipe = Pipeline(steps=[('preprocessor', preprocessor), ('regressor', config["model"])])
    
    grid_search = GridSearchCV(pipe, config["grid"], cv=10, scoring='r2', n_jobs=-1, verbose=1)
    grid_search.fit(X_train, y_train)
    
    cv_mae_scores = cross_val_score(grid_search.best_estimator_, X_train, y_train, 
                                    cv=10, scoring='neg_mean_absolute_error', n_jobs=-1)
    mean_mae_cv = -cv_mae_scores.mean() 
    
    cv_r2_score = grid_search.best_score_
    
    comparison_results.append({
        "Modèle": name,
        "R² moyen (CV)": cv_r2_score,
        "MAE moyenne (CV)": mean_mae_cv,
        "Estimator": grid_search.best_estimator_
    })
    
    if cv_r2_score > best_overall_cv_score:
        best_overall_cv_score = cv_r2_score
        meilleur_modele = name
        pipeline_meilleur_modele = grid_search.best_estimator_

# --- TABLEAU DE COMPARAISON ---
df_res = pd.DataFrame(comparison_results).sort_values(by="R² moyen (CV)", ascending=False)
print("Comparaison des modèles :")
df_res_display = df_res[["Modèle", "R² moyen (CV)", "MAE moyenne (CV)"]].copy()
df_res_display["MAE moyenne (CV)"] = df_res_display["MAE moyenne (CV)"].map("{:,.0f} €".format)
print(df_res_display)

# --- ÉVALUATION DU MEILLEUR MODÈlE ---
print("\n" + "="*70)
print(f"Évaluation du meilleur modèle sur données test : {meilleur_modele}")
print("="*70)

y_pred_final = pipeline_meilleur_modele.predict(X_test)
final_test_r2 = r2_score(y_test, y_pred_final)
final_test_mae = mean_absolute_error(y_test, y_pred_final)

print(f"   - R² Final : {final_test_r2:.4f}")
print(f"   - Erreur moyenne (MAE) : {final_test_mae:,.0f} €")

# --- SAUVEGARDE DU MODÈLE ---
joblib.dump(pipeline_meilleur_modele, 'modele_final_2.pkl')
print(f"Modèle sauvegardé sous 'modele_final_2.pkl'")

# ---  PRÉDICTIONS SUR LE DF COMPLET ---
df_complet = df.copy()

df_complet['valeur_estimee'] = pipeline_meilleur_modele.predict(df_complet[cols_utiles])
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

df_complet.to_csv('dataset_avec_predictions_final_2.csv', index=False)
print("Données complètes sauvegardées sous 'dataset_avec_predictions_final_2.csv'")
