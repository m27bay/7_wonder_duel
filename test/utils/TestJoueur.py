"""
Fichier test de la classe Joueur.
"""

import unittest

from src.utils.Carte import Carte
from src.utils.Joueur import Joueur
from src.utils.CarteFille import CarteFille
from src.utils.JetonProgres import JetonProgres


class TestJoeur(unittest.TestCase):
	def setUp(self) -> None:
		"""
		Initialise un nom_joueur pour la suite des test.
		"""
		self.joueur = Joueur("pierre")

	def testConstructeur(self):
		self.assertEqual(self.joueur.nom, "pierre")

	def testRessourcesManquantes(self):
		self.joueur.cartes.append(Carte(None, None, ["ressource bois 2"], None, None, None, None))
		carte = Carte("carte_a_enlever", None, None, ["ressource bois 2"], None, None, None)
		self.assertEqual([], self.joueur.couts_manquants(carte))
		self.joueur.cartes.clear()

		self.joueur.cartes.append(Carte(None, None, ["ressource bois 2"], None, None, None, None))
		carte2 = Carte("carte2", None, None, ["ressource bois 1", "ressource verre 2"], None, None, None)
		self.assertEqual(["ressource verre 2"], self.joueur.couts_manquants(carte2))
		self.joueur.cartes.clear()

		self.joueur.cartes.append(Carte(None, None, ["ressource bois 1"], None, None, None, None))
		carte3 = Carte("carte3", None, None, ["ressource bois 2", "ressource verre 2"], None, None, None)
		self.assertEqual(["ressource bois 1", "ressource verre 2"], self.joueur.couts_manquants(carte3))
		self.joueur.cartes.clear()

	def testMonnaiesManquantes(self):
		self.joueur.monnaie = 4
		carte = Carte(None, None, None, ["monnaie 4"], None, None, None)
		self.assertEqual([], self.joueur.couts_manquants(carte))

		carte = Carte(None, None, None, ["monnaie 5"], None, None, None)
		self.assertEqual(["monnaie 1"], self.joueur.couts_manquants(carte))
		self.joueur.monnaie = 0

	def testPossedeCarteChainage(self):
		self.joueur.cartes.append(Carte("carte_a_enlever", None, None, None, None, None, None))

		self.assertTrue(self.joueur.possede_carte_chainage(Carte("carte2", None, None, None, "carte_a_enlever", None, None)))
		self.assertFalse(self.joueur.possede_carte_chainage(Carte("carte3", None, None, None, "erreur", None, None)))

		self.joueur.cartes.clear()

	def testProductionTypeRessources(self):
		self.joueur.cartes.append(Carte("carte_a_enlever", None, ["ressource bois 1"], None, None, None, None))

		self.assertEqual("carte_a_enlever", self.joueur.production_type_ressources("ressource bois 1").nom)
		self.assertEqual(None, self.joueur.production_type_ressources("ressource pierre 1"))

		self.joueur.cartes.clear()

	def testListeRessourcePrixReduit(self):
		douane = Carte("douanes", None, ["reduc_ressource papyrus 1", "reduc_ressource verre 1"], ["monnaie 4"],
			None, "jaune", age=2)
		self.joueur.cartes.append(douane)

		self.assertEqual(1, self.joueur.possede_carte_reduction("papyrus"))
		self.assertEqual(0, self.joueur.possede_carte_reduction("pierre"))

		self.joueur.cartes.clear()

	def testPossedeCartesCouleur(self):
		carte = Carte("chantier", None, ["ressource bois 1"], None, None, "marron", age=1)
		self.joueur.cartes.append(carte)
		liste_carte_coul = self.joueur.possede_cartes_couleur("marron")

		self.assertEqual([carte], liste_carte_coul)

		carte2 = Carte("exploitation", None, ["ressource bois 1"], ["monnaie 1"], None, "marron", age=1)
		self.joueur.cartes.append(carte2)
		liste_carte_coul = self.joueur.possede_cartes_couleur("marron")

		self.assertEqual([carte, carte2], liste_carte_coul)

		self.joueur.cartes.clear()

	def testPossedePasCartesCouleur(self):
		carte = Carte("chantier", None, ["ressource bois 1"], None, None, "marron", age=1)
		self.joueur.cartes.append(carte)
		liste_carte_coul = self.joueur.possede_cartes_couleur("grise")

		self.assertEqual([], liste_carte_coul)

		self.joueur.cartes.clear()

	def testCompterPointVictoireAvecLesCartes(self):
		self.joueur.cartes.append(Carte("theatre", None, ["point_victoire 3"], None, None, "blue", age=1))
		self.joueur.cartes.append(Carte("autel", None, ["point_victoire 3"], None, None, "blue", age=1))
		self.joueur.compter_point_victoire()
		self.assertEqual(6, self.joueur.points_victoire)
		self.joueur.cartes.clear()

	def testCompterPointVictoireAvecLesMerveilles(self):
		self.joueur.merveilles.append(
			CarteFille("circus maximus", None,
			           ["defausse_carte_adversaire grise", "attaquer 1", "point_victoire 3"],
			           ["ressource pierre 2", "ressource bois 1", "ressource verre 1"]
			           )
		)
		self.joueur.merveilles.append(
			CarteFille("colosse", None,
			           ["attaquer 2", "point_victoire 3"],
			           ["ressource argile 3", "ressource verre 1"]
			           )
		)
		self.joueur.compter_point_victoire()
		self.assertEqual(6, self.joueur.points_victoire)
		self.joueur.merveilles.clear()
		self.joueur.points_victoire = 0

	def testCompterPointVictoireAvecLesJetons(self):
		self.joueur.jetons.append(
			JetonProgres("agriculture", None, ["monnaie 6", "point_victoire 4"])
		)
		self.joueur.jetons.append(
			JetonProgres("mathematiques_custom", None, ["point_victoire 3"]),
		)
		self.joueur.compter_point_victoire()
		self.assertEqual(7, self.joueur.points_victoire)
		self.joueur.jetons.clear()
		self.joueur.points_victoire = 0

	def testCompterPointVictoireAvecLesJetons2(self):
		self.joueur.jetons.append(
			JetonProgres("agriculture", None, ["monnaie 6", "point_victoire 4"])
		)
		self.joueur.jetons.append(
			JetonProgres("mathematiques", None, ["point_victoire_par_jeton 3", "point_victoire 3"]),
		)
		self.joueur.compter_point_victoire()
		self.assertEqual(13, self.joueur.points_victoire)
		self.joueur.jetons.clear()
		self.joueur.points_victoire = 0
		
	def testSelectionMerveille(self):
		liste_merveilles = [
			CarteFille("merveille0", None, None, None),
			CarteFille("merveille1", None, None, None),
			CarteFille("merveille2", None, None, None),
			CarteFille("merveille3", None, None, None),
			CarteFille("merveille4", None, None, None)
		]
	
		# entree : merveille3, merveille1
		joueur = Joueur("joueur2")
		# copy de la liste car on supprime les merveilles une fois choisie.
		joueur.selection_merveille(2, liste_merveilles.copy())
		self.assertEqual([liste_merveilles[3], liste_merveilles[1]], joueur.merveilles)


if __name__ == '__main__':
	unittest.main()
