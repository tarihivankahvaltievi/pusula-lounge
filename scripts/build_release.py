"""Rebuild the static release in its dependency order; never publishes or pushes."""
from pathlib import Path
import subprocess,sys
root=Path(sys.argv[1]).resolve()
for name in ['build_tourism_seo.py','build_reservations.py','build_international_seo.py','optimize_home_fonts.py','build_blog_design.py','build_visitor_quality.py']:
    subprocess.run([sys.executable,str(Path(__file__).parent/name),str(root)],check=True)
print('Static release rebuilt. Run the SEO and browser checks before publishing.')
