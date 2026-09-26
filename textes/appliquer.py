# Réinjecte la colonne « Nouveau texte » du classeur dans les pages du site.
# Les références (page#n) désignent le n-ième texte trouvé par extraire.py ;
# on relit donc les pages dans l'état où elles ont été extraites (commit BASE),
# puis on réapplique la marque Avila Patrimoine par-dessus.
import html, html.parser, os, re, subprocess, sys
import openpyxl

ICI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ICI, "..", "docs")
BASE = "d815cd1"  # pages au moment de l'extraction (thème ajouté, textes d'origine)
SKIP = {"script", "style", "noscript", "svg", "iconify-icon"}
TAGS = ("title", "h1", "h2", "h3", "h4", "h5", "h6", "p", "a", "button", "li", "span", "label",
        "option", "blockquote", "th", "td")


class Localiseur(html.parser.HTMLParser):
    """Même parcours que extraire.py, mais note où se trouve chaque texte dans la source."""

    def __init__(self, src):
        super().__init__()
        self.src, self.stack, self.zone, self.items = src, [], "corps", []
        self.lignes = [0]
        for l in src.splitlines(keepends=True):
            self.lignes.append(self.lignes[-1] + len(l))
        self.en_cours = None  # texte dont on attend la fin

    def pos(self):
        l, c = self.getpos()
        return self.lignes[l - 1] + c

    def fermer(self):
        if self.en_cours is not None:
            self.en_cours["fin"] = self.pos()
            self.en_cours = None

    def handle_starttag(self, t, a):
        self.fermer()
        a = dict(a)
        if t == "header": self.zone = "en-tête"
        if t == "footer": self.zone = "pied de page"
        if t in ("img", "input", "textarea", "meta"):
            debut, brut = self.pos(), self.get_starttag_text()
            for k in ("alt", "placeholder"):
                if a.get(k) and not re.fullmatch(r"(logo|img|image)?", a[k].strip(), re.I):
                    self.items.append({"zone": self.zone, "attr": k, "debut": debut, "fin": debut + len(brut)})
            if t == "meta" and a.get("name") == "description":
                self.items.append({"zone": "meta", "attr": "content", "debut": debut, "fin": debut + len(brut)})
        if t not in ("img", "input", "meta", "link", "br", "hr", "source"):
            self.stack.append(t)

    def handle_startendtag(self, t, a):
        self.handle_starttag(t, a)
        if self.stack and self.stack[-1] == t: self.stack.pop()

    def handle_endtag(self, t):
        self.fermer()
        if t in self.stack:
            while self.stack and self.stack.pop() != t: pass
        if t in ("header", "footer"): self.zone = "corps"

    def handle_comment(self, d): self.fermer()
    def handle_decl(self, d): self.fermer()

    def handle_data(self, d):
        self.fermer()
        if not " ".join(d.split()) or any(x in SKIP for x in self.stack): return
        tag = next((x for x in reversed(self.stack) if x in TAGS), self.stack[-1] if self.stack else "?")
        it = {"zone": "head" if tag == "title" else self.zone, "attr": None, "debut": self.pos()}
        self.items.append(it)
        self.en_cours = it

    def close(self):
        super().close()
        if self.en_cours is not None: self.en_cours["fin"] = len(self.src)


def items_de(page):
    src = subprocess.run(["git", "show", f"{BASE}:{page}"], cwd=SITE, capture_output=True, text=True, check=True).stdout
    p = Localiseur(src); p.feed(src); p.close()
    return src, p.items


def remplacer_texte(brut, neuf):
    # garde les espaces autour, remplace le contenu
    m = re.match(r"(\s*)(.*?)(\s*)$", brut, re.S)
    texte = html.escape(neuf, quote=False)
    texte = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", texte)  # **gras** saisi dans le classeur
    return m.group(1) + texte + m.group(3)


def remplacer_attr(balise, attr, neuf):
    return re.sub(r'(\s%s\s*=\s*)(["\'])(.*?)\2' % attr,
                  lambda m: m.group(1) + m.group(2) + html.escape(neuf) + m.group(2), balise, count=1, flags=re.S)


def retirer_etape(src, onglet, suivant):
    """Retire un onglet de la section « services » (ligne + photo) et active le suivant."""
    n = len(src)
    src = re.sub(r'\n\s*<li\b(?:(?!</li>).)*?id="%s-tab".*?</li>' % onglet, "", src, count=1, flags=re.S)
    src = re.sub(r'\n\s*<div class="tab-pane[^"]*" id="%s".*?</div>' % onglet, "", src, count=1, flags=re.S)
    assert len(src) < n, "onglet %s introuvable" % onglet
    src = src.replace('<div class="tab-pane" id="%s"' % suivant, '<div class="tab-pane active" id="%s"' % suivant, 1)
    src = re.sub(r'(<button class="nav-link[^"]*?)(" id="%s-tab"(?:(?!</button>).)*?aria-selected=")false"' % suivant,
                 r'\1 active\2true"', src, count=1, flags=re.S)
    return src


