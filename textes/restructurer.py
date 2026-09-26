# Transforme le site en une seule page : l'accueil et 7 sections numérotées,
# un menu qui mène à chacune, et les deux pages légales. Lancé par appliquer.py
# après l'injection des textes (il peut aussi être relancé seul, mais seulement
# sur des pages fraîchement régénérées : il suppose la structure du template).
import os, re

ICI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ICI, "..", "docs")
GARDER = ("index.html", "privacy-policy.html", "terms-and-conditions.html")

# (ancre, libellé du menu) dans l'ordre de la page
SECTIONS = [
    ("engagements", "Nos engagements"),
    ("moments-de-vie", "Moments de vie"),
    ("accompagnement", "Accompagnement"),
    ("qui-suis-je", "Qui suis-je ?"),
    ("reseau", "Mon réseau"),
    ("contact", "Contactons-nous"),
    ("faq", "FAQ"),
]


def lire(nom):
    return open(os.path.join(SITE, nom), encoding="utf-8").read()


def section(src, classe):
    """Le bloc <section class="classe …">…</section> (les sections ne s'imbriquent pas)."""
    m = re.search(r'\n[ \t]*<section class="%s[ "].*?</section>' % re.escape(classe), src, re.S)
    assert m, "section %s introuvable" % classe
    return m.group(0)


def entete(src, numero, libelle):
    """Remplace le numéro et l'étiquette de l'en-tête de section (01 ── Libellé)."""
    src, n = re.subn(r'(fw-medium">)\d\d(</span>\s*<hr[^>]*>\s*<span class="badge[^"]*">)[^<]*(</span>)',
                     r"\g<1>%s\g<2>%s\g<3>" % (numero, libelle), src, count=1)
    assert n, "en-tête introuvable pour %s" % libelle
    return src


def ancre(src, id_):
    src = re.sub(r'\sid="services"', "", src, count=1)
    return re.sub(r"<section ", '<section id="%s" ' % id_, src, count=1)


def fond(src, gris):
    src = src.replace(" bg-light-gray", "", 1)
    if gris:
        src = re.sub(r'(<section [^>]*class="[^"]*)"', r'\1 bg-light-gray"', src, count=1)
    return src


def qui_suis_je(about):
    """Section 04 : la présentation de l'ancienne page À propos, avec sa photo et son bandeau."""
    contenu = section(about, "about-content")
    titre = re.search(r"<h2[^>]*>(.*?)</h2>", contenu, re.S).group(1)
    paras = re.search(r'(<div class="d-flex flex-column gap-4 gap-lg-5".*?</div>)', contenu, re.S).group(1)
    bandeau = re.search(r'<div class="marquee.*</div>', section(about, "about-img"), re.S).group(0)
    conferences = "\n".join(
        '            <div class="col-md-4"><img src="../assets/images/ana/ana-conference-%d.jpg" alt="Ana Avila en conférence"\n'
        '                class="img-fluid w-100 rounded-3 object-fit-cover" style="aspect-ratio:4/3" data-aos="fade-up"\n'
        '                data-aos-delay="%d" data-aos-duration="1000"></div>' % (i, 100 * i) for i in (1, 2, 3))
    photo = """<div class="container mt-5 mt-xl-10">
          <div class="row g-4">
%s
          </div>
        </div>
        <div class="mt-5 mt-xl-10">
        %s
        </div>""" % (conferences, bandeau)
    return """
    <section class="about-content py-5 py-lg-11 py-xl-12">
      <div class="container">
        <div class="row gap-7 gap-xl-0">
          <div class="col-xl-4 col-xxl-4">
            <div class="d-flex align-items-center gap-7 py-2" data-aos="fade-right" data-aos-delay="100"
              data-aos-duration="1000">
              <span
                class="round-36 flex-shrink-0 text-dark rounded-circle bg-primary hstack justify-content-center fw-medium">04</span>
              <hr class="border-line">
              <span class="badge text-bg-dark">Qui suis-je ?</span>
            </div>
            <img src="../assets/images/ana/ana-portrait.jpg" alt="Portrait d'Ana Avila"
              class="img-fluid rounded-3 mt-6" style="max-width:88%%" data-aos="fade-right"
              data-aos-delay="200" data-aos-duration="1000">
          </div>
          <div class="col-xl-8 col-xxl-7">
            <div class="d-flex flex-column gap-6">
              <h2 class="mb-0" data-aos="fade-up" data-aos-delay="100" data-aos-duration="1000">%s</h2>
              %s
            </div>
          </div>
        </div>
      </div>
      %s
    </section>""" % (titre, paras, photo)


