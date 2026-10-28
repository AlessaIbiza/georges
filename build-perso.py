# Fabrique la page perso « Mon assiette » (mes-proteines/) à partir de Georges.
# À relancer après chaque modification de index.html :  python3 build-perso.py
import json, re
h = open('index.html', encoding='utf-8').read()
def rep(a, b):
    global h
    assert a in h, a
    h = h.replace(a, b)
rep('<meta charset="utf-8">', '<meta charset="utf-8">\n<script>window.PERSO_MODE=1</script>')
rep('<meta name="apple-mobile-web-app-title" content="Georges">', '<meta name="apple-mobile-web-app-title" content="Mon assiette">')
rep('href="icon.png?v=7"', 'href="icon.png?v=1"')
h = re.sub(r'<link rel="icon" href="icon-512.png\?v=\d+">', '<link rel="icon" href="icon.png?v=1">', h)
rep('fetch("version.json?t="', 'fetch("../version.json?t="')
rep('<h1>Georges</h1>', '<h1>Mon assiette</h1>')
if '<title>' in h:
    h = re.sub(r'<title>.*?</title>', '<title>Mon assiette</title>', h, count=1)
else:
    h = h.replace('</head>', '<title>Mon assiette</title></head>', 1) if '</head>' in h else h.replace('<script>window.PERSO_MODE=1</script>', '<script>window.PERSO_MODE=1</script>\n<title>Mon assiette</title>', 1)
open('mes-proteines/index.html', 'w', encoding='utf-8').write(h)
json.dump({"id": "/mes-proteines/", "name": "Mon assiette", "short_name": "Mon assiette", "start_url": "./", "scope": "./",
           "display": "standalone", "background_color": "#eaf6f6", "theme_color": "#0a8379",
           "icons": [{"src": "icon-192.png?v=1", "sizes": "192x192", "type": "image/png", "purpose": "any"},
                     {"src": "icon.png?v=1", "sizes": "512x512", "type": "image/png", "purpose": "any"}]},
          open('mes-proteines/manifest.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('mes-proteines/index.html régénéré')
