import html, re, os

base_dir = os.path.dirname(os.path.abspath(__file__))
blog_txt_path = os.path.join(base_dir, 'blog.txt')
blog_html_path = os.path.join(base_dir, 'blog.html')

with open(blog_txt_path, 'r', encoding='utf-8') as f:
    raw_md = f.read()

def parse_md(md):
    lines = md.split('\n')
    out = []
    in_list = False
    in_table = False
    table_rows = []
    sec_count = 0

    def format_inline(t):
        t = html.escape(t)
        t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
        t = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', t)
        t = re.sub(r'`([^`]+)`', r'<code class="inline-code">\1</code>', t)
        t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank" rel="noopener noreferrer" class="blog-link">\1 ↗</a>', t)
        return t

    def flush_list():
        nonlocal in_list
        if in_list:
            out.append('</ul>')
            in_list = False

    def flush_table():
        nonlocal in_table, table_rows
        if in_table and table_rows:
            t_html = ['<div class="table-container"><table class="blog-data-table">', '<thead><tr>']
            for h in table_rows[0]:
                t_html.append(f'<th>{format_inline(h.strip())}</th>')
            t_html.append('</tr></thead><tbody>')
            for row in table_rows[1:]:
                t_html.append('<tr>')
                for c in row:
                    t_html.append(f'<td>{format_inline(c.strip())}</td>')
                t_html.append('</tr>')
            t_html.append('</tbody></table></div>')
            out.append('\n'.join(t_html))
            in_table = False
            table_rows = []

    for line in lines:
        tr = line.strip()
        if tr.startswith('|') and tr.endsWith('|') if hasattr(tr, 'endsWith') else tr.endswith('|'):
            flush_list()
            if re.match(r'^\|[-|\s]+\|$', tr):
                continue
            in_table = True
            cols = [c for c in tr[1:-1].split('|')]
            table_rows.append(cols)
            continue
        elif in_table:
            flush_table()

        if tr.startswith('- '):
            if not in_list:
                in_list = True
                out.append('<ul class="blog-bullet-list">')
            out.append(f'<li>{format_inline(tr[2:])}</li>')
            continue
        elif in_list:
            flush_list()

        if not tr:
            continue

        if tr.startswith('# '):
            out.append(f'<h1 class="blog-main-title">{format_inline(tr[2:])}</h1>')
            continue

        if tr.startswith('## '):
            sec_count += 1
            sec_id = f'section-{sec_count}'
            out.append(f'<h2 id="{sec_id}" class="blog-section-title"><span class="section-num">{sec_count:02d}</span> {format_inline(tr[3:])}</h2>')
            continue

        if tr.startswith('### '):
            out.append(f'<h3 class="blog-sub-title">{format_inline(tr[4:])}</h3>')
            continue

        if tr.startswith('> '):
            out.append(f'<blockquote class="blog-blockquote"><p>{format_inline(tr[2:])}</p></blockquote>')
            continue

        if tr == '---':
            out.append('<hr class="blog-divider">')
            continue

        if tr.startswith('By Hanshal Bobate'):
            out.append('''<div class="blog-byline-banner">
              <div class="byline-avatar">HB</div>
              <div class="byline-details">
                <span class="byline-author">Hanshal Bobate</span>
                <span class="byline-meta">Team HackOPs · October 16–17, 2026 · WILDHACK 2K26</span>
              </div>
              <div class="byline-tag">SPECIAL MENTION AWARD</div>
            </div>''')
            continue

        out.append(f'<p class="blog-p">{format_inline(tr)}</p>')

    flush_list()
    flush_table()
    return '\n'.join(out)

parsed_body = parse_md(raw_md)

html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>WildID at WILDHACK 2K26: Building AI for Wildlife Conservation in 24 Hours</title>
  <meta name="description" content="The complete engineering and field story of WildID: a simulation-driven AI system for individual wildlife re-identification built at WILDHACK 2K26 in collaboration with Tadoba-Andhari Tiger Reserve.">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' fill='%23142820'/><path d='M8 6 C12 12, 6 18, 12 26 M16 4 C20 12, 14 20, 18 28 M24 8 C22 14, 26 20, 22 26' stroke='%23D5A54A' stroke-width='2.5' fill='none' stroke-linecap='round'/></svg>">
  <link rel="stylesheet" href="css/style.css">
  <link rel="stylesheet" href="css/blog.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
