(() => {
  const burger = document.getElementById('heroBurger');
  const menu = document.getElementById('heroMobileMenu');
  if (!burger || !menu) return;
  const close = menu.querySelector('.hero-mobile-close');
  const header = menu.querySelector('.hero-mobile-menu-header');
  const switcher = document.querySelector('.bd-language-switcher');
  const switcherParent = switcher?.parentNode;
  const switcherNext = switcher?.nextSibling;
  const desktop = matchMedia('(min-width: 1180px)');
  const german = document.documentElement.lang.startsWith('de');
  let savedScroll = 0;
  let savedBodyStyle = '';
  let inertStates = [];

  // Keep fixed-position UI clear of the hero's animation and stacking context.
  document.body.append(menu);
  burger.setAttribute('aria-controls', menu.id);
  burger.setAttribute('aria-expanded', 'false');
  burger.setAttribute('aria-label', german ? 'Menü öffnen' : 'Menü megnyitása');

  function setOpen(open, restoreFocus = true) {
    if (open === menu.classList.contains('open')) return;
    if (open) {
      savedScroll = window.scrollY;
      savedBodyStyle = document.body.getAttribute('style') || '';
      if (switcher) header.prepend(switcher);
      inertStates = [...document.body.children].filter(e => e !== menu && !['SCRIPT', 'STYLE'].includes(e.tagName)).map(e => [e, e.inert]);
      inertStates.forEach(([e]) => { e.inert = true; });
      Object.assign(document.body.style, {position: 'fixed', top: `-${savedScroll}px`, left: '0', right: '0', width: '100%'});
    }
    menu.inert = !open;
    menu.classList.toggle('open', open);
    menu.setAttribute('aria-hidden', String(!open));
    burger.classList.toggle('open', open);
    burger.setAttribute('aria-expanded', String(open));
    document.body.classList.toggle('hero-menu-open', open);
    if (open) {
      menu.querySelector('.hero-mobile-menu-scroll').scrollTop = 0;
      setTimeout(() => {
        if (menu.classList.contains('open')) close.focus({preventScroll: true});
      }, 0);
    } else {
      inertStates.forEach(([e, inert]) => { e.inert = inert; });
      if (switcher) switcherParent.insertBefore(switcher, switcherNext);
      if (savedBodyStyle) document.body.setAttribute('style', savedBodyStyle);
      else document.body.removeAttribute('style');
      const previousBehavior = document.documentElement.style.scrollBehavior;
      document.documentElement.style.scrollBehavior = 'auto';
      window.scrollTo(0, savedScroll);
      document.documentElement.style.scrollBehavior = previousBehavior;
      if (restoreFocus && !desktop.matches) burger.focus({preventScroll: true});
    }
  }
  burger.addEventListener('click', () => setOpen(!menu.classList.contains('open')));
  close.addEventListener('click', () => setOpen(false));
  menu.addEventListener('click', event => {
    if (event.target.closest('a[href]')) setOpen(false, false);
    else if (event.target === menu || event.target.classList.contains('hero-mobile-menu-scroll') || event.target.classList.contains('hero-mobile-menu-inner')) setOpen(false);
  });
  menu.addEventListener('keydown', event => {
    if (event.key === 'Escape') { event.preventDefault(); setOpen(false); }
    if (event.key !== 'Tab') return;
    const items = [...menu.querySelectorAll('a[href], button')].filter(e => e.getClientRects().length);
    const first = items[0], last = items[items.length - 1];
    if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
    else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
  });
  desktop.addEventListener('change', event => { if (event.matches) setOpen(false, false); });
  window.addEventListener('pagehide', () => setOpen(false, false));
})();
