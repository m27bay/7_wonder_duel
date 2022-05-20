import math
import csv
import random

from src.utils.Colours import Couleurs
from src.utils.Merveille import Merveille
from src.utils.Outils import mon_str_liste
from src.utils.Plateau import Plateau
from src.utils.Joueur import Joueur


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
	evaluation_j2 = 0
	for carte in partie.joueur2.cartes:
		if carte.est_face_cachee:
			evaluation_j2 += 10
		else:
			evaluation_j2 += notation_carte[carte.nom]
			
	# print(f"evaluation_j2 cartes : {evaluation_j2}")
	
	for merveille in partie.joueur2.liste_merveilles_construite():
		evaluation_j2 += notation_carte[merveille.nom]
	
	# print(f"evaluation_j2 merveilles : {evaluation_j2}")
	
	evaluation_j2 += partie.joueur2.monnaie
	
	# print(f"evaluation_j2 monnaies : {evaluation_j2}")
	
	if partie.position_jeton_conflit == 0:
		evaluation_j2 += 20
	
	# print(f"evaluation_j2 conflit : {evaluation_j2}")
	
	evaluation_j1 = 0
	for carte in partie.joueur1.cartes:
		if carte.est_face_cachee:
			evaluation_j1 += 10
		else:
			evaluation_j1 += notation_carte[carte.nom]
	
	# print(f"evaluation_j1 cartes : {evaluation_j1}")
	
	for merveille in partie.joueur1.liste_merveilles_construite():
		evaluation_j1 += notation_carte[merveille.nom]
	
	# print(f"evaluation_j1 merveilles : {evaluation_j1}")
	
	evaluation_j1 += partie.joueur1.monnaie
	
	# print(f"evaluation_j1 monnaies : {evaluation_j1}")
	
	if partie.position_jeton_conflit == 18:
		evaluation_j1 += 20
	
	# print(f"evaluation_j1 conflit : {evaluation_j1}")


	# print(f"evaluation_j2 : {evaluation_j2}, evaluation_j1 : {evaluation_j1}")
	return evaluation_j2 - evaluation_j1


def minimax(partie, profondeur, coup_bot, nbr_noeuds):
	if profondeur == 0 or partie_fini(partie):
		return fonction_evaluation(partie), None, nbr_noeuds+1
	
	carte_a_prendre = None
	
	if coup_bot:
		partie.joueur_qui_joue = partie.joueur2
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
			
			if evaluation > max_eval:
				max_eval = evaluation
				carte_a_prendre = carte
				
		return max_eval, carte_a_prendre, nbr_noeuds+1
	
	else:
		partie.joueur_qui_joue = partie.joueur1
		min_eval = math.inf
		
		for carte in partie.liste_cartes_prenables():
			
			copie_partie: Plateau = partie.constructeur_par_copie()
			copie_partie.piocher(carte)
			copie_partie.joueur_qui_joue.cartes.append(carte)
			copie_partie.enlever_carte(carte)
		
			evaluation, _, nbr_noeuds = minimax(copie_partie, profondeur - 1, True, nbr_noeuds)
			
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
			
			if evaluation > max_eval:
				max_eval = evaluation
				carte_a_prendre = carte
				
				alpha = max(alpha, evaluation)
				if beta <= alpha:
					break
				
		return max_eval, carte_a_prendre, nbr_noeuds+1
	
	else:
		partie.joueur_qui_joue = partie.joueur1
		min_eval = math.inf
		
		for carte in partie.liste_cartes_prenables():
			
			copie_partie: Plateau = partie.constructeur_par_copie()
			copie_partie.piocher(carte)
			copie_partie.joueur_qui_joue.cartes.append(carte)
			copie_partie.enlever_carte(carte)
			
			evaluation, _, nbr_noeuds = alpha_beta(copie_partie, profondeur - 1, alpha, beta, True, nbr_noeuds)
			
			if evaluation < min_eval:
				min_eval = evaluation
				carte_a_prendre = carte
				
				beta = min(beta, evaluation)
				if beta <= alpha:
					break
		
		return min_eval, carte_a_prendre, nbr_noeuds+1


