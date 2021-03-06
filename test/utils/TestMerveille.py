"""
Fichier test de la classe CarteFille.
"""

import unittest

from src.utils.Merveille import Merveille


class TestMerveille(unittest.TestCase):
    def setUp(self) -> None:
        """
        Initialise une merveille utilisee durant tous les tests.
        """
        self.merveille = Merveille("merveille",
                                   ["defausse_carte_adversaire grise",
                                       "attaquer 1", "point_victoire 3"],
                                   ["ressource bois 2", "ressource verre 3"]
                                   )

    def test_constructeur_merveille(self):
        self.assertEqual("merveille", self.merveille.nom)
        self.assertEqual(
            ["defausse_carte_adversaire grise", "attaquer 1", "point_victoire 3"],
            self.merveille.effets
        )
        self.assertEqual(
            ["ressource bois 2", "ressource verre 3"],
            self.merveille.couts
        )

    def test_constructeur_par_copie_suppression_effet(self):
        copie = self.merveille.constructeur_par_copie()
        self.assertEqual(copie, self.merveille)

        copie.effets.remove("defausse_carte_adversaire grise")
        self.assertEqual(copie.effets, ["attaquer 1", "point_victoire 3"])
        self.assertEqual(
            self.merveille.effets,
            ["defausse_carte_adversaire grise", "attaquer 1", "point_victoire 3"]
        )
        self.assertNotEqual(copie, self.merveille)

    def test_constructeur_par_copie_construire_merveille(self):
        copie = self.merveille.constructeur_par_copie()
        copie.est_construite = True
        self.assertFalse(self.merveille.est_construite)


if __name__ == '__main__':
    unittest.main()
