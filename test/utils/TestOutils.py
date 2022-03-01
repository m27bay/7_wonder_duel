"""
Fichier test de fonction.
"""

import unittest

from src.utils.Carte import Carte
from src.utils.CarteFille import CarteFille

from src.utils.Outils import trouver_element_avec_nom
from src.utils.Outils import demander_element_dans_une_liste
from src.utils.Outils import trouver_ressource_avec_nom
from src.utils.Outils import demander_ressource_dans_une_liste


class TestOutils(unittest.TestCase):
	def setUp(self) -> None:
		"""
		Initialise deux listes utilisees pour la suite des tests.
		"""
		self.liste_cartes = [
			Carte("carte0", None, None, None, None, None, None),
			Carte("carte1", None, None, None, None, None, None),
			Carte("carte2", None, None, None, None, None, None),
			Carte("carte3", None, None, None, None, None, None),
			Carte("carte4", None, None, None, None, None, None)
		]

		self.liste_merveilles = [
			CarteFille("merveille0", None, None, None),
			CarteFille("merveille1", None, None, None),
			CarteFille("merveille2", None, None, None),
			CarteFille("merveille3", None, None, None),
			CarteFille("merveille4", None, None, None)
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

	def test_demander_carte_dans_une_liste(self):
		# entree : carte0
		
		carte_demandee = demander_element_dans_une_liste(
			"joueur1",
			"carte_a_enlever",
			self.liste_cartes
		)
		
		self.assertEqual(self.liste_cartes[0], carte_demandee)

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

	def test_demander_ressource_dans_une_liste(self):
		# entree : bois
		
		nom_ressource, ressource_choisie = demander_ressource_dans_une_liste(
			"joueur1",
			["ressource pierre 2", "ressource argile 1", "ressource bois 1"]
		)

		self.assertEqual("bois", nom_ressource)
		self.assertEqual("ressource bois 1", ressource_choisie)
		

if __name__ == '__main__':
	unittest.main()
