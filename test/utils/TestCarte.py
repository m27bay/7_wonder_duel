"""
Fichier test pour la classe Carte.
"""

import unittest

from src.utils.Carte import Carte


class TestCarte(unittest.TestCase):
	def setUp(self) -> None:
		"""
		Initialisation d'une carte_a_enlever utilisee durant tous les tests
		"""
		self.carte = Carte("carte_a_enlever test", "images\\carte_test.png",
			["ressource bois 2"], ["monnaie 4"], None, "marron", 1)

	def testConstructeurCarte(self):
		str_carte = "nom : carte_a_enlever test, image : images\\carte_test.png, effets : " \
			"[\'ressource bois 2\'], couts : [\'monnaie 4\'], cout chainage : " \
			"None, couleur : marron, age : 1, face cachee : False"
		self.assertEqual(str_carte, str(self.carte))

	def testCacherCarte(self):
		self.carte.cacher()
		str_carte = "nom : carte_a_enlever test, image : images\\carte_test.png, effets : " \
			"[\'ressource bois 2\'], couts : [\'monnaie 4\'], cout chainage : " \
			"None, couleur : marron, age : 1, face cachee : True"
		self.assertEqual(str_carte, str(self.carte))

	def testDevoilerCarte(self):
		self.carte.devoiler()
		str_carte = "nom : carte_a_enlever test, image : images\\carte_test.png, effets : " \
			"[\'ressource bois 2\'], couts : [\'monnaie 4\'], cout chainage : " \
			"None, couleur : marron, age : 1, face cachee : False"
		self.assertEqual(str_carte, str(self.carte))

	def testCarteEgal(self):
		carte2 = Carte("carte_a_enlever test", "images\\carte_test.png",
			["ressource bois 2"], ["monnaie 4"], None, "marron", 1)
		self.assertEqual(carte2, self.carte)

		carte3 = Carte("carte_a_enlever test", "images\\carte_test.png",
			None, ["monnaie 4"], None, "marron", 1)
		self.assertEqual(carte3, self.carte)

		carte4 = Carte("carte_a_enlever test2", "images\\carte_test.png",
			["ressource bois 2"], ["monnaie 4"], None, "marron", 1)
		self.assertNotEqual(carte4, self.carte)


if __name__ == '__main__':
	unittest.main()
