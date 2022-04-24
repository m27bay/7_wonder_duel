"""
Fichier test pour la classe Carte.
"""

import unittest

from src.utils.Carte import Carte
from src.utils.Merveille import Merveille
from src.utils.JetonMilitaire import JetonMilitaire
from src.utils.JetonProgres import JetonProgres


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
		
	def test_carte_egal(self):
		carte2 = Carte("carte2", ["ressource bois 2"], ["monnaie 4"], None, "marron", 1)
		self.assertNotEqual(carte2, self.carte)
		
		carte3 = Carte("carte", ["ressource bois 2"], ["monnaie 4"], None, "marron", 1)
		self.assertEqual(carte3, self.carte)
		
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

	def test_constructeur_par_copie(self):
		copie = self.carte.constructeur_par_copie()
		self.assertEqual(copie, self.carte)
		
		copie.effets.remove("ressource bois 2")
		self.assertEqual(self.carte.effets, ["ressource bois 2"])
		self.assertEqual(copie.effets, [])
		

class TestCarteFille(unittest.TestCase):
	def setUp(self) -> None:
		self.carte_fille = Merveille("pyramides",
					["point_victoire 9"],
					["ressource pierre 3", "ressource papyrus 1"]
				)
		
	def test_constructeur(self):
		self.assertEqual(self.carte_fille.nom, "pyramides")
		self.assertEqual(self.carte_fille.effets, ["point_victoire 9"],
					["ressource pierre 3", "ressource papyrus 1"])
		
	def test_constructeur_par_copie(self):
		copie = self.carte_fille.constructeur_par_copie()
		self.assertEqual(copie, self.carte_fille)
		
		
class TestJetonMilitaire(unittest.TestCase):
	def setUp(self) -> None:
		self.jeton_militaire = JetonMilitaire("5piecesJ1", 5, 10)

	def test_constructeur(self):
		self.assertEqual(self.jeton_militaire.nom, "5piecesJ1")
		self.assertEqual(self.jeton_militaire.pieces, 5)
		self.assertEqual(self.jeton_militaire.points_victoire, 10)
		
	def test_constructeur_par_copie(self):
		copie = self.jeton_militaire.constructeur_par_copie()
		self.assertEqual(copie, self.jeton_militaire)
		
		copie.points_victoire = 9
		self.assertEqual(copie.points_victoire, 9)
		self.assertEqual(self.jeton_militaire.points_victoire, 10)
		
		
class TestJetonProgres(unittest.TestCase):
	def setUp(self) -> None:
		self.jeton_progres = JetonProgres("agriculture", ["monnaie 6", "point_victoire 4"])


if __name__ == '__main__':
	unittest.main()
