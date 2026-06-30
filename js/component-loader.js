/**
 * Component Loader
 * Dynamically loads reusable HTML components into pages
 * Edit components in components/ folder - changes apply across all pages
 */

// Component configuration
const components = {
  // Global components
  'topbar': 'components/topbar/topbar.html',
  'header': 'components/header/header.html',
  'features-section': 'components/features-section/features-section.html',
  'footer': 'components/footer/footer.html',
  'whatsapp-button': 'components/whatsapp-button/whatsapp-button.html',
  'wa-chat-widget': 'components/wa-chat-widget/wa-chat-widget.html',
  'scroll-to-top': 'components/scroll-to-top/scroll-to-top.html',
  
  // Index page components
  'index-hero': 'components/index/hero-section.html',
  'index-services-preview': 'components/index/services-preview.html',
  'index-testimonials': 'components/index/testimonials.html',
  
  // Services page components
  'services-hero': 'components/services/hero-section.html',
  'services-container': 'components/services/services-static.html',
  'services-process': 'components/services/process-section.html',
  
  // Blog page components
  'blog-hero': 'components/blog/hero-section.html',
  'blog-filters': 'components/blog/filters-section.html',
  'blog-grid': 'components/blog/grid-static.html',
  'blog-post-hero': 'components/blog/post-hero.html',
  'blog-post-content': 'components/blog/post-content.html',
  'blog-post-cta': 'components/blog/post-cta.html',
  
  // Blog-specific header and footer (for blog posts in blogs/ directory)
  'blog-header': 'components/blog/blog-header.html',
  'blog-footer': 'components/blog/blog-footer.html',
  
  // About page components
  'about-hero': 'components/about/hero-section.html',
  'about-stats': 'components/about/stats-section.html',
  'about-story': 'components/about/story-section.html',
  'about-values': 'components/about/values-section.html',
  'about-team': 'components/about/team-section.html',
  
  // Contact page components
  'contact-hero': 'components/contact/hero-section.html',
  'contact-form': 'components/contact/form-section-static.html',
  'contact-map': 'components/contact/map-section.html',
  
  // Quote page components
  'quote-hero': 'components/quote/hero-section.html',
  'quote-form': 'components/quote/quote-form-professional.html'
};

/**
 * Get base path for subdirectory deployment (e.g. localhost/manwithvan.ae/)
 * Returns project root so components load correctly from locations/, blog/, etc.
 */
function getBasePath() {
  try {
    const scripts = document.getElementsByTagName('script');
    for (let i = scripts.length - 1; i >= 0; i--) {
      const src = scripts[i].src;
      if (src && src.indexOf('component-loader') !== -1) {
        const base = src.replace(/\/js\/[^/]*$/, '/');
        const path = new URL(base).pathname;
        return path.endsWith('/') ? path : path + '/';
      }
    }
  } catch (e) {}
  const pathname = window.location.pathname;
  const subfolders = ['/locations/', '/blog/', '/services', '/about', '/contact', '/quote', '/get-free-quote'];
  for (const sub of subfolders) {
    const idx = pathname.indexOf(sub);
    if (idx > 0) return pathname.substring(0, idx) + '/';
    if (idx === 0) return '/';
  }
  if (pathname === '/' || pathname === '') return '/';
  const match = pathname.match(/^(\/[^/]+\/)/);
  return match ? match[1] : '/';
}

/**
 * Load a single component
 * @param {string} componentId - The ID of the element to load component into
 * @param {string} componentPath - Path to the component HTML file
 */
