import math
import unittest

from src.utils.Carte import Carte
from src.utils.Joueur import Joueur
from src.utils.Plateau import Plateau, SYMBOLE_SCIENTIFIQUES
from src.utils.Stategie import fonction_evaluation, alpha_beta_avec_merveille
from src.utils.Stategie import minimax


class TestFonctionEvaluationAge1(unittest.TestCase):
    def setUp(self) -> None:
        self.plateau = Plateau(Joueur("j1"), Joueur("j2"))

    def test_fonction_evaluation_ordi_1_carte(self):
        self.plateau.joueur2.cartes.append(
            Carte("chantier", ["ressource bois 1"], None, None, "marron", age=1))

        evaluation = fonction_evaluation(self.plateau)
        self.assertEqual(20, evaluation)

    def test_fonction_evaluation_ordi_et_joueur_1_carte(self):
        self.plateau.joueur1.cartes.append(Carte("exploitation", ["ressource bois 1"],
                                                 ["monnaie 1"], None, "marron", age=1))
        self.plateau.joueur2.cartes.append(
            Carte("chantier", ["ressource bois 1"], None, None, "marron", age=1))

        evaluation = fonction_evaluation(self.plateau)
        self.assertEqual(4, evaluation)

        plateau2 = Plateau(Joueur("j1"), Joueur("j2"))

        plateau2.joueur1.cartes.append(Carte("armurerie", ["monnaie_par_carte rouge 1", "point_victoire 3"],
                                             ["ressource pierre 2", "ressource verre 1"], None, "jaune", age=3))
        plateau2.joueur2.cartes.append(Carte("haras", ["attaquer 1"], ["ressource argile 1", "ressource bois 1"],
                                             "ecuries", "rouge", age=2))

        evaluation = fonction_evaluation(plateau2)
        self.assertNotEqual(2, evaluation)
        self.assertEqual(-2, evaluation)

    def test_fonction_evaluation_ordi_et_joueur_2_cartes(self):
        self.plateau.joueur1.cartes.append(Carte("exploitation", ["ressource bois 1"],
                                                 ["monnaie 1"], None, "marron", age=1))
        self.plateau.joueur1.cartes.append(
            Carte("chantier", ["ressource bois 1"], None, None, "marron", age=1))
        self.plateau.joueur2.cartes.append(Carte("bassin argileux", ["ressource argile 1"],
                                                 None, None, "marron", age=1))
        self.plateau.joueur2.cartes.append(
            Carte("tour de garde", ["attaquer 1"], None, None, "rouge", age=1))

        evaluation = fonction_evaluation(self.plateau)
        self.assertEqual(-4, evaluation)


