"""Description.

Fichier contenant l'essentiel des fonctions au machine learning.

Prérequis : Avoir la base de données finale propre.

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.dummy import DummyRegressor
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score, ShuffleSplit
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import learning_curve
from competition import Tournement


def prepare_donnees(X, y):
    """Sépare les données en un groupe d'entraînement et en un groupe de test avec la proportion suivante 80/20."""
    scaler = MinMaxScaler()
    #vars_num = ['Ratio']
    #X[vars_num] = scaler.fit_transform(X[vars_num])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    """test_size = le % de taille de l'echantillon test"""
    return X_train, X_test, y_train, y_test


def trouve_meilleur_modele(X_train, y_train):
    """Trouve le meilleur modèle parmi plusieurs modèles et selon plusieurs paramètres."""
    modeles = {
        'DummyRegressor': {
            'model': DummyRegressor(),
            'params': {
                'strategy': ["mean", "median", "quantile", "constant"]
            }
        },
        'Linear Regression': {
            'model': LinearRegression(),
            'params': {
                'fit_intercept': [True, False] 
                #prend une valeur booléenne qui calcule l’interception  si elle est mise à la valeur True, sinon elle prend la valeur zéro. Ce paramètre prend True par défaut."""
            }
        },
        #Modele lineraire sur un param précis"""
        'Lasso': {
            'model': Lasso(),
            'params': {
                'fit_intercept': [True, False],
                'alpha': [0.01, 0.1, 1., 10.],
                'max_iter': [1000,3000,5000,10000],
            }
        },#modele avec solver, utilisant d'autre méthodes de moindre carré"""
        'Ridge': {
            'model': Ridge(),
            'params': {
                'fit_intercept': [True, False],
                'alpha': [0.01, 0.1, 1., 10.],
                'solver': ["cholesky","svd", "lsqr"]
                
            }
        },#Modele avec pénalité"""
        'ElasticNet': {
            'model': ElasticNet(),
            'params': {
                 'alpha': [0.1, 1.0, 10.0],
                 'fit_intercept': [True, False],
                 'l1_ratio': [0.1, 0.5, 0.9],
                 'max_iter': [1000,2000,5000,10000]
            }
        },
        'KNeighborsRegressor': {
            'model': KNeighborsRegressor(),
            'params': {
                'n_neighbors': [3, 5, 7, 9, 11, 13, 15]
            }
        },
        'Random Forest': {
            'model': RandomForestRegressor(),
            'params': {
                'n_estimators': [20,30,40,50, 100, 150, 200, 250, 300,400]
            }
        },
        'SVR': {
            'model': SVR(),
            'params': {
                'C': [0.1, 1., 10., 100,500,1000,2000,5000,10000],  
                'epsilon': [0.01, 0.1, 1., 10.]
            }
        }
        
    }
    resultats = []
    for modele, config in modeles.items():
        g =  GridSearchCV(config['model'], config['params'])#Dénombrement de tout les parametres"""
        g.fit(X_train, y_train)#applique sur les data train"""
        resultats.append({
            'model': modele,
            'best_score': g.best_score_,
            'best_params': g.best_params_
        })

    return pd.DataFrame(resultats, columns=['model', 'best_score', 'best_params'])

def affiche_scores_meilleur_modele(Best_model, X_train, y_train, X_test, y_test):
    """Affiche les différentes métriques du meilleur modèle pour les données d'entraînement et de test."""
    Best_model.fit(X_train, y_train)
    score_train = cross_val_score(Best_model, X_train, y_train, cv=5).mean()
    score_test = Best_model.score(X_test, y_test)
    print("Moyenne du score des données d'entraînement :", round(score_train, 2))
    print("Score des données de test :", round(score_test, 2))
    
    



def courbe_apprentissage(Best_model, X_train, y_train):
    """Trace la courbe d'apprentissage"""
    N, train_score, val_score = learning_curve(Best_model, X_train, y_train,
                                               train_sizes = np.linspace(0.1,1.0,10), cv = 5 )
    plt.plot(N, val_score.mean(axis=1), label='validation')
    plt.xlabel('train_sizes')
    plt.legend()
    

def calcule_mae(Best_model, y_test, X_test):
    """Calcule l'erreur moyenne absolue pour les données de test."""
    y_test_predicted = Best_model.predict(X_test)
    print('Erreur moyenne absolue : ', round(mean_absolute_error(y_test, y_test_predicted), 2))
    
def prediction_donnees_test(Best_model, X_train, y_train, y_test, X_test):
    """Effectue une prédiction sur les données de test et affiche les supporters réel et les supporters prédit dans un tableau."""
    Best_model.fit(X_train, y_train)
    y_test_predicted = Best_model.predict(X_test)
    resultat = pd.DataFrame({"Réalité":y_test, "Prédiction":y_test_predicted})
    resultat['Écart'] = resultat.Prédiction - resultat.Réalité
    return round(resultat.head(10),)

