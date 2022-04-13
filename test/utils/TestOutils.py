"""
Fichier test de fonction.
"""

import unittest

from src.utils.Carte import Carte
from src.utils.CarteFille import CarteFille

from src.utils.Outils import trouver_element_avec_nom, mon_str_liste
from src.utils.Outils import trouver_ressource_avec_nom


class TestOutils(unittest.TestCase):
	def setUp(self) -> None:
		self.liste_cartes = [
			Carte("carte0", None, None, None, None, None),
			Carte("carte1", None, None, None, None, None),
			Carte("carte2", None, None, None, None, None),
			Carte("carte3", None, None, None, None, None),
			Carte("carte4", None, None, None, None, None)
		]

		self.liste_merveilles = [
			CarteFille("merveille0", None, None),
			CarteFille("merveille1", None, None),
			CarteFille("merveille2", None, None),
			CarteFille("merveille3", None, None),
			CarteFille("merveille4", None, None)
		]

	def test_trouver_carte_avec_nom(self):
		self.assertEqual(
			self.liste_cartes[4],
			trouver_element_avec_nom(
				"carte4",
				self.liste_cartes)
		)
		
		self.assertEqual(
			None,
			trouver_element_avec_nom(
				"erreur",
				self.liste_cartes)
		)

	def test_trouver_merveille_avec_nom(self):
		self.assertEqual(
			self.liste_merveilles[2],
			trouver_element_avec_nom(
				"merveille2",
				self.liste_merveilles)
		)
		
		self.assertEqual(
			None,
			trouver_element_avec_nom(
				"erreur",
				self.liste_merveilles)
		)

	def test_trouver_ressource_avec_nom(self):
		self.assertEqual(
			"ressource bois 1",
			trouver_ressource_avec_nom(
				"bois",
				["ressource pierre 2", "ressource argile 1", "ressource bois 1"]
			)
		)

		self.assertEqual(
			None,
			trouver_ressource_avec_nom(
				"erreur",
				["ressource pierre 2", "ressource argile 1", "ressource bois 1"]
			)
		)

	def test_mon_str_liste_avec_cartes(self):
		c = Carte("arsenal", ["attaquer 3"], ["ressource argile 3", "ressource bois 2"], None, "rouge", age=3)
		c2 = Carte("palace", ["point_victoire 7"],
			["ressource argile 1", "ressource pierre 1", "ressource bois 1", "ressource verre 2"], None, "bleu",
			age=3)
		c3 = Carte("depot de pierre", ["reduc_ressource pierre 1"], ["monnaie 3"], None, "jaune", age=1)
		
		liste = [c, c2, c3]
		str_liste = str(c) + "\n" + str(c2) + "\n" + str(c3) + "\n"
		
		self.assertEqual(str_liste, mon_str_liste(liste))
		
	def test_mon_str_liste_avec_cartes_et_0(self):
		c = Carte("arsenal", ["attaquer 3"], ["ressource argile 3", "ressource bois 2"], None, "rouge", age=3)
		c2 = Carte("palace", ["point_victoire 7"],
			["ressource argile 1", "ressource pierre 1", "ressource bois 1", "ressource verre 2"], None, "bleu", age=3)
		c3 = Carte("depot de pierre", ["reduc_ressource pierre 1"], ["monnaie 3"], None, "jaune", age=1)
		
		liste = [c, 0, c2, c3]
		str_liste = str(c) + "\n0\n" + str(c2) + "\n" + str(c3) + "\n"
		
		self.assertEqual(str_liste, mon_str_liste(liste))
		

if __name__ == '__main__':
	unittest.main()
