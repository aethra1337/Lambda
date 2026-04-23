// ─── CUSTOM CURSOR ───
const cursor = document.createElement('div');
cursor.className = 'cursor';
const ring = document.createElement('div');
ring.className = 'cursor-ring';
document.body.append(cursor, ring);

let mouseX = 0, mouseY = 0, ringX = 0, ringY = 0;

document.addEventListener('mousemove', e => {
  mouseX = e.clientX;
  mouseY = e.clientY;
  cursor.style.left = mouseX + 'px';
  cursor.style.top = mouseY + 'px';
});

(function animRing() {
  ringX += (mouseX - ringX) * 0.12;
  ringY += (mouseY - ringY) * 0.12;
  ring.style.left = ringX + 'px';
  ring.style.top = ringY + 'px';
  requestAnimationFrame(animRing);
})();

document.querySelectorAll('a, button, .gallery-item, .post-card, .filter-btn').forEach(el => {
  el.addEventListener('mouseenter', () => document.body.classList.add('cursor-hover'));
  el.addEventListener('mouseleave', () => document.body.classList.remove('cursor-hover'));
});

// ─── NAV SCROLL ───
const nav = document.getElementById('nav');
if (nav) {
  window.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', window.scrollY > 20);
  }, { passive: true });
}

// ─── MOBILE MENU ───
const burger = document.getElementById('navBurger');
const mobileMenu = document.getElementById('navMobile');
if (burger && mobileMenu) {
  burger.addEventListener('click', () => {
    mobileMenu.classList.toggle('open');
    const spans = burger.querySelectorAll('span');
    if (mobileMenu.classList.contains('open')) {
      spans[0].style.transform = 'rotate(45deg) translate(4px, 4px)';
      spans[1].style.transform = 'rotate(-45deg) translate(4px, -4px)';
    } else {
      spans[0].style.transform = '';
      spans[1].style.transform = '';
    }
  });
}

// ─── SCROLL REVEAL ───
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry, i) => {
    if (entry.isIntersecting) {
      const el = entry.target;
      const delay = el.dataset.delay || (i * 80);
      setTimeout(() => el.classList.add('visible'), parseInt(delay));
      revealObserver.unobserve(el);
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.post-card, .gallery-item').forEach((el, i) => {
  el.dataset.delay = i * 90;
  revealObserver.observe(el);
});

// ─── HERO IMAGE SCALE ───
const heroImg = document.querySelector('.hero-image-wrap');
if (heroImg) {
  setTimeout(() => heroImg.classList.add('loaded'), 100);
}

// ─── FILTER TABS ───
const filterBtns = document.querySelectorAll('.filter-btn');
const postCards = document.querySelectorAll('.post-card');

filterBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    filterBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    const cat = btn.dataset.cat;
    postCards.forEach(card => {
      const cardCat = card.dataset.cat;
      if (cat === 'all' || cardCat === cat) {
        card.style.display = '';
        setTimeout(() => card.classList.add('visible'), 50);
      } else {
        card.classList.remove('visible');
        setTimeout(() => card.style.display = 'none', 400);
      }
    });
  });
});

// ─── LIGHTBOX ───
const lightbox = document.getElementById('lightbox');
if (lightbox) {
  const lbImg = lightbox.querySelector('.lightbox-img');
  const lbCap = lightbox.querySelector('.lightbox-caption');
  const lbClose = lightbox.querySelector('.lightbox-close');
  const lbPrev = lightbox.querySelector('.lightbox-prev');
  const lbNext = lightbox.querySelector('.lightbox-next');

  let items = [];
  let currentIdx = 0;

  document.querySelectorAll('.gallery-item').forEach((item, i) => {
    const src = item.querySelector('img').src;
    const cap = item.querySelector('.gallery-caption')?.textContent || '';
    items.push({ src, cap });

    item.addEventListener('click', () => {
      currentIdx = i;
      openLightbox(i);
    });
  });

  function openLightbox(idx) {
    lbImg.src = items[idx].src;
    lbCap.textContent = items[idx].cap;
    lightbox.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeLightbox() {
    lightbox.classList.remove('open');
    document.body.style.overflow = '';
  }

  lbClose.addEventListener('click', closeLightbox);
  lightbox.addEventListener('click', e => { if (e.target === lightbox) closeLightbox(); });

  lbNext?.addEventListener('click', () => {
    currentIdx = (currentIdx + 1) % items.length;
    openLightbox(currentIdx);
  });
  lbPrev?.addEventListener('click', () => {
    currentIdx = (currentIdx - 1 + items.length) % items.length;
    openLightbox(currentIdx);
  });

  document.addEventListener('keydown', e => {
    if (!lightbox.classList.contains('open')) return;
    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowRight') { currentIdx = (currentIdx + 1) % items.length; openLightbox(currentIdx); }
    if (e.key === 'ArrowLeft') { currentIdx = (currentIdx - 1 + items.length) % items.length; openLightbox(currentIdx); }
  });
}

// ─── PARALLAX ───
const heroSection = document.querySelector('.hero-image-wrap img');
if (heroSection) {
  window.addEventListener('scroll', () => {
    const scrolled = window.scrollY;
    heroSection.style.transform = `scale(1) translateY(${scrolled * 0.15}px)`;
  }, { passive: true });
}
