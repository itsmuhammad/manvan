/**
 * Modern UI - Page initialization (no Node.js)
 * AOS, marquee, mobile menu
 */

// Initialize Animate on Scroll
if (typeof AOS !== 'undefined') {
  AOS.init({
    duration: 600,
    once: true,
    offset: 80,
  });
}