def trouve_annee_ecart(Best_model, X_train, y_train, X_test, y_test):
    Gros_ecart = prediction_donnees_test(Best_model, X_train,
                            y_train, y_test, X_test).sort_values(by="Écart",ascending=True).head(10).index
    for i in X_test.loc[Gros_ecart].columns[
                np.where(X_test.loc[Gros_ecart]!=0)[1]]:
        if i.startswith("Year")==True:
            print(i)
            
def affiche_nuage_prediction(Best_model, X_train, y_train, X_test, y_test):
    """Construit et affiche le nuage de point entre les supporters réel et prédit"""
    Best_model.fit(X_train, y_train)
    y_test_predicted = Best_model.predict(X_test)
    fig = plt.figure()
    plt.scatter(y_test, y_test_predicted)
    fig.suptitle('Réalité et prédiction', fontsize=20)               
    plt.xlabel('Supporter réel', fontsize=18)                         
    plt.ylabel('Supporter fictif', fontsize=16)
    plt.show()
    
def affiche_var_importantes(Best_model, X_train, y_train):
    """Construit et affiche le graphique permettant d'identifier les variables qui ont été les plus importantes lors de la construction du meilleur modèle."""
    Best_model.fit(X_train, y_train)
    var_imp = pd.Series(data = Best_model.feature_importances_, index = X_train.columns)
    var_imp.sort_values(ascending = False, inplace = True)
    Contrib = var_imp.nlargest(10)
    Contrib = Contrib.reset_index()
    Contrib.columns = ["Variables", "Importance"]
    sns.barplot(x="Variables", y="Importance",
             data=Contrib)
    plt.xticks(rotation=90)
    plt.show()
    
    
def prediction_huit(data,Huitieme,Best_model):
    """Prédit les supporters théorique des huitiemes de finale"""
    
    Bute = Tournement.But(Huitieme, data)
    Exterieur=Bute[(Bute.lieu!=Bute.equipe_1) & (Bute.lieu!=Bute.equipe_2)]  
    
    df_sub = Exterieur[["equipe_1","equipe_2","Annee","Situation"]]
    futur_huit = pd.DataFrame([ (Huitieme[0], Huitieme[1],"2018", "1/8F"),
                    (Huitieme[2],Huitieme[3], "2018",'1/8F'),
             (Huitieme[4],Huitieme[5], "2018",'1/8F'),
                    (Huitieme[6],Huitieme[7], "2018",'1/8F'),
                    (Huitieme[8], Huitieme[9], "2018",'1/8F'),
                    (Huitieme[10], Huitieme[11], "2018",'1/8F'),
                    (Huitieme[12], Huitieme[13], "2018",'1/8F'),
                    (Huitieme[14], Huitieme[15], "2018",'1/8F')],
             columns = ['equipe_1', 'equipe_2','Annee',"Situation"])  
    df_sub=df_sub.append(futur_huit)
    df_sub.reset_index(inplace=True)
    del df_sub["index"]
    df_sub["Annee"]=df_sub["Annee"].astype(str)
    df_sub["equipe_2"]=df_sub["equipe_2"].str.replace("RDA",'Allemagne')
    X_predict_huit=pd.get_dummies(df_sub[["equipe_1","equipe_2",
                   "Annee","Situation"]], prefix=['Team1', 'Team2',"Year","Pos"]).tail(8)
    
    aff_att_huit = Best_model.predict(X_predict_huit)
    Pred_huit = pd.DataFrame([ (Huitieme[0], Huitieme[1],"2022", "1/8F",aff_att_huit[0]),
                    (Huitieme[2],Huitieme[3], "2022",'1/8F',aff_att_huit[1]),
             (Huitieme[4],Huitieme[5], "2022",'1/8F',aff_att_huit[2]),
                    (Huitieme[6],Huitieme[7], "2022",'1/8F',aff_att_huit[3]),
                    (Huitieme[8], Huitieme[9], "2022",'1/8F',aff_att_huit[4]),
                    (Huitieme[10], Huitieme[11], "2022",'1/8F',aff_att_huit[5]),
                    (Huitieme[12], Huitieme[13], "2022",'1/8F',aff_att_huit[6]),
                    (Huitieme[14], Huitieme[15], "2022",'1/8F',aff_att_huit[7])],
             columns = ['equipe_1', 'equipe_2','Annee',"Situation","affluence_attendue"])
    Pred_huit["affluence_attendue"]=round(Pred_huit["affluence_attendue"],2)
    return Pred_huit


