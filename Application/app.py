import streamlit as st
import pandas as pd
import joblib
import numpy as np
import os
import plotly.graph_objects as go
import plotly.express as px

# --- CONFIGURATION DE LA PAGE ---

st.set_page_config(
    page_title="Mercato Analytics ⚽",
    page_icon="⚽",
    layout="wide"
)

# --- CHARGEMENT DES DONNÉES ---

dossier_actuel = os.path.dirname(os.path.abspath(__file__))
chemin_csv = os.path.join(dossier_actuel, '..', 'data', 'dataset_avec_predictions_final.csv')
chemin_csv_2 = os.path.join(dossier_actuel, '..', 'data', 'dataset_avec_predictions_final_2.csv')
chemin_modele = os.path.join(dossier_actuel, '..', 'data', 'modele_final.pkl')
chemin_modele_2 = os.path.join(dossier_actuel, '..', 'data', 'modele_final_2.pkl')

@st.cache_data
def load_data():
    if not os.path.exists(chemin_csv):
        st.error(f"Fichier introuvable ici : {chemin_csv}")
        return None
        
    df = pd.read_csv(chemin_csv)
    return df

@st.cache_data
def load_data_2():
    if not os.path.exists(chemin_csv):
        st.error(f"Fichier introuvable ici : {chemin_csv_2}")
        return None
        
    df2 = pd.read_csv(chemin_csv_2)
    return df2

df = load_data()
df2 = load_data_2()

if df is None:
    st.stop()

if df2 is None:
    st.stop()

@st.cache_resource
def load_modele():
    if os.path.exists(chemin_modele):
        return joblib.load(chemin_modele)
    else:
        return None

best_model = load_modele()

@st.cache_resource
def load_modele_2():
    if os.path.exists(chemin_modele):
        return joblib.load(chemin_modele_2)
    else:
        return None

best_model_2 = load_modele_2()

# --- CRÉATION DE LA BARRE LATÉRALE ---

with st.sidebar:
    st.markdown("""
        <style>
        .nav-title {
            color: white !important;
            font-size: 38px !important;
            font-weight: 800 !important;
            text-align: center !important;
            margin-bottom: 25px !important;
        }

        [data-testid="stSidebar"] [role="radiogroup"] {
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            gap: 12px !important;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label {
            background-color: #3867d6 !important;
            border-radius: 30px !important;
            padding: 12px 0px !important;
            width: 85% !important;
            box-sizing: border-box !important;
            border: 2px solid transparent !important;

            display: flex !important;
            align-items: center !important;
            justify-content: center !important;

            cursor: pointer !important;
            transition: all 0.3s ease !important;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label > div:first-child {
            display: none !important;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label div[data-testid="stMarkdownContainer"] {
            width: 100% !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label p {
            color: white !important;
            font-size: 17px !important;
            font-weight: 700 !important;
            margin: 0 !important;
            padding: 0 !important;
            width: 100% !important;
            text-align: center !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            line-height: 1 !important;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label:hover {
            background-color: #4b7bec !important;
            transform: scale(1.05) !important;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
            background-color: #1e3799 !important;
            border: 2px solid white !important;
        }
        </style>

        <p class="nav-title">Navigation</p>
    """, unsafe_allow_html=True)

    options_nav = ["🏠 Accueil", "👤 Profil Joueur", "💰 Estimation Valeur Réelle", "💎 Pépites", "🔮 Simulateur", "ℹ️ À propos"]
    choix_page = st.radio("Navigation", options_nav, key="navigation", label_visibility="collapsed")

st.sidebar.info(f"Nombre de joueurs dans la base : {len(df)}")
st.title(f"{choix_page}")