class TestFonctionEvaluationDurantPartie1(unittest.TestCase):
    def setUp(self) -> None:
        self.plateau = Plateau(Joueur("j1"), Joueur("j2"))
        self.plateau.preparation_plateau()

        self.plateau.cartes_plateau[4][0] = Carte("apothicaire",
                                                  [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[5]}", "point_victoire 1"], [
                                                      "ressource verre 1"], None,
                                                  "vert", age=1)
        self.plateau.cartes_plateau[4][2] = Carte("exploitation", ["ressource bois 1"], ["monnaie 1"], None, "marron",
                                                  age=1)
        self.plateau.cartes_plateau[4][4] = Carte("depot de bois", ["reduc_ressource bois 1"], ["monnaie 3"], None,
                                                  "jaune", age=1)
        self.plateau.cartes_plateau[4][6] = Carte("presse", ["ressource papyrus 1"], [
                                                  "monnaie 1"], None, "gris", age=1)
        self.plateau.cartes_plateau[4][8] = Carte("bassin argileux", ["ressource argile 1"], None, None, "marron",
                                                  age=1)
        self.plateau.cartes_plateau[4][10] = Carte("officine", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[2]}"],
                                                   ["monnaie 2"], None, "vert", age=1)

        self.plateau.cartes_plateau[3][1] = Carte(
            "chantier", ["ressource bois 1"], None, None, "marron", age=1)
        self.plateau.cartes_plateau[3][3] = Carte(
            "gisement", ["ressource pierre 1"], None, None, "marron", age=1)
        self.plateau.cartes_plateau[3][5] = Carte("mine", ["ressource pierre 1"], [
                                                  "monnaie 1"], None, "marron", age=1)
        self.plateau.cartes_plateau[3][7] = Carte("verrerie", ["ressource verre 1"], [
                                                  "monnaie 1"], None, "gris", age=1)
        self.plateau.cartes_plateau[3][9] = Carte(
            "tour de garde", ["attaquer 1"], None, None, "rouge", age=1)

        self.plateau.cartes_plateau[2][2] = Carte("depot de pierre", ["reduc_ressource pierre 1"], ["monnaie 3"], None,
                                                  "jaune", age=1)
        self.plateau.cartes_plateau[2][4] = Carte(
            "taverne", ["monnaie 4"], None, None, "jaune", age=1)
        self.plateau.cartes_plateau[2][6] = Carte("palissade", ["attaquer 1"], [
                                                  "monnaie 2"], None, "rouge", age=1)
        self.plateau.cartes_plateau[2][8] = Carte("depot d argile", ["reduc_ressource argile 1"], ["monnaie 3"], None,
                                                  "jaune", age=1)

        self.plateau.cartes_plateau[1][3] = Carte(
            "ecuries", ["attaquer 1"], ["ressource bois 1"], None, "rouge", age=1)
        self.plateau.cartes_plateau[1][5] = Carte("scriptorium", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[4]}"],
                                                  ["monnaie 2"], None, "vert", age=1)
        self.plateau.cartes_plateau[1][7] = Carte(
            "autel", ["point_victoire 3"], None, None, "bleu", age=1)

        self.plateau.cartes_plateau[0][4] = Carte("cavite", ["ressource argile 1"], ["monnaie 1"], None, "marron",
                                                  age=1)
        self.plateau.cartes_plateau[0][6] = Carte("bains", ["point_victoire 3"], ["ressource pierre 1"], None, "bleu",
                                                  age=1)

    def test_minimax_profondeur_1(self):
        self.plateau.joueur_qui_joue = self.plateau.joueur2
        nbr_noeuds = 0
        eval_minimax, carte_a_prendre, nbr_noeuds = minimax(
            self.plateau, 1, True, nbr_noeuds)

        self.assertEqual(20, eval_minimax)
        self.assertEqual("bassin argileux", carte_a_prendre.nom)
        self.assertEqual(7, nbr_noeuds)

    # TODO : mettre ?? jour
    # def test_minimax_profondeur_2(self):
    # 	self.plateau.joueur_qui_joue = self.plateau.joueur2
    # 	nbr_noeuds = 0
    # 	eval_minimax, carte_a_prendre, nbr_noeuds = minimax(self.plateau, 2, True, nbr_noeuds)
    #
    # 	self.assertEqual(20 - 16, eval_minimax)
    # 	self.assertEqual("bassin argileux", carte_a_prendre.nom)
    # 	self.assertEqual(37, nbr_noeuds)
    #
    # def test_alpha_beta_profondeur_2(self):
    # 	self.plateau.joueur_qui_joue = self.plateau.joueur2
    # 	nbr_noeuds = 0
    # 	eval_minimax, carte_a_prendre, nbr_noeuds = alpha_beta(self.plateau, 2, -math.inf, math.inf, True, nbr_noeuds)
    #
    # 	self.assertEqual(20 - 16, eval_minimax)
    # 	self.assertEqual("bassin argileux", carte_a_prendre.nom)
    # 	self.assertEqual(37, nbr_noeuds)

    def test_alpha_beta_avec_merveille_profondeur_2(self):
        self.plateau.joueur_qui_joue = self.plateau.joueur2

        nbr_noeuds_alpha_beta_merveille = 0
        evaluation_alpha_beta_merveille, carte, merveille, nbr_noeuds_alpha_beta_merveille = \
            alpha_beta_avec_merveille(self.plateau, 3, -math.inf, math.inf,
                                      True, nbr_noeuds_alpha_beta_merveille)

        print(
            f"carte : {carte}\neval : {evaluation_alpha_beta_merveille}\nmerveille : {merveille}")
        self.assertIsNotNone(merveille)
        self.assertEqual(merveille.nom, "via appia")


