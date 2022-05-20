"""
Fichier de test pour la classe Jeu.
"""
import math
from tkinter.messagebox import NO
import unittest

from src.utils.Carte import Carte
from src.utils.CarteGuilde import CarteGuilde
from src.utils.JetonProgres import JetonProgres
from src.utils.Joueur import Joueur
from src.utils.Merveille import Merveille
from src.utils.Outils import mon_str_liste
from src.utils.Plateau import Plateau, SYMBOLE_SCIENTIFIQUES
from src.utils.Stategie import alpha_beta_avec_merveille


class TestConstructionPlateau(unittest.TestCase):
    def setUp(self) -> None:
        self.j1 = Joueur("Bruno")
        self.j2 = Joueur("Antoine")
        self.plateau = Plateau(self.j1, self.j2)

    def test_constructeur(self):
        self.assertEqual(self.plateau.joueur1, self.j1)
        self.assertEqual(self.plateau.joueur2, self.j2)
        self.assertEqual(self.plateau.joueur_qui_joue, None)
        self.assertEqual(self.plateau.choix_auto_merveilles, True)
        self.assertEqual(self.plateau.monnaie_banque, 86)
        self.assertEqual(self.plateau.age, 1)
        self.assertEqual(self.plateau.position_jeton_conflit, 9)

    def test_constructeur_vide(self):
        plateau = Plateau(None, None)

        self.assertIsNone(plateau.joueur1)
        self.assertIsNone(plateau.joueur2)
        self.assertIsNone(plateau.joueur_qui_joue)
        self.assertIsNone(plateau.choix_auto_merveilles)
        self.assertIsNone(plateau.monnaie_banque)
        self.assertIsNone(plateau.age)
        self.assertIsNone(plateau.position_jeton_conflit)

        self.assertEqual(plateau.jetons_militaire, [])
        self.assertEqual(plateau.cartes_age_I, [])
        self.assertEqual(plateau.cartes_age_II, [])
        self.assertEqual(plateau.cartes_age_III, [])
        self.assertEqual(plateau.cartes_guilde, [])
        self.assertEqual(plateau.cartes_plateau, [])
        self.assertEqual(plateau.cartes_defaussees, [])
        self.assertEqual(plateau.merveilles, [])
        self.assertEqual(plateau.jetons_progres, [])
        self.assertEqual(plateau.jetons_progres_plateau, [])

    def test_eq(self):
        j1 = Joueur("Bruno")
        j2 = Joueur("Antoine")
        plateau = Plateau(j1, j2)

        self.assertEqual(plateau, self.plateau)

    def test_constructeur_par_copie(self):
        copie = self.plateau.constructeur_par_copie()

        self.assertEqual(copie, self.plateau)

    def test_constructeur_par_copie_ajout(self):
        copie = self.plateau.constructeur_par_copie()
        copie.cartes_plateau.append(Carte("pretoire", ["attaquer 3"], [
                                    "monnaie 8"], None, "rouge", age=3))

        self.assertNotEqual(copie, self.plateau)

    def test_constructeur_par_copie_suppression(self):
        copie = self.plateau.constructeur_par_copie()
        copie.cartes_age_I.clear()

        self.assertNotEqual(copie, self.plateau)

    def test_constructeur_par_copie_symb_scientifique(self):
        copie = self.plateau.constructeur_par_copie()
        symb_scientifique = {
            "sphere_armillaire": 0,
            "roue": 0,
            "cadran_solaire": 0,
            "pilon": 1,
            "compas_maconniques": 0,
            "plume": 0
        }
        copie.joueur1.symb_scientifique = symb_scientifique

        symb_scientifique2 = {
            "sphere_armillaire": 0,
            "roue": 0,
            "cadran_solaire": 0,
            "pilon": 0,
            "compas_maconniques": 0,
            "plume": 0
        }

        self.assertEqual(symb_scientifique2,
                         self.plateau.joueur1.symb_scientifique)

    def test_constructeur_par_copie_suppression_carte_original_dans_copie_plateau(self):
        self.plateau.cartes_plateau = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        carte2 = Carte("pretoire", ["attaquer 3"], [
                       "monnaie 8"], None, "rouge", age=3)
        self.plateau.cartes_plateau[4][0] = carte2

        copie = self.plateau.constructeur_par_copie()

        # copie.enlever_carte(carte2)
        for num_ligne, ligne_carte in enumerate(copie.cartes_plateau):
            for num_colonne, carte in enumerate(ligne_carte):
                if carte == carte2:
                    copie.cartes_plateau[num_ligne][num_colonne] = 0

        carte_presente = False
        for num_ligne, ligne_carte in enumerate(self.plateau.cartes_plateau):
            for num_colonne, carte in enumerate(ligne_carte):
                if carte == carte2:
                    carte_presente = True

        self.assertTrue(carte_presente)
        self.assertFalse(copie.reste_des_cartes())

    def test_copie_merveilles(self):
        self.plateau.preparation_plateau()
        self.plateau.joueur_qui_joue = self.plateau.joueur2
        self.plateau.joueur2.ressources["pierre"] = 2
        self.plateau.joueur2.ressources["bois"] = 1
        self.plateau.joueur2.ressources["verre"] = 1

        copie = self.plateau.constructeur_par_copie()
        copie.construire_merveille(copie.joueur2.merveilles[0])

        self.assertFalse(self.plateau.merveilles[0].est_construite)

    def test_preparation_merveilles(self):
        self.plateau.preparation_plateau()

        self.assertEqual(self.plateau.joueur1.merveilles[0].nom, "pyramides")
        self.assertEqual(self.plateau.joueur1.merveilles[1].nom, "grand phare")
        self.assertEqual(
            self.plateau.joueur1.merveilles[2].nom, "temple d artemis")
        self.assertEqual(
            self.plateau.joueur1.merveilles[3].nom, "statue de zeus")

        self.assertEqual(
            self.plateau.joueur2.merveilles[0].nom, "circus maximus")
        self.assertEqual(self.plateau.joueur2.merveilles[1].nom, "piree")
        self.assertEqual(self.plateau.joueur2.merveilles[2].nom, "via appia")
        self.assertEqual(self.plateau.joueur2.merveilles[3].nom, "colosse")


