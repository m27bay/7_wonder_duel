import unittest

from src.utils.Joueur import Joueur
from src.utils.Plateau import Plateau
from src.utils.Strategie import ArbreMinimax


class TestStrategie(unittest.TestCase):
	def setUp(self) -> None:
		self.jeu = Plateau(Joueur("j1"), Joueur("j2"))
		self.jeu.joueur_qui_joue = self.jeu.joueur1
		self.jeu.preparation_plateau()
		self.arbre = ArbreMinimax(self.jeu)
		
	def test_creation_arbre(self):
		self.assertEqual(self.arbre.jeu_actuel, self.jeu)
		self.assertEqual(self.arbre.evaluation_coup, None)
		self.assertEqual(self.arbre.hauteur, 0)
		self.assertEqual(self.arbre.reponses_possibles, [])
		self.assertEqual(self.arbre.meilleur_coup, None)
		self.assertEqual(self.arbre.evaluation_meilleur_coup, None)
	
	def test_remplir(self):
		self.arbre.remplir_arbre_minimax(0, 1)
		
		self.assertEqual(len(self.arbre.reponses_possibles), 6)
		
		compteur = 0
		for carte in self.jeu.liste_cartes_prenables():
			copie_jeu = self.jeu
			copie_jeu.jouer_coup_carte(carte)
			compteur += 1
			
			nouv_etat_jeu = ArbreMinimax(copie_jeu)
			
			reponse = self.arbre.reponses_possibles[compteur]
			self.assertEqual(nouv_etat_jeu, reponse)
			self.assertEqual(reponse.evaluation_coup, 0)
			self.assertEqual(reponse.hauteur, 1)
			
	def test_remonter_meilleur_coup(self):
		self.arbre.remplir_arbre_minimax(0, 1)
		self.arbre.remonter_meilleur_coup()
		
		self.assertEqual(self.arbre.evaluation_meilleur_coup, 0)


if __name__ == '__main__':
	unittest.main()
