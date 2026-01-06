import streamlit as st
import pandas as pd
import joblib
import numpy as np
import os
import plotly.graph_objects as go
from sklearn.metrics import r2_score, mean_absolute_error
import plotly.express as px

# --- CONFIGURATION DE LA PAGE ---

st.set_page_config(
    page_title="Football Moneyball ⚽",
    page_icon="⚽",
    layout="wide"
)

# --- CHARGEMENT DES DONNÉES ---

dossier_actuel = os.path.dirname(os.path.abspath(__file__))
chemin_csv = os.path.join(dossier_actuel, '..', 'data', 'dataset_avec_predictions.csv')
chemin_modele = os.path.join(dossier_actuel, '..', 'data', 'modele.pkl')

@st.cache_data
def load_data():
    if not os.path.exists(chemin_csv):
        st.error(f"Fichier introuvable ici : {chemin_csv}")
        return None
        
    df = pd.read_csv(chemin_csv)
    return df

df = load_data()

if df is None:
    st.stop()

# --- CRÉATION DE LA BARRE LATÉRALE ---

st.sidebar.title("⚽ Outil d'analyse footballistique")

pages = ["📊 Profil Joueur", "🔎 Estimation valeur réelle", "💎 Pépites", "🔮 Simulateur", "ℹ️ À Propos"]
choix_page = st.sidebar.radio("Menu", pages)

st.sidebar.markdown("---")
st.sidebar.info(f"Nombre de joueur dans la base de donnée : {len(df)}")
st.title(f"{choix_page}")