class TestOutilsPlateau(unittest.TestCase):
    def setUp(self) -> None:
        self.j1 = Joueur("Bruno")
        self.j2 = Joueur("Antoine")
        self.plateau = Plateau(self.j1, self.j2)

    def test_obtenir_adversaire(self):
        self.plateau.joueur_qui_joue = self.plateau.joueur1
        self.assertEqual(self.plateau.adversaire(), self.plateau.joueur2)

    def test_enlever_une_carte(self):
        self.plateau.joueur_qui_joue = self.j1
        self.plateau.cartes_plateau = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        carte = Carte(
            "carriere", ["ressource pierre 2"], ["monnaie 2"], None, "marron", age=2
        )
        self.plateau.cartes_plateau[4][0] = carte
        self.plateau.enlever_carte(carte)

        self.assertEqual(0, self.plateau.cartes_plateau[4][0])

    def test_reste_des_cartes(self):
        self.plateau.cartes_plateau = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        self.assertTrue(self.plateau.reste_des_cartes())

        self.plateau.cartes_plateau = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        self.assertFalse(self.plateau.reste_des_cartes())

    def test_carte_prenable(self):
        self.plateau.joueur_qui_joue = self.j1
        self.plateau.preparation_plateau()

        self.assertTrue(self.plateau.cartes_prenable(4, 0))
        self.assertTrue(self.plateau.cartes_prenable(4, 10))
        self.assertFalse(self.plateau.cartes_prenable(3, 1))
        self.assertFalse(self.plateau.cartes_prenable(0, 4))

    def test_liste_cartes_prenable(self):
        plateau = Plateau(Joueur("j1"), Joueur("j2"))
        plateau.preparation_plateau()

        liste_carte_prenable = []

        for num_ligne, ligne_carte in enumerate(plateau.cartes_plateau):
            for _, carte in enumerate(ligne_carte):
                if carte != 0 and num_ligne == 4:
                    liste_carte_prenable.append(carte)

        self.assertEqual(liste_carte_prenable,
                         plateau.liste_cartes_prenables())

    def test_changement_age_cartes_plateau_vide(self):
        ret = self.plateau.changement_age()

        self.assertEqual(1, ret)
        self.assertEqual(2, self.plateau.age)

    def test_changement_age_cartes_plateau_rempli(self):
        self.plateau.preparation_plateau()
        ret = self.plateau.changement_age()

        self.assertEqual(0, ret)
        self.assertEqual(1, self.plateau.age)

    def test_changement_age_cartes_plateau_age_3(self):
        self.plateau.age = 3
        ret = self.plateau.changement_age()

        self.assertEqual(-1, ret)

    def test_fin_partie_militaire_joueur1(self):
        self.plateau.joueur1.monnaie = self.plateau.joueur2.monnaie = 1
        self.plateau.position_jeton_conflit = 18
        self.plateau.fin_de_partie()
        self.assertEqual(self.plateau.victoire, (self.j1.nom, "militaire"))

    def test_fin_partie_militaire_joueur2(self):
        self.plateau.joueur1.monnaie = self.plateau.joueur2.monnaie = 1
        self.plateau.position_jeton_conflit = 0
        self.plateau.fin_de_partie()
        self.assertEqual(self.plateau.victoire, (self.j2.nom, "militaire"))

    def test_fin_partie_scientifique_joueur1(self):
        self.plateau.joueur1.monnaie = self.plateau.joueur2.monnaie = 1
        self.j1.nbr_symb_scientifique_diff = 6
        self.plateau.fin_de_partie()
        self.assertEqual(self.plateau.victoire, (self.j1.nom, "scientifique"))

    def test_fin_partie_scientifique_joueur2(self):
        self.plateau.joueur1.monnaie = self.plateau.joueur2.monnaie = 1
        self.j2.nbr_symb_scientifique_diff = 6
        self.plateau.fin_de_partie()
        self.assertEqual(self.plateau.victoire, (self.j2.nom, "scientifique"))

    def test_fin_partie_points_victoire_joueur1(self):
        self.plateau.joueur1.monnaie = self.plateau.joueur2.monnaie = 1
        self.j1.cartes.append(
            Carte("atelier",
                  [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[3]}", "point_victoire 1"], [
                      "ressource papurys 1"],
                  None, "vert", age=1)
        )
        self.plateau.fin_de_partie()
        self.assertEqual(self.plateau.victoire,
                         (self.j1.nom, "points victoire"))

    def test_fin_partie_points_victoire_joueur2(self):
        self.plateau.joueur1.monnaie = self.plateau.joueur2.monnaie = 1
        self.j2.cartes.append(
            Carte("atelier",
                  [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[3]}", "point_victoire 1"], [
                      "ressource papurys 1"],
                  None, "vert", age=1)
        )
        self.plateau.fin_de_partie()
        self.assertEqual(self.plateau.victoire,
                         (self.j2.nom, "points victoire"))

    def test_fin_partie_points_victoire_egalite(self):
        self.plateau.joueur1.monnaie = self.plateau.joueur2.monnaie = 1
        self.j1.cartes.append(
            Carte("atelier",
                  [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[3]}", "point_victoire 1"], [
                      "ressource papurys 1"],
                  None, "vert", age=1)
        )
        self.j2.cartes.append(
            Carte("apothicaire",
                  [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[5]}",
                      "point_victoire 1"],
                  ["ressource verre 1"], None, "vert", age=1)
        )
        self.plateau.fin_de_partie()
        self.assertEqual(self.plateau.victoire, (None, "égalité"))

    def test_piocher_1(self):
        self.plateau.joueur_qui_joue = self.plateau.joueur1
        carte = Carte("bassin argileux", ["ressource argile 1"], None, None, "marron", age=1)
        self.plateau.piocher(carte)
        self.plateau.appliquer_effets_carte(carte)
        self.plateau.joueur_qui_joue.cartes.append(carte)
        
        carte = Carte("chantier", ["ressource bois 1"], None, None, "marron", age=1)
        self.plateau.piocher(carte)
        self.plateau.appliquer_effets_carte(carte)
        self.plateau.joueur_qui_joue.cartes.append(carte)
        
        carte = Carte("mine", ["ressource pierre 1"], None, None, "marron", age=1)
        self.plateau.piocher(carte)
        self.plateau.appliquer_effets_carte(carte)
        self.plateau.joueur_qui_joue.cartes.append(carte)

        carte = Carte("verrerie", ["ressource verre 1"], None, None, "gris", age=1)
        self.plateau.piocher(carte)
        self.plateau.appliquer_effets_carte(carte)
        self.plateau.joueur_qui_joue.cartes.append(carte)

        carte = Carte("soufflerie", ["ressource verre 1"], None, None, "gris", age=2)
        self.plateau.piocher(carte)
        self.plateau.appliquer_effets_carte(carte)
        self.plateau.joueur_qui_joue.cartes.append(carte)

        self.plateau.joueur_qui_joue = self.plateau.joueur2
        carte = Carte("depot d argile", ["reduc_ressource argile 1"], None, None, "jaune", age=1)
        self.plateau.piocher(carte)
        self.plateau.appliquer_effets_carte(carte)
        self.plateau.joueur_qui_joue.cartes.append(carte)
        self.plateau.joueur_qui_joue.monnaie = 7

        carte = Carte("place d armes", ["attaquer 2"], ["ressource argile 2", "ressource verre 1"], None, "rouge", age=2)
        liste_ressource_necessaire = self.plateau.joueur_qui_joue.couts_manquants(carte)
        self.assertEqual(["ressource argile 2", "ressource verre 1"], liste_ressource_necessaire)
        self.assertEqual(8, self.plateau.acheter_ressources(liste_ressource_necessaire))
        
        ret = self.plateau.piocher(carte)
        self.assertEqual(-1, ret)
        
    def test_piocher_2(self):
        self.plateau.joueur_qui_joue = self.plateau.joueur1
        carte = Carte("bassin argileux", ["ressource argile 1"], None, None, "marron", age=1)
        self.plateau.piocher(carte)
        self.plateau.appliquer_effets_carte(carte)
        self.plateau.joueur_qui_joue.cartes.append(carte)

        carte = Carte("cavite", ["ressource argile 1"], None, None, "marron", age=1)
        self.plateau.piocher(carte)
        self.plateau.appliquer_effets_carte(carte)
        self.plateau.joueur_qui_joue.cartes.append(carte)

        self.plateau.joueur_qui_joue = self.plateau.joueur2
        self.plateau.joueur_qui_joue.monnaie = 6
        carte = Carte("forum", ["ressource_au_choix verre papyrus"], ["monnaie 3", "ressource argile 1"],
                      None, "jaune", age=2)
        
        ret = self.plateau.piocher(carte)
        self.assertEqual(-1, ret)
        

