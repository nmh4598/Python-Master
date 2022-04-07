<div align="center">
  
   # Web scraping sur The Canadian Encyclopedia

</div>

L'objectif est d'analyser les articles d'une catégorie( Politics & Law/Commissions & Reports) de l'encyclopédie en ligne The Canadian Encyclopedia.
Les catégories d’articles sont accessibles à cette adresse :
https://www.thecanadianencyclopedia.ca/en/browse/things.
## Partie scraping avec l’extraction d’informations dans un ensemble de pages web. La sérialisation du contenu extrait sous forme d’un fichier .pick

## Partie analyse avec la construction d’une DTM et d’outils de requêtes sur le corpus.
### 1. queryScore(chaine, N) 
- Cette méthode prend en entrée une requête sous la forme d’une chaîne de caractères, et un entier N, et qui renvoie les urls des N documents les plus pertinents pour cette requête,
### 2. wordCloud(numDoc) 
- Cette méthode  affiche un nuage de tags pour le document d’indice numdoc. L’importance des mots sur le nuage est donné par la mesure tf-idf. On utilisera le
module Python « wordcloud » pour la représentation des nuages de mots.
- Voici un exemple de nuage de mots construit pour la deuxième document du thème Politics & Law/Commissions & Reports.
<div align="center">
<img src="https://raw.githubusercontent.com/nmh4598/Python-Master/main/S2/Text_Mining/nuagedemots.png" width="45%" style="min-height:'250px'"/>
</div>

### 3. nMostSimilar(numDoc, N) 
- Cette méthode prend en entrée un numéro de document et qui renvoie les titres des N documents les plus similaires à ce document. Pour calculer la
similarité, on utilisera une similarité cosinus entre les vecteurs td-idf des documents.
## Projet
Ce projet à été réalisé dans le cadre du cours de Python pour la data science en 1<sup>re</sup> année de Master dans la filière Mathématiques appliquées, Statistique.

