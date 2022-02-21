import unittest

from src.main import Carte


class TestCarte(unittest.TestCase):
	def setUp(self) -> None:
		self.carte = Carte("carte test", "images\\carte_test.png",
		              ["ressource bois 2"], ["monnaie 4"], None, "marron", 1)

	def testConstructeurCarte(self):
		strCarte = "nom : carte test, image : images\\carte_test.png, effets : " \
		           "[\'ressource bois 2\'], couts : [\'monnaie 4\'], cout chainage : " \
		           "None, couleur : marron, age : 1, face cachée : False"
		self.assertEqual(strCarte, str(self.carte))

	def testCacherCarte(self):
		self.carte.cacher()
		strCarte = "nom : carte test, image : images\\carte_test.png, effets : " \
		           "[\'ressource bois 2\'], couts : [\'monnaie 4\'], cout chainage : " \
		           "None, couleur : marron, age : 1, face cachée : True"
		self.assertEqual(strCarte, str(self.carte))

	def testDevoilerCarte(self):
		self.carte.devoiler()
		strCarte = "nom : carte test, image : images\\carte_test.png, effets : " \
		           "[\'ressource bois 2\'], couts : [\'monnaie 4\'], cout chainage : " \
		           "None, couleur : marron, age : 1, face cachée : False"
		self.assertEqual(strCarte, str(self.carte))

	def testCarteEgal(self):
		carte2 = Carte("carte test", "images\\carte_test.png",
		                   ["ressource bois 2"], ["monnaie 4"], None, "marron", 1)
		self.assertEqual(carte2, self.carte)

		carte3 = Carte("carte test", "images\\carte_test.png",
		               None, ["monnaie 4"], None, "marron", 1)
		self.assertEqual(carte3, self.carte)

		carte4 = Carte("carte test2", "images\\carte_test.png",
		               ["ressource bois 2"], ["monnaie 4"], None, "marron", 1)
		self.assertNotEqual(carte4, self.carte)


if __name__ == '__main__':
	unittest.main()