class TestEffetsCartesGuide(unittest.TestCase):
    def setUp(self) -> None:
        self.j1 = Joueur("Bruno")
        self.j2 = Joueur("Antoine")
        self.plateau = Plateau(self.j1, self.j2)

    def test_fin_partie_j1_possede_armateurs_j1_gagne(self):
        self.plateau.preparation_plateau()

        carte = Carte("sechoir", ["ressource papyrus 1"],
                      None, None, "gris", age=2)
        self.plateau.piocher(carte)
        self.plateau.appliquer_effets_carte(carte)
        self.plateau.joueur_qui_joue.cartes.append(carte)

        carte = Carte("carriere", ["ressource pierre 2"], [
                      "monnaie 2"], None, "marron", age=2)
        self.plateau.piocher(carte)
        self.plateau.appliquer_effets_carte(carte)
        self.plateau.joueur_qui_joue.monnaie += 2
        self.plateau.joueur_qui_joue.cartes.append(carte)

        self.j1.ressources["argile"] = 1
        self.j1.ressources["verre"] = 1

        carte = CarteGuilde("guilde des armateurs",
                            ["effet_guild_armateurs 1"],
                            ["ressource argile 1", "ressource pierre 1",
                                "ressource verre 1", "ressource papyrus 1"]
                            )
        self.plateau.piocher(carte)
        self.plateau.appliquer_effets_carte(carte)
        self.plateau.joueur_qui_joue.cartes.append(carte)

        self.plateau.joueur_qui_joue = self.plateau.joueur2
        carte = Carte(
            "soufflerie", ["ressource verre 1"], None, None, "gris", age=2)
        self.plateau.piocher(carte)
        self.plateau.appliquer_effets_carte(carte)
        self.plateau.joueur_qui_joue.cartes.append(carte)

        self.plateau.fin_de_partie()

        self.assertEqual(9, self.plateau.joueur1.monnaie)
        # 2 points pour les cartes, 3 points pour les pièces (3 paquets de 3)
        self.assertEqual(2+3, self.j1.points_victoire)
        self.assertEqual((self.j1.nom, "points victoire"),
                         self.plateau.victoire)

    def test_fin_partie_j1_possede_usuriers_j1_gagne(self):
        self.plateau.preparation_plateau()
        self.j1.monnaie = 10
        self.j2.cartes.append(CarteGuilde("guilde des usuriers",
                                          ["effet_guild_usuriers 1"],
                                          ["ressource pierre 2", "ressource bois 2"])
                              )
        self.plateau.fin_de_partie()

        # calcul fin de partie = j1 a 10 pièces donc 3 lot de 3 donc 3 points victoire
        # plus effet usuriers qui donne 3 pièces par lot de 3 donc 6 points victoire
        self.assertEqual(6, self.j1.points_victoire)
        self.assertEqual(2, self.j2.points_victoire)
        self.assertEqual((self.j1.nom, "points victoire"),
                         self.plateau.victoire)