class TestFonctionEvaluationDurantPartie2(unittest.TestCase):
    def setUp(self) -> None:
        self.plateau = Plateau(Joueur("j1"), Joueur("j2"))
        self.plateau.preparation_plateau()

        self.plateau.cartes_plateau[4][0] = Carte("cavite", ["ressource argile 1"], [
                                                  "monnaie 1"], None, "marron", age=1)
        self.plateau.cartes_plateau[4][2] = Carte("scriptorium", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[4]}"],
                                                  ["monnaie 2"], None, "vert", age=1)
        self.plateau.cartes_plateau[4][4] = Carte("depot d argile", ["reduc_ressource argile 1"], ["monnaie 3"], None,
                                                  "jaune", age=1)
        self.plateau.cartes_plateau[4][6] = Carte(
            "taverne", ["monnaie 4"], None, None, "jaune", age=1)
        self.plateau.cartes_plateau[4][8] = Carte(
            "tour de garde", ["attaquer 1"], None, None, "rouge", age=1)
        self.plateau.cartes_plateau[4][10] = Carte(
            "gisement", ["ressource pierre 1"], None, None, "marron", age=1)

        self.plateau.cartes_plateau[3][1] = Carte(
            "chantier", ["ressource bois 1"], None, None, "marron", age=1)
        self.plateau.cartes_plateau[3][3] = Carte("officine", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[3]}"],
                                                  ["monnaie 2"], None, "vert", age=1)
        self.plateau.cartes_plateau[3][5] = Carte("mine", ["ressource pierre 1"], [
                                                  "monnaie 1"], None, "marron", age=1)
        self.plateau.cartes_plateau[3][7] = Carte("verrerie", ["ressource verre 1"], [
                                                  "monnaie 1"], None, "gris", age=1)
        self.plateau.cartes_plateau[3][9] = Carte(
            "bassin argileux", ["ressource argile 1"], None, None, "marron", age=1)
        self.plateau.cartes_plateau[2][2] = Carte("depot de pierre", ["reduc_ressource pierre 1"], ["monnaie 3"], None,
                                                  "jaune", age=1)
        self.plateau.cartes_plateau[2][4] = Carte("presse", ["ressource papyrus 1"], [
                                                  "monnaie 1"], None, "gris", age=1)
        self.plateau.cartes_plateau[2][6] = Carte("palissade", ["attaquer 1"], [
                                                  "monnaie 2"], None, "rouge", age=1)
        self.plateau.cartes_plateau[2][8] = Carte("depot de bois", ["reduc_ressource bois 1"], ["monnaie 3"], None, "jaune",
                                                  age=1)

        self.plateau.cartes_plateau[1][3] = Carte(
            "ecurie", ["attaquer 1"], ["ressource bois 1"], None, "rouge", age=1)
        self.plateau.cartes_plateau[1][5] = Carte("exploitation", ["ressource bois 1"], [
                                                  "monnaie 1"], None, "marron", age=1)
        self.plateau.cartes_plateau[1][7] = Carte(
            "autel", ["point_victoire 3"], None, None, "bleu", age=1)

        self.plateau.cartes_plateau[0][4] = Carte("apothicaire",
                                                  [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[1]}", "point_victoire 1"], [
                                                      "ressource verre 1"], None,
                                                  "vert", age=1)
        self.plateau.cartes_plateau[0][6] = Carte("bains", ["point_victoire 3"], [
                                                  "ressource pierre 1"], None, "bleu", age=1)

    def test_minimax_profondeur_2(self):
        self.plateau.joueur_qui_joue = self.plateau.joueur2
        nbr_noeuds = 0
        eval_minimax, carte_a_prendre, nbr_noeuds = minimax(
            self.plateau, 2, True, nbr_noeuds)

        self.assertEqual(1, eval_minimax)
        self.assertTrue(
            carte_a_prendre.nom in ["cavite", "tour de garde", "gisement"])
        self.assertEqual(37, nbr_noeuds)


