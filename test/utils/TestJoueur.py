"""
Fichier test de la classe Joueur.
"""

import unittest

from src.utils.Carte import Carte
from src.utils.Joueur import Joueur
from src.utils.Merveille import Merveille
from src.utils.JetonProgres import JetonProgres
from src.utils.Plateau import SYMBOLE_SCIENTIFIQUES


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
		
	def test_constructeur_par_copie_symb_scientifique(self):
		joueur = Joueur("test")
		joueur.symb_scientifique["pilon"] = 1
		
		copie = joueur.constructeur_par_copie()
		
		symb_scientifique_copie = {
			"sphere_armillaire": 0,
			"roue": 0,
			"cadran_solaire": 0,
			"pilon": 1,
			"compas_maconniques": 0,
			"plume": 0
		}
		self.assertEqual(copie.symb_scientifique, symb_scientifique_copie)
	
	def test_eq(self):
		joueur2 = Joueur("j2")
		self.assertNotEqual(self.joueur, joueur2)
		
		joueur3 = Joueur("j1")
		self.assertEqual(self.joueur, joueur3)
	
	def test_aucune_ressources_manquantes(self):
		self.joueur.cartes.append(Carte("chantier", ["ressource bois 1"], None, None, "marron", age=1))
		self.joueur.ressources["bois"] = 1
		carte = Carte("ecurie", ["attaquer 1"], ["ressource bois 1"], None, "rouge", age=1)
		self.assertEqual([], self.joueur.couts_manquants(carte))
		
	def test_une_ressources_manquantes(self):
		carte = Carte("atelier",
			[f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[3]}", "point_victoire 1"], ["ressource papyrus 1"],
			None, "vert", age=1)
		self.assertEqual(["ressource papyrus 1"], self.joueur.couts_manquants(carte))
		
	def test_une_quantite_ressources_manquantes(self):
		self.joueur.cartes.append(Carte("gisement", ["ressource pierre 1"], None, None, "marron", age=1))
		self.joueur.ressources["pierre"] = 1
		carte = Carte("muraille", ["attaquer 2"], ["ressource pierre 2"], None, "rouge", age=2)
		self.assertEqual(["ressource pierre 1"], self.joueur.couts_manquants(carte))
		
	def test_une_quantite_et_une_autre_ressources_manquantes(self):
		self.joueur.cartes.append(Carte("chantier", ["ressource bois 1"], None, None, "marron", age=1))
		self.joueur.ressources["bois"] = 1
		carte = Carte("tribunal", ["point_victoire 5"], ["ressource bois 2", "ressource verre 1"], None,
			"bleu", age=2)
		self.assertEqual(["ressource bois 1", "ressource verre 1"], self.joueur.couts_manquants(carte))
		
	def test_cout_manquant_une_ressource_au_choix(self):
		self.joueur.cartes.append(Carte("forum_custom", ["ressource_au_choix bois papyrus"],
			["monnaie 3", "ressource argile 1"], None, "jaune", age=2))
		carte = Carte("haras", ["attaquer 1"], ["ressource argile 1", "ressource bois 1"], "ecuries", "rouge", age=2)
		liste_couts_manquant = self.joueur.couts_manquants(carte)
		self.assertEqual(["ressource argile 1"], self.joueur.cout_manquant_ressource_au_choix(liste_couts_manquant))
	
	def test_cout_manquant_deux_ressource_au_choix(self):
		self.joueur.cartes.append(Carte("caravanserail", ["ressource_au_choix bois argile pierre"],
			["monnaie 2", "ressource verre 1", "ressource papyrus 1"], None, "jaune", age=2))
		carte = Carte("haras", ["attaquer 1"], ["ressource argile 1", "ressource bois 1"], "ecuries", "rouge", age=2)
		liste_couts_manquant = self.joueur.couts_manquants(carte)
		self.assertEqual(["ressource bois 1"], self.joueur.cout_manquant_ressource_au_choix(liste_couts_manquant))
	
	def test_monnaies_manquantes(self):
		self.joueur.monnaie = 4
		carte = Carte(None, None, ["monnaie 4"], None, None, None)
		self.assertEqual([], self.joueur.couts_manquants(carte))
		
		carte = Carte(None, None, ["monnaie 5"], None, None, None)
		self.assertEqual(["monnaie 1"], self.joueur.couts_manquants(carte))
	
	def test_possede_carte_chainage(self):
		self.joueur.cartes.append(Carte("carte", None, None, None, None, None))
		
		self.assertTrue(self.joueur.possede_carte_chainage(Carte("carte2", None, None, "carte", None, None)))
		self.assertFalse(self.joueur.possede_carte_chainage(Carte("carte3", None, None, "erreur", None, None)))
	
	def test_production_type_ressources(self):
		self.joueur.cartes.append(Carte("carte", ["ressource bois 1"], None, None, None, None))
		
		self.assertEqual("carte", self.joueur.production_type_ressources("ressource bois 1").nom)
		self.assertEqual(None, self.joueur.production_type_ressources("ressource pierre 1"))
	
	def test_liste_ressource_prix_reduit(self):
		douane = Carte("douanes", ["reduc_ressource papyrus 1", "reduc_ressource verre 1"], ["monnaie 4"],
			None, "jaune", age=2)
		self.joueur.cartes.append(douane)
		
		self.assertEqual(1, self.joueur.possede_carte_reduction("papyrus"))
		self.assertEqual(0, self.joueur.possede_carte_reduction("pierre"))
	
	def test_possede_cartes_couleur(self):
		carte = Carte("chantier", ["ressource bois 1"], None, None, "marron", age=1)
		self.joueur.cartes.append(carte)
		liste_carte_coul = self.joueur.possede_cartes_couleur("marron")
		
		self.assertEqual([carte], liste_carte_coul)
		
		carte2 = Carte("exploitation", ["ressource bois 1"], ["monnaie 1"], None, "marron", age=1)
		self.joueur.cartes.append(carte2)
		liste_carte_coul = self.joueur.possede_cartes_couleur("marron")
		
		self.assertEqual([carte, carte2], liste_carte_coul)
	
	def test_possede_pas_cartes_couleur(self):
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
		self.joueur.cartes.append(Carte("theatre", ["point_victoire 3"], None, None, "blue", age=1))
		self.joueur.cartes.append(Carte("autel", ["point_victoire 3"], None, None, "blue", age=1))
		self.joueur.compter_point_victoire()
		self.assertEqual(6, self.joueur.points_victoire)
	
	def test_compter_point_victoire_avec_les_merveilles(self):
		self.joueur.merveilles.append(
			Merveille("circus maximus",
				["defausse_carte_adversaire grise", "attaquer 1", "point_victoire 3"],
				["ressource pierre 2", "ressource bois 1", "ressource verre 1"]
			)
		)
		self.joueur.merveilles.append(
			Merveille("colosse",
				["attaquer 2", "point_victoire 3"],
				["ressource argile 3", "ressource verre 1"]
			)
		)
		self.joueur.compter_point_victoire()
		self.assertEqual(6, self.joueur.points_victoire)
	
	def test_compter_point_victoire_avec_les_jetons(self):
		self.joueur.jetons_progres.append(
			JetonProgres("agriculture", ["monnaie 6", "point_victoire 4"])
		)
		self.joueur.jetons_progres.append(
			JetonProgres("mathematiques_custom", ["point_victoire 3"]),
		)
		self.joueur.compter_point_victoire()
		self.assertEqual(7, self.joueur.points_victoire)
	
	def test_compter_point_victoire_avec_les_jetons2(self):
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
		
	def test_liste_merveilles_non_construite(self):
		merveilles = [
			Merveille("mausolee", ["construction_fausse_gratuite", "point_victoire 2"],
			["ressource argile 2", "ressource verre 2", "ressource papyrus 1"]),
			Merveille("grand phare", ["ressource_au_choix bois argile pierre", "point_victoire 4"],
			["ressource bois 1", "ressource pierre 1", "ressource papyrus 2"]),
			Merveille("via appia", ["monnaie 3", "adversaire_perd_monnaie 3", "rejouer", "point_victoire 3"],
			["ressource pierre 2", "ressource argile 2", "ressource papyrus 1"])
		]
		self.joueur.merveilles = merveilles.copy()
		self.joueur.merveilles[0].est_construite = True
		merveilles.remove(merveilles[0])
		
		self.assertEqual(merveilles, self.joueur.liste_merveilles_non_construite())
		
	def test_liste_merveilles_construite(self):
		merveilles = [
			Merveille("mausolee", ["construction_fausse_gratuite", "point_victoire 2"],
			["ressource argile 2", "ressource verre 2", "ressource papyrus 1"]),
			Merveille("grand phare", ["ressource_au_choix bois argile pierre", "point_victoire 4"],
			["ressource bois 1", "ressource pierre 1", "ressource papyrus 2"]),
			Merveille("via appia", ["monnaie 3", "adversaire_perd_monnaie 3", "rejouer", "point_victoire 3"],
			["ressource pierre 2", "ressource argile 2", "ressource papyrus 1"])
		]
		self.joueur.merveilles = merveilles.copy()
		self.joueur.merveilles[0].est_construite = True
		self.joueur.merveilles[2].est_construite = True
		merveilles.remove(merveilles[0])
		merveilles.remove(merveilles[1])
		
		self.assertEqual(merveilles, self.joueur.liste_merveilles_non_construite())


if __name__ == '__main__':
	unittest.main()
