import unittest

from src.main import Carte, trouverElmentAvecNom, Merveille, Joueur, demanderElementDansUneListe, selectionMerveille, \
	differenceListeRessources


class TestFonction(unittest.TestCase):
	def setUp(self) -> None:
		self.listeCarte = [
			Carte("carte0", None, None, None, None, None, None),
			Carte("carte1", None, None, None, None, None, None),
			Carte("carte2", None, None, None, None, None, None),
			Carte("carte3", None, None, None, None, None, None),
			Carte("carte4", None, None, None, None, None, None)
		]

		self.listeMerveille = [
			Merveille("merveille0", None, None, None),
			Merveille("merveille1", None, None, None),
			Merveille("merveille2", None, None, None),
			Merveille("merveille3", None, None, None),
			Merveille("merveille4", None, None, None)
		]

	def testTrouverCarteAvecNom(self):
		self.assertEqual(self.listeCarte[4], trouverElmentAvecNom("carte4", self.listeCarte))
		self.assertEqual(None, trouverElmentAvecNom("erreur", self.listeCarte))

	def testTrouverMerveilleAvecNom(self):
		self.assertEqual(self.listeMerveille[2], trouverElmentAvecNom("merveille2", self.listeMerveille))
		self.assertEqual(None, trouverElmentAvecNom("erreur", self.listeMerveille))

	def testDemanderCarteDansUneListe(self):
		# entree : carte0
		carteDemandee = demanderElementDansUneListe(Joueur("joueur1"), "carte", self.listeCarte)
		self.assertEqual(self.listeCarte[0], carteDemandee)

	def testSelectionMerveille(self):
		# entree : merveille3, merveille1
		joueur = Joueur("joueur2")
		# copy de la liste car on supprime les merveilles une fois choisie.
		selectionMerveille(2, joueur, self.listeMerveille.copy())
		self.assertEqual([self.listeMerveille[3], self.listeMerveille[1]], joueur.merveilles)

	def testDifferenceListeRessources(self):
		listeRessource = ["ressource bois 2"]
		listeRessource2 = ["ressource bois 2"]
		self.assertEqual([], differenceListeRessources(listeRessource, listeRessource2))

		listeRessource.append("ressource pierre 2")
		self.assertEqual(["ressource pierre 2"], differenceListeRessources(listeRessource, listeRessource2))

		listeRessource = ["ressource pierre 2", "ressource bois 2"]
		listeRessource2 = ["ressource bois 2", "ressource pierre 1"]
		self.assertEqual(["ressource pierre 1"], differenceListeRessources(listeRessource, listeRessource2))


if __name__ == '__main__':
	unittest.main()
