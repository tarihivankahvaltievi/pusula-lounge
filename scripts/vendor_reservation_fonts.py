from pathlib import Path
import urllib.request, urllib.parse, re, sys
sys.path.insert(0,str(Path(__file__).parent))
# Only the heading/caption characters are needed; keep CJK downloads small.
# Importing the static builder is intentionally avoided because it writes output.
import ast
module=ast.parse((Path(__file__).parent/'build_reservations.py').read_text())
node=next(n.value for n in module.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='COPY' for t in n.targets))
copy=eval(compile(ast.Expression(node), '<copy>', 'eval'), {'__builtins__':{}, 'dict':dict})
root=Path(sys.argv[1]); folder=root/'rezervasyon/fonts';folder.mkdir(exist_ok=True)
rules=[]
for lang,family,slug in [('ru','Noto Serif','notoserif'),('ar','Noto Naskh Arabic','notonaskharabic'),('ko','Noto Serif KR','notoserifkr'),('zh','Noto Serif SC','notoserifsc')]:
    chars=''.join(copy[lang][k] for k in ['heading','photo','faqTitle','ready'])
    params=urllib.parse.urlencode({'family':family+':wght@400','text':''.join(sorted(set(chars))),'display':'swap'})
    source='https://fonts.googleapis.com/css2?'+params
    req=urllib.request.Request(source,headers={'User-Agent':'Mozilla/5.0'})
    css=urllib.request.urlopen(req).read().decode()
    font_url=re.search(r'url\((https:[^)]+)\)',css).group(1)
    data=urllib.request.urlopen(font_url).read()
    ext='woff2' if data[:4]==b'wOF2' else 'ttf'
    name=slug+'.'+ext;(folder/name).write_bytes(data)
    license_url=f'https://raw.githubusercontent.com/google/fonts/main/ofl/{slug}/OFL.txt'
    (folder/(slug+'-OFL.txt')).write_bytes(urllib.request.urlopen(license_url).read())
    rules.append(f"@font-face{{font-family:'{family}';font-weight:400;font-style:normal;font-display:swap;src:url('./fonts/{name}') format('{ 'woff2' if ext=='woff2' else 'truetype'}')}}")
    print(lang,family,len(data),'bytes')
(folder/'SOURCES.txt').write_text('Reservation display fonts from Google Fonts, licensed under SIL Open Font License 1.1.\nEach font is subset to the localized headings and captions; see adjacent license files.\nhttps://fonts.google.com/\n')
cssfile=root/'rezervasyon/reservation.css';current=re.sub(r"@font-face\{font-family:'(?:Noto Serif|Noto Naskh Arabic|Noto Serif KR|Noto Serif SC)';[^}]*\}\n?", '', cssfile.read_text());cssfile.write_text('\n'.join(rules)+'\n'+current.replace("font-family:Georgia,'Times New Roman',serif", "font-family:'Noto Serif',Georgia,serif"))
