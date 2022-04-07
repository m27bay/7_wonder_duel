class ArbreMinimax:
	def __init__(self, coup_possible):
		self.jeu_actuel = coup_possible
		self.evaluation_coup = None
		
		self.hauteur = 0
		
		self.reponses_possibles = []
		
		self.meilleur_coup = None
		self.evaluation_meilleur_coup = None
		
	def __eq__(self, autre):
		return self.jeu_actuel == autre.jeu_actuel
		
	def evaluer_coup(self):
		self.evaluation_coup = 0
			
	def remplir_arbre_minimax(self, hauteur_actuelle, hauteur_max):
		if hauteur_actuelle < hauteur_max:
			
			for carte in self.jeu_actuel.liste_cartes_prenables():

				copie_jeu = self.jeu_actuel
				copie_jeu.jouer_coup_carte(carte)

				nouv_etat_jeu = ArbreMinimax(copie_jeu)
				nouv_etat_jeu.hauteur = hauteur_actuelle + 1
				
				if hauteur_actuelle + 1 == hauteur_max:
					nouv_etat_jeu.evaluer_coup()
					
				self.reponses_possibles.append(nouv_etat_jeu)
				
				nouv_etat_jeu.remplir_arbre_minimax(hauteur_actuelle + 1, hauteur_max)
				
	def remonter_meilleur_coup(self):
		if not self or not self.reponses_possibles:
			return
		
		for reponse in self.reponses_possibles:
			
			reponse.remonter_meilleur_coup()
			
			if self.meilleur_coup is None:
				self.meilleur_coup = reponse.jeu_actuel
				self.evaluation_meilleur_coup = reponse.evaluation_coup
			else:
				if self.hauteur % 2 != 0:
					if reponse.evaluation_coup < self.evaluation_meilleur_coup:
						self.meilleur_coup = reponse.jeu_actuel
						self.evaluation_meilleur_coup = reponse.evaluation_coup
				else:
					if reponse.evaluation_coup > self.evaluation_meilleur_coup:
						self.meilleur_coup = reponse.jeu_actuel
						self.evaluation_meilleur_coup = reponse.evaluation_coup
			

class Minimax:
	def __init__(self, jeu_initial):
		self.jeu_initial = jeu_initial
		self.arbre = ArbreMinimax(jeu_initial)
		self.prochain_coup = None
		
	def algo_minimax(self):
		self.jeu_initial.remplir_arbre_minimax(self.jeu_initial, 0, 1)
		