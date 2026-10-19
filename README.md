# WildID — The Identity Atlas & Technical Research Dispatch
### AI-Powered Individual Wildlife Re-Identification | Image Gallery & Blog

> **“The Forest Has a Memory. We Are Learning to Read It.”**

An authentic, forensic photographic gallery, scientific editorial atlas, and 24-hour hackathon research dispatch created for **WildID** during the **WILDHACK 2K26** sprint (October 16–17, 2026) in collaboration with **Tadoba-Andhari Tiger Reserve (TATR)**.

---

## 🌲 Static Architecture (Zero Node.js / Zero Python Flask Required)

This is a **100% pure client-side static application**. It runs natively in any modern browser without servers, build tools, package managers, or backend dependencies:

- **Direct Browser Opening**: Double-click [`index.html`](file:///d:/WILDHACKS/SORTED/WILDHACKS_HACKOPS_IMAGE_GALLERY/index.html) or [`blog.html`](file:///d:/WILDHACKS/SORTED/WILDHACKS_HACKOPS_IMAGE_GALLERY/blog.html) to open directly in Chrome, Edge, Safari, or Firefox.
- **Static Hosting Ready**: Deployable immediately to GitHub Pages, Netlify, Cloudflare Pages, AWS S3, or any static web server.

---

## 🔄 Dynamic Content & Image Synchronization

The site is built to be **dynamic** when images are added/removed or when `blog.txt` is updated:

### 1. Dynamic Blog (`blog.txt`)
- The blog page (`blog.html`) uses client-side dynamic fetching (`js/blog.js`) to load and parse [`blog.txt`](file:///d:/WILDHACKS/SORTED/WILDHACKS_HACKOPS_IMAGE_GALLERY/blog.txt) on the fly.
- Editing [`blog.txt`](file:///d:/WILDHACKS/SORTED/WILDHACKS_HACKOPS_IMAGE_GALLERY/blog.txt) immediately alters the website when refreshed!
- Contains an interactive Table of Contents tracking reading progress, estimated read time, and contextual photography.

### 2. Adding / Removing Images (`images/`)
- **Option A (One-Click Sync)**: Double-click [`update.bat`](file:///d:/WILDHACKS/SORTED/WILDHACKS_HACKOPS_IMAGE_GALLERY/update.bat) (or run `python sync.py`).
  - Scans `images/` in ~0.08s.
  - Automatically generates missing thumbnails in `thumbs/`.
  - Removes deleted images and adds new ones to `gallery_data.js` and `gallery_data.json`.
  - Re-syncs `blog.html` with `blog.txt`.
- **Option B (Real-Time Watcher)**: Run `python watch.py`.
  - Monitors `images/` and `blog.txt` in real time, auto-updating whenever any file is added or deleted.
- **Option C (Live In-Browser Ingestion)**: In `index.html`, click the `[+] Ingest Images` button to dynamically load new observation images directly into the active browser session.

---

## 📁 Directory Structure

```text
WILDHACKS_HACKOPS_IMAGE_GALLERY/
├── index.html              # The Identity Atlas Master Image Gallery
├── blog.html               # WILDHACK 2K26 Technical Research Dispatch (Blog)
├── blog.txt                # Exact source markdown text for the blog
├── sync.py                 # Fast 0.08s synchronization script
├── update.bat              # One-click Windows batch runner for sync.py
├── watch.py                # Live background file watcher
├── generate_blog.py        # Static blog generator & parser
├── gallery_data.json       # Structured JSON manifest of all 130 documented assets
├── README.md               # Technical documentation
├── css/
│   ├── style.css           # Vanilla CSS design system (Field Canopy, Tiger Ochre, Archival Ivory)
│   └── blog.css            # Specialized article & research publication typography
├── js/
│   ├── gallery_data.js     # Client-side JavaScript dataset containing 130 records
│   ├── app.js              # Gallery engine (Search, Filters, Lightbox, Workbench, Soundscape)
│   └── blog.js             # Dynamic blog engine (TOC scrollspy, blog.txt live loader)
├── images/                 # All 130 original full-resolution master image files
└── thumbs/                 # 130 lightweight thumbnails for instant 60fps rendering
```

---

## 🎨 Master Visual Art Direction

- **Palette**: Field Canopy (`#142820`), Tiger Ochre (`#D5A54A`), Carbon Black (`#111513`), Archival Ivory (`#F2EFE6`), Research Navy (`#243746`), Field Slate (`#65736D`).
- **Typography**: `Cinzel` & `Cormorant Garamond` (editorial display), `Plus Jakarta Sans` (body), `JetBrains Mono` (technical annotations).
- **Identity Progression**: Landscape → Individual → Evidence → Interpretation → HackOps Lab.
- **Interactive Workbench**: Side-by-side biometric comparator verifying stripe correspondence and similarity across candidate pairs.
