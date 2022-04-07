class Arbre:
	def __init__(self, etat_jeu):
		self.eval = 0
		self.etat_jeu = etat_jeu
		self.liste_fils = []
		
	def __eq__(self, autre):
		return self.etat_jeu == autre.etat_jeu \
			and self.eval == autre.eval \
			and self.liste_fils == autre.liste_fils
		
	def fct_eval(self):
		self.eval = 0
			
	def remplir(self, profondeur_actuelle, profondeur_max):
		if profondeur_actuelle < profondeur_max:
			for carte in self.etat_jeu.liste_cartes_prenables():

				copie_jeu = self.etat_jeu
				copie_jeu.jouer_coup_carte(carte)

				nouv_etat_jeu = Arbre(copie_jeu)
				nouv_etat_jeu.remplir(profondeur_actuelle+1, profondeur_max)
				nouv_etat_jeu.fct_eval()
				
				self.liste_fils.append(nouv_etat_jeu)


class Minimax:
	def __init__(self, jeu_initial):
		self.jeu_initial = jeu_initial
		self.arbre = Arbre(jeu_initial)
		self.prochain_coup = None
		
	def simuler(self):
		self.jeu_initial.remplir(self.jeu_initial, 0, 1)
	
	
				