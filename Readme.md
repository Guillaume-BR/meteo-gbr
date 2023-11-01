# Projet météo

Dans ce projet météo, l'objectif était de créer une page web permettant d'afficher la météo à 5 jours pour la ville de Montpellier. La page devait s'actualiser automatiquement tous les jours. 

Le résultat obtenu est visible en cliquant sur [ce lien](https://guillaume-br.github.io/) ! 

## Les éléments demandés

Voici un aperçu de l'affichage : 

![exemple](https://guillaume-br.github.io/index_files/figure-html/cell-2-output-1.png)

On peut voir : 
* le temps approximatif du jour
* la température maximale
* la température minimale
* le cumul des précipitations 
* le vent moyen avec la direction principale

Pour le cumul des précipitations et le vent moyen, il y a une absence d'icône lorsque les données étaient manquantes.

## Détails techniques

Pour réaliser cette page, je devais utiliser le jeu de données suivant : [open-meteo](https://open-meteo.com/en/docs).

Tout le développement a été fait en Python et notamment le visuel où j'ai utilisé le package matplotlib. Le rendu correspond à un graphique où les données sont en fait des annotations et images placées aux endroits désirés.

J'ai utilisé deux dataframes :
* un pour les données journalières
* un autre pour calculer le vent moyen quotidien et l'intégrer au premier dataframe.

Enfin c'est à l'aide de l'utilitaire quarto et le sytème GitHub-pages que j'ai pu faire le déploiement de la page.

## Source

Pour réaliser le tableau, ce [tutoriel](https://www.sonofacorner.com/beautiful-tables/) bien détaillé a été très utile.

Pour le déploiement, j'ai principalement utilisé la documentation de [Quarto](https://quarto.org/docs/publishing/github-pages.html). 

L'actualisation a été la plus grosse difficulté du projet. Vous pouvez voir des exemples des fichiers yml qui ont permis le déploiement : [publish.yml](https://github.com/Guillaume-BR/Guillaume-BR.github.io/blob/main/.github/workflows/publish.yml) et [_quarto.yml](https://github.com/Guillaume-BR/Guillaume-BR.github.io/blob/main/_quarto.yml)

## Contact

Guillaume Bernard-Reymond : guillaume.bernard-reymond@etu.umontpellier.fr