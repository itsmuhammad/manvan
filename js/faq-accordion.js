/**
 * FAQ Accordion - Services page
 * Toggles FAQ answers; only one open at a time (accordion style)
 */
(function() {
  function initFaqAccordion() {
    const questions = document.querySelectorAll('.faq-question, .svc-faq-q');
    questions.forEach(function(btn) {
      btn.addEventListener('click', function() {
        const targetId = this.getAttribute('aria-controls');
        const target = targetId ? document.getElementById(targetId) : null;
        if (!target) return;

        const wasExpanded = this.getAttribute('aria-expanded') === 'true';

        // Close all others
        document.querySelectorAll('.faq-question, .svc-faq-q').forEach(function(q) {
          q.setAttribute('aria-expanded', 'false');
          const id = q.getAttribute('aria-controls');
          if (id) {
            const el = document.getElementById(id);
            if (el) el.setAttribute('hidden', '');
          }
        });

        if (!wasExpanded) {
          this.setAttribute('aria-expanded', 'true');
          target.removeAttribute('hidden');
        }
      });
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initFaqAccordion);
  } else {
    initFaqAccordion();
  }
})();
