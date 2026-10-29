"""Clarify shared-portion costs in crawlable, progressively disclosed menu HTML.

Run after translated menus and before font/integrity finalization. The Turkish
published menu is the only price source; per-person values are calculations,
never new Offers or promises of individually orderable portions.
"""
from decimal import Decimal, ROUND_HALF_UP
from html import escape
from pathlib import Path
import re, sys
from bs4 import BeautifulSoup

ROOT = Path(sys.argv[1]).resolve()
source = BeautifulSoup((ROOT/'menu/index.html').read_text(), 'html.parser')
portions = [(int(row.small.get_text().split()[0]), int(re.sub(r'\D', '', row.b.get_text())))
            for row in source.select('#serpme-van-kahvaltisi .portion-prices > span')]
assert [n for n, _ in portions] == [2, 3, 4], 'Review shared portion changes'
assert all(price > 0 for _, price in portions), 'Invalid menu price'
copy = {
 'tr': ['Serpme kahvaltı fiyatı toplam mı, kişi başı mı?', 'Serpme Van kahvaltısı: bütçenizi karşılaştırın', ['Kişi', 'Porsiyon toplamı', 'Kişi başına düşen'], 'Menü fiyatı porsiyonun toplamıdır. Kişi başına tutar, toplamın kişi sayısına bölünmesiyle hesaplanır; ayrı satılan bir menü değildir. İlave siparişler dahil değildir.', 'Sınırsız çay serpme kahvaltı içeriğinde listelenir. Güncel fiyatı, ilaveleri ve ürün uygunluğunu sipariş öncesinde ekibimizle teyit edin.', 'Serpme kahvaltının tüm içeriği', 'Tek kişilik kahvaltı tabağı'],
 'en': ['Is the shared breakfast price total or per person?', 'Shared Van breakfast: compare your budget', ['People', 'Portion total', 'Per person'], 'The menu price is the total for the shared portion. The per-person amount is calculated by dividing the total by the number of people; it is not a separately sold menu. Extras are not included.', 'Unlimited tea is listed with the shared breakfast. Confirm current prices, extras and availability with our team before ordering.', 'Full shared breakfast contents', 'Individual breakfast plate'],
 'ru': ['Цена завтрака указана за всех или за человека?', 'Ванский завтрак: сравните стоимость', ['Гостей', 'За всю порцию', 'На человека'], 'В меню указана цена за всю порцию. Сумма на человека рассчитана делением общей цены на число гостей; это не отдельный набор для заказа. Дополнительные блюда не включены.', 'В состав общего завтрака входит чай без ограничений. Перед заказом уточните у команды актуальные цены, дополнения и наличие блюд.', 'Полный состав общего завтрака', 'Завтрак на одного'],
 'ar': ['هل سعر الفطور المشترك إجمالي أم للفرد؟', 'فطور فان المشترك: قارن التكلفة', ['الأشخاص', 'إجمالي الوجبة', 'لكل شخص'], 'السعر في القائمة هو إجمالي الوجبة المشتركة. تُحسب تكلفة الفرد بقسمة الإجمالي على عدد الأشخاص، وليست وجبة مستقلة يمكن طلبها. الطلبات الإضافية غير مشمولة.', 'يشمل الفطور المشترك الشاي بلا حدود حسب القائمة. يرجى تأكيد الأسعار الحالية والإضافات وتوفر الأطباق مع فريقنا قبل الطلب.', 'مكونات الفطور المشترك كاملة', 'طبق فطور لشخص واحد'],
}
def money(value, lang):
    value = Decimal(value).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
    formatted = f'{value:,.2f}'.rstrip('0').rstrip('.')
    if lang == 'tr':
        formatted = formatted.replace(',', '_').replace('.', ',').replace('_', '.')
    return '<bdi dir="ltr">'+formatted+' TL</bdi>'

for lang, (summary, caption, columns, note, tea, shared, solo) in copy.items():
    route = 'menu/index.html' if lang == 'tr' else lang+'/menu/index.html'
    file = ROOT/route
    text = re.sub(r'<!-- MENU-BUDGET:START -->.*?<!-- MENU-BUDGET:END -->', '', file.read_text(), flags=re.S)
    rows = ''.join('<tr><th scope="row">'+str(n)+'</th><td>'+money(price, lang)+'</td><td>'+money(Decimal(price)/n, lang)+'</td></tr>' for n, price in portions)
    block = ('<!-- MENU-BUDGET:START --><details class="menu-budget" id="shared-breakfast-budget"><summary>'+escape(summary)+'</summary>'
             '<div class="menu-budget-body"><table><caption>'+escape(caption)+'</caption><thead><tr>'
             +''.join('<th scope="col">'+escape(c)+'</th>' for c in columns)+'</tr></thead><tbody>'+rows+'</tbody></table>'
             '<p>'+escape(note)+'</p><p>'+escape(tea)+'</p><nav aria-label="'+escape(caption)+'">'
             '<a href="#serpme-van-kahvaltisi">'+escape(shared)+'</a><a href="#kahvalti-tabagi">'+escape(solo)+'</a>'
             '</nav></div></details><!-- MENU-BUDGET:END -->')
    # Keep the primary request/directions actions before this optional comparison.
    marker = '<!-- MENU-VISIT:END -->' if lang == 'tr' else '<!-- MENU-ACTIONS:END -->'
    # International actions are produced later in the existing pipeline. Anchor
    # directly after the intro instead; visitor-quality inserts actions before us.
    if lang == 'tr':
        assert marker in text
        text = text.replace(marker, marker+block, 1)
    else:
        intro = re.search(r'<(?:header|div) class="visit-intro">.*?</(?:header|div)>', text, re.S)
        assert intro, route
        text = text[:intro.end()]+block+text[intro.end():]
    text = re.sub(r'<link\b[^>]*href="/menu-budget.css(?:\?[^\"]*)?"[^>]*>', '', text)
    file.write_text(text.replace('</head>', '<link rel="stylesheet" href="/menu-budget.css"></head>'))
print('Four menu budget comparisons derived from published portion totals.')
