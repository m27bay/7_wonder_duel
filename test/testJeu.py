"""
Fichier de test pour la classe Jeu.
"""

import unittest

from src.main import Joueur, Jeu, Carte, JetonProgres, demander_element_dans_une_liste


class TestJeu(unittest.TestCase):
	def setUp(self) -> None:
		"""
		Initialise 2 joueurs, et le jeu pour les test suivant.
		"""
		self.j1 = Joueur("Bruno")
		self.j2 = Joueur("Antoine")
		self.jeu = Jeu(self.j1, self.j2)
		self.j1.monnaie = self.j2.monnaie = 10
		self.jeu.joueur_qui_joue = self.j2

	def testDemanderElementDansUneListe(self):
		# entrée carte2
		j1 = Joueur("j1")

		carte1 = Carte("carte1", None, None, None, None, None, None)
		carte2 = Carte("carte2", None, None, None, None, None, None)
		carte3 = Carte("carte3", None, None, None, None, None, None)
		carte4 = Carte("carte4", None, None, None, None, None, None)

		liste = [carte1, carte2, carte3, carte4]

		carte_choisie = demander_element_dans_une_liste(j1, "carte", liste)
		self.assertEqual(carte2, carte_choisie)

	def testAcheterRessourceNonProduiteParAdversaire(self):
		prix = self.jeu.acheter_ressources(["ressource pierre 1"])
		self.assertEqual(2, prix)

	def testAcheterRessourceProduiteParAdversaire(self):
		# exemple du manuel
		# https://cdn.1j1ju.com/medias/bd/ad/a7-7-wonders-duel-regles.pdf
		# page 9

		self.j1.cartes.append(Carte("carrière", None, ["ressource pierre 2"], ["monnaie 2"], None, "marron", age=2))
		prix = self.jeu.acheter_ressources(["ressource pierre 1"])
		# j2 veut acheter une pierre, mais j1 en produit deux, [ 2 + (quantite_pierre_j1) ] * quantite_pierre_acheté
		self.assertEqual(4, prix)

		self.j1.cartes.clear()

	def testAcheterRessourceProduiteParAdversaire2(self):
		# exemple du manuel

		self.j1.cartes.append(Carte("bassin argileux", None, ["ressource argile 1"], None, None, "marron", age=1))
		prix = self.jeu.acheter_ressources(["ressource argile 1", "ressource papyrus 1"])

		self.assertEqual(5, prix)

		self.j1.cartes.clear()

	def testAcheterRessourceProduiteParAdversaire3(self):
		# exemple du manuel
		self.j1.monnaie = self.j2.monnaie = 12

		self.j1.cartes.append(Carte("carte custom", None, ["ressource pierre 2"], None, None, None, None))
		prix = self.jeu.acheter_ressources(["ressource pierre 3"])

		self.assertEqual(12, prix)

		self.j1.cartes.clear()

	def testAcheterRessourceProduiteParAdversaireAvecReduction(self):
		self.j1.cartes.append(Carte("carrière", None, ["ressource pierre 2"], ["monnaie 2"], None, "marron", age=2))
		self.j2.cartes.append(
			Carte("dépot de pierre", None, ["reduc_ressource pierre 1"], ["monnaie 3"], None, "jaune", age=1)
		)
		prix = self.jeu.acheter_ressources(["ressource pierre 1"])

		self.assertEqual(1, prix)

		self.j1.cartes.clear()
		self.j2.cartes.clear()

	def testDemanderActionCartePiocherCarteQuiNeCouteRien(self):
		self.jeu.joueur_qui_joue = self.j1

		self.jeu.cartes_plateau = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		]
		self.jeu.cartes_plateau[4][0] = Carte("presse", None, ["ressource papyrus 1"], ["monnaie 1"], None, "grise", age=1)

		self.jeu.demander_action_carte(self.jeu.cartes_plateau[4][0])

		self.assertFalse(self.jeu.reste_des_cartes())

	def testDemanderActionCarteDefausserSansCarteJaune(self):
		self.j1.monnaie = 0
		self.jeu.joueur_qui_joue = self.j1
		self.jeu.cartes_plateau = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		]
		carte = Carte("carrière", None, ["ressource pierre 2"], ["monnaie 2"], None, "marron", age=2)
		self.jeu.cartes_plateau[4][0] = carte

		self.jeu.demander_action_carte(carte)

		self.assertEqual(2, self.jeu.joueur_qui_joue.monnaie)
		self.assertFalse(self.jeu.reste_des_cartes())

	def testDemanderActionCarteDefausserAvecCarteJaune(self):
		self.j1.monnaie = 0
		self.jeu.joueur_qui_joue = self.j1

		self.jeu.cartes_plateau = [
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		]
		carte = Carte("carrière", None, ["ressource pierre 2"], ["monnaie 2"], None, "marron", age=2)
		self.jeu.cartes_plateau[4][0] = carte

		self.j1.cartes.append(
			Carte("arène", None, ["monnaie_par_merveille 2", "point_victoire 3"],
			["ressource argile 1", "ressource pierre 1", "ressource bois 1"], "brasserie", "jaune", age=3)
		)

		self.jeu.demander_action_carte(carte)
		self.assertFalse(self.jeu.reste_des_cartes())

		try:
			self.jeu.cartes_defaussees.index(carte)
		except ValueError:
			self.fail("la carte n'a pas été ajouté à la fausse.")

		self.assertEqual(3, self.jeu.joueur_qui_joue.monnaie)
		self.assertFalse(self.jeu.reste_des_cartes())

	def testDemanderActionCartePiocherAvecCarteChainage(self):
		self.jeu.joueur_qui_joue = self.j1

		self.jeu.cartes_plateau = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		]
		carte = Carte("arène ", None, ["monnaie_par_merveille 2", "point_victoire 3"],
		              ["ressource argile 1", "ressource pierre 1", "ressource bois 1"],
		              "brasserie", "jaune", age=3)
		self.jeu.cartes_plateau[4][0] = carte

		self.j1.cartes.append(Carte("brasserie", None, ["monnaie 6"], None, "taverne", "jaune", age=2))

		self.jeu.demander_action_carte(carte)

		self.assertFalse(self.jeu.reste_des_cartes())

	def testDemanderActionCartePiocherJoueurPossedeRessourceMonnaie(self):
		self.jeu.joueur_qui_joue = self.j1

		self.jeu.cartes_plateau = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		]
		carte = Carte("presse", None, ["ressource papyrus 1"], ["monnaie 1"], None, "grise", age=1)
		self.jeu.cartes_plateau[4][0] = carte

		self.jeu.demander_action_carte(carte)

		self.assertFalse(self.jeu.reste_des_cartes())
		self.assertEqual(9, self.j1.monnaie)

	def testDemanderActionCartePiocherJoueurPossedePasRessources(self):
		self.jeu.joueur_qui_joue = self.j1

		self.jeu.cartes_plateau = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		]
		self.jeu.joueur_qui_joue.cartes.append(
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
		self.jeu.cartes_plateau[4][0] = carte2

		self.jeu.demander_action_carte(carte2)

		self.assertFalse(self.jeu.reste_des_cartes())
		self.assertEqual(8, self.j1.monnaie)

	def testResteDesCartes(self):
		self.jeu.cartes_plateau = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
		]

		self.assertTrue(self.jeu.reste_des_cartes())

		self.jeu.cartes_plateau = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		]

		self.assertFalse(self.jeu.reste_des_cartes())

	def testCartePrenable(self):
		self.jeu.preparation_cartes()

		self.assertTrue(self.jeu.cartes_prenable(4, 0))
		self.assertTrue(self.jeu.cartes_prenable(4, 10))
		self.assertFalse(self.jeu.cartes_prenable(3, 1))
		self.assertFalse(self.jeu.cartes_prenable(0, 4))

	def testListeCartesPrenable(self):
		self.jeu.preparation_cartes()

		liste_carte_prenable = []

		for ligne in range(len(self.jeu.cartes_plateau)):
			for colonne in range(len(self.jeu.cartes_plateau[ligne])):
				if self.jeu.cartes_plateau[ligne][colonne] != 0 and ligne == 4:
					liste_carte_prenable.append(self.jeu.cartes_plateau[ligne][colonne])

		self.assertEqual(liste_carte_prenable, self.jeu.liste_cartes_prenables())

	def testDefausserCarteAdversairePossedeCarteCouleur(self):
		self.jeu.joueur_qui_joue = self.j1
		carte = Carte("chantier", None, ["ressource bois 1"], None, None, "marron", age=1)
		self.j2.cartes.append(carte)

		self.jeu.defausser_carte_adversaire("marron")

		self.assertEqual([], self.j2.cartes)
		self.assertEqual([carte], self.jeu.cartes_defaussees)

	def testDefausserCarteAdversairePossedePasCarteCouleur(self):
		self.jeu.joueur_qui_joue = self.j1
		carte = Carte("chantier", None, ["ressource bois 1"], None, None, "marron", age=1)
		self.j2.cartes.append(carte)

		self.jeu.defausser_carte_adversaire("grise")

		self.assertEqual([], self.j2.cartes)
		self.assertEqual([carte], self.jeu.cartes_defaussees)

	def testDemanderRessourceAuChoix(self):
		# entrée bois
		ressource = self.jeu.demander_ressource_au_choix(["bois", "pierre"])

		self.assertEqual("ressource bois 1", ressource)

	def testGainSymboleScientifique(self):
		# entrée agriculture

		jeton = JetonProgres("agriculture", None, ["monnaie 6", "point_victoire 4"])
		self.jeu.jetons_progres_plateau.append(jeton)

		carte = Carte("atelier", None, ["symbole_scientifique pendule", "point_victoire 1"], ["ressource papurys 1"],
			      None, "vert", age=1)
		self.jeu.joueur_qui_joue.cartes.append(carte)

		self.jeu.gain_symbole_scientifique("pendule")

		carte_custom = Carte("atelier", None, ["point_victoire 1"], ["ressource papurys 1"], None, "vert", age=1)
		self.assertEqual([jeton], self.jeu.joueur_qui_joue.jetons)
		self.assertEqual([], self.jeu.jetons_progres_plateau)
		self.assertEqual(carte_custom, self.jeu.joueur_qui_joue.cartes[0])

	# def test


if __name__ == '__main__':
	unittest.main()
