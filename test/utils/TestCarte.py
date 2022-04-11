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
		self.carte = Carte("carte",	["ressource bois 2"], ["monnaie 4"], None, "marron", 1)

	def test_constructeur_carte(self):
		self.assertEqual(self.carte.nom, "carte")
		self.assertEqual(self.carte.effets, ["ressource bois 2"])
		self.assertEqual(self.carte.couts, ["monnaie 4"])
		self.assertEqual(self.carte.nom_carte_chainage, None)
		self.assertEqual(self.carte.couleur, "marron")
		self.assertEqual(self.carte.age, 1)
		
	def test_affichage_carte(self):
		carte = Carte("arsenal", ["attaquer 3"], ["ressource argile 3", "ressource bois 2"], None, "rouge", age=3)
		str_carte = "nom : arsenal, effets : [\'attaquer 3\'], couts : [\'ressource argile 3\', \'ressource bois 2\']"\
			", cout chainage : None, couleur : rouge, age : 3, face cachee : False"
		
		self.assertEqual(str(carte), str_carte)
	
	def test_cacher_carte(self):
		carte = Carte("carte", ["ressource bois 2"], ["monnaie 4"], None, "marron", 1)
		carte.cacher()
		self.assertTrue(carte.est_face_cachee)
		
	def test_devoiler_carte(self):
		carte = Carte("carte", ["ressource bois 2"], ["monnaie 4"], None, "marron", 1)
		carte.devoiler()
		self.assertFalse(carte.est_face_cachee)

	def test_carte_egal(self):
		carte2 = Carte("carte2", ["ressource bois 2"],
			["monnaie 4"], None, "marron", 1)
		self.assertNotEqual(carte2, self.carte)
		
		carte3 = Carte("carte",	["ressource bois 2"], ["monnaie 4"], None, "marron", 1)
		self.assertEqual(carte3, self.carte)


if __name__ == '__main__':
	unittest.main()
