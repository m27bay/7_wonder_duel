import unittest

from src.utils.Carte import Carte
from src.utils.Joueur import Joueur
from src.utils.Plateau import Plateau
from src.utils.Stategie import fonction_evaluation


class TestStrategie(unittest.TestCase):
	def test_fonction_evaluation_carte(self):
		plateau = Plateau(Joueur("j1"), Joueur("j2"))
		plateau.joueur2.cartes.append(Carte("chantier", ["ressource bois 1"], None, None, "marron", age=1))
		evaluation = fonction_evaluation(plateau)
		self.assertEqual(20, evaluation)


if __name__ == '__main__':
	unittest.main()
