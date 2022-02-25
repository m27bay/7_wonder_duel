"""
Fichier de test pour la classe Jeu.
"""

import unittest

from src.main import Joueur, Jeu, Carte, JetonProgres, demander_element_dans_une_liste


class TestJeu(unittest.TestCase):
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
		jeu = Jeu(Joueur("j1"), Joueur("j2"))
		prix = jeu.acheter_ressources(["ressource pierre 1"])
		self.assertEqual(2, prix)

	def testAcheterRessourceProduiteParAdversaire(self):
		# exemple du manuel
		# https://cdn.1j1ju.com/medias/bd/ad/a7-7-wonders-duel-regles.pdf
		# page 9
		
		j1 = Joueur("Bruno")
		j2 = Joueur("Antoine")
		jeu = Jeu(j1, j2)
		j1.monnaie = j2.monnaie = 10
		jeu.joueur_qui_joue = j2
		
		j1.cartes.append(Carte("carrière", None, ["ressource pierre 2"], ["monnaie 2"], None, "marron", age=2))
		prix = jeu.acheter_ressources(["ressource pierre 1"])
		# j2 veut acheter une pierre, mais j1 en produit deux, [ 2 + (quantite_pierre_j1) ] * quantite_pierre_acheté
		self.assertEqual(4, prix)

	def testAcheterRessourceProduiteParAdversaire2(self):
		# exemple du manuel
		
		j1 = Joueur("Bruno")
		j2 = Joueur("Antoine")
		jeu = Jeu(j1, j2)
		j1.monnaie = j2.monnaie = 10
		jeu.joueur_qui_joue = j2

		j1.cartes.append(Carte("bassin argileux", None, ["ressource argile 1"], None, None, "marron", age=1))
		prix = jeu.acheter_ressources(["ressource argile 1", "ressource papyrus 1"])

		self.assertEqual(5, prix)

	def testAcheterRessourceProduiteParAdversaire3(self):
		# exemple du manuel
		
		j1 = Joueur("Bruno")
		j2 = Joueur("Antoine")
		jeu = Jeu(j1, j2)
		j1.monnaie = j2.monnaie = 12
		jeu.joueur_qui_joue = j2

		j1.cartes.append(Carte("carte custom", None, ["ressource pierre 2"], None, None, None, None))
		prix = jeu.acheter_ressources(["ressource pierre 3"])

		self.assertEqual(12, prix)

	def testAcheterRessourceProduiteParAdversaireAvecReduction(self):
		j1 = Joueur("Bruno")
		j2 = Joueur("Antoine")
		jeu = Jeu(j1, j2)
		j1.monnaie = j2.monnaie = 10
		jeu.joueur_qui_joue = j2
		
		j1.cartes.append(Carte("carrière", None, ["ressource pierre 2"], ["monnaie 2"], None, "marron", age=2))
		j2.cartes.append(
			Carte("dépot de pierre", None, ["reduc_ressource pierre 1"], ["monnaie 3"], None, "jaune", age=1)
		)
		prix = jeu.acheter_ressources(["ressource pierre 1"])

		self.assertEqual(1, prix)
		
	def testDemanderActionCartePiocherCarteQuiNeCouteRien(self):
		# entrée piocher
		j1 = Joueur("Bruno")
		j2 = Joueur("Antoine")
		jeu = Jeu(j1, j2)
		j1.monnaie = j2.monnaie = 10
		jeu.joueur_qui_joue = j1

		jeu.cartes_plateau = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		]
		jeu.cartes_plateau[4][0] = Carte("presse", None, ["ressource papyrus 1"], ["monnaie 1"], None, "grise", age=1)

		jeu.demander_action_carte(jeu.cartes_plateau[4][0])
		self.assertFalse(jeu.reste_des_cartes())

	def testDemanderActionCarteDefausserSansCarteJaune(self):
		# entrée defausser
		j1 = Joueur("Bruno")
		j2 = Joueur("Antoine")
		jeu = Jeu(j1, j2)
		j1.monnaie = 0
		j2.monnaie = 10
		jeu.joueur_qui_joue = j1
		
		jeu.cartes_plateau = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		]
		carte = Carte("carrière", None, ["ressource pierre 2"], ["monnaie 2"], None, "marron", age=2)
		jeu.cartes_plateau[4][0] = carte

		jeu.demander_action_carte(carte)

		self.assertEqual(2, jeu.joueur_qui_joue.monnaie)
		self.assertFalse(jeu.reste_des_cartes())

	def testDemanderActionCarteDefausserAvecCarteJaune(self):
		# entrée defausser
		j1 = Joueur("Bruno")
		j2 = Joueur("Antoine")
		jeu = Jeu(j1, j2)
		j1.monnaie = 0
		j2.monnaie = 10
		jeu.joueur_qui_joue = j1

		jeu.cartes_plateau = [
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
				[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		]
		carte = Carte("carrière", None, ["ressource pierre 2"], ["monnaie 2"], None, "marron", age=2)
		jeu.cartes_plateau[4][0] = carte

		j1.cartes.append(
			Carte("arène", None, ["monnaie_par_merveille 2", "point_victoire 3"],
			["ressource argile 1", "ressource pierre 1", "ressource bois 1"], "brasserie", "jaune", age=3)
		)

		jeu.demander_action_carte(carte)
		self.assertFalse(jeu.reste_des_cartes())

		try:
			jeu.cartes_defaussees.index(carte)
		except ValueError:
			self.fail("la carte n'a pas été ajouté à la fausse.")

		self.assertEqual(3, jeu.joueur_qui_joue.monnaie)
		self.assertFalse(jeu.reste_des_cartes())

	def testDemanderActionCartePiocherAvecCarteChainage(self):
		# entrée piocher
		j1 = Joueur("Bruno")
		j2 = Joueur("Antoine")
		jeu = Jeu(j1, j2)
		j1.monnaie = j2.monnaie = 10
		jeu.joueur_qui_joue = j1

		jeu.cartes_plateau = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		]
		carte = Carte("arène ", None, ["monnaie_par_merveille 2", "point_victoire 3"],
			["ressource argile 1", "ressource pierre 1", "ressource bois 1"],
			"brasserie", "jaune", age=3)
		jeu.cartes_plateau[4][0] = carte

		j1.cartes.append(Carte("brasserie", None, ["monnaie 6"], None, "taverne", "jaune", age=2))
		jeu.demander_action_carte(carte)

		self.assertFalse(jeu.reste_des_cartes())

	def testDemanderActionCartePiocherJoueurPossedeRessourceMonnaie(self):
		# entrée piocher
		j1 = Joueur("Bruno")
		j2 = Joueur("Antoine")
		jeu = Jeu(j1, j2)
		j1.monnaie = j2.monnaie = 10
		jeu.joueur_qui_joue = j1

		jeu.cartes_plateau = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		]
		carte = Carte("presse", None, ["ressource papyrus 1"], ["monnaie 1"], None, "grise", age=1)
		jeu.cartes_plateau[4][0] = carte
		jeu.demander_action_carte(carte)

		self.assertFalse(jeu.reste_des_cartes())
		self.assertEqual(9, j1.monnaie)

	def testDemanderActionCartePiocherJoueurPossedePasRessources(self):
		# entrée piocher
		j1 = Joueur("Bruno")
		j2 = Joueur("Antoine")
		jeu = Jeu(j1, j2)
		j1.monnaie = j2.monnaie = 10
		jeu.joueur_qui_joue = j1

		jeu.cartes_plateau = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		]
		jeu.joueur_qui_joue.cartes.append(
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
		jeu.cartes_plateau[4][0] = carte2
		jeu.demander_action_carte(carte2)

		self.assertFalse(jeu.reste_des_cartes())
		self.assertEqual(8, j1.monnaie)

	def testResteDesCartes(self):
		j1 = Joueur("Bruno")
		j2 = Joueur("Antoine")
		jeu = Jeu(j1, j2)
		
		jeu.cartes_plateau = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
		]

		self.assertTrue(jeu.reste_des_cartes())

		jeu.cartes_plateau = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		]

		self.assertFalse(jeu.reste_des_cartes())

	def testCartePrenable(self):
		j1 = Joueur("Bruno")
		j2 = Joueur("Antoine")
		jeu = Jeu(j1, j2)
		
		jeu.preparation_cartes()

		self.assertTrue(jeu.cartes_prenable(4, 0))
		self.assertTrue(jeu.cartes_prenable(4, 10))
		self.assertFalse(jeu.cartes_prenable(3, 1))
		self.assertFalse(jeu.cartes_prenable(0, 4))

	def testListeCartesPrenable(self):
		j1 = Joueur("Bruno")
		j2 = Joueur("Antoine")
		jeu = Jeu(j1, j2)
		
		jeu.preparation_cartes()

		liste_carte_prenable = []

		for num_ligne, ligne_carte in enumerate(jeu.cartes_plateau):
			for num_colonne, carte in enumerate(ligne_carte):
				if carte != 0 and num_ligne == 4:
					liste_carte_prenable.append(carte)

		self.assertEqual(liste_carte_prenable, jeu.liste_cartes_prenables())

	def testDefausserCarteAdversairePossedeCarteCouleur(self):
		# entrée chantier
		j1 = Joueur("Bruno")
		j2 = Joueur("Antoine")
		jeu = Jeu(j1, j2)
		jeu.joueur_qui_joue = j1
		
		carte = Carte("chantier", None, ["ressource bois 1"], None, None, "marron", age=1)
		j2.cartes.append(carte)
		jeu.defausser_carte_adversaire("marron")

		self.assertEqual([], j2.cartes)
		self.assertEqual([carte], jeu.cartes_defaussees)

	def testDemanderRessourceAuChoix(self):
		# entrée bois
		j1 = Joueur("Bruno")
		j2 = Joueur("Antoine")
		jeu = Jeu(j1, j2)
		jeu.joueur_qui_joue = j1
		
		ressource = jeu.demander_ressource_au_choix(["bois", "pierre"])
		self.assertEqual("ressource bois 1", ressource)

	def testGainSymboleScientifique(self):
		# entrée agriculture
		j1 = Joueur("Bruno")
		j2 = Joueur("Antoine")
		jeu = Jeu(j1, j2)
		jeu.joueur_qui_joue = j1
		
		jeton = JetonProgres("agriculture", None, ["monnaie 6", "point_victoire 4"])
		jeu.jetons_progres_plateau.append(jeton)

		carte = Carte("atelier", None, ["symbole_scientifique pendule", "point_victoire 1"], ["ressource papurys 1"],
			None, "vert", age=1)
		jeu.joueur_qui_joue.cartes.append(carte)
		jeu.gain_symbole_scientifique("pendule")
		carte_custom = Carte("atelier", None, ["point_victoire 1"], ["ressource papurys 1"], None, "vert", age=1)
		
		self.assertEqual([jeton], jeu.joueur_qui_joue.jetons)
		self.assertEqual([], jeu.jetons_progres_plateau)
		self.assertEqual(carte_custom, jeu.joueur_qui_joue.cartes[0])

	def testJoueur1AttaquePositionNeutre(self):
		j1 = Joueur("Bruno")
		j2 = Joueur("Antoine")
		jeu = Jeu(j1, j2)
		jeu.joueur_qui_joue = j1
		
		jeu.joueur_deplace_pion_militaire(1)
		
		self.assertEqual(10, jeu.position_jeton_conflit)
	
	def testJoueur3AttaquePositionNeutre(self):
		j1 = Joueur("Bruno")
		j2 = Joueur("Antoine")
		jeu = Jeu(j1, j2)
		j1.monnaie = j2.monnaie = 10
		jeu.joueur_qui_joue = j1
		
		jeu.joueur_deplace_pion_militaire(3)
		
		self.assertEqual(12, jeu.position_jeton_conflit)
		self.assertEqual(7, j1.points_victoire)
		self.assertEqual(8, j2.monnaie)


if __name__ == '__main__':
	unittest.main()
