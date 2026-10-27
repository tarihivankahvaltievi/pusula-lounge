(() => {
  const form = document.querySelector('#reservation-form');
  form.querySelector('[type=submit]').disabled = false;
  const date = form.elements.date, time = form.elements.time;
  const nowParts = () => { const p = new Intl.DateTimeFormat('en-CA', {timeZone:'Europe/Istanbul', year:'numeric', month:'2-digit', day:'2-digit', hour:'2-digit', minute:'2-digit', hourCycle:'h23'}).formatToParts(new Date()); const v = key => p.find(x => x.type === key).value; return [v('year')+'-'+v('month')+'-'+v('day'), v('hour')+':'+v('minute')]; };
  const refresh = () => { date.min = nowParts()[0]; date.setCustomValidity(''); time.setCustomValidity(''); };
  refresh(); date.addEventListener('focus', refresh); date.addEventListener('input', refresh); time.addEventListener('input', () => time.setCustomValidity(''));
  form.addEventListener('submit', event => {
    event.preventDefault(); refresh(); const [today, currentTime] = nowParts();
    if (date.value < today || (date.value === today && time.value <= currentTime)) { time.setCustomValidity(form.dataset.dateError); time.reportValidity(); return; }
    const d = new FormData(form); const lines = ['Merhaba, Pusula Lounge için rezervasyon talebim var.', '', 'Tarih: '+d.get('date'), 'Saat (İstanbul): '+d.get('time'), 'Kişi sayısı: '+d.get('guests'), 'Ad soyad: '+d.get('name').trim(), 'Telefon: '+d.get('phone').trim()];
    if (d.get('note').trim()) lines.push('Not: '+d.get('note').trim());
    lines.push('', 'Müsaitliği ve rezervasyonumu teyit edebilir misiniz?');
    const url = 'https://wa.me/905078162994?text='+encodeURIComponent(lines.join('\n'));
    const link = document.querySelector('#whatsapp-request'); link.href = url; document.querySelector('#request-summary').hidden = false; document.querySelector('#summary-title').focus();
    window.open(url, '_blank', 'noopener,noreferrer');
  });
})();