# --- PAGE 0 : ACCUEIL ---
if choix_page == "🏠 Accueil":
        
        def changer_page(nom_page):
            st.session_state.navigation = nom_page

        st.markdown("""
            <style>
            .main-title {
                color: #3867d6; 
                font-size: 3rem;
                font-weight: 800;
                margin-bottom: 0px;
            }
            .subtitle {
                color: #808495;
                font-size: 1.2rem;
                margin-bottom: 30px;
            }
            .feature-header {
                color: #4b7bec;
                font-weight: bold;
                font-size: 1.4rem;
                border-left: 5px solid #3867d6;
                padding-left: 15px;
                margin-bottom: 15px;
            }
            div[data-testid="stContainer"] {
                border-color: #3867d6 !important; 
            }
            </style>
            """, unsafe_allow_html=True)

        st.markdown('<p class="main-title">Bienvenue sur Mercato Analytics !</p>', unsafe_allow_html=True)
        
        st.write("""
            Rationalisez vos décisions grâce à la puissance du Machine Learning. 
            Notre application transforme les statistiques brutes en **indicateurs de valeur concrets** pour optimiser votre stratégie de recrutement.
            """)

        st.markdown("---")

        col_home_1, col_home_2 = st.columns(2)

        with col_home_1:
            with st.container(border=True):
                st.markdown('<p class="feature-header">Data Visualization 📊</p>', unsafe_allow_html=True)
                st.write("Explorez les performances et statistiques des joueurs des 5 grands championnats.")
                st.button("Explorer les Profils ➔", on_click=changer_page, args=["👤 Profil Joueur"], key="btn_p1", use_container_width=True)

        with col_home_2:
            with st.container(border=True):
                st.markdown('<p class="feature-header">Estimation de la valeur sportive 💰</p>', unsafe_allow_html=True)
                st.write("Déterminez la juste valeur sportive d'un joueur, débarrassée des biais et de la hype médiatique.")
                st.button("Estimer une Valeur ➔", on_click=changer_page, args=["💰 Estimation & Juste Prix"], key="btn_p2", use_container_width=True)

        st.write("") 

        with col_home_1:
            with st.container(border=True):
                st.markdown('<p class="feature-header">Chasse aux Pépites 💎</p>', unsafe_allow_html=True)
                st.write("Identifiez les anomalies de marché. Trouvez les joueurs dont la valeur de notre modèle dépasse le prix réel.")
                st.button("Détecter des Pépites ➔", on_click=changer_page, args=["💎 Pépites"], key="btn_p3", use_container_width=True)

        with col_home_2:
            with st.container(border=True):
                st.markdown('<p class="feature-header">Simulateur 🔮</p>', unsafe_allow_html=True)
                st.write("Anticipez l'avenir. Modifiez les stats et voyez l'impact direct sur la valorisation marchande.")
                st.button("Lancer la Simulation ➔", on_click=changer_page, args=["🔮 Simulateur"], key="btn_p4", use_container_width=True)