# --- PAGE 1 : PROFIL JOUEUR ---
if choix_page == "📊 Profil Joueur":
    st.header("Visualisation :")
    mode_recherche = st.radio(
        "Méthode de recherche :",
        ["📂 Recherche par Filtres", "🔍 Recherche par Nom"],
        horizontal=True,
        key="mode_p1" 
    )

    joueur_data = None 

    # --- OPTION A : PAR FILTRES ---
    if mode_recherche == "📂 Recherche par Filtres":
        col_ligue, col_club, col_joueur = st.columns(3)

        # LIGUE
        with col_ligue:
            toutes_ligues = df['ligue'].dropna().unique().tolist()
            top_5 = ["Premier League", "LaLiga", "Bundesliga", "Serie A", "Ligue 1"]

            ligues_vip = [L for L in top_5 if L in toutes_ligues]
            ligues_autres = sorted([L for L in toutes_ligues if L not in ligues_vip])
            
            liste_ligues_final = ligues_vip + ligues_autres
            
            ligue_sel = st.selectbox(
                "1️⃣ Ligue", 
                liste_ligues_final,  
                key="ligue_p1", 
                index=None,
                placeholder="Choix ligue..."
            )

        # CLUB 
        with col_club:
            if ligue_sel:
                df_ligue = df[df['ligue'] == ligue_sel]
                liste_clubs = sorted(df_ligue['club'].astype(str).unique())
            else:
                liste_clubs = []
            
            club_sel = st.selectbox(
                "2️⃣ Club", 
                liste_clubs, 
                key="club_p1", 
                index=None,
                placeholder="Choix club...",
                disabled=(ligue_sel is None) 
            )

        # JOUEUR 
        with col_joueur:
            if club_sel and ligue_sel: 
                df_club = df_ligue[df_ligue['club'] == club_sel]
                liste_joueurs = sorted(df_club['nom'].astype(str).unique())
            else:
                liste_joueurs = []

            joueur_sel = st.selectbox(
                "3️⃣ Joueur", 
                liste_joueurs, 
                key="joueur_p1", 
                index=None, 
                placeholder="Choix joueur...",
                disabled=(club_sel is None)
            )

        if joueur_sel:
            joueur_data = df_club[df_club['nom'] == joueur_sel].iloc[0]

    # --- OPTION B : PAR NOM ---
    else:
        if 'label_recherche' not in df.columns:
            df['label_recherche'] = df['nom'] + " (" + df['club'] + ")"
            
        liste_complete = sorted(df['label_recherche'].unique())
        
        choix_recherche = st.selectbox(
            "🔎 Saisir le nom du joueur", 
            liste_complete, 
            key="search_p1",
            index=None, 
            placeholder="Ex: Kylian Mbappé..."
        )
        
        if choix_recherche:
            joueur_data = df[df['label_recherche'] == choix_recherche].iloc[0]

    # --- GESTION DE L'ATTENTE ---
    if joueur_data is None:
        if mode_recherche == "📂 Recherche par Filtres":
            st.info("👆 Commencez par sélectionner une **Ligue** pour activer les filtres.")
        else:
            st.info("👆 Tapez le nom d'un joueur dans la barre de recherche.")
        st.stop()

    st.markdown("---")

    # --- AFFICHAGE DU PROFIL JOUEUR ---

    st.subheader(f"Profil de {joueur_data['nom']}")
    
    info1, info2, info3, info4 = st.columns(4)

    with info1:
        st.info(f"**Club**\n\n{joueur_data['club']}")
    
    with info2:
        st.info(f"**Nationalité**\n\n{joueur_data['nationalite']}")
        
    with info3:
        st.info(f"**Âge**\n\n{int(joueur_data['age'])} ans")
        
    with info4:
        valeur = joueur_data['valeur']
        if pd.notna(valeur):
            valeur_txt = f"{valeur:,.0f}".replace(',', ' ') + " €"
        else:
            valeur_txt = "Non coté"
            
        st.info(f"**Valeur marchande**\n\n{valeur_txt}")

    # --- TROIS COLONNES D'INFOS ---

    st.markdown("---")

    col_gauche_fixe, col_droite_dyn, spider_graph = st.columns([1.8, 1.5, 2.1])
    
    with col_gauche_fixe:
        st.subheader("📊 Infos Générales")
        
        config_affichage = {
            'taille': '📏 Taille',
            'pied_fort': '🦶 Pied fort',
            'position': '🎯 Poste',
            'selections_inter': '🌍 Sélections Internationales',
            'nb_trophees_3ans': '🏆 Trophées (3 dernières années)',
            'fin_contrat': '📅 Jours avant fin de contrat',
            'nb_blessures_3ans': '🚑 Blessures (3 dernières années)',
            'jours_blessures': '🕘 Durée blessures en jours (3 dernières années)',
            'matchs_manques_3ans': "❌ Matchs manqués (3 dernières années)"
        } 
        donnees_tableau = {}
        
        for col_technique, nom_joli in config_affichage.items():
            if col_technique in df.columns:
                valeur = joueur_data[col_technique]
                
                if pd.notna(valeur) and isinstance(valeur, (int, float)):
                    
                    if col_technique == 'taille':
                        valeur = f"{valeur:.2f} m"
                    else:
                        valeur = f"{valeur:,.0f}".replace(',', ' ')
                
                elif pd.isna(valeur):
                    valeur = "-"
                    
                donnees_tableau[nom_joli] = valeur

        df_affichage = pd.DataFrame(donnees_tableau.items(), columns=['Statistique', 'Valeur'])
        
        st.dataframe(
            df_affichage, 
            hide_index=True, 
            use_container_width=True
        )

    with col_droite_dyn:
        st.subheader("📈 Performances par Saison")
        
        saison_choisie = st.radio(
            "Choisir la saison :",
            ["2023-2024", "2024-2025", "2025-2026"],
            horizontal=True
        )
        
        if saison_choisie == "2023-2024":
            suffixe = "_23_24"
        elif saison_choisie == "2024-2025":
            suffixe = "_24_25"
        else: 
            suffixe = "_25_26"

        position_joueur = joueur_data['position']
        
        if "Gardien" in str(position_joueur):
            config_saison = {
                f'minutes{suffixe}': '⏱️ Minutes jouées',
                f'matchs{suffixe}': '🏟️ Matchs joués', 
                f'titularisations{suffixe}': '👕 Titularisations', 
                f'entrees{suffixe}': '🔄 Entrées en jeu',         
                f'buts_encaisses{suffixe}': '🥅 Buts encaissés',
                f'clean_sheets{suffixe}': '🧤 Clean Sheets'
            }
        
        else:
            config_saison = {
                f'minutes{suffixe}': '⏱️ Minutes jouées',
                f'matchs{suffixe}': '🏟️ Matchs joués',
                f'titularisations{suffixe}': '👕 Titularisations',
                f'entrees{suffixe}': '🔄 Entrées en jeu',
                f'buts{suffixe}': '⚽ Buts',
                f'penaltys{suffixe}': '🥅 Penaltys marqués',
                f'passes_d{suffixe}': '🎯 Passes décisives',
            }
        
        data_saison = {}
        
        for col_tech, nom_joli in config_saison.items():
            if col_tech in df.columns:
                val = joueur_data[col_tech]
                
                if pd.notna(val) and isinstance(val, (int, float)):
                    val = f"{val:,.0f}".replace(',', ' ')
                elif pd.isna(val):
                    val = "-"
                data_saison[nom_joli] = val
            else:
                data_saison[nom_joli] = "Non dispo"

        df_saison = pd.DataFrame(data_saison.items(), columns=['Statistique', 'Valeur'])
        st.dataframe(df_saison, hide_index=True, use_container_width=True)
    
    with spider_graph:
        st.subheader(
            "🕸️ Positionnement",
            help = "L'échelle (0-100) compare le joueur au **meilleur profil** de la base de données. \n Les données de référence se basent sur la saison complète 2024-2025."
        )

        if "Gardien" in str(joueur_data['position']):
            categories = ['Minutes', 'Clean Sheets', 'Titularisations', 'Matchs Joués', 'Âge (Jeunesse)']
            cols_ref   = ['minutes_24_25', 'clean_sheets_24_25', 'titularisations_24_25', 'matchs_24_25', 'age']
        else:
            categories = ['Efficacité (Buts)', 'Altruisme (Passes D)', 'Temps de jeu', 'Expérience (Matchs)', 'Titularisations']
            cols_ref   = ['buts_24_25', 'passes_d_24_25', 'minutes_24_25', 'matchs_24_25', 'titularisations_24_25']

        # --- CALCUL DES SCORES NORMALISÉS ---

        values = []
        
        for col in cols_ref:
            valeur_joueur = joueur_data[col]
            max_base = df[col].max()
            
            if col == 'age':
                score = (valeur_joueur / max_base) * 100
            else:
                if max_base > 0:
                    score = (valeur_joueur / max_base) * 100
                else:
                    score = 0
            
            values.append(score)

        values += values[:1]
        categories += categories[:1]

        # --- CRÉATION DU GRAPHIQUE ---
        fig_radar = go.Figure()

        fig_radar.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=joueur_data['nom'],
            line_color='#1D428A',
            fillcolor='rgba(29, 66, 138, 0.4)' 
        ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    showticklabels=False
            )),
            showlegend=False,
            margin=dict(l=40, r=40, t=40, b=40),
            height = 390
        )

        st.plotly_chart(fig_radar, use_container_width=True)


