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
		
	def test_enlever_une_carte(self):
		self.plateau.joueur_qui_joue = self.j1
		self.plateau.cartes_plateau = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		]
		carte = Carte(
			"carriere", ["ressource pierre 2"], ["monnaie 2"], None, "marron", age=2
		)
		self.plateau.cartes_plateau[4][0] = carte
		self.plateau.enlever_carte(carte)
		
		self.assertEqual(0, self.plateau.cartes_plateau[4][0])
		
	def test_obtenir_adversaire(self):
		self.plateau.joueur_qui_joue = self.j1
		self.assertEqual(self.j2, self.plateau.obtenir_adversaire())
	
	def test_reste_des_cartes(self):
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
	
	def test_carte_prenable(self):
		self.plateau.joueur_qui_joue = self.j1
		self.plateau.preparation_plateau()
		
		self.assertTrue(self.plateau.cartes_prenable(4, 0))
		self.assertTrue(self.plateau.cartes_prenable(4, 10))
		self.assertFalse(self.plateau.cartes_prenable(3, 1))
		self.assertFalse(self.plateau.cartes_prenable(0, 4))
	
	def test_liste_cartes_prenable(self):
		plateau = Plateau(Joueur("j1"), Joueur("j2"))
		plateau.preparation_plateau()
		
		liste_carte_prenable = []
		
		for num_ligne, ligne_carte in enumerate(plateau.cartes_plateau):
			for _, carte in enumerate(ligne_carte):
				if carte != 0 and num_ligne == 4:
					liste_carte_prenable.append(carte)
		
		self.assertEqual(liste_carte_prenable, plateau.liste_cartes_prenables())
	
	def test_acheter_ressource_non_produite_par_adversaire(self):
		self.plateau.joueur_qui_joue = self.j1
		prix = self.plateau.acheter_ressources(["ressource pierre 1"])
		self.assertEqual(2, prix)
	
	def test_acheter_ressource_produite_par_adversaire(self):
		# exemple du manuel
		# https://cdn.1j1ju.com/medias/bd/ad/a7-7-wonders-duel-regles.pdf
		# page 9
		
		self.j1.monnaie = self.j2.monnaie = 10
		self.plateau.joueur_qui_joue = self.j2
		
		self.j1.cartes.append(Carte("carriere", ["ressource pierre 2"], ["monnaie 2"], None, "marron", age=2))
		prix = self.plateau.acheter_ressources(["ressource pierre 1"])
		# j2 veut acheter une pierre, mais j1 en produit deux, [ 2 + (quantite_pierre_j1) ] * quantite_pierre_acheté
		self.assertEqual(4, prix)
	
	def test_acheter_ressource_produite_par_adversaire_2(self):
		# exemple du manuel
		
		self.j1.monnaie = self.j2.monnaie = 10
		self.plateau.joueur_qui_joue = self.j2
		
		self.j1.cartes.append(Carte("bassin argileux", ["ressource argile 1"], None, None, "marron", age=1))
		prix = self.plateau.acheter_ressources(["ressource argile 1", "ressource papyrus 1"])
		
		self.assertEqual(5, prix)
	
	def test_acheter_ressource_produite_par_adversaire_3(self):
		# exemple du manuel
		
		self.j1.monnaie = self.j2.monnaie = 12
		self.plateau.joueur_qui_joue = self.j2
		
		self.j1.cartes.append(Carte("carte custom", ["ressource pierre 2"], None, None, None, None))
		prix = self.plateau.acheter_ressources(["ressource pierre 3"])
		
		self.assertEqual(12, prix)
	
	def test_acheter_ressource_produite_par_adversaire_avec_reduction(self):
		self.j1.monnaie = self.j2.monnaie = 10
		self.plateau.joueur_qui_joue = self.j2
		
		self.j1.cartes.append(Carte("carriere", ["ressource pierre 2"], ["monnaie 2"], None, "marron", age=2))
		self.j2.cartes.append(
			Carte("depot de pierre", ["reduc_ressource pierre 1"], ["monnaie 3"], None, "jaune", age=1)
		)
		prix = self.plateau.acheter_ressources(["ressource pierre 1"])
		
		self.assertEqual(1, prix)
	
	def test_demander_action_carte_piocher_carte_qui_ne_coute_rien(self):
		# entree piocher
		
		self.j1.monnaie = self.j2.monnaie = 10
		self.plateau.joueur_qui_joue = self.j1
		
		self.plateau.cartes_plateau = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		]
		self.plateau.cartes_plateau[4][0] = Carte("presse",
				["ressource papyrus 1"], ["monnaie 1"], None, "grise", age=1)
		
		self.plateau.demander_action_carte(self.plateau.cartes_plateau[4][0])
		self.assertFalse(self.plateau.reste_des_cartes())
	
	def test_demander_action_carte_defausser_sans_carte_jaune(self):
		# entree defausser
		
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
		carte = Carte("carriere", ["ressource pierre 2"], ["monnaie 2"], None, "marron", age=2)
		self.plateau.cartes_plateau[4][0] = carte
		
		self.plateau.demander_action_carte(carte)
		
		self.assertEqual(2, self.plateau.joueur_qui_joue.monnaie)
		self.assertFalse(self.plateau.reste_des_cartes())
	
	def test_demander_action_carte_defausser_avec_carte_jaune(self):
		# entree defausser
		
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
		carte = Carte("carriere", ["ressource pierre 2"], ["monnaie 2"], None, "marron", age=2)
		self.plateau.cartes_plateau[4][0] = carte
		
		self.j1.cartes.append(
			Carte("arene", ["monnaie_par_merveille 2", "point_victoire 3"],
				["ressource argile 1", "ressource pierre 1", "ressource bois 1"], "brasserie", "jaune", age=3)
		)
		
		self.plateau.demander_action_carte(carte)
		self.assertFalse(self.plateau.reste_des_cartes())
		
		try:
			self.plateau.cartes_defaussees.index(carte)
		except ValueError:
			self.fail("la carte n'a pas ete ajoute a la fausse.")
		
		self.assertEqual(4, self.plateau.joueur_qui_joue.monnaie)
	
	def test_demander_action_carte_piocher_avec_carte_chainage(self):
		# entree piocher
		
		self.j1.monnaie = self.j2.monnaie = 10
		self.plateau.joueur_qui_joue = self.j1
		
		self.plateau.cartes_plateau = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		]
		carte = Carte("arene ", ["monnaie_par_merveille 2", "point_victoire 3"],
			["ressource argile 1", "ressource pierre 1", "ressource bois 1"],
			"brasserie", "jaune", age=3)
		self.plateau.cartes_plateau[4][0] = carte
		
		self.j1.cartes.append(Carte("brasserie", ["monnaie 6"], None, "taverne", "jaune", age=2))
		self.plateau.demander_action_carte(carte)
		
		self.assertFalse(self.plateau.reste_des_cartes())
	
	def test_demander_action_carte_piocher_joueur_possede_ressource_monnaie(self):
		# entree piocher
		
		self.j1.monnaie = self.j2.monnaie = 10
		self.plateau.joueur_qui_joue = self.j1
		
		self.plateau.cartes_plateau = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		]
		carte = Carte("presse", ["ressource papyrus 1"], ["monnaie 1"], None, "grise", age=1)
		self.plateau.cartes_plateau[4][0] = carte
		self.plateau.demander_action_carte(carte)
		
		self.assertFalse(self.plateau.reste_des_cartes())
		self.assertEqual(9, self.j1.monnaie)
	
	def test_demander_action_carte_piocher_joueur_possede_pas_ressources(self):
		# entree piocher
		
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
				"presse", ["ressource papyrus 1"], ["monnaie 1"], None,
				"grise", age=1
			)
		)
		
		carte2 = Carte(
			"apothicaire",
			["symbole_scientifique roue", "point_victoire 1"],
			["ressource verre 1"],
			None, "vert", age=1
		)
		self.plateau.cartes_plateau[4][0] = carte2
		self.plateau.demander_action_carte(carte2)
		
		self.assertFalse(self.plateau.reste_des_cartes())
		self.assertEqual(8, self.j1.monnaie)
		
	def test_reduction_couts_ressources(self):
		# entree bois, verre
	
		self.plateau.joueur_qui_joue = self.j1
		carte = Carte("bibliotheque",
			["symbole_scientifique plume", "point_victoire 2"],
			["ressource pierre 1", "ressource bois 1", "ressource verre 1"],
			"scriptorium", "vert", age=2
		)
		
		self.plateau.reduction_couts_construction_carte(carte)
		
		self.assertEqual(["ressource pierre 1"], carte.couts)
	
	def test_defausser_carte_adversaire_possede_carte_couleur(self):
		# entree chantier
		
		self.plateau.joueur_qui_joue = self.j1
		
		carte = Carte("chantier", ["ressource bois 1"], None, None, "marron", age=1)
		self.j2.cartes.append(carte)
		self.plateau.defausser_carte_adversaire("marron")
		
		self.assertEqual([], self.j2.cartes)
		self.assertEqual([carte], self.plateau.cartes_defaussees)
		
	def test_demander_action_merveille_sans_ressources_pour_construire(self):
		# entree oui, circus maximus

		self.plateau.joueur_qui_joue = self.j1
		merveille = CarteFille("circus maximus",
				["defausse_carte_adversaire grise", "attaquer 1", "point_victoire 3"],
				["ressource pierre 2", "ressource bois 1", "ressource verre 1"]
			)
		self.j1.merveilles = [
			merveille,
			CarteFille("jardin suspendus",
				["monnaie 6", "rejouer", "point_victoire 3"],
				["ressource bois 2 ", "ressource verre 1", "ressource papyrus 1"]
			)
		]
		merveille_a_construire = self.plateau.demander_action_merveille()
		
		self.assertEqual(merveille_a_construire, None)
		
	def test_demander_action_merveille_avec_ressources_pour_construire(self):
		# entree oui, circus maximus
		
		self.plateau.joueur_qui_joue = self.j1
		merveille = CarteFille("circus maximus",
			["defausse_carte_adversaire grise", "attaquer 1", "point_victoire 3"],
			["ressource pierre 2", "ressource bois 1", "ressource verre 1"])
		self.j1.merveilles = [merveille,
			CarteFille("jardin suspendus", ["monnaie 6", "rejouer", "point_victoire 3"],
				["ressource bois 2 ", "ressource verre 1", "ressource papyrus 1"])]
		
		self.j1.cartes = [Carte("carte custom",
			["ressource pierre 2", "ressource bois 1", "ressource verre 1"],
			None, None, None, None)]
		merveille_a_construire = self.plateau.demander_action_merveille()
		
		self.assertEqual(merveille_a_construire, None)
	
	def test_demander_ressource_au_choix(self):
		# entree bois
		
		self.plateau.joueur_qui_joue = self.j1
		
		ressource = self.plateau.demander_ressource_au_choix(["bois", "pierre"])
		self.assertEqual("ressource bois 1", ressource)
	
	def test_gain_symbole_scientifique(self):
		# entree agriculture
		
		self.plateau.joueur_qui_joue = self.j1
		
		jeton = JetonProgres("agriculture", ["monnaie 6", "point_victoire 4"])
		self.plateau.jetons_progres_plateau.append(jeton)
		
		carte = Carte("atelier", ["symbole_scientifique pendule", "point_victoire 1"], ["ressource papurys 1"],
			None, "vert", age=1)
		self.plateau.joueur_qui_joue.cartes.append(carte)
		self.plateau.gain_symbole_scientifique("pendule")
		carte_custom = Carte("atelier", ["point_victoire 1"], ["ressource papurys 1"], None, "vert", age=1)
		
		self.assertEqual([jeton], self.plateau.joueur_qui_joue.jetons_progres)
		self.assertEqual([], self.plateau.jetons_progres_plateau)
		self.assertEqual(carte_custom, self.plateau.joueur_qui_joue.cartes[0])
		

if __name__ == '__main__':
	unittest.main()
