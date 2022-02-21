import unittest

from src.main import Joueur, Jeu, Carte


class TestJeu(unittest.TestCase):
	def testAcheterRessource(self):
		# exemple du manuel
		j1 = Joueur("Bruno")
		j2 = Joueur("Antoine")
		jeu = Jeu(j1, j2)

		j1.monnaie = j2.monnaie = 10
		jeu.quiJoue = j2

		j1.cartes.append(Carte("carrière", None, ["ressource pierre 2"], ["monnaie 2"], None, "marron", age=2))
		jeu.acheterRessource(["ressource pierre 1"])
		# j2 veut acheter une pierre, mais j1 en produit deux, [ 2 + 2(quantite_pierre_j1) ] * quantite_pierre_acheté
		self.assertEqual(6, jeu.quiJoue.monnaie)

	def testAcheterRessource2(self):
		# exemple du manuel
		j1 = Joueur("Bruno")
		j2 = Joueur("Antoine")
		jeu = Jeu(j1, j2)

		j1.monnaie = j2.monnaie = 10
		jeu.quiJoue = j2

		j1.cartes.append(Carte("bassin argileux", None, ["ressource argile 1"], None, None, "marron", age=1))
		jeu.acheterRessource(["ressource argile 1", "ressource papyrus 1"])

		self.assertEqual(5, jeu.quiJoue.monnaie)


if __name__ == '__main__':
	unittest.main()