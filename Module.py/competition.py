"""Description : Simulation du gagnant potentiel et l'arbre de tout les match à chaque situation

Prérequis : Avoir effectuer la liste des qualifié dans ft.Qualif.team_qualifie(data)"""

from dataclasses import dataclass
import pandas as pd
from formatage import Qualif, Intro, Resume
import random
from math import *

@dataclass

class Tournement:
    
    def tirage_aleatoire(Qualifier : Qualif):
        """retourne une liste avec les équipes répartis aléatoirement"""
        equipe=[]
        for i in Qualifier.reset_index()["Equipe"]:
            equipe.append(i)
        list_random=[]

        while len(equipe)>0:
            selection = random.choice(equipe)
            equipe.remove(selection)
            list_random.append(selection)
        return list_random
    
    def But(Huitieme, data):
        """Créer deux colonnees but marqués et but pris."""
        But=pd.DataFrame()
        for i in Huitieme:
            Selec=data[data["equipe_1"]==i]
            Selec["But_marque"], Selec["But_pris"] = Selec["score"].str.split("-", 1).str
            Selec_bis=data[data["equipe_2"]==i]
            Selec_bis["But_pris"], Selec_bis["But_marque"] = Selec_bis["score"].str.split("-", 1).str
            Selec=Selec.append(Selec_bis)
            But=But.append(Selec)
            But["But_marque"]=But["But_marque"].astype(int)
            But["But_pris"]=But["But_pris"].astype(int)
        return But
    
     
    def poisson(k,m):
        """poisson(k,m): donne la probabilité d'avoir k évènements distribués selon une loi de Poisson de paramètre m"""
        p=e**(-m)
        for i in range(0,k):
            p*=m/k
            k-=1
        return p

    def poissoncum(k,m):
        """poissoncum(k,m): probabilité d'avoir k évènement(s) ou moins, dans une distribution de Poisson de paramètre m."""
        pk=e**(-m)
        p=pk
        for i in range(1,k+1):
            pk*=m/i
            p+=pk
        return p
    
    def Match_huit(Huitieme,data):
        """Renvois les probabilités cumulées de la loi de Poisson des matchs de huitièmes"""
        Bute = Tournement.But(Huitieme, data)
        Exterieur=Bute[(Bute.lieu!=Bute.equipe_1) & (Bute.lieu!=Bute.equipe_2)]
        
        team_1 = []
        team_2 = []
        Force_att=Exterieur["But_marque"].mean()
        Force_def=Exterieur["But_pris"].mean()
        for i in range(0,len(Huitieme),2):
        
            Force_att_1=Exterieur[(Exterieur["equipe_1"]==Huitieme[i]) | (
                Exterieur["equipe_2"]==Huitieme[i])]["But_marque"].mean()/Exterieur["But_marque"].mean()

            Force_att_2=Exterieur[(Exterieur["equipe_1"]==Huitieme[i+1]) | (
                Exterieur["equipe_2"]==Huitieme[i+1])]["But_marque"].mean()/Exterieur["But_marque"].mean()

            Force_def_1=Exterieur[(Exterieur["equipe_1"]==Huitieme[i]) | (
                Exterieur["equipe_2"]==Huitieme[i])]["But_pris"].mean()/Exterieur["But_pris"].mean()

            Force_def_2=Exterieur[(Exterieur["equipe_1"]==Huitieme[i+1]) | (
                Exterieur["equipe_2"]==Huitieme[i+1])]["But_pris"].mean()/Exterieur["But_pris"].mean()

            for j in range(0,6):
                k=j
                m=Force_att_1*Force_def_2*Force_att
                team_1.append(round(Tournement.poissoncum(k,m),3))
                m=Force_att_2*Force_def_1*Force_att
                team_2.append(round(Tournement.poissoncum(k,m),3))

        Butte=[]
        for i in range(0,6):
            Butte.append(i)
        Match_Huit=pd.DataFrame({"But" : Butte,
              Huitieme[0] : team_1[0:6],
             Huitieme[1]  : team_2[0:6],
             Huitieme[2]  : team_1[6:12],
             Huitieme[3]  : team_2[6:12],
             Huitieme[4]  : team_1[12:18],
             Huitieme[5]  : team_2[12:18],
             Huitieme[6]  : team_1[18:24],
             Huitieme[7]  : team_2[18:24],
             Huitieme[8]  : team_1[24:30],
             Huitieme[9]  : team_2[24:30],
             Huitieme[10]  : team_1[30:36],
             Huitieme[11]  : team_2[30:36],
             Huitieme[12]  : team_1[36:42],
             Huitieme[13]  : team_2[36:42],
             Huitieme[14]  : team_1[42:48],
             Huitieme[15]  : team_2[42:48]})
        return Match_Huit
    
    def Gagnant_Huitieme(Match_Huit):
        """Renvois la liste des gagnants des huitièmes de finale"""
        Quart=[]
        for i in range(1,len(Match_Huit.columns),2):
            select=Match_Huit.iloc[:,[i,i+1]]
            if select.where((select[select.columns[0]] <= select[select.columns[1]]
                            ) & (select[select.columns[1]] >= select[select.columns[0]])).isnull().values.any()==False:
                Quart.append(select.iloc[:,[0]].columns[0])
            elif select.where((select[select.columns[1]] <= select[select.columns[0]]
                            ) & (select[select.columns[0]] >= select[select.columns[1]])).isnull().values.any()==False:
                Quart.append(select.iloc[:,[1]].columns[0])
            else :
                print("Les équipes suivantes " + select.columns[0] + " et " + select.columns[1] + " mériterait d'être approfondie")
        return Quart
                
                #.where me sert a savoir dans quelle colonne de selec la probabilité est plus petite ou grande que l'autre
                #En cas d'égalité de probabilité on se penche dessus plus manuellement comme dit dans le else:
                
    def Match_quart(Quart,data,Huitieme):
        """Renvois les probabilités cumulées de la loi de Poisson des matchs de quart"""
        Bute = Tournement.But(Huitieme, data)
        Exterieur=Bute[(Bute.lieu!=Bute.equipe_1) & (Bute.lieu!=Bute.equipe_2)]
        
        team_1 = []
        team_2 = []
        Force_att=Exterieur["But_marque"].mean()
        Force_def=Exterieur["But_pris"].mean()
        
        for i in range(0,len(Quart),2):
            Force_att_1=Exterieur[(Exterieur["equipe_1"]==Quart[i]) | (
                Exterieur["equipe_2"]==Quart[i])]["But_marque"].mean()/Exterieur["But_marque"].mean()

            Force_att_2=Exterieur[(Exterieur["equipe_1"]==Quart[i+1]) | (
                Exterieur["equipe_2"]==Quart[i+1])]["But_marque"].mean()/Exterieur["But_marque"].mean()

            Force_def_1=Exterieur[(Exterieur["equipe_1"]==Quart[i]) | (
                Exterieur["equipe_2"]==Quart[i])]["But_pris"].mean()/Exterieur["But_pris"].mean()

            Force_def_2=Exterieur[(Exterieur["equipe_1"]==Quart[i+1]) | (
                Exterieur["equipe_2"]==Quart[i+1])]["But_pris"].mean()/Exterieur["But_pris"].mean()

            for j in range(0,6):
                k=j
                m=Force_att_1*Force_def_2*Force_att
                team_1.append(round(Tournement.poissoncum(k,m),3))
                m=Force_att_2*Force_def_1*Force_att
                team_2.append(round(Tournement.poissoncum(k,m),3))

        Butte=[]
        for i in range(0,6):
            Butte.append(i)    

        Match_Quart=pd.DataFrame({"But" : Butte,
                                  Quart[0] : team_1[0:6],
                                  Quart[1]  : team_2[0:6],
                                  Quart[2]  : team_1[6:12],
                                  Quart[3]  : team_2[6:12],
                                  Quart[4]  : team_1[12:18],
                                  Quart[5]  : team_2[12:18],
                                  Quart[6]  : team_1[18:24],
                                  Quart[7]  : team_2[18:24]})
        return Match_Quart
    
    def Gagnant_Quart(Match_Quart):
        """Renvois la liste des gagnants des quarts de finale"""
        Demi=[]
        for i in range(1,len(Match_Quart.columns),2):
            select=Match_Quart.iloc[:,[i,i+1]]
            if select.where((select[select.columns[0]] <= select[select.columns[1]]
                            ) & (select[select.columns[1]] >= select[select.columns[0]])).isnull().values.any()==False:
                Demi.append(select.iloc[:,[0]].columns[0])
            elif select.where((select[select.columns[1]] <= select[select.columns[0]]
                            ) & (select[select.columns[0]] >= select[select.columns[1]])).isnull().values.any()==False:
                Demi.append(select.iloc[:,[1]].columns[0])
            else :
                print("Les équipes suivantes " + select.columns[0] + " et " + select.columns[1] + " mériterait d'être approfondie")
        return Demi
    
    def Match_demi(Demi,data,Huitieme):
        """Renvois les probabilités cumulées de la loi de Poisson des matchs de demi"""
        Bute = Tournement.But(Huitieme, data)
        Exterieur=Bute[(Bute.lieu!=Bute.equipe_1) & (Bute.lieu!=Bute.equipe_2)]
        team_1 = []
        team_2 = []
        Force_att=Exterieur["But_marque"].mean()
        Force_def=Exterieur["But_pris"].mean()
        for i in range(0,len(Demi),2):
            Force_att_1=Exterieur[(Exterieur["equipe_1"]==Demi[i]) | (
                Exterieur["equipe_2"]==Demi[i])]["But_marque"].mean()/Exterieur["But_marque"].mean()

            Force_att_2=Exterieur[(Exterieur["equipe_1"]==Demi[i+1]) | (
                Exterieur["equipe_2"]==Demi[i+1])]["But_marque"].mean()/Exterieur["But_marque"].mean()

            Force_def_1=Exterieur[(Exterieur["equipe_1"]==Demi[i]) | (
                Exterieur["equipe_2"]==Demi[i])]["But_pris"].mean()/Exterieur["But_pris"].mean()

            Force_def_2=Exterieur[(Exterieur["equipe_1"]==Demi[i+1]) | (
                Exterieur["equipe_2"]==Demi[i+1])]["But_pris"].mean()/Exterieur["But_pris"].mean()

            for j in range(0,6):
                k=j
                m=Force_att_1*Force_def_2*Force_att
                team_1.append(round(Tournement.poissoncum(k,m),3))
                m=Force_att_2*Force_def_1*Force_att
                team_2.append(round(Tournement.poissoncum(k,m),3))

        Butte=[]
        for i in range(0,6):
            Butte.append(i)  
        Match_Demi=pd.DataFrame({"But" : Butte,
                      Demi[0] : team_1[0:6],
                     Demi[1]  : team_2[0:6],
                     Demi[2]  : team_1[6:12],
                     Demi[3]  : team_2[6:12]})
        
        return Match_Demi
    
    def Gagnant_Demi(Match_Demi):
        """Renvois les finalistes"""
        Finalistes=[]
        for i in range(1,len(Match_Demi.columns),2):
            select=Match_Demi.iloc[:,[i,i+1]]
            if select.where((select[select.columns[0]] <= select[select.columns[1]]
                            ) & (select[select.columns[1]] >= select[select.columns[0]])).isnull().values.any()==False:
                Finalistes.append(select.iloc[:,[0]].columns[0])
            elif select.where((select[select.columns[1]] <= select[select.columns[0]]
                            ) & (select[select.columns[0]] >= select[select.columns[1]])).isnull().values.any()==False:
                Finalistes.append(select.iloc[:,[1]].columns[0])
            else :
                print("Les équipes suivantes " + select.columns[0] + " et " + select.columns[1] + " mériterait d'être approfondie")
        return Finalistes
                
    def Match_final(Finalistes,data,Huitieme):
        """Renvois les probabilités cumulées de la loi de Poisson des matchs de finale"""
        Bute = Tournement.But(Huitieme, data)
        Exterieur=Bute[(Bute.lieu!=Bute.equipe_1) & (Bute.lieu!=Bute.equipe_2)]
        team_1 = []
        team_2 = []
        Force_att=Exterieur["But_marque"].mean()
        Force_def=Exterieur["But_pris"].mean()
        for i in range(0,len(Finalistes),2):
            Force_att_1=Exterieur[(Exterieur["equipe_1"]==Finalistes[i]) | (
                Exterieur["equipe_2"]==Finalistes[i])]["But_marque"].mean()/Exterieur["But_marque"].mean()

            Force_att_2=Exterieur[(Exterieur["equipe_1"]==Finalistes[i+1]) | (
                Exterieur["equipe_2"]==Finalistes[i+1])]["But_marque"].mean()/Exterieur["But_marque"].mean()

            Force_def_1=Exterieur[(Exterieur["equipe_1"]==Finalistes[i]) | (
                Exterieur["equipe_2"]==Finalistes[i])]["But_pris"].mean()/Exterieur["But_pris"].mean()

            Force_def_2=Exterieur[(Exterieur["equipe_1"]==Finalistes[i+1]) | (
                Exterieur["equipe_2"]==Finalistes[i+1])]["But_pris"].mean()/Exterieur["But_pris"].mean()

            for j in range(0,6):
                k=j
                m=Force_att_1*Force_def_2*Force_att
                team_1.append(round(Tournement.poissoncum(k,m),3))
                m=Force_att_2*Force_def_1*Force_att
                team_2.append(round(Tournement.poissoncum(k,m),3))

        Butte=[]
        for i in range(0,6):
            Butte.append(i)  

        Match_Finalistes=pd.DataFrame({"But" : Butte,
                      Finalistes[0] : team_1[0:6],
                     Finalistes[1]  : team_2[0:6]})
        return Match_Finalistes
    
    def Gagnant_CoupeDuMonde_2022(Match_Finalistes):
        """Renvois le gagnant prédit"""
        
        Gagnant=[]
        for i in range(1,len(Match_Finalistes.columns),2):
            select=Match_Finalistes.iloc[:,[i,i+1]]
            if select.where((select[select.columns[0]] <= select[select.columns[1]]
                            ) & (select[select.columns[1]] >= select[select.columns[0]])).isnull().values.any()==False:
                Gagnant.append(select.iloc[:,[0]].columns[0])
            elif select.where((select[select.columns[1]] <= select[select.columns[0]]
                            ) & (select[select.columns[0]] >= select[select.columns[1]])).isnull().values.any()==False:
                Gagnant.append(select.iloc[:,[1]].columns[0])
            else :
                print("Les équipes suivantes " + select.columns[0] + " et " + select.columns[1] + " mériterait d'être approfondie")
        return "La phase finale se déroule entre : " + Match_Finalistes.columns[2] + " et " + Match_Finalistes.columns[1] + ", le gagnant est " + Gagnant[0] + "."
    
    def Gagnant_troisieme(Demi,Finalistes,Huitieme,data):
        """Renvois le gagnant du match de classement"""
        Classement= []
        for i in Demi:
            if i not in Finalistes:
                Classement.append(i)

        Bute = Tournement.But(Huitieme, data)
        Exterieur=Bute[(Bute.lieu!=Bute.equipe_1) & (Bute.lieu!=Bute.equipe_2)]
        team_1 = []
        team_2 = []
        Force_att=Exterieur["But_marque"].mean()
        Force_def=Exterieur["But_pris"].mean()
        for i in range(0,len(Classement),2):
            Force_att_1=Exterieur[(Exterieur["equipe_1"]==Classement[i]) | (
                Exterieur["equipe_2"]==Classement[i])]["But_marque"].mean()/Exterieur["But_marque"].mean()

            Force_att_2=Exterieur[(Exterieur["equipe_1"]==Classement[i+1]) | (
                Exterieur["equipe_2"]==Classement[i+1])]["But_marque"].mean()/Exterieur["But_marque"].mean()

            Force_def_1=Exterieur[(Exterieur["equipe_1"]==Classement[i]) | (
                Exterieur["equipe_2"]==Classement[i])]["But_pris"].mean()/Exterieur["But_pris"].mean()

            Force_def_2=Exterieur[(Exterieur["equipe_1"]==Classement[i+1]) | (
                Exterieur["equipe_2"]==Classement[i+1])]["But_pris"].mean()/Exterieur["But_pris"].mean()

            for j in range(0,6):
                k=j
                m=Force_att_1*Force_def_2*Force_att
                team_1.append(round(Tournement.poissoncum(k,m),3))
                m=Force_att_2*Force_def_1*Force_att
                team_2.append(round(Tournement.poissoncum(k,m),3))

        Butte=[]
        for i in range(0,6):
            Butte.append(i)  

        Match_Classement=pd.DataFrame({"But" : Butte,
                      Classement[0] : team_1[0:6],
                     Classement[1]  : team_2[0:6]})

        Troisieme=[]
        for i in range(1,len(Match_Classement.columns),2):
            select=Match_Classement.iloc[:,[i,i+1]]
            if select.where((select[select.columns[0]] <= select[select.columns[1]]
                            ) & (select[select.columns[1]] >= select[select.columns[0]])).isnull().values.any()==False:
                Troisieme.append(select.iloc[:,[0]].columns[0])
            elif select.where((select[select.columns[1]] <= select[select.columns[0]]
                            ) & (select[select.columns[0]] >= select[select.columns[1]])).isnull().values.any()==False:
                Troisieme.append(select.iloc[:,[1]].columns[0])
            else :
                print("Les équipes suivantes " + select.columns[0] + " et " + select.columns[1] + " mériterait d'être approfondie")
        return "La troisième place se joue entre " + Match_Classement.columns[1] + " et " + Match_Classement.columns[2] + " le troisième est donc : " + Troisieme[0] + "."