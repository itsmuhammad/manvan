// Main JavaScript for common functionality

// Mobile Menu Toggle
function initMobileMenu() {
  const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
  const mobileMenu = document.querySelector('.mobile-menu');
  const mobileMenuClose = document.querySelector('.mobile-menu-close');
  const overlay = document.createElement('div');
  overlay.className = 'mobile-menu-overlay';

  if (mobileMenuBtn && mobileMenu) {
    mobileMenuBtn.addEventListener('click', () => {
      mobileMenu.classList.add('active');
      document.body.appendChild(overlay);
      document.body.style.overflow = 'hidden';
    });

    const closeMobileMenu = () => {
      mobileMenu.classList.remove('active');
      if (overlay.parentNode) {
        document.body.removeChild(overlay);
      }
      document.body.style.overflow = '';
    };

    if (mobileMenuClose) {
      mobileMenuClose.addEventListener('click', closeMobileMenu);
    }

    overlay.addEventListener('click', closeMobileMenu);

    // Close menu on link click
    const mobileLinks = mobileMenu.querySelectorAll('a');
    mobileLinks.forEach(link => {
      link.addEventListener('click', closeMobileMenu);
    });
  }
}

// Scroll to Top Button
function initScrollToTop() {
  const scrollTopBtn = document.querySelector('.scroll-top');

  if (scrollTopBtn) {
    // Show/hide button based on scroll position
    window.addEventListener('scroll', () => {
      if (window.pageYOffset > 300) {
        scrollTopBtn.classList.add('visible');
      } else {
        scrollTopBtn.classList.remove('visible');
      }
    });

    // Scroll to top on click
    scrollTopBtn.addEventListener('click', () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }
}

// Active Navigation Link
function setActiveNavLink() {
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('.nav-links a, .mobile-nav-links a');

  navLinks.forEach(link => {
    const linkPath = new URL(link.href).pathname;
    if (linkPath === currentPath || 
        (currentPath.endsWith('.html') && linkPath.endsWith(currentPath.split('/').pop())) ||
        (currentPath === '/' && linkPath.includes('index.html')) ||
        (currentPath.endsWith('/') && linkPath.includes('index.html'))) {
      link.classList.add('active');
    }
  });
}

// Sticky Header on Scroll
function initStickyHeader() {
  const header = document.querySelector('header');
  if (header) {
    window.addEventListener('scroll', () => {
      if (window.pageYOffset > 20) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    });
  }
}

// Animate on Scroll
function animateOnScroll() {
  const elements = document.querySelectorAll('.fade-in, .scale-in');

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
      }
    });
  }, {
    threshold: 0.1
  });

  elements.forEach(element => {
    element.style.opacity = '0';
    observer.observe(element);
  });
}

// Form Validation
function validateForm(formId) {
  const form = document.getElementById(formId);
  if (!form) return;

  form.addEventListener('submit', (e) => {
    const inputs = form.querySelectorAll('[required]');
    let isValid = true;

    inputs.forEach(input => {
      if (!input.value.trim()) {
        isValid = false;
        input.style.borderColor = 'var(--secondary-red)';
      } else {
        input.style.borderColor = 'var(--gray-300)';
      }
    });

    if (!isValid) {
      e.preventDefault();
      alert('Please fill in all required fields.');
    }
  });
}

// Smooth Scroll for Anchor Links
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const href = this.getAttribute('href');
      if (href !== '#' && href !== '#!') {
        e.preventDefault();
        const target = document.querySelector(href);
        if (target) {
          target.scrollIntoView({
            behavior: 'smooth'
          });
        }
      }
    });
  });
}

// WhatsApp Button
function initWhatsAppButton() {
  const whatsappBtn = document.querySelector('.whatsapp-button');
  if (whatsappBtn) {
    whatsappBtn.addEventListener('click', () => {
      // Track WhatsApp click (add analytics here if neeservice)
    });
  }
}

// WhatsApp Popup - shows on first visit, links to WhatsApp
function initWhatsAppPopup() {
  const popup = document.getElementById('whatsapp-popup');
  const closeBtn = document.getElementById('whatsapp-popup-close');
  const startChatBtn = document.getElementById('whatsapp-start-chat');

  if (!popup) return;

  // Don't show if already closed this session
  if (sessionStorage.getItem('whatsappPopupClosed')) return;

  function closePopup() {
    popup.style.display = 'none';
    sessionStorage.setItem('whatsappPopupClosed', '1');
  }

  // Show popup after 1.5 seconds
  setTimeout(() => {
    popup.style.display = 'block';
  }, 1500);

  if (closeBtn) closeBtn.addEventListener('click', closePopup);

  if (startChatBtn) {
    startChatBtn.addEventListener('click', () => {
      closePopup();
    });
  }

  // Close when clicking outside
  popup.addEventListener('click', (e) => {
    if (e.target === popup) closePopup();
  });
}

// Format Date
function formatDate(dateString) {
  const date = new Date(dateString);
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return date.toLocaleDateString('en-US', options);
}

// Format Date Short
function formatDateShort(dateString) {
  const date = new Date(dateString);
  const options = { year: 'numeric', month: 'short', day: 'numeric' };
  return date.toLocaleDateString('en-US', options);
}

// Get Query Parameter
function getQueryParam(param) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(param);
}

// Called by component-loader.js after all components are loaded (avoids duplicate init)
window.initializePageScripts = function() {
  initMobileMenu();
  initStickyHeader();
  animateOnScroll();
  initScrollToTop();
  setActiveNavLink();
  initSmoothScroll();
  initWhatsAppButton();
  initWhatsAppPopup();
};

// Export functions for use in other scripts
window.AppUtils = {
  formatDate,
  formatDateShort,
  getQueryParam,
  validateForm
};

