# Lucas

## 11th of September

Pas de vocal pour l'instant :p

- J'ai surtout récupérer les données jsons edf en local et écrit les notes pour avoir une idée de notre objectif principal et des différentes étapes, et check un peu les codes qui utilisent l'API météo france.

- J'ai crée une branche pour moi mais pas encore utilisé, je vais mettre mes notes en main pour l'instant si c'est ok. J'ai fais un compte Graphana et Météo France API.

- On pourrait commencer à travailler sur des choses séparamment si on fait ce qu'il y a écrit dans **goals**.
   Je peux commencer à faire une map aveec les jsons du réseaux, voir comment récupérer des infos via météo france API (pour l'instant sans temps réel). Tu peux regarder comment récupérer des infos via Copernicus (j'ai pas du tout regardé ça). 
  On peux tout les deux regarder plotly dash et Graphana et choisir lequel des 2 on utilise (en gardant l'autre en plan B). 
  Il faudrait définir qui fait quoi. On peut chacun se concentrer sur un phénomène naturel que l'on choisit au début. Un de nous deux peut aussi même déjà penser à la visualization pourquoi pas même si c'est un peu prématuré 

## 18th of September
- J'ai organisé le squelette d'un code un minimum propre, avec un env _(c'est à faire tout le temps, ne jamais travailler sur (base), mais dans mon cas c'est encore plus primordial car j'ai un PC du labo, nomade, ce qui veut dire que les gens ont mis de la merde dans (base) petit à petit, ce qui fait que quoi que tu veuilles installer comme package (pip conda ou autre) tu auras des conflit)_, à la shlagos j'ai pas d'API comme c'est l'ordi nomade, donc je fais avec Sublime text et j'ai installé PUDB dans mon env pour avoir un debugger dans le termnal. 

- Je propose qu'on utilise tout les deux au moins des configs pour pouvoir travailler plus facilement, hardcoder les chemins c'est vraiment degueux. Pour le reste aucune restriction dans le code. Qu'en penses-tu? Genre on utilise pas de convention d'écriture à la PEP8 ou équivalent, le projet et trop court pour ça, non? Aussi on ne fais pas de management d'env, chacun à son propre env. 

- J'ai ajouté les pylones pour me rendre compte que c'est juste entre chaque HTB aerien tu as un fucking pylones. donc ça sert à rien.

- J'ai commencé beaucoup trop tard - 21h et j'ai 1h de trajet pour rentrer - plus il faut compter le temps d'écrire les notes à partager - donc j'ai fais que dalle, beaucoup moins  que la dernière fois. Cependant il me reste plein de séances de travail, j'ai fais mon agenda dans mes notes perso si tu veux voir. Le Samedi 12 Octobre on pourrait même s'organiser une demi journée qui correspond pour que l'on travaille en même temps. Cette semaine je pourrais pas rattraper le temps perdu de ce Mercredi je suis pris jusqu'à dimanche soir. Tant pis.

  Il  faut probablement répartir les tâches comme suit. Une personne s'occupe de:

  - l'apparence du dashboard 
  - affichage des données réseaux sur la carte (ce qui à déjà commencé voir fini)
  - récupérer un type de données environmentale et de l'afficher sur la carte, sur la même tab ou pas c'est selon
  -  d'avoir un indicateur d'alerte de cette donnée sur la partie de réseaux concernée.  

  Comme j'ai compris ton code pour le dashboard et l'affiche des données réseaux, on en est au même point. Je propose d'être cette personne. Mais 2 personnes sur l'apparence du dashboard plus l'affichage du réseaux c'est contre-productif. 

  Une autre personne s'occupe d'une (ou deux) autres problématique environementale, soit:

  - de récupérer un type de données environmentale et de l'afficher sur la carte, sur la même tab ou pas c'est selon
  - d'avoir un indicateur d'alerte de cette donnée sur la partie de réseaux concernée.
  - potentiellement cela pour 2 menaces différentes, ou alors des données plus compliqué que la personne numéro 1 qui fait aussi le réseau et le dashboard.

  On pourrait faire un tableau avec plusieurs choix, on commencerait par ce qui fait le plus de sens. Comme ceci:
  
  

| Données Réseaux Affichées | API pour données Environnementales | Données Environnementales       | Seuil d'alerte                                          | Autres         |
|---------------------------|-----------------------------------|---------------------------------|--------------------------------------------------------|----------------|
| Hta et Htb aérien          | Météo France                      | Température, Humidité, Vent      | T > 30°C + Humidité < 30% + Vent > 30 km/h              | ------------   |
| Machin souterrain          | Copernicus? Météo France?         | Pluie                           | Si précipitation plus de Xmm dans la zone               | ------------   |
| To fill         | To fill       | To fill                          | To fill   | ------------   |



  J'aime beaucoup ton point d), on de nous 2 pourrait s'en occuper en première menace / données environementales à traiter.

On devrait choisir en priorité des données qui peuvent avoir un flox online pour la prochaine étape de passer du online au offline. 

# Alberto

Jour 7. Toujours pas de vocal. Je crois que Lucas n'est plus. Il vivra toujours dans notre mémoire.

- J'ai une branche 'alberto' que j'ai alimenté avec un src/test.py qui permet de lancer un dashboard dash. Il suffit d'executer le fichier puis d'aller sur http://127.0.0.1:8050/ . Pour l'instant, j'ai récupèré les données des lignes aériennes des geojason, parsé, puis fait un scatter mapbox des données. J'ai mis deux tabs pour organiser un peu.
- J'ai un compte météo france qui marche. Pas essayé l'api encore.
- Ok je viens de lire. Je regarderai pour Copernicus alors.
- Pour la météo et EDF sur l'API il y a le vent moyent et les rafales. En plus on pourrait penser à utiliser :
a) pluie! ça peut inonder les sous stations et les lignes souterraines!
b) température! T élevées -> plus de conso electrique, surcharge des systèmes? A coupler avec les données de prod et conso peut être?
c) orages et foudre
d) feux, règle des 30 : T > 30 + Humidité < 30% + Vent > 30km/h -> risque important de feu. Les lignes aériennes peuvent générer des étincelles.
