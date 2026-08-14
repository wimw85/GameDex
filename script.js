/*
 * Two effects, both driven by one scroll handler.
 *
 * Parallax reads the scroll position once per frame and writes transforms; the
 * reveal is an IntersectionObserver, so nothing is measured on scroll for it at
 * all. Doing it the other way around is how a marketing page ends up stuttering
 * on the very device it is selling to.
 */

const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* Anything that drifts as you scroll, with how far it drifts per pixel. */
const layers = [...document.querySelectorAll('[data-speed]')].map((el) => ({
  el,
  speed: Number(el.dataset.speed),
  /* Where it sits in the page, so the drift is measured from its own middle
     rather than from the top of the document. */
  base: 0,
}));

const bar = document.querySelector('header.bar');
let ticking = false;

/** Re-measures every layer. Called on load and whenever the page reflows. */
function measure() {
  for (const layer of layers) {
    const box = layer.el.getBoundingClientRect();

    layer.base = box.top + window.scrollY + box.height / 2;
  }
}

/** Writes the frame: one read of scrollY, then transforms only. */
function frame() {
  const y = window.scrollY;
  const middle = y + window.innerHeight / 2;

  for (const layer of layers) {
    const distance = middle - layer.base;

    layer.el.style.transform = `translate3d(0, ${(-distance * layer.speed).toFixed(2)}px, 0)`;
  }

  bar.classList.toggle('stuck', y > 40);
  ticking = false;
}

function onScroll() {
  if (ticking) {
    return;
  }

  ticking = true;
  requestAnimationFrame(frame);
}

if (!reduced) {
  measure();
  frame();
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', () => {
    measure();
    frame();
  });
  // Screenshots change the layout as they load, so the bases move with them.
  window.addEventListener('load', () => {
    measure();
    frame();
  });
} else {
  bar.classList.toggle('stuck', window.scrollY > 40);
  window.addEventListener('scroll', () => bar.classList.toggle('stuck', window.scrollY > 40), {
    passive: true,
  });
}

/* Arrive-on-scroll, once per element. */
const watcher = new IntersectionObserver(
  (entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        entry.target.classList.add('in');
        watcher.unobserve(entry.target);
      }
    }
  },
  { rootMargin: '0px 0px -12% 0px', threshold: 0.08 },
);

for (const el of document.querySelectorAll('.reveal')) {
  watcher.observe(el);
}
