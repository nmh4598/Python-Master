# -*- coding: utf-8 -*-
"""
Nom et prénom: NGUYEN_Manh_Hung
Numéro étudiant : 22110466

"""

from pandas import DataFrame, Series, concat
import pickle
import re
from math import *
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np

# Définition des fonctions
def getTokens(doc):
    regex = r"""\w+"""
    tokens = [word.strip().lower() for word in re.findall(regex, doc)]
    return tokens

# Définition des classes
class DTM:
    def __init__(self, liste_tuple,mots_vides):
        #Récupération des titres et des URLS
        les_url = []
        les_titres = []
        self.stopWords = mots_vides

        for tuple in liste_tuple :
            les_url.append(tuple[0])
            les_titres.append(tuple[1])

        self.url = les_url
        self.title = les_titres

        #Construction du dataframe de mots

        termes_docs = []  #Liste de dictionnaires, qui compte de le nombre d'occurrences de chaque terme dans chaque doc
        for tuple in liste_tuple :
            texte = tuple[2]
            les_mots = getTokens(texte)
            dico = {} #Dictionnaire qui va compter le nombre d'occurrences de chaque mot
            for mot in les_mots :
                if mot not in self.stopWords : #Gestion des mots vides
                    dico[mot] = dico.get(mot,0)+1
            termes_docs.append(dico)
        self.data = DataFrame(termes_docs).fillna(0)

        #Calcul du df : il faut connaitre le nombre de documents qui contiennent chaque terme
        df = self.data.astype('bool').sum()
        # print(df)
        nbdoc = self.data.shape[0]
        # print(nbdoc)
        log_idf = [log(nbdoc/value) for value in df]
        # print(log_idf)
        # print(self.data.max(axis=1))
        self.data = self.data.div(self.data.max(axis=1),axis=0)
        self.data = self.data.mul(log_idf,axis=1)
        #sur un dataframe, div et mul multiplient ou divisent sur toute la ligne (axis=0) ou sur la colonne (axis=1)

    def __repr__(self):
        return self.data.__repr__()
    
    def nBest(self,N):
        return self.data.sum().sort_values(ascending=False)[:N]

    def nBestDoc(self,N,indice):
        return self.data.iloc[indice].sort_values(ascending=False)[:N]

    def query(self,requete):
        mots_valides = [mot for mot in getTokens(requete) if mot not in self.stopWords]
        # print(mots_valides)
        
        if len(mots_valides)==0:
            return []
        
        if not all (mot in self.data.columns for mot in mots_valides):
            return []

        les_url = []
        for i in self.data.index:
            if all([self.data.loc[i,mot]>0 for mot in mots_valides]):
                les_url.append(self.url[i])
        return les_url
    
    def queryScore(self, requete, N):
        mots_valides = [mot for mot in requete.split() if mot not in self.stopWords]
        
        if len(mots_valides)==0:
            return []
        
        if not all (mot in self.data.columns for mot in mots_valides):
            return []
        
        scores = self.data[mots_valides].sum(axis=1)
        return concat({"score": scores, "url": Series(self.url)}, 
                      axis=1).sort_values(by="score", ascending=False)[:N]
    
    def wordCloud(self, numDoc):
        
        # Nombre de document commence à 0 donc on doit prends numDoc-1
        score_mot = self.data.iloc[numDoc-1]
        # Tri décroissant des mots selon leur score
        score_mot1= score_mot.sort_values(ascending=False)
        # Création du WordCloud
        wordcloud = WordCloud(width=3300, height=2000, random_state=1, background_color="White",
                              colormap="rainbow", collocations=False, 
                              stopwords = STOPWORDS).generate(str(list(score_mot1.index)))
        # Affichage du WordCloud
        plt.figure(figsize=(40, 30))
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.show()
            
    def nMostSimilar(self, numDoc, N):
        # Nombre de document commence à 0 donc on doit prends numDoc-1
        doc=self.data.iloc[numDoc-1]
        sim=[]
        # Unc boucle pour trouver la similarité cosinus entre les vecteurs td-idf de article avec tous les autres documents
        for i in range(len(self.data)):
            autre_doc = self.data.iloc[i]
            sim.append(np.linalg.norm(autre_doc) * doc.dot(autre_doc) / (np.linalg.norm(doc) ))
        DF=DataFrame(sim,self.title)
        #print(DF) # Les documents avec les similarité de tous les documents avec le document original
        DF.columns=["similarité"]
        # renvoie les titre des 1:N+1 douments les plus similaires, car 0 c'est le document original
        return DF.sort_values(by="similarité",ascending=False)[1:N+1].index.values 
    
### Programme principal
# Ouverture du fichiers .pick avec le contenu des articles
with open("NGUYEN_Manh_Hung_canada.pick", 'rb') as pickFile:
    doc = pickle.load(pickFile)

# Ouverture du fichier avec les mots vides anglais
with open("mots_vides.txt", "r") as textFile:
    mots_vides = []
    for ligne in textFile:
        mot = ligne.split("\n")[0].strip()
        if mot != "":
            mots_vides.append(mot)

maDTM = DTM(doc, mots_vides)
#print(maDTM)
# Appels des fonctions
print(maDTM.queryScore("make recommendations to improve", 3))
print(maDTM.wordCloud(2))
print(maDTM.nMostSimilar(2,5))