# 1. Lire le classeur
wb = openpyxl.load_workbook(os.path.join(ICI, "Textes du site Studiova.xlsx"))
nouveaux, commun = {}, {}
for ws in wb.worksheets[1:]:
    for ref, _, _, orig, neuf in ws.iter_rows(min_row=2, max_col=5, values_only=True):
        if neuf is None or str(neuf).strip() == "": continue
        page, n = ref.split("#")
        (commun if page == "commun" else nouveaux.setdefault(page, {}))[int(n)] = str(neuf).strip()

# Les textes « commun » sont repérés par leur rang parmi ceux du menu et du pied de page de l'accueil.
_, accueil = items_de("index.html")
rang_commun = {}
k = 0
for i, it in enumerate(accueil):
    if it["zone"] in ("en-tête", "pied de page"):
        if i in commun: rang_commun[k] = commun[i]
        k += 1

# 2. Remplacer dans chaque page
LOGO_B = '<span class="brand-logo text-white">Avila Patrimoine<span class="brand-dot">.</span></span>'
LOGO_N = '<span class="brand-logo text-dark">Avila Patrimoine<span class="brand-dot">.</span></span>'
bilan = {}
PAGES = subprocess.run(["git", "ls-tree", "--full-tree", "--name-only", BASE], cwd=SITE, capture_output=True, text=True, check=True).stdout.split()
for page in sorted(f for f in PAGES if f.endswith(".html")):
    src, items = items_de(page)
    a_faire = dict(nouveaux.get(page, {}))
    k = 0
    for i, it in enumerate(items):
        if it["zone"] in ("en-tête", "pied de page"):
            if k in rang_commun and i not in a_faire: a_faire[i] = rang_commun[k]
            k += 1
    # de la fin vers le début pour ne pas décaler les positions
    for i in sorted(a_faire, reverse=True):
        if i >= len(items):
            print(f"!! {page}#{i} introuvable", file=sys.stderr); continue
        it = items[i]
        brut = src[it["debut"]:it["fin"]]
        neuf = remplacer_attr(brut, it["attr"], a_faire[i]) if it["attr"] else remplacer_texte(brut, a_faire[i])
        src = src[:it["debut"]] + neuf + src[it["fin"]:]
    # la marque, comme dans le commit « Avila Patrimoine à la place de Studiova »
    src = re.sub(r'<img src="\.\./assets/images/logos/logo-white\.svg"[^>]*>', LOGO_B, src)
    src = re.sub(r'<img src="\.\./assets/images/logos/logo-dark\.svg"[^>]*>', LOGO_N, src)
    src = src.replace('<h1 class="mb-0 fs-16 text-white lh-1">', '<h1 class="mb-0 fs-16 text-white lh-1 hero-title">')
    src = src.replace("www.studiova.com", "www.avila-patrimoine.com").replace("Studiova", "Avila Patrimoine")
    if page == "index.html":
        src = retirer_etape(src, "one", "two")  # « Diagnostic patrimonial » retiré de l'accompagnement
    src = src.replace('<html lang="en"', '<html lang="fr"')
    theme = '<script src="../assets/js/theme.js"></script>'
    src = src.replace(theme, theme + '\n  <script src="../assets/js/defilement.js" defer></script>')
    # le template colle parfois le mot qui suit un passage coloré (« Guidelines</span>Before »)
    src = re.sub(r"</span>(?=[^\W\d_])", "</span> ", src)
    # liens du template → coordonnées d'Avila Patrimoine
    for vieux, neuf in (('href="mailto:info@wrappixel.com"', 'href="mailto:contact@avilapatrimoine.fr"'),
                        ('href="https://www.wrappixel.com/" target="_blank"', 'href="mailto:contact@avilapatrimoine.fr"'),
                        ('href="https://www.wrappixel.com/templates/"', 'href="contact.html"'),
                        ('href="tel:+1-212-456-7890"', 'href="tel:+33123456789"')):
        src = src.replace(vieux, neuf)
    open(os.path.join(SITE, page), "w", encoding="utf-8").write(src)
    bilan[page] = len(a_faire)
print(bilan, sum(bilan.values()), "textes remplacés")

# 3. Une seule page : sections, menu, pages supprimées
import restructurer
restructurer.restructurer()
