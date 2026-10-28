"""Subset existing OFL home fonts without changing their outlines or metrics.

Requires fonttools[woff]. Original licensed fonts are retained as build inputs;
optimized derivatives use Pusula internal names and retain copyright/licenses.
"""
from pathlib import Path
import hashlib,json,re,sys
from bs4 import BeautifulSoup
from fontTools import subset
from fontTools.ttLib import TTFont

ROOT=Path(sys.argv[1]).resolve()
text=''.join(chr(n) for n in range(32,127))+'₺→←↑↓›‹·–—…‘’“”×'
for page in ROOT.rglob('index.html'):
    if '.git' in page.parts:continue
    soup=BeautifulSoup(page.read_text(),'html.parser')
    for script in soup.select('script,style'):script.decompose()
    text+=soup.get_text(' ',strip=True)
    for tag in soup.select('[aria-label],[alt],[title]'):
        text+=''.join(tag.get(name,'') for name in ['aria-label','alt','title'])
points=set(map(ord,text))
folder=ROOT/'assets/fonts/optimized';folder.mkdir(exist_ok=True)
mapping={};report=[]
for source in sorted((ROOT/'assets/fonts').glob('*.woff2')):
    font=TTFont(source,recalcTimestamp=False)
    cmap=font.getBestCmap()
    wanted=points.intersection(cmap)
    original_metrics={p:font['hmtx'].metrics[cmap[p]][0] for p in wanted}
    family=font['name'].getDebugName(1)
    options=subset.Options()
    options.flavor='woff2';options.glyph_names=True
    options.name_IDs=['*'];options.name_legacy=True;options.name_languages=['*']
    subsetter=subset.Subsetter(options=options)
    subsetter.populate(unicodes=wanted)
    subsetter.subset(font)
    name='Pusula F'+source.stem
    for record in font['name'].names:
        if record.nameID in [1,3,4,6,16,18,21,25]:
            record.string=name.encode(record.getEncoding())
    font.flavor='woff2'
    output=folder/source.name
    font.save(output,reorderTables=True)
    result=TTFont(output)
    result_map=result.getBestCmap()
    assert wanted.issubset(result_map),'Lost codepoints: '+source.name
    assert all(result['hmtx'].metrics[result_map[p]][0]==width for p,width in original_metrics.items()),'Changed glyph advance'
    digest=hashlib.sha256(output.read_bytes()).hexdigest()[:12]
    mapping[source.name]=f'optimized/{source.name}?v={digest}'
    report.append({'source':source.relative_to(ROOT).as_posix(),'output':output.relative_to(ROOT).as_posix(),'originalFamily':family,'originalBytes':source.stat().st_size,'optimizedBytes':output.stat().st_size,'supportedCharacters':len(wanted),'metricsPreserved':True})
for file in [ROOT/'assets/home.css',ROOT/'styles.css',ROOT/'assets/fonts/site-fonts.css']:
    current=file.read_text()
    for name,replacement in mapping.items():
        current=re.sub(r'(?:optimized/)?'+re.escape(name)+r'(?:\?v=[a-f0-9]+)?',replacement,current)
    file.write_text(current)
(folder/'manifest.json').write_text(json.dumps({'corpus':'Published page text, accessible labels, printable ASCII and UI punctuation','originalsRetained':True,'fonts':report},ensure_ascii=False,indent=2)+'\n')
print('Home font sources:',sum(f['originalBytes'] for f in report),'→',sum(f['optimizedBytes'] for f in report),'bytes; outlines/advance widths retained.')
