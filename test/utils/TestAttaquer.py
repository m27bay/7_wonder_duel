import unittest

from src.utils.Carte import Carte
from src.utils.JetonProgres import JetonProgres
from src.utils.Joueur import Joueur
from src.utils.Plateau import Plateau


class TestAttaquerJoueur1(unittest.TestCase):
	def setUp(self) -> None:
		self.j1 = Joueur("j1")
		self.j2 = Joueur("j2")
		self.plateau = Plateau(self.j1, self.j2)
		self.j1.monnaie = self.j2.monnaie = 7
		self.plateau.joueur_qui_joue = self.j1
		
	def tearDown(self) -> None:
		for jeton in self.plateau.jetons_militaire:
			jeton.est_utilise = False
	
	def test_attaque1_position_jeton_militaire_neutre(self):
		self.plateau.deplacer_pion_miltaire(1)
		
		# position_neutre (=9) + deplacement (=1) deplacement position car c'est j1 qui attaque
		# = 9 + 1
		# = 10
		self.assertEqual(10, self.plateau.position_jeton_conflit)
		
		# points_victoire_depart + points_victoire_premier_jeton (=2)
		# = 0 + 2
		# = 2
		self.assertEqual(2, self.j1.points_victoire)
		
		# monnaie_depart - monnaie_premier_jeton (=0)
		# = 7 - 0
		# = 7
		self.assertEqual(7, self.j2.monnaie)
		self.assertTrue(self.plateau.jetons_militaire[3].est_utilise)
		
	def test_attaque3_position_jeton_militaire_neutre(self):
		self.plateau.deplacer_pion_miltaire(3)

		# position_neutre (=9) + deplacement (=3) deplacement position car c'est j1 qui attaque
		# = 9 + 3
		# = 12
		self.assertEqual(12, self.plateau.position_jeton_conflit)

		# points_victoire_depart + points_victoire_premier_jeton (=2) + points_victoire_deuxieme_jeton (=5)
		# = 0 + 2 + 5
		# = 7
		self.assertEqual(7, self.j1.points_victoire)

		# monnaie_depart - monnaie_premier_jeton (=0) - monnaie_deuxieme_jeton (=2)
		# = 7 - 0 - 2
		# = 5
		self.assertEqual(5, self.j2.monnaie)
		self.assertTrue(self.plateau.jetons_militaire[3].est_utilise)
		self.assertTrue(self.plateau.jetons_militaire[4].est_utilise)

	def test_appliquer_effets_carte_attaquer1_sans_bonus_jeton_strategie(self):
		carte = Carte("tour de garde", ["attaquer 1"], None, None, "rouge", age=1)

		self.plateau.appliquer_effets_carte(carte)

		self.assertEqual(10, self.plateau.position_jeton_conflit)
		self.assertEqual(2, self.plateau.joueur1.points_victoire)
		self.assertEqual(7, self.plateau.joueur2.monnaie)
		self.assertTrue(self.plateau.jetons_militaire[3].est_utilise)
	
	def test_appliquer_effets_carte_attaquer1_avec_bonus_jeton_strategie(self):
		carte = Carte("tour de garde", ["attaquer 1"], None, None, "rouge", age=1)
		self.plateau.joueur1.jetons_progres.append(JetonProgres("strategie", ["bonus_attaque"]))
	
		self.plateau.appliquer_effets_carte(carte)
	
		self.assertEqual(11, self.plateau.position_jeton_conflit)
		self.assertEqual(2, self.plateau.joueur1.points_victoire)
		self.assertEqual(7, self.plateau.joueur2.monnaie)
		self.assertTrue(self.plateau.jetons_militaire[3].est_utilise)
	
	def test_joueur1_appliquer_effets_carte_attaquer2_avec_bonus_jeton_strategie(self):
		carte = Carte("muraille", ["attaquer 2"], ["ressource pierre 2"], None, "rouge", age=2)
		self.plateau.joueur1.jetons_progres.append(JetonProgres("strategie", ["bonus_attaque"]))
	
		self.plateau.appliquer_effets_carte(carte)
	
		self.assertEqual(12, self.plateau.position_jeton_conflit)
		self.assertEqual(7, self.plateau.joueur1.points_victoire)
		self.assertEqual(5, self.plateau.joueur2.monnaie)
		self.assertTrue(self.plateau.jetons_militaire[3].est_utilise)
		self.assertTrue(self.plateau.jetons_militaire[4].est_utilise)
		
		