def prediction_quart(data,Huitieme,Quart,Best_model):
    """Prédit les supporters théorique des quarts de finale"""
    Bute = Tournement.But(Huitieme, data)
    Exterieur=Bute[(Bute.lieu!=Bute.equipe_1) & (Bute.lieu!=Bute.equipe_2)]
    df_sub = Exterieur[["equipe_1","equipe_2","Annee","Situation"]]
    manque_quart = pd.DataFrame([ (Quart[0], Quart[1],"2018", "1/4F"),
                    (Quart[2],Quart[3], "2018",'1/4F'),
             (Quart[4],Quart[5], "2018",'1/4F'),
                    (Quart[6],Quart[7], "2018",'1/4F')],
             columns = ['equipe_1', 'equipe_2','Annee',"Situation"])  
    df_sub=df_sub.append(manque_quart)
    df_sub.reset_index(inplace=True)
    del df_sub["index"]
    df_sub["Annee"]=df_sub["Annee"].astype(str)
    df_sub["equipe_2"]=df_sub["equipe_2"].str.replace("RDA",'Allemagne')
    X_predict_quart=pd.get_dummies(df_sub[["equipe_1","equipe_2",
                   "Annee","Situation"]], prefix=['Team1', 'Team2',"Year","Pos"]).tail(4)
    aff_att_quart = Best_model.predict(X_predict_quart)
    Pred_quart = pd.DataFrame([ (Quart[0], Quart[1],"2022", "1/4F",aff_att_quart[0]),
                    (Quart[2],Quart[3], "2022",'1/4F',aff_att_quart[1]),
             (Quart[4],Quart[5], "2022",'1/4F',aff_att_quart[2]),
                    (Quart[6],Quart[7], "2022",'1/4F',aff_att_quart[3])],
             columns = ['equipe_1', 'equipe_2','Annee',"Situation","affluence_attendue"])
    Pred_quart["affluence_attendue"]=round(Pred_quart["affluence_attendue"],2)
    return Pred_quart

def prediction_demi(data,Huitieme,Demi,Best_model):
    """Prédit les supporters théorique des demi de finale"""
    Bute = Tournement.But(Huitieme, data)
    Exterieur=Bute[(Bute.lieu!=Bute.equipe_1) & (Bute.lieu!=Bute.equipe_2)]
    df_sub = Exterieur[["equipe_1","equipe_2","Annee","Situation"]]
    manque_demi = pd.DataFrame([ (Demi[0], Demi[1],"2018", "1/2F"),
                    (Demi[2],Demi[3], "2018",'1/2F')],
             columns = ['equipe_1', 'equipe_2','Annee',"Situation"])  
    df_sub=df_sub.append(manque_demi)
    df_sub.reset_index(inplace=True)
    del df_sub["index"]
    df_sub["Annee"]=df_sub["Annee"].astype(str)
    df_sub["equipe_2"]=df_sub["equipe_2"].str.replace("RDA",'Allemagne')
    X_predict_demi=pd.get_dummies(df_sub[["equipe_1","equipe_2",
                   "Annee","Situation"]], prefix=['Team1', 'Team2',"Year","Pos"]).tail(2)
    aff_att_demi = Best_model.predict(X_predict_demi)
    Pred_demi = pd.DataFrame([ (Demi[0], Demi[1],"2022", "1/2F",aff_att_demi[0]),
                    (Demi[2],Demi[3], "2022",'1/2F',aff_att_demi[1])],
             columns = ['equipe_1', 'equipe_2','Annee',"Situation","affluence_attendue"])
    Pred_demi["affluence_attendue"]=round(Pred_demi["affluence_attendue"],2)
    return Pred_demi

def prediction_finale(data,Huitieme,Finalistes,Best_model):
    """Prédit les supporters théorique de la finale"""
    Bute = Tournement.But(Huitieme, data)
    Exterieur=Bute[(Bute.lieu!=Bute.equipe_1) & (Bute.lieu!=Bute.equipe_2)]
    df_sub = Exterieur[["equipe_1","equipe_2","Annee","Situation"]]
    manque_finale = pd.DataFrame([ (Finalistes[0], Finalistes[1],"2018", "Finale")],
             columns = ['equipe_1', 'equipe_2','Annee',"Situation"])  
    df_sub=df_sub.append(manque_finale)
    df_sub.reset_index(inplace=True)
    del df_sub["index"]
    df_sub["Annee"]=df_sub["Annee"].astype(str)
    df_sub["equipe_2"]=df_sub["equipe_2"].str.replace("RDA",'Allemagne')
    X_predict_finale=pd.get_dummies(df_sub[["equipe_1","equipe_2",
                   "Annee","Situation"]], prefix=['Team1', 'Team2',"Year","Pos"]).tail(1)
    aff_att_finale = Best_model.predict(X_predict_finale)
    Pred_finale = pd.DataFrame([ (Finalistes[0], Finalistes[1],"2022", "Finale",aff_att_finale[0])],
             columns = ['equipe_1', 'equipe_2','Annee',"Situation","affluence_attendue"])
    Pred_finale["affluence_attendue"]=round(Pred_finale["affluence_attendue"],2)
    return Pred_finale

