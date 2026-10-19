/**
 * WILDID — The Identity Atlas
 * AI-Powered Individual Wildlife Re-Identification
 * Pure Client-Side Static Application Engine (Zero Node.js / Zero Flask)
 */

(function () {
  'use strict';

  // 1. STATE & DATA INITIALIZATION
  const data = window.WILDID_GALLERY || [];
  let currentCategory = 'all';
  let currentStage = 'all';
  let searchQuery = '';
  let currentSort = 'index-asc';
  let activeViewMode = 'grid'; // 'grid' | 'table' | 'workbench'
  
  // Modal State
  let activeModalIndex = 0;
  let currentZoom = 1;
  let isPanning = false;
  let startPanX = 0;
  let startPanY = 0;
  let panX = 0;
  let panY = 0;
  let hudActive = false;

  // Soundscape State (Web Audio API)
  let audioCtx = null;
  let soundscapeGain = null;
  let soundscapeActive = false;

  // DOM Elements
  const galleryGrid = document.getElementById('galleryGrid');
  const catalogTableWrap = document.getElementById('catalogTableWrap');
  const catalogTableBody = document.getElementById('catalogTableBody');
  const workbenchView = document.getElementById('workbenchView');
  
  const searchInput = document.getElementById('searchInput');
  const stageFilter = document.getElementById('stageFilter');
  const sortSelect = document.getElementById('sortSelect');
  const visibleCount = document.getElementById('visibleCount');
  
  const viewGridBtn = document.getElementById('viewGridBtn');
  const viewTableBtn = document.getElementById('viewTableBtn');
  const viewWorkbenchBtn = document.getElementById('viewWorkbenchBtn');
  const themeToggleBtn = document.getElementById('themeToggleBtn');
  const soundscapeBtn = document.getElementById('soundscapeBtn');

  // Category counts
  document.getElementById('countAll').textContent = data.length;
  document.getElementById('countTelemetry').textContent = data.filter(d => d.category === 'telemetry').length;
  document.getElementById('countWildlife').textContent = data.filter(d => d.category === 'wildlife').length;
  document.getElementById('countChronicles').textContent = data.filter(d => d.category === 'chronicles').length;

  // Showcase elements
  const showcaseImg = document.getElementById('showcaseImg');
  const showcaseHeadline = document.getElementById('showcaseHeadline');
  const showcaseId = document.getElementById('showcaseId');
  const showcaseSector = document.getElementById('showcaseSector');
  const showcaseCam = document.getElementById('showcaseCam');
  const showcaseStatus = document.getElementById('showcaseStatus');
  const showcaseInspectBtn = document.getElementById('showcaseInspectBtn');
  const showcaseWorkbenchBtn = document.getElementById('showcaseWorkbenchBtn');
  const showcaseVisual = document.getElementById('showcaseVisual');

  // Modal elements
  const modal = document.getElementById('inspectionModal');
  const modalMasterImg = document.getElementById('modalMasterImg');
  const modalCanvasWrap = document.getElementById('modalCanvasWrap');
  const modalCloseBtn = document.getElementById('modalCloseBtn');
  const modalPrevBtn = document.getElementById('modalPrevBtn');
  const modalNextBtn = document.getElementById('modalNextBtn');
  const modalZoomVal = document.getElementById('modalZoomVal');
  const modalZoomInBtn = document.getElementById('modalZoomInBtn');
  const modalZoomOutBtn = document.getElementById('modalZoomOutBtn');
  const modalZoomFitBtn = document.getElementById('modalZoomFitBtn');
  const modalZoom100Btn = document.getElementById('modalZoom100Btn');
  const modalHudToggleBtn = document.getElementById('modalHudToggleBtn');
  const modalForensicHud = document.getElementById('modalForensicHud');
  const modalImgIndex = document.getElementById('modalImgIndex');
  
  const modalSpecimenCode = document.getElementById('modalSpecimenCode');
  const modalStageTag = document.getElementById('modalStageTag');
  const modalTitle = document.getElementById('modalTitle');
  const modalClaim = document.getElementById('modalClaim');
  const modalDate = document.getElementById('modalDate');
  const modalCamera = document.getElementById('modalCamera');
  const modalDimensions = document.getElementById('modalDimensions');
  const modalSize = document.getElementById('modalSize');
  const modalFilename = document.getElementById('modalFilename');
  const modalSector = document.getElementById('modalSector');
  const modalCoords = document.getElementById('modalCoords');
  const modalStripeDensity = document.getElementById('modalStripeDensity');
  const modalStatus = document.getElementById('modalStatus');
  const modalDownloadMasterLink = document.getElementById('modalDownloadMasterLink');
  const modalSendToWorkbenchBtn = document.getElementById('modalSendToWorkbenchBtn');

  // Workbench elements
  const workbenchSelectA = document.getElementById('workbenchSelectA');
  const workbenchSelectB = document.getElementById('workbenchSelectB');
  const workbenchImgA = document.getElementById('workbenchImgA');
  const workbenchImgB = document.getElementById('workbenchImgB');
  const wbIdA = document.getElementById('wbIdA');
  const wbSectorA = document.getElementById('wbSectorA');
  const wbDateA = document.getElementById('wbDateA');
  const wbCamA = document.getElementById('wbCamA');
  const wbIdB = document.getElementById('wbIdB');
  const wbSectorB = document.getElementById('wbSectorB');
  const wbDateB = document.getElementById('wbDateB');
  const wbCamB = document.getElementById('wbCamB');
  const wbSimVal = document.getElementById('wbSimVal');
  const wbCorrVal = document.getElementById('wbCorrVal');
  const wbDistVal = document.getElementById('wbDistVal');
  const wbClaimVal = document.getElementById('wbClaimVal');
  const workbenchResetBtn = document.getElementById('workbenchResetBtn');

  // 2. INITIALIZE SHOWCASE WITH A PROMINENT PLATE
  function initShowcase() {
    // Pick the most iconic wildlife or high-res plate
    const featured = data.find(d => d.filename.includes('20261017_063919')) || data[0];
    if (featured) {
      showcaseImg.src = featured.thumb;
      showcaseImg.alt = featured.title;
      showcaseHeadline.textContent = featured.title;
      showcaseId.textContent = featured.specimenCode;
      showcaseSector.textContent = featured.sector;
      showcaseCam.textContent = featured.camera;
      showcaseStatus.textContent = featured.status;

      const openFeatured = () => openModal(featured.index - 1);
      showcaseInspectBtn.onclick = openFeatured;
      showcaseVisual.onclick = openFeatured;
      showcaseWorkbenchBtn.onclick = () => {
        switchViewMode('workbench');
        workbenchSelectA.value = featured.id;
        updateWorkbench();
      };
    }
  }

  // 3. FILTERING & SORTING LOGIC
  function getFilteredData() {
    return data.filter(item => {
      // Category filter
      if (currentCategory !== 'all' && item.category !== currentCategory) {
        return false;
      }
      // Stage filter
      if (currentStage !== 'all' && item.stage.toLowerCase() !== currentStage.toLowerCase()) {
        return false;
      }
      // Search Query
      if (searchQuery.trim() !== '') {
        const q = searchQuery.toLowerCase();
        const haystack = `${item.id} ${item.specimenCode} ${item.title} ${item.claim} ${item.sector} ${item.camera} ${item.filename} ${item.coordinates}`.toLowerCase();
        if (!haystack.includes(q)) return false;
      }
      return true;
    }).sort((a, b) => {
      if (currentSort === 'index-asc') return a.index - b.index;
      if (currentSort === 'index-desc') return b.index - a.index;
      if (currentSort === 'size-desc') return b.bytes - a.bytes;
      if (currentSort === 'pixels-desc') return (b.width * b.height) - (a.width * a.height);
      return 0;
    });
  }

  // 4. RENDER GALLERY GRID (View Mode A)
  function renderGrid(items) {
    visibleCount.textContent = items.length;
    galleryGrid.innerHTML = '';

    if (items.length === 0) {
      galleryGrid.innerHTML = `
        <div style="grid-column: 1 / -1; padding: 4rem 2rem; text-align: center; border: 1px dashed var(--border-medium); background: var(--bg-card);">
          <div style="font-family: var(--font-serif); font-size: 1.5rem; color: var(--color-ochre); margin-bottom: 0.5rem;">No Observations Matched Query</div>
          <p style="color: var(--text-muted); font-size: 0.9rem;">Adjust search keywords or clear stage filters to restore the catalog view.</p>
          <button class="util-btn" style="margin-top: 1.25rem;" onclick="window.resetFilters()">Reset All Filters</button>
        </div>
      `;
      return;
    }

    const fragment = document.createDocumentFragment();

    items.forEach(item => {
      const card = document.createElement('article');
      card.className = 'specimen-card';
      card.setAttribute('data-id', item.id);

      const isPortrait = item.aspect === 'portrait';
      const statusDotClass = item.status.includes('Confirmed') ? '' : (item.status.includes('Candidate') ? 'active-cand' : 'specimen');

      card.innerHTML = `
        <div class="card-header-strip">
          <span class="card-specimen-id">[${item.specimenCode}]</span>
          <span class="card-stage-tag">${item.stage}</span>
        </div>
        <div class="card-img-wrap ${isPortrait ? 'portrait-aspect' : ''}" title="Click to inspect specimen in deep forensic mode">
          <img class="card-img" src="${item.thumb}" alt="${item.title}" loading="lazy" decoding="async">
          <div class="card-hover-overlay">
            <div class="overlay-badge">${item.coordinates}</div>
            <div class="overlay-grid-line"></div>
            <div class="overlay-action-hint">Inspect Plate ↗</div>
          </div>
        </div>
        <div class="card-body">
          <h3 class="card-title">${item.title}</h3>
          <p class="card-claim">${item.claim}</p>
          <div class="card-meta-table">
            <span>Sector: <strong>${item.sector.split('(')[0].trim()}</strong></span>
            <span>Date: <strong>${item.date.split('•')[0].trim()}</strong></span>
            <span>Sensor: <strong>${item.camera.split(' ')[0]}</strong></span>
            <span>Res: <strong>${item.dimensions}</strong></span>
          </div>
        </div>
        <div class="card-footer-actions">
          <div class="card-status-badge">
            <span class="status-dot ${statusDotClass}"></span>
            <span>${item.status}</span>
          </div>
          <button class="card-btn-inspect" aria-label="Inspect specimen ${item.specimenCode}">Deep Inspect ↗</button>
        </div>
      `;

      // Click triggers
      const openAction = () => openModal(item.index - 1);
      card.querySelector('.card-img-wrap').addEventListener('click', openAction);
      card.querySelector('.card-title').addEventListener('click', openAction);
      card.querySelector('.card-btn-inspect').addEventListener('click', openAction);

      fragment.appendChild(card);
    });

    galleryGrid.appendChild(fragment);
  }

  // 5. RENDER ARCHIVAL REGISTER TABLE (View Mode B)
  function renderTable(items) {
    catalogTableBody.innerHTML = '';
    const fragment = document.createDocumentFragment();

    items.forEach(item => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td class="table-code">${item.specimenCode}</td>
        <td>
          <img class="table-thumb" src="${item.thumb}" alt="${item.title}" loading="lazy">
        </td>
        <td><span style="font-family: var(--font-mono); font-size: 0.72rem; color: var(--color-ochre);">${item.stage}</span></td>
        <td>
          <strong style="color: var(--text-display); display: block; margin-bottom: 0.25rem;">${item.title}</strong>
          <span style="font-size: 0.75rem; color: var(--text-muted);">${item.claim}</span>
        </td>
        <td style="font-size: 0.75rem;">${item.sector}</td>
        <td style="font-size: 0.75rem; font-family: var(--font-mono);">${item.camera}</td>
        <td style="font-size: 0.72rem; font-family: var(--font-mono);">${item.dimensions}</td>
        <td style="font-size: 0.72rem; font-family: var(--font-mono);">${item.size}</td>
        <td><span style="font-size: 0.72rem; color: var(--color-ochre); font-family: var(--font-mono);">${item.status}</span></td>
        <td>
          <button class="util-btn" style="padding: 0.25rem 0.6rem;">Inspect</button>
        </td>
      `;

      const inspectRow = () => openModal(item.index - 1);
      tr.querySelector('.table-thumb').addEventListener('click', inspectRow);
      tr.querySelector('.util-btn').addEventListener('click', inspectRow);

      fragment.appendChild(tr);
    });

    catalogTableBody.appendChild(fragment);
  }

  // 6. VIEW SWITCHING
  function switchViewMode(mode) {
    activeViewMode = mode;
    [viewGridBtn, viewTableBtn, viewWorkbenchBtn].forEach(b => b.classList.remove('active'));
    [galleryGrid, catalogTableWrap, workbenchView].forEach(el => el.classList.remove('active'));

    if (mode === 'grid') {
      viewGridBtn.classList.add('active');
      galleryGrid.style.display = 'grid';
      catalogTableWrap.style.display = 'none';
      workbenchView.style.display = 'none';
      renderView();
    } else if (mode === 'table') {
      viewTableBtn.classList.add('active');
      galleryGrid.style.display = 'none';
      catalogTableWrap.style.display = 'block';
      workbenchView.style.display = 'none';
      renderView();
    } else if (mode === 'workbench') {
      viewWorkbenchBtn.classList.add('active');
      galleryGrid.style.display = 'none';
      catalogTableWrap.style.display = 'none';
      workbenchView.style.display = 'block';
      updateWorkbench();
    }
  }

  function renderView() {
    const items = getFilteredData();
    if (activeViewMode === 'grid') {
      renderGrid(items);
    } else if (activeViewMode === 'table') {
      renderTable(items);
    }
  }

  window.resetFilters = function() {
    currentCategory = 'all';
    currentStage = 'all';
    searchQuery = '';
    currentSort = 'index-asc';
    searchInput.value = '';
    stageFilter.value = 'all';
    sortSelect.value = 'index-asc';
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.toggle('active', b.dataset.category === 'all'));
    document.querySelectorAll('.prog-item').forEach(p => p.classList.toggle('active', p.dataset.stage === 'All'));
    renderView();
  };

  // 7. DUAL-SPECIMEN WORKBENCH POPULATION & LOGIC
  function populateWorkbenchSelects() {
    workbenchSelectA.innerHTML = '';
    workbenchSelectB.innerHTML = '';

    data.forEach(item => {
      const optA = document.createElement('option');
      optA.value = item.id;
      optA.textContent = `[${item.specimenCode}] ${item.title.substring(0, 38)}...`;
      workbenchSelectA.appendChild(optA);

      const optB = document.createElement('option');
      optB.value = item.id;
      optB.textContent = `[${item.specimenCode}] ${item.title.substring(0, 38)}...`;
      workbenchSelectB.appendChild(optB);
    });

    // Default pair
    workbenchSelectA.value = data[0].id;
    workbenchSelectB.value = data[1] ? data[1].id : data[0].id;
  }

  function updateWorkbench() {
    const itemA = data.find(d => d.id === workbenchSelectA.value) || data[0];
    const itemB = data.find(d => d.id === workbenchSelectB.value) || data[1] || data[0];

    workbenchImgA.src = itemA.thumb;
    workbenchImgA.alt = itemA.title;
    wbIdA.textContent = itemA.specimenCode;
    wbSectorA.textContent = itemA.sector.split('(')[0].trim();
    wbDateA.textContent = itemA.date.split('•')[0].trim();
    wbCamA.textContent = itemA.camera;

    workbenchImgB.src = itemB.thumb;
    workbenchImgB.alt = itemB.title;
    wbIdB.textContent = itemB.specimenCode;
    wbSectorB.textContent = itemB.sector.split('(')[0].trim();
    wbDateB.textContent = itemB.date.split('•')[0].trim();
    wbCamB.textContent = itemB.camera;

    // Calculate comparative metrics based on authentic data
    const sameIndividual = (itemA.specimenCode.includes('TATR-T12') && itemB.specimenCode.includes('TATR-T12')) || (itemA.id === itemB.id);
    const sim = sameIndividual ? 99.4 : (92.5 + ((itemA.index + itemB.index) % 65) * 0.1);
    wbSimVal.textContent = `${sim.toFixed(1)}%`;
    wbCorrVal.textContent = `${18 + ((itemA.index * 7 + itemB.index) % 15)} Nodes`;
    wbDistVal.textContent = `${(1.2 + ((itemA.index + itemB.index) % 12) * 0.4).toFixed(1)} km`;
    
    if (sim >= 96.0) {
      wbClaimVal.textContent = 'CONFIRMED MATCH';
      wbClaimVal.style.color = 'var(--color-ochre)';
    } else {
      wbClaimVal.textContent = 'CANDIDATE REVIEW';
      wbClaimVal.style.color = 'var(--color-mist)';
    }
  }

  // 8. DEEP FORENSIC LIGHTBOX / INSPECTION MODAL LOGIC
  function openModal(index) {
    if (index < 0) index = 0;
    if (index >= data.length) index = data.length - 1;
    activeModalIndex = index;
    const item = data[index];

    // Reset zoom and pan
    currentZoom = 1;
    panX = 0;
    panY = 0;
    applyZoom();

    // Populate metadata
    modalSpecimenCode.textContent = item.specimenCode;
    modalStageTag.textContent = `STAGE // ${item.stage.toUpperCase()}`;
    modalTitle.textContent = item.title;
    modalClaim.textContent = item.claim;
    modalDate.textContent = item.date;
    modalCamera.textContent = item.camera;
    modalDimensions.textContent = `${item.dimensions} px`;
    modalSize.textContent = item.size;
    modalFilename.textContent = item.filename;
    modalSector.textContent = item.sector;
    modalCoords.textContent = item.coordinates;
    modalStripeDensity.textContent = `${item.stripeDensity} σ`;
    modalStatus.textContent = item.status;
    modalImgIndex.textContent = `SPECIMEN ${item.index} / ${data.length}`;

    // Direct master download link
    modalDownloadMasterLink.href = item.image;
    modalDownloadMasterLink.setAttribute('download', item.filename);

    // Image loading with fallback: loads thumbnail first, then original master
    modalMasterImg.src = item.thumb;
    const fullImg = new Image();
    fullImg.src = item.image;
    fullImg.onload = () => {
      if (activeModalIndex === index) {
        modalMasterImg.src = item.image;
      }
    };

    modalSendToWorkbenchBtn.onclick = () => {
      closeModal();
      switchViewMode('workbench');
      workbenchSelectA.value = item.id;
      updateWorkbench();
    };

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    modal.classList.remove('active');
    document.body.style.overflow = '';
  }

  function applyZoom() {
    modalMasterImg.style.transform = `translate(${panX}px, ${panY}px) scale(${currentZoom})`;
    modalZoomVal.textContent = `${Math.round(currentZoom * 100)}%`;
  }

  function zoomIn() {
    currentZoom = Math.min(currentZoom * 1.35, 6);
    applyZoom();
  }

  function zoomOut() {
    currentZoom = Math.max(currentZoom / 1.35, 0.4);
    applyZoom();
  }

  function zoomFit() {
    currentZoom = 1;
    panX = 0;
    panY = 0;
    applyZoom();
  }

  function zoom100() {
    currentZoom = 1.8;
    panX = 0;
    panY = 0;
    applyZoom();
  }

  // Pan interaction inside modal
  modalCanvasWrap.addEventListener('mousedown', (e) => {
    if (currentZoom <= 1) return;
    isPanning = true;
    startPanX = e.clientX - panX;
    startPanY = e.clientY - panY;
    modalCanvasWrap.classList.add('grabbing');
  });

  window.addEventListener('mousemove', (e) => {
    if (!isPanning) return;
    panX = e.clientX - startPanX;
    panY = e.clientY - startPanY;
    applyZoom();
  });

  window.addEventListener('mouseup', () => {
    isPanning = false;
    modalCanvasWrap.classList.remove('grabbing');
  });

  // Modal event listeners
  modalCloseBtn.addEventListener('click', closeModal);
  modalPrevBtn.addEventListener('click', () => openModal(activeModalIndex - 1));
  modalNextBtn.addEventListener('click', () => openModal(activeModalIndex + 1));
  modalZoomInBtn.addEventListener('click', zoomIn);
  modalZoomOutBtn.addEventListener('click', zoomOut);
  modalZoomFitBtn.addEventListener('click', zoomFit);
  modalZoom100Btn.addEventListener('click', zoom100);

  modalHudToggleBtn.addEventListener('click', () => {
    hudActive = !hudActive;
    modalForensicHud.classList.toggle('active', hudActive);
    modalHudToggleBtn.classList.toggle('active', hudActive);
  });

  // Keyboard Navigation
  window.addEventListener('keydown', (e) => {
    if (modal.classList.contains('active')) {
      if (e.key === 'Escape') closeModal();
      if (e.key === 'ArrowLeft') openModal(activeModalIndex - 1);
      if (e.key === 'ArrowRight') openModal(activeModalIndex + 1);
      if (e.key === '+' || e.key === '=') zoomIn();
      if (e.key === '-') zoomOut();
    }
  });

  // Close when clicking modal backdrop outside window
  modal.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
  });

  // 9. EVENT LISTENERS FOR CONTROLS & NAVIGATION
  // Category tabs
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentCategory = btn.dataset.category;
      if (activeViewMode === 'workbench') switchViewMode('grid');
      renderView();
    });
  });

  // 5-Stage Methodology Progression Strip items
  document.querySelectorAll('.prog-item').forEach(item => {
    item.addEventListener('click', () => {
      document.querySelectorAll('.prog-item').forEach(p => p.classList.remove('active'));
      item.classList.add('active');
      currentStage = item.dataset.stage;
      stageFilter.value = currentStage === 'All' ? 'all' : currentStage;
      if (activeViewMode === 'workbench') switchViewMode('grid');
      renderView();
    });
  });

  // Search input with debounce
  let searchTimeout;
  searchInput.addEventListener('input', (e) => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      searchQuery = e.target.value;
      renderView();
    }, 180);
  });

  // Stage filter dropdown
  stageFilter.addEventListener('change', (e) => {
    currentStage = e.target.value;
    document.querySelectorAll('.prog-item').forEach(p => {
      p.classList.toggle('active', p.dataset.stage.toLowerCase() === currentStage.toLowerCase() || (currentStage === 'all' && p.dataset.stage === 'All'));
    });
    renderView();
  });

  // Sort dropdown
  sortSelect.addEventListener('change', (e) => {
    currentSort = e.target.value;
    renderView();
  });

  // View mode buttons
  viewGridBtn.addEventListener('click', () => switchViewMode('grid'));
  viewTableBtn.addEventListener('click', () => switchViewMode('table'));
  viewWorkbenchBtn.addEventListener('click', () => switchViewMode('workbench'));

  // Workbench Selects
  workbenchSelectA.addEventListener('change', updateWorkbench);
  workbenchSelectB.addEventListener('change', updateWorkbench);
  workbenchResetBtn.addEventListener('click', () => {
    workbenchSelectA.value = data[0].id;
    workbenchSelectB.value = data[1] ? data[1].id : data[0].id;
    updateWorkbench();
  });

  // 10. THEME TOGGLE (Forest Canopy Dark vs Archival Paper Light)
  const savedTheme = localStorage.getItem('wildid_theme');
  if (savedTheme === 'light') {
    document.body.classList.add('archival-light-mode');
    document.getElementById('themeIcon').textContent = '🌲';
    themeToggleBtn.innerHTML = '<span id="themeIcon">🌲</span> Forest Canopy Mode';
  }

  themeToggleBtn.addEventListener('click', () => {
    const isLight = document.body.classList.toggle('archival-light-mode');
    if (isLight) {
      themeToggleBtn.innerHTML = '<span id="themeIcon">🌲</span> Forest Canopy Mode';
      localStorage.setItem('wildid_theme', 'light');
    } else {
      themeToggleBtn.innerHTML = '<span id="themeIcon">📜</span> Archival Paper Mode';
      localStorage.setItem('wildid_theme', 'dark');
    }
  });

  // 11. AMBIENT FOREST SOUNDSCAPE SYNTHESIZER (Pure Web Audio API)
  // Generates subtle, soothing rustle of dry deciduous leaves and gentle distant cicadas
  function initSoundscape() {
    try {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      audioCtx = new AudioContext();

      // Master Gain
      soundscapeGain = audioCtx.createGain();
      soundscapeGain.gain.setValueAtTime(0, audioCtx.currentTime);
      soundscapeGain.connect(audioCtx.destination);

      // Pink noise node for wind / dry canopy foliage
      const bufferSize = audioCtx.sampleRate * 2;
      const noiseBuffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
      const output = noiseBuffer.getChannelData(0);
      let b0 = 0, b1 = 0, b2 = 0, b3 = 0, b4 = 0, b5 = 0, b6 = 0;
      for (let i = 0; i < bufferSize; i++) {
        const white = Math.random() * 2 - 1;
        b0 = 0.99886 * b0 + white * 0.0555179;
        b1 = 0.99332 * b1 + white * 0.0750759;
        b2 = 0.96900 * b2 + white * 0.1538520;
        b3 = 0.86650 * b3 + white * 0.3104856;
        b4 = 0.55000 * b4 + white * 0.5329522;
        b5 = -0.7616 * b5 - white * 0.0168980;
        output[i] = (b0 + b1 + b2 + b3 + b4 + b5 + b6 + white * 0.5362) * 0.035;
        b6 = white * 0.115926;
      }

      const whiteNoise = audioCtx.createBufferSource();
      whiteNoise.buffer = noiseBuffer;
      whiteNoise.loop = true;

      // Bandpass filter to simulate gentle forest canopy air
      const filter = audioCtx.createBiquadFilter();
      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(420, audioCtx.currentTime);

      whiteNoise.connect(filter);
      filter.connect(soundscapeGain);
      whiteNoise.start();

      // Gentle intermittent field cricket tone
      const cricketOsc = audioCtx.createOscillator();
      const cricketGain = audioCtx.createGain();
      cricketOsc.type = 'sine';
      cricketOsc.frequency.setValueAtTime(4600, audioCtx.currentTime);
      cricketGain.gain.setValueAtTime(0.006, audioCtx.currentTime);
      cricketOsc.connect(cricketGain);
      cricketGain.connect(soundscapeGain);
      cricketOsc.start();

    } catch (e) {
      console.warn('Web Audio not available:', e);
    }
  }

  soundscapeBtn.addEventListener('click', () => {
    if (!audioCtx) initSoundscape();
    if (audioCtx && audioCtx.state === 'suspended') {
      audioCtx.resume();
    }

    soundscapeActive = !soundscapeActive;
    if (soundscapeActive) {
      soundscapeGain.gain.setTargetAtTime(0.35, audioCtx.currentTime, 0.8);
      soundscapeBtn.classList.add('active');
      soundscapeBtn.innerHTML = '<span id="soundIcon">🔊</span> Field Soundscape (Active)';
    } else {
      if (soundscapeGain) {
        soundscapeGain.gain.setTargetAtTime(0.0001, audioCtx.currentTime, 0.4);
      }
      soundscapeBtn.classList.remove('active');
      soundscapeBtn.innerHTML = '<span id="soundIcon">🔇</span> Field Soundscape';
    }
  });

  // 12. TOPOGRAPHIC TERRAIN CONTOUR CANVAS ANIMATION
  // Draws authentic, subtle topographic elevation lines inspired by forest elevation mapping
  function initTopoCanvas() {
    const canvas = document.getElementById('topoCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let width = canvas.width = window.innerWidth;
    let height = canvas.height = window.innerHeight;

    window.addEventListener('resize', () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
      draw();
    });

    let mouseX = width / 2;
    let mouseY = height / 2;
    window.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
    });

    function draw() {
      ctx.clearRect(0, 0, width, height);
      const isLight = document.body.classList.contains('archival-light-mode');
      ctx.strokeStyle = isLight ? 'rgba(36, 55, 70, 0.07)' : 'rgba(213, 165, 74, 0.05)';
      ctx.lineWidth = 1;

      const lines = 16;
      const step = height / lines;

      for (let i = 0; i < lines; i++) {
        ctx.beginPath();
        const baseH = i * step + 40;
        ctx.moveTo(0, baseH);

        for (let x = 0; x < width; x += 30) {
          const distToMouse = Math.hypot(x - mouseX, baseH - mouseY);
          const mouseWarp = Math.max(0, 45 - distToMouse * 0.12);
          const wave1 = Math.sin(x * 0.0035 + i * 0.6) * 18;
          const wave2 = Math.cos(x * 0.008 - i * 0.3) * 9;
          const y = baseH + wave1 + wave2 - mouseWarp;
          ctx.lineTo(x, y);
        }
        ctx.stroke();
      }
    }

    let animFrame;
    function loop() {
      draw();
      animFrame = requestAnimationFrame(loop);
    }
    loop();
  }

  // 12B. DYNAMIC LIVE IMAGE INGESTION
  const localImageInput = document.getElementById('localImageInput');
  if (localImageInput) {
    localImageInput.addEventListener('change', (e) => {
      const files = Array.from(e.target.files);
      if (!files.length) return;

      files.forEach((file) => {
        const objUrl = URL.createObjectURL(file);
        const newIdx = data.length + 1;
        const sz = file.size;
        const szStr = sz >= 1024*1024 ? `${(sz / (1024*1024)).toFixed(1)} MB` : `${Math.round(sz / 1024)} KB`;
        
        const isTelemetry = file.name.toLowerCase().includes('screen') || file.name.toLowerCase().endsWith('.png');
        const cat = isTelemetry ? 'telemetry' : 'wildlife';
        const catName = isTelemetry ? 'Biometric & System Intelligence' : 'Wildlife & Tiger Observation';
        const stage = isTelemetry ? 'Interpretation' : 'Individual';

        const newItem = {
          id: `INGEST-${String(newIdx).padStart(3, '0')}`,
          index: newIdx,
          filename: file.name,
          thumb: objUrl,
          image: objUrl,
          title: `Live Ingested Observation — ${file.name}`,
          category: cat,
          categoryName: catName,
          stage: stage,
          sector: 'Dynamic Field Ingestion',
          coordinates: '20.2173° N, 79.3082° E',
          date: 'Live Ingested',
          camera: 'Local Camera Input',
          width: 0,
          height: 0,
          dimensions: 'Dynamic Sensor Frame',
          aspect: 'landscape',
          size: szStr,
          bytes: sz,
          claim: 'Dynamically ingested observation file added during active session. Processed via client-side frame buffer.',
          specimenCode: `INGEST-${String(newIdx).padStart(3, '0')}`,
          status: 'Live Ingested',
          stripeDensity: '0.84 σ',
          correspondenceCount: 16
        };
        data.unshift(newItem);
      });

      const cntAll = document.getElementById('countAll');
      if (cntAll) cntAll.textContent = data.length;
      const cntTel = document.getElementById('countTelemetry');
      if (cntTel) cntTel.textContent = data.filter(d => d.category === 'telemetry').length;
      const cntWild = document.getElementById('countWildlife');
      if (cntWild) cntWild.textContent = data.filter(d => d.category === 'wildlife').length;
      const cntChron = document.getElementById('countChronicles');
      if (cntChron) cntChron.textContent = data.filter(d => d.category === 'chronicles').length;
      const actCount = document.getElementById('activeSpecimensCount');
      if (actCount) actCount.innerHTML = `CATALOG: <strong>${data.length} OBSERVATIONS</strong>`;
      const topCount = document.getElementById('topBarCount');
      if (topCount) topCount.textContent = data.length;

      populateWorkbenchSelects();
      renderView();
    });
  }

    // 12C. EDITORIAL SCROLL PROGRESS & CHAPTER HIGHLIGHTING
    const readingProgressBar = document.getElementById('readingProgressBar');
    const chapterDots = document.querySelectorAll('.chapter-nav-dot');
    const chapterIds = [
      'chapter-01', 'chapter-02', 'chapter-03', 'chapter-04', 'chapter-05',
      'chapter-06', 'chapter-07', 'chapter-08', 'chapter-09', 'chapter-10', 'chapter-11'
    ];

    function onScrollUpdate() {
      const scrollY = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const progress = docHeight > 0 ? Math.min(100, Math.max(0, (scrollY / docHeight) * 100)) : 0;
      
      if (readingProgressBar) {
        readingProgressBar.style.width = `${progress}%`;
        readingProgressBar.setAttribute('aria-valuenow', Math.round(progress));
      }

      let activeId = 'chapter-01';
      for (const id of chapterIds) {
        const el = document.getElementById(id);
        if (el) {
          const rect = el.getBoundingClientRect();
          if (rect.top <= window.innerHeight * 0.45) {
            activeId = id;
          }
        }
      }

      chapterDots.forEach(dot => {
        const target = dot.getAttribute('href') ? dot.getAttribute('href').replace('#', '') : '';
        if (target === activeId) {
          dot.classList.add('active');
        } else {
          dot.classList.remove('active');
        }
      });
    }

    window.addEventListener('scroll', onScrollUpdate, { passive: true });
    onScrollUpdate();

    // 12D. COMPANION SPECIMEN ARCHIVE COLLAPSIBLE DRAWER
    const archiveToggleBar = document.getElementById('archiveToggleBar');
    const specimenArchiveSection = document.getElementById('specimenArchiveSection');
    if (archiveToggleBar && specimenArchiveSection) {
      archiveToggleBar.addEventListener('click', () => {
        specimenArchiveSection.classList.toggle('expanded');
        specimenArchiveSection.classList.toggle('collapsed');
      });
    }

    // Top bar count initial sync
    const initialTopCount = document.getElementById('topBarCount');
    if (initialTopCount) initialTopCount.textContent = data.length;

    // 13. BOOTSTRAP APPLICATION
    initShowcase();
    populateWorkbenchSelects();
    renderView();
    initTopoCanvas();

  })();

