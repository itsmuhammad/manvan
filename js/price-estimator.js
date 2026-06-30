/**
 * Price Estimator - Clickable room icons, instant price update
 * Studio: 500 | 1BR: 800 | 2BR: 1,200 | 3BR: 1,800 | 4BR: 2,500 | 5+: Contact
 */
(function() {
  'use strict';
  var PRICES = {
    studio: 500,
    '1br': 800,
    '2br': 1200,
    '3br': 1800,
    '4br': 2500,
    '5br': null  // Contact for Quote
  };

  function init() {
    var output = document.getElementById('price-estimator-output');
    var btns = document.querySelectorAll('.price-room-btn');
    if (!output || !btns.length) return;

    function updatePrice(room) {
      var price = PRICES[room];
      if (price === null) {
        output.textContent = 'Contact for Quote';
      } else {
        output.textContent = price.toLocaleString('en-AE') + ' AED';
      }
    }

    function setActive(room) {
      btns.forEach(function(b) {
        b.classList.toggle('active', b.getAttribute('data-room') === room);
      });
    }

    btns.forEach(function(btn) {
      btn.addEventListener('click', function() {
        var room = btn.getAttribute('data-room');
        setActive(room);
        updatePrice(room);
      });
    });

    var activeBtn = document.querySelector('.price-room-btn.active');
    if (activeBtn) {
      updatePrice(activeBtn.getAttribute('data-room'));
    } else {
      updatePrice('studio');
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
