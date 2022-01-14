"""Nettoyage et manipulation de colonne de DataFrame 

Prérequis : Avoir les DataFrame de formatage.py"""
from formatage import Resume, Intro
from competition import Tournement
from dataclasses import dataclass
import pandas as pd

@dataclass

class Fixe:
    def fixe_annee(data : Resume, an : Intro):
        """remplace par les vrais valeures annees"""
        for i in zip(data["Annee"].unique(),an):
            data["Annee"]=data["Annee"].replace(i[0],i[1])

        
    def enleve_n(data):
        """Enleve les \n"""
        data["equipe_1"]=data["equipe_1"].str.strip()
        data["equipe_2"]=data["equipe_2"].str.strip()
        data["score"]=data["score"].str.strip()
        data["affluence"]=data["affluence"].str.strip()
        data["lieu"]=data["lieu"].str.strip()
        
        """Enleve une ligne inutile et réindexe le dataframe"""
        data.reset_index(inplace=True)
        del data["index"]
        data.drop(869,0,inplace=True)
        data.reset_index(inplace=True)
        del data["index"]
        data.to_csv('Final.csv',sep=';',index=False)

    
    def fixe_manque(data):
        """injecte les lignes manquantes qui ne figure pas sur le site"""
        manque = pd.DataFrame([ ('', "Autriche", "Etat-Unis",'2-1', "37857", 1990),
                    ('', "Argentine", "Bosnie",'2-1', "74738 ", 2014),
             ('', "Iran", "Nigeria",'0-0', "39081", 2014),
                    ('', "Argentine", "Iran",'1-0', "57698", 2014),
                    ('', "Nigeria", "Bosnie",'1-0', "40499", 2014),
                    ('', "Nigeria", "Argentine",'2-3', "43285", 2014),
                    ('', "Bosnie", "Iran",'3-1', "48011", 2014),
                    ('', "Allemagne", "Portugal",'4-0', "51081", 2014),
                    ('', "Ghana", "Etat-Unis",'1-2', "39760", 2014),
                    ('', "Allemagne", "Ghana",'2-2', "59621", 2014),
                    ('', "Etat-Unis", "Portugal",'2-2', "40123", 2014),
                    ('', "Etat-Unis", "Allemagne",'0-1', "41876", 2014),
                    ('', "Portugal", "Ghana",'2-1', "67540", 2014),
                    ('', "Belgique", "Algerie",'2-1', "56800", 2014),
                    ('', "Russie", "Coree du Sud",'1-1', "37603", 2014),
                    ('', "Belgique", "Russie",'1-0', "73819", 2014),
                    ('', "Coree du Sud", "Algerie",'2-4', "42732", 2014),
                    ('', "Coree du Sud", "Belgique",'0-1', "61397", 2014),
                    ('', "Algérie", "Russie",'1-1', "39311", 2014)], 
             columns = ['lieu' , 'equipe_1', 'equipe_2','score','affluence','Annee'])
        data=manque.append(data)
        """Enleve les accents"""
        data["equipe_1"]=data["equipe_1"].str.replace("é",'e')
        data["equipe_2"]=data["equipe_2"].str.replace("é",'e')
        
    def fixe_situation(data):
        """met les situations dans le dataframe"""
        
        """Cas à part"""
        cdm1930=data[data["Annee"]==1930]
        cdm1930["Situation"]=""
        cdm1930["Situation"][0:15]= cdm1930["Situation"][0:15].replace("","Poule")
        cdm1930["Situation"][15:17]= cdm1930["Situation"][15:17].replace("","1/2F")
        cdm1930["Situation"][17]= cdm1930["Situation"][17].replace("","Finale")

        cdm1934=data[data["Annee"]==1934]
        cdm1934["Situation"]=0
        cdm1934["Situation"][0:8]="1/8F"
        cdm1934["Situation"][8:12]="1/4F"
        cdm1934["Situation"][12:14]="1/2F"
        cdm1934["Situation"][32]="Troisieme"
        cdm1934["Situation"][33]="Finale"

        cdm1938=data[data["Annee"]==1938]
        cdm1938["Situation"]=0
        cdm1938["Situation"][0:9]="1/8F"
        cdm1938["Situation"][9:13]="1/4F"
        cdm1938["Situation"][13:15]="1/2F"
        cdm1938["Situation"][49]="Troisieme"
        cdm1938["Situation"][50]="Finale"

        cdm1950=data[data["Annee"]==1950]
        cdm1950["Situation"]=0
        cdm1950["Situation"][0:16]="Poule"
        cdm1950["Situation"][16:22]="1/2F"
        cdm1950["Situation"][73]="Finale"


        cdm1954=data[data["Annee"]==1954]
        cdm1954["Situation"]=0
        cdm1954["Situation"][0:18]="Poule"
        cdm1954["Situation"][18:22]="1/4F"
        cdm1954["Situation"][22:24]="1/2F"
        cdm1954["Situation"][98]="Troisieme"
        cdm1954["Situation"][99]="Finale"


        cdm1958=data[data["Annee"]==1958]
        cdm1958["Situation"]=0
        cdm1958["Situation"][0:27]="Poule"
        cdm1958["Situation"][27:31]="1/4F"
        cdm1958["Situation"][31:33]="1/2F"
        cdm1958["Situation"][132]="Troisieme"
        cdm1958["Situation"][133]="Finale"


        cdm1974=data[data["Annee"]==1974]
        cdm1974["Situation"]=0
        cdm1974["Situation"][0:24]="Poule"
        cdm1974["Situation"][24:36]="1/8F"
        cdm1974["Situation"][266]="Troisieme"
        cdm1974["Situation"][267]="Finale"


        cdm1978=data[data["Annee"]==1978]
        cdm1978["Situation"]=0
        cdm1978["Situation"][0:24]="Poule"
        cdm1978["Situation"][24:36]="1/8F"
        cdm1978["Situation"][304]="Troisieme"
        cdm1978["Situation"][305]="Finale"


        cdm1982=data[data["Annee"]==1982]
        cdm1982["Situation"]=0
        cdm1982["Situation"][0:36]="Poule"
        cdm1982["Situation"][36:48]="1/8F"
        cdm1982["Situation"][48:50]="1/2F"
        cdm1982["Situation"][357]="Troisieme"
        cdm1982["Situation"][358]="Finale"

        
        """de 1962 à 1970"""
        cdm62_70=pd.DataFrame()
        good62_70=pd.DataFrame()
        for i in range(1962,1974,4):
            cdm62_70=cdm62_70.append(data[data["Annee"]==i])
        cdm62_70["Situation"]=""
        for i in range(1962,1974,4):
            selec=cdm62_70[cdm62_70["Annee"]==i]
            nb_equipe=list(selec["equipe_1"].unique())
            for x in selec["equipe_2"].unique():
                if x not in selec["equipe_1"].unique():
                    nb_equipe.append(x)
            nb_groupe=int(len(nb_equipe)/4)
            row_poul=nb_groupe*6
            selec["Situation"][0:row_poul]="Poule"
            selec["Situation"][row_poul:int(row_poul+4)]="1/4F"
            selec["Situation"][int(row_poul+4):int(row_poul+4+2)]="1/2F"
            selec["Situation"][len(selec)-2:len(selec)]=["Troisieme","Finale"]
            good62_70=good62_70.append(selec)

        """De 1986 à 2018"""
        cdm86_2018=pd.DataFrame()
        good=pd.DataFrame()
        for i in range(1986,2022,4):
            cdm86_2018=cdm86_2018.append(data[data["Annee"]==i])
        cdm86_2018["Situation"]=""
        for i in range(1986,2022,4):
            selec=cdm86_2018[cdm86_2018["Annee"]==i]
            nb_equipe=list(selec["equipe_1"].unique())
            for x in selec["equipe_2"].unique():
                if x not in selec["equipe_1"].unique():
                    nb_equipe.append(x)
            nb_groupe=int(len(nb_equipe)/4)
            row_poul=nb_groupe*6
            selec["Situation"][0:row_poul]="Poule"
            selec["Situation"][row_poul:int(row_poul+8)]="1/8F"
            selec["Situation"][int(row_poul+8):int(row_poul+8+4)]="1/4F"
            selec["Situation"][int(row_poul+8+4):int(row_poul+8+4+2)]="1/2F"
            selec["Situation"][len(selec)-2:len(selec)]=["Troisieme","Finale"]
            good=good.append(selec)
            
            data = cdm1930.append([cdm1934,cdm1938,cdm1950,cdm1954,cdm1958,good62_70,cdm1974,cdm1978,cdm1982,good])
        return data
        
    def fixe_lieu(data):
        """insère le pays organisateur dans le colonne lieu"""
        
        Organisateur = ["Uruguay","Italie","France","Bresil","Suisse","Suede",
                        "Chili","Angleterre","Mexique","Allemagne","Argentine",
                        "Espagne","Mexique","Italie","Etat-Unis","France","Coree du Sud",
                        "Allemagne","Afrique du Sud","Bresil","Russie"]

        for i in zip(Organisateur,data["Annee"].unique()):
            data.loc[data.Annee==i[1],"lieu"]=i[0]
        """Enleve les lignes ou l'affluence est nulle et converti la colonne affluence en nombre"""
        data.drop(data[data["affluence"]==""].index, inplace=True)
        data.reset_index(inplace=True)
        del data["index"]
        data["affluence"]=data["affluence"].astype(int)
        return data
    
    def fixe_ratio_dummies(Huitieme, data):
        """fixe le ratio d'affluence par année et transforme les variable catégorielles en variable dummies"""
        Bute = Tournement.But(Huitieme, data)
        Exterieur=Bute[(Bute.lieu!=Bute.equipe_1) & (Bute.lieu!=Bute.equipe_2)]
        ratio=pd.DataFrame(Exterieur.groupby(["Annee"])["affluence"].max()/Exterieur["affluence"].max()).reset_index()
        ratio.rename(columns={'affluence': 'Ratio'}, inplace=True)
        df=pd.merge(Exterieur,ratio,on="Annee", how="left")
        df.rename(columns={'affluence_x': 'affluence'}, inplace=True)
        df.rename(columns={'affluence_y': 'Ratio'}, inplace=True)
        df["equipe_2"]=df["equipe_2"].str.replace("RDA",'Allemagne')
        df["Annee"]=df["Annee"].astype(str)
        df_final = pd.get_dummies(df[["equipe_1","equipe_2",
                   "affluence","Annee","Situation"]], prefix=['Team1', 'Team2',"Year","Pos"])
        return df_final
