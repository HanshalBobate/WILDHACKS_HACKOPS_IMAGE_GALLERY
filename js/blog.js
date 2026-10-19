/**
 * WILDID — The Identity Atlas
 * Dynamic Blog Parser & Engine (Pure Client-Side Static)
 * Dynamically fetches and parses blog.txt so editing blog.txt updates the site!
 */

(function () {
  'use strict';

  const blogContainer = document.getElementById('blogArticleContent');
  const tocList = document.getElementById('tocList');
  const readingProgressBar = document.getElementById('readingProgressBar');
  const syncStatusEl = document.getElementById('blogSyncStatus');
  const rawTextModal = document.getElementById('rawTextModal');
  const rawTextContent = document.getElementById('rawTextContent');
  const viewRawBtn = document.getElementById('viewRawBtn');
  const closeRawBtn = document.getElementById('closeRawBtn');

  // Markdown to HTML converter tailored for blog.txt
  function parseMarkdown(md) {
    const lines = md.split('\n');
    let html = '';
    let inList = false;
    let inTable = false;
    let tableRows = [];
    let sectionCounter = 0;

    // Helper to format inline markdown
    function formatInline(text) {
      return text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
        .replace(/\*([^*]+)\*/g, '<em>$1</em>')
        .replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>')
        .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer" class="blog-link">$1 ↗</a>');
    }

    function flushList() {
      if (inList) {
        html += '</ul>\n';
        inList = false;
      }
    }

    function flushTable() {
      if (inTable && tableRows.length > 0) {
        let tHtml = '<div class="table-container"><table class="blog-data-table">\n<thead>\n<tr>';
        const headers = tableRows[0];
        headers.forEach(h => {
          tHtml += `<th>${formatInline(h.trim())}</th>`;
        });
        tHtml += '</tr>\n</thead>\n<tbody>\n';
        for (let i = 1; i < tableRows.length; i++) {
          tHtml += '<tr>';
          tableRows[i].forEach(cell => {
            tHtml += `<td>${formatInline(cell.trim())}</td>`;
          });
          tHtml += '</tr>\n';
        }
        tHtml += '</tbody>\n</table></div>\n';
        html += tHtml;
        inTable = false;
        tableRows = [];
      }
    }

    lines.forEach((line) => {
      const trimmed = line.trim();

      // Check if table row
      if (trimmed.startsWith('|') && trimmed.endsWith('|')) {
        flushList();
        // Skip separator row like |---|---|
        if (/^\|[-|\s]+\|$/.test(trimmed)) {
          return;
        }
        inTable = true;
        const cols = trimmed.slice(1, -1).split('|');
        tableRows.push(cols);
        return;
      } else if (inTable) {
        flushTable();
      }

      // Check bullet list
      if (trimmed.startsWith('- ')) {
        if (!inList) {
          inList = true;
          html += '<ul class="blog-bullet-list">\n';
        }
        const itemText = trimmed.substring(2);
        html += `<li>${formatInline(itemText)}</li>\n`;
        return;
      } else if (inList) {
        flushList();
      }

      // Empty line
      if (trimmed === '') {
        return;
      }

      // Headings
      if (trimmed.startsWith('# ')) {
        const titleText = trimmed.substring(2);
        html += `<h1 class="blog-main-title">${formatInline(titleText)}</h1>\n`;
        return;
      }

      if (trimmed.startsWith('## ')) {
        sectionCounter++;
        const h2Text = trimmed.substring(3);
        const sectionId = 'section-' + sectionCounter;
        html += `<h2 id="${sectionId}" class="blog-section-title"><span class="section-num">${sectionCounter.toString().padStart(2, '0')}</span> ${formatInline(h2Text)}</h2>\n`;
        return;
      }

      if (trimmed.startsWith('### ')) {
        const h3Text = trimmed.substring(4);
        html += `<h3 class="blog-sub-title">${formatInline(h3Text)}</h3>\n`;
        return;
      }

      // Blockquote
      if (trimmed.startsWith('> ')) {
        const quoteText = trimmed.substring(2);
        html += `<blockquote class="blog-blockquote"><p>${formatInline(quoteText)}</p></blockquote>\n`;
        return;
      }

      // Horizontal rule
      if (trimmed === '---') {
        html += '<hr class="blog-divider">\n';
        return;
      }

      // Byline check
      if (trimmed.startsWith('By Hanshal Bobate')) {
        html += `<div class="blog-byline-banner">
          <div class="byline-avatar">HB</div>
          <div class="byline-details">
            <span class="byline-author">Hanshal Bobate</span>
            <span class="byline-meta">Team HackOPs · October 16–17, 2026 · WILDHACK 2K26</span>
          </div>
          <div class="byline-tag">SPECIAL MENTION AWARD</div>
        </div>\n`;
        return;
      }

      // Standard Paragraph
      html += `<p class="blog-p">${formatInline(trimmed)}</p>\n`;
    });

    flushList();
    flushTable();

    return html;
  }

  // Generate Table of Contents from parsed H2 elements
  function buildTableOfContents() {
    tocList.innerHTML = '';
    const h2Elements = blogContainer.querySelectorAll('h2.blog-section-title');
    h2Elements.forEach((h2, idx) => {
      const li = document.createElement('li');
      li.className = 'toc-item';
      
      const a = document.createElement('a');
      a.href = '#' + h2.id;
      a.className = 'toc-link';
      // Clean up text
      const cleanText = h2.textContent.replace(/^\d+\s*/, '').trim();
      a.innerHTML = `<span class="toc-num">${(idx + 1).toString().padStart(2, '0')}</span> <span class="toc-label">${cleanText}</span>`;
      
      a.addEventListener('click', (e) => {
        e.preventDefault();
        h2.scrollIntoView({ behavior: 'smooth', block: 'start' });
        history.replaceState(null, null, '#' + h2.id);
      });

      li.appendChild(a);
      tocList.appendChild(li);
    });

    // Setup active scrollspy
    setupScrollSpy(h2Elements);
  }

  function setupScrollSpy(h2Elements) {
    const tocLinks = tocList.querySelectorAll('.toc-link');
    window.addEventListener('scroll', () => {
      const scrollPos = window.scrollY + 140;
      let currentActive = null;

      h2Elements.forEach(h2 => {
        if (h2.offsetTop <= scrollPos) {
          currentActive = h2.id;
        }
      });

      tocLinks.forEach(link => {
        if (link.getAttribute('href') === '#' + currentActive) {
          link.classList.add('active');
        } else {
          link.classList.remove('active');
        }
      });

      // Reading progress bar
      const winHeight = document.documentElement.scrollHeight - window.innerHeight;
      if (winHeight > 0) {
        const progress = (window.scrollY / winHeight) * 100;
        readingProgressBar.style.width = Math.min(100, Math.max(0, progress)) + '%';
      }
    });
  }

  // Injects editorial photos from gallery into matching blog sections
  function injectEditorialPhotos() {
    // 1. Photo of Team HackOps in Section 3
    const sec3 = document.getElementById('section-3');
    if (sec3) {
      const photoCard = document.createElement('figure');
      photoCard.className = 'blog-editorial-figure';
      photoCard.innerHTML = `
        <div class="figure-img-frame">
          <img src="thumbs/IMG_20261016_131054.jpg" alt="Team HackOps at WILDHACK 2K26" loading="lazy">
          <div class="figure-reticle-corner">[TEAM HACKOPS // BIT BAMNI CAMPUS]</div>
        </div>
        <figcaption class="figure-caption">
          <strong>Figure 1.1 // Team HackOPs at WILDHACK 2K26:</strong> Hanshal Bobate, Vaishnav Balpande, Lokesh Parate, and Soham Bagmare gathered around the campus installation at Ballarpur Institute of Technology before the hackathon kickoff.
        </figcaption>
      `;
      sec3.parentNode.insertBefore(photoCard, sec3.nextSibling);
    }

    // 2. Photo of Tiger Biometric Prototype in Section 4
    const sec4 = document.getElementById('section-4');
    if (sec4) {
      const photoCard = document.createElement('figure');
      photoCard.className = 'blog-editorial-figure';
      photoCard.innerHTML = `
        <div class="figure-img-frame">
          <img src="thumbs/IMG-20261017-WA0010.jpg" alt="Biometric Screen Test of Tiger Re-ID" loading="lazy">
          <div class="figure-reticle-corner">[PROTOTYPE SCREEN // TIGER RE-ID BENCH]</div>
        </div>
        <figcaption class="figure-caption">
          <strong>Figure 2.1 // Biometric Stripe Isolation Prototype:</strong> Testing invariant stripe feature extraction across multiple candidate tiger postures and camera angles on our development workstation.
        </figcaption>
      `;
      sec4.parentNode.insertBefore(photoCard, sec4.nextSibling);
    }

    // 3. Biometric Verification Channels in Section 8
    const sec8 = document.getElementById('section-8');
    if (sec8) {
      const photoCard = document.createElement('figure');
      photoCard.className = 'blog-editorial-figure';
      photoCard.innerHTML = `
        <div class="figure-img-frame">
          <img src="thumbs/Screenshot 2026-10-17 080835.png" alt="Biometric Verification Channels" loading="lazy">
          <div class="figure-reticle-corner">[SYS-TELEMETRY // PIPELINE BENCH]</div>
        </div>
        <figcaption class="figure-caption">
          <strong>Figure 3.1 // Multi-Stage Computer Vision Pipeline:</strong> Surface isolation, high-pass stripe topology extraction, and real-time comparison channels against the park reference registry.
        </figcaption>
      `;
      sec8.parentNode.insertBefore(photoCard, sec8.nextSibling);
    }

    // 4. Reserve-Wide Roaming Territory in Section 10
    const sec10 = document.getElementById('section-10');
    if (sec10) {
      const photoCard = document.createElement('figure');
      photoCard.className = 'blog-editorial-figure';
      photoCard.innerHTML = `
        <div class="figure-img-frame">
          <img src="thumbs/Screenshot 2026-10-17 100531.png" alt="Reserve-Wide Roaming Territory GIS Map" loading="lazy">
          <div class="figure-reticle-corner">[GIS-CARTOGRAPHY // TADOBA RESERVE]</div>
        </div>
        <figcaption class="figure-caption">
          <strong>Figure 4.1 // Spatial GIS & Patrol Decision Support Dashboard:</strong> Whole-reserve interactive territory mapping connecting camera trap detections, home ranges, and Andheri River waterhole corridors.
        </figcaption>
      `;
      sec10.parentNode.insertBefore(photoCard, sec10.nextSibling);
    }

    // 5. Special Mention Award in Section 14
    const sec14 = document.getElementById('section-14');
    if (sec14) {
      const photoCard = document.createElement('figure');
      photoCard.className = 'blog-editorial-figure';
      photoCard.innerHTML = `
        <div class="figure-img-frame">
          <img src="thumbs/IMG-20261018-WA0000.jpg" alt="WILDHACK 2K26 Special Mention Citation and Medal" loading="lazy">
          <div class="figure-reticle-corner">[VALEDICTORY CITATION // SPECIAL MENTION]</div>
        </div>
        <figcaption class="figure-caption">
          <strong>Figure 5.1 // Special Mention Recognition:</strong> The official certificate of excellence and green-ribbon medal awarded to Team HackOPs by Ballarpur Institute of Technology and Tadoba-Andhari Tiger Reserve leadership.
        </figcaption>
      `;
      sec14.parentNode.insertBefore(photoCard, sec14.nextSibling);
    }
  }

  // Load and Render blog.txt dynamically
  async function loadBlog() {
    try {
      syncStatusEl.textContent = 'Synchronizing with blog.txt...';
      const cacheBust = '?t=' + Date.now();
      const response = await fetch('./blog.txt' + cacheBust);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const rawText = await response.text();
      rawTextContent.textContent = rawText;
      
      const parsedHtml = parseMarkdown(rawText);
      blogContainer.innerHTML = parsedHtml;

      injectEditorialPhotos();
      buildTableOfContents();

      syncStatusEl.innerHTML = '<span class="status-pulse-green"></span> Dynamically Synced with <code>blog.txt</code>';
    } catch (err) {
      console.warn('Dynamic fetch of blog.txt not available (likely file:// protocol):', err);
      // Fallback: If blog.html already has pre-rendered markup, just build TOC and photos
      if (blogContainer.children.length > 0) {
        injectEditorialPhotos();
        buildTableOfContents();
        syncStatusEl.innerHTML = '<span>📜</span> Loaded from Local Master Copy';
      }
    }
  }

  // Raw text modal controls
  if (viewRawBtn && rawTextModal) {
    viewRawBtn.addEventListener('click', () => {
      rawTextModal.classList.add('active');
    });
    closeRawBtn.addEventListener('click', () => {
      rawTextModal.classList.remove('active');
    });
    rawTextModal.addEventListener('click', (e) => {
      if (e.target === rawTextModal) rawTextModal.classList.remove('active');
    });
  }

  // Archival Theme Sync with Gallery
  const savedTheme = localStorage.getItem('wildid_theme');
  const themeToggleBtn = document.getElementById('themeToggleBtn');
  if (savedTheme === 'light') {
    document.body.classList.add('archival-light-mode');
    if (themeToggleBtn) {
      themeToggleBtn.innerHTML = '<span>🌲</span> Forest Canopy Mode';
    }
  }

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      const isLight = document.body.classList.toggle('archival-light-mode');
      if (isLight) {
        themeToggleBtn.innerHTML = '<span>🌲</span> Forest Canopy Mode';
        localStorage.setItem('wildid_theme', 'light');
      } else {
        themeToggleBtn.innerHTML = '<span>📜</span> Archival Paper Mode';
        localStorage.setItem('wildid_theme', 'dark');
      }
    });
  }

  // Start load
  loadBlog();

})();