class TestAttaquerJoueur2(unittest.TestCase):
	def setUp(self) -> None:
		self.j1 = Joueur("j1")
		self.j2 = Joueur("j2")
		self.plateau = Plateau(self.j1, self.j2)
		self.j1.monnaie = self.j2.monnaie = 7
		self.plateau.joueur_qui_joue = self.j2
		
	def tearDown(self) -> None:
		for jeton in self.plateau.jetons_militaire:
			jeton.est_utilise = False
	
	def test_attaque1_position_jeton_militaire_neutre(self):
		self.plateau.deplacer_pion_miltaire(1)
		
		# position_neutre (=9) + deplacement (=1) deplacement negatif car c'est j2 qui attaque
		# = 9 - 1
		# = 8
		self.assertEqual(8, self.plateau.position_jeton_conflit)
		
		# raisonnement identique qu'au dessus
		self.assertEqual(2, self.j2.points_victoire)
		self.assertEqual(7, self.j1.monnaie)
		self.assertTrue(self.plateau.jetons_militaire[2].est_utilise)

	def test_attaque3_position_jeton_militaire_neutre(self):
		self.plateau.deplacer_pion_miltaire(3)

		# position_neutre (=9) + deplacement (=3) deplacement negatif car c'est j2 qui attaque
		# = 9 - 3
		# = 6
		self.assertEqual(6, self.plateau.position_jeton_conflit)

		# raisonnement identique qu'au dessus
		self.assertEqual(7, self.j2.points_victoire)
		self.assertEqual(5, self.j1.monnaie)
		self.assertTrue(self.plateau.jetons_militaire[2].est_utilise)
		self.assertTrue(self.plateau.jetons_militaire[1].est_utilise)
	
	def test_appliquer_effets_carte_attaquer1_sans_bonus_jeton_strategie(self):
		carte = Carte("tour de garde", ["attaquer 1"], None, None, "rouge", age=1)

		self.plateau.appliquer_effets_carte(carte)

		self.assertEqual(8, self.plateau.position_jeton_conflit)
		self.assertEqual(2, self.plateau.joueur2.points_victoire)
		self.assertEqual(7, self.plateau.joueur1.monnaie)
		self.assertTrue(self.plateau.jetons_militaire[2].est_utilise)
		
	def test_appliquer_effets_carte_attaquer1_avec_bonus_jeton_strategie(self):
		carte = Carte("tour de garde", ["attaquer 1"], None, None, "rouge", age=1)
		self.plateau.joueur2.jetons_progres.append(JetonProgres("strategie", ["bonus_attaque"]))

		self.plateau.appliquer_effets_carte(carte)

		self.assertEqual(7, self.plateau.position_jeton_conflit)
		self.assertEqual(2, self.plateau.joueur2.points_victoire)
		self.assertEqual(7, self.plateau.joueur1.monnaie)
		self.assertTrue(self.plateau.jetons_militaire[2].est_utilise)

	def test_appliquer_effets_carte_attaquer2_avec_bonus_jeton_strategie(self):
		carte = Carte("muraille", ["attaquer 2"], ["ressource pierre 2"], None, "rouge", age=2)
		self.plateau.joueur2.jetons_progres.append(JetonProgres("strategie", ["bonus_attaque"]))

		self.plateau.appliquer_effets_carte(carte)

		self.assertEqual(6, self.plateau.position_jeton_conflit)
		self.assertEqual(7, self.plateau.joueur2.points_victoire)
		self.assertEqual(5, self.plateau.joueur1.monnaie)
		self.assertTrue(self.plateau.jetons_militaire[2].est_utilise)
		self.assertTrue(self.plateau.jetons_militaire[1].est_utilise)


if __name__ == '__main__':
	unittest.main()
