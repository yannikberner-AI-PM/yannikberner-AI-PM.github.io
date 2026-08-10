# Predictive Mentoring Portfolio Case — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans (inline; user asked to ship for local preview). Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a third `#projects` case study “Predictive Mentoring” (no AUGUVIO, no public link) so it is visible on the local portfolio page.

**Architecture:** Mirror Career/Stakeholder Intelligence case markup; extend `translations.de/en.projects.predictiveMentoring`; add one 1600×900 collage asset.

**Tech Stack:** Static HTML/CSS/JS (no build tools); Pillow for collage.

## Global Constraints

- Never use the product name AUGUVIO in HTML, JS copy, alt/aria text, or the image asset.
- No external repo/store link.
- Identical i18n keys in `de` and `en`.
- Reuse `.case-study.project` patterns; no new CSS unless broken.
- Honesty: frame as prototype, not shipped store product.

## File map

| File | Responsibility |
|------|----------------|
| `index.html` | Third project `<article id="predictive-mentoring">` after Stakeholder Intelligence |
| `script.js` | `projects.predictiveMentoring` in `de` + `en` |
| `assets/images/predictive-mentoring-case-study-collage.png` | Preview image 1600×900, no brand name |

---

### Task 1: Collage asset

**Files:**
- Create: `assets/images/predictive-mentoring-case-study-collage.png`

- [ ] **Step 1:** Build 1600×900 PNG from the Quick-Log screenshot (no AUGUVIO) centered on a neutral canvas.
- [ ] **Step 2:** Confirm dimensions 1600×900 and no AUGUVIO in source.

### Task 2: HTML case study

**Files:**
- Modify: `index.html` (insert article before closing `</div>` of projects section)

- [ ] **Step 1:** Insert mirror `<article class="case-study project reveal" id="predictive-mentoring">` after Stakeholder Intelligence with `data-i18n` keys under `projects.predictiveMentoring.*`.
- [ ] **Step 2:** Image `src="assets/images/predictive-mentoring-case-study-collage.png"` width/height 1600/900.
- [ ] **Step 3:** Tags: React Native, Expo, TypeScript, SQLite + i18n for Prediction Engine / LLM Layer / Coaching UX.
- [ ] **Step 4:** No external links.

### Task 3: i18n copy (de + en)

**Files:**
- Modify: `script.js` — after `stakeholderIntelligence` blocks in both languages

- [ ] **Step 1:** Add full `predictiveMentoring` object in `translations.de.projects`.
- [ ] **Step 2:** Add matching keys in `translations.en.projects`.
- [ ] **Step 3:** `node --check script.js`

### Task 4: Local preview + QA

- [ ] **Step 1:** `python3 -m http.server 4173` in portfolio root.
- [ ] **Step 2:** Open `http://localhost:4173/#projects` (and `?lang=en`).
- [ ] **Step 3:** Grep portfolio for `AUGUVIO` — expect zero matches outside docs/specs if any; zero in `index.html`/`script.js`/new PNG path references.
- [ ] **Step 4:** Do **not** commit/push unless user asks (local preview first).