def menu(src):
    """Menu déroulant : une entrée par section ; plus de connexion / inscription."""
    feuille = ('<img src="../assets/images/svgs/secondary-leaf.svg" alt="" width="20" height="20" '
               'class="img-fluid animate-spin">')
    entrees = [("accueil", "Accueil")] + SECTIONS
    items = "\n".join(
        '                    <li class="header-item">\n'
        '                      <a href="index.html#%s" class="header-link hstack gap-2 fs-7 fw-bold text-dark">%s%s</a>\n'
        "                    </li>" % (a, feuille, l) for a, l in entrees)
    src, n = re.subn(r'(<ul class="header-menu[^>]*>).*?(</ul>)', r"\1\n%s\n                  \2" % items.replace("\\", r"\\"),
                     src, count=1, flags=re.S)
    assert n, "menu introuvable"
    src = re.sub(r'\s*<div class="hstack gap-3">\s*<a href="sign-in\.html".*?</div>', "", src, count=1, flags=re.S)
    # l'e-mail du menu : même taille que le téléphone (en gras), chacun sur sa ligne
    src, n = re.subn(r'<div>(\s*<a class="text-dark" href="tel:[^>]*>[^<]*</a>\s*)<a class="fs-8 text-dark fw-bold" (href="mailto:)',
                     r'<div class="d-flex flex-column gap-1">\1<a class="text-dark fw-bold" \2', src, count=1)
    assert n, "coordonnées du menu introuvables"
    return src


def pied(src):
    liens = [("index.html#accueil", "Accueil"), ("index.html#qui-suis-je", "Qui suis-je ?"),
             ("index.html#accompagnement", "Accompagnement"), ("index.html#contact", "Contactons-nous"),
             ("terms-and-conditions.html", "Conditions"), ("privacy-policy.html", "Confidentialité")]
    items = "\n".join('            <li><a class="link-hover fs-5 text-white" href="%s">%s</a></li>' % l for l in liens)
    src, n = re.subn(r'(<ul class="footer-menu[^>]*>)\s*<li><a[^>]*href="index\.html">.*?(</ul>)',
                     r"\1\n%s\n          \2" % items, src, count=1, flags=re.S)
    assert n, "pied de page introuvable"
    return src


def sans_reseaux_sociaux(src):
    # colonne Facebook / Instagram / LinkedIn du pied de page ; le © reprend la place, calé à droite
    src, n = re.subn(r'\s*<div class="col-md-4 col-xl-2 mb-8 mb-xl-0">\s*<ul class="footer-menu[^>]*>\s*<li><a[^>]*facebook.*?</ul>\s*</div>',
                     "", src, count=1, flags=re.S)
    assert n, "réseaux sociaux du pied de page introuvables"
    src = src.replace('<div class="col-md-4 col-xl-3 mb-8 mb-xl-0">\n          <p class="mb-0 text-white text-opacity-70 text-md-end">',
                      '<div class="col-md-8 col-xl-5 mb-8 mb-xl-0">\n          <p class="mb-0 text-white text-opacity-70 text-md-end">', 1)
    return src


def en_ligne(src):
    """Réglages pour l'hébergement (GitHub Pages, site servi dans un sous-dossier)."""
    # chemins relatifs à la page : « ../assets » sortirait du dossier du site
    src = src.replace('"../assets/', '"assets/').replace("url(../assets/", "url(assets/")
    # pas d'indexation tant que le contenu est provisoire
    if 'name="robots"' not in src:
        src = src.replace("</title>", '</title>\n  <meta name="robots" content="noindex, nofollow">', 1)
    # formulaire : plus d'envoi à formsubmit (adresse de l'auteur du template) ;
    # le bouton ouvre un e-mail pré-rempli (voir custom.js)
    src = re.sub(r'<form action="https://formsubmit\.co/[^"]*" method="post"',
                 '<form data-contact-mailto="contact@avilapatrimoine.fr"', src)
    assert "formsubmit" not in src
    return src


def commun(src):
    src = menu(src)
    src = pied(src)
    src = sans_reseaux_sociaux(src)
    # bouton flottant : « Contactons-nous » vers la section 06
    src, n = re.subn(r'\s+target="_blank"(\s+href="contact\.html">)[^<]*</a>', r'\1Contactons-nous</a>', src)
    src = src.replace('href="contact.html">Contactons-nous</a>', 'href="index.html#contact">Contactons-nous</a>')
    return src


