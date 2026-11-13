"""Install the consent-controlled Ads tag on campaign entry and booking pages."""
import base64
import hashlib
import json
from pathlib import Path
import re
import sys

root = Path(sys.argv[1]).resolve()
digest = hashlib.sha256((root / 'ads-measurement.js').read_bytes())
integrity = 'sha256-' + base64.b64encode(digest.digest()).decode()
script = (
    f'<script src="/ads-measurement.js?v={digest.hexdigest()[:12]}" '
    f'integrity="{integrity}" crossorigin="anonymous" defer></script>'
)
pages = (
    'index.html', 'kahvalti/index.html', 'menu/index.html',
    'kahvalti-rehberi/index.html', 'konum/index.html', 'rezervasyon/index.html',
    'en/index.html', 'en/breakfast/index.html', 'en/menu/index.html', 'en/reservation/index.html',
    'ru/index.html', 'ru/menu/index.html', 'ru/reservation/index.html',
    'ar/index.html', 'ar/menu/index.html', 'ar/reservation/index.html',
)
for name in pages:
    page = root / name
    original = page.read_text()
    updated = re.sub(r'<script src="/ads-measurement\.js\?[^"]*"[^>]*></script>\n?', '', original)
    updated = updated.replace('</head>', script + '\n</head>', 1)
    if updated != original:
        page.write_text(updated)

config = root / 'vercel.json'
settings = json.loads(config.read_text())
google_tag = 'https://www.googletagmanager.com'
google_ads = 'https://www.googleadservices.com'
google = ('https://www.google.com', 'https://www.google.com.tr')
measurement = (
    google_tag, google_ads, 'https://googleads.g.doubleclick.net',
    'https://pagead2.googlesyndication.com', *google,
)
for group in settings['headers']:
    for header in group['headers']:
        if header['key'] != 'Content-Security-Policy':
            continue
        directives = {}
        for directive in header['value'].split(';'):
            name, *sources = directive.strip().split()
            directives[name] = sources
        script_hosts = (google_tag, google_ads, google[0])
        for name, sources in {
            'script-src': (f"'{integrity}'", *script_hosts),
            'img-src': measurement,
            'connect-src': (*measurement, 'https://ad.doubleclick.net'),
            'frame-src': (google_tag,),
        }.items():
            existing = [source for source in directives.get(name, []) if source != "'none'"]
            directives[name] = list(dict.fromkeys(existing + list(sources)))
        header['value'] = '; '.join(' '.join([name, *sources]) for name, sources in directives.items())
config.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + '\n')
