# Avalam IA

Fait par :

Sohaib El Amiri Charif 17049
Achrafe Ben Ammi 17190

# Libraries utilisées 

- cherrypy
- sys
- random

# Stratégie 

Le IA calcule tous les mouvements possibles, ensuite supprime les badmoves en laissant que les good moves. Le IA créé une liste de best moves parmi les good moves et choisi le meilleur coup à lancer. Si le nombre de tours du From + le nombre de tours du To est exactement 5, alors le IA priorise ce mouvement.

# Inscription 

Il faut envoyer le JSON suivant au port TCP 3001 du serveur:

{
	"matricules": ["17049", "17190"],
	"port": 5031,
	"name": "AvalamCiIA"
}