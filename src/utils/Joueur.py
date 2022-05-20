"""
Fichier de la classe Joueur.
"""
from src.utils.Carte import Carte
from src.utils.Outils import mon_str_liste


class Joueur:
    """
    Classe representant un nom_joueur.
    """

    def __init__(self, nom):
        """
        Constructeur de la classe Joueur.

        :param nom: nom du nom_joueur.
        """
        self.nom = nom

        # Informations visible sur le plateau.
        self.cartes = []
        self.merveilles = []
        self.jetons_progres = []
        self.monnaie = 0

        #
        self.ressources = {
            "bois": 0,
            "pierre": 0,
            "argile": 0,
            "verre": 0,
            "papyrus": 0
        }
        self.points_victoire = 0
        self.symb_scientifique = {
            "sphere_armillaire": 0,
            "roue": 0,
            "cadran_solaire": 0,
            "pilon": 0,
            "compas_maconniques": 0,
            "plume": 0
        }

        self.nbr_symb_scientifique_diff = 0

    def __eq__(self, other):
        if isinstance(other, Joueur):
            return self.nom == other.nom \
                and self.cartes == other.cartes \
                and self.merveilles == other.merveilles \
                and self.jetons_progres == other.jetons_progres \
                and self.ressources == other.ressources \
                and self.monnaie == other.monnaie \
                and self.points_victoire == other.points_victoire \
                and self.symb_scientifique == other.symb_scientifique \
                and self.nbr_symb_scientifique_diff == other.nbr_symb_scientifique_diff

        return False

    def __str__(self):
        return f"nom : {self.nom}\n" \
            f"cartes : {mon_str_liste(self.cartes)}" \
            f"merveilles : {mon_str_liste(self.merveilles)}" \
            f"jetons_progres : {mon_str_liste(self.jetons_progres)}" \
            f"monnaie : {self.monnaie}\n" \
            f"points_victoire : {self.points_victoire}\n" \
            f"nbr_symb_scientifique_diff : {self.nbr_symb_scientifique_diff}\n"

    def constructeur_par_copie(self):
        joueur = Joueur(self.nom)

        joueur.cartes = []
        for carte in self.cartes:
            joueur.cartes.append(carte.constructeur_par_copie())

        joueur.merveilles = []
        for merveille in self.merveilles:
            joueur.merveilles.append(merveille.constructeur_par_copie())

        joueur.jetons_progres = []
        for jeton in self.jetons_progres:
            joueur.jetons_progres.append(jeton.constructeur_par_copie())

        joueur.ressources = {
            "bois": 0,
            "pierre": 0,
            "argile": 0,
            "verre": 0,
            "papyrus": 0
        }
        for ressource, qte in self.ressources.items():
            joueur.ressources[ressource] = qte

        joueur.monnaie = self.monnaie
        joueur.points_victoire = self.points_victoire

        joueur.symb_scientifique = {
            "sphere_armillaire": 0,
            "roue": 0,
            "cadran_solaire": 0,
            "pilon": 0,
            "compas_maconniques": 0,
            "plume": 0
        }
        for symb, qte in self.symb_scientifique.items():
            joueur.symb_scientifique[symb] = qte

        joueur.compter_symb_scientifique()

        return joueur

    def compter_symb_scientifique(self):
        self.nbr_symb_scientifique_diff = 0
        for _, qte in self.symb_scientifique.items():
            if qte != 0:
                self.nbr_symb_scientifique_diff += 1

    def couts_manquants(self, carte: Carte):
        if carte.couts is None or len(carte.couts) == 0:
            return []

        else:
            liste_couts_manquants = []

            for cout in carte.couts:
                cout_split = cout.split(" ")
                cout_type = cout_split[0]

                if cout_type == "ressource":
                    cout_type_ressource = cout_split[1]
                    cout_qte_ressource = int(cout_split[2])
                    qte_produite = self.ressources[cout_type_ressource]

                    if qte_produite < cout_qte_ressource:
                        difference_qte = cout_qte_ressource - qte_produite
                        ressource_manquante = f"ressource {cout_type_ressource} {difference_qte}"
                        liste_couts_manquants.append(ressource_manquante)

                elif cout_type == "monnaie":
                    qte_monnaie = int(cout_split[1])

                    if self.monnaie < qte_monnaie:
                        difference_qte = qte_monnaie - self.monnaie
                        ressource_manquante = f"monnaie {difference_qte}"
                        liste_couts_manquants.append(ressource_manquante)

            if len(liste_couts_manquants) == 0:
                return []

            if len(liste_couts_manquants) == 1:
                cout_manquant_split = liste_couts_manquants[0].split(" ")
                cout_manquant_type = cout_manquant_split[0]

                if cout_manquant_type == "monnaie":
                    return liste_couts_manquants

            return liste_couts_manquants

    def cout_manquant_ressource_au_choix(self, liste_couts_manquants: list):
        copy_liste_couts_manquants = liste_couts_manquants.copy()
        for ma_carte in self.cartes:

            for effet in ma_carte.effets:
                effet_split = effet.split(" ")
                effet_type = effet_split[0]

                if effet_type == "ressource_au_choix":
                    effet_type_ressource_1 = effet_split[1]
                    effet_type_ressource_2 = effet_split[2]
                    effet_type_ressource_3 = None

                    if len(effet_split) == 4:
                        effet_type_ressource_3 = effet_split[3]

                    for cout_manquant in copy_liste_couts_manquants:
                        cout_manquant_split = cout_manquant.split(" ")
                        cout_manquant_type = cout_manquant_split[0]

                        if cout_manquant_type == "ressource":
                            cout_manquant_ressource = cout_manquant_split[1]
                            cout_manquant_qte = int(cout_manquant_split[2])

                            if cout_manquant_ressource in [effet_type_ressource_1, effet_type_ressource_2, effet_type_ressource_3]:

                                if cout_manquant_qte == 1:
                                    liste_couts_manquants.remove(cout_manquant)
                                else:
                                    difference_qte = cout_manquant_qte - 1
                                    nouv_cout_manquant = f"ressource {cout_manquant_ressource} {difference_qte}"
                                    liste_couts_manquants[liste_couts_manquants.index(
                                        cout_manquant)] = nouv_cout_manquant

                                return liste_couts_manquants

        return liste_couts_manquants

    def possede_carte_chainage(self, carte: Carte):
        
        # si la carte ne possede pas de carte de chainage
        if carte.nom_carte_chainage is None:
            return False

        return any(carte_joueur.nom == carte.nom_carte_chainage for carte_joueur in self.cartes)

    def production_type_ressources(self, ressource: str):
        """
        Retourne la carte produisant la ressource.

        :param ressource: la ressource dont on veut la carte.
        :return: une carte si elle existe, None sinon.
        """

        ressource_split = ressource.split(" ")
        for carte in self.cartes:
            for effet in carte.effets:
                effet_split = effet.split(" ")

                # ressource type quantite
                if effet_split[0] == "ressource" and effet_split[1] == ressource_split[1]:
                    return carte
        return None

    def possede_carte_reduction(self, ressource: str):
        """
        Renvoie le prix de la reduction de la ressource.

        :param ressource: la ressource dont on cherche la reduction.
        :return: le prix reduit si le nom_joueur possede une carte reduction de la ressource, 0 sinon.
        """
        for carte in self.cartes:
            # print(f"carte : {carte.nom}", end=", ")
            for effet in carte.effets:
                # print(effet, end="")
                effet_split = effet.split(" ")

                # reduc_ressource type prixReduc
                if effet_split[0] == "reduc_ressource" and effet_split[1] == ressource:
                    # print(f" reduc : ", effet_split[2])
                    return int(effet_split[2])

        return 0

    def possede_cartes_couleur(self, couleur: str) -> list:
        """
        Renvoie une liste de carte de la même couleur que celle en parametre.

        :param couleur: la couleur a rechercher.
        :return: une liste de carte.
        """
        return [carte for carte in self.cartes if carte.couleur == couleur]

    def possede_jeton_scientifique(self, nom_jetons_progres: str):
        """
        Indique si le joueur possede ou non un jetons progres precis.

        :param nom_jetons_progres: le nom du jeton que l'on cherche.
        :return: vrai/ faux
        """

        return any(jeton.nom == nom_jetons_progres for jeton in self.jetons_progres)

    def compter_point_victoire(self) -> None:
        """
        Ajoute les points de victoires des differents objets (Carte, Jeton, CarteFille)
        """

        self.points_victoire = 0
        # compter points victoire avec les cartes
        for carte in self.cartes:
            for effet in carte.effets:

                # decoupe l effet
                effet_split = effet.split(" ")
                if effet_split[0] == "point_victoire":
                    self.points_victoire += int(effet_split[1])

        # compter points de victoire avec les merveilles
        for merveille in self.merveilles:
            for effet in merveille.effets:
                if merveille.est_construite:
                    # decoupe l effet
                    effet_split = effet.split(" ")
                    if effet_split[0] == "point_victoire":
                        self.points_victoire += int(effet_split[1])

        # compter points de victoire avec les jetons_progres
        for jeton in self.jetons_progres:
            for effet in jeton.effets:

                # decoupe l effet
                effet_split = effet.split(" ")

                # mathematiques
                if effet_split[0] == "point_victoire_par_jeton":
                    self.points_victoire += int(
                        effet_split[1]) * len(self.jetons_progres)

                # agriculture,
                elif effet_split[0] == "point_victoire":
                    self.points_victoire += int(effet_split[1])

                # philosophie
                elif effet_split[0] == "point_victoire_fin_partie":
                    self.points_victoire += int(effet_split[1])

    def trouver_repartition_monnaies(self):
        repartition = {6: 0, 3: 0, 1: 0}

        monnaie = self.monnaie

        pieces = [6, 3, 1]
        pos = 0

        while monnaie > 0:
            if monnaie >= pieces[pos]:
                monnaie -= pieces[pos]
                repartition[pieces[pos]] += 1
            else:
                pos += 1

        return repartition

    def liste_merveilles_non_construite(self):
        return [merveille for merveille in self.merveilles if not merveille.est_construite]

    def liste_merveilles_construite(self):
        return [merveille for merveille in self.merveilles if merveille.est_construite]