</head>
<body class="blog-body">

  <!-- Top Reading Progress Indicator -->
  <div id="readingProgressBar" class="reading-progress-bar" aria-hidden="true"></div>

  <div class="app-container">

    <!-- Top Telemetry & Navigation Bar -->
    <header class="telemetry-bar" role="banner">
      <div class="telemetry-left">
        <a href="index.html" class="nav-back-link" title="Return to Our Experience at WILDHACK 2K26 field story">
          ← <strong>OUR EXPERIENCE AT WILDHACK 2K26</strong> [FIELD STORY]
        </a>
        <span class="telemetry-tag">// COMPLETE RESEARCH DISPATCH</span>
        <span>WILDHACK 2K26 PROCEEDINGS</span>
      </div>
      <div class="telemetry-right">
        <span id="blogSyncStatus" class="sync-status-indicator">
          <span class="status-pulse-green"></span> Dynamically Synced with <code>blog.txt</code>
        </span>
        <button id="viewRawBtn" class="util-btn" title="View raw unformatted blog.txt source">
          <span>📄</span> Raw Source
        </button>
        <button id="themeToggleBtn" class="util-btn" title="Toggle Archival Paper Publication theme">
          <span id="themeIcon">📜</span> Archival Paper Mode
        </button>
      </div>
    </header>

    <!-- Main Editorial Article Layout -->
    <div class="blog-layout-grid">

      <!-- Left Sticky Sidebar: Table of Contents & Article Metadata -->
      <aside class="blog-sidebar">
        <div class="sidebar-sticky-wrapper">
          
          <div class="sidebar-meta-card">
            <div class="meta-card-label">ARCHIVAL RESEARCH DOSSIER</div>
            <h2 class="meta-card-title">WildID Technical Dispatch</h2>
            <div class="meta-card-item">
              <span class="meta-k">Author</span>
              <span class="meta-v">Hanshal Bobate</span>
            </div>
            <div class="meta-card-item">
              <span class="meta-k">Team</span>
              <span class="meta-v">HackOPs (4 Members)</span>
            </div>
            <div class="meta-card-item">
              <span class="meta-k">Event</span>
              <span class="meta-v">WILDHACK 2K26 (16–17 Oct)</span>
            </div>
            <div class="meta-card-item">
              <span class="meta-k">Reserve Partner</span>
              <span class="meta-v">Tadoba-Andhari (TATR)</span>
            </div>
            <div class="meta-card-item">
              <span class="meta-k">Recognition</span>
              <span class="meta-v" style="color: var(--color-ochre);">Special Mention</span>
            </div>
            <div class="meta-card-item">
              <span class="meta-k">Estimated Read</span>
              <span class="meta-v">18 Minutes</span>
            </div>
          </div>

          <!-- Interactive Table of Contents -->
          <nav class="blog-toc-card" aria-label="Article Table of Contents">
            <div class="toc-header">
              <span>TABLE OF CONTENTS</span>
              <span class="toc-count">18 SECTIONS</span>
            </div>
            <ul id="tocList" class="toc-list">
              <!-- Dynamically populated / updated by blog.js -->
            </ul>
          </nav>

          <a href="index.html" class="btn-primary-ochre" style="display: block; text-align: center; text-decoration: none;">
            Explore The 130 Specimen Plates ↗
          </a>

        </div>
      </aside>

      <!-- Right Column: Full Dynamic Article Body -->
      <main class="blog-content-area" role="main">
        <article id="blogArticleContent" class="blog-article-body">
{parsed_body}
        </article>
      </main>

    </div>

    <!-- Raw Source Modal -->
    <div id="rawTextModal" class="modal-overlay" role="dialog" aria-modal="true" aria-label="Raw blog.txt content">
      <div class="inspection-docket-window" style="grid-template-columns: 1fr; max-width: 960px; height: 80vh;">
        <div class="modal-viewport" style="background: var(--bg-card); padding: 1.5rem; overflow-y: auto;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; border-bottom: 1px solid var(--border-subtle); padding-bottom: 0.75rem;">
            <div>
              <strong style="color: var(--color-ochre); font-family: var(--font-mono);">SOURCE FILE: blog.txt</strong>
              <div style="font-size: 0.72rem; color: var(--text-muted);">Exact local text file loaded dynamically</div>
            </div>
            <button id="closeRawBtn" class="modal-close-btn">✕</button>
          </div>
          <pre id="rawTextContent" style="font-family: var(--font-mono); font-size: 0.8rem; line-height: 1.6; color: var(--text-body); white-space: pre-wrap; word-break: break-word;">{html.escape(raw_md)}</pre>
        </div>
      </div>
    </div>

    <!-- Site Footer -->
    <footer class="site-footer" role="contentinfo">
      <div>
        <p class="footer-quote">“The Forest Has a Memory. We Are Learning to Read It.”</p>
        <p class="footer-credits">
          <strong>WildID</strong> — AI-Powered Individual Wildlife Re-Identification Initiative.<br>
          Published by <strong>Team HackOPs</strong> (Hanshal Bobate, Vaishnav Balpande, Lokesh Parate, Soham Bagmare).<br>
          In collaboration with <strong>Tadoba-Andhari Tiger Reserve (TATR)</strong>.
        </p>
      </div>
      <div style="text-align: right;">
        <p><a href="index.html" style="color: var(--color-ochre); text-decoration: none;">← Return to The Identity Atlas Image Gallery</a></p>
        <p style="margin-top: 0.35rem; color: var(--text-muted);">100% Client-Side Static Architecture · Dynamic Sync Enabled</p>
      </div>
    </footer>

  </div>

  <!-- Dynamic Blog Engine -->
  <script src="js/blog.js"></script>

</body>
</html>
'''

with open(blog_html_path, 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f'Successfully created {blog_html_path}')
