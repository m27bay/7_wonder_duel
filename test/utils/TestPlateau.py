"""
Fichier de test pour la classe Jeu.
"""

import unittest

from src.utils.Carte import Carte
from src.utils.CarteFille import CarteFille
from src.utils.JetonProgres import JetonProgres
from src.utils.Joueur import Joueur
from src.utils.Plateau import Plateau


class TestPlateau(unittest.TestCase):
	def setUp(self) -> None:
		"""
		Initialisation de deux joueurs et du plateau pour le reste des tests.
		
		:return:
		"""
		
		self.j1 = Joueur("Bruno")
		self.j2 = Joueur("Antoine")
		self.plateau = Plateau(self.j1, self.j2)
		
	def testEnleverUneCarte(self):
		self.plateau.joueur_qui_joue = self.j1
		self.plateau.cartes_plateau = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		]
		carte = Carte(
			"carriere", None, ["ressource pierre 2"], ["monnaie 2"], None, "marron", age=2
		)
		self.plateau.cartes_plateau[4][0] = carte
		self.plateau.enlever_carte(carte)
		
		self.assertEqual(0, self.plateau.cartes_plateau[4][0])
		
	def testObtenirAdversaire(self):
		self.plateau.joueur_qui_joue = self.j1
		self.assertEqual(self.j2, self.plateau.obtenir_adversaire())
	
	def testResteDesCartes(self):
		self.plateau.cartes_plateau = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
		]
		
		self.assertTrue(self.plateau.reste_des_cartes())
		
		self.plateau.cartes_plateau = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		]
		
		self.assertFalse(self.plateau.reste_des_cartes())
	
	def testCartePrenable(self):
		self.plateau.preparation_cartes()
		
		self.assertTrue(self.plateau.cartes_prenable(4, 0))
		self.assertTrue(self.plateau.cartes_prenable(4, 10))
		self.assertFalse(self.plateau.cartes_prenable(3, 1))
		self.assertFalse(self.plateau.cartes_prenable(0, 4))
	
	def testListeCartesPrenable(self):
		self.plateau.preparation_cartes()
		
		liste_carte_prenable = []
		
		for num_ligne, ligne_carte in enumerate(self.plateau.cartes_plateau):
			for _, carte in enumerate(ligne_carte):
				if carte != 0 and num_ligne == 4:
					liste_carte_prenable.append(carte)
		
		self.assertEqual(liste_carte_prenable, self.plateau.liste_cartes_prenables())
	
	def testAcheterRessourceNonProduiteParAdversaire(self):
		self.plateau.joueur_qui_joue = self.j1
		prix = self.plateau.acheter_ressources(["ressource pierre 1"])
		self.assertEqual(2, prix)
	
	def testAcheterRessourceProduiteParAdversaire(self):
		# exemple du manuel
		# https://cdn.1j1ju.com/medias/bd/ad/a7-7-wonders-duel-regles.pdf
		# page 9
		
		self.j1.monnaie = self.j2.monnaie = 10
		self.plateau.joueur_qui_joue = self.j2
		
		self.j1.cartes.append(Carte("carriere", None, ["ressource pierre 2"], ["monnaie 2"], None, "marron", age=2))
		prix = self.plateau.acheter_ressources(["ressource pierre 1"])
		# j2 veut acheter une pierre, mais j1 en produit deux, [ 2 + (quantite_pierre_j1) ] * quantite_pierre_acheté
		self.assertEqual(4, prix)
	
	def testAcheterRessourceProduiteParAdversaire2(self):
		# exemple du manuel
		
		self.j1.monnaie = self.j2.monnaie = 10
		self.plateau.joueur_qui_joue = self.j2
		
		self.j1.cartes.append(Carte("bassin argileux", None, ["ressource argile 1"], None, None, "marron", age=1))
		prix = self.plateau.acheter_ressources(["ressource argile 1", "ressource papyrus 1"])
		
		self.assertEqual(5, prix)
	
	def testAcheterRessourceProduiteParAdversaire3(self):
		# exemple du manuel
		
		self.j1.monnaie = self.j2.monnaie = 12
		self.plateau.joueur_qui_joue = self.j2
		
		self.j1.cartes.append(Carte("carte_a_enlever custom", None, ["ressource pierre 2"], None, None, None, None))
		prix = self.plateau.acheter_ressources(["ressource pierre 3"])
		
		self.assertEqual(12, prix)
	
	def testAcheterRessourceProduiteParAdversaireAvecReduction(self):
		self.j1.monnaie = self.j2.monnaie = 10
		self.plateau.joueur_qui_joue = self.j2
		
		self.j1.cartes.append(Carte("carriere", None, ["ressource pierre 2"], ["monnaie 2"], None, "marron", age=2))
		self.j2.cartes.append(
			Carte("depot de pierre", None, ["reduc_ressource pierre 1"], ["monnaie 3"], None, "jaune", age=1)
		)
		prix = self.plateau.acheter_ressources(["ressource pierre 1"])
		
		self.assertEqual(1, prix)
	
	def testDemanderActionCartePiocherCarteQuiNeCouteRien(self):
		# entrée piocher
		
		self.j1.monnaie = self.j2.monnaie = 10
		self.plateau.joueur_qui_joue = self.j1
		
		self.plateau.cartes_plateau = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		]
		self.plateau.cartes_plateau[4][0] = Carte("presse", None,
				["ressource papyrus 1"], ["monnaie 1"], None, "grise", age=1)
		
		self.plateau.demander_action_carte(self.plateau.cartes_plateau[4][0])
		self.assertFalse(self.plateau.reste_des_cartes())
	
	def testDemanderActionCarteDefausserSansCarteJaune(self):
		# entrée defausser
		
		self.j1.monnaie = 0
		self.j2.monnaie = 10
		self.plateau.joueur_qui_joue = self.j1
		
		self.plateau.cartes_plateau = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		]
		carte = Carte("carriere", None, ["ressource pierre 2"], ["monnaie 2"], None, "marron", age=2)
		self.plateau.cartes_plateau[4][0] = carte
		
		self.plateau.demander_action_carte(carte)
		
		self.assertEqual(2, self.plateau.joueur_qui_joue.monnaie)
		self.assertFalse(self.plateau.reste_des_cartes())
	
	def testDemanderActionCarteDefausserAvecCarteJaune(self):
		# entrée defausser
		
		self.j1.monnaie = 0
		self.j2.monnaie = 10
		self.plateau.joueur_qui_joue = self.j1
		
		self.plateau.cartes_plateau = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		]
		carte = Carte("carriere", None, ["ressource pierre 2"], ["monnaie 2"], None, "marron", age=2)
		self.plateau.cartes_plateau[4][0] = carte
		
		self.j1.cartes.append(
			Carte("arene", None, ["monnaie_par_merveille 2", "point_victoire 3"],
				["ressource argile 1", "ressource pierre 1", "ressource bois 1"], "brasserie", "jaune", age=3)
		)
		
		self.plateau.demander_action_carte(carte)
		self.assertFalse(self.plateau.reste_des_cartes())
		
		try:
			self.plateau.cartes_defaussees.index(carte)
		except ValueError:
			self.fail("la carte_a_enlever n'a pas ete ajoute a la fausse.")
		
		self.assertEqual(3, self.plateau.joueur_qui_joue.monnaie)
		self.assertFalse(self.plateau.reste_des_cartes())
	
	def testDemanderActionCartePiocherAvecCarteChainage(self):
		# entrée piocher
		
		self.j1.monnaie = self.j2.monnaie = 10
		self.plateau.joueur_qui_joue = self.j1
		
		self.plateau.cartes_plateau = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		]
		carte = Carte("arene ", None, ["monnaie_par_merveille 2", "point_victoire 3"],
			["ressource argile 1", "ressource pierre 1", "ressource bois 1"],
			"brasserie", "jaune", age=3)
		self.plateau.cartes_plateau[4][0] = carte
		
		self.j1.cartes.append(Carte("brasserie", None, ["monnaie 6"], None, "taverne", "jaune", age=2))
		self.plateau.demander_action_carte(carte)
		
		self.assertFalse(self.plateau.reste_des_cartes())
	
	def testDemanderActionCartePiocherJoueurPossedeRessourceMonnaie(self):
		# entrée piocher
		
		self.j1.monnaie = self.j2.monnaie = 10
		self.plateau.joueur_qui_joue = self.j1
		
		self.plateau.cartes_plateau = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		]
		carte = Carte("presse", None, ["ressource papyrus 1"], ["monnaie 1"], None, "grise", age=1)
		self.plateau.cartes_plateau[4][0] = carte
		self.plateau.demander_action_carte(carte)
		
		self.assertFalse(self.plateau.reste_des_cartes())
		self.assertEqual(9, self.j1.monnaie)
	
	def testDemanderActionCartePiocherJoueurPossedePasRessources(self):
		# entrée piocher
		
		self.j1.monnaie = self.j2.monnaie = 10
		self.plateau.joueur_qui_joue = self.j1
		
		self.plateau.cartes_plateau = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		]
		self.plateau.joueur_qui_joue.cartes.append(
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
		self.plateau.cartes_plateau[4][0] = carte2
		self.plateau.demander_action_carte(carte2)
		
		self.assertFalse(self.plateau.reste_des_cartes())
		self.assertEqual(8, self.j1.monnaie)
	
	def testDefausserCarteAdversairePossedeCarteCouleur(self):
		# entrée chantier
		
		self.plateau.joueur_qui_joue = self.j1
		
		carte = Carte("chantier", None, ["ressource bois 1"], None, None, "marron", age=1)
		self.j2.cartes.append(carte)
		self.plateau.defausser_carte_adversaire("marron")
		
		self.assertEqual([], self.j2.cartes)
		self.assertEqual([carte], self.plateau.cartes_defaussees)
		
	def testDemanderActionMerveille(self):
		# entrée oui, circus maximus

		self.plateau.joueur_qui_joue = self.j1
		merveille = CarteFille("circus maximus", None,
				["defausse_carte_adversaire grise", "attaquer 1", "point_victoire 3"],
				["ressource pierre 2", "ressource bois 1", "ressource verre 1"]
			)
		self.j1.merveilles = [
			merveille,
			CarteFille("jardin suspendus", None,
				["monnaie 6", "rejouer", "point_victoire 3"],
				["ressource bois 2 ", "ressource verre 1", "ressource papyrus 1"]
			)
		]
		merveille_a_construire = self.plateau.demander_action_merveille()
		
		self.assertEqual(merveille_a_construire, merveille)
	
	def testDemanderRessourceAuChoix(self):
		# entrée bois
		
		self.plateau.joueur_qui_joue = self.j1
		
		ressource = self.plateau.demander_ressource_au_choix(["bois", "pierre"])
		self.assertEqual("ressource bois 1", ressource)
	
	def testGainSymboleScientifique(self):
		# entrée agriculture
		
		self.plateau.joueur_qui_joue = self.j1
		
		jeton = JetonProgres("agriculture", None, ["monnaie 6", "point_victoire 4"])
		self.plateau.jetons_progres_plateau.append(jeton)
		
		carte = Carte("atelier", None, ["symbole_scientifique pendule", "point_victoire 1"], ["ressource papurys 1"],
			None, "vert", age=1)
		self.plateau.joueur_qui_joue.cartes.append(carte)
		self.plateau.gain_symbole_scientifique("pendule")
		carte_custom = Carte("atelier", None, ["point_victoire 1"], ["ressource papurys 1"], None, "vert", age=1)
		
		self.assertEqual([jeton], self.plateau.joueur_qui_joue.jetons)
		self.assertEqual([], self.plateau.jetons_progres_plateau)
		self.assertEqual(carte_custom, self.plateau.joueur_qui_joue.cartes[0])
	
	def testJoueur1AttaquePositionNeutre(self):
		self.plateau.joueur_qui_joue = self.j1
		
		self.plateau.joueur_deplace_pion_militaire(1)
		
		self.assertEqual(10, self.plateau.position_jeton_conflit)
	
	def testJoueur3AttaquePositionNeutre(self):
		self.j1.monnaie = self.j2.monnaie = 10
		self.plateau.joueur_qui_joue = self.j1
		
		self.plateau.joueur_deplace_pion_militaire(3)
		
		self.assertEqual(12, self.plateau.position_jeton_conflit)
		self.assertEqual(7, self.j1.points_victoire)
		self.assertEqual(8, self.j2.monnaie)


if __name__ == '__main__':
	unittest.main()
