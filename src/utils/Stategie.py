import math
import csv

from src.utils.Plateau import Plateau


notation_carte = {}
# with open("../../src/utils/notation_cartes.csv", mode='r') as file:
with open("src/utils/notation_cartes.csv", mode='r') as file:
	fichier_cvs = csv.reader(file)
	for lignes in fichier_cvs:
		notation_carte[lignes[0]] = int(lignes[1])


def partie_fini(partie: Plateau):
	return (not partie.reste_des_cartes() and partie.age == 3) \
		or (partie.joueur1.symb_scientifique == 6 or partie.joueur2.symb_scientifique == 6) \
		or (partie.position_jeton_conflit in [0, 18])
	
	
def fonction_evaluation(partie):
	# TODO : prendre en compte merveille, carte guilde
	evaluation_j2 = 0
	for carte in partie.joueur2.cartes:
		if carte.est_face_cachee:
			evaluation_j2 += 10
		else:
			evaluation_j2 += notation_carte[carte.nom]
			
	if partie.joueur1.monnaie == 0:
		evaluation_j2 += 10
	
	if partie.position_jeton_conflit == 0:
		evaluation_j2 += 10
	
	evaluation_j1 = 0
	for carte in partie.joueur1.cartes:
		if carte.est_face_cachee:
			evaluation_j1 += 10
		else:
			evaluation_j1 += notation_carte[carte.nom]
			
	if partie.position_jeton_conflit == 18:
		evaluation_j1 += 10
		
	return evaluation_j2 - evaluation_j1


def minimax(partie, profondeur, coup_bot, nbr_noeuds):
	if profondeur == 0 or partie_fini(partie):
		return fonction_evaluation(partie), None, nbr_noeuds+1
	
	carte_a_prendre = None
	
	if coup_bot:
		partie.joueur_qui_joue = partie.joueur2
		# print("j2")
		max_eval = -math.inf
		
		for carte in partie.liste_cartes_prenables():
			
			copie_partie: Plateau = partie.constructeur_par_copie()
			
			ret = copie_partie.piocher(carte)
			
			if ret == -1:
				copie_partie.defausser(carte)
			
			else:
				copie_partie.joueur_qui_joue.cartes.append(carte)
				copie_partie.enlever_carte(carte)
			
			evaluation, _, nbr_noeuds = minimax(copie_partie, profondeur - 1, False, nbr_noeuds)
			# print(f"evaluation : {evaluation}, carte : {carte}")
			
			if evaluation > max_eval:
				max_eval = evaluation
				carte_a_prendre = carte
				
		return max_eval, carte_a_prendre, nbr_noeuds+1
	
	else:
		partie.joueur_qui_joue = partie.joueur1
		# print("j1")
		min_eval = math.inf
		
		for carte in partie.liste_cartes_prenables():
			
			copie_partie: Plateau = partie.constructeur_par_copie()
			copie_partie.piocher(carte)
			copie_partie.joueur_qui_joue.cartes.append(carte)
			copie_partie.enlever_carte(carte)
		
			evaluation, _, nbr_noeuds = minimax(copie_partie, profondeur - 1, True, nbr_noeuds)
			# print(f"evaluation : {evaluation}, carte : {carte}")
			
			if evaluation < min_eval:
				min_eval = evaluation
				carte_a_prendre = carte
		
		return min_eval, carte_a_prendre, nbr_noeuds+1
	

def alpha_beta(partie, profondeur, alpha, beta, coup_bot, nbr_noeuds):
	if profondeur == 0 or partie_fini(partie):
		return fonction_evaluation(partie), None, nbr_noeuds+1
	
	carte_a_prendre = None
	
	if coup_bot:
		partie.joueur_qui_joue = partie.joueur2
		# print("j2")
		max_eval = -math.inf
		
		for carte in partie.liste_cartes_prenables():
			
			copie_partie: Plateau = partie.constructeur_par_copie()
			ret = copie_partie.piocher(carte)
			if ret == -1:
				copie_partie.defausser(carte)
			else:
				copie_partie.joueur_qui_joue.cartes.append(carte)
				copie_partie.enlever_carte(carte)
			
			evaluation, _, nbr_noeuds = alpha_beta(copie_partie, profondeur - 1, alpha, beta, False, nbr_noeuds)
			# print(f"evaluation : {evaluation}, carte : {carte}")
			
			if evaluation > max_eval:
				max_eval = evaluation
				carte_a_prendre = carte
				
				alpha = max(alpha, evaluation)
				if beta <= alpha:
					break
				
		return max_eval, carte_a_prendre, nbr_noeuds+1
	
	else:
		partie.joueur_qui_joue = partie.joueur1
		# print("j1")
		min_eval = math.inf
		
		for carte in partie.liste_cartes_prenables():
			
			copie_partie: Plateau = partie.constructeur_par_copie()
			copie_partie.piocher(carte)
			copie_partie.joueur_qui_joue.cartes.append(carte)
			copie_partie.enlever_carte(carte)
			
			evaluation, _, nbr_noeuds = alpha_beta(copie_partie, profondeur - 1, alpha, beta, True, nbr_noeuds)
			# print(f"evaluation : {evaluation}, carte : {carte}")
			
			if evaluation < min_eval:
				min_eval = evaluation
				carte_a_prendre = carte
				
				beta = min(beta, evaluation)
				if beta <= alpha:
					break
		
		return min_eval, carte_a_prendre, nbr_noeuds+1
	


