![Logo](https://i.ibb.co/XpnzsTk/Py-Lyre-Final-No-Color.png)


Audio Streaming Platform - Projet Python3 IPI

<h3> Database structure </h3>

![Database structure](https://i.ibb.co/1vyHVc9/draw-SQL-export-2020-10-20-10-16.png)

<h3> Spécifications </h3>

- Il va falloir modifier / ajouter des infos dans la BDD pour voir une fonctionnalité (notification lorsqu'une nouvelle musique sort) : ajouter un album

Pour cela, il va falloir simuler un ajout d'album :

La méthode la plus simple est d'ouvrir le fichier pylyre.sqlite dans un gestionnaire de base de données. (Il faut déjà avoir créé un compte sur le site)
  -> se déconnecter du site
  -> aller dans la table 'albums'
  -> copier les informations de la dernière ligne de cette table (sans l'id, ni la date, puisqu'ils sont générés automatiquement)
  -> la supprimer
  -> enregistrer les modifications de la bdd
  -> ajouter une ligne
  -> coller les informations
  -> enregistrer les modifications
  -> se connecter au site
