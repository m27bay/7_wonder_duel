import unittest

from src.main import Joueur, Carte


class TestJoeur(unittest.TestCase):
	def setUp(self) -> None:
		self.joueur = Joueur("pierre")

	def testConstructeur(self):
		self.assertEqual(self.joueur.nom, "pierre")

	def testRessourcesManquantes(self):
		self.joueur.cartes.append(Carte(None, None, ["ressource bois 2"], None, None, None, None))
		carte = Carte(None, None, None, ["ressource bois 2"], None, None, None)
		self.assertEqual([], self.joueur.coutsManquant(carte))
		self.joueur.cartes.clear()

		self.joueur.cartes.append(Carte(None, None, ["ressource bois 2"], None, None, None, None))
		carte = Carte(None, None, None, ["ressource bois 1", "ressource verre 2"], None, None, None)
		self.assertEqual(["ressource verre 2"], self.joueur.coutsManquant(carte))
		self.joueur.cartes.clear()

		self.joueur.cartes.append(Carte(None, None, ["ressource bois 1"], None, None, None, None))
		carte = Carte(None, None, None, ["ressource bois 2", "ressource verre 2"], None, None, None)
		self.assertEqual(["ressource bois 1", "ressource verre 2"], self.joueur.coutsManquant(carte))
		self.joueur.cartes.clear()

	def testMonnaiesManquantes(self):
		self.joueur.monnaie = 4
		carte = Carte(None, None, None, ["monnaie 4"], None, None, None)
		self.assertEqual([], self.joueur.coutsManquant(carte))

		carte = Carte(None, None, None, ["monnaie 5"], None, None, None)
		self.assertEqual(["monnaie 1"], self.joueur.coutsManquant(carte))
		self.joueur.monnaie = 0

	def testPossedeCarteChainage(self):
		self.joueur.cartes.append(Carte("carte", None, None, None, None, None, None))
		self.assertTrue(self.joueur.possedeCarteChainage(Carte("carte2", None, None, None, "carte", None, None)))

		self.assertFalse(self.joueur.possedeCarteChainage(Carte("carte3", None, None, None, "erreur", None, None)))
		self.joueur.cartes.clear()

	def testListeRessourcePrixReduit(self):
		douane = Carte("douanes", None, ["reduc_ressource papyrus 1", "reduc_ressource verre 1"], ["monnaie 4"],
		      None, "jaune", age=2)
		self.joueur.cartes.append(douane)
		self.assertEqual(1, self.joueur.possedeReduction("papyrus"))
		self.assertEqual(0, self.joueur.possedeReduction("pierre"))


if __name__ == '__main__':
	unittest.main()
