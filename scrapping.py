"""Description.

Scrapping et stockage du code cdm et qualif

"""
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup as BS




def creation_backup_cdm(lien):
    """Créer i backup pour i années de coupe du monde"""
    nav = webdriver.Chrome()
    nav.get(lien)
    code_accueil = nav.page_source
    soupe_acc = BS(code_accueil)
    menu_gauche = nav.find_element(By.ID, "menugauche")
    menu_gauche.find_element(By.LINK_TEXT, "Historique Coupe du monde").click()
    code_tableau = nav.page_source
    soupe_tableau = BS(code_tableau,"lxml")
    #liste des années ou la cdm a été organisée
    an = list()
    for i in range(1930,2022,4):
        an.append(i)
    del an[3:5] #enlever les 2 annees ou il n'y a pas eu de cdm
    #clique sur chaque annee et créer le backup associé à chaque année"""
    for annee in an:
        for i in nav.find_elements(By.LINK_TEXT , str(annee)):
            if i.text == str(annee):
                bon = []
                bon.append(i)
                if len(bon)<=1:
                    bon[0].click()
                    with open("backup"+ str(annee)+".html" , "w", encoding="utf8") as fichier:
                        fichier.write(nav.page_source)
    nav.quit()
#Autre méthode avec get attribute pour trouver le code a inserer pour By.Class etc...



def creation_backup_Qualif(lien):
    """Créer un backup de chaque continent pour les qualifications"""
    nav = webdriver.Chrome()
    nav.get(lien)
    nav.find_element(By.LINK_TEXT,"fermer et accepter").click()
    nav.find_element(By.LINK_TEXT,"football").click()
    try:
        nav.find_element(By.LINK_TEXT,"Ligue des nations").click()
    except:
        pass
    nav.find_element(By.LINK_TEXT,"Qualif Coupe du Monde 2022").click()
    nav.find_element(By.LINK_TEXT,"zone Europe").click()
    nav.get("https://www.lequipe.fr/Football/qualif-cm-europe/page-calendrier-resultats/tous-les-groupes")
    code_europe = nav.page_source
    nav.find_element(By.LINK_TEXT,"Qualif Coupe du Monde 2022").click()
    nav.find_element(By.LINK_TEXT,"zone Afrique").click()
    code_afrique = nav.page_source
    nav.find_element(By.LINK_TEXT,"Qualif Coupe du Monde 2022").click()
    try:
        nav.find_element(By.LINK_TEXT,"zone Asie").click()
    except:
        pass
    nav.find_element(By.LINK_TEXT,"zone Amsud").click()
    code_amerique_sud = nav.page_source
    nav.find_element(By.LINK_TEXT,"Qualif Coupe du Monde 2022").click()
    try:
        nav.find_element(By.LINK_TEXT,"classement FIFA").click()
    except:
        pass
    nav.find_element(By.LINK_TEXT,"zone Asie").click()
    code_asie = nav.page_source
    nav.find_element(By.LINK_TEXT,"Qualif Coupe du Monde 2022").click()
    try:
        nav.find_element(By.LINK_TEXT,"classement FIFA").click()
    except:
        pass
    nav.find_element(By.LINK_TEXT,"zone Concacaf").click()
    code_ame_nord = nav.page_source
    Code_qual_all = []
    Code_qual_all.append(code_europe,code_afrique,code_amerique_sud,code_asie,code_ame_nord)
    Continent = []
    Continent.append(europe,afrique,amerique_sud,asie,ame_nord)
    for i in zip(Code_qual_all,Continent):
         with open("backup_qualification_" + i[1] +".html" , "w", encoding="utf8") as fichier:
                    fichier.write(i[0])
    nav.quit()