def alpha_beta_avec_merveille(partie, profondeur, alpha, beta, coup_bot, nbr_noeuds):
	if profondeur == 0 or partie_fini(partie):
		return fonction_evaluation(partie), None, nbr_noeuds+1
	
	carte_a_prendre = None
	
	if coup_bot:
		partie.joueur_qui_joue = partie.joueur2
		# print("j2")
		max_eval = -math.inf
		
		for carte in partie.liste_cartes_prenables():
			
			if partie.age == 1:
				
				copie_partie: Plateau = partie.constructeur_par_copie()
				ret = copie_partie.piocher(carte)
				if ret == -1:
					copie_partie.defausser(carte)
				else:
					copie_partie.joueur_qui_joue.cartes.append(carte)
					copie_partie.enlever_carte(carte)
				
				evaluation, _, nbr_noeuds = alpha_beta_avec_merveille(copie_partie,
					profondeur - 1, alpha, beta, False, nbr_noeuds)
				# print(f"evaluation : {evaluation}, carte : {carte}")
				
				if evaluation > max_eval:
					max_eval = evaluation
					carte_a_prendre = carte
					
					alpha = max(alpha, evaluation)
					if beta <= alpha:
						break
						
			else:
				copie_partie_piocher: Plateau = partie.constructeur_par_copie()
				ret = copie_partie_piocher.piocher(carte)
				
				if ret == -1:
					copie_partie_piocher.defausser(carte)
				else:
					copie_partie_piocher.joueur_qui_joue.cartes.append(carte)
					copie_partie_piocher.enlever_carte(carte)
				
				evaluation_piocher, _, nbr_noeuds_piocher = alpha_beta_avec_merveille(copie_partie_piocher,
					profondeur - 1, alpha, beta, False, nbr_noeuds)
				
				for merveille in partie.joueur2.liste_merveilles_non_construite():
					
					copie_partie_merveille: Plateau = partie.constructeur_par_copie()
					ret = copie_partie_merveille.construire_merveille(merveille)
					evaluation_merveille = -math.inf
					nbr_noeuds_merveille = 0
					if ret != -1:
						copie_partie_merveille.enlever_carte(carte)
						evaluation_merveille, _, nbr_noeuds_merveille = alpha_beta_avec_merveille(
							copie_partie_merveille, profondeur - 1, alpha, beta, False, nbr_noeuds)
					
					evaluation = max(evaluation_piocher, evaluation_merveille)
					if evaluation == evaluation_piocher:
						nbr_noeuds = nbr_noeuds_piocher
					else:
						nbr_noeuds = nbr_noeuds_merveille
					
					if evaluation > max_eval:
						max_eval = evaluation
						carte_a_prendre = carte
						
						alpha = max(alpha, evaluation)
						if beta <= alpha:
							break
				
		return max_eval, carte_a_prendre, nbr_noeuds+1
	
	else:
		partie.joueur_qui_joue = partie.joueur1
		# print("j1")
		min_eval = math.inf
		
		for carte in partie.liste_cartes_prenables():
			
			if partie.age == 1:
				
				copie_partie: Plateau = partie.constructeur_par_copie()
				copie_partie.piocher(carte)
				copie_partie.joueur_qui_joue.cartes.append(carte)
				copie_partie.enlever_carte(carte)
				
				evaluation, _, nbr_noeuds = alpha_beta_avec_merveille(copie_partie,
					profondeur - 1, alpha, beta, True, nbr_noeuds)
				# print(f"evaluation : {evaluation}, carte : {carte}")
				
				if evaluation < min_eval:
					min_eval = evaluation
					carte_a_prendre = carte
					
					beta = min(beta, evaluation)
					if beta <= alpha:
						break
						
			else:
				copie_partie_piocher: Plateau = partie.constructeur_par_copie()
				ret = copie_partie_piocher.piocher(carte)
				
				if ret == -1:
					copie_partie_piocher.defausser(carte)
				else:
					copie_partie_piocher.joueur_qui_joue.cartes.append(carte)
					copie_partie_piocher.enlever_carte(carte)
				
				evaluation_piocher, _, nbr_noeuds_piocher = alpha_beta_avec_merveille(copie_partie_piocher,
					profondeur - 1, alpha, beta, False, nbr_noeuds)
				
				for merveille in partie.joueur2.liste_merveilles_non_construite():
					
					copie_partie_merveille: Plateau = partie.constructeur_par_copie()
					ret = copie_partie_merveille.construire_merveille(merveille)
					evaluation_merveille = -math.inf
					nbr_noeuds_merveille = 0
					if ret != -1:
						copie_partie_merveille.enlever_carte(carte)
						evaluation_merveille, _, nbr_noeuds_merveille = alpha_beta_avec_merveille(
							copie_partie_merveille, profondeur - 1, alpha, beta, False, nbr_noeuds)
					
					evaluation = max(evaluation_piocher, evaluation_merveille)
					if evaluation == evaluation_piocher:
						nbr_noeuds = nbr_noeuds_piocher
					else:
						nbr_noeuds = nbr_noeuds_merveille
					
					if evaluation < min_eval:
						min_eval = evaluation
						carte_a_prendre = carte
						
						beta = min(beta, evaluation)
						if beta <= alpha:
							break
		
		return min_eval, carte_a_prendre, nbr_noeuds+1
	