"""Builds the TADAWA telemedicine guide into one self-contained file.
   python build.py   ->  index.html (open directly)  +  dist/TadawaTelemedicineGuide.html (artifact body)
   Sources: src/guide.src.html, src/img/*, Tadawa fonts and logos from the html-deck-publisher skill,
   Phosphor fonts from the Tadawa design system bundle.css (path in PHOSPHOR_CSS or src/phosphor.css)."""
import base64, io, os, re, sys
here = os.path.dirname(os.path.abspath(__file__))
skill = os.path.expanduser("~/.claude/skills/html-deck-publisher/assets/tadawa")
def b64(path, mime):
    return "data:%s;base64,%s" % (mime, base64.b64encode(open(path, "rb").read()).decode())
src = open(os.path.join(here, "src", "guide.src.html"), encoding="utf-8").read()
css = open(os.path.join(here, "src", "phosphor.css"), encoding="utf-8").read()
faces = "\n".join(re.findall(r'@font-face\{font-family:"Phosphor(?:-Fill)?";[^}]*\}', css))
names = sorted(set(re.findall(r'ph(?:-fill)? (ph-[a-z0-9-]+)', src)))
rules = []
for n in names:
    m = re.search(r'\.ph\.' + re.escape(n) + r':before\s*\{\s*content:\s*"(\\[0-9a-fA-F]+)"', css)
    if not m: sys.exit("icon not in Phosphor: " + n)
    rules.append('.%s::before{content:"%s"}' % (n, m.group(1)))
rep = {
    "FONT_MADANI_REG": b64(os.path.join(skill, "fonts", "MadaniArabic-Regular.ttf"), "font/ttf"),
    "FONT_MADANI_BOLD": b64(os.path.join(skill, "fonts", "MadaniArabic-Bold.ttf"), "font/ttf"),
    "PHOSPHOR_FACES": faces, "ICON_RULES": "\n".join(rules),
    "LOGO_COLOR": b64(os.path.join(skill, "img", "logo-color.svg"), "image/svg+xml"),
    "LOGO_WHITE": b64(os.path.join(skill, "img", "logo-white.svg"), "image/svg+xml"),
    "SHOT_EN": b64(os.path.join(here, "src", "img", "app-home-en.jpg"), "image/jpeg"),
    "SHOT_AR": b64(os.path.join(here, "src", "img", "app-home-ar.jpg"), "image/jpeg"),
}
MIME = {".webp": "image/webp", ".png": "image/png", ".jpg": "image/jpeg", ".svg": "image/svg+xml"}
out = re.sub(r"\{\{IMG:([\w.-]+)\}\}", lambda m: b64(os.path.join(here, "src", "img", m.group(1)), MIME[os.path.splitext(m.group(1))[1]]), src)
out = re.sub(r"\{\{([A-Z_]+)\}\}", lambda m: rep[m.group(1)], out)
head, body = out.split("<!--BODY-->")
os.makedirs(os.path.join(here, "dist"), exist_ok=True)
open(os.path.join(here, "dist", "TadawaTelemedicineGuide.html"), "w", encoding="utf-8").write(head + body)
full = ('<!doctype html>\n<html lang="en" dir="ltr">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        '<style>[hidden]{display:none!important}img{max-width:100%}</style>\n' + head + '</head>\n<body>\n' + body + '\n</body>\n</html>\n')
open(os.path.join(here, "index.html"), "w", encoding="utf-8").write(full)
print("icons:", len(names), "| index.html", len(full) // 1024, "KB")
