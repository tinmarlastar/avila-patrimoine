// Défilement aimanté : quand on s'arrête de défiler près du début d'une section,
// la page se cale pour que cette section commence juste sous le menu fixe.
// Au milieu d'une longue section, on laisse lire tranquillement.
(function () {
  var SEUIL = 0.25;  // distance max (part de la hauteur de fenêtre) pour aimanter
  var DUREE = 900;   // durée du recalage en ms : plus c'est long, plus l'attraction est douce
  if (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  var anim = null, finAnim = 0, minuterie;

  // Hauteur du menu une fois fixé (padding 20px en haut et en bas), même pendant
  // sa transition de 0,5 s depuis la version haute (padding 28px).
  function hauteurMenu() {
    var h = document.querySelector("header.position-fixed, header");
    if (!h) return 0;
    var cs = getComputedStyle(h);
    return h.offsetHeight - parseFloat(cs.paddingTop) - parseFloat(cs.paddingBottom) + 40;
  }

  // lent au départ, lent à l'arrivée
  function douceur(t) { return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }

  function stopper() {
    if (anim) { cancelAnimationFrame(anim); anim = null; }
  }

  function glisser(distance) {
    var depart = window.scrollY, t0 = null;
    function pas(t) {
      if (t0 === null) t0 = t;
      var p = Math.min((t - t0) / DUREE, 1);
      window.scrollTo({ top: depart + distance * douceur(p), behavior: "instant" });
      if (p < 1) anim = requestAnimationFrame(pas);
      else { anim = null; finAnim = Date.now(); }
    }
    anim = requestAnimationFrame(pas);
  }

  function aimanter() {
    if (anim) return;                                  // notre glissement est en cours
    if (Date.now() - finAnim < 250) return;           // fin de notre propre glissement
    var doc = document.documentElement;
    if (window.scrollY + window.innerHeight >= doc.scrollHeight - 2) return; // tout en bas : pied de page
    var haut = hauteurMenu(), meilleur = null;
    document.querySelectorAll("section").forEach(function (s) {
      var ecart = s.getBoundingClientRect().top - (s.classList.contains("banner-section") ? 0 : haut);
      if (meilleur === null || Math.abs(ecart) < Math.abs(meilleur)) meilleur = ecart;
    });
    if (meilleur === null || Math.abs(meilleur) < 2 || Math.abs(meilleur) > window.innerHeight * SEUIL) return;
    glisser(meilleur);
  }

  // l'utilisateur reprend la main : on lâche immédiatement
  ["wheel", "touchstart", "keydown", "mousedown"].forEach(function (e) {
    window.addEventListener(e, function () { stopper(); }, { passive: true });
  });

  if ("onscrollend" in window) {
    window.addEventListener("scrollend", aimanter);
  } else { // Safari : pas d'événement scrollend, on attend la fin du défilement
    window.addEventListener("scroll", function () {
      clearTimeout(minuterie);
      minuterie = setTimeout(aimanter, 150);
    }, { passive: true });
  }
})();
