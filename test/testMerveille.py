"""
Fichier test de la classe Merveille.
"""

import unittest

from src.main import Merveille


class TestMerveille(unittest.TestCase):
	def setUp(self) -> None:
		"""
		Initialise une merveille utilisee durant tous les tests.
		"""
		self.merveille = Merveille("merveille", "images\\merveille.png",
			["defausse_carte_adversaire grise", "attaquer 1", "point_victoire 3"],
			["ressource bois 2", "ressource verre 3"]
		)

	def testConstructeurMerveille(self):
		str_merveille = "nom : merveille, image : images\\merveille.png, effets : " \
			"[\'defausse_carte_adversaire grise\', \'attaquer 1\', \'point_victoire 3\']" \
			", couts : [\'ressource bois 2\', \'ressource verre 3\']" \
			", cout chainage : None, couleur : None, age : None, face cachée : False"
		self.assertEqual(str(self.merveille), str_merveille)

	def testCarteEgal(self):
		merveille2 = Merveille("merveille", "images\\carte_test.png", None, None)
		self.assertEqual(self.merveille, merveille2)

		merveille3 = Merveille("merveille", "images\\merveille.png",
			["defausse_carte_adversaire grise", "attaquer 1", "point_victoire 3"],
			["ressource bois 2", "ressource verre 3"]
		)
		self.assertEqual(self.merveille, merveille3)

		merveille4 = Merveille("merveille2", "images\\merveille.png",
			["defausse_carte_adversaire grise", "attaquer 1", "point_victoire 3"],
			["ressource bois 2", "ressource verre 3"]
		)
		self.assertNotEqual(self.merveille, merveille4)


if __name__ == '__main__':
	unittest.main()
	