// Sélecteur de thème : un carré de couleur en haut à droite, quatre palettes.
(function () {
  var THEMES = [
    { id: "original", name: "Original Studiova", dark: "#1F2A2E", accent: "#C1FF72" },
    { id: "ocean", name: "Océan profond", dark: "#0B1F3A", accent: "#4FC3F7" },
    { id: "graphite", name: "Graphite et orange", dark: "#151515", accent: "#FF6B2C" },
    { id: "violet", name: "Violet électrique", dark: "#16132B", accent: "#A78BFA" }
  ];
  var KEY = "studiova-theme";
  var root = document.documentElement;

  function saved() {
    try { return localStorage.getItem(KEY) || "original"; } catch (e) { return "original"; }
  }
  function find(id) {
    return THEMES.filter(function (t) { return t.id === id; })[0] || THEMES[0];
  }

  // Appliqué dès le <head> pour éviter un flash de l'ancien thème.
  root.setAttribute("data-theme", find(saved()).id);

  // Les SVG (logo, feuilles, icônes) ont les couleurs d'origine en dur : on les recolore.
  var svgCache = {};
  function recolorSvgs(theme) {
    document.querySelectorAll('img[src$=".svg"], img[data-svg-src]').forEach(function (img) {
      var src = img.getAttribute("data-svg-src") || img.getAttribute("src");
      img.setAttribute("data-svg-src", src);
      var load = svgCache[src] || (svgCache[src] = fetch(src).then(function (r) { return r.text(); }));
      load.then(function (text) {
        if (!/#C1FF72|#1F2A2E/i.test(text)) return;
        if (theme.id === "original") { img.src = src; return; }
        var out = text.replace(/#C1FF72/gi, theme.accent).replace(/#1F2A2E/gi, theme.dark);
        img.src = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(out);
      }).catch(function () {});
    });
  }

  function apply(id) {
    var theme = find(id);
    root.setAttribute("data-theme", theme.id);
    try { localStorage.setItem(KEY, theme.id); } catch (e) {}
    var swatch = document.querySelector(".theme-switch-btn");
    if (swatch) swatch.style.setProperty("--sw-accent", theme.accent);
    document.querySelectorAll(".theme-switch-item").forEach(function (el) {
      el.setAttribute("aria-checked", el.dataset.theme === theme.id ? "true" : "false");
    });
    recolorSvgs(theme);
  }

  var CSS =
    ".theme-switch{position:relative}" +
    ".theme-switch-btn{width:45px;height:45px;border-radius:10px;border:2px solid #fff;cursor:pointer;padding:0;" +
    "background:linear-gradient(135deg,var(--sw-accent) 50%,var(--th-dark) 50%);box-shadow:0 2px 8px rgba(0,0,0,.25);transition:transform .15s}" +
    ".theme-switch-btn:hover{transform:scale(1.06)}" +
    ".theme-switch-menu{position:absolute;right:0;top:56px;background:#fff;border-radius:12px;padding:8px;min-width:230px;" +
    "box-shadow:0 12px 32px rgba(0,0,0,.18);display:none;z-index:2000}" +
    ".theme-switch.open .theme-switch-menu{display:block}" +
    ".theme-switch-item{display:flex;align-items:center;gap:12px;width:100%;border:0;background:none;padding:8px 10px;" +
    "border-radius:8px;font:inherit;font-size:15px;color:#1f2a2e;cursor:pointer;text-align:left}" +
    ".theme-switch-item:hover{background:#f2f4f5}" +
    ".theme-switch-item[aria-checked=true]{background:#eceff1;font-weight:600}" +
    ".theme-switch-item span{width:26px;height:26px;border-radius:6px;flex:none;border:1px solid rgba(0,0,0,.1)}" +
    ".theme-switch-fixed{position:fixed;top:20px;right:20px;z-index:2000}";

  function build() {
    var style = document.createElement("style");
    style.textContent = CSS;
    document.head.appendChild(style);

    var wrap = document.createElement("div");
    wrap.className = "theme-switch";
    wrap.innerHTML =
      '<button type="button" class="theme-switch-btn" aria-haspopup="true" aria-expanded="false" aria-label="Changer de thème" title="Changer de thème"></button>' +
      '<div class="theme-switch-menu" role="radiogroup" aria-label="Thèmes">' +
      THEMES.map(function (t) {
        return '<button type="button" role="radio" class="theme-switch-item" data-theme="' + t.id + '">' +
          '<span style="background:linear-gradient(135deg,' + t.accent + ' 50%,' + t.dark + ' 50%)"></span>' + t.name + "</button>";
      }).join("") +
      "</div>";

    // Dans l'en-tête, juste avant le bouton menu ; sinon, flottant en haut à droite.
    var slot = document.querySelector(".header-wrapper > .d-flex");
    if (slot) slot.insertBefore(wrap, slot.firstChild);
    else { wrap.classList.add("theme-switch-fixed"); document.body.appendChild(wrap); }

    var btn = wrap.querySelector(".theme-switch-btn");
    function toggle(open) {
      wrap.classList.toggle("open", open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    }
    btn.addEventListener("click", function (e) { e.stopPropagation(); toggle(!wrap.classList.contains("open")); });
    wrap.querySelectorAll(".theme-switch-item").forEach(function (el) {
      el.addEventListener("click", function () { apply(el.dataset.theme); toggle(false); });
    });
    document.addEventListener("click", function (e) { if (!wrap.contains(e.target)) toggle(false); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") toggle(false); });

    apply(saved());
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", build);
  else build();
})();
