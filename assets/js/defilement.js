// Défilement aimanté : quand on s'arrête de défiler près du début d'une section,
// la page se cale pour que cette section commence juste sous le menu fixe.
// Au milieu d'une longue section, on laisse lire tranquillement.
(function () {
  var SEUIL = 0.25; // distance max (part de la hauteur de fenêtre) pour aimanter
  if (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  var enCours = false, minuterie;

  function hauteurMenu() {
    var h = document.querySelector("header.position-fixed, header");
    return h ? h.offsetHeight : 0;
  }

  function aimanter() {
    if (enCours) { enCours = false; return; } // fin de notre propre défilement
    var doc = document.documentElement;
    if (window.scrollY + window.innerHeight >= doc.scrollHeight - 2) return; // tout en bas : pied de page
    var haut = hauteurMenu(), meilleur = null;
    document.querySelectorAll("section").forEach(function (s) {
      var ecart = s.getBoundingClientRect().top - (s.classList.contains("banner-section") ? 0 : haut);
      if (meilleur === null || Math.abs(ecart) < Math.abs(meilleur)) meilleur = ecart;
    });
    if (meilleur === null || Math.abs(meilleur) < 2 || Math.abs(meilleur) > window.innerHeight * SEUIL) return;
    enCours = true;
    window.scrollBy({ top: meilleur, behavior: "smooth" });
  }

  if ("onscrollend" in window) {
    window.addEventListener("scrollend", aimanter);
  } else { // Safari : pas d'événement scrollend, on attend la fin du défilement
    window.addEventListener("scroll", function () {
      clearTimeout(minuterie);
      minuterie = setTimeout(aimanter, 150);
    }, { passive: true });
  }
})();
