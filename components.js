/* ===== ENTERTAINMENT PROS — GLOBAL COMPONENTS ===== */
/* Sticky header, UNIVERSAL mobile nav (single source of truth), accordions, scroll animations */

/* ===================================================================
   CANONICAL NAVIGATION — edit here ONCE to update the mobile menu on
   every page. Mirrors the desktop mega-menu so nothing can go missing.
   =================================================================== */
const EP_NAV = [
  { label: 'Home', href: '/' },
  {
    label: 'Services', href: '/services-audio-visual-planning-and-installation',
    groups: [
      { heading: 'Audio & Sound', links: [
        ['Audio-Video Planning', '/audio-video-planning-and-installation'],
        ['Home Theater Design', '/home-theater-design-and-installation'],
        ['Surround Sound Systems', '/living-room-surround-sound'],
        ['Condo TV & Sound', '/condo-tv-and-sound-solutions'],
      ]},
      { heading: 'TV & Installations', links: [
        ['TV Hanging & Mounting', '/hanging-tvs-mounting-services'],
        ['Residential Installations', '/installations-residential'],
        ['Light Commercial AV', '/commercial-audio-video'],
        ['Equipment Sales', '/sales'],
      ]},
      { heading: 'Lighting', links: [
        ['Lighting Control', '/lighting-control'],
        ['LED Accent Lighting', '/led-accent-lighting'],
        ['Exterior Illumination', '/exterior-illumination'],
        ['Landscape Lighting', '/exterior-lighting'],
      ]},
      { heading: 'Smart Home', links: [
        ['Home Automation', '/home-automation'],
        ['Automated Shades', '/automated-shades'],
      ]},
    ],
  },
  {
    label: 'Portfolio', href: '/portfolio',
    links: [
      ['Gallery', '/portfolio'],
      ['Brands We Carry', '/brands'],
    ],
  },
  { label: 'About', href: '/about-us' },
  {
    label: 'Resources', href: '/blog',
    links: [
      ['Blog', '/blog'],
      ['Tell Us About Your Project', '/your-project'],
      ['TV Size Calculator', '/tv-size'],
      ['Surround Sound Calculator', '/surround-sound-and-setup'],
      ['AV Budget Calculator', '/av-budget-calculator'],
    ],
  },
  { label: 'Contact', href: '/contact' },
];

const CHEVRON = '<svg class="mnav-chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>';

function buildMobileNav() {
  const mn = document.getElementById('mobileNav');
  if (!mn) return;

  const linkRow = ([label, href]) => `<a href="${href}">${label}</a>`;
  let body = '';

  EP_NAV.forEach(item => {
    const hasChildren = item.groups || item.links;
    if (!hasChildren) {
      body += `<a class="mnav-link" href="${item.href}">${item.label}</a>`;
      return;
    }
    let panel = '';
    if (item.href) panel += `<a class="mnav-all" href="${item.href}">All ${item.label}</a>`;
    if (item.groups) {
      item.groups.forEach(g => {
        panel += `<div class="mnav-group"><span class="mnav-group-title">${g.heading}</span>${g.links.map(linkRow).join('')}</div>`;
      });
    }
    if (item.links) panel += item.links.map(linkRow).join('');
    body += `<div class="mnav-section">` +
      `<button class="mnav-acc" aria-expanded="false"><span>${item.label}</span>${CHEVRON}</button>` +
      `<div class="mnav-panel">${panel}</div></div>`;
  });

  mn.innerHTML =
    `<div class="mnav-head">` +
      `<a href="/" class="mnav-brand">Entertainment&nbsp;<b>Pros</b></a>` +
      `<button class="mobile-nav-close" id="mobileNavClose" aria-label="Close menu">` +
        `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>` +
      `</button>` +
    `</div>` +
    `<div class="mnav-body" role="navigation" aria-label="Site menu">${body}</div>` +
    `<div class="mnav-foot">` +
      `<a href="/your-project" class="btn btn-primary mnav-cta">Tell Us About Your Project</a>` +
      `<a href="tel:727-804-2277" class="mnav-phone"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>727-804-2277</a>` +
      `<p class="mnav-meta">Lic. ES12001376 &middot; Serving Pinellas since 2006</p>` +
    `</div>`;
}

