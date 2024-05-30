
# Bot Discord

Ce code est un bot Discord écrit en Python utilisant la bibliothèque `discord.py`. Il offre plusieurs fonctionnalités, notamment la conversion d'images en PDF, l'affichage de la météo, des jeux de dés et de pile ou face, l'affichage de citations de Chuck Norris, de mèmes aléatoires et la traduction de texte.

## Importation des modules

Le code commence par importer les modules nécessaires :

-   `discord` : La bibliothèque principale pour interagir avec l'API Discord.
-   `commands` : Un module de `discord.py` pour créer des bots avec un système de commandes.
-   `PIL` (Python Imaging Library) : Utilisé pour la conversion d'images en PDF.
-   `io` : Utilisé pour la manipulation des flux de données.
-   `requests` : Utilisé pour effectuer des requêtes HTTP.
-   `random` : Utilisé pour générer des nombres aléatoires.
-   `config` : Un module local contenant les tokens d'authentification.
-   `translate` : Un module pour la traduction de texte.
-   `langdetect` : Un module pour détecter la langue d'un texte.

## Configuration du bot

Le code configure ensuite les intentions du bot Discord, en activant notamment l'intention "Privileged Message Content" pour pouvoir accéder au contenu des messages.
## Event 

- ### `Content_link`

Cette fonctionnalité permet de déplacer automatiquement les messages contenant des liens vers des canaux spécifiques en fonction du type de lien, tout en mentionnant l'auteur du message d'origine. Cela peut être utile pour organiser et modérer les liens partagés sur un serveur Discord

## Commandes

Le code définit ensuite plusieurs commandes pour le bot, chacune décorée avec `@bot.command()`.

- ### `img2pdf`

Cette commande convertit une image jointe à un message en fichier PDF et l'envoie dans le salon.

- ### `weather`

Cette commande affiche la météo d'une ville spécifiée en utilisant l'API OpenWeatherMap.

- ### `dé`

Cette commande simule un jeu de dés et affiche les résultats sous forme d'embed.

- ### `coinflip`

Cette commande simule un lancer de pièce et affiche le résultat (pile ou face).

- ### `chuck_norris`

Cette commande affiche une citation aléatoire de Chuck Norris en utilisant l'API Chuck Norris.

- ### `meme`

Cette commande affiche un mème aléatoire en utilisant l'API meme-api.com.

- ### `translate`

Cette commande traduit un texte donné dans une langue spécifiée.

- ###  `translate_message`

Cette commande traduit le message auquel l'utilisateur répond dans une langue spécifiée.

## Exécution du bot

Enfin, le code exécute le bot en utilisant le token d'authentification stocké dans le module `config`.
