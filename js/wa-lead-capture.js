/**
 * WhatsApp Lead Capture
 * Handles quote/contact forms without backend dependencies.
 */
(function() {
  'use strict';

  var TARGET_FORM_IDS = {
    'qtp-quote-form': true,
    'quick-quote-form': true,
    'quote-form': true,
    'contact-form': true,
    'ctp-contact-form': true
  };
  var WA_URL = 'https://wa.me/971508268481?text=';

  function cleanName(name) {
    return String(name || '')
      .replace(/^_+/, '')
      .replace(/[-_]+/g, ' ')
      .replace(/\s+/g, ' ')
      .trim()
      .replace(/\b\w/g, function(ch) { return ch.toUpperCase(); });
  }

  function cssEscape(value) {
    if (window.CSS && typeof window.CSS.escape === 'function') return window.CSS.escape(value);
    return String(value).replace(/["\\]/g, '\\$&');
  }

  function isLeadForm(form) {
    if (!form || form.hasAttribute('data-skip-wa')) return false;
    return form.hasAttribute('data-wa-lead') || !!TARGET_FORM_IDS[form.id];
  }

  function isVisibleField(field) {
    if (!field || field.disabled) return false;
    if (field.hidden || field.closest('[hidden]')) return false;
    if (field.type) {
      var type = field.type.toLowerCase();
      if (type === 'submit' || type === 'button' || type === 'reset' || type === 'hidden') return false;
    }
    if (field.offsetParent === null && field.getClientRects().length === 0) return false;
    return true;
  }

  function fieldLabel(field) {
    if (field.id) {
      var label = field.ownerDocument.querySelector('label[for="' + cssEscape(field.id) + '"]');
      if (label && label.textContent.trim()) return label.textContent.trim().replace(/\s*\*+\s*$/, '');
    }
    if (field.placeholder && field.placeholder.trim()) return field.placeholder.trim();
    return cleanName(field.name || field.id);
  }

  function fieldValue(field) {
    var tag = field.tagName.toLowerCase();
    var type = (field.type || '').toLowerCase();

    if (type === 'checkbox') return field.checked ? (field.value || 'Yes') : '';
    if (type === 'radio') return field.checked ? field.value : '';
    if (tag === 'select' && field.multiple) {
      return Array.prototype.filter.call(field.options, function(option) {
        return option.selected && option.value;
      }).map(function(option) {
        return option.textContent.trim() || option.value;
      }).join(', ');
    }
    if (tag === 'select') {
      var selected = field.options[field.selectedIndex];
      if (!field.value) return '';
      return selected ? (selected.textContent.trim() || field.value) : field.value;
    }
    return String(field.value || '').trim();
  }

  function collectFields(form) {
    var fields = form.querySelectorAll('input, select, textarea');
    var lines = [];

    Array.prototype.forEach.call(fields, function(field) {
      var name = field.getAttribute('name') || '';
      if (name === '_subject' || name === '_next') return;
      if (!isVisibleField(field)) return;

      var value = fieldValue(field);
      if (!value) return;

      lines.push(fieldLabel(field) + ': ' + value);
    });

    return lines;
  }

  document.addEventListener('submit', function(event) {
    var form = event.target;
    if (!isLeadForm(form)) return;

    event.preventDefault();

    var lines = collectFields(form);
    var message = '*New Lead — manwithvan.ae*';
    if (lines.length) {
      message += '\n\n' + lines.join('\n');
    }

    window.open(WA_URL + encodeURIComponent(message), '_blank', 'noopener,noreferrer');
  }, true);
})();
