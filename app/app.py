import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go

# --- CONFIGURATION DE LA PAGE ---

st.set_page_config(
    page_title="Football Moneyball ⚽",
    page_icon="⚽",
    layout="wide"
)

# --- CHARGEMENT DES DONNÉES ---

@st.cache_data
def load_data():
    dossier_actuel = os.path.dirname(os.path.abspath(__file__))
    
    chemin_csv = os.path.join(dossier_actuel, '..', 'data', 'dataset_avec_predictions.csv')

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

pages = ["📊 Profil Joueur", "🔎 Analyse & Robustesse", "💎 Pépites", "🔮 Simulateur", "ℹ️ À Propos"]
choix_page = st.sidebar.radio("Menu", pages)

st.sidebar.markdown("---")
st.sidebar.info(f"Nombre de joueur dans la base de donnée : {len(df)}")
st.title(f"{choix_page}")

# --- PAGE 1 : PROFIL JOUEUR ---
if choix_page == "📊 Profil Joueur":
    st.header("Visualisation : Fiche Joueur")
    col_ligue, col_club, col_joueur = st.columns(3)

    with col_ligue:
        liste_ligues = sorted(df['ligue'].astype(str).unique())
        ligue_sel = st.selectbox("1️⃣ Choisir la Ligue", liste_ligues)

    df_ligue = df[df['ligue'] == ligue_sel]

    with col_club:
        liste_clubs = sorted(df_ligue['club'].astype(str).unique())
        club_sel = st.selectbox("2️⃣ Choisir le Club", liste_clubs)

    df_club = df_ligue[df_ligue['club'] == club_sel]

    with col_joueur:
        liste_joueurs = sorted(df_club['nom'].astype(str).unique())
        joueur_sel = st.selectbox("3️⃣ Choisir le Joueur", liste_joueurs)

    joueur_data = df_club[df_club['nom'] == joueur_sel].iloc[0]

    st.markdown("---")

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

    st.markdown("### 📋 Détails supplémentaires") 
    
    config_affichage = {
        'taille': 'Taille',
        'pied': 'Pied fort',
        'selections_inter': 'Nombre de sélections internationales',
        'nb_trophees_3ans': 'Nombre de trophées ces 3 dernières années',
        'fin_contrat': 'Nombre de jours avant fin de contrat',
        'nb_blessures_3ans': 'Nombre de blessures ces 3 dernières années',
        'matchs_manques_3ans': "Nombre d'abscences ces 3 dernières années"
    } 
    donnees_tableau = {}
    
    for col_technique, nom_joli in config_affichage.items():
        if col_technique in df.columns:
            valeur = joueur_data[col_technique]
            
            if pd.notna(valeur) and isinstance(valeur, (int, float)):
    
                if col_technique == 'taille':
                    valeur = f"{valeur:.2f}"

                else:
                    valeur = f"{valeur:,.0f}".replace(',', ' ')
            
            elif pd.isna(valeur):
                valeur = "-"
                
            donnees_tableau[nom_joli] = valeur

    df_affichage = pd.DataFrame(donnees_tableau.items(), columns=['Indicateur', 'Valeur'])
    
    st.dataframe(
        df_affichage, 
        hide_index=True, 
        use_container_width=True
    )



# --- PAGE 2 : ANALYSE ---
elif choix_page == "🔎 Analyse & Robustesse":
    st.header("Analyse : Réel vs Estimé")
    st.info("Ici on affichera le Delta de valeur et les stats de robustesse du modèle.")

# --- PAGE 3 : PÉPITES ---
elif choix_page == "💎 Pépites":
    st.header("Chasse aux Pépites (Moneyball)")
    st.info("Ici on affichera le Top 10 des joueurs sous-cotés et le Scatter Plot.")

# --- PAGE 4 : SIMULATEUR ---
elif choix_page == "🔮 Simulateur":
    st.header("Simulateur de Valeur")
    st.info("Ici on pourra modifier les stats d'un joueur pour voir sa valeur changer.")

# --- PAGE 5 : À PROPOS ---
elif choix_page == "ℹ️ À Propos":
    st.header("À Propos du Projet")
    st.info("Présentation du projet et de la méthodologie.")