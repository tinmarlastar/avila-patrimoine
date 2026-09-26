# Extrait les textes visibles de chaque page, dans l'ordre, avec leur balise.
import html.parser, os, json, re
SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs")
SKIP = {"script", "style", "noscript", "svg", "iconify-icon"}
class P(html.parser.HTMLParser):
    def __init__(s):
        super().__init__(); s.stack=[]; s.out=[]; s.zone="corps"
    def handle_starttag(s, t, a):
        a=dict(a)
        if t=="header": s.zone="en-tête"
        if t=="footer": s.zone="pied de page"
        if t in ("img","input","textarea") or t=="meta":
            for k in ("alt","placeholder"):
                if a.get(k) and not re.fullmatch(r"(logo|img|image)?", a[k].strip(), re.I): s.out.append((s.zone,f"{t}[{k}]",a[k].strip()))
            if t=="meta" and a.get("name")=="description": s.out.append(("meta","description",a.get("content","")))
        if t not in ("img","input","meta","link","br","hr","source"): s.stack.append(t)
    def handle_endtag(s, t):
        if t in s.stack:
            while s.stack and s.stack.pop()!=t: pass
        if t in ("header","footer"): s.zone="corps"
    def handle_data(s, d):
        d=" ".join(d.split())
        if not d or any(x in SKIP for x in s.stack): return
        tag=next((x for x in reversed(s.stack) if x in("title","h1","h2","h3","h4","h5","h6","p","a","button","li","span","label","option","blockquote","th","td")), s.stack[-1] if s.stack else "?")
        if s.out and s.out[-1][1]==tag and s.out[-1][0]==s.zone and tag in("p","li"):  # fusionne les morceaux d'une même phrase
            pass
        s.out.append(("head" if tag=="title" else s.zone, tag, d))
res={}
for f in sorted(os.listdir(SITE)):
    if f.endswith(".html"):
        p=P(); p.feed(open(os.path.join(SITE,f),encoding="utf-8").read()); res[f]=p.out
json.dump(res, open(os.path.join(os.path.dirname(__file__),"textes.json"),"w"), ensure_ascii=False, indent=1)
for f,v in res.items(): print(f, len(v), sum(1 for z,_,_ in v if z=="en-tête"), sum(1 for z,_,_ in v if z=="pied de page"))
