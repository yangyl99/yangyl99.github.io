# GBH Spectroscopy Results Implementation Plan

> **For Codex:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add selected-nuclide excitation spectra and `GBH.out` download links to the existing static nuclear map site.

**Architecture:** Keep the existing static site flow: selecting a nuclide updates the current detail panel. Move the existing `GBH_results` tree under `main/`, generate a static JS manifest from actual files, and have `search.js` render spectroscopy assets when a selected nuclide exists in the manifest.

**Tech Stack:** Static HTML, Bootstrap, plain JavaScript, generated manifest file.

---

### Task 1: Place Data Under the Static Site

**Files:**
- Move: `GBH_results/` to `main/GBH_results/`

**Steps:**
1. Move the directory without changing its internal naming.
2. Confirm image and `GBH.out` counts remain matched.

### Task 2: Generate Manifest

**Files:**
- Create: `main/js/gbh_results_manifest.js`

**Steps:**
1. Scan `main/GBH_results/**/**/*_excitation_bands.png`.
2. Build `window.GBH_RESULTS` entries keyed by canonical nuclide name such as `O16` and `Hf164`.
3. Store actual image and `GBH.out` relative paths so legacy names like `_O_iso/_O16` work.

### Task 3: Render Spectroscopy Result

**Files:**
- Modify: `main/index.html`
- Modify: `main/js/search.js`

**Steps:**
1. Add a spectroscopy result section to the existing detail view.
2. Load the manifest before `search.js`.
3. Add helper functions to clear and update spectroscopy content on every valid nuclide selection.
4. Reuse the existing selection path from map clicks, search, and neighbor arrows.

### Task 4: Verify

**Commands:**
- `find main/GBH_results -mindepth 3 -maxdepth 3 -type f -name '*_excitation_bands.png' | wc -l`
- `find main/GBH_results -mindepth 3 -maxdepth 3 -type f -name 'GBH.out' | wc -l`
- `python3 -m http.server 8765 -d main`

**Checks:**
- `O16` shows the `_O16` excitation image and `GBH.out` link.
- `Hf164` shows the regular `Hf164` excitation image and `GBH.out` link.
- A valid nuclide without GBH data shows an unavailable message.
