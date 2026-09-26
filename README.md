# Avila Patrimoine

Site vitrine d'**Ana Avila**, conseillère en gestion de patrimoine indépendante.

**En ligne : https://tinmarlastar.github.io/avila-patrimoine/**

Une seule page, en HTML statique : pas de framework, pas d'étape de compilation.
Le site est publié par GitHub Pages à chaque `push` sur `main`.

> Contenu provisoire : le site n'est pas indexé par les moteurs de recherche
> (`<meta name="robots" content="noindex">` et `robots.txt`). À retirer quand le
> contenu sera définitif.

## La page

| | Section | Ancre |
|---|---|---|
| | Accueil (grand titre sur vidéo) | `#accueil` |
| 01 | Nos engagements | `#engagements` |
| 02 | Moments de vie | `#moments-de-vie` |
| 03 | Accompagnement | `#accompagnement` |
| 04 | Qui suis-je ? | `#qui-suis-je` |
| 05 | Mon réseau | `#reseau` |
| 06 | Contactons-nous | `#contact` |
| 07 | FAQ | `#faq` |

Plus deux pages légales : `privacy-policy.html` (confidentialité) et
`terms-and-conditions.html` (conditions), reliées au pied de page.

## Ce qui est propre à ce site

- **Quatre thèmes de couleur** : Océan profond (par défaut), Ardoise et citron,
  Graphite et orange, Violet électrique. Le carré en haut à droite permet de changer ;
  le choix est mémorisé dans le navigateur. → `assets/js/theme.js` et les variables
  `--th-*` en tête de `assets/css/styles.css`.
- **Une vidéo d'accueil différente à chaque chargement**, jamais la même deux fois de
  suite. → `assets/js/video-accueil.js`
- **Défilement aimanté** : une section qui arrive près du haut de l'écran s'y cale,
  sous le menu ; chaque chargement repart en haut de page. → `assets/js/defilement.js`
- **Formulaire de contact sans service tiers** : il ouvre un e-mail pré-rempli vers
  `contact@avilapatrimoine.fr`. → fin de `assets/js/custom.js`

## Ajouter ou changer une vidéo d'accueil

Déposer les fichiers dans `assets/videos/`, numérotés sans trou :

```
accueil-1.mp4
accueil-2.mp4
accueil-3.mp4
…
```

Le script détecte ceux qui existent (jusqu'à `accueil-20.mp4`) et en tire un au
hasard. Viser 3 à 8 Mo par vidéo : 15 à 20 secondes en boucle, 1080p, sans son.

## Voir le site en local

```bash
python3 -m http.server 8090
```

puis ouvrir http://localhost:8090 depuis ce dossier.

## Modifier le site

- **Styles et comportements** : directement dans `assets/css/styles.css` et
  `assets/js/`.
- **Textes et structure des pages** : les fichiers HTML sont **générés** à partir d'un
  classeur Excel et de deux scripts Python (`appliquer.py`, `restructurer.py`),
  conservés hors de ce dépôt, dans le dossier `textes/` voisin. Une modification faite
  à la main dans `index.html` serait écrasée à la prochaine génération : la reporter
  dans le classeur (textes) ou dans `restructurer.py` (structure).

## Fichiers

```
index.html                  la page
privacy-policy.html         confidentialité
terms-and-conditions.html   conditions
assets/css/styles.css       styles (Bootstrap 5 + thème du site)
assets/js/                  scripts du site (voir plus haut)
assets/libs/                Bootstrap, jQuery, Owl Carousel, AOS
assets/images/ana/          photos d'Ana Avila
assets/videos/              vidéos d'accueil
robots.txt, .nojekyll       réglages de publication
```

## Crédits

Mise en page tirée du template Bootstrap **Studiova** de
[WrapPixel](https://www.wrappixel.com/). Bibliothèques : Bootstrap, jQuery,
Owl Carousel, AOS, Iconify.
