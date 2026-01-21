from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class JoueurStats(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    # --- Infos Générales ---
    nom: Optional[str] = Field(alias="Nom")
    nationalite: Optional[str] = Field(alias="Nationalité", default=None)
    ligue: Optional[str] = Field(alias="Ligue", default=None)
    club: Optional[str] = Field(alias="Club", default=None)
    valeur_club: float | str | None = Field(alias="Valeur totale du club", default=None)
    classement_club: int | str | None = Field(alias="Classement actuel du club", default=None)
    age: int | str | None = Field(alias="Âge", default=None)
    taille: float | str | None = Field(alias="Taille", default=None)
    position: Optional[str] = Field(alias="Position", default=None)
    fin_contrat: int | str | None = Field(alias="Fin de contrat dans", default=None)
    valeur: int | float | str | None = Field(alias="Valeur", default=None)
    selections_inter: int | str | None = Field(alias="Nombre de sélections internationales", default=None)
    pied_fort: Optional[str] = Field(alias="Pied fort", default=None)

    # --- SAISON 25/26 ---
    minutes_25_26: int | str | None = Field(alias="Minutes jouées 25/26", default=None)
    matchs_25_26: int | str | None = Field(alias="Nombre de matchs 25/26", default=None)
    entrees_25_26: int | str | None = Field(alias="Nombre d'entrées en jeu 25/26", default=None)
    titularisations_25_26: int | str | None = Field(alias="Nombre de titularisations 25/26", default=None)
    buts_25_26: int | str | None = Field(alias="Nombre de buts 25/26", default=None)
    penaltys_25_26: int | str | None = Field(alias="Nombre de penaltys 25/26", default=None)
    passes_d_25_26: int | str | None = Field(alias="Nombre de passes décisives 25/26", default=None)
    clean_sheets_25_26: int | str | None = Field(alias="Nombre clean de sheets 25/26", default=None)
    buts_encaisses_25_26: int | str | None = Field(alias="Nombre de buts encaissés 25/26", default=None)

    # --- SAISON 24/25 ---
    minutes_24_25: int | str | None = Field(alias="Minutes jouées 24/25", default=None)
    matchs_24_25: int | str | None = Field(alias="Nombre de matchs 24/25", default=None)
    entrees_24_25: int | str | None = Field(alias="Nombre d'entrées en jeu 24/25", default=None)
    titularisations_24_25: int | str | None = Field(alias="Nombre de titularisations 24/25", default=None)
    buts_24_25: int | str | None = Field(alias="Nombre de buts 24/25", default=None)
    penaltys_24_25: int | str | None = Field(alias="Nombre de penaltys 24/25", default=None)
    passes_d_24_25: int | str | None = Field(alias="Nombre de passes décisives 24/25", default=None)
    clean_sheets_24_25: int | str | None = Field(alias="Nombre clean de sheets 24/25", default=None)
    buts_encaisses_24_25: int | str | None = Field(alias="Nombre de buts encaissés 24/25", default=None)

    # --- SAISON 23/24 ---
    minutes_23_24: int | str | None = Field(alias="Minutes jouées 23/24", default=None)
    matchs_23_24: int | str | None = Field(alias="Nombre de matchs 23/24", default=None)
    entrees_23_24: int | str | None = Field(alias="Nombre d'entrées en jeu 23/24", default=None)
    titularisations_23_24: int | str | None = Field(alias="Nombre de titularisations 23/24", default=None)
    buts_23_24: int | str | None = Field(alias="Nombre de buts 23/24", default=None)
    penaltys_23_24: int | str | None = Field(alias="Nombre de penaltys 23/24", default=None)
    passes_d_23_24: int | str | None = Field(alias="Nombre de passes décisives 23/24", default=None)
    clean_sheets_23_24: int | str | None = Field(alias="Nombre clean de sheets 23/24", default=None)
    buts_encaisses_23_24: int | str | None = Field(alias="Nombre de buts encaissés 23/24", default=None)

    # --- EXTRAS ---
    nb_blessures_3ans: int | str | None = Field(alias="Nombre de blessures sur les 3 dernières saisons", default=0)
    matchs_manques_3ans: int | str | None = Field(alias="Nombre de matchs manqués sur les 3 dernières saisons", default=0)
    jours_blessures: int | str | None = Field(alias="Nombre de jours sous blessures", default=0)
    nb_trophees_3ans: int | str | None = Field(alias="Nombre de trophées sur les 3 dernières saisons", default=0)