class TestFonctionEvaluationDurantPartie3(unittest.TestCase):
    def setUp(self) -> None:
        self.plateau = Plateau(Joueur("j1"), Joueur("j2"))
        self.plateau.preparation_plateau()

        self.plateau.cartes_plateau[4][0] = Carte("cavite", ["ressource argile 1"], [
                                                  "monnaie 1"], None, "marron", age=1)
        self.plateau.cartes_plateau[4][2] = Carte("scriptorium", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[4]}"],
                                                  ["monnaie 2"], None, "vert", age=1)
        self.plateau.cartes_plateau[4][4] = Carte("depot d argile", ["reduc_ressource argile 1"], ["monnaie 3"], None,
                                                  "jaune", age=1)
        self.plateau.cartes_plateau[4][6] = Carte(
            "taverne", ["monnaie 4"], None, None, "jaune", age=1)
        self.plateau.cartes_plateau[4][8] = Carte(
            "tour de garde", ["attaquer 1"], None, None, "rouge", age=1)
        self.plateau.cartes_plateau[4][10] = Carte(
            "gisement", ["ressource pierre 1"], None, None, "marron", age=1)

        self.plateau.cartes_plateau[3][1] = Carte(
            "chantier", ["ressource bois 1"], None, None, "marron", age=1)
        self.plateau.cartes_plateau[3][3] = Carte("officine", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[3]}"],
                                                  ["monnaie 2"], None, "vert", age=1)
        self.plateau.cartes_plateau[3][5] = Carte("mine", ["ressource pierre 1"], [
                                                  "monnaie 1"], None, "marron", age=1)
        self.plateau.cartes_plateau[3][7] = Carte("verrerie", ["ressource verre 1"], [
                                                  "monnaie 1"], None, "gris", age=1)
        self.plateau.cartes_plateau[3][9] = Carte(
            "bassin argileux", ["ressource argile 1"], None, None, "marron", age=1)
        self.plateau.cartes_plateau[2][2] = Carte("depot de pierre", ["reduc_ressource pierre 1"], ["monnaie 3"], None,
                                                  "jaune", age=1)
        self.plateau.cartes_plateau[2][4] = Carte("presse", ["ressource papyrus 1"], [
                                                  "monnaie 1"], None, "gris", age=1)
        self.plateau.cartes_plateau[2][6] = Carte("palissade", ["attaquer 1"], [
                                                  "monnaie 2"], None, "rouge", age=1)
        self.plateau.cartes_plateau[2][8] = Carte("depot de bois", ["reduc_ressource bois 1"], ["monnaie 3"], None, "jaune",
                                                  age=1)

        self.plateau.cartes_plateau[1][3] = Carte(
            "ecurie", ["attaquer 1"], ["ressource bois 1"], None, "rouge", age=1)
        self.plateau.cartes_plateau[1][5] = Carte("exploitation", ["ressource bois 1"], [
                                                  "monnaie 1"], None, "marron", age=1)
        self.plateau.cartes_plateau[1][7] = Carte(
            "autel", ["point_victoire 3"], None, None, "bleu", age=1)

        self.plateau.cartes_plateau[0][4] = Carte("apothicaire",
                                                  [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[1]}", "point_victoire 1"], [
                                                      "ressource verre 1"], None,
                                                  "vert", age=1)
        self.plateau.cartes_plateau[0][6] = Carte("bains", ["point_victoire 3"], [
                                                  "ressource pierre 1"], None, "bleu", age=1)

    def test_minimax_profondeur_2(self):
        self.plateau.joueur_qui_joue = self.plateau.joueur2
        nbr_noeuds = 0
        eval_minimax, carte_a_prendre, nbr_noeuds = minimax(
            self.plateau, 2, True, nbr_noeuds)

        self.assertEqual(1, eval_minimax)
        self.assertTrue(carte_a_prendre.nom in [
                        "cavite", "tour de garde" "gisement"])
        self.assertEqual(37, nbr_noeuds)


if __name__ == '__main__':
    unittest.main()