def alpha_beta_avec_merveille(partie, profondeur, alpha, beta, coup_bot, nbr_noeuds):
	print(f"{Couleurs.WARNING}alpha_beta_avec_merveille{Couleurs.RESET}")
	if profondeur == 0 or partie_fini(partie):
		print(f"{Couleurs.WARNING}evaluation{Couleurs.RESET}")
		return fonction_evaluation(partie), None, None, nbr_noeuds+1
	
	merveille_a_construire = None
	carte_a_sacrifier = None
	
	if coup_bot:
		print(f"{Couleurs.WARNING}coup bot{Couleurs.RESET}")
		partie.joueur_qui_joue = partie.joueur2
		max_eval = -math.inf
		
		liste_cartes_prenable = partie.liste_cartes_prenables()
		if len(liste_cartes_prenable) == 0:
			return fonction_evaluation(partie), carte_a_sacrifier, merveille_a_construire, nbr_noeuds
		cartes = liste_cartes_prenable + partie.joueur2.liste_merveilles_non_construite()
		for carte in cartes:
			print(f"boucle carte : {carte.nom}")
			copie_partie: Plateau = partie.constructeur_par_copie()
			
			if isinstance(carte, Merveille):
				merveille = carte
				if len(liste_cartes_prenable) >= 1:
					
					carte_random = None
					if len(liste_cartes_prenable) == 1:
						carte_random = liste_cartes_prenable[0]
					
					else:
						print("choix carte à sacrifier")
						for carte_a_sacrifier in liste_cartes_prenable:
							copie_partie_copie = copie_partie.constructeur_par_copie()
							ret = copie_partie_copie.piocher(carte_a_sacrifier)
							if ret == 0:
								carte_random = carte_a_sacrifier
								print(f"choix = {carte_random.nom}")
								break
						if carte_random is None:
							carte_random = liste_cartes_prenable[0]
					
					print(f"carte a sacrifier ? {carte_random.nom}")
					ret = copie_partie.piocher(carte_a_sacrifier)
					if ret == 0:
						copie_partie.enlever_carte(carte_random)
						
						print("construire merveille ?")
						ret = copie_partie.construire_merveille(merveille)
						if ret == (-1, None):
							print(f" non, ressources insuffisantes")
						
						elif ret == (-2, None):
							print(f" non, deja construite")
						
						else:
							copie_partie.joueur_qui_joue.merveilles.append(merveille)
							
							evaluation_merveille, _, _, nbr_noeuds = alpha_beta_avec_merveille(copie_partie,
								profondeur - 1, alpha, beta, True, nbr_noeuds)
							# else:
							# 	evaluation_merveille, _, _, nbr_noeuds = alpha_beta_avec_merveille(copie_partie, profondeur - 1,
							# 		alpha, beta, False, nbr_noeuds)
							
							if evaluation_merveille > max_eval:
								max_eval = evaluation_merveille
								merveille_a_construire = merveille
								carte_a_sacrifier = carte_random
								print(f"merveille : {merveille_a_construire.nom} avec carte {carte_a_sacrifier.nom} : meilleur eval : {max_eval}")
								
								alpha = max(alpha, evaluation_merveille)
								if beta <= alpha:
									break
			
			else:
				print("piocher ?")
				ret = copie_partie.piocher(carte)
				
				if ret == -1:
					print("non, defausse")
					copie_partie.defausser(carte)
				else:
					print("oui")
					copie_partie.joueur_qui_joue.cartes.append(carte)
					copie_partie.enlever_carte(carte)
				
				evaluation_piocher, _, _, nbr_noeuds = alpha_beta_avec_merveille(copie_partie,
					profondeur - 1, alpha, beta, False, nbr_noeuds)
				
				if evaluation_piocher > max_eval:
					max_eval = evaluation_piocher
					print(f"carte {carte.nom} : meilleur eval : {max_eval}")
					carte_a_sacrifier = carte
					
					alpha = max(alpha, evaluation_piocher)
					if beta <= alpha:
						break
						
		print(f"{Couleurs.WARNING}fin coup bot{Couleurs.RESET}")
		return max_eval, carte_a_sacrifier, merveille_a_construire, nbr_noeuds+1
	
	else:
		print(f"{Couleurs.WARNING}coup joueur{Couleurs.RESET}")
		partie.joueur_qui_joue = partie.joueur1
		min_eval = math.inf
		
		for carte in partie.liste_cartes_prenables():
			print(f"joueur piocher : {carte.nom}")
			copie_partie: Plateau = partie.constructeur_par_copie()
			copie_partie.piocher(carte)
			copie_partie.joueur_qui_joue.cartes.append(carte)
			copie_partie.enlever_carte(carte)
			
			evaluation, _, _, nbr_noeuds = alpha_beta_avec_merveille(copie_partie, profondeur - 1, alpha, beta, True, nbr_noeuds)
			
			if evaluation < min_eval:
				min_eval = evaluation
				print(f"carte {carte.nom} : meilleur eval : {min_eval}")
				carte_a_sacrifier = carte
				
				beta = min(beta, evaluation)
				if beta <= alpha:
					break
					
		print(f"{Couleurs.WARNING}fin coup joueur{Couleurs.RESET}")
		return min_eval, carte_a_sacrifier, None, nbr_noeuds+1