# --- PAGE 2 : ESTIMATION VALEUR RÉELLE ---

elif choix_page == "🔎 Estimation valeur réelle":
    st.header("Valeur : Réel vs Estimée")

# --- EXPLICATION DU MODELE ---

    st.info("""
        **🧠 Comment fonctionne ce prédicteur ?**
        
        Cet outil d'aide au recrutement repose sur un modèle de **Machine Learning (Random Forest)**. 
        L'objectif est d'éliminer les biais subjectifs (réputation, "hype") pour isoler la **Juste Valeur (Fair Value)** d'un joueur basée sur la data.
        
        Le modèle pondère une quarantaine de variables réparties en trois axes :
        * 📈 **Performance & Impact :** Buts, passes décisives, minutes jouées ...
        * 🏥 **Fiabilité & Palmarès :** Historique des blessures, nombre de trophées récents, régularité...
        * 📝 **Contexte Contractuel :** Durée restante de contrat, âge, ligue, poste...
        
        **Usage pour les recruteurs :** Détecter les **opportunités d'achat** (joueurs sous-cotés) et optimiser les **ventes** (joueurs sur-cotés par la hype), afin d'appuyer chaque négociation sur une valeur objective.
        """)

    st.markdown("---")

# --- Choix du joueur ---

    st.subheader("👤 Sélectionner un joueur")

    mode_recherche = st.radio(
        "Méthode de recherche :",
        ["📂 Recherche par Filtres", "🔍 Recherche par Nom"],
        horizontal=True
    )

    joueur = None 

    # --- PAR FILTRES ---
    if mode_recherche == "📂 Recherche par Filtres":
        col_ligue, col_club, col_joueur = st.columns(3)

        # LIGUE
        with col_ligue:
            toutes_ligues = df['ligue'].dropna().unique().tolist()
            top_5 = ["Premier League", "LaLiga", "Bundesliga", "Serie A", "Ligue 1"]

            ligues_vip = [L for L in top_5 if L in toutes_ligues]
            ligues_autres = sorted([L for L in toutes_ligues if L not in ligues_vip])
            

            liste_ligues_final = ligues_vip + ligues_autres
            
            ligue_sel = st.selectbox(
                "1️⃣ Ligue", 
                liste_ligues_final,  
                key="ligue_p2", 
                index=None,
                placeholder="Choix ligue..."
            )

        # CLUB 
    
        with col_club:
            if ligue_sel:
                df_ligue = df[df['ligue'] == ligue_sel]
                liste_clubs = sorted(df_ligue['club'].astype(str).unique())
            else:
                liste_clubs = []
            
            club_sel = st.selectbox(
                "2️⃣ Club", 
                liste_clubs, 
                key="club_p2", 
                index=None,
                placeholder="Choix club...",
                disabled=(ligue_sel is None) 
            )

        # JOUEUR 
        with col_joueur:
            if club_sel and ligue_sel: 
                df_club = df_ligue[df_ligue['club'] == club_sel]
                liste_joueurs = sorted(df_club['nom'].astype(str).unique())
            else:
                liste_joueurs = []

            joueur_sel = st.selectbox(
                "3️⃣ Joueur", 
                liste_joueurs, 
                key="joueur_p2", 
                index=None, 
                placeholder="Choix joueur...",
                disabled=(club_sel is None)
            )

        if joueur_sel:
            joueur = df_club[df_club['nom'] == joueur_sel].iloc[0]

    # --- PAR NOM ---
    else:
        df['label_recherche'] = df['nom'] + " (" + df['club'] + ")"
        liste_complete = sorted(df['label_recherche'].unique())
        
        choix_recherche = st.selectbox(
            "🔎 Saisir le nom du joueur", 
            liste_complete, 
            index=None, 
            placeholder="Ex: Kylian Mbappé..."
        )
        
        if choix_recherche:
            joueur = df[df['label_recherche'] == choix_recherche].iloc[0]

    if joueur is None:
        if mode_recherche == "📂 Recherche par Filtres":
            st.info("👆 Commencez par sélectionner une **Ligue** pour activer les filtres.")
        else:
            st.info("👆 Tapez le nom d'un joueur dans la barre de recherche.")
            
        st.stop() 

    st.markdown("---")

    # --- VERDICT FINANCIER ---

    st.subheader(f"💰 Verdict Financier : {joueur['nom']}")

     # --- TROIS BOÎTES D'INFOS ---

    col_reel, col_ia, col_verdict = st.columns(3)

    with col_reel:
        valeur_reelle = joueur['valeur']
        
        if pd.isna(valeur_reelle):
            txt_reel = "Inconnue"
            valeur_reelle_num = 0
        else:
            txt_reel = f"{valeur_reelle:,.0f} €".replace(',', ' ')
            valeur_reelle_num = valeur_reelle
        
        st.markdown(f"""
        <div style="
            text-align: center; 
            border: 2px solid #ffffff; 
            background-color: transparent; 
            padding: 15px; 
            border-radius: 10px;
            height: 100%;">
            <p style="margin:0; opacity: 0.7; font-size: 0.9em; font-weight: bold;">VALEUR MARCHÉ</p>
            <h2 style="margin:5px 0;">{txt_reel}</h2>
            <p style="margin:0; opacity: 0.5; font-size: 0.8em;">Prix officiel transfermarkt</p>
        </div>
        """, unsafe_allow_html=True)

    with col_ia:
        valeur_ia = joueur['valeur_estimee']
        
        if pd.isna(valeur_ia):
            txt_ia = "Erreur"
            delta_html = ""
        else:
            txt_ia = f"{valeur_ia:,.0f} €".replace(',', ' ')
            
            if valeur_reelle_num > 0:
                delta = valeur_ia - valeur_reelle_num
                signe = "+" if delta > 0 else ""
                couleur_delta = "#4ade80" if delta > 0 else "#f87171" 
                delta_txt = f"{signe}{delta:,.0f} €".replace(',', ' ')
                delta_html = f"<span style='color: {couleur_delta}; font-weight: bold;'>{delta_txt}</span>"
            else:
                delta_html = "<span style='color: #60a5fa; font-weight: bold;'>✨ Nouvelle Estimation</span>"

        st.markdown(f"""
        <div style="
            text-align: center; 
            border: 2px solid #ffffff; 
            background-color: transparent; 
            padding: 15px; 
            border-radius: 10px;
            height: 100%;">
            <p style="margin:0; opacity: 0.7; font-size: 0.9em; font-weight: bold;">VALEUR MODÈLE</p>
            <h2 style="margin:5px 0;">{txt_ia}</h2>
            <p style="margin:0; font-size: 0.9em;">{delta_html}</p>
        </div>
        """, unsafe_allow_html=True)

    with col_verdict:
        statut = joueur['statut']
        
        if statut == "Sous-coté":
            couleur_bordure = "#4ade80"
            emoji = "✅"
            msg = "BONNE AFFAIRE"
            desc = "Potentiel de plus-value"
        elif statut == "Sur-coté":
            couleur_bordure = "#f87171" 
            emoji = "⚠️"
            msg = "TROP CHER"
            desc = "Attention au prix"
        else: 
            couleur_bordure = "#60a5fa" 
            emoji = "💎"
            msg = "PÉPITE"
            desc = "Joueur à révéler"

        st.markdown(f"""
        <div style="
            text-align: center; 
            border: 2px solid {couleur_bordure}; 
            background-color: transparent; 
            padding: 15px; 
            border-radius: 10px;
            height: 100%;">
            <p style="margin:0; color: {couleur_bordure}; font-size: 0.9em; font-weight: bold;">VERDICT</p>
            <h2 style="margin:5px 0; color: {couleur_bordure};">{emoji} {statut}</h2>
            <p style="margin:0; opacity: 0.7; font-size: 0.8em;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

     # --- PERFORMANCE DU MODÈLE ---

    st.subheader("📊 Performance du prédicteur & Philosophie du Modèle")

    df_perf = df.dropna(subset=['valeur', 'valeur_estimee'])
    
    if len(df_perf) > 0:

        r2 = r2_score(df_perf['valeur'], df_perf['valeur_estimee'])
        
        mae = mean_absolute_error(df_perf['valeur'], df_perf['valeur_estimee'])

        kpi1, kpi2, kpi3 = st.columns(3)

        with kpi1:
            st.metric(
                label="Précision (R²)", 
                value=f"{r2:.2%}", 
                help="Proche de 100% = Le modèle colle parfaitement aux prix du marché."
            )
        
        with kpi2:
            st.metric(
                label="Écart Moyen (MAE)", 
                value=f"{mae:,.0f} €".replace(',', ' '),
                help="En moyenne, le modèle surestime ou sous-estime les joueurs de ce montant."
            )

        with kpi3:
            st.metric(
                label="Joueurs Analysés", 
                value=f"{len(df_perf)}",
                help="Nombre de joueurs utilisés pour ces calculs."
            )


        st.info(f"""
        **🧠 Analyse du score ({r2:.1%}) :**
        
        Nous ne cherchons pas à atteindre un score de **100%**. Une corrélation parfaite signifierait que le modèle reproduit les biais émotionnels du marché (Hype, Marketing, Panic buy...).
        
        Ce modèle se concentre **uniquement sur la performance sportive objective**. 
        L'écart restant n'est donc pas une erreur technique, mais représente la **subjectivité du marché** (la différence entre le talent pur et le prix affiché).
        """)

        st.markdown("---")

         # --- GRAPHIQUE SUR/SOUS CÔTÉ ---

        st.write("### 🎯 Analyse Visuelle : Marché vs Prédicteur")
        st.caption("Si un point est sur la ligne rouge, le modèle a trouvé exactement le bon prix. S'il est au-dessus, le modèle pense qu'il vaut plus cher (Sous-coté).")
        
        fig_perf = px.scatter(
            df_perf,
            x='valeur',
            y='valeur_estimee',
            color='ligue',     
            hover_name='nom', 
            hover_data=['club', 'age'],
            opacity=0.6,
            labels={'valeur': 'Valeur Transfermarkt (€)', 'valeur_estimee': 'Valeur estimée (€)'},
            title=f"Nuage de points"
        )
        
        fig_perf.add_shape(
            type="line",
            x0=0, y0=0,
            x1=df_perf['valeur'].max(), y1=df_perf['valeur'].max(),
            line=dict(color="Red", width=2, dash="dash")
        )
        
        st.plotly_chart(fig_perf, use_container_width=True)

    else:
        st.warning("⚠️ Erreur : Pas assez de données pour évaluer les performances du modèle.")

    st.markdown("---")

     # --- TOP 10 VARIABLES IMPORTANTES ---

    st.subheader("Features importantes du modèle")

    best_model = joblib.load(chemin_modele)

    try:
        cols_num_reelles = [
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

        cols_cat_reelles = ['position', 'nationalite', 'pied_fort']
        
        rf_model_opti = best_model.named_steps['regressor']
        preprocessor_opti = best_model.named_steps['preprocessor']

        variables_names_cat = preprocessor_opti.named_transformers_['cat'].get_feature_names_out(cols_cat_reelles)
        
        toutes_les_cols = np.concatenate([cols_num_reelles, variables_names_cat])

        importances = rf_model_opti.feature_importances_
        
        if len(toutes_les_cols) == len(importances):
            df_importances = pd.DataFrame({'Variable': toutes_les_cols, 'Importance': importances})
            
            df_top10 = df_importances.sort_values(by='Importance', ascending=True).tail(10)


            df_top10['Variable_Clean'] = df_top10['Variable']

            fig_imp = px.bar(
                df_top10, 
                x='Importance', 
                y='Variable_Clean', 
                orientation='h',
                title="Top 10 des facteurs déterminants du prix",
                text_auto='.1%' 
            )
            
            fig_imp.update_traces(marker_color='#1D428A', textposition='outside')
            fig_imp.update_layout(xaxis_title="Impact sur la valeur (%)", yaxis_title="")
            
            st.plotly_chart(fig_imp, use_container_width=True)
            
        else:
            st.error(f"Erreur de dimension : {len(toutes_les_cols)} noms vs {len(importances)} scores.")

    except Exception as e:
        st.error(f"Erreur lors de l'extraction des features : {e}")

    st.info("""
            💡 **Analyse du modèle :**
            
            On constate que le modèle ne se focalise pas uniquement sur les statistiques individuelles (buts, passes). 
            Il priorise deux axes majeurs pour fixer le prix :
            1. **Le Palmarès (19%)** : Avoir gagné des trophées récemment augmente drastiquement la valeur.
            2. **La Fiabilité & Régularité (~22%)** : Le cumul des matchs joués sur les deux dernières saisons est déterminant. Un joueur disponible vaut plus cher qu'un joueur souvent blessé ou remplaçant.
            """)
    
# --- PAGE 3 : PÉPITES ---
elif choix_page == "💎 Pépites":
        st.header("Détection des joueurs les plus sous-côtés")

        # --- AJOUT DU POTENTIEL DANS LE DF ---

        df_potentiel = df.copy()
        
        df_potentiel = df_potentiel.dropna(subset=['valeur', 'valeur_estimee'])
        
        df_potentiel['plus_value'] = df_potentiel['valeur_estimee'] - df_potentiel['valeur']
        
        df_potentiel['renta'] = (df_potentiel['plus_value'] / df_potentiel['valeur']) * 100

        # --- FILTRES ---

        st.markdown("### 🔍 Critères de recherche")
        
        col_filtre_1, col_filtre_2, col_filtre_3 = st.columns(3)
        
        with col_filtre_1:
            mode_ligue = st.radio("Périmètre :", ["5 Grands Championnats", "Par Ligue"], horizontal=True)
            
            ligue_selected = None
            if mode_ligue == "Par Ligue":
                toutes_les_ligues = df_potentiel['ligue'].unique()
                top_5_target = ['Premier League', 'LaLiga', 'Bundesliga', 'Serie A', 'Ligue 1']
                top_5_present = [ligue for ligue in top_5_target if ligue in toutes_les_ligues]
                autres_ligues = sorted([ligue for ligue in toutes_les_ligues if ligue not in top_5_target])
                ligues_dispo = top_5_present + autres_ligues
                
                ligue_selected = st.selectbox("Choisir le championnat :", ligues_dispo)

        with col_filtre_2:
            age_min, age_max = st.slider("Tranche d'âge :", 15, 40, (16, 25))

        with col_filtre_3:
            budget_max = st.number_input("Budget Max (€)", value=200000000, step=10000000)

        # --- APPLICATION DES FILTRES ---
        df_filtre = df_potentiel[df_potentiel['plus_value'] > 0]
        
        if mode_ligue == "Par Ligue" and ligue_selected:
            df_filtre = df_filtre[df_filtre['ligue'] == ligue_selected]
            
        df_filtre = df_filtre[
            (df_filtre['age'] >= age_min) & 
            (df_filtre['age'] <= age_max) &
            (df_filtre['valeur'] <= budget_max)
        ]

        # 4. --- AFFICHAGE TOP 20 ---

        top_20 = df_filtre.sort_values(by='plus_value', ascending=False).head(20)
        
        tableau_final = top_20[[
            'nom', 'age', 'club', 'ligue', 'position', 
            'valeur', 'valeur_estimee', 'plus_value', 'renta'
        ]]

        st.markdown(f"### 🎯 Top 20 des joueurs sous-côtés ")
        
        max_val = top_20['plus_value'].max() if len(top_20) > 0 else 100 # Sécurité pour la barre de progression (éviter crash si liste vide)

        st.dataframe(
            tableau_final,
            use_container_width=True,
            hide_index=True,
            column_config={
                "nom": "Joueur",
                "age": "Age",
                "club": "Club actuel",
                "valeur": st.column_config.NumberColumn(
                    "Prix Marché",
                    format="%.0f €"
                ),
                "valeur_estimee": st.column_config.NumberColumn(
                    "Valeur Modèle",
                    format="%.0f €",
                    help="Prix que le joueur 'devrait' coûter selon ses stats"
                ),
                "plus_value": st.column_config.ProgressColumn(
                    "Gain Potentiel (€)",
                    format="%.0f €",
                    min_value=0,
                    max_value=max_val,
                    help="Différence brute entre le prix réel et l'estimation du modèle"
                ),
                "renta": st.column_config.NumberColumn(
                    "Rentabilité",
                    format="%.1f %%",
                    help="Retour sur investissement théorique"
                )
            }
        )
        
        st.info("💡 **Remarque :** Les joueurs avec une forte plus-value sont souvent des éléments performants évoluant dans des ligues et/ou clubs moins médiatisées. Ce sont des bonnes cibles pour les recruteurs.")

# --- PAGE 4 : SIMULATEUR ---
elif choix_page == "🔮 Simulateur":
    st.header("Simulateur de Valeur")
    st.info("Ici on pourra modifier les stats d'un joueur pour voir sa valeur changer.")

# --- PAGE 5 : À PROPOS ---
elif choix_page == "ℹ️ À Propos":
    st.header("À Propos du Projet")
    st.info("Présentation du projet et de la méthodologie.")