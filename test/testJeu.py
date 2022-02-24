import unittest

from src.main import Joueur, Jeu, Carte, JetonProgres, demanderElementDansUneListe


class TestJeu(unittest.TestCase):
	def setUp(self) -> None:
		self.j1 = Joueur("Bruno")
		self.j2 = Joueur("Antoine")
		self.jeu = Jeu(self.j1, self.j2)
		self.j1.monnaie = self.j2.monnaie = 10
		self.jeu.quiJoue = self.j2

	def testDemanderElementDansUneListe(self):
		# entrée carte2
		j1 = Joueur("j1")

		carte1 = Carte("carte1", None, None, None, None, None, None)
		carte2 = Carte("carte2", None, None, None, None, None, None)
		carte3 = Carte("carte3", None, None, None, None, None, None)
		carte4 = Carte("carte4", None, None, None, None, None, None)

		liste = [carte1, carte2, carte3, carte4]

		carteChoisie = demanderElementDansUneListe(j1, "carte", liste)
		self.assertEqual(carte2, carteChoisie)

	def testAcheterRessourceNonProduiteParAdversaire(self):
		prix = self.jeu.acheterRessource(["ressource pierre 1"])

		self.assertEqual(2, prix)

	def testAcheterRessourceProduiteParAdversaire(self):
		# exemple du manuel
		# https://cdn.1j1ju.com/medias/bd/ad/a7-7-wonders-duel-regles.pdf
		# page 9

		self.j1.cartes.append(Carte("carrière", None, ["ressource pierre 2"], ["monnaie 2"], None, "marron", age=2))
		prix = self.jeu.acheterRessource(["ressource pierre 1"])
		# j2 veut acheter une pierre, mais j1 en produit deux, [ 2 + (quantite_pierre_j1) ] * quantite_pierre_acheté
		self.assertEqual(4, prix)

		self.j1.cartes.clear()

	def testAcheterRessourceProduiteParAdversaire2(self):
		# exemple du manuel

		self.j1.cartes.append(Carte("bassin argileux", None, ["ressource argile 1"], None, None, "marron", age=1))
		prix = self.jeu.acheterRessource(["ressource argile 1", "ressource papyrus 1"])

		self.assertEqual(5, prix)

		self.j1.cartes.clear()

	def testAcheterRessourceProduiteParAdversaire3(self):
		# exemple du manuel
		self.j1.monnaie = self.j2.monnaie = 12

		self.j1.cartes.append(Carte("carte custom", None, ["ressource pierre 2"], None, None, None, None))
		prix = self.jeu.acheterRessource(["ressource pierre 3"])

		self.assertEqual(12, prix)

		self.j1.cartes.clear()

	def testAcheterRessourceProduiteParAdversaireAvecReduction(self):
		self.j1.cartes.append(Carte("carrière", None, ["ressource pierre 2"], ["monnaie 2"], None, "marron", age=2))
		self.j2.cartes.append(
			Carte("dépot de pierre", None, ["reduc_ressource pierre 1"], ["monnaie 3"], None, "jaune", age=1)
		)
		prix = self.jeu.acheterRessource(["ressource pierre 1"])

		self.assertEqual(1, prix)

		self.j1.cartes.clear()
		self.j2.cartes.clear()

	def testDemanderActionCartePiocherCarteQuiNeCouteRien(self):
		self.jeu.quiJoue = self.j1

		self.jeu.cartesPlateau = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		]
		self.jeu.cartesPlateau[4][0] = Carte("presse", None, ["ressource papyrus 1"], ["monnaie 1"], None, "grise", age=1)

		self.jeu.demanderActionCarte(self.jeu.cartesPlateau[4][0])

		self.assertFalse(self.jeu.resteDesCartes())

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

		self.assertEqual(2, self.jeu.quiJoue.monnaie)
		self.assertFalse(self.jeu.resteDesCartes())

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

	def testDemanderActionCartePiocherJoueurPossedeRessourceMonnaie(self):
		self.jeu.quiJoue = self.j1

		self.jeu.cartesPlateau = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		]
		carte = Carte("presse", None, ["ressource papyrus 1"], ["monnaie 1"], None, "grise", age=1)
		self.jeu.cartesPlateau[4][0] = carte

		self.jeu.demanderActionCarte(carte)

		self.assertFalse(self.jeu.resteDesCartes())
		self.assertEqual(9, self.j1.monnaie)

	def testDemanderActionCartePiocherJoueurPossedePasRessources(self):
		self.jeu.quiJoue = self.j1

		self.jeu.cartesPlateau = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		]
		self.jeu.quiJoue.cartes.append(
			Carte(
				"presse", None, ["ressource papyrus 1"], ["monnaie 1"], None,
				"grise", age=1
			)
		)

		carte2 = Carte(
			"apothicaire", None,
			["symbole_scientifique roue", "point_victoire 1"],
			["ressource verre 1"],
			None, "vert", age=1
		)
		self.jeu.cartesPlateau[4][0] = carte2

		self.jeu.demanderActionCarte(carte2)

		self.assertFalse(self.jeu.resteDesCartes())
		self.assertEqual(8, self.j1.monnaie)

	def testResteDesCartes(self):
		self.jeu.cartesPlateau = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
		]

		self.assertTrue(self.jeu.resteDesCartes())

		self.jeu.cartesPlateau = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		]

		self.assertFalse(self.jeu.resteDesCartes())

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

	def testDefausserCarteAdversairePossedeCarteCouleur(self):
		self.jeu.quiJoue = self.j1
		carte = Carte("chantier", None, ["ressource bois 1"], None, None, "marron", age=1)
		self.j2.cartes.append(carte)

		self.jeu.defausserCarteAdversaire("marron")

		self.assertEqual([], self.j2.cartes)
		self.assertEqual([carte], self.jeu.fausseCarte)

	def testDefausserCarteAdversairePossedePasCarteCouleur(self):
		self.jeu.quiJoue = self.j1
		carte = Carte("chantier", None, ["ressource bois 1"], None, None, "marron", age=1)
		self.j2.cartes.append(carte)

		self.jeu.defausserCarteAdversaire("grise")

		self.assertEqual([], self.j2.cartes)
		self.assertEqual([carte], self.jeu.fausseCarte)

	def testDemanderRessourceAuChoix(self):
		# entrée bois
		ressource = self.jeu.demanderRessourceAuChoix(["bois", "pierre"])

		self.assertEqual("ressource bois 1", ressource)

	def testGainSymboleScientifique(self):
		# entrée agriculture

		jeton = JetonProgres("agriculture", None, ["monnaie 6", "point_victoire 4"])
		self.jeu.jetonsProgresPlateau.append(jeton)

		carte = Carte("atelier", None, ["symbole_scientifique pendule", "point_victoire 1"], ["ressource papurys 1"],
			      None, "vert", age=1)
		self.jeu.quiJoue.cartes.append(carte)

		self.jeu.gainSymboleScientifique("pendule")

		carteCustom = Carte("atelier", None, ["point_victoire 1"], ["ressource papurys 1"], None, "vert", age=1)
		self.assertEqual([jeton], self.jeu.quiJoue.jetons)
		self.assertEqual([], self.jeu.jetonsProgresPlateau)
		self.assertEqual(carteCustom, self.jeu.quiJoue.cartes[0])

	# def test


if __name__ == '__main__':
	unittest.main()
