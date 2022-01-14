""" Prise des stockage backup afin de les mettre sous forme de DataFrame


Prérequis : Avoir les backups stocké issus de scrapping.py"""

# Extraction des informations voulues
# sous forme structurée

from bs4 import BeautifulSoup as BS
from dataclasses import dataclass
import pandas as pd
import numpy as np

@dataclass
class Intro:
    
    def annee(Debut,Fin):
        """sert à avoir toutes les annees de coupe du monde en excluant les exeptions"""
        an=[]
        for i in range(Debut,Fin+4,4):
            an.append(i)
        #Enleve les annees ou les cdm n'ont pas été présente
        if 1942 in an:
            an.remove(1942)
        if 1946 in an:
            an.remove(1946)
        return an


    def all_coupe(Debut,Fin):
        """Sert à avoir tout le code des coupes en une seule liste"""
        ann = Intro.annee(Debut,Fin)
        if Debut < 1930:
            raise ValueError("Le début des coupes du monde commence en 1930 donc l'année "+ str(Debut) + " est impossible.")
        Code_cdm = []
        for annee in ann:
            with open("backup"+str(annee)+".html", "r",encoding="utf8") as fichier:
                Code_cdm.append(fichier.read())
        return Code_cdm

@dataclass
class Resume:
    
    lieu : str
    equipe_1: str
    equipe_2 : str
    score : str
    affluence : str
    Annee : int
    
    def data(code : Intro):
        """Renvoie un dataframe des données de coupe du monde stocké en backup"""
        Final = pd.DataFrame()
        for annee in range(0,len(code)):
            test = pd.DataFrame()
            """selection de l'annee de la cdm"""
            resultat = list()
            soupe_all=BS(code[annee])
            code_tableau_all = soupe_all.find_all(attrs={"class" : "coupe"})
            """me prend tout le tableau de la page des matchs"""
            for i in code_tableau_all[0].find_all(attrs={"class" : "classement"}):
                """retait des tableau de classement en poule"""
                if len(i)>=1:
                    i.decompose()
            for i in code_tableau_all[0].find_all(attrs={"class" : "titre"}):
                """retait des titre de tableau"""
                situation = i.text
                if len(i)>=1:
                    i.decompose()
            for y in code_tableau_all[0].find_all("th"):
                """retait du noms des variables"""
                if len(y)>=1:
                    y.decompose()
            for i in code_tableau_all[0].find_all("td"):
                """retait de balises inutiles"""
                if i.text=="\n\n":
                    i.decompose()    
            for index in range(0,len(code_tableau_all[0].find_all("td")),5):
                """création du df"""
                lieu=code_tableau_all[0].find_all("td")[index]
                equipe_1=code_tableau_all[0].find_all("td")[index+1]
                equipe_2=code_tableau_all[0].find_all("td")[index+2]
                score=code_tableau_all[0].find_all("td")[index+3]
                affluence=code_tableau_all[0].find_all("td")[index+4]
                Annee = annee
                lieu = lieu.text
                equipe_1 = equipe_1.text
                equipe_2 = equipe_2.text
                score = score.text
                affluence = affluence.text
                resultat.append(
                Resume(
                        lieu, equipe_1,equipe_2,score,affluence, Annee
                    )
                )
            Final=Final.append(pd.DataFrame(resultat))
        return Final
    

# Extraction des informations voulues
# sous forme structurée
@dataclass
class Qualif:
    
    Position : str
    Equipe : str
    Trou : str
    Pts : int
    Match : int
    Gagne : int
    Nul : int
    Perdu : int
    Po : int
    Ca : int
    Diff : int
    
    
    
    
    def team_qualifie(data):
        """Créer le dataframe des pays qualifié en tenant compte des places des continents"""
        
        continent = ["europe","afrique","amerique_sud","asie","ame_nord"]
        for i in continent:
            Qualif_Cont = pd.DataFrame()
            qualification_cont=list()
            with open("backup_qualification_" + i + ".html" , "r", encoding="utf8") as fichier:
                code_continent=fichier.read()
                code_cont = BS(code_continent)
                for index in range(0,len(code_cont.find_all("td")),11):
                    """création du df"""
                    position=code_cont.find_all("td")[index]
                    equipe=code_cont.find_all("td")[index+1]
                    trou=code_cont.find_all("td")[index+2]
                    pts=code_cont.find_all("td")[index+3]
                    match=code_cont.find_all("td")[index+4]
                    gagne=code_cont.find_all("td")[index+5]
                    nul=code_cont.find_all("td")[index+6]
                    perdu=code_cont.find_all("td")[index+7]
                    po=code_cont.find_all("td")[index+8]
                    ca=code_cont.find_all("td")[index+9]
                    diff=code_cont.find_all("td")[index+10]

                    Position = position.text.strip()
                    Equipe = equipe.text.strip()
                    Trou = trou.text
                    Pts = int(pts.text)
                    Match = int(match.text)
                    Gagne = int(gagne.text)
                    Nul = int(nul.text)
                    Perdu = int(perdu.text)
                    Po = int(po.text)
                    Ca = int(ca.text)
                    Diff = int(diff.text)

                    qualification_cont.append(
                        Qualif(
                            Position, Equipe, Trou, Pts, Match, Gagne, Nul, Perdu, Po, Ca, Diff,
                        )
                    )

                Qualif_Cont=Qualif_Cont.append(qualification_cont)
                Qualif_Cont["Ratio"]=Qualif_Cont["Pts"]/Qualif_Cont["Match"]
                
                if i=="europe":
                    Europe = Qualif_Cont[Qualif_Cont["Position"]=="1"].append(Qualif_Cont[
                        Qualif_Cont["Position"]=="2"].sort_values(by=['Ratio'],ascending = False).head(3))
                elif i=="afrique":
                    Afrique = Qualif_Cont[Qualif_Cont["Position"]=="1"].sort_values(by="Pts",ascending=False).head(5)
                elif i=="amerique_sud":
                    Amerique_du_Sud=Qualif_Cont.head(5)
                elif i=="asie":
                    Asie_Oce=Qualif_Cont.sort_values(by="Ratio",ascending=False).head(6)
                else:
                    Amerique_du_Nord=Qualif_Cont.sort_values(by="Pts",ascending=False).head(3)
                    
        Qualifier=Europe["Equipe"].append(Amerique_du_Nord["Equipe"])
        Qualifier=Qualifier.append(Amerique_du_Sud["Equipe"])
        Qualifier=Qualifier.append(Asie_Oce["Equipe"])
        Qualifier=Qualifier.append(Afrique["Equipe"])
                
        return Qualifier
