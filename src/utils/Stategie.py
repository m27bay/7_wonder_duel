import math

from src.utils.Plateau import Plateau


eval_carte = {
	"chantier": 20,
	"exploitation": 16,
	"bassin argileux": 20,
	"cavite": 16,
	"gisement": 20,
	"mine": 16,
	"verrerie": 16,
	"presse": 16,
	"tour de garde": 12,
	"atelier": 12,
	"apothicaire": 12,
	"depot de pierre": 16,
	"depot d argile": 16,
	"depot de bois": 16,
	"ecurie": 13,
	"caserne": 13,
	"palissade": 13,
	"scriptorium": 13,
	"officine": 13,
	"theatre": 6,
	"autel": 6,
	"bains": 7,
	"taverne": 19,
	"scierie": 16,
	"briqueterie": 16,
	"carriere": 16,
	"soufflerie": 20,
	"sechoir": 20,
	"muraille": 14,
	"forum": 5,
	"caravanserail": 5,
	"douane": 6,
	"tribunal": 5,
	"haras": 14,
	"baraquements": 14,
	"champs de tir": 15,
	"place d armes": 15,
	"bibliotheque": 13,
	"dispensaire": 13,
	"ecole": 12,
	"laboratoire": 12,
	"statue": 13,
	"temple": 13,
	"aqueduc": 12,
	"rostres": 13,
	"brasserie": 20,
	"arsenal": 17,
	"pretoire": 17,
	"academie": 12,
	"etude": 12,
	"chambre de commerce": 15,
	"port": 16,
	"armurerie": 16,
	"palace": 15,
	"hotel de ville": 14,
	"obelisque": 13,
	"fortifications": 15,
	"atelier de siege": 15,
	"cirque": 15,
	"universite": 12,
	"observatoire": 12,
	"jardins": 14,
	"pantheon": 14,
	"senat": 13,
	"phare": 11,
	"arene": 11
}


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
			evaluation_j2 += eval_carte[carte.nom]
	
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
			evaluation_j1 += eval_carte[carte.nom]
		
	if partie.age != 1:
		evaluation_j1 += 2*partie.joueur1.nbr_symb_scientifique_diff
		evaluation_j1 += partie.joueur1.points_victoire
		if partie.position_jeton_conflit > 9:
			evaluation_j1 += 2 * (partie.position_jeton_conflit - 9)
	
	print(f"evaluation_j2 : {evaluation_j2}, evaluation_j1 : {evaluation_j1}")
	return evaluation_j2 - evaluation_j1


def minimax(partie, profondeur, coup_bot, nbr_noeuds):
	if profondeur == 0 or partie_fini(partie):
		return fonction_evaluation(partie), None, nbr_noeuds+1
	
	carte_a_prendre = None
	
	if coup_bot:
		partie.joueur_qui_joue = partie.joueur2
		print("j2")
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
			print(f"evaluation : {evaluation}, carte : {carte}")
			
			if evaluation > max_eval:
				max_eval = evaluation
				carte_a_prendre = carte
				
		return max_eval, carte_a_prendre, nbr_noeuds+1
	
	else:
		partie.joueur_qui_joue = partie.joueur1
		print("j1")
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
			print(f"evaluation : {evaluation}, carte : {carte}")
			
			if evaluation < min_eval:
				min_eval = evaluation
				carte_a_prendre = carte
		
		return min_eval, carte_a_prendre, nbr_noeuds+1
		