"""Rebuild in dependency order; preserve lastmod on unchanged final pages."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import subprocess, sys, xml.etree.ElementTree as ET

root = Path(sys.argv[1]).resolve()
namespace = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
before = {p: p.read_bytes() for p in root.rglob('index.html') if '.git' not in p.parts}
old_dates = {u.find(namespace+'loc').text: u.findtext(namespace+'lastmod')
             for u in ET.parse(root/'sitemap.xml').getroot()}
for name in ['build_tourism_seo.py', 'build_reservations.py', 'build_international_seo.py',
             'build_blog_design.py', 'build_search_growth.py', 'optimize_home_fonts.py', 'build_visitor_quality.py',
             'finalize_search_metadata.py']:
    subprocess.run([sys.executable, str(Path(__file__).parent/name), str(root)], check=True)
from urllib.parse import urlsplit
tree = ET.parse(root/'sitemap.xml')
for prefix, uri in [('', namespace[1:-1]), ('xhtml', 'http://www.w3.org/1999/xhtml'),
                    ('image', 'http://www.google.com/schemas/sitemap-image/1.1')]:
    ET.register_namespace(prefix, uri)
for entry in tree.getroot():
    url = entry.find(namespace+'loc').text
    file = root/urlsplit(url).path.lstrip('/')/'index.html'
    lastmod = entry.find(namespace+'lastmod')
    if lastmod is None:
        lastmod = ET.SubElement(entry, namespace+'lastmod')
    lastmod.text = (old_dates[url] if before.get(file) == file.read_bytes() and old_dates.get(url)
                    else datetime.now(ZoneInfo('Europe/Istanbul')).date().isoformat())
ET.indent(tree, space='  ')
tree.write(root/'sitemap.xml', encoding='unicode', xml_declaration=True)
print('Static release rebuilt. Run the SEO and browser checks before publishing.')
