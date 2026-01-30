## Origine du projet

Dans le cadre de notre cours « Web Scraping et Machine Learning » du Master 2 MECEN à l'Université de Tours, nous avons souhaité allier notre passion commune pour le football à nos compétences en Data Science. Partant du constat que l'évaluation d'un joueur lors du mercato est souvent biaisée par la "hype" ou l'émotion, nous avons cherché à rationaliser ce processus. Ce projet académique a pour but de fournir une analyse objective aux recruteurs : en nous basant uniquement sur la performance statistique réelle (via le scraping de données et l'entraînement de modèles prédictifs), notre outil vise à définir la "juste valeur" marchande des joueurs et à détecter les opportunités sous-cotées du marché.

---

## Méthodologie & Organisation du projet

Le premier objectif de ce projet a été de constituer une base de données complète. Pour cela, nous avons utilisé la méthode de **web scraping** sur le site de référence *Transfermarkt*. Cela nous a permis de récupérer les fiches de tous les joueurs évoluant dans les 5 grands championnats européens pour créer notre propre dataset.

Une phase importante de **nettoyage des données** a ensuite été nécessaire. En effet, selon la popularité des joueurs, certaines fiches étaient incomplètes ou comportaient des valeurs manquantes. Il a fallu trier et traiter ces informations pour obtenir une base propre et exploitable par nos algorithmes.

La seconde partie repose sur l'utilisation du **Machine Learning**. Nous avons entraîné plusieurs modèles pour prédire la valeur marchande d'un joueur, mais avec une stratégie bien précise : nous avons volontairement retenu **uniquement les statistiques sportives** (buts, passes, âge, régularité... ) pour l'entraînement.

C'est un choix crucial : si nous avions donné au modèle le nom du club actuel ou la réputation du joueur, il aurait simplement appris à copier les prix du marché. Or, notre objectif est inverse : nous voulons supprimer tout ce qui relève de la "hype" ou du marketing pour isoler et calculer la **valeur purement sportive** du joueur.

---

## L'outil au service du Mercato

L'objectif de cette application est de rationaliser la prise de décision sur le marché des transferts. Elle a été conçue comme un assistant pour les recruteurs, permettant de naviguer entre l'analyse du présent et la projection vers le futur.

**Voici comment utiliser les différentes fonctionnalités de l'outil :**

- **1. Profil & Visualisation :**  
  C'est le point d'entrée pour analyser un joueur spécifique. Cette section offre une vue d'ensemble sur les **statistiques générales et récentes**. Elle permet de valider le profil d'un joueur et de juger sa régularité.

- **2. Estimation (Le Cœur du Projet) :**  
  C'est la fonctionnalité centrale de notre travail. Ici, notre modèle calcule la **valeur purement sportive** du joueur.

- **3. Détection de Pépites :**  
  Cette page sert à repérer les **anomalies du marché**. Elle filtre automatiquement la base de données pour faire ressortir les joueurs que notre modèle considère comme "sous-cotés". C'est l'outil idéal pour identifier de potentielles bonnes recrues à fort retour sur investissement.

- **4. Simulateur Interactif :**  
  Un espace d'expérimentation qui permet de **jouer avec les statistiques**. Vous pouvez modifier les performances d'un joueur (ajouter des buts, prolonger un contrat, augmenter le temps de jeu...) pour observer instantanément comment ces changements impacteraient sa valeur marchande.

---

## Limites et Perspectives d'amélioration

Notre application n'est pas sans limites et reste un projet académique.  
Elle n'est pas dynamique car le scraping des données n'est pas automatique : elle est donc utile pour le mercato hivernal 2025/2026, mais pas au-delà dans son état actuel.

L'amélioration première serait de rendre automatique le scraping des données et de permettre la visualisation des 3 dernières saisons en continu.

---

Développé par Yann BROCHET et Iruomachi IRUOMAH – Master 2 Économie de l'entreprise et des marchés – 2025/2026