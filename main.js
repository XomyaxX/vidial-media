(function () {
  'use strict';

  // Mobile menu
  const navToggle = document.getElementById('navToggle');
  const navLinks = document.getElementById('navLinks');
  if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
      navLinks.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', navLinks.classList.contains('open'));
    });
    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => navLinks.classList.remove('open'));
    });
  }

  // Nav background on scroll
  const nav = document.getElementById('nav');
  function onScroll() {
    if (!nav) return;
    nav.classList.toggle('scrolled', window.scrollY > 40);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Reveal on scroll
  const revealElements = () => {
    const reveals = document.querySelectorAll('.about-box, .service-card, .tech-card, .project-card, .contact-card');
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
    reveals.forEach((el, i) => {
      el.classList.add('reveal');
      el.style.transitionDelay = `${i * 0.06}s`;
      observer.observe(el);
    });
  };
  revealElements();

  // Current year
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // About section video playlist
  const videoSources = [
    'assets/videos/IMG_2090.MOV',
    'assets/videos/IMG_2091.MOV',
    'assets/videos/IMG_2092.MOV',
    'assets/videos/IMG_2093.MOV',
    'assets/videos/IMG_2094.MOV',
    'assets/videos/IMG_2095.MOV',
    'assets/videos/IMG_2096.MOV',
    'assets/videos/IMG_2097.MOV',
    'assets/videos/IMG_2103.MOV',
    'assets/videos/IMG_2104.MOV',
    'assets/videos/IMG_2105.MOV',
  ];
  const aboutVideo = document.getElementById('aboutVideo');
  if (aboutVideo && videoSources.length) {
    let current = 0;
    aboutVideo.src = videoSources[current];
    aboutVideo.addEventListener('ended', function () {
      current = (current + 1) % videoSources.length;
      aboutVideo.src = videoSources[current];
      aboutVideo.play();
    });
  }
})();
