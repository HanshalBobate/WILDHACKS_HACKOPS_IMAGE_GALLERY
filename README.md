# Our Experience at WILDHACK 2K26
### A 24-Hour Journey Where Wildlife, Computer Vision, and an Idea Finally Came Together
**By Team HackOPs (Hanshal Bobate · Vaishnav Balpande · Lokesh Parate · Soham Bagmare)**  
*Organized in collaboration with Tadoba-Andhari Tiger Reserve (TATR) & Ballarpur Institute of Technology*

> **“The Forest Has a Memory. We Are Learning to Read It.”**

A first-person editorial digital story documenting Team HackOPs' experience at WILDHACK 2K26 — an offline 24-hour hackathon where we attempted to build **WildID**, an AI-powered individual wildlife re-identification system.

**Live Website on GitHub Pages:**  
👉 [https://hanshalbobate.github.io/WILDHACKS_HACKOPS_IMAGE_GALLERY/](https://hanshalbobate.github.io/WILDHACKS_HACKOPS_IMAGE_GALLERY/)

---

## 📖 The 11 Narrative Chapters

1. **Chapter 01: The Opening** — *“Our Experience at WILDHACK 2K26”*  
   24 hours. One conservation challenge. An idea we had been waiting to build.
2. **Chapter 02: Why We Showed Up** — *“Some ideas stay with you until you finally do something about them.”*  
   The intersection of computer science, wildlife photography, and the question: *If not me, then who?*
3. **Chapter 03: The Place, The People, The Opportunity** — *“First offline hackathon. Twenty-four hours. A problem that mattered to us.”*  
   Arrival at Ballarpur Institute of Technology, top 30 shortlisted teams from across India, and introducing Team HackOPs.
4. **Chapter 04: The Challenge** — *“What if recognising a tiger was only the beginning?”*  
   Moving beyond detection to re-identifying individual animals across viewpoints, illumination, distance, and non-rigid posture deformations.
5. **Chapter 05: The Build** — *“We didn't want to stop at an idea or a presentation.”*  
   The 5-stage vision pipeline and Blender + Python (`bpy`) + GroveScape synthetic data simulation (~10,000 images rendered locally).
6. **Chapter 06: Twenty-Four Hours** — *“Building is one thing. Making everything work together is another.”*  
   The authentic midnight sprint: fighting memory leaks, pruning code, and pushing through exhaustion at 2:58 AM.
7. **Chapter 07: Showing What We Built** — *“From a working prototype to a conversation about real-world use.”*  
   Live demonstration to the judges at 2:03 PM: territorial roaming maps, ecological correlation, and conversational RAG queries.
8. **Chapter 08: The Feedback That Mattered** — *“The most useful feedback was about what we hadn't solved yet.”*  
   Judges' critical insight: synthetic data is great for prototyping, but real-world conservation demands training and validation on genuine, messy camera-trap photographs.
9. **Chapter 09: A Special Mention** — *“Not the finish line. A reason to keep going.”*  
   Honored with a Special Mention among the 30 national teams; meeting dignitaries and conservation directors.
10. **Chapter 10: What Comes After the Hackathon?** — *“The 24 hours ended. The problem didn't.”*  
    Our roadmap: authentic camera-trap datasets, bulk ingestion pipelines, GNN stripe embeddings, and field collaboration aspirations with Pench & Tadoba.
11. **Chapter 11: The Closing** — *“We came to build a project. We left with a clearer direction.”*  
    Reflections on bringing computer science and wildlife together, learning from critical feedback, and continuing on a problem that matters.

---

## 🐅 Companion Interactive Features

- **125-Observation Specimen Atlas**: Collapsible drawer featuring the complete 125-image archive with multi-channel biometric filters, live search, and tabular registers.
- **Deep Forensic Lightbox**: Full-resolution pixel zoom (up to 400%), pan & drag, and cartographic HUD coordinate grid overlays.
- **Dual Re-ID Workbench**: Side-by-side biometric comparison verifying stripe correspondence, flank bifurcation topology, and similarity scores.
- **Synthesized Ambient Soundscape**: Subtle Web Audio forest soundscape (dry leaves and distant crickets).
- **Archival Dual Themes**: Default Forest Canopy Dark (`#142820` / `#111513`) and Archival Paper Light (`#F2EFE6` / `#FAF9F5`).
- **Research Dispatch (`blog.html`)**: Complete 731-line technical paper dynamically synchronized with `blog.txt`.

---

## 🌲 Static Architecture (Zero Node.js / Zero Python Flask Required)

This is a **100% pure client-side static web application**. It runs natively in any modern browser without servers, package managers, or backend runtimes.

- **Direct Browser Opening**: Double-click [`index.html`](file:///d:/WILDHACKS/SORTED/WILDHACKS_HACKOPS_IMAGE_GALLERY/index.html) or [`blog.html`](file:///d:/WILDHACKS/SORTED/WILDHACKS_HACKOPS_IMAGE_GALLERY/blog.html).
- **GitHub Pages Deployed**: Fully optimized and published directly to GitHub Pages.

---

## 📁 Repository Structure

```text
WILDHACKS_HACKOPS_IMAGE_GALLERY/
├── index.html              # "Our Experience at WILDHACK 2K26" Editorial Narrative + Atlas
├── blog.html               # 731-line Technical Research Dispatch (Blog)
├── blog.txt                # Exact source markdown text written by Hanshal Bobate
├── sync.py                 # Fast 0.08s asset & thumbnail synchronization script
├── update.bat              # One-click Windows batch runner for sync.py
├── watch.py                # Live background file watcher
├── generate_blog.py        # Static blog generator & parser
├── gallery_data.json       # Structured JSON manifest of all 125 documented assets
├── README.md               # Documentation
├── css/
│   ├── style.css           # Core visual design tokens & gallery/workbench styles
│   ├── editorial.css       # Long-form editorial storytelling layout & typography
│   └── blog.css            # Specialized research dispatch publication styles
├── js/
│   ├── gallery_data.js     # Client-side JavaScript manifest of all 125 observations
│   ├── app.js              # Story progress spy, soundscape, lightbox, & workbench engine
│   └── blog.js             # Dynamic blog engine (TOC scrollspy, blog.txt live loader)
├── images/                 # Master high-resolution photographic evidence
└── thumbs/                 # Web-optimized thumbnails for instant 60fps rendering
```

---

## 👥 Team HackOPs Credits

- **Hanshal Bobate** — Lead & Computer Vision Architecture
- **Vaishnav Balpande** — Systems & Simulation Engineering
- **Lokesh Parate** — Integration & Spatial Telemetry
- **Soham Bagmare** — Pipeline Engineering & Interface

*Presented at WILDHACK 2K26, Ballarpur Institute of Technology, Bamni, Chandrapur (16–17 October 2026).*
