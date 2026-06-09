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

  // Nav background on scroll + FLIP logo animation
  const nav = document.getElementById('nav');
  const heroLogo = document.querySelector('.hero-logo-icon');
  const navLogo = document.querySelector('.logo-icon-img');
  let flip = null;

  function calcFlip() {
    if (!heroLogo || !navLogo) return;
    const h = heroLogo.getBoundingClientRect();
    const n = navLogo.getBoundingClientRect();
    flip = {
      dx: n.left - h.left + (n.width - h.width) / 2,
      dy: n.top - h.top + (n.height - h.height) / 2,
      scale: n.width / h.width
    };
  }

  function onScroll() {
    if (!nav) return;
    const scrolled = window.scrollY > 40;
    nav.classList.toggle('scrolled', scrolled);

    if (heroLogo && navLogo && flip) {
      const maxScroll = 120;
      const progress = Math.min(Math.max(window.scrollY / maxScroll, 0), 1);
      heroLogo.style.transform = `translate(${flip.dx * progress}px, ${flip.dy * progress}px) scale(${1 - (1 - flip.scale) * progress})`;
      heroLogo.style.opacity = 1 - progress;
      navLogo.style.opacity = progress;
    }
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', calcFlip);
  window.addEventListener('load', calcFlip);
  calcFlip();
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
    'assets/videos/0608.mp4',
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