document.addEventListener('DOMContentLoaded', () => {
  // ===== STICKY HEADER =====
  const header = document.getElementById('header');
  if (header) {
    const updateHeader = () => header.classList.toggle('scrolled', window.scrollY > 60);
    window.addEventListener('scroll', updateHeader, { passive: true });
    updateHeader();
  }

  // ===== UNIVERSAL MOBILE NAV =====
  buildMobileNav();
  const toggle = document.getElementById('mobileToggle');
  const mobileNav = document.getElementById('mobileNav');

  if (toggle && mobileNav) {
    const openNav = () => {
      mobileNav.classList.add('open');
      document.body.style.overflow = 'hidden';
      toggle.setAttribute('aria-expanded', 'true');
    };
    const closeNav = () => {
      mobileNav.classList.remove('open');
      document.body.style.overflow = '';
      toggle.setAttribute('aria-expanded', 'false');
    };

    toggle.addEventListener('click', openNav);
    const closeBtn = mobileNav.querySelector('#mobileNavClose');
    if (closeBtn) closeBtn.addEventListener('click', closeNav);
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && mobileNav.classList.contains('open')) closeNav(); });

    // Collapsible sections
    mobileNav.querySelectorAll('.mnav-acc').forEach(btn => {
      btn.addEventListener('click', () => {
        const section = btn.parentElement;
        const panel = section.querySelector('.mnav-panel');
        const willOpen = !section.classList.contains('open');
        section.classList.toggle('open', willOpen);
        btn.setAttribute('aria-expanded', willOpen ? 'true' : 'false');
        panel.style.maxHeight = willOpen ? panel.scrollHeight + 'px' : null;
      });
    });

    // Tapping any real link closes the drawer
    mobileNav.querySelectorAll('a[href]').forEach(a => a.addEventListener('click', closeNav));
  }

  // ===== ACTIVE NAV LINK (desktop + mobile) + auto-expand active section =====
  const currentPath = window.location.pathname.replace(/\/$/, '') || '/';
  document.querySelectorAll('nav a, .mobile-nav a').forEach(link => {
    const href = link.getAttribute('href');
    if (!href || href.startsWith('tel:') || href.startsWith('#')) return;
    const linkPath = new URL(href, window.location.origin).pathname.replace(/\/$/, '') || '/';
    if (linkPath === currentPath) {
      link.classList.add('active');
      const section = link.closest('.mnav-section');
      if (section) {
        section.classList.add('open');
        const acc = section.querySelector('.mnav-acc');
        const panel = section.querySelector('.mnav-panel');
        if (acc) acc.setAttribute('aria-expanded', 'true');
        if (panel) panel.style.maxHeight = panel.scrollHeight + 'px';
      }
    }
  });

  // ===== FAQ ACCORDION =====
  document.querySelectorAll('.faq-question').forEach(btn => {
    btn.addEventListener('click', () => {
      const item = btn.parentElement;
      const answer = item.querySelector('.faq-answer');
      const isOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item.open').forEach(openItem => {
        openItem.classList.remove('open');
        openItem.querySelector('.faq-answer').style.maxHeight = null;
      });
      if (!isOpen) {
        item.classList.add('open');
        answer.style.maxHeight = answer.scrollHeight + 'px';
      }
    });
  });

  // ===== SCROLL ANIMATIONS =====
  const animateEls = document.querySelectorAll(
    '.service-card, .review-card, .blog-card, .gallery-item, .about-feature, .faq-item, [data-animate]'
  );
  if (animateEls.length > 0) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
    );
    animateEls.forEach(el => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(24px)';
      el.style.transition = 'opacity .6s ease, transform .6s ease';
      observer.observe(el);
    });
  }
});
