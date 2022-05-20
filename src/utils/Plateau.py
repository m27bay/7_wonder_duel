"""
Fichier classe Plateau
"""
import random

from src.utils.Carte import Carte
from src.utils.CarteGuilde import CarteGuilde
from src.utils.Colours import Couleurs
from src.utils.JetonMilitaire import JetonMilitaire
from src.utils.Merveille import Merveille
from src.utils.JetonProgres import JetonProgres
from src.utils.Joueur import Joueur


from src.utils.Outils import mon_str_liste2D
import sys

SYMBOLE_SCIENTIFIQUES = [
    "sphere_armillaire",
    "cadran_solaire",
    "pilon",
    "compas_maconniques",
    "plume",
    "roue"
]


class Plateau:
    """
    Classe Plateau
    """

    def __init__(self, joueur1, joueur2, choix_auto_merveilles: bool = True):
        """
        Constructeur de la classe plateau.

        :param joueur1: premier joueur.
        :param joueur2: deuxieme joueur.
        :param choix_auto_merveilles: boolean indiquant si le choix
                des merveilles est automatique ou non.
        """

        if isinstance(joueur1, Joueur) and isinstance(joueur2, Joueur):
            self.joueur1 = joueur1
            self.joueur2 = joueur2
            self.joueur_qui_joue = None
            self.victoire = None  # (nom du joueur, motif)
            # motif : militaire, points victoire, scientifique, égalité

            #
            self.choix_auto_merveilles = choix_auto_merveilles

            self.monnaie_banque = 86  # 14 de valeur 1, 10 de valeur 3, 7 de valeur 6
            self.age = 1

            # 9 : neutre
            # 0 : victoire militaire joueur2
            # 18: victoire militaire joueur1
            self.position_jeton_conflit = 9
            self.jetons_militaire = [
                JetonMilitaire("5piecesJ1", 5, 10),
                JetonMilitaire("2piecesJ1", 2, 5),
                JetonMilitaire("0piecesJ1", 0, 2),
                JetonMilitaire("0piecesJ2", 0, 2),
                JetonMilitaire("2piecesJ2", 2, 5),
                JetonMilitaire("5piecesJ2", 5, 10)]

            # matrice de 0 et Carte
            self.cartes_plateau = []
            self.cartes_defaussees = []
            self.jetons_progres_plateau = []

            # listes des cartes
            # constructeur : Carte(nom, chemin_image, effets, couts, nom_carte_chainage, couleur, age)
            self.cartes_age_I = [
                Carte("chantier", ["ressource bois 1"],
                      None, None, "marron", age=1),
                Carte("exploitation", ["ressource bois 1"], [
                      "monnaie 1"], None, "marron", age=1),
                Carte("bassin argileux", [
                      "ressource argile 1"], None, None, "marron", age=1),
                Carte("cavite", ["ressource argile 1"], [
                      "monnaie 1"], None, "marron", age=1),
                Carte("gisement", ["ressource pierre 1"],
                      None, None, "marron", age=1),
                Carte("mine", ["ressource pierre 1"], [
                      "monnaie 1"], None, "marron", age=1),
                Carte("verrerie", ["ressource verre 1"], [
                      "monnaie 1"], None, "gris", age=1),
                Carte("presse", ["ressource papyrus 1"], [
                      "monnaie 1"], None, "gris", age=1),
                Carte("tour de garde", ["attaquer 1"],
                      None, None, "rouge", age=1),
                Carte("atelier",
                      [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[3]}", "point_victoire 1"], [
                          "ressource papyrus 1"],
                      None, "vert", age=1),
                Carte("apothicaire",
                      [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[5]}", "point_victoire 1"], [
                          "ressource verre 1"],
                      None, "vert", age=1),
                Carte("depot de pierre", ["reduc_ressource pierre 1"], [
                      "monnaie 3"], None, "jaune", age=1),
                Carte("depot d argile", ["reduc_ressource argile 1"], [
                      "monnaie 3"], None, "jaune", age=1),
                Carte("depot de bois", ["reduc_ressource bois 1"], [
                      "monnaie 3"], None, "jaune", age=1),
                Carte("ecuries", ["attaquer 1"], [
                      "ressource bois 1"], None, "rouge", age=1),
                Carte("caserne", ["attaquer 1"], [
                      "ressource argile 1"], None, "rouge", age=1),
                Carte("palissade", ["attaquer 1"], [
                      "monnaie 2"], None, "rouge", age=1),
                Carte("scriptorium", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[4]}"], [
                      "monnaie 2"], None, "vert", age=1),
                Carte("officine", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[2]}"], [
                      "monnaie 2"], None, "vert", age=1),
                Carte("theatre", ["point_victoire 3"],
                      None, None, "bleu", age=1),
                Carte("autel", ["point_victoire 3"],
                      None, None, "bleu", age=1),
                Carte("bains", ["point_victoire 3"], [
                      "ressource pierre 1"], None, "bleu", age=1),
                Carte("taverne", ["monnaie 4"], None, None, "jaune", age=1)
            ]

            self.cartes_age_II = [
                Carte("scierie", ["ressource bois 2"], [
                      "monnaie 2"], None, "marron", age=2),
                Carte("briqueterie", ["ressource argile 2"], [
                      "monnaie 2"], None, "marron", age=2),
                Carte("carriere", ["ressource pierre 2"], [
                      "monnaie 2"], None, "marron", age=2),
                Carte("soufflerie", ["ressource verre 1"],
                      None, None, "gris", age=2),
                Carte("sechoir", ["ressource papyrus 1"],
                      None, None, "gris", age=2),
                Carte("muraille", ["attaquer 2"], [
                      "ressource pierre 2"], None, "rouge", age=2),
                Carte("forum", ["ressource_au_choix verre papyrus"], ["monnaie 3", "ressource argile 1"],
                      None, "jaune", age=2),
                Carte("caravanserail", ["ressource_au_choix bois argile pierre"],
                      ["monnaie 2", "ressource verre 1", "ressource papyrus 1"], None, "jaune", age=2),
                Carte("douanes", ["reduc_ressource papyrus 1", "reduc_ressource verre 1"], ["monnaie 4"],
                      None, "jaune", age=2),
                Carte("tribunal", ["point_victoire 5"], ["ressource bois 2", "ressource verre 1"], None,
                      "bleu", age=2),
                Carte("haras", ["attaquer 1"], [
                      "ressource argile 1", "ressource bois 1"], "ecuries", "rouge", age=2),
                Carte("baraquements", ["attaquer 1"], [
                      "monnaie 3"], "caserne", "rouge", age=2),
                Carte("champ de tir", ["attaquer 2"],
                      ["ressource pierre 1", "ressource bois 1",
                          "ressource papyrus 1"],
                      None, "rouge", age=2),
                Carte("place d armes", ["attaquer 2"], ["ressource argile 2", "ressource verre 1"], None, "rouge",
                      age=2),
                Carte("bibliotheque", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[4]}", "point_victoire 2"],
                      ["ressource pierre 1", "ressource bois 1", "ressource verre 1"], "scriptorium", "vert", age=2),
                Carte("dispensaire", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[2]}", "point_victoire 2"],
                      ["ressource argile 2", "ressource verre 1"], "officine", "vert", age=2),
                Carte("ecole", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[5]}", "point_victoire 1"],
                      ["ressource papyrus 2", "ressource bois 1"], None, "vert", age=2),
                Carte("laboratoire", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[3]}", "point_victoire 1"],
                      ["ressource verre 2", "ressource bois 1"], None, "vert", age=2),
                Carte("statue", ["point_victoire 4"], [
                      "ressource argile 2"], "theatre", "bleu", age=2),
                Carte("temple", ["point_victoire 4"], ["ressource papyrus 1", "ressource bois 1"], "autel",
                      "bleu", age=2),
                Carte("aqueduc", ["point_victoire 5"], [
                      "ressource pierre 3"], "bains", "bleu", age=2),
                Carte("rostres", ["point_victoire 4"], ["ressource pierre 1", "ressource bois 1"],
                      None, "bleu", age=2),
                Carte("brasserie", ["monnaie 6"],
                      None, "taverne", "jaune", age=2)
            ]

            self.cartes_age_III = [
                Carte("arsenal", ["attaquer 3"], [
                      "ressource argile 3", "ressource bois 2"], None, "rouge", age=3),
                Carte("pretoire", ["attaquer 3"], [
                      "monnaie 8"], None, "rouge", age=3),
                Carte("academie", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[1]}", "point_victoire 3"],
                      ["ressource pierre 1", "ressource bois 1", "ressource verre 2"], None, "vert", age=3),
                Carte("etude", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[1]}", "point_victoire 3"],
                      ["ressource papyrus 1", "ressource bois 2", "ressource verre 1"], None, "vert", age=3),
                Carte("chambre de commerce", ["monnaie_par_carte gris 3", "point_victoire 3"],
                      ["ressource papyrus 2"], None, "jaune", age=3),
                Carte("port", ["monnaie_par_carte marron 2", "point_victoire 3"],
                      ["ressource verre 1", "ressource bois 1", "ressource papyrus 1"], None, "jaune", age=3),
                Carte("armurerie", ["monnaie_par_carte rouge 1", "point_victoire 3"],
                      ["ressource pierre 2", "ressource verre 1"], None, "jaune", age=3),
                Carte("palace", ["point_victoire 7"],
                      ["ressource argile 1", "ressource pierre 1",
                          "ressource bois 1", "ressource verre 2"],
                      None, "bleu", age=3),
                Carte("hotel de ville", ["point_victoire 7"], ["ressource pierre 3", "ressource bois 2"],
                      None, "bleu", age=3),
                Carte("obelisque", ["point_victoire 5"], ["ressource pierre 2", "ressource verre 1"],
                      None, "bleu", age=3),
                Carte("fortifications", ["attaquer 2"],
                      ["ressource pierre 2", "ressource argile 1",
                          "ressource papyrus 1"],
                      "palissade", "rouge", age=3),
                Carte("atelier de siege", ["attaquer 2"], ["ressource bois 3", "ressource verre 1"],
                      "champ de tir", "rouge", age=3),
                Carte("cirque", ["attaquer 2"], ["ressource argile 2", "ressource pierre 2"],
                      "place d armes", "rouge", age=3),
                Carte("universite", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[0]}", "point_victoire 2"],
                      ["ressource argile 1", "ressource verre 1", "ressource papyrus 1"], "ecole", "vert", age=3),
                Carte("observatoire", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[0]}", "point_victoire 2"],
                      ["ressource pierre 1", "ressource papyrus 2"], "laboratoire", "vert", age=3),
                Carte("jardins", ["point_victoire 6"], ["ressource argile 2", "ressource bois 2"], "statue",
                      "bleu", age=3),
                Carte("pantheon", ["point_victoire 6"],
                      ["ressource argile 1", "ressource bois 1",
                          "ressource papyrus 2"],
                      "temple", "bleu", age=3),
                Carte("senat", ["point_victoire 5"],
                      ["ressource argile 2", "ressource pierre 1",
                          "ressource papyrus 2"],
                      "rostres", "bleu", age=3),
                Carte("phare", ["monnaie_par_carte jaune 1", "point_victoire 3"],
                      ["ressource argile 2", "ressource verre 1"], "taverne", "jaune", age=3),
                Carte("arene", ["monnaie_par_merveille 2", "point_victoire 3"],
                      ["ressource argile 1", "ressource pierre 1", "ressource bois 1"], "brasserie", "jaune", age=3),
            ]

            self.cartes_guilde = [
                CarteGuilde("guilde des commercants",
                            ["effet_guild_commercants 1"],
                            ["ressource argile 1", "ressource bois 1",
                                "ressource verre 1", "ressource papyrus 1"]
                            ),
                CarteGuilde("guilde des armateurs",
                            ["effet_guild_armateurs 1"],
                            ["ressource argile 1", "ressource pierre 1",
                                "ressource verre 1", "ressource papyrus 1"]
                            ),
                CarteGuilde("guilde des batisseurs",
                            ["effet_guild_batisseurs 1"],
                            ["ressource pierre 2", "ressource argile 1", "ressource bois 1",
                             "ressource papyrus 1", "ressource verre 1"]
                            ),
                CarteGuilde("guilde des magistrats",
                            ["effet_guild_magistrats 1"],
                            ["ressource bois 2", "ressource argile 1",
                                "ressource papyrus 1"]
                            ),
                CarteGuilde("guilde des scientifiques",
                            ["effet_guild_scientifiques 1"],
                            ["ressource argile 2", "ressource bois 2"]
                            ),
                CarteGuilde("guilde des usuriers",
                            ["effet_guild_usuriers 1"],
                            ["ressource pierre 2", "ressource bois 2"]
                            ),
                CarteGuilde("guilde des tacticiens",
                            ["effet_guild_tacticiens 1"],
                            ["ressource pierre 2", "ressource argile 1",
                                "ressource papyrus 1"]
                            )
            ]

            # constructeur : CarteFille(nom, chemin_image, effets)
            self.merveilles = [
                Merveille("circus maximus",
                              ["defausse_carte_adversaire gris",
                                  "attaquer 1", "point_victoire 3"],
                          ["ressource pierre 2", "ressource bois 1",
                              "ressource verre 1"]
                          ),
                Merveille("colosse",
                          ["attaquer 2", "point_victoire 3"],
                          ["ressource argile 3", "ressource verre 1"]
                          ),
                Merveille("grand phare",
                          ["ressource_au_choix bois argile pierre",
                              "point_victoire 4"],
                          ["ressource bois 1", "ressource pierre 1",
                              "ressource papyrus 2"]
                          ),
                Merveille("jardin suspendus",
                          ["monnaie 6", "rejouer", "point_victoire 3"],
                          ["ressource bois 2 ", "ressource verre 1",
                              "ressource papyrus 1"]
                          ),
                Merveille("grande bibliotheque",
                          ["jeton_progres_aleatoire", "point_victoire 4"],
                          ["ressource bois 3", "ressource verre 1",
                              "ressource papyrus 1"]
                          ),
                Merveille("mausolee",
                          ["construction_fausse_gratuite", "point_victoire 2"],
                          ["ressource argile 2", "ressource verre 2",
                              "ressource papyrus 1"]
                          ),
                Merveille("piree",
                          ["ressource_au_choix papyrus verre",
                              "rejouer", "point_victoire 2"],
                          ["ressource bois 2", "ressource pierre 1",
                              "ressource argile 1"]
                          ),
                Merveille("pyramides",
                          ["point_victoire 9"],
                          ["ressource pierre 3", "ressource papyrus 1"]
                          ),
                Merveille("sphinx",
                          ["rejouer", "point_victoire 6"],
                          ["ressource pierre 1", "ressource argile 1",
                              "ressource verre 2"]
                          ),
                Merveille("statue de zeus",
                          ["defausse_carte_adversaire marron",
                              "attaquer 1", "point_victoire 3"],
                          ["ressource pierre 1", "ressource bois 1",
                           "ressource argile 1", "ressource papyrus 2"]
                          ),
                Merveille("temple d artemis",
                          ["monnaie 12", "rejouer"],
                          ["ressource bois 1", "ressource pierre 1",
                           "ressource verre 1", "ressource papyrus 1"]
                          ),
                Merveille("via appia",
                          ["monnaie 3", "adversaire_perd_monnaie 3",
                              "rejouer", "point_victoire 3"],
                          ["ressource pierre 2", "ressource argile 2",
                              "ressource papyrus 1"]
                          )
            ]

            self.jetons_progres = [
                JetonProgres("agriculture", ["monnaie 6", "point_victoire 4"]),
                JetonProgres("architecture", ["reduc_merveille"]),
                JetonProgres("economie", ["gain_monnaie_adversaire"]),
                JetonProgres("loi", ["symbole_scientifique"]),
                JetonProgres("maconnerie", ["reduc_carte bleu"]),
                JetonProgres("philosophie", ["point_victoire_fin_partie 7"]),
                JetonProgres("mathematiques", [
                             "point_victoire_par_jeton 3", "point_victoire 3"]),
                JetonProgres("strategie", ["bonus_attaque"]),
                JetonProgres("theologie", ["rejouer"]),
                JetonProgres(
                    "urbanisme", ["monnaie 6", "bonus_monnaie_chainage 4"]),
            ]

        else:
            self.joueur1 = None
            self.joueur2 = None
            self.joueur_qui_joue = None
            self.victoire = None
            self.choix_auto_merveilles = None
            self.monnaie_banque = None
            self.age = None
            self.position_jeton_conflit = None

            self.jetons_militaire = []
            self.cartes_age_I = []
            self.cartes_age_II = []
            self.cartes_age_III = []
            self.cartes_guilde = []
            self.cartes_plateau = []
            self.cartes_defaussees = []
            self.merveilles = []
            self.jetons_progres = []
            self.jetons_progres_plateau = []

    def constructeur_par_copie(self):
        plateau = Plateau(None, None)

        plateau.joueur1 = self.joueur1.constructeur_par_copie()
        plateau.joueur2 = self.joueur2.constructeur_par_copie()

        if self.victoire is not None:
            plateau.victoire = self.victoire

        if self.joueur_qui_joue == self.joueur1:
            plateau.joueur_qui_joue = plateau.joueur1
        elif self.joueur_qui_joue == self.joueur2:
            plateau.joueur_qui_joue = plateau.joueur2

        plateau.choix_auto_merveilles = self.choix_auto_merveilles
        plateau.monnaie_banque = self.monnaie_banque
        plateau.age = self.age
        plateau.position_jeton_conflit = self.position_jeton_conflit

        for jetons_militaire in self.jetons_militaire:
            plateau.jetons_militaire.append(
                jetons_militaire.constructeur_par_copie())

        for carte in self.cartes_age_I:
            plateau.cartes_age_I.append(carte.constructeur_par_copie())
        for carte in self.cartes_age_II:
            plateau.cartes_age_II.append(carte.constructeur_par_copie())
        for carte in self.cartes_age_III:
            plateau.cartes_age_III.append(carte.constructeur_par_copie())
        for carte in self.cartes_guilde:
            plateau.cartes_guilde.append(carte.constructeur_par_copie())

        for _, ligne_carte in enumerate(self.cartes_plateau):
            copie_ligne = []
            for _, carte in enumerate(ligne_carte):
                if carte != 0:
                    copie_ligne.append(carte.constructeur_par_copie())
                else:
                    copie_ligne.append(0)
            plateau.cartes_plateau.append(copie_ligne)

        for carte in self.cartes_defaussees:
            plateau.cartes_defaussees.append(carte.constructeur_par_copie())

        for merveille in self.merveilles:
            plateau.merveilles.append(merveille.constructeur_par_copie())

        plateau.jetons_progres = self.jetons_progres.copy()
        plateau.jetons_progres_plateau = self.jetons_progres_plateau.copy()

        return plateau

    def __eq__(self, other):
        if isinstance(other, Plateau):
            return self.joueur1 == other.joueur1 \
                and self.joueur2 == other.joueur2 \
                and self.joueur_qui_joue == other.joueur_qui_joue \
                and self.choix_auto_merveilles == other.choix_auto_merveilles \
                and self.monnaie_banque == other.monnaie_banque \
                and self.age == other.age \
                and self.position_jeton_conflit == other.position_jeton_conflit \
                and self.jetons_militaire == other.jetons_militaire \
                and self.cartes_age_I == other.cartes_age_I \
                and self.cartes_age_II == other.cartes_age_II \
                and self.cartes_age_III == other.cartes_age_III \
                and self.cartes_guilde == other.cartes_guilde \
                and self.cartes_plateau == other.cartes_plateau \
                and self.cartes_defaussees == other.cartes_defaussees \
                and self.merveilles == other.merveilles \
                and self.jetons_progres == other.jetons_progres \
                and self.jetons_progres_plateau == other.jetons_progres_plateau

        return False

    def __str__(self):
        return f"cartes_plateau : {mon_str_liste2D(self.cartes_plateau)}" \
            f"j1 : {str(self.joueur1)}\n" \
            f"j2 : {str(self.joueur2)}\n" \
            f"joueur_qui_joue : {self.joueur_qui_joue.nom}\n" \
            f"position_jeton_conflit : {self.position_jeton_conflit}\n"

    def preparation_plateau(self) -> None:
        """
        Prepare le plateau, les cartes, les jetons_progres, la monnaie des joueurs, les merveilles des joueurs.
        """
        self.__preparation_cartes()
        self.__preparation_jetons_progres()
        self.__preparation_monnaies_joueurs()
        self.__preparation_merveilles()
        self.joueur_qui_joue = self.joueur1

    def __preparation_cartes(self) -> None:
        """
        Methode privee.

        Prepare les cartes, sort aleatoirement des cartes et le place selon
        une structure precise.
        """

        # preparation de la structure des cartes en fonction de l age.
        if self.age == 1:
            self.cartes_plateau = [
                [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
                [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
                [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
            ]

            liste_carte = self.cartes_age_I

            # suppression de 3 cartes
            # il nous faut 20 cartes parmis les 23
            for _ in range(3):
                carte_random = random.choice(liste_carte)
                liste_carte.remove(carte_random)

        elif self.age == 2:
            self.cartes_plateau = [
                [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
                [0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0]
            ]

            liste_carte = self.cartes_age_II

            # suppression de 3 cartes
            # il nous faut 20 cartes parmis les 23
            for _ in range(3):
                carte_random = random.choice(liste_carte)
                liste_carte.remove(carte_random)

        else:  # Age 3
            self.cartes_plateau = [
                [0, 0, 1, 0, 1, 0, 0],
                [0, 1, 0, 1, 0, 1, 0],
                [1, 0, 1, 0, 1, 0, 1],
                [0, 1, 0, 0, 0, 1, 0],
                [1, 0, 1, 0, 1, 0, 1],
                [0, 1, 0, 1, 0, 1, 0],
                [0, 0, 1, 0, 1, 0, 0]
            ]

            liste_carte = self.cartes_age_III

            # suppression de 3 cartes
            # il nous faut 17 cartes parmis les 20
            for _ in range(3):
                carte_random = random.choice(liste_carte)
                liste_carte.remove(carte_random)

            # ajout de 3 cartes guilde
            for _ in range(3):
                carte_guild_random = random.choice(self.cartes_guilde)
                self.cartes_guilde.remove(carte_guild_random)
                liste_carte.append(carte_guild_random)

        # remplissage de la structure avec des cartes aleatoires.
        for num_ligne, ligne_carte in enumerate(self.cartes_plateau):
            for num_colonne, _ in enumerate(ligne_carte):
                if self.cartes_plateau[num_ligne][num_colonne] == 1:

                    nouvelle_carte = random.choice(liste_carte)
                    liste_carte.remove(nouvelle_carte)

                    # une ligne sur deux la carte sont face cachee,
                    # par defaut une carte n est pas face cachee
                    if num_ligne % 2 != 0:
                        nouvelle_carte.cacher()

                    self.cartes_plateau[num_ligne][num_colonne] = nouvelle_carte

    def __preparation_jetons_progres(self) -> None:
        """
        Methode privee.

        Prepare les 5 jetons_progres progres aleatoire du plateau.
        """

        for _ in range(5):
            jeton_random = random.choice(self.jetons_progres)
            self.jetons_progres.remove(jeton_random)
            self.jetons_progres_plateau.append(jeton_random)

    def __preparation_monnaies_joueurs(self) -> None:
        """
        Methode privee.

        Prepare les monnaies des deux joueurs.
        """

        self.joueur1.monnaie = self.joueur2.monnaie = 7
        self.monnaie_banque -= 14

    def __preparation_merveilles(self) -> None:
        """
        Methode privee.

        Prepare les merveilles.
        Sort aleatoirement 4 merveiles, le joueur1 en choisie 1, puis le joueur2 en choisie 2,
        enfin le joueur1 prend la derniere.
        Sort aleatoirement 4 merveiles, le joueur2 en choisie 1, puis le joueur1 en choisie 2,
        enfin le joueur2 prend la derniere.
        """

        if not self.choix_auto_merveilles:
            # choix de 4 merveilles pour j1 (sans replacement)
            self.joueur1.merveilles.extend(random.sample(self.merveilles, k=4))
            # suppression des merveilles dans j1
            self.merveilles = [
                merv for merv in self.merveilles if merv not in self.joueur1.merveilles]
            # choix de 4 merveilles pour j2 (sans replacement)
            self.joueur2.merveilles.extend(random.sample(self.merveilles, k=4))
            # suppression des merveilles dans j2
            self.merveilles = [
                merv for merv in self.merveilles if merv not in self.joueur2.merveilles]

        else:  # choix automatique des merveilles (d'apres les regles)
            self.joueur1.merveilles.append(self.merveilles[7])  # pyramides
            self.joueur1.merveilles.append(self.merveilles[2])  # grand phare
            self.joueur1.merveilles.append(
                self.merveilles[10])  # temple d artemis
            self.joueur1.merveilles.append(
                self.merveilles[9])  # statue de zeus

            self.joueur2.merveilles.append(
                self.merveilles[0])  # circus maximus
            self.joueur2.merveilles.append(self.merveilles[6])  # piree
            self.joueur2.merveilles.append(self.merveilles[11])  # via appia
            self.joueur2.merveilles.append(self.merveilles[1])  # colosse

    def adversaire(self):
        if self.joueur_qui_joue == self.joueur1:
            return self.joueur2

        return self.joueur1

    def enlever_carte(self, carte_a_enlever: Carte) -> None:
        """
        Enleve une carte du plateau.

        :param carte_a_enlever: la carte a enlever.
        """
        carte_trouvee = False

        for num_ligne, ligne_carte in enumerate(self.cartes_plateau):
            for num_colonne, carte in enumerate(ligne_carte):
                if carte == carte_a_enlever:

                    self.cartes_plateau[num_ligne][num_colonne] = 0
                    carte_trouvee = True

        if not carte_trouvee:
            print(
                f"{Couleurs.FAIL} ERREUR enlever_carte {carte_a_enlever.nom} : introuvble {Couleurs.FAIL}")
            sys.exit(-1)

        for carte in self.liste_cartes_prenables():
            carte.devoiler()

    def reste_des_cartes(self) -> bool:
        """
        Indique s'il reste des cartes sur le plateau.

        :return: vrai/ faux
        """
        for ligne_carte in self.cartes_plateau:
            for carte in ligne_carte:
                if carte != 0:
                    return True

        return False

    def cartes_prenable(self, ligne: int, colonne: int) -> bool:
        # si la carte est sur la dernière ligne
        if ligne == len(self.cartes_plateau) - 1:
            return True
        # si la carte est sur le bord gauche, pas de "fils" à sa gauche
        if colonne == 0:
            return self.cartes_plateau[ligne + 1][colonne + 1] == 0
        # si la carte est sur le bord droit, pas de "fils" à sa droite
        if colonne == len(self.cartes_plateau[ligne]) - 1:
            return self.cartes_plateau[ligne + 1][colonne - 1] == 0
        # milieu de la matrice
        return (self.cartes_plateau[ligne + 1][colonne - 1] == 0) and (
            self.cartes_plateau[ligne + 1][colonne + 1] == 0)

    def liste_cartes_prenables(self):
        cartes_prenable = []
        for num_ligne, ligne_carte in enumerate(self.cartes_plateau):
            for num_colonne, carte in enumerate(ligne_carte):
                if carte != 0 and self.cartes_prenable(num_ligne, num_colonne):
                    cartes_prenable.append(carte)

        return cartes_prenable

    def changement_age(self):
        if not self.reste_des_cartes():

            if self.age == 3:
                self.fin_de_partie()
                return -1

            self.age += 1
            self.__preparation_cartes()
            return 1

        return 0

    def fin_de_partie(self):
        if self.position_jeton_conflit == 0:
            self.victoire = (self.joueur2.nom, "militaire")

        elif self.position_jeton_conflit == 18:
            self.victoire = (self.joueur1.nom, "militaire")

        elif self.joueur1.nbr_symb_scientifique_diff == 6:
            self.victoire = (self.joueur1.nom, "scientifique")

        elif self.joueur2.nbr_symb_scientifique_diff == 6:
            self.victoire = (self.joueur2.nom, "scientifique")

        else:
            self.joueur1.compter_point_victoire()
            self.joueur2.compter_point_victoire()

            numero_jeton = self.numero_jeton_militaire()
            jeton = self.jetons_militaire[numero_jeton]

            if self.position_jeton_conflit > 9:
                self.joueur1.points_victoire += jeton.points_victoire

            elif self.position_jeton_conflit < 9:
                self.joueur2.points_victoire += jeton.points_victoire

            for nom_carte in ["guilde des armateurs", "guilde des commercants", "guilde des magistrats",
                              "guilde des tacticiens", "guilde des scientifiques"]:
                j1_possede_carte = any(
                    carte_joueur.nom == nom_carte for carte_joueur in self.joueur1.cartes)
                j2_possede_carte = any(
                    carte_joueur.nom == nom_carte for carte_joueur in self.joueur2.cartes)

                if j1_possede_carte or j2_possede_carte:
                    if nom_carte == "guilde des armateurs":
                        recherche = ["gris", "marron"]
                    elif nom_carte == "guilde des commercants":
                        recherche = ["jaune"]
                    elif nom_carte == "guilde des magistrats":
                        recherche = ["bleu"]
                    elif nom_carte == "guilde des tacticiens":
                        recherche = ["rouge"]
                    else:
                        recherche = ["vert"]

                    nbr_carte_recherche_j1 = len(
                        [carte for carte in self.joueur1.cartes if carte.couleur in recherche])
                    nbr_carte_recherche_j2 = len(
                        [carte for carte in self.joueur2.cartes if carte.couleur in recherche])

                    if nbr_carte_recherche_j1 != nbr_carte_recherche_j2:
                        maxi = max(nbr_carte_recherche_j1,
                                   nbr_carte_recherche_j2)
                        joueur = self.joueur1 if maxi == nbr_carte_recherche_j1 else self.joueur2
                        joueur.points_victoire += maxi

            j1_possede_usuriers = any(
                carte_joueur.nom == "guilde des usuriers" for carte_joueur in self.joueur1.cartes)
            j2_possede_usuriers = any(
                carte_joueur.nom == "guilde des usuriers" for carte_joueur in self.joueur2.cartes)

            if j1_possede_usuriers or j2_possede_usuriers:
                if self.joueur1.monnaie != self.joueur2.monnaie:
                    maxi = max(self.joueur1.monnaie, self.joueur2.monnaie)
                    joueur = self.joueur1 if maxi == self.joueur1.monnaie else self.joueur2
                    joueur.points_victoire += int(joueur.monnaie / 3)

            self.joueur1.points_victoire += int(self.joueur1.monnaie / 3)
            self.joueur2.points_victoire += int(self.joueur2.monnaie / 3)

            if self.joueur1.points_victoire > self.joueur2.points_victoire:
                self.victoire = (self.joueur1.nom, "points victoire")

            elif self.joueur1.points_victoire < self.joueur2.points_victoire:
                self.victoire = (self.joueur2.nom, "points victoire")

            else:
                self.victoire = (None, "égalité")

    def action_banque(self, monnaies: int):
        if monnaies == 0:
            return 0

        if self.monnaie_banque == 0:
            print(
                f"{Couleurs.FAIL} ERREUR : la banque n'a plus d'argent {Couleurs.FAIL}")
            sys.exit(-2)

        elif self.monnaie_banque < monnaies:
            gain = self.monnaie_banque
            self.monnaie_banque = 0

        else:
            gain = monnaies
            self.monnaie_banque -= monnaies

        return gain

    def acheter_ressources(self, ressources_manquantes: list) -> int:
        prix_commerce = 0

        # calcul ressources produite par adversaire
        adversaire = self.adversaire()
        ressource_adversaire = {"bois": 0, "pierre": 0,
                                "argile": 0, "verre": 0, "papyrus": 0}
        for carte_ressource_adversaire in adversaire.cartes:
            if carte_ressource_adversaire.couleur != "jaune":
                for effet in carte_ressource_adversaire.effets:
                    ressource_adversaire_split = effet.split(" ")
                    if len(ressource_adversaire_split) == 3 and ressource_adversaire_split[0] == "ressource":
                        ressource = ressource_adversaire_split[1]
                        qte = int(ressource_adversaire_split[2])
                        ressource_adversaire[ressource] += qte

        # calcul ressources necessaire
        ressource_necessaire = {"bois": 0, "pierre": 0,
                                "argile": 0, "verre": 0, "papyrus": 0}
        for ressource in ressources_manquantes:
            ressource_split = ressource.split(" ")
            type = ressource_split[1]
            qte = int(ressource_split[2])
            ressource_necessaire[type] += qte

        for type, qte in ressource_necessaire.items():
            # si j'ai besoin d'une ressource
            if qte != 0:
                # si l'adversaire produit la ressource
                if ressource_adversaire[type] != 0:
                    prix_reduc = self.joueur_qui_joue.possede_carte_reduction(
                        type)
                    # si j'ai un reduc
                    if prix_reduc != 0:
                        # prix_commerce = (prix_reduc + qte produite par adv) * qte necessaire
                        prix_commerce += ((prix_reduc +
                                          ressource_adversaire[type]) * qte)

                    # si je n'ai pas de reduc
                    else:
                        # prix_commerce = (2 + quantite_qte produite par adv) * qte necessaire
                        prix_commerce += ((2 +
                                          ressource_adversaire[type]) * qte)

                else:  # si l'adversaire ne produit pas la ressource
                    prix_commerce += (2 * qte)

        return prix_commerce

    def piocher(self, carte_prenable: Carte):
        # construction carte
        if not self.joueur_qui_joue.possede_carte_chainage(carte_prenable):

            # la carte ne coute rien
            if carte_prenable.couts is None or len(carte_prenable.couts) == 0:
                return 0

            liste_ressource_necessaire = self.joueur_qui_joue.couts_manquants(
                carte_prenable)
            if len(liste_ressource_necessaire) != 0:
                liste_ressource_necessaire = self.joueur_qui_joue.cout_manquant_ressource_au_choix(
                    liste_ressource_necessaire)

            if carte_prenable.couleur == "bleu" and self.joueur_qui_joue.possede_jeton_scientifique("maconnerie"):
                liste_ressource_necessaire = self.effet_jeton_architecture_et_maconnerie(
                    liste_ressource_necessaire)

            monnaie = None
            # carte coute monnaie ?
            for cout in carte_prenable.couts:
                cout_split = cout.split(" ")
                if cout_split[0] == "monnaie":
                    monnaie = int(cout_split[1])

            # manque des monnaie
            if monnaie is not None and monnaie > self.joueur_qui_joue.monnaie:
                return -1

            # manque des ressources autre que monnaie
            prix = self.acheter_ressources(liste_ressource_necessaire)
            if monnaie is None:
                monnaie = 0
            if prix + monnaie > self.joueur_qui_joue.monnaie:
                return -1

            if self.adversaire().possede_jeton_scientifique("economie"):
                self.adversaire().monnaie += prix
            else:
                self.monnaie_banque += prix
            self.monnaie_banque += monnaie
            self.joueur_qui_joue.monnaie -= (prix + monnaie)

        else:
            # le joueur possede la carte chainage, construction gratuite
            # application effet jeton "urbanisme"
            if self.joueur_qui_joue.possede_jeton_scientifique("urbanisme"):
                self.joueur_qui_joue.monnaie += self.action_banque(4)

        return 0

    def defausser(self, carte_prenable: Carte):
        self.joueur_qui_joue.monnaie += self.action_banque(2)

        # gain de une piece par carte jaune
        for carte_joueur in self.joueur_qui_joue.cartes:
            if carte_joueur.couleur == "jaune":
                self.joueur_qui_joue.monnaie += self.action_banque(1)

        self.cartes_defaussees.append(carte_prenable)
        self.enlever_carte(carte_prenable)

    def effet_jeton_architecture_et_maconnerie(self, liste_ressource_necessaire: list):
        ressource = liste_ressource_necessaire[0]
        ressource_split = ressource.split(" ")
        qte = int(ressource_split[2])

        if qte == 1:
            ressource2 = liste_ressource_necessaire[1]
            ressource_split2 = ressource2.split(" ")
            qte2 = int(ressource_split2[2])

            if qte2 == 1:
                liste_ressource_necessaire.remove(ressource2)

            elif qte2 >= 2:
                liste_ressource_necessaire[2] = f"{ressource_split[0]} {ressource_split[1]} {qte2 - 1}"
                return liste_ressource_necessaire

            liste_ressource_necessaire.remove(ressource)
            return liste_ressource_necessaire

        if qte == 2:
            liste_ressource_necessaire.remove(ressource)
            return liste_ressource_necessaire

        liste_ressource_necessaire[0] = f"{ressource_split[0]} {ressource_split[1]} {qte - 2}"
        return liste_ressource_necessaire

    def construire_merveille(self, merveille_a_construire: Merveille):
        if merveille_a_construire.est_construite:
            return -2, None

        nbr_merveille_construite_j1 = self.joueur1.liste_merveilles_construite()
        nbr_merveille_construite_j2 = self.joueur2.liste_merveilles_construite()
        if len(nbr_merveille_construite_j1) + len(nbr_merveille_construite_j2) > 7:
            return -2, None

        # verification ressources joueur
        liste_ressource_necessaire = self.joueur_qui_joue.couts_manquants(
            merveille_a_construire)
        # print(liste_ressource_necessaire)
        joueur_possede_jeton_archi = any(
            jeton.nom == "architecture" for jeton in self.joueur_qui_joue.jetons_progres)
        if joueur_possede_jeton_archi:
            liste_ressource_necessaire = self.effet_jeton_architecture_et_maconnerie(
                liste_ressource_necessaire)

        # manque des ressouces
        if len(liste_ressource_necessaire) != 0:
            prix = self.acheter_ressources(liste_ressource_necessaire)
            if prix > self.joueur_qui_joue.monnaie:
                return -1, None

            self.joueur_qui_joue.monnaie -= prix
            self.monnaie_banque += prix

        for merveille in self.joueur_qui_joue.merveilles:
            if merveille == merveille_a_construire:
                merveille.est_construite = True

        return self.appliquer_effets_merveille(merveille_a_construire)

    def numero_jeton_militaire(self):
        """
        Renvoie le numero du jeton militaire dans le tableau en fonction de la postion
        du jeton conflit.

        :return: le numero du jeton militaire.
        """

        if self.position_jeton_conflit in [1, 2, 3]:
            return 0
        if self.position_jeton_conflit in [4, 5, 6]:
            return 1
        if self.position_jeton_conflit in [7, 8]:
            return 2
        if self.position_jeton_conflit in [10, 11]:
            return 3
        if self.position_jeton_conflit in [12, 13, 14]:
            return 4
        if self.position_jeton_conflit in [15, 16, 17]:
            return 5
        return -1

    def deplacer_pion_miltaire(self, nbr_deplacement: int):
        # On deplace le pion case par case
        for _ in range(nbr_deplacement):

            if self.joueur_qui_joue == self.joueur2:
                self.position_jeton_conflit -= 1
            else:
                self.position_jeton_conflit += 1

            # si le pion se situe au bout du plateau militaire, il y a une victoire militaire
            if self.position_jeton_conflit in [0, 18]:
                self.fin_de_partie()

            else:
                numero_jeton = self.numero_jeton_militaire()

                if numero_jeton != -1:
                    jeton = self.jetons_militaire[numero_jeton]

                    if not jeton.est_utilise:
                        self.adversaire().monnaie -= jeton.pieces
                        if self.adversaire().monnaie < 0:
                            self.fin_de_partie()
                        self.monnaie_banque += jeton.pieces

                        jeton.est_utilise = True

    def appliquer_effets_carte(self, carte: Carte):
        ret = 0
        for effet in carte.effets:

            effet_split = effet.split(" ")
            type = effet_split[0]

            if type == "ressource":
                self.joueur_qui_joue.ressources[effet_split[1]
                                                ] += int(effet_split[2])

            if type == "attaquer":
                nbr_bouclier = int(effet_split[1])
                if self.joueur_qui_joue.possede_jeton_scientifique("strategie"):
                    nbr_bouclier += 1

                self.deplacer_pion_miltaire(nbr_bouclier)

            if type == "symbole_scientifique":
                self.joueur_qui_joue.symb_scientifique[effet_split[1]] += 1
                self.joueur_qui_joue.compter_symb_scientifique()
                if self.joueur_qui_joue.nbr_symb_scientifique_diff == 6:
                    self.fin_de_partie()
                    return ret
                
                if self.joueur_qui_joue.symb_scientifique[effet_split[1]] == 2:
                    ret = 2

            if type == "monnaie":
                self.joueur_qui_joue.monnaie += self.action_banque(
                    int(effet_split[1]))

            if type == "monnaie_par_merveille":
                self.joueur_qui_joue.monnaie += self.action_banque(
                    int(effet_split[1]))

            if type == "monnaie_par_carte":
                for ma_carte in self.joueur_qui_joue.cartes:
                    if ma_carte.couleur == effet_split[1]:
                        self.joueur_qui_joue.monnaie += self.action_banque(
                            int(effet_split[2]))

            if carte.nom in ["guilde des armateurs", "guilde des commercants", "guilde des magistrats",
                             "guilde des tacticiens", "guilde des scientifiques"]:

                if carte.nom == "guilde des armateurs":
                    recherche = ["gris", "marron"]
                elif carte.nom == "guilde des commercants":
                    recherche = ["jaune"]
                elif carte.nom == "guilde des magistrats":
                    recherche = ["bleu"]
                elif carte.nom == "guilde des tacticiens":
                    recherche = ["rouge"]
                else:
                    recherche = ["vert"]

                nbr_carte_recherche_j1 = len(
                    [carte for carte in self.joueur1.cartes if carte.couleur in recherche])
                nbr_carte_recherche_j2 = len(
                    [carte for carte in self.joueur2.cartes if carte.couleur in recherche])

                if nbr_carte_recherche_j1 != nbr_carte_recherche_j2:
                    maxi = max(nbr_carte_recherche_j1, nbr_carte_recherche_j2)
                    joueur = self.joueur1 if maxi == nbr_carte_recherche_j1 else self.joueur2

                    if self.monnaie_banque >= maxi:
                        joueur.monnaie += maxi
                        self.monnaie_banque -= maxi

                    else:
                        print(
                            f"{Couleurs.FAIL} ERREUR : la banque n'a plus d'argent {Couleurs.FAIL}")
                        sys.exit(-2)
        return ret

    def appliquer_effets_merveille(self, merveille: Merveille):
        liste_effet = []
        for effet in merveille.effets:

            effet_split = effet.split(" ")
            type = effet_split[0]

            # effet commun avec certaines cartes
            if type in ["monnaie", "monnaie_par_carte"]:
                self.appliquer_effets_carte(merveille)

            if type == "attaquer":
                self.deplacer_pion_miltaire(int(effet_split[1]))

            if type == "adversaire_perd_monnaie":
                self.adversaire(
                ).monnaie -= self.action_banque(-int(effet_split[1]))

            if type == "defausse_carte_adversaire":
                couleur = effet_split[1]

                if couleur in ["gris", "marron"]:
                    adversaire = self.adversaire()
                    cartes = adversaire.possede_cartes_couleur(couleur)
                    if len(cartes) != 0:
                        while True:
                            carte = random.choice(cartes)
                            if carte.couleur == couleur:
                                adversaire.cartes.remove(carte)
                                self.cartes_defaussees.append(carte)
                                break
                        liste_effet.append((type, carte))

            if type == "jeton_progres_aleatoire":
                if len(self.jetons_progres_plateau) >= 2:

                    if len(self.jetons_progres_plateau) == 2:
                        jetons = random.sample(
                            self.jetons_progres_plateau, k=2)

                    else:
                        jetons = random.sample(
                            self.jetons_progres_plateau, k=3)

                    jeton = random.choice(jetons)
                    self.joueur_qui_joue.jetons_progres.append(jeton)
                    self.jetons_progres_plateau.remove(jeton)
                    liste_effet.append((type, jeton))

            if type == "construction_fausse_gratuite":
                if len(self.cartes_defaussees) != 0:
                    carte = random.choice(self.cartes_defaussees)
                    self.joueur_qui_joue.cartes.append(carte)
                    self.cartes_defaussees.remove(carte)
                    liste_effet.append((type, carte))

            if type == "rejouer" or self.joueur_qui_joue.possede_jeton_scientifique("theologie"):
                liste_effet.append("rejouer")

        return liste_effet

    def appliquer_effets_jeton(self, jeton: JetonProgres):
        if jeton.nom in ["agriculture", "urbanisme"]:
            self.joueur_qui_joue.monnaie += self.action_banque(6)

        elif jeton.nom == "loi":
            while True:
                list_symb = ["sphere_armillaire", "roue", "cadran_solaire", "pilon",
                             "compas_maconniques", "plume"]
                nom_jeton_random = random.choice(list_symb)

                if self.joueur_qui_joue.symb_scientifique[nom_jeton_random] != 2:
                    print(nom_jeton_random)
                    self.joueur_qui_joue.symb_scientifique[nom_jeton_random] += 1
                    if self.joueur_qui_joue.symb_scientifique[nom_jeton_random] == 2:
                        return 2
                    break
