![Logo](https://i.ibb.co/XpnzsTk/Py-Lyre-Final-No-Color.png)


Audio Streaming Platform - Projet Python3 IPI

<h3> Database structure </h3>

![Database structure](https://i.ibb.co/1vyHVc9/draw-SQL-export-2020-10-20-10-16.png)

<h2> Guide de premiers pas </h2>

Pour initaliser la base de données : Un fichier *pylyre.sql* est fourni dans le dépot. Créer la base de donnée avec la commande : 
> sqlite3.exe pylyre.sqlite < pylyre.sql

Se créer un compte (plus rigolo) ou utiliser le compte suivant (avec déjà des likes de musiques, des abonnements à des artistes) :
* email : erictran@live.fr
* mot de passe : admin

<h3> Spécifications </h3>

Il va falloir modifier / ajouter des infos dans la BDD pour voir une fonctionnalité (notification lorsqu'une nouvelle musique sort) : ajouter un album

Pour cela, il va falloir simuler un ajout d'album :

La méthode la plus simple est d'ouvrir le fichier pylyre.sqlite dans un gestionnaire de base de données. (Il faut déjà avoir créé un compte sur le site)
  - se déconnecter du site
  - aller dans la table 'albums'
  - copier les informations de la dernière ligne de cette table (sans l'id, ni la date, puisqu'ils sont générés automatiquement)
  - la supprimer
  - enregistrer les modifications de la bdd
  - ajouter une ligne
  - coller les informations
  - enregistrer les modifications
  - se connecter au site
  
  <h3> Notes : </h3>
  Malheureusement, le PEPE 8 n'est pas forcément respecté partout :(
  
  Il était compliqué de faire certaines fonctionnalités face à la restriction du language Javascript. Il y a seulement un script js pour le lecteur audio.
  
  Un bouton ne fonctionne pas : le bouton d'albums aimés (situé au milieu de la sidebar). Cependant, le code est le même que la fonction de likes de "tracks" qui kui est fonctionnel. Seule la requete SQL change.

<h3> Choses qu'on aurait aimé faire avec un peu plus de temps : </h3>
- Rendre fonctionnelle la fonction de 'likes' d'albums
- Faire un outil de recherche : mettre un input permettant à l'utilisateur de rechercher un album, une musique ou un artiste en particulier
- Revoir un peu l'UX en affichant le nom des albums et des artistes dans la selection d'albums ou d'artistes.
