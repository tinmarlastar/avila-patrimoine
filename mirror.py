import re, os, urllib.request, urllib.parse
BASE = "https://studiova-agency-business-bootstrap-template-v2.21st.app/"
HOST = urllib.parse.urlparse(BASE).netloc
OUT = os.path.dirname(os.path.abspath(__file__))
seen, queue, failed = set(), [BASE + "index.html"], []
ATTR = re.compile(r'(?:href|src|data-src|poster)\s*=\s*["\']([^"\'#]+)', re.I)
CSSURL = re.compile(r'url\(\s*["\']?([^"\')]+)["\']?\s*\)', re.I)
while queue:
    url = urllib.parse.urldefrag(queue.pop())[0].split("?")[0]
    if url in seen: continue
    seen.add(url)
    p = urllib.parse.urlparse(url)
    if p.netloc != HOST: continue
    path = p.path.lstrip("/") or "index.html"
    if path.endswith("/"): path += "index.html"
    try:
        data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read()
    except Exception as e:
        failed.append((url, str(e))); continue
    dest = os.path.join(OUT, "site", path)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, "wb").write(data)
    if path.endswith((".html", ".css", ".js")) :
        text = data.decode("utf-8", "ignore")
        refs = CSSURL.findall(text) if path.endswith(".css") else ATTR.findall(text) + CSSURL.findall(text) if path.endswith(".html") else []
        for r in refs:
            if r.startswith(("data:", "mailto:", "tel:", "javascript:")): continue
            queue.append(urllib.parse.urljoin(url, r.strip()))
print(len(seen), "URLs vues;", len(failed), "échecs")
for f in failed: print("  ", *f)
