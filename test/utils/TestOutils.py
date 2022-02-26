"""
Fichier test de fonction.
"""

import unittest

from src.utils.Carte import Carte
from src.utils.Merveille import Merveille

from src.utils.Outils import trouver_element_avec_nom
from src.utils.Outils import demander_element_dans_une_liste


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
		carte_demandee = demander_element_dans_une_liste("joueur1", "carte", self.liste_cartes)
		self.assertEqual(self.liste_cartes[0], carte_demandee)


if __name__ == '__main__':
	unittest.main()
