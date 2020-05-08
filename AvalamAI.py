import cherrypy
import sys
from random import choice
import random

class Server:
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    
    def move(self):
        # Deal with CORS
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        cherrypy.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        cherrypy.response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        if cherrypy.request.method == "OPTIONS":
            return ''
            
        #Messages affichés 
        messages = ["omae wa mou shindeiru"," La roue tourne tkt"," Tu comptais vraiment me battre avec ça ?","Tu veux des lunettes ?","Nani ?!","Noob","On ne compare pas une F1 à un Karting","ԅ(≖‿≖ԅ)","(ง’̀-‘́)ง","Je t'aimais Anakin..."]
        w = random.choice(messages)
        self.body = cherrypy.request.json
        return {"move":self.MonIA, "message": w}

#Fonction permettant d'identifier les joueurs à partir du body
    @property
    def identifier_joueur(self): 
        if self.body["players"][0] == self.body["you"]:
            self.joueur = 0 
            self.adversaire = 1
        else:
            self.joueur = 1
            self.adversaire = 0
        return self.joueur

#Fonction qui détermine tous les mouvements possibles.
    @property
    def coup_possible(self):
            mouv_possibles=[]
            mouv_interdits = []
            bons_mouvs = []
            for lignes in range(9):
                for colonnes in range(9):
                    if len(self.body["game"][lignes][colonnes]) != 0:
                        # Carré centrale du game
                        for elem in self.body["game"][lignes][colonnes]:
                            if 0<colonnes<8 and 0<lignes<8:
                                for i in range(-1,2):
                                    for v in range(-1,2):
                                        mouv_possibles.append({"from" : [lignes,colonnes], "to" :[lignes +i,colonnes+v]}) 
                            #Exceptions cadre du game
                            if 0<lignes<8 and colonnes==0:							
                                for v in range(0,2):
                                    for i in range(-1,2):
                                        mouv_possibles.append({"from" : [lignes,colonnes], "to" :[lignes +i,colonnes+v]}) 
                            if 0<lignes<8 and colonnes==8:
                                for v in range(-1,1):
                                    for i in range(-1,2):
                                        mouv_possibles.append({"from" : [lignes,colonnes], "to" :[lignes +i,colonnes+v]})
                            if lignes == 0 and 0<colonnes<8:
                                for v in range (-1,2):
                                    for i in range(0,2):
                                        mouv_possibles.append({"from" : [lignes,colonnes], "to" :[lignes +i,colonnes+v]}) 
                            if lignes == 8 and 0<colonnes<8:    
                                for v in range (-1,2):
                                    for i in range(-1,1):
                                        mouv_possibles.append({"from" : [lignes,colonnes], "to" :[lignes +i,colonnes+v]}) 

                            #Exceptions des cases des coins
                            if lignes == 0 and colonnes == 0:
                                for v in range(0,2):
                                    for i in range(0,2):
                                        mouv_possibles.append({"from" : [lignes,colonnes], "to" :[lignes +i,colonnes+v]}) 
                            if lignes == 0 and colonnes == 8:
                                for v in range(-1,1):
                                    for i in range(0,2):
                                        mouv_possibles.append({"from" : [lignes,colonnes], "to" :[lignes +i,colonnes+v]}) 
                            if lignes == 8 and colonnes == 0:
                                for v in range(0,2):
                                    for i in range(-1,1):
                                        mouv_possibles.append({"from" : [lignes,colonnes], "to" :[lignes +i,colonnes+v]}) 
                            if lignes == 8 and colonnes == 8:
                                for v in range(-1,1):
                                    for i in range(-1,1):
                                        mouv_possibles.append({"from" : [lignes,colonnes], "to" :[lignes +i,colonnes+v]})

            #Boucle permettant d'obtenir les coordonées de chaque mouvement pour récuperer les bons mouvements                         
            for elem in mouv_possibles:
                A= elem.get("from")
                B= elem.get("to")
                a1=A[0]
                a2=A[1]
                b1=B[0]
                b2=B[1]
                fromvaleur= self.body["game"][a1][a2]
                tovaleur= self.body["game"][b1][b2]
                if self.mouvementsInterdits(fromvaleur,tovaleur,A,B) == "no":
                    mouv_interdits.append(elem)
                elif self.mouvementsInterdits(fromvaleur,tovaleur,A,B) == "yes":
                    bons_mouvs.append(elem)
            return bons_mouvs

# Fonction qui détermine les mouvements interdits
    def mouvementsInterdits(self,x,y,A,B):
        a=len(x)
        b=len(y)
        if a + b > 5:	
            return "no"
        if a == 0:
            return "no"
        if b == 0:
            return "no"
        if A == B:
            return"no"
        else:
            return "yes"
# Fonction qui détermine les meilleurs mouvements parmi les bons mouvements
    @property
    def meilleursmouvements(self):
        meilleurs_mouvements = []
        for elem in self.coup_possible:
            A= elem.get("from")
            B= elem.get("to")
            a1=A[0]
            a2=A[1]
            b1=B[0]
            b2=B[1]
            fromvaleur= self.body["game"][a1][a2]
            tovaleur= self.body["game"][b1][b2]

            # Stratégie 1 
            i = len(fromvaleur)-1
            if fromvaleur[i]== self.identifier_joueur: 
                if len(fromvaleur)+len(tovaleur)== 5:
                    meilleurs_mouvements.append(elem)
        return meilleurs_mouvements

    # Fonction IA qui choisit quelle liste renvoyer
    @property
    def MonIA(self):
        if len(self.meilleursmouvements) != 0: 
            return random.choice(self.meilleursmouvements)
        else:
            return random.choice(self.coup_possible)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port=int(sys.argv[1])
    else:
        port=5031

    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': port})
    cherrypy.quickstart(Server())
