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
	return (partie.age == 3 and len(partie.cartes_plateau) == 0) \
		or (partie.joueur1.nombre_symb_scientifique == 6 or partie.joueur2.nombre_symb_scientifique == 6) \
		or (partie.position_jeton_conflit == 18 or partie.position_jeton_conflit == 0)
	
	
def fonction_evaluation(partie):
	evaluation = 0
	for carte in partie.joueur2.cartes:
		evaluation += eval_carte[carte.nom]
	
	for carte in partie.joueur1.cartes:
		evaluation -= eval_carte[carte.nom]
		
	evaluation -= 2*(9 - partie.position_jeton_conflit)
	
	evaluation += partie.joueur2.monnaie
	evaluation -= partie.joueur1.monnaie
	
	evaluation += 2*partie.joueur2.nombre_symb_scientifique
	evaluation -= 2*partie.joueur1.nombre_symb_scientifique
	
	evaluation += partie.joueur2.points_victoire
	evaluation -= partie.joueur1.points_victoire
	
	return evaluation


def minimax(partie, profondeur, coup_joueur):
	if profondeur == 0 or partie_fini(partie):
		return fonction_evaluation(partie)
	
	if coup_joueur:
		maxEval = -math.inf
		for carte in partie.liste_cartes_prenables():
			copie_partie = partie
			copie_partie.jouer_coup_carte(carte)
			eval = minimax(copie_partie, profondeur - 1, False)
			maxEval = max(maxEval, eval)
		return maxEval
	
	else:
		minEval = math.inf
		for carte in partie.liste_cartes_prenables():
			copie_partie = partie
			copie_partie.jouer_coup_carte(carte)
			eval = minimax(copie_partie, profondeur - 1, True)
			minEval = min(minEval, eval)
		return minEval
		