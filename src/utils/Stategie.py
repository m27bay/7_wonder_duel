import math
import csv

from src.utils.Plateau import Plateau


notation_carte = {}
with open("src/utils/notation_cartes.csv", mode='r') as file:
	fichier_cvs = csv.reader(file)
	for lignes in fichier_cvs:
		notation_carte[lignes[0]] = int(lignes[1])


def partie_fini(partie: Plateau):
	return (not partie.reste_des_cartes()) \
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
	
	if partie.age != 1:
		evaluation_j2 += 2 * partie.joueur2.nbr_symb_scientifique_diff
		evaluation_j2 += partie.joueur2.points_victoire
		
		if partie.position_jeton_conflit < 9:
			evaluation_j2 += 2 * (9 - partie.position_jeton_conflit)
	
	evaluation_j1 = 0
	for carte in partie.joueur1.cartes:
		if carte.est_face_cachee:
			evaluation_j1 += 10
		else:
			evaluation_j1 += notation_carte[carte.nom]
		
	if partie.age != 1:
		evaluation_j1 += 2*partie.joueur1.nbr_symb_scientifique_diff
		evaluation_j1 += partie.joueur1.points_victoire
		if partie.position_jeton_conflit > 9:
			evaluation_j1 += 2 * (partie.position_jeton_conflit - 9)
	
	# print(f"evaluation_j2 : {evaluation_j2}, evaluation_j1 : {evaluation_j1}")
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
			# TODO : vérifier ajouter carte dans joueur qui joue
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
			ret = copie_partie.piocher(carte)
			
			if ret == -1:
				copie_partie.defausser(carte)
				
			else:
				copie_partie.joueur_qui_joue.cartes.append(carte)
				copie_partie.enlever_carte(carte)
			
			evaluation, _, nbr_noeuds = minimax(copie_partie, profondeur - 1, True, nbr_noeuds)
			# print(f"evaluation : {evaluation}, carte : {carte}")
			
			if evaluation < min_eval:
				min_eval = evaluation
				carte_a_prendre = carte
		
		return min_eval, carte_a_prendre, nbr_noeuds+1
		