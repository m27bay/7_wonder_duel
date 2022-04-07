import unittest

from src.utils.Joueur import Joueur
from src.utils.Plateau import Plateau
from src.utils.Strategie import Arbre


class MyTestCase(unittest.TestCase):
	def test_creation_arbre(self):
		jeu = Plateau(Joueur("j1"), Joueur("j2"))
		arbre = Arbre(jeu)
		
		self.assertEqual(arbre.etat_jeu, jeu)
		self.assertEqual(arbre.eval, 0)
		self.assertEqual(arbre.liste_fils, [])
		
	def test_fct_eval(self):
		jeu = Plateau(Joueur("j1"), Joueur("j2"))
		arbre = Arbre(jeu)
		
		self.assertEqual(arbre.eval, 0)
	
	def test_remplir(self):
		jeu = Plateau(Joueur("j1"), Joueur("j2"))
		arbre = Arbre(jeu)
		
		arbre.remplir(0, 1)
		for carte in arbre.etat_jeu.liste_cartes_prenables():
			
			copie_jeu = arbre.etat_jeu
			copie_jeu.jouer
		
	# def test_creation_minimax(self):
	

if __name__ == '__main__':
	unittest.main()