# --- PAGE 1 : PROFIL JOUEUR ---
if choix_page == "👤 Profil Joueur":
    st.header("Visualisation")
    mode_recherche = st.radio(
        "Méthode de recherche :",
        ["Recherche par Filtres", "Recherche par Nom"],
        horizontal=True,
        key="mode_p1" 
    )

    joueur_data = None 

    # --- PAR FILTRES ---
    if mode_recherche == "Recherche par Filtres":
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

    # --- PAR NOM ---
    else:
        if 'label_recherche' not in df.columns:
            df['label_recherche'] = df['nom'] + " (" + df['club'] + ")"
            
        liste_complete = sorted(df['label_recherche'].unique())
        
        choix_recherche = st.selectbox(
            "Saisir le nom du joueur", 
            liste_complete, 
            key="search_p1",
            index=None, 
            placeholder="Ex: Kylian Mbappé..."
        )
        
        if choix_recherche:
            joueur_data = df[df['label_recherche'] == choix_recherche].iloc[0]

    if joueur_data is None:
        if mode_recherche == "Recherche par Filtres":
            st.info("👆 Commencez par sélectionner une **Ligue**.")
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

    col_gauche_fixe, col_droite_dyn = st.columns(2)
    
    with col_gauche_fixe:
        st.subheader("Infos Générales")
        
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
        st.dataframe(df_affichage, hide_index=True, use_container_width=True)

    with col_droite_dyn:
        st.subheader("Performances par Saison")
        
        saison_choisie = st.radio(
            "Choisir la saison :",
            ["2023-2024", "2024-2025", "2025-2026"],
            horizontal=True,
            key="saison_selector" 
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

        st.caption("Les données disponibles vont jusqu’à la trêve hivernale 2025.")

    # --- LE SPIDER GRAPH ---  
    st.write("---")
    _, col_spider, _ = st.columns([0.2, 1, 0.2])
    
    with col_spider:
        st.subheader("Spider-graph")
        
        if "Gardien" in str(joueur_data['position']):
            categories = ['Minutes', 'Clean Sheets', 'Titularisations', 'Matchs Joués', 'Âge']
            cols_ref   = ['minutes_24_25', 'clean_sheets_24_25', 'titularisations_24_25', 'matchs_24_25', 'age']
        else:
            categories = ['Buts', 'Passes D', 'Temps de jeu', 'Matchs', 'Titularisations']
            cols_ref   = ['buts_24_25', 'passes_d_24_25', 'minutes_24_25', 'matchs_24_25', 'titularisations_24_25']

        import plotly.graph_objects as go

        values = []
        for col in cols_ref:
            valeur_joueur = joueur_data[col]
            max_base = df[col].max()
            
            if max_base > 0:
                score = (valeur_joueur / max_base) * 100
            else:
                score = 0
            values.append(score)

        plot_values = values + [values[0]]
        plot_categories = categories + [categories[0]]

        fig_radar = go.Figure()

        fig_radar.add_trace(go.Scatterpolar(
            r=plot_values,
            theta=plot_categories,
            fill='toself',
            name=joueur_data.get('nom', 'Joueur'), 
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
            height=450
        )


        st.plotly_chart(fig_radar, use_container_width=True)
        st.caption("Comparaison au meilleur profil de la base (Saison 2024-2025).")

# --- PAGE 2 : ESTIMATION VALEUR RÉELLE ---
elif choix_page == "💰 Estimation Valeur Réelle":
    st.header("Valeur : Réel vs Estimée")

    # --- EXPLICATION DU MODELE ---

    st.info("""
        **Comment fonctionne ce prédicteur ?**
        
        Cet outil d'aide au recrutement repose sur un modèle de **Machine Learning (Gradient Boosting)**. 
        L'objectif est d'éliminer les biais subjectifs (maillot, réputation, "hype") pour isoler la **valeur uniquement sportive** d'un joueur basée sur la data.
        
        Le modèle pondère une quarantaine de variables réparties en trois axes :
        * **Performance & Impact :** Buts, passes décisives, minutes jouées ...
        * **Fiabilité & Palmarès :** Historique des blessures, nombre de trophées récents, régularité...
        * **Contexte Contractuel :** Durée restante de contrat, âge, ligue, poste...
        
        Pour distinguer le talent brut de la valeur marchande, nous avons confronté un modèle "pure performance" à un modèle "contexte global". L'objectif est d'isoler l'impact du club et de la ligue afin d'identifier les joueurs dont le prix est artificiellement gonflé par leur environnement sportif (l'objectif pour le recruteur est de cibler les bonnes affaires ou les profils surpayés).
        """)

    st.markdown("---")

    # --- Choix du joueur ---

    st.subheader("👤 Sélectionner un joueur")

    mode_recherche = st.radio(
        "Méthode de recherche :",
        ["Recherche par Filtres", "Recherche par Nom"],
        horizontal=True
    )

    joueur = None
    joueur2 = None

    # --- PAR FILTRES ---
    if mode_recherche == "Recherche par Filtres":
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
            joueur2 = df2[(df2['nom'] == joueur['nom']) & (df2['club'] == joueur['club'])].iloc[0]

    # --- PAR NOM ---
    else:
        df['label_recherche'] = df['nom'] + " (" + df['club'] + ")"
        liste_complete = sorted(df['label_recherche'].unique())
        
        choix_recherche = st.selectbox(
            "Saisir le nom du joueur", 
            liste_complete, 
            index=None, 
            placeholder="Ex: Kylian Mbappé..."
        )
        
        if choix_recherche:
            joueur = df[df['label_recherche'] == choix_recherche].iloc[0]
            joueur2 = df2[(df2['nom'] == joueur['nom']) & (df2['club'] == joueur['club'])].iloc[0]

    if joueur is None or joueur2 is None:
        if mode_recherche == "Recherche par Filtres":
            st.info("👆 Commencez par sélectionner une **Ligue**.")
        else:
            st.info("👆 Tapez le nom d'un joueur dans la barre de recherche.")
            
        st.stop() 

    st.markdown("---")

    # --- VERDICT FINANCIER ---

    # --- VERDICT FINANCIER / MODELE 1 ---

    st.subheader(f"💰 Verdict Financier : {joueur['nom']}")

    st.subheader("Modèle 1 : Performance Pure")
    st.write("")

     # --- TROIS BOÎTES D'INFOS ---

    col_reel, col_modele, col_verdict = st.columns(3)

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

    with col_modele:
        valeur_modele = joueur['valeur_estimee']
        
        if pd.isna(valeur_modele):
            txt_modele = "Erreur"
            delta_html = ""
        else:
            txt_modele = f"{valeur_modele:,.0f} €".replace(',', ' ')
            
            if valeur_reelle_num > 0:
                delta = valeur_modele - valeur_reelle_num
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
            <h2 style="margin:5px 0;">{txt_modele}</h2>
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

    st.write("")
    st.write("")
    st.subheader("Modèle 2 : Club et ligue pris en compte")
    st.write("")

    # --- VERDICT FINANCIER / MODELE 2 ---

     # --- TROIS BOÎTES D'INFOS ---

    col_reel2, col_modele2, col_verdict2 = st.columns(3)

    with col_reel2:
        valeur_reelle2 = joueur2['valeur']
        
        if pd.isna(valeur_reelle2):
            txt_reel2 = "Inconnue"
            valeur_reelle_num2 = 0
        else:
            txt_reel2 = f"{valeur_reelle2:,.0f} €".replace(',', ' ')
            valeur_reelle_num2 = valeur_reelle2
        
        st.markdown(f"""
        <div style="text-align: center; border: 2px solid #ffffff; padding: 15px; border-radius: 10px; height: 100%;">
            <p style="margin:0; opacity: 0.7; font-size: 0.9em; font-weight: bold;">VALEUR MARCHÉ</p>
            <h2 style="margin:5px 0;">{txt_reel2}</h2>
            <p style="margin:0; opacity: 0.5; font-size: 0.8em;">Prix officiel Transfermarkt</p>
        </div>
        """, unsafe_allow_html=True)

    with col_modele2:
        valeur_modele2 = joueur2['valeur_estimee']
        
        if pd.isna(valeur_modele2):
            txt_modele2 = "Erreur"
            delta_html2 = ""
        else:
            txt_modele2 = f"{valeur_modele2:,.0f} €".replace(',', ' ')
            
            if valeur_reelle_num2 > 0:
                delta2 = valeur_modele2 - valeur_reelle_num2
                signe2 = "+" if delta2 > 0 else ""
                couleur_delta2 = "#4ade80" if delta2 > 0 else "#f87171" 
                delta_txt2 = f"{signe2}{delta2:,.0f} €".replace(',', ' ')
                delta_html2 = f"<span style='color: {couleur_delta2}; font-weight: bold;'>{delta_txt2}</span>"
            else:
                delta_html2 = "<span style='color: #60a5fa; font-weight: bold;'>✨ Nouvelle Estimation</span>"

        st.markdown(f"""
        <div style="text-align: center; border: 2px solid #ffffff; padding: 15px; border-radius: 10px; height: 100%;">
            <p style="margin:0; opacity: 0.7; font-size: 0.9em; font-weight: bold;">VALEUR MODÈLE</p>
            <h2 style="margin:5px 0;">{txt_modele2}</h2>
            <p style="margin:0; font-size: 0.9em;">{delta_html2}</p>
        </div>
        """, unsafe_allow_html=True)

    with col_verdict2:
        statut2 = joueur2['statut']
        
        if statut2 == "Sous-coté":
            couleur_bordure2 = "#4ade80"
            emoji2 = "✅"
            desc2 = "Potentiel de plus-value"
        elif statut2 == "Sur-coté":
            couleur_bordure2 = "#f87171" 
            emoji2 = "⚠️"
            desc2 = "Attention au prix"
        else: 
            couleur_bordure2 = "#60a5fa" 
            emoji2 = "💎"
            desc2 = "Joueur à révéler"

        st.markdown(f"""
        <div style="text-align: center; border: 2px solid {couleur_bordure2}; padding: 15px; border-radius: 10px; height: 100%;">
            <p style="margin:0; color: {couleur_bordure2}; font-size: 0.9em; font-weight: bold;">VERDICT</p>
            <h2 style="margin:5px 0; color: {couleur_bordure2};">{emoji2} {statut2}</h2>
            <p style="margin:0; opacity: 0.7; font-size: 0.8em;">{desc2}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

     # --- PERFORMANCE DU MODÈLE ---

    st.subheader("📊 Performance des prédicteurs :")

    kpi1, kpi2, kpi3 = st.columns(3)
    
    with kpi1:
        st.metric(
            label="R² (Précision)", 
            value=f"71,12%", 
        )
        
    with kpi2:
        st.metric(
            label="Écart Moyen (MAE)", 
            value="5 529 367 €",
            help="En moyenne, le modèle surestime ou sous-estime les joueurs de ce montant."
        )
    
    with kpi3:
        st.metric(
            label="Nombre de variables explicatives", 
            value="38"
        )

    st.write("")
    st.write("")
    st.subheader("Comparaison en prenant en compte le club et la ligue")

    kpi11, kpi22, kpi33 = st.columns(3)
    
    with kpi11:
        st.metric(
            label="R² (Précision)", 
            value=f"84,72%", 
        )
        
    with kpi22:
        st.metric(
            label="Écart Moyen (MAE)", 
            value="4 021 781 €",
            help="En moyenne, le modèle surestime ou sous-estime les joueurs de ce montant."
        )
    
    with kpi33:
        st.metric(
            label="Nombre de variables explicatives", 
            value="42",
            help="Ajout des variables 'club', 'ligue', 'classement_club' et 'valeur_club'."
        )

    st.write("")

    st.info(f"""
    **Comparaison des modèles :**
    
    En rajoutant les variables de **club** et de **ligue**, le modèle explique une plus grande partie de la variance des prix (84,72% vs 71,12%).
    
    Bien que l'influence du club et de la ligue soit indéniable sur la valeur marchande, notre objectif est de neutraliser ces variables contextuelles afin d'isoler et d'évaluer uniquement la performance sportive du joueur. Nous portons donc notre regard sur le premier modèle
    """)

    st.markdown("---")

    # --- GRAPHIQUE SUR/SOUS CÔTÉ ---

    st.write("### Analyse Visuelle : Marché vs Prédicteur (Modèle 1)")
    st.caption("Si un point est sur la ligne rouge, le modèle a trouvé exactement le bon prix. S'il est au-dessus, le modèle pense qu'il vaut plus cher (Sous-coté).")
    
    top_5_ligues = ['Ligue 1', 'Premier League', 'Bundesliga', 'Serie A', 'LaLiga']
    df_ligue = df[df['ligue'].isin(top_5_ligues)].copy()
    
    fig_perf = px.scatter(
        df_ligue,
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
        x1=df['valeur'].max(), y1=df['valeur'].max(),
        line=dict(color="Red", width=2, dash="dash")
    )
    
    st.plotly_chart(fig_perf, use_container_width=True)

    st.markdown("---")

    # --- TOP 10 VARIABLES IMPORTANTES / MODÈLE 1 ---

    st.subheader("Features importantes des modèles")

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
                title="Top 10 des facteurs déterminants du prix - Modèle 1 (Performance Pure)",
                text_auto='.1%' 
            )
            
            fig_imp.update_traces(marker_color='#1D428A', textposition='outside')
            fig_imp.update_layout(xaxis_title="Impact sur la valeur (%)", yaxis_title="")
            
            st.plotly_chart(fig_imp, use_container_width=True)
            
        else:
            st.error(f"Erreur de dimension : {len(toutes_les_cols)} noms vs {len(importances)} scores.")

    except Exception as e:
        st.error(f"Erreur lors de l'extraction des features : {e}")

    # --- TOP 10 VARIABLES IMPORTANTES / MODÈLE 2 ---

    try:
        cols_num_2 = [
            'age', 'taille', 'fin_contrat', 'selections_inter', 'minutes_25_26',
            'matchs_25_26', 'entrees_25_26', 'titularisations_25_26', 'buts_25_26',
            'penaltys_25_26', 'passes_d_25_26', 'clean_sheets_25_26','buts_encaisses_25_26', 
            'minutes_24_25', 'matchs_24_25', 'entrees_24_25', 'titularisations_24_25', 
            'buts_24_25', 'penaltys_24_25', 'passes_d_24_25', 'clean_sheets_24_25', 
            'buts_encaisses_24_25', 'minutes_23_24', 'matchs_23_24', 'entrees_23_24', 
            'titularisations_23_24', 'buts_23_24', 'penaltys_23_24',
            'passes_d_23_24', 'clean_sheets_23_24', 'buts_encaisses_23_24', 
            'nb_blessures_3ans', 'matchs_manques_3ans', 'jours_blessures', 'nb_trophees_3ans',
            'classement_club', 'valeur_club' 
        ]

        cols_cat_2 = ['position', 'nationalite', 'pied_fort', 'club', 'ligue'] 
        
        modele_2_reg = best_model_2.named_steps['regressor']
        prepro_2 = best_model_2.named_steps['preprocessor']

        noms_cat_2 = prepro_2.named_transformers_['cat'].get_feature_names_out(cols_cat_2)
        toutes_les_cols_2 = np.concatenate([cols_num_2, noms_cat_2])

        importances_2 = modele_2_reg.feature_importances_
        
        if len(toutes_les_cols_2) == len(importances_2):
            df_imp_2 = pd.DataFrame({'Variable': toutes_les_cols_2, 'Importance': importances_2})
            
            df_top10_m2 = df_imp_2.sort_values(by='Importance', ascending=True).tail(10)

            fig_imp_2 = px.bar(
                df_top10_m2, 
                x='Importance', 
                y='Variable', 
                orientation='h',
                title="Top 10 des facteurs déterminants - Modèle 2 (Club + ligue)",
                text_auto='.1%' 
            )
            
            fig_imp_2.update_traces(marker_color='#c084fc', textposition='outside')
            fig_imp_2.update_layout(xaxis_title="Impact sur la valeur (%)", yaxis_title="")
            
            st.plotly_chart(fig_imp_2, use_container_width=True)
            
        else:
            st.warning(f"Note : Le nombre de colonnes ({len(toutes_les_cols_2)}) diffère des scores ({len(importances_2)}).")

    except Exception as e:
        st.error(f"Erreur lors de l'analyse du Modèle 2 : {e}")

    st.info("""
            **Analyse du modèle 1:**
            
            On constate que le modèle ne se focalise pas uniquement sur les statistiques individuelles (buts, passes). 
            Il priorise deux axes majeurs pour fixer le prix :
            1. **Le Palmarès (19%)** : Avoir gagné des trophées récemment augmente drastiquement la valeur.
            2. **La Fiabilité & Régularité (~22%)** : Le cumul des matchs joués sur les deux dernières saisons est déterminant. Un joueur disponible vaut plus cher qu'un joueur souvent blessé ou remplaçant.
            
            Pour le second modèle, c'est la valeur du club qui explique en grande partie le prix du joueur, c'est ensuite l'âge et les performances individuelles.
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

        st.markdown("### Critères de recherche")
        
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
        
        max_val = top_20['plus_value'].max() if len(top_20) > 0 else 100 

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
        
        st.info("**Remarque :** Les joueurs avec une forte plus-value sont souvent des éléments performants évoluant dans des ligues et/ou clubs moins médiatisées. Ce sont des bonnes cibles pour les recruteurs.")

# --- PAGE 4 : SIMULATEUR ---
elif choix_page == "🔮 Simulateur":
        st.caption("Modifiez les performances pour voir l'impact sur la valeur marchande.")

        # --- SÉLECTION DU JOUEUR ---
        liste_joueurs = sorted(df['nom'].unique())

        dict_affichage = {}
        for index, ligne in df.iterrows():
            dict_affichage[ligne['nom']] = f"{ligne['nom']} ({ligne['position']} - {ligne['club']})"

        joueur_simu = st.selectbox(
            "Sélectionnez un joueur :", 
            liste_joueurs,
            format_func=lambda x: dict_affichage.get(x, x)
        
        )

        ligne_original = df[df['nom'] == joueur_simu].iloc[0]

        st.markdown("---")

        # --- INTERFACE DE SIMULATION ---
        st.subheader("Paramètres de la simulation")
        
        col_simu_1, col_simu_2, col_simu_3 = st.columns(3)

        # --- COLONNE 1  ---
        with col_simu_1:
            st.markdown("##### 👤 Profil & Contrat")
            
            nouvel_age = st.number_input(
            "Âge", 
            value=int(ligne_original['age']), 
            step=1, 
            min_value=15, max_value=45
            )
            
            annees_restantes = ligne_original['fin_contrat'] / 365
            nouvelle_duree = st.slider(
            "Années de contrat restantes", 
            min_value=0.0, max_value=5.0, 
            value=float(annees_restantes),
            step=0.5
            )
            nouveaux_jours_contrat = nouvelle_duree * 365

        # --- COLONNE 2  ---
        with col_simu_2:
            st.markdown("##### ⏱️ Temps de jeu (24/25)")
            
            nouveaux_matchs = st.slider(
            "Matchs joués", 
            min_value=0, max_value=80, 
            value=int(ligne_original['matchs_24_25'])
            )
            
            # --- CORRECTION DU CALCUL DES MINUTES ---
            minutes_actuelles = ligne_original['minutes_24_25']
            matchs_actuels = ligne_original['matchs_24_25']
            
            if matchs_actuels > 0 and minutes_actuelles > 0:
                ratio_min_match = minutes_actuelles / matchs_actuels
            else:
                ratio_min_match = 90 
            
            if ratio_min_match > 100: 
                ratio_min_match = 90
            
            nouvelles_minutes = nouveaux_matchs * ratio_min_match
            
            st.caption(f"Minutes estimées : **{nouvelles_minutes:,.0f}**")

        # --- COLONNE 3 ---
        with col_simu_3:
            st.markdown("##### 🏆 Stats & Palmarès")
            
            nouveaux_trophees = st.number_input(
            "Trophées (3 dernières années)",
            min_value=0,
            value=int(ligne_original['nb_trophees_3ans']),
            step=1
            )
            
            est_gardien = "Gardien" in str(ligne_original['position'])
            
            if est_gardien:
                nouveaux_clean_sheets = st.number_input(
                    "Clean Sheets", 
                    min_value=0, max_value=nouveaux_matchs,
                    value=int(ligne_original['clean_sheets_24_25'])
                )
                nouveaux_buts_encaisses = st.number_input(
                    "Buts Encaissés", min_value=0,
                    value=int(ligne_original['buts_encaisses_24_25'])
                )
                nouveaux_buts = 0
                nouvelles_passes = 0
            else:
                nouveaux_buts = st.number_input(
                    "Buts marqués", min_value=0, 
                    value=int(ligne_original['buts_24_25'])
                )
                nouvelles_passes = st.number_input(
                    "Passes décisives", min_value=0, 
                    value=int(ligne_original['passes_d_24_25'])
                )
                nouveaux_clean_sheets = 0
                nouveaux_buts_encaisses = 0

        df_simule = pd.DataFrame(ligne_original).T 
        
        df_simule['age'] = nouvel_age
        df_simule['fin_contrat'] =  nouveaux_jours_contrat
        
        df_simule['matchs_24_25'] = nouveaux_matchs
        df_simule['minutes_24_25'] = nouvelles_minutes
        
        df_simule['nb_trophees_3ans'] = nouveaux_trophees
        
        df_simule['buts_24_25'] = nouveaux_buts
        df_simule['passes_d_24_25'] = nouvelles_passes
        df_simule['clean_sheets_24_25'] = nouveaux_clean_sheets
        df_simule['buts_encaisses_24_25'] = nouveaux_buts_encaisses

        try:
            prix_simule = best_model.predict(df_simule)[0]
            prix_actuel_ia = ligne_original['valeur_estimee']
            
            delta_prix = prix_simule - prix_actuel_ia
            variation_percent = (delta_prix / prix_actuel_ia) * 100 if prix_actuel_ia > 0 else 0

            st.markdown("---")
            st.subheader("Résultat de la simulation")

            col_res_1, col_res_2, col_res_3 = st.columns(3)
            
            with col_res_1:
                st.metric(
                    "Valeur Modèle",
                    f"{prix_actuel_ia:,.0f} €".replace(',', ' '),
                    help="Estimation basée sur les stats réelles"
                )
            
            with col_res_2:
                st.metric(
                    "Valeur Simulée",
                    f"{prix_simule:,.0f} €".replace(',', ' '),
                    delta=f"{delta_prix:,.0f} €",
                    help="Estimation avec vos modifications"
                )
            
            with col_res_3:
                couleur = "green" if variation_percent > 0 else "red"
                if variation_percent == 0: couleur = "gray"
            
                st.markdown(f"""
                ### Impact : :{couleur}[{variation_percent:+.2f}%]
                """)

        except Exception as e:
            st.error(f"Erreur lors de la simulation : {e}")

        st.caption("Note : Les variations ne sont pas toujours linéaires. Le modèle se base sur des profils types existants.")

# --- PAGE 5 : À PROPOS ---
elif choix_page == "ℹ️ À propos":
        
        
        st.markdown("""
        ### Origine du projet
        Dans le cadre de notre cours « Web Scraping et Machine Learning » du Master 2 MECEN à l'Université de Tours, nous avons souhaité allier notre passion commune pour le football à nos compétences en Data Science. Partant du constat que l'évaluation d'un joueur lors du mercato est souvent biaisée par la "hype" ou l'émotion, nous avons cherché à rationaliser ce processus. Ce projet académique a pour but de fournir une analyse objective aux recruteurs : en nous basant uniquement sur la performance statistique réelle (via le scraping de données et l'entraînement de modèles prédictifs), notre outil vise à définir la "juste valeur" marchande des joueurs et à détecter les opportunités sous-cotées du marché.
        """)

        st.markdown("---")

        st.markdown("""
        ### Méthodologie & Organisation du projet
        
        Le premier objectif de ce projet a été de constituer une base de données complète. Pour cela, nous avons utilisé la méthode de **web scraping** sur le site de référence *Transfermarkt*. Cela nous a permis de récupérer les fiches de tous les joueurs évoluant dans les 5 grands championnats européens pour créer notre propre dataset.

        Une phase importante de **nettoyage des données** a ensuite été nécessaire. En effet, selon la popularité des joueurs, certaines fiches étaient incomplètes ou comportaient des valeurs manquantes. Il a fallu trier et traiter ces informations pour obtenir une base propre et exploitable par nos algorithmes.

        La seconde partie repose sur l'utilisation du **Machine Learning**. Nous avons entraîné plusieurs modèles pour prédire la valeur marchande d'un joueur, mais avec une stratégie bien précise : nous avons volontairement retenu **uniquement les statistiques sportives** (buts, passes, âge, régularité... ) pour l'entraînement. 
        
        C'est un choix crucial : si nous avions donné au modèle le nom du club actuel ou la réputation du joueur, il aurait simplement appris à copier les prix du marché. Or, notre objectif est inverse : nous voulons supprimer tout ce qui relève de la "hype" ou du marketing pour isoler et calculer la **valeur purement sportive** du joueur.
        """)

        st.markdown("---")
        
        st.markdown("""
        ### L'outil au service du Mercato
        
        L'objectif de cette application est de rationaliser la prise de décision sur le marché des transferts. Elle a été conçue comme un assistant pour les recruteurs, permettant de naviguer entre l'analyse du présent et la projection vers le futur.
        
        **Voici comment utiliser les différentes fonctionnalités de l'outil :**
        
        * **1. Profil & Visualisation :** C'est le point d'entrée pour analyser un joueur spécifique. Cette section offre une vue d'ensemble sur les **statistiques générales et récentes**. Elle permet de valider le profil d'un joueur et de juger sa régularité.
            
        * **2. Estimation (Le Cœur du Projet) :** C'est la fonctionnalité centrale de notre travail. Ici, notre modèle calcule la **valeur purement sportive** du joueur. 
            
        * **3. Détection de Pépites :** Cette page sert à repérer les **anomalies du marché**. Elle filtre automatiquement la base de données pour faire ressortir les joueurs que notre modèle considère comme "sous-cotés". C'est l'outil idéal pour identifier de potentielles bonnes recrues à fort retour sur investissement.
            
        * **4. Simulateur Interactif :** Un espace d'expérimentation qui permet de **jouer avec les statistiques**. Vous pouvez modifier les performances d'un joueur (ajouter des buts, prolonger un contrat, augmenter le temps de jeu...) pour observer instantanément comment ces changements impacteraient sa valeur marchande.
        """)

        st.markdown("---")

        st.markdown("""
        ### Limites et Perspectives d'amélioration
        
        Notre application n'est pas sans limites et reste un projet académique. 
        Elle n'est pas dynamique car le scraping des données n'est pas automatique : elle est donc utile pour le mercato hivernal 2025/2026, mais pas au-delà dans son état actuel.
        
        L'amélioration première serait de rendre automatique le scraping des données et de permettre la visualisation des 3 dernières saisons en continu.
        """)

        st.caption("Développé par Yann BROCHET et Iruomachi IRUOMAH - Master 2 Économie de l'entreprise et des marchés - 2025/2026")