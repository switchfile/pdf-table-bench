<!-- page 1 -->

# Barème de l'épreuve physique gendarmerie (EPG)

Documentation du jeu de données. Benjamin Sant, 9 octobre 2026. Licence Creative Commons Attribution 4.0.

## Objet

Ce jeu de données transcrit, en format lisible par une machine, le barème de notation et les paramètres techniques de l'épreuve physique des concours de recrutement des sous-officiers de gendarmerie.

Il s'agit d'une publication indépendante. Elle n'émane ni de la gendarmerie nationale ni du ministère de l'Intérieur.

## Raison d'être

Le barème est public, mais il ne figure qu'en annexe d'un arrêté, sous forme de tableau inséré dans un texte juridique. La gendarmerie en diffuse une version en PDF dont les tableaux sont des images, donc inexploitables par un programme. Les valeurs que l'on trouve en ligne sont par conséquent contradictoires.

## Source

Arrêté du 27 avril 2011 fixant les programmes, les conditions d'organisation et de déroulement ainsi que les coefficients attribués aux différentes épreuves des concours prévus à l'article 13-1 du décret n° 2008-952 du 12 septembre 2008 portant statut particulier du corps des sous-officiers de gendarmerie.

NOR : IOCJ1029171A. Version en vigueur au 9 octobre 2026. Annexe IV pour le barème et les ateliers. Article 23 et annexes I et II pour le coefficient et la note éliminatoire.

<!-- page 2 -->

Aucune valeur de ce jeu de données ne provient d'une source secondaire.

Composition

bareme_epg_gendarmerie.csv, 42 lignes

Barème de notation des deux ateliers chronométrés, de la note 20 à la note 0, pour les hommes et pour les femmes.

Colonne

Contenu

note_sur_20

Note attribuée, de 20 à 0

sexe

homme ou femme, le barème est distinct

valeur_texte_officiel

Valeur telle qu'écrite dans l'arrêté, par exemple 3'10

minutes

Minutes, vide pour la note 0

secondes

Secondes, vide pour la note 0

temps_total_secondes

Temps converti en secondes, pour le calcul

type_de_seuil

Sens de la valeur : temps maximum pour obtenir la note, ou seuil au-delà duquel la note est 0

source

Référence du texte

<!-- page 3 -->

La colonne temps_total_secondes est un calcul dérivé, et non une valeur du texte. Les colonnes brutes sont conservées pour permettre la vérification.

## ateliers_epg.csv, 19 lignes

Paramètres des trois ateliers et de l'épreuve dans son ensemble : charges, distances, dimensions, répétitions, seuils d'échec, coefficient et note éliminatoire, séparément pour les hommes et les femmes.

Deux points que ce jeu de données tranche

L'irrégularité du palier 6

La progression des temps est de cinq secondes par palier sur la quasitotalité du barème. Elle ne l'est pas partout. Entre les notes 7 et 6 elle est de six secondes, puis de quatre secondes entre les notes 6 et 5. Un autre écart atypique, de dix secondes, apparaît entre les notes 9 et 8.

Ces valeurs sont celles du texte officiel. Elles n'ont pas été lissées.

## La note éliminatoire

Il est souvent écrit que l'épreuve physique disposerait d'un seuil particulier à 3 sur 20. Ce seuil a existé, il ne figure plus dans la version en vigueur. L'article 23 fixe un seuil général : est éliminé tout candidat ayant obtenu une note inférieure à 6 sur 20 à l'une des épreuves, à l'exception de l'épreuve d'évaluation numérique qui ne revêt aucun caractère éliminatoire.

## Portée et limites

Ce jeu de données ne couvre que les sous-officiers de gendarmerie. Il ne contient ni les barèmes de la police nationale, ni ceux des armées, ni ceux des sapeurs-pompiers professionnels, qui relèvent de textes distincts.

<!-- page 4 -->

Il ne prédit aucune réussite. Il décrit un barème réglementaire. Les coefficients et les règles d'admission relèvent du décret et des arrêtés d'ouverture de chaque session.

Un texte réglementaire évolue. Avant toute utilisation ayant un effet sur un candidat, il convient de vérifier la version en vigueur sur Légifrance. Seul le texte officiel fait foi.

## Citation

Sant, B. (2026). Barème de l'épreuve physique gendarmerie (EPG) des concours de sous-officiers. Jeu de données, licence CC BY 4.0.

Auteur : Benjamin Sant, ORCID 0009-0007-7018-3550.
