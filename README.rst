Anime Bot
==========

Bot renvoyant des informations sur les animés en fonction.

Instructions
------------
-  !request info 'nom_de_l_anime'

    Donne des informations sur l'anime.

    -> exemple : info 'Clannad'

-  !request episode 'nom_de_l_anime' num_saison num_episode
-  !request episode 'nom_de_l_anime' num_episode

    Affiche l'épisode demandé s'il existe.

    -> exemple : episode 'Clannad' 2 14

    -> exemple : episode 'Clannad' 38

-  !request search 'genre1' 'genre2'

    Affiche tous les animés qui correspondent aux genres précisés

    -> exemple : search 'action' 'comédie'

- !request help

    Affiche les commandes


Installation et utilisation
----------------------------
1. python3 -m pip install -U https://https://github.com/MarcFriedli/HeArcPythonBot

2. crée un fichier config.ini

3. insérer les valeurs suivantes :

        [animebot]

        TOKEN = {token_de_votre_bot}

4.lancer le bot