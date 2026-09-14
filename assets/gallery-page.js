(() => {
  const photoCatalog = [
    [1620,1080,'Feine Charakterisierung einer Frontzahnrestauration','Frontfog-restauráció finom karakterizálása'],
    [1080,1620,'Detailarbeit an einer mehrgliedrigen Keramikrestauration','Többtagú kerámiarestauráció részletgazdag kidolgozása'],
    [1620,1080,'Manuelle Oberflächenbearbeitung einer Zahnrestauration','Fogtechnikai restauráció kézi felszínkidolgozása'],
    [1620,1080,'Zahntechniker bei der Präzisionsarbeit am Mikroskop','Fogtechnikus precíziós munka közben, mikroszkópnál'],
    [1620,1080,'Funktionskontrolle einer Restauration im Artikulator','Restauráció funkcionális ellenőrzése artikulátorban'],
    [1920,1080,'Sorgfältige Ausarbeitung eines keramischen Zahnersatzes','Kerámia fogpótlás gondos kézi kidolgozása'],
    [1620,1080,'Individuelle Farbabstimmung mit dentalen Farbmustern','Egyedi fogszín-meghatározás fogszínkulccsal'],
    [1920,1080,'Teamarbeit an den zahntechnischen Arbeitsplätzen','Csapatmunka a fogtechnikai munkaállomásoknál'],
    [1620,1080,'Konzentrierte Handarbeit im offenen Bridge Dental Labor','Koncentrált kézi munka a Bridge Dental nyitott laborában'],
    [1080,1620,'Feine Werkzeuge für die manuelle Finalisierung','Finom kéziszerszámok a restaurációk készreviteléhez'],
    [1080,1620,'Detailarbeit an einer Restauration unter der Arbeitsplatzleuchte','Restauráció részletmunkája a munkaasztali világításnál'],
    [1620,1080,'Zahntechnische Ausarbeitung am Mikroskop-Arbeitsplatz','Fogtechnikai kidolgozás mikroszkópos munkaállomáson'],
    [1080,1620,'Hédi Császárné Demeter, Office Managerin bei Bridge Dental','Hédi Császárné Demeter, a Bridge Dental irodavezetője'],
    [1080,1620,'Attila Kínál, Ansprechpartner für die fachliche Kommunikation','Attila Kínál, a szakmai kommunikáció kapcsolattartója'],
    [1080,1620,'Porträt eines Mitarbeiters von Bridge Dental','A Bridge Dental egyik munkatársának portréja'],
    [1920,1080,'Digitale Planung im Team an mehreren CAD-Arbeitsplätzen','Közös digitális tervezés több CAD munkaállomáson'],
    [1620,1080,'Kolleginnen bei der Abstimmung digitaler Restaurationspläne','Kollégák digitális restaurációs tervek egyeztetése közben'],
    [1620,1080,'Virtuelle Konstruktion einer vollständigen Zahnrestauration','Teljes fogtechnikai restauráció virtuális tervezése'],
    [1620,1080,'Digitaler Gesichtsscan für die patientenbezogene Planung','Digitális arcszkennelés a páciensre szabott tervezéshez'],
    [1620,1080,'Manuelle Finalisierung an einem ergonomischen Laborarbeitsplatz','Kézi készrevitel ergonomikus laboratóriumi munkaállomáson'],
    [1620,1080,'Innenraum einer CAD/CAM-Fräsmaschine','CAD/CAM marógép megmunkálóterének belseje'],
    [1620,1080,'Zirkonoxidbearbeitung während des Fräsvorgangs','Cirkónium megmunkálása marási folyamat közben'],
    [1620,1080,'Bedienung der Fräsmaschinen im digitalen Fertigungszentrum','Marógépek kezelése a digitális gyártóközpontban'],
    [1350,1080,'Maschinenpark für die präzise CAD/CAM-Fertigung','Precíz CAD/CAM gyártást szolgáló géppark'],
    [1620,1080,'Große CORiTEC-Fräsanlage im Bridge Dental Labor','Nagy CORiTEC maróberendezés a Bridge Dental laborjában'],
    [1620,1080,'Präzisionsfräsen einer dentalen Restauration','Fogtechnikai restauráció precíziós marása'],
    [1080,1620,'Additive Fertigung dentaler Bauteile im 3D-Drucker','Fogtechnikai elemek additív gyártása 3D nyomtatóban'],
    [1080,1620,'PolyJet-Druckprozess für monolithische Dentalarbeiten','PolyJet nyomtatási folyamat monolitikus fogpótlásokhoz'],
    [1620,1080,'Druckplattform während der additiven Fertigung','Nyomtatótálca az additív gyártási folyamat közben'],
    [1620,1080,'Bearbeitung einer Zirkonoxid-Ronde in der Fräsmaschine','Cirkóniumkorong megmunkálása marógépben'],
    [1620,1080,'Gedruckter Zahnbogen im blauen Licht des Fertigungssystems','Nyomtatott fogív a gyártórendszer kék fényében'],
    [1620,1080,'Geöffneter 3D-Drucker mit einer dentalen Arbeit','Nyitott 3D nyomtató elkészült fogtechnikai munkával'],
    [1620,1080,'Mehrere additiv gefertigte Dentalmodelle','Több, additív technológiával készült fogtechnikai modell'],
    [1620,1080,'Individuelle Modellation einer Zahnrestauration von Hand','Fogtechnikai restauráció egyedi kézi kialakítása'],
    [1620,1080,'Abgleich einer Restauration mit der digitalen Vorlage','Restauráció összevetése a digitális referenciával'],
    [1620,1080,'Keramische Charakterisierung mit feinem Pinsel','Kerámiarestauráció karakterizálása finom ecsettel'],
    [1620,1080,'Farbabstimmung während der manuellen Finalisierung','Színegyeztetés a restauráció kézi készrevitele során'],
    [1620,1080,'Kontrolle eines Zahnbogens anhand der Farbskala','Fogív ellenőrzése fogszínkulcs segítségével'],
    [1080,1620,'Zahntechnikerin bei der präzisen Handarbeit','Fogtechnikus precíz kézi munka közben'],
    [1080,1620,'Porträt einer Mitarbeiterin von Bridge Dental','A Bridge Dental egyik munkatársának portréja'],
    [1080,1620,'Porträt einer Zahntechnikerin aus dem Bridge Dental Team','A Bridge Dental egyik fogtechnikusának portréja'],
    [1620,1080,'Gemeinsame Kontrolle eines digitalen Zahnbogens am Monitor','Digitális fogív közös ellenőrzése a monitoron'],
    [1620,1080,'Digitale Smile-Design-Planung am CAD-Arbeitsplatz','Digitális mosolytervezés CAD munkaállomáson'],
    [1620,1080,'Patientenbezogene Gestaltung einer Frontzahnrestauration','Frontfog-restauráció páciensre szabott digitális kialakítása'],
    [1620,1080,'Keramikofen im digitalen Laborprozess','Kerámiaégető kemence a digitális laborfolyamatban'],
    [1620,1080,'Zahntechniker bei der Arbeit unter dem Mikroskop','Fogtechnikus munka közben, mikroszkóp alatt'],
    [1620,1080,'Präzisionskontrolle einer Restauration mit Lupenbrille','Restauráció precíziós ellenőrzése nagyítószemüveggel'],
    [1620,1080,'Qualitätsprüfung eines Zahnbogens mit optischer Vergrößerung','Fogív minőségellenőrzése optikai nagyítás mellett'],
    [1620,1080,'Mikroskopische Kontrolle feiner Restaurationsdetails','Restauráció finom részleteinek mikroszkópos ellenőrzése'],
    [1620,1080,'Manuelle Bearbeitung am Mikroskop-Arbeitsplatz','Kézi kidolgozás mikroszkópos munkaállomáson'],
    [1080,1620,'Mikroskop und Arbeitslicht bei der Qualitätskontrolle','Mikroszkóp és munkafény a minőségellenőrzés során'],
    [1620,1080,'Zahntechnikerin mit Lupenbrille bei der Finalisierung','Fogtechnikus nagyítószemüvegben, készrevitel közben'],
    [1920,1080,'Blick in das moderne Bridge Dental Labor','A modern Bridge Dental labor belső tere'],
    [1620,1080,'Digitale Konstruktion am Exocad-Arbeitsplatz','Digitális tervezés Exocad munkaállomáson'],
    [1620,1080,'Zwei Zahntechniker bei der gemeinsamen Fallplanung','Két fogtechnikus közös esettervezés közben'],
    [1350,1080,'Fachliche Abstimmung eines digitalen Restaurationsplans','Digitális restaurációs terv szakmai egyeztetése'],
    [1620,1080,'Gemeinsame Kontrolle der CAD-Konstruktion am Bildschirm','CAD terv közös ellenőrzése a képernyőn'],
    [1620,1080,'Implantatgetragene Konstruktion in der CAD-Software','Implantátumokra épülő restauráció tervezése CAD szoftverben'],
    [1620,1080,'Virtuelles Wax-up am digitalen Arbeitsplatz','Virtuális wax-up készítése digitális munkaállomáson'],
    [1620,1080,'Vorbereitung eines Bauteils für die additive Fertigung','Fogtechnikai elem előkészítése additív gyártáshoz'],
    [1620,1080,'Detailansicht einer digital geplanten Restauration','Digitálisan tervezett restauráció részletnézete'],
    [1620,1080,'Teamgespräch zur digitalen Konstruktion eines Zahnbogens','Szakmai egyeztetés egy fogív digitális tervezéséről'],
    [1620,1080,'Gemeinsame manuelle Kontrolle einer zahntechnischen Arbeit','Fogtechnikai munka közös kézi ellenőrzése'],
    [1292,1080,'Die beiden Zahntechnikermeister hinter Bridge Dental','A Bridge Dental mögött álló két fogtechnikus mester'],
    [1080,1080,'Porträt der Gründer von Bridge Dental','A Bridge Dental alapítóinak portréja'],
    [1620,1080,'Kolleginnen bei der gemeinsamen Arbeit im Labor','Kollégák közös munka közben a laborban'],
    [1620,1080,'Voll bestückte Druckplattform mit Dentalmodellen','Fogtechnikai modellekkel megtöltött nyomtatótálca']
  ];

  // Egyetlen kép marad minden hasonló sorozatból; a portrék nem kerülnek a galériába.
  const visiblePhotoIds = [
    1, 3, 4, 5, 6, 7, 8, 10, 11, 16, 18, 19, 20, 21, 22, 23, 24,
    27, 28, 29, 33, 34, 35, 36, 38, 42, 43, 45, 47, 53, 54, 55, 56,
    58, 59, 60, 61, 62, 63, 66, 67
  ];
  const photos = visiblePhotoIds.map((id) => [id, ...photoCatalog[id - 1]]);

  const body = document.body;
  const lang = body.dataset.lang === 'hu' ? 'hu' : 'de';
  const assetRoot = body.dataset.galleryRoot || 'assets/gallery';
  const grid = document.getElementById('galleryGrid');
  const galleryCount = document.querySelector('.gallery-count');
  const lightbox = document.getElementById('galleryLightbox');
  const lightboxImage = document.getElementById('lightboxImage');
  const lightboxCaption = document.getElementById('lightboxCaption');
  const lightboxCounter = document.getElementById('lightboxCounter');
  const closeButton = document.getElementById('lightboxClose');
  const prevButton = document.getElementById('lightboxPrev');
  const nextButton = document.getElementById('lightboxNext');
  let activeIndex = 0;
  let lastFocused = null;
  let pointerStartX = null;

  const strings = lang === 'hu'
    ? {
        open: 'Kép nagyítása',
        counter: (current) => `${current} / ${photos.length}`,
        count: `${photos.length} pillanat a laborunkból`
      }
    : {
        open: 'Bild vergrößern',
        counter: (current) => `${current} / ${photos.length}`,
        count: `${photos.length} Aufnahmen aus unserem Labor`
      };

  const fileFor = (index, size) => `${assetRoot}/${size}/photo-${String(photos[index][0]).padStart(3, '0')}.webp`;
  const captionFor = (index) => photos[index][lang === 'hu' ? 4 : 3];

  if (galleryCount) galleryCount.textContent = strings.count;

  photos.forEach((photo, index) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'gallery-item';
    button.dataset.index = String(index);
    button.setAttribute('aria-label', `${strings.open}: ${captionFor(index)}`);

    const image = document.createElement('img');
    image.src = fileFor(index, 'thumb-480');
    image.srcset = `${fileFor(index, 'thumb-480')} 480w, ${fileFor(index, 'thumb-960')} 960w`;
    image.sizes = '(max-width: 420px) 100vw, (max-width: 760px) 50vw, (max-width: 1120px) 33vw, 25vw';
    image.alt = captionFor(index);
    image.width = photo[1];
    image.height = photo[2];
    image.decoding = 'async';
    image.loading = index < 6 ? 'eager' : 'lazy';
    button.append(image);
    grid.append(button);
  });

  const layoutGrid = () => {
    const gridStyles = window.getComputedStyle(grid);
    const columns = gridStyles.gridTemplateColumns.split(' ').filter(Boolean).length || 1;
    const rowHeight = Number.parseFloat(gridStyles.gridAutoRows) || 1;
    const gap = Number.parseFloat(gridStyles.rowGap) || 0;
    const columnWidth = (grid.clientWidth - gap * (columns - 1)) / columns;

    grid.querySelectorAll('.gallery-item').forEach((item, index) => {
      const photo = photos[index];
      const imageHeight = columnWidth * (photo[2] / photo[1]);
      const span = Math.ceil((imageHeight + gap) / (rowHeight + gap));
      const nextValue = `span ${span}`;
      if (item.style.gridRowEnd !== nextValue) item.style.gridRowEnd = nextValue;
    });
  };

  let layoutFrame = 0;
  const scheduleGridLayout = () => {
    window.cancelAnimationFrame(layoutFrame);
    layoutFrame = window.requestAnimationFrame(layoutGrid);
  };
  scheduleGridLayout();
  window.addEventListener('resize', scheduleGridLayout, { passive: true });

  const setActivePhoto = (index) => {
    activeIndex = (index + photos.length) % photos.length;
    lightboxImage.src = fileFor(activeIndex, 'full');
    lightboxImage.alt = captionFor(activeIndex);
    lightboxCaption.textContent = captionFor(activeIndex);
    lightboxCounter.textContent = strings.counter(activeIndex + 1);

    [-1, 1].forEach((offset) => {
      const preload = new Image();
      preload.src = fileFor((activeIndex + offset + photos.length) % photos.length, 'full');
    });
  };

  const openLightbox = (index, trigger) => {
    lastFocused = trigger;
    setActivePhoto(index);
    lightbox.classList.add('open');
    lightbox.setAttribute('aria-hidden', 'false');
    body.classList.add('lightbox-open');
    closeButton.focus({ preventScroll: true });
  };

  const closeLightbox = () => {
    lightbox.classList.remove('open');
    lightbox.setAttribute('aria-hidden', 'true');
    body.classList.remove('lightbox-open');
    lightboxImage.removeAttribute('src');
    if (lastFocused) lastFocused.focus({ preventScroll: true });
  };

  grid.addEventListener('click', (event) => {
    const trigger = event.target.closest('.gallery-item');
    if (trigger) openLightbox(Number(trigger.dataset.index), trigger);
  });
  closeButton.addEventListener('click', closeLightbox);
  prevButton.addEventListener('click', () => setActivePhoto(activeIndex - 1));
  nextButton.addEventListener('click', () => setActivePhoto(activeIndex + 1));
  lightbox.addEventListener('click', (event) => {
    if (event.target === lightbox || event.target.classList.contains('lightbox-stage')) closeLightbox();
  });

  lightbox.addEventListener('pointerdown', (event) => { pointerStartX = event.clientX; });
  lightbox.addEventListener('pointerup', (event) => {
    if (pointerStartX === null) return;
    const distance = event.clientX - pointerStartX;
    pointerStartX = null;
    if (Math.abs(distance) > 55) setActivePhoto(activeIndex + (distance < 0 ? 1 : -1));
  });

  document.addEventListener('keydown', (event) => {
    if (!lightbox.classList.contains('open')) return;
    if (event.key === 'Escape') closeLightbox();
    if (event.key === 'ArrowLeft') setActivePhoto(activeIndex - 1);
    if (event.key === 'ArrowRight') setActivePhoto(activeIndex + 1);
    if (event.key === 'Tab') {
      const controls = [closeButton, prevButton, nextButton];
      const first = controls[0];
      const last = controls[controls.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }
  });

  const burger = document.getElementById('galleryBurger');
  const mobileMenu = document.getElementById('galleryMobileMenu');
  if (burger && mobileMenu) {
    const closeMenu = () => {
      burger.classList.remove('open');
      mobileMenu.classList.remove('open');
      burger.setAttribute('aria-expanded', 'false');
      if (!lightbox.classList.contains('open')) body.style.overflow = '';
    };
    burger.addEventListener('click', () => {
      const open = mobileMenu.classList.toggle('open');
      burger.classList.toggle('open', open);
      burger.setAttribute('aria-expanded', String(open));
      body.style.overflow = open ? 'hidden' : '';
    });
    mobileMenu.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeMenu));
  }
})();
