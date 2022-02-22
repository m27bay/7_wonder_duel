import unittest

from src.main import Joueur, Jeu, Carte


class TestJeu(unittest.TestCase):
	def setUp(self) -> None:
		self.j1 = Joueur("Bruno")
		self.j2 = Joueur("Antoine")
		self.jeu = Jeu(self.j1, self.j2)
		self.j1.monnaie = self.j2.monnaie = 10
		self.jeu.quiJoue = self.j2

	def testAcheterRessourceNonProduiteParAdversaire(self):
		self.jeu.acheterRessource(["ressource pierre 1"])

		self.assertEqual(8, self.jeu.quiJoue.monnaie)

	def testAcheterRessourceProduiteParAdversaire(self):
		# exemple du manuel
		# https://cdn.1j1ju.com/medias/bd/ad/a7-7-wonders-duel-regles.pdf
		# page 9

		self.j1.cartes.append(Carte("carrière", None, ["ressource pierre 2"], ["monnaie 2"], None, "marron", age=2))
		self.jeu.acheterRessource(["ressource pierre 1"])
		# j2 veut acheter une pierre, mais j1 en produit deux, [ 2 + (quantite_pierre_j1) ] * quantite_pierre_acheté
		self.assertEqual(6, self.jeu.quiJoue.monnaie)

		self.j1.cartes.clear()

	def testAcheterRessourceProduiteParAdversaire2(self):
		# exemple du manuel

		self.j1.cartes.append(Carte("bassin argileux", None, ["ressource argile 1"], None, None, "marron", age=1))
		self.jeu.acheterRessource(["ressource argile 1", "ressource papyrus 1"])

		self.assertEqual(5, self.jeu.quiJoue.monnaie)

		self.j1.cartes.clear()

	def testAcheterRessourceProduiteParAdversaire3(self):
		# exemple du manuel
		self.j1.monnaie = self.j2.monnaie = 12

		self.j1.cartes.append(Carte("carte custom", None, ["ressource pierre 2"], None, None, None, None))
		self.jeu.acheterRessource(["ressource pierre 3"])

		self.assertEqual(0, self.jeu.quiJoue.monnaie)

		self.j1.cartes.clear()

	def testAcheterRessourceProduiteParAdversaireAvecReduction(self):
		self.j1.cartes.append(Carte("carrière", None, ["ressource pierre 2"], ["monnaie 2"], None, "marron", age=2))
		self.j2.cartes.append(
			Carte("dépot de pierre", None, ["reduc_ressource pierre 1"], ["monnaie 3"], None, "jaune", age=1)
		)
		self.jeu.acheterRessource(["ressource pierre 1"])

		self.assertEqual(9, self.jeu.quiJoue.monnaie)

		self.j1.cartes.clear()
		self.j2.cartes.clear()

	def testCartePrenable(self):
		self.jeu.preparationCartes()

		self.assertTrue(self.jeu.cartePrenable(4, 0))
		self.assertTrue(self.jeu.cartePrenable(4, 10))
		self.assertFalse(self.jeu.cartePrenable(3, 1))
		self.assertFalse(self.jeu.cartePrenable(0, 4))

	def testListeCartesPrenable(self):
		self.jeu.preparationCartes()

		listeCartePrenable = []

		for ligne in range(len(self.jeu.cartesPlateau)):
			for colonne in range(len(self.jeu.cartesPlateau[ligne])):
				if self.jeu.cartesPlateau[ligne][colonne] != 0 and ligne == 4:
					listeCartePrenable.append(self.jeu.cartesPlateau[ligne][colonne])

		self.assertEqual(listeCartePrenable, self.jeu.listeCartesPrenable())

	def testDemanderActionCarteDefausserSansCarteJaune(self):
		self.j1.monnaie = 0
		self.jeu.quiJoue = self.j1
		self.jeu.cartesPlateau = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		]

		carte = Carte("carrière", None, ["ressource pierre 2"], ["monnaie 2"], None, "marron", age=2)
		self.jeu.cartesPlateau[4][0] = carte

		self.jeu.demanderActionCarte(carte)

		try:
			self.jeu.fausseCarte.index(carte)
		except ValueError:
			self.fail("la carte n'a pas été ajouté à la fausse.")

		self.assertEqual(2, self.jeu.quiJoue.monnaie)

	def testDemanderActionCarteDefausserAvecCarteJaune(self):
		self.j1.monnaie = 0
		self.jeu.quiJoue = self.j1

		self.jeu.cartesPlateau = [
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		]

		carte = Carte("carrière", None, ["ressource pierre 2"], ["monnaie 2"], None, "marron", age=2)
		self.jeu.cartesPlateau[4][0] = carte

		self.j1.cartes.append(
			Carte("arène", None, ["monnaie_par_merveille 2", "point_victoire 3"],
			["ressource argile 1", "ressource pierre 1", "ressource bois 1"], "brasserie", "jaune", age=3)
		)

		self.jeu.demanderActionCarte(carte)
		self.assertFalse(self.jeu.resteDesCartes())

		try:
			self.jeu.fausseCarte.index(carte)
		except ValueError:
			self.fail("la carte n'a pas été ajouté à la fausse.")

		self.assertEqual(3, self.jeu.quiJoue.monnaie)
		self.assertFalse(self.jeu.resteDesCartes())

	def testDemanderActionCartePiocherAvecCarteChainage(self):
		self.jeu.quiJoue = self.j1

		self.jeu.cartesPlateau = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		]
		carte = Carte("arène ", None, ["monnaie_par_merveille 2", "point_victoire 3"],
		              ["ressource argile 1", "ressource pierre 1", "ressource bois 1"],
		              "brasserie", "jaune", age=3)
		self.jeu.cartesPlateau[4][0] = carte

		self.j1.cartes.append(Carte("brasserie", None, ["monnaie 6"], None, "taverne", "jaune", age=2))

		self.jeu.demanderActionCarte(carte)

		self.assertFalse(self.jeu.resteDesCartes())


if __name__ == '__main__':
	unittest.main()
