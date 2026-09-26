// Vidéo de fond de l'accueil : une vidéo différente à chaque chargement.
// Déposer les fichiers dans assets/videos/ en les numérotant sans trou :
// accueil-1.mp4, accueil-2.mp4, accueil-3.mp4… Le script détecte ceux qui existent.
(function () {
  var DOSSIER = "../assets/videos/accueil-";
  var MAX = 20;                 // numéros testés : accueil-1 à accueil-20
  var CLE = "video-accueil-derniere";
  var video = document.querySelector("video[data-video-accueil]");
  if (!video) return;

  function existe(n) {
    return fetch(DOSSIER + n + ".mp4", { method: "HEAD" })
      .then(function (r) { return r.ok ? n : null; })
      .catch(function () { return null; });
  }

  var essais = [];
  for (var n = 1; n <= MAX; n++) essais.push(existe(n));

  Promise.all(essais).then(function (res) {
    var dispo = res.filter(function (n) { return n !== null; });
    if (!dispo.length) return;
    var derniere = null;
    try { derniere = localStorage.getItem(CLE); } catch (e) {}
    // jamais la même vidéo deux fois de suite (quand il y en a au moins deux)
    var choix = dispo.length > 1 ? dispo.filter(function (n) { return String(n) !== derniere; }) : dispo;
    var n = choix[Math.floor(Math.random() * choix.length)];
    try { localStorage.setItem(CLE, String(n)); } catch (e) {}
    video.src = DOSSIER + n + ".mp4";
    var lecture = video.play();
    if (lecture && lecture.catch) lecture.catch(function () {});
  });
})();
