"""
Fichier test de la classe CarteFille.
"""

import unittest

from src.utils.CarteFille import CarteFille


class TestMerveille(unittest.TestCase):
	def setUp(self) -> None:
		"""
		Initialise une merveille utilisee durant tous les tests.
		"""
		self.merveille = CarteFille("merveille",
			["defausse_carte_adversaire grise", "attaquer 1", "point_victoire 3"],
			["ressource bois 2", "ressource verre 3"]
		)

	# def test_constructeur_merveille(self):
	# 	str_merveille = "nom : merveille, effets : " \
	# 		"[\'defausse_carte_adversaire grise\', \'attaquer 1\', \'point_victoire 3\']" \
	# 		", couts : [\'ressource bois 2\', \'ressource verre 3\']"
	# 	self.assertEqual(str(self.merveille), str_merveille)

	def test_carte_egal(self):
		merveille2 = CarteFille("merveille", None, None)
		self.assertEqual(self.merveille, merveille2)

		merveille3 = CarteFille("merveille",
			["defausse_carte_adversaire grise", "attaquer 1", "point_victoire 3"],
			["ressource bois 2", "ressource verre 3"]
		)
		self.assertEqual(self.merveille, merveille3)

		merveille4 = CarteFille("merveille2",
			["defausse_carte_adversaire grise", "attaquer 1", "point_victoire 3"],
			["ressource bois 2", "ressource verre 3"]
		)
		self.assertNotEqual(self.merveille, merveille4)


if __name__ == '__main__':
	unittest.main()
	