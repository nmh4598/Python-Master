# -*- coding: utf-8 -*-
"""
Nom et prénom: NGUYEN_Manh_Hung
Numéro étudiant : 22110466

"""

import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup, Tag, NavigableString
import pickle
from multiprocessing import Pool, cpu_count


### Définition des fonctions :
def getSelectedText(monTag):
    texte = ""
    for elem in monTag.children:
        if type(elem) == NavigableString:
            texte += " " + (elem.string).strip()
        elif type(elem) == Tag and validTag(elem):
            texte += getSelectedText(elem)
    return texte


def parseURL(monURL):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    req = Request(monURL, headers={'User-Agent': user_agent})
    try:
        html = urlopen(req)
    except (HTTPError, URLError) as e:
        sys.exit(e)
    bsObj = BeautifulSoup(html, "lxml")

    titre = bsObj.find("h1").get_text()

    texte = getSelectedText(bsObj.find("div", class_="article-content"))
    return (monURL, titre, texte)


def validTag(tag):
    if tag.name == "footer":
        return False
    if "class" in tag.attrs:
        for elem in tag.attrs["class"]:
            if elem in ['grid--col12', 'sb', 'nav']:
                return False
    return True


### Programme principal :
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
full_url = "https://www.thecanadianencyclopedia.ca/en/browse/things/politics-law/commissions-reports"
req = Request(full_url, headers={'User-Agent': user_agent})

try:  # gestion des exceptions avec un bloc try/except
    html = urlopen(req)
except (HTTPError, URLError) as e:
    sys.exit(e)

bsObj = BeautifulSoup(html, "lxml")

# Les liens
liens = bsObj.find("div", class_="contentContainerDesktop").find("main",class_="wrap--narrow l l--hasSidebar search-listing-result")
# Les liens de pages
num_pages = liens.find("div", class_="pagination_widget")
# Les liens de chaque numéro de page
num = num_pages.find_all("li")

liens_articles = []
# Une boucle pour trouver les liens d'articles sur chaque page
for numpage in range(1, int(len(num))):
    # Ajout de chaque numéro de page à la fin du lien
    url = "https://www.thecanadianencyclopedia.ca/en/browse/things/politics-law/commissions-reports?page=" + str(numpage)

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    req = Request(url, headers={'User-Agent': user_agent})
    try:
        html = urlopen(req)
    except (HTTPError, URLError) as e:
        sys.exit(e)

    bsObj = BeautifulSoup(html, "lxml")

    # Les balises <article> dans les classes
    liens = bsObj.find("div", class_="contentContainerDesktop").find("main",class_="wrap--narrow l l--hasSidebar search-listing-result").find_all("article", class_="calloutList-item")

    # Boucle pour récupérer chaque lien d'article (seulement d'article) dans chaque balise
    for article in liens:
        liens_int = article.find("a").get("href")
        liens_articles.append(liens_int)

# Création du fichier .pick avec des tuples contenant pour chaque article son lien, son titre ainsi que son contenu
if __name__ == '__main__':
    res = []
    with Pool(cpu_count() - 1) as p:
        res = p.map(parseURL, liens_articles)

    with open('NGUYEN_Manh_Hung_canada.pick', 'wb') as pickFile:
        pickle.dump(res, pickFile)