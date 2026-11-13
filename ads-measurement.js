(() => {
  'use strict';
  const tagId = 'AW-18465361078';
  const conversion = tagId + '/cT-jCN-70rcdELaZ_ORE';
  const preferenceKey = 'pusula-ads-measurement';
  const copy = {
    tr: ['Reklam ölçümü', 'Google Ads, reklamların ardından WhatsApp’ın kaç kez açıldığını ölçebilir.', 'İzin ver', 'Reddet'],
    en: ['Ad measurement', 'Google Ads can measure how often people open WhatsApp after clicking an ad.', 'Allow', 'Decline'],
    ru: ['Измерение рекламы', 'Google Ads может измерять, как часто после клика по рекламе открывают WhatsApp.', 'Разрешить', 'Отклонить'],
    ar: ['قياس الإعلانات', 'يمكن لخدمة إعلانات Google قياس مرات فتح واتساب بعد النقر على الإعلان.', 'سماح', 'رفض'],
  };
  const [label, description, allow, decline] = copy[document.documentElement.lang] || copy.en;
  let choice;
  let tagStarted = false;

  try {
    choice = localStorage.getItem(preferenceKey);
  } catch {
    // Visitors can still choose for the current page if storage is unavailable.
  }

  function gtag() {
    window.dataLayer.push(arguments);
  }

  function startTag() {
    if (tagStarted) return;
    tagStarted = true;
    window.dataLayer = window.dataLayer || [];
    gtag('consent', 'default', {
      ad_storage: 'granted',
      ad_user_data: 'granted',
      ad_personalization: 'denied',
      analytics_storage: 'denied',
    });
    gtag('js', new Date());
    gtag('config', tagId, { allow_ad_personalization_signals: false });
    const script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + tagId;
    document.head.append(script);
  }

  const controls = document.createElement('details');
  const summary = document.createElement('summary');
  summary.textContent = label;
  const explanation = document.createElement('p');
  explanation.textContent = description;
  const accept = document.createElement('button');
  const reject = document.createElement('button');
  accept.type = reject.type = 'button';
  accept.textContent = allow;
  reject.textContent = decline;
  controls.append(summary, explanation, accept, ' ', reject);
  controls.open = choice !== 'allow' && choice !== 'decline';
  (document.querySelector('footer') || document.body).append(controls);

  function choose(value) {
    choice = value;
    try {
      localStorage.setItem(preferenceKey, value);
    } catch {
      // The current page still respects the choice.
    }
    if (value === 'allow') {
      if (tagStarted) gtag('consent', 'update', { ad_storage: 'granted', ad_user_data: 'granted' });
      else startTag();
    } else if (tagStarted) {
      gtag('consent', 'update', { ad_storage: 'denied', ad_user_data: 'denied' });
    }
    controls.open = false;
    summary.focus();
  }

  accept.addEventListener('click', () => choose('allow'));
  reject.addEventListener('click', () => choose('decline'));
  if (choice === 'allow') startTag();

  window.addEventListener('pusula:interaction', event => {
    if (choice === 'allow' && event.detail?.name === 'reservation_whatsapp_open') {
      gtag('event', 'conversion', { send_to: conversion });
    }
  });
})();
