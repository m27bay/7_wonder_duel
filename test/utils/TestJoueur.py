"""
Fichier test de la classe Joueur.
"""

import unittest

from src.utils.Carte import Carte
from src.utils.Joueur import Joueur
from src.utils.CarteFille import CarteFille
from src.utils.JetonProgres import JetonProgres


class TestJoueur(unittest.TestCase):
	def setUp(self) -> None:
		"""
		Initialise un nom_joueur pour la suite des test.
		"""
		self.joueur = Joueur("j1")
	
	def test_constructeur(self):
		self.assertEqual(self.joueur.nom, "j1")
		self.assertEqual(self.joueur.cartes, [])
		self.assertEqual(self.joueur.merveilles, [])
		self.assertEqual(self.joueur.jetons_progres, [])
		self.assertEqual(self.joueur.ressources,
			{"bois": 0, "pierre": 0, "argile": 0, "verre": 0, "papyrus": 0})
		self.assertEqual(self.joueur.monnaie, 0)
		self.assertEqual(self.joueur.points_victoire, 0)
		
	def test_constructeur_par_copie(self):
		joueur_copie = self.joueur.constructeur_par_copie()
		
		self.assertEqual(joueur_copie, self.joueur)
	
	def test_eq(self):
		joueur2 = Joueur("j2")
		self.assertNotEqual(self.joueur, joueur2)
		
		joueur3 = Joueur("j1")
		self.assertEqual(self.joueur, joueur3)
	
	def test_ressources_manquantes(self):
		self.joueur.cartes.clear()
		
		self.joueur.cartes.append(Carte(None, ["ressource bois 2"], None, None, None, None))
		carte = Carte("carte", None, ["ressource bois 2"], None, None, None)
		self.assertEqual([], self.joueur.couts_manquants(carte))
		self.joueur.cartes.clear()
		
		self.joueur.cartes.append(Carte(None, ["ressource bois 2"], None, None, None, None))
		carte2 = Carte("carte2", None, ["ressource bois 1", "ressource verre 2"], None, None, None)
		self.assertEqual(["ressource verre 2"], self.joueur.couts_manquants(carte2))
		self.joueur.cartes.clear()
		
		self.joueur.cartes.append(Carte(None, ["ressource bois 1"], None, None, None, None))
		carte3 = Carte("carte3", None, ["ressource bois 2", "ressource verre 2"], None, None, None)
		self.assertEqual(["ressource bois 1", "ressource verre 2"], self.joueur.couts_manquants(carte3))
		self.joueur.cartes.clear()
	
	def test_monnaies_manquantes(self):
		self.joueur.monnaie = 4
		carte = Carte(None, None, ["monnaie 4"], None, None, None)
		self.assertEqual([], self.joueur.couts_manquants(carte))
		
		carte = Carte(None, None, ["monnaie 5"], None, None, None)
		self.assertEqual(["monnaie 1"], self.joueur.couts_manquants(carte))
	
	def test_possede_carte_chainage(self):
		self.joueur.cartes.clear()
		
		self.joueur.cartes.append(Carte("carte", None, None, None, None, None))
		
		self.assertTrue(self.joueur.possede_carte_chainage(Carte("carte2", None, None, "carte", None, None)))
		self.assertFalse(self.joueur.possede_carte_chainage(Carte("carte3", None, None, "erreur", None, None)))
	
	def test_production_type_ressources(self):
		self.joueur.cartes.clear()
		
		self.joueur.cartes.append(Carte("carte", ["ressource bois 1"], None, None, None, None))
		
		self.assertEqual("carte", self.joueur.production_type_ressources("ressource bois 1").nom)
		self.assertEqual(None, self.joueur.production_type_ressources("ressource pierre 1"))
	
	def test_liste_ressource_prix_reduit(self):
		self.joueur.cartes.clear()
		
		douane = Carte("douanes", ["reduc_ressource papyrus 1", "reduc_ressource verre 1"], ["monnaie 4"],
			None, "jaune", age=2)
		self.joueur.cartes.append(douane)
		
		self.assertEqual(1, self.joueur.possede_carte_reduction("papyrus"))
		self.assertEqual(0, self.joueur.possede_carte_reduction("pierre"))
	
	def test_possede_cartes_couleur(self):
		self.joueur.cartes.clear()
		
		carte = Carte("chantier", ["ressource bois 1"], None, None, "marron", age=1)
		self.joueur.cartes.append(carte)
		liste_carte_coul = self.joueur.possede_cartes_couleur("marron")
		
		self.assertEqual([carte], liste_carte_coul)
		
		carte2 = Carte("exploitation", ["ressource bois 1"], ["monnaie 1"], None, "marron", age=1)
		self.joueur.cartes.append(carte2)
		liste_carte_coul = self.joueur.possede_cartes_couleur("marron")
		
		self.assertEqual([carte, carte2], liste_carte_coul)
	
	def test_possede_pas_cartes_couleur(self):
		self.joueur.cartes.clear()
		
		carte = Carte("chantier", ["ressource bois 1"], None, None, "marron", age=1)
		self.joueur.cartes.append(carte)
		liste_carte_coul = self.joueur.possede_cartes_couleur("grise")
		
		self.assertEqual([], liste_carte_coul)
	
	def test_possede_jeton_scientifique(self):
		self.joueur.jetons_progres.append(
			JetonProgres("agriculture", ["monnaie 6", "point_victoire 4"])
		)
		
		self.assertTrue(self.joueur.possede_jeton_scientifique("agriculture"))
	
	def test_compter_point_victoire_avec_les_cartes(self):
		self.joueur.cartes.clear()
		
		self.joueur.cartes.append(Carte("theatre", ["point_victoire 3"], None, None, "blue", age=1))
		self.joueur.cartes.append(Carte("autel", ["point_victoire 3"], None, None, "blue", age=1))
		self.joueur.compter_point_victoire()
		self.assertEqual(6, self.joueur.points_victoire)
	
	def test_compter_point_victoire_avec_les_merveilles(self):
		self.joueur.merveilles.clear()
		self.joueur.points_victoire = 0
		
		self.joueur.merveilles.append(
			CarteFille("circus maximus",
				["defausse_carte_adversaire grise", "attaquer 1", "point_victoire 3"],
				["ressource pierre 2", "ressource bois 1", "ressource verre 1"]
			)
		)
		self.joueur.merveilles.append(
			CarteFille("colosse",
				["attaquer 2", "point_victoire 3"],
				["ressource argile 3", "ressource verre 1"]
			)
		)
		self.joueur.compter_point_victoire()
		self.assertEqual(6, self.joueur.points_victoire)
	
	def test_compter_point_victoire_avec_les_jetons(self):
		self.joueur.jetons_progres.clear()
		self.joueur.points_victoire = 0
		
		self.joueur.jetons_progres.append(
			JetonProgres("agriculture", ["monnaie 6", "point_victoire 4"])
		)
		self.joueur.jetons_progres.append(
			JetonProgres("mathematiques_custom", ["point_victoire 3"]),
		)
		self.joueur.compter_point_victoire()
		self.assertEqual(7, self.joueur.points_victoire)
	
	def test_compter_point_victoire_avec_les_jetons2(self):
		self.joueur.jetons_progres.clear()
		self.joueur.points_victoire = 0
		
		self.joueur.jetons_progres.append(
			JetonProgres("agriculture", ["monnaie 6", "point_victoire 4"])
		)
		self.joueur.compter_point_victoire()
		self.assertEqual(4, self.joueur.points_victoire)
		
		self.joueur.jetons_progres.append(
			JetonProgres("mathematiques", ["point_victoire_par_jeton 3", "point_victoire 3"]),
		)
		self.joueur.compter_point_victoire()
		self.assertEqual(4+3*2+3, self.joueur.points_victoire)
	
	def test_selection_merveille(self):
		liste_merveilles = [
			CarteFille("merveille0", None, None),
			CarteFille("merveille1", None, None),
			CarteFille("merveille2", None, None),
			CarteFille("merveille3", None, None),
			CarteFille("merveille4", None, None)
		]
		
		# entree : merveille3, merveille1
		joueur = Joueur("joueur2")
		# copy de la liste car on supprime les merveilles une fois choisie.
		joueur.selection_merveille(2, liste_merveilles.copy())
		self.assertEqual([liste_merveilles[3], liste_merveilles[1]], joueur.merveilles)


if __name__ == '__main__':
	unittest.main()