class TestEffetsMerveillesGuide(unittest.TestCase):
    def setUp(self) -> None:
        self.j1 = Joueur("Bruno")
        self.j2 = Joueur("Antoine")
        self.plateau = Plateau(self.j1, self.j2)

    def test_construction_merveille_deja_constuite(self):
        self.plateau.preparation_plateau()
        self.plateau.joueur1.merveilles[0].est_construite = True
        ret = self.plateau.construire_merveille(
            self.plateau.joueur1.merveilles[0])
        self.assertEqual((-2, None), ret)

    def test_construction_merveille_monnaie_manquante(self):
        self.plateau.preparation_plateau()
        self.plateau.joueur1.monnaie = 0
        ret = self.plateau.construire_merveille(
            Merveille("via appia", None, ["monnaie 2"]))
        self.assertEqual((-1, None), ret)

    def test_construction_merveille_prix_achat_trop_eleve(self):
        self.plateau.preparation_plateau()
        self.plateau.joueur1.monnaie = 1
        ret = self.plateau.construire_merveille(
            Merveille("via appia", None, ["ressource pierre 1"]))
        self.assertEqual((-1, None), ret)

    def test_construction_merveille(self):
        self.plateau.preparation_plateau()
        self.plateau.joueur1.ressources["pierre"] = 3
        self.plateau.joueur1.ressources["papyrus"] = 1
        # merveilles[0] c'est pyramides
        self.plateau.construire_merveille(self.plateau.joueur1.merveilles[0])
        self.assertTrue(self.plateau.joueur1.merveilles[0].est_construite)

    def test_effets_circus_maximus(self):
        self.plateau.preparation_plateau()
        self.plateau.joueur_qui_joue = self.plateau.joueur2
        self.plateau.joueur2.ressources["pierre"] = 2
        self.plateau.joueur2.ressources["bois"] = 1
        self.plateau.joueur2.ressources["verre"] = 1

        self.plateau.joueur1.cartes.append(
            Carte("soufflerie", ["ressource verre 1"], None, None, "gris", age=2))
        self.plateau.joueur1.cartes.append(
            Carte("sechoir", ["ressource papyrus 1"], None, None, "gris", age=2))

        self.plateau.construire_merveille(self.plateau.joueur2.merveilles[0])
        self.plateau.joueur2.compter_point_victoire()

        self.assertEqual(1, len(self.plateau.joueur1.cartes))
        self.assertEqual(8, self.plateau.position_jeton_conflit)
        self.assertEqual(3, self.plateau.joueur2.points_victoire)

    def test_effets_jardin_suspendus(self):
        self.plateau.preparation_plateau()
        self.plateau.joueur1.merveilles[0] = Merveille("jardin suspendus",
                                                       ["monnaie 6", "rejouer",
                                                           "point_victoire 3"],
                                                       ["ressource bois 2 ", "ressource verre 1",
                                                           "ressource papyrus 1"]
                                                       )
        self.plateau.joueur1.ressources["bois"] = 2
        self.plateau.joueur1.ressources["verre"] = 1
        self.plateau.joueur1.ressources["papyrus"] = 1

        self.plateau.construire_merveille(self.plateau.joueur1.merveilles[0])
        self.plateau.joueur1.compter_point_victoire()

        self.assertEqual(13, self.plateau.joueur1.monnaie)
        self.assertEqual(3, self.plateau.joueur1.points_victoire)