async function loadComponent(componentId, componentPath) {
  const element = document.getElementById(componentId);
  
  if (!element) return;

  // Topbar removed - hide placeholder and skip loading
  if (componentId === 'topbar') {
    element.style.display = 'none';
    element.innerHTML = '';
    return;
  }

  const basePath = getBasePath();
  const fullPath = basePath + componentPath.replace(/^\//, '');
  const componentUrl = fullPath + (fullPath.indexOf('?') === -1 ? '?v=20260627-components1' : '&v=20260627-components1');

  try {
    const response = await fetch(componentUrl);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const html = await response.text();
    element.outerHTML = html;
    
  } catch (error) {
    element.innerHTML = `<!-- Component ${componentId} failed to load -->`;
  }
}

/**
 * Load all components on the page
 */
async function loadAllComponents() {
  const promises = [];
  
  // Find all component placeholders and load them
  for (const [componentId, componentPath] of Object.entries(components)) {
    if (document.getElementById(componentId)) {
      promises.push(loadComponent(componentId, componentPath));
    }
  }
  
  // Wait for all components to load
  await Promise.all(promises);
  
  // Fix paths for subdirectory deployment (e.g. localhost/manwithvan.ae/)
  fixLogoPaths();
  fixBasePathLinks();
  initLanguageNavigation();
  
  // After components are loaded, initialize any page-specific scripts
  if (typeof initializePageScripts === 'function') {
    initializePageScripts();
  }
  // WA chat widget: init after load (elements may not exist until components load)
  if (document.getElementById('wa-mini-chat') && typeof window.initWaChatWidget === 'function') {
    window.initWaChatWidget();
  }
  if (typeof window.initNavDrawer === 'function') {
    window.initNavDrawer();
  }
  document.dispatchEvent(new CustomEvent('componentsLoaded'));
}

/**
 * Fix logo image paths to work in subdirectory (localhost/project/) and at domain root
 */
function fixLogoPaths() {
  const basePath = getBasePath();
  const logoPath = basePath.replace(/\/?$/, '/') + 'images/logo/logo.png';
  document.querySelectorAll('.logo-image, .footer-logo, .drawer-logo').forEach(img => {
    img.src = logoPath;
  });
}

/**
 * Fix root-relative links (href="/...") and relative links in nav/footer
 * so they work in subdirectory (e.g. localhost/manwithvan.ae/)
 */
function fixBasePathLinks() {
  const basePath = getBasePath();
  const isSubdir = basePath && basePath !== '/';
  const basePrefix = isSubdir ? basePath.replace(/\/$/, '') : '';

  // Fix root-absolute links (href="/...")
  if (isSubdir) {
    document.querySelectorAll('a[href^="/"]').forEach(link => {
      const href = link.getAttribute('href');
      if (href && !href.startsWith('//') && !href.startsWith('/#')) {
        link.setAttribute('href', basePrefix + href);
      }
    });
  }

  // Fix relative links in header/footer when in subfolder
  // so "blog.html" resolves to site root (e.g. /manwithvan.ae/blog.html)
  if (isSubdir) {
    document.querySelectorAll('header a[href], footer a[href], .nav-drawer a[href], .mobile-menu a[href]').forEach(link => {
      const href = link.getAttribute('href');
      if (!href || /^(https?:|\/\/|#|tel:|mailto:|javascript:)/.test(href)) return;
      if (href.startsWith('/')) return;
      link.setAttribute('href', basePrefix + '/' + href.replace(/^\.\//, ''));
    });
  }
}

/**
 * Wire EN/AR language switcher and Arabic header links after component injection.
 */
function initLanguageNavigation() {
  const arTwins = new Set([
    '/1-bhk-movers-abu-dhabi.html',
    '/2-bhk-movers-abu-dhabi.html',
    '/3-bhk-movers-abu-dhabi.html',
    '/about.html',
    '/apartment-movers-abu-dhabi.html',
    '/blog/5-essential-tips-stress-free-house-move-uae.html',
    '/blog/cost-of-moving-abu-dhabi.html',
    '/blog/how-to-choose-movers-abu-dhabi.html',
    '/blog/ultimate-moving-checklist-8-weeks-stress-free.html',
    '/blog/villa-moving-checklist-abu-dhabi.html',
    '/blog/office-relocation-abu-dhabi-complete-guide.html',
    '/blog/moving-to-al-reem-island.html',
    '/blog/best-months-to-move-uae.html',
    '/blog/how-to-pack-fragile-items.html',
    '/blog/full-service-movers-vs-diy-moving-uae.html',
    '/appliances-movers-abu-dhabi.html',
    '/cheap-movers-abu-dhabi.html',
    '/contact.html',
    '/furniture-movers-abu-dhabi.html',
    '/get-free-quote.html',
    '/house-shifting-abu-dhabi.html',
    '/index.html',
    '/locations/movers-al-ain.html',
    '/locations/movers-al-bateen-abu-dhabi.html',
    '/locations/movers-al-falah-abu-dhabi.html',
    '/locations/movers-al-karamah-abu-dhabi.html',
    '/locations/movers-al-khalidiyah-abu-dhabi.html',
    '/locations/movers-al-maryah-island-abu-dhabi.html',
    '/locations/movers-al-mushrif-abu-dhabi.html',
    '/locations/movers-al-raha-beach-abu-dhabi.html',
    '/locations/movers-al-rahba-abu-dhabi.html',
    '/locations/movers-al-reef-abu-dhabi.html',
    '/locations/movers-al-reem-island-abu-dhabi.html',
    '/locations/movers-al-ruwais-abu-dhabi.html',
    '/locations/movers-al-shahama-abu-dhabi.html',
    '/locations/movers-al-shamkha-abu-dhabi.html',
    '/locations/movers-al-zahiyah-abu-dhabi.html',
    '/locations/movers-baniyas-abu-dhabi.html',
    '/locations/movers-corniche-abu-dhabi.html',
    '/locations/movers-khalifa-city-abu-dhabi.html',
    '/locations/movers-madinat-zayed-abu-dhabi.html',
    '/locations/movers-masdar-city-abu-dhabi.html',
    '/locations/movers-mohammed-bin-zayed-city.html',
    '/locations/movers-mohammed-bin-zayed-city-abu-dhabi.html',
    '/locations/movers-mussafah-abu-dhabi.html',
    '/locations/movers-saadiyat-island-abu-dhabi.html',
    '/locations/movers-shakhbout-city-abu-dhabi.html',
    '/locations/movers-tourist-club-area-abu-dhabi.html',
    '/locations/movers-yas-island-abu-dhabi.html',
    '/man-with-van-abu-dhabi.html',
    '/movers-abu-dhabi-to-dubai.html',
    '/movers-near-me-abu-dhabi.html',
    '/office-movers-abu-dhabi.html',
    '/packing-services-abu-dhabi.html',
    '/piano-movers-abu-dhabi.html',
    '/same-day-movers-abu-dhabi.html',
    '/services.html',
    '/single-furniture-movers-abu-dhabi.html',
    '/storage-abu-dhabi.html',
    '/studio-movers-abu-dhabi.html',
    '/villa-movers-abu-dhabi.html'
  ]);

  const basePath = getBasePath();
  const isSubdir = basePath && basePath !== '/';
  const basePrefix = isSubdir ? basePath.replace(/\/$/, '') : '';

  function stripBase(path) {
    if (isSubdir && path.indexOf(basePrefix + '/') === 0) {
      return path.substring(basePrefix.length) || '/';
    }
    return path || '/';
  }

  function siteHref(path) {
    return (isSubdir ? basePrefix : '') + path;
  }

  function normalizePath(path) {
    let clean = stripBase(path).replace(/\/+$/, '');
    if (clean === '' || clean === '/') clean = '/index.html';
    if (clean === '/ar') clean = '/ar/index.html';
    if (clean === '/ar/') clean = '/ar/index.html';
    return clean;
  }

  const currentPath = normalizePath(window.location.pathname);
  const isArabicPage = currentPath === '/ar/index.html' || currentPath.indexOf('/ar/') === 0;
  const englishPath = isArabicPage ? normalizePath(currentPath.replace(/^\/ar/, '')) : currentPath;
  const hasTwin = arTwins.has(englishPath);
  const enHref = hasTwin ? (englishPath === '/index.html' ? '/' : englishPath) : '/';
  const arHref = hasTwin ? (englishPath === '/index.html' ? '/ar/' : '/ar' + englishPath) : '/ar/';

  document.querySelectorAll('[data-lang-switch="en"]').forEach(link => {
    link.setAttribute('href', siteHref(enHref));
  });
  document.querySelectorAll('[data-lang-switch="ar"]').forEach(link => {
    link.setAttribute('href', siteHref(arHref));
  });

  if (!isArabicPage) return;

  document.querySelectorAll('[data-ar-label]').forEach(el => {
    el.textContent = el.getAttribute('data-ar-label');
  });
  document.querySelectorAll('header a[href], .nav-drawer a[href]').forEach(link => {
    const href = link.getAttribute('href');
    if (!href || /^(https?:|\/\/|#|tel:|mailto:|javascript:)/.test(href)) return;
    const urlPath = normalizePath(href);
    const enLinkPath = urlPath.indexOf('/ar/') === 0 ? normalizePath(urlPath.replace(/^\/ar/, '')) : urlPath;
    if (arTwins.has(enLinkPath)) {
      link.setAttribute('href', siteHref(enLinkPath === '/index.html' ? '/ar/' : '/ar' + enLinkPath));
    } else if (enLinkPath.indexOf('/blog/') === 0 || enLinkPath === '/blog.html') {
      link.setAttribute('href', siteHref('/ar/'));
    }
  });
}

// Load components when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', loadAllComponents);
} else {
  loadAllComponents();
}

