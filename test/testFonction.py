"""
Fichier test de fonction.
"""

import unittest

from src.main import Carte
from src.main import Joueur
from src.main import Merveille
from src.main import selection_merveille
from src.main import trouver_element_avec_nom
from src.main import demander_element_dans_une_liste


class TestFonction(unittest.TestCase):
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
			Merveille("merveille0", None, None, None),
			Merveille("merveille1", None, None, None),
			Merveille("merveille2", None, None, None),
			Merveille("merveille3", None, None, None),
			Merveille("merveille4", None, None, None)
		]

	def testTrouverCarteAvecNom(self):
		self.assertEqual(self.liste_cartes[4], trouver_element_avec_nom("carte4", self.liste_cartes))
		self.assertEqual(None, trouver_element_avec_nom("erreur", self.liste_cartes))

	def testTrouverMerveilleAvecNom(self):
		self.assertEqual(self.liste_merveilles[2], trouver_element_avec_nom("merveille2", self.liste_merveilles))
		self.assertEqual(None, trouver_element_avec_nom("erreur", self.liste_merveilles))

	def testDemanderCarteDansUneListe(self):
		# entree : carte0
		carte_demandee = demander_element_dans_une_liste(Joueur("joueur1"), "carte", self.liste_cartes)
		self.assertEqual(self.liste_cartes[0], carte_demandee)

	def testSelectionMerveille(self):
		# entree : merveille3, merveille1
		joueur = Joueur("joueur2")
		# copy de la liste car on supprime les merveilles une fois choisie.
		selection_merveille(2, joueur, self.liste_merveilles.copy())
		self.assertEqual([self.liste_merveilles[3], self.liste_merveilles[1]], joueur.merveilles)


if __name__ == '__main__':
	unittest.main()