class TestAcheterRessources(unittest.TestCase):
    def setUp(self) -> None:
        self.j1 = Joueur("Bruno")
        self.j2 = Joueur("Antoine")
        self.plateau = Plateau(self.j1, self.j2)

    def test_acheter_ressource_non_produite_par_adversaire(self):
        self.plateau.joueur_qui_joue = self.j1
        prix = self.plateau.acheter_ressources(["ressource pierre 1"])
        self.assertEqual(2, prix)

    def test_acheter_ressource_produite_par_adversaire(self):
        # exemple du manuel
        # https://cdn.1j1ju.com/medias/bd/ad/a7-7-wonders-duel-regles.pdf
        # page 9

        self.j1.monnaie = self.j2.monnaie = 10
        self.plateau.joueur_qui_joue = self.j2

        self.j1.cartes.append(Carte("carriere", ["ressource pierre 2"], [
                              "monnaie 2"], None, "marron", age=2))
        prix = self.plateau.acheter_ressources(["ressource pierre 1"])
        # j2 veut acheter une pierre, mais j1 en produit deux, [ 2 + (quantite_pierre_j1) ] * quantite_pierre_acheté
        self.assertEqual(4, prix)

    def test_acheter_ressource_produite_par_adversaire_2(self):
        # exemple du manuel

        self.j1.monnaie = self.j2.monnaie = 10
        self.plateau.joueur_qui_joue = self.j2

        self.j1.cartes.append(
            Carte("bassin argileux", ["ressource argile 1"], None, None, "marron", age=1))
        prix = self.plateau.acheter_ressources(
            ["ressource argile 1", "ressource papyrus 1"])

        self.assertEqual(5, prix)

    def test_acheter_ressource_produite_par_adversaire_3(self):
        # exemple du manuel

        self.j1.monnaie = self.j2.monnaie = 12
        self.plateau.joueur_qui_joue = self.j2

        self.j1.cartes.append(
            Carte("carte custom", ["ressource pierre 2"], None, None, None, None))
        prix = self.plateau.acheter_ressources(["ressource pierre 3"])

        self.assertEqual(12, prix)

    def test_acheter_ressource_produite_par_adversaire_avec_reduction(self):
        self.j1.monnaie = self.j2.monnaie = 10
        self.plateau.joueur_qui_joue = self.j2

        self.j1.cartes.append(Carte("carriere", ["ressource pierre 2"], [
                              "monnaie 2"], None, "marron", age=2))
        self.j2.cartes.append(
            Carte("depot de pierre", ["reduc_ressource pierre 1"], [
                  "monnaie 3"], None, "jaune", age=1)
        )
        prix = self.plateau.acheter_ressources(["ressource pierre 1"])

        self.assertEqual(3, prix)


