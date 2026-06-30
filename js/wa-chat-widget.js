/**
 * Smart WhatsApp Chat Widget - sessionStorage memory (auto-opens once per session)
 */
(function() {
  'use strict';
  var STORAGE_KEY = 'waCardClosed';

  function init() {
    var miniChat = document.getElementById('wa-mini-chat');
    var waBubble = document.getElementById('wa-bubble');
    var waClose = document.getElementById('wa-chat-close');
    var waSendBtn = document.getElementById('wa-send-btn');
    var waChips = document.querySelectorAll('.wa-service-chip');
    var waChatBody = document.querySelector('.wa-chat-body');
    var waStep2Message = document.getElementById('wa-step2-message');
    var waDetailsInput = document.getElementById('wa-details-input');
    var waErrorMsg = document.getElementById('wa-error-msg');
    var waConfirmBtn = document.getElementById('wa-confirm-btn');
    var waBackBtn = document.getElementById('wa-back-btn');
    var selectedService = null;
    var STEP2_MESSAGES = {
      villa: 'Excellent choice! 🏠 Our Villa specialists are ready. Where are you moving from/to?',
      apartment: 'Great! 🏢 Moving apartments in Abu Dhabi? Where should we pick up your items?',
      office: 'Professional Relocation 💼. Please provide your office location or company name.'
    };
    var STEP2_LABEL = { villa: 'Villa', apartment: 'Apartment', office: 'Office' };

    function setClosed() {
      try { sessionStorage.setItem(STORAGE_KEY, 'true'); } catch (e) {}
    }

    function goToStep1() {
      if (waChatBody) waChatBody.classList.remove('wa-step2-active');
      selectedService = null;
      if (waChips) waChips.forEach(function(c) { c.classList.remove('selected'); });
      if (waDetailsInput) { waDetailsInput.value = ''; waDetailsInput.classList.remove('error'); }
      if (waErrorMsg) waErrorMsg.classList.remove('visible');
    }

    function goToStep2(service) {
      if (!waChips) return;
      waChips.forEach(function(c) { c.classList.remove('selected'); });
      var chip = document.querySelector('.wa-service-chip[data-service="' + service + '"]');
      if (chip) chip.classList.add('selected');
      selectedService = service;
      if (waStep2Message) waStep2Message.textContent = STEP2_MESSAGES[service] || 'Where are you moving from/to?';
      if (waDetailsInput) { waDetailsInput.value = ''; waDetailsInput.classList.remove('error'); }
      if (waErrorMsg) waErrorMsg.classList.remove('visible');
      if (waChatBody) waChatBody.classList.add('wa-step2-active');
    }

    function doRedirect() {
      var details = (waDetailsInput && waDetailsInput.value.trim()) || '';
      var serviceType = selectedService ? STEP2_LABEL[selectedService] : 'moving';
      var msg = 'Hi Man With Van! I am interested in a ' + serviceType + ' move. Details: ' + details + '. Please provide a quote.';
      window.open('https://wa.me/971508268481?text=' + encodeURIComponent(msg), '_blank', 'noopener,noreferrer');
      setClosed();
      if (miniChat) miniChat.classList.remove('open');
      goToStep1();
    }

    /* Auto-open once per session if user hasn't closed it */
    if (miniChat) {
      try {
        if (!sessionStorage.getItem(STORAGE_KEY)) {
          setTimeout(function() { miniChat.classList.add('open'); }, 1500);
        }
      } catch (e) {}
    }

    if (waChips && waChips.length) {
      waChips.forEach(function(chip) {
        chip.addEventListener('click', function() {
          var s = chip.getAttribute('data-service');
          if (s) goToStep2(s);
        });
      });
    }

    if (waBackBtn) waBackBtn.addEventListener('click', goToStep1);

    if (waConfirmBtn) {
      waConfirmBtn.addEventListener('click', function() {
        if (waErrorMsg) waErrorMsg.classList.remove('visible');
        if (waDetailsInput) waDetailsInput.classList.remove('error');
        doRedirect();
      });
    }


    if (waClose) waClose.addEventListener('click', function() {
      if (miniChat) miniChat.classList.remove('open');
      setClosed();
      goToStep1();
    });

    if (waBubble && miniChat) {
      waBubble.addEventListener('click', function(e) {
        e.preventDefault();
        miniChat.classList.toggle('open');
        if (miniChat.classList.contains('open')) goToStep1();
      });
    }

    if (waSendBtn) {
      waSendBtn.addEventListener('click', function() {
        window.open('https://wa.me/971508268481?text=' + encodeURIComponent('Hi! I am planning a move and need your help.'), '_blank', 'noopener,noreferrer');
        setClosed();
        if (miniChat) miniChat.classList.remove('open');
      });
    }

    /* Open widget from Get Quote buttons (data-service for preselect) */
    document.addEventListener('click', function(e) {
      var btn = e.target.closest('.js-open-wa');
      if (!btn || !miniChat) return;
      miniChat.classList.add('open');
      var service = (btn.getAttribute('data-service') || '').toLowerCase();
      if (service === 'villa' || service === 'apartment' || service === 'office') {
        goToStep2(service);
      } else {
        goToStep1();
      }
    });
  }

  window.initWaChatWidget = init;
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      if (document.getElementById('wa-mini-chat')) init();
    });
  } else if (document.getElementById('wa-mini-chat')) {
    init();
  }
})();
