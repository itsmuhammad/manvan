/**
 * Nav Drawer - Hamburger menu for glass-header (index/services style)
 */
(function() {
  'use strict';
  function init() {
    var hamburgerBtn = document.getElementById('hamburger-btn');
    var drawerOverlay = document.getElementById('drawer-overlay');
    var navDrawer = document.getElementById('nav-drawer');
    var drawerCloseBtn = document.getElementById('drawer-close-btn');
    var servicesTrigger = document.getElementById('drawer-services-trigger');
    var drawerServices = document.getElementById('drawer-services');
    if (!hamburgerBtn || !drawerOverlay || !navDrawer) return;
    if (hamburgerBtn.dataset.drawerReady === 'true') return;
    hamburgerBtn.dataset.drawerReady = 'true';

    function openDrawer() {
      if (hamburgerBtn) hamburgerBtn.classList.add('active');
      if (drawerOverlay) { drawerOverlay.classList.add('active'); drawerOverlay.setAttribute('aria-hidden', 'false'); }
      if (navDrawer) navDrawer.classList.add('active');
      document.body.style.overflow = 'hidden';
    }
    function closeDrawer() {
      if (hamburgerBtn) hamburgerBtn.classList.remove('active');
      if (drawerOverlay) { drawerOverlay.classList.remove('active'); drawerOverlay.setAttribute('aria-hidden', 'true'); }
      if (navDrawer) navDrawer.classList.remove('active');
      document.body.style.overflow = '';
    }

    hamburgerBtn.addEventListener('click', function() {
      if (navDrawer.classList.contains('active')) closeDrawer();
      else openDrawer();
    });
    drawerOverlay.addEventListener('click', closeDrawer);
    if (drawerCloseBtn) drawerCloseBtn.addEventListener('click', closeDrawer);
    navDrawer.querySelectorAll('.drawer-nav a').forEach(function(a) { a.addEventListener('click', closeDrawer); });
    if (drawerServices) {
      drawerServices.querySelectorAll('a').forEach(function(a) { a.addEventListener('click', closeDrawer); });
    }

    if (servicesTrigger && drawerServices) {
      servicesTrigger.addEventListener('click', function() {
        var isOpen = drawerServices.classList.toggle('active');
        servicesTrigger.classList.toggle('active', isOpen);
        servicesTrigger.setAttribute('aria-expanded', isOpen);
      });
    }

    // Mark current page as active in drawer nav
    var page = (window.location.pathname || '').split('/').pop() || 'index.html';
    if (navDrawer) {
      navDrawer.querySelectorAll('.drawer-nav a[href]').forEach(function(link) {
        var href = (link.getAttribute('href') || '').split('?')[0];
        var linkPage = href.split('/').pop() || 'index.html';
        if (linkPage === page) link.classList.add('active');
      });
    }
  }
  window.initNavDrawer = init;
  document.addEventListener('componentsLoaded', init);
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