class TestAttaquerJoueur1(unittest.TestCase):
    def setUp(self) -> None:
        self.j1 = Joueur("j1")
        self.j2 = Joueur("j2")
        self.plateau = Plateau(self.j1, self.j2)
        self.plateau.preparation_plateau()
        self.plateau.joueur_qui_joue = self.j1

    def test_attaque1_position_jeton_militaire_neutre(self):
        self.plateau.deplacer_pion_miltaire(1)

        # position_neutre (=9) + deplacement (=1) deplacement position car c'est j1 qui attaque
        # = 9 + 1
        # = 10
        self.assertEqual(10, self.plateau.position_jeton_conflit)

        # points_victoire_depart + points_victoire_premier_jeton (=2)
        # = 0 + 2
        # = 2
        self.assertEqual(2, self.j1.points_victoire)

        # monnaie_depart - monnaie_premier_jeton (=0)
        # = 7 - 0
        # = 7
        self.assertEqual(7, self.j2.monnaie)
        self.assertTrue(self.plateau.jetons_militaire[3].est_utilise)

    def test_attaque3_position_jeton_militaire_neutre(self):
        self.plateau.deplacer_pion_miltaire(3)

        # position_neutre (=9) + deplacement (=3) deplacement position car c'est j1 qui attaque
        # = 9 + 3
        # = 12
        self.assertEqual(12, self.plateau.position_jeton_conflit)

        # points_victoire_depart + points_victoire_premier_jeton (=2) + points_victoire_deuxieme_jeton (=5)
        # = 0 + 2 + 5
        # = 7
        self.assertEqual(7, self.j1.points_victoire)

        # monnaie_depart - monnaie_premier_jeton (=0) - monnaie_deuxieme_jeton (=2)
        # = 7 - 0 - 2
        # = 5
        self.assertEqual(5, self.j2.monnaie)
        self.assertTrue(self.plateau.jetons_militaire[3].est_utilise)
        self.assertTrue(self.plateau.jetons_militaire[4].est_utilise)

    def test_appliquer_effets_carte_attaquer1_sans_bonus_jeton_strategie(self):
        carte = Carte("tour de garde", [
                      "attaquer 1"], None, None, "rouge", age=1)

        self.plateau.appliquer_effets_carte(carte)

        self.assertEqual(10, self.plateau.position_jeton_conflit)
        self.assertEqual(2, self.plateau.joueur1.points_victoire)
        self.assertEqual(7, self.plateau.joueur2.monnaie)
        self.assertTrue(self.plateau.jetons_militaire[3].est_utilise)

    def test_appliquer_effets_carte_attaquer1_avec_bonus_jeton_strategie(self):
        carte = Carte("tour de garde", [
                      "attaquer 1"], None, None, "rouge", age=1)
        self.plateau.joueur1.jetons_progres.append(
            JetonProgres("strategie", ["bonus_attaque"]))

        self.plateau.appliquer_effets_carte(carte)

        self.assertEqual(11, self.plateau.position_jeton_conflit)
        self.assertEqual(2, self.plateau.joueur1.points_victoire)
        self.assertEqual(7, self.plateau.joueur2.monnaie)
        self.assertTrue(self.plateau.jetons_militaire[3].est_utilise)

    def test_joueur1_appliquer_effets_carte_attaquer2_avec_bonus_jeton_strategie(self):
        carte = Carte("muraille", ["attaquer 2"], [
                      "ressource pierre 2"], None, "rouge", age=2)
        self.plateau.joueur1.jetons_progres.append(
            JetonProgres("strategie", ["bonus_attaque"]))

        self.plateau.appliquer_effets_carte(carte)

        self.assertEqual(12, self.plateau.position_jeton_conflit)
        self.assertEqual(7, self.plateau.joueur1.points_victoire)
        self.assertEqual(5, self.plateau.joueur2.monnaie)
        self.assertTrue(self.plateau.jetons_militaire[3].est_utilise)
        self.assertTrue(self.plateau.jetons_militaire[4].est_utilise)