def accueil(index, about):
    banniere = section(index, "banner-section")
    banniere = ancre(banniere, "accueil").replace('href="javascript:void(0)"', 'href="#engagements"', 1)
    # vidéo tirée au hasard parmi assets/videos/accueil-N.mp4 (voir js/video-accueil.js)
    banniere, n = re.subn(r'(<video )([^>]*>)\s*<source src="[^"]*banner-video\.mp4"[^>]*>\s*',
                          r'\1data-video-accueil \2\n      ', banniere, count=1)
    assert n, "vidéo de la bannière introuvable"

    s1 = ancre(entete(section(index, "stats-facts"), "01", "Nos engagements"), "engagements")
    s1 = s1.replace('href="about-us.html"', 'href="#qui-suis-je"')
    s2 = fond(ancre(entete(section(index, "featured-projects"), "02", "Moments de vie"), "moments-de-vie"), True)
    # les cartes ne mènent plus à une page de détail : on retire la flèche au survol
    s2 = re.sub(r'\s*<div class="portfolio-overlay">.*?</div>', "", s2, flags=re.S)
    s3 = ancre(entete(section(index, "services"), "03", "Accompagnement"), "accompagnement")
    s3 = s3.replace('href="projects.html"', 'href="#moments-de-vie"')
    for vieux, neuf, alt in (("services/services-img-2.jpg", "ana/accompagnement-audit.jpg", "Ana Avila en rendez-vous d'audit patrimonial"),
                             ("services/services-img-3.jpg", "ana/accompagnement-recommandations.jpg", "Ana Avila présente ses recommandations à un couple"),
                             ("services/services-img-4.jpg", "ana/accompagnement-suivi.jpg", "Ana Avila en rendez-vous de suivi")):
        s3, n = re.subn(r'src="\.\./assets/images/%s" alt="[^"]*"' % re.escape(vieux),
                        'src="../assets/images/%s" alt="%s"' % (neuf, alt), s3)
        assert n, vieux
    s4 = ancre(qui_suis_je(about), "qui-suis-je")
    s5 = fond(ancre(entete(section(index, "meet-our-team"), "05", "Mon réseau"), "reseau"), True)
    # plus de pastilles Twitter / Behance / LinkedIn au survol des photos
    s5, n = re.subn(r'\s*<div class="meet-team-overlay[^"]*">\s*<ul class="social.*?</ul>\s*</div>', "", s5, flags=re.S)
    assert n, "pastilles des réseaux sociaux introuvables"
    s5, n = re.subn(r'src="\.\./assets/images/team/team-img-1\.jpg" alt="[^"]*"',
                    'src="../assets/images/ana/ana-reseau.jpg" alt="Ana Avila"', s5, count=1)
    assert n, "photo d'Ana dans Mon réseau introuvable"
    s6 = ancre(entete(section(index, "get-in-touch"), "06", "Contactons-nous"), "contact")
    s7 = fond(ancre(entete(section(index, "faq"), "07", "FAQ"), "faq"), True)
    # les questions occupent toute la largeur (au lieu de la colonne de droite)
    s7, n = re.subn(r'<div class="row justify-content-end">(\s*)<div class="col-xl-8">(\s*<div class="accordion)',
                    r'<div class="row">\1<div class="col-12">\2', s7, count=1)
    assert n, "liste des questions introuvable"

    debut = index.index(section(index, "banner-section"))
    fin = index.index(section(index, "get-in-touch")) + len(section(index, "get-in-touch"))
    page = index[:debut] + banniere + s1 + s2 + s3 + s4 + s5 + s6 + s7 + index[fin:]
    defil = '<script src="../assets/js/defilement.js" defer></script>'
    return page.replace(defil, defil + '\n  <script src="../assets/js/video-accueil.js" defer></script>', 1)


def restructurer():
    index, about = lire("index.html"), lire("about-us.html")
    pages = {"index.html": accueil(index, about)}
    for nom in GARDER[1:]:
        pages[nom] = lire(nom)
    for nom, src in pages.items():
        src = en_ligne(commun(src))
        open(os.path.join(SITE, nom), "w", encoding="utf-8").write(src)
    for nom in os.listdir(SITE):
        if nom.endswith(".html") and nom not in GARDER:
            os.remove(os.path.join(SITE, nom))
    # vérification : plus aucun lien vers une page supprimée
    for nom in GARDER:
        src = lire(nom)
        morts = sorted(set(h for h in re.findall(r'href="([^"#:]+\.html)', src) if h not in GARDER))
        assert not morts, "%s : liens vers des pages supprimées %s" % (nom, morts)
        assert "../assets" not in src, "%s : chemin ../assets restant" % nom
    print("une seule page :", ", ".join("%02d %s" % (i + 1, l) for i, (_, l) in enumerate(SECTIONS)))


if __name__ == "__main__":
    restructurer()
