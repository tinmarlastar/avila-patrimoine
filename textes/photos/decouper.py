# Découpe la planche de photos d'Ana (3 × 3) en images prêtes pour le site.
import os
from PIL import Image

ICI = os.path.dirname(os.path.abspath(__file__))
SORTIE = os.path.join(ICI, "..", "..", "docs", "assets", "images", "ana")
planche = Image.open(os.path.join(ICI, "planche-ana.webp")).convert("RGB")

# cases (gauche, haut, droite, bas) ; la 3e rangée est découpée autrement
L1, L2, L3 = (0, 358), (363, 668), (674, 1024)
CASES = {
    1: (0, L1[0], 506, L1[1]),    2: (512, L1[0], 1021, L1[1]),  3: (1027, L1[0], 1536, L1[1]),
    4: (0, L2[0], 506, L2[1]),    5: (512, L2[0], 1021, L2[1]),  6: (1027, L2[0], 1536, L2[1]),
    7: (0, L3[0], 506, L3[1]),    8: (512, L3[0], 1061, L3[1]),  9: (1068, L3[0], 1536, L3[1]),
}


def case(n):
    return planche.crop(CASES[n])


def recadrer(img, ratio, centre_x=0.5, haut=0.0):
    """Recadre au ratio largeur/hauteur voulu, centré horizontalement sur centre_x (0–1)."""
    w, h = img.size
    if w / h > ratio:  # trop large : on rogne les côtés
        nw = round(h * ratio)
        x = min(max(round(w * centre_x - nw / 2), 0), w - nw)
        return img.crop((x, 0, x + nw, h))
    nh = round(w / ratio)
    y = round((h - nh) * haut)
    return img.crop((0, y, w, y + nh))


def enregistrer(img, nom, largeur=None):
    if largeur and img.width < largeur:  # léger agrandissement pour les petites cases
        img = img.resize((largeur, round(img.height * largeur / img.width)), Image.LANCZOS)
    img.save(os.path.join(SORTIE, nom), quality=88, optimize=True, progressive=True)
    print(nom, img.size)


os.makedirs(SORTIE, exist_ok=True)
# 03 Accompagnement : format 3:2 des onglets
enregistrer(recadrer(case(2), 3 / 2), "accompagnement-audit.jpg")
enregistrer(recadrer(case(1), 3 / 2), "accompagnement-recommandations.jpg")
enregistrer(recadrer(case(4), 3 / 2), "accompagnement-suivi.jpg")
# 04 Qui suis-je : portrait et trois conférences
enregistrer(recadrer(case(5), 4 / 3, centre_x=0.45), "ana-portrait.jpg")
enregistrer(recadrer(case(3), 4 / 3, centre_x=1.0), "ana-conference-1.jpg")
enregistrer(recadrer(case(6), 4 / 3, centre_x=0.6), "ana-conference-2.jpg")
enregistrer(recadrer(case(8), 4 / 3, centre_x=0.62), "ana-conference-3.jpg")
# 05 Mon réseau : carte d'Ana, format des cartes de l'équipe (416 × 467)
enregistrer(recadrer(case(9), 416 / 467, centre_x=0.55), "ana-reseau.jpg", largeur=416)