class TestAttaquerJoueur2(unittest.TestCase):
    def setUp(self) -> None:
        self.j1 = Joueur("j1")
        self.j2 = Joueur("j2")
        self.plateau = Plateau(self.j1, self.j2)
        self.plateau.preparation_plateau()
        self.plateau.joueur_qui_joue = self.j2

    def test_attaque1_position_jeton_militaire_neutre(self):
        self.plateau.deplacer_pion_miltaire(1)

        # position_neutre (=9) + deplacement (=1) deplacement negatif car c'est j2 qui attaque
        # = 9 - 1
        # = 8
        self.assertEqual(8, self.plateau.position_jeton_conflit)

        # raisonnement identique qu'au dessus
        self.assertEqual(2, self.j2.points_victoire)
        self.assertEqual(7, self.j1.monnaie)
        self.assertTrue(self.plateau.jetons_militaire[2].est_utilise)

    def test_attaque3_position_jeton_militaire_neutre(self):
        self.plateau.deplacer_pion_miltaire(3)

        # position_neutre (=9) + deplacement (=3) deplacement negatif car c'est j2 qui attaque
        # = 9 - 3
        # = 6
        self.assertEqual(6, self.plateau.position_jeton_conflit)

        # raisonnement identique qu'au dessus
        self.assertEqual(7, self.j2.points_victoire)
        self.assertEqual(5, self.j1.monnaie)
        self.assertTrue(self.plateau.jetons_militaire[2].est_utilise)
        self.assertTrue(self.plateau.jetons_militaire[1].est_utilise)

    def test_appliquer_effets_carte_attaquer1_sans_bonus_jeton_strategie(self):
        carte = Carte("tour de garde", [
                      "attaquer 1"], None, None, "rouge", age=1)

        self.plateau.appliquer_effets_carte(carte)

        self.assertEqual(8, self.plateau.position_jeton_conflit)
        self.assertEqual(2, self.plateau.joueur2.points_victoire)
        self.assertEqual(7, self.plateau.joueur1.monnaie)
        self.assertTrue(self.plateau.jetons_militaire[2].est_utilise)

    def test_appliquer_effets_carte_attaquer1_avec_bonus_jeton_strategie(self):
        carte = Carte("tour de garde", [
                      "attaquer 1"], None, None, "rouge", age=1)
        self.plateau.joueur2.jetons_progres.append(
            JetonProgres("strategie", ["bonus_attaque"]))

        self.plateau.appliquer_effets_carte(carte)

        self.assertEqual(7, self.plateau.position_jeton_conflit)
        self.assertEqual(2, self.plateau.joueur2.points_victoire)
        self.assertEqual(7, self.plateau.joueur1.monnaie)
        self.assertTrue(self.plateau.jetons_militaire[2].est_utilise)

    def test_appliquer_effets_carte_attaquer2_avec_bonus_jeton_strategie(self):
        carte = Carte("muraille", ["attaquer 2"], [
                      "ressource pierre 2"], None, "rouge", age=2)
        self.plateau.joueur2.jetons_progres.append(
            JetonProgres("strategie", ["bonus_attaque"]))

        self.plateau.appliquer_effets_carte(carte)

        self.assertEqual(6, self.plateau.position_jeton_conflit)
        self.assertEqual(7, self.plateau.joueur2.points_victoire)
        self.assertEqual(5, self.plateau.joueur1.monnaie)
        self.assertTrue(self.plateau.jetons_militaire[2].est_utilise)
        self.assertTrue(self.plateau.jetons_militaire[1].est_utilise)


if __name__ == '__main__':
    unittest.main()
