# Avila Patrimoine — site vitrine

Site statique d'une seule page (accueil + 7 sections), tiré d'un template Bootstrap.

Tout le dossier est le dépôt git `tinmarlastar/avila-patrimoine` (public).

- `docs/` : le site, publié par GitHub Pages (source : `main`, dossier `/docs`) sur
  https://tinmarlastar.github.io/avila-patrimoine/ à chaque push sur `main`.
- `textes/` : le classeur Excel des textes, `appliquer.py` (réinjecte les textes) et
  `restructurer.py` (appelé par `appliquer.py` : une seule page, menu, sections, photos,
  réglages de mise en ligne). Ils régénèrent `index.html` et les deux pages légales.

## Règles

- **Publier après chaque modification** : commit, puis `git push origin main`,
  puis vérifier que le build GitHub Pages passe à `built`. Accord durable du propriétaire
  (27/09/2026), pas besoin de redemander.
- Un texte se change dans l'Excel (colonne « Nouveau texte »), puis `python3 textes/appliquer.py`
  — jamais directement dans le HTML, qui serait écrasé à la prochaine régénération.
  Un changement de structure du HTML va dans `restructurer.py`, pour la même raison.
- CSS et JS (`docs/assets/css/styles.css`, `docs/assets/js/*.js`) se modifient directement.
- Seul `docs/` est publié, tel quel : n'y mettre aucun fichier de travail.
- Chemins en `assets/…` (pas `../assets/…`) : le site est servi dans un sous-dossier.
- Le site n'est pas indexé (`noindex` + `robots.txt`) tant que le contenu est provisoire.
- Le formulaire de contact ouvre un e-mail pré-rempli : aucun envoi vers un service tiers.

En local : `python3 -m http.server 8090 --directory docs` → http://localhost:8090
