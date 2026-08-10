# Stakeholder Intelligence Comms-Rhythm Copy Implementation Plan

> **For agentic workers:** Execute inline (single copy pass). Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reframe Stakeholder Intelligence portfolio copy around communication rhythm while keeping circle + matrix.

**Architecture:** Text-only change in existing i18n objects and HTML fallbacks; no UI or asset changes.

**Tech Stack:** Static HTML + `script.js` translations; `node scripts/check-i18n.js`.

## Global Constraints

- Keep circle (Core/Direct/Indirect) + 2×2 matrix as visible product core
- Job value = communication rhythm / follow-ups (whom, when, how)
- No Next/roadmap, no GDPR/profiling/“no personal data” claims
- DE/EN parallel; HTML fallbacks match DE

---

### Task 1: Rewrite DE + EN stakeholderIntelligence strings

**Files:** `script.js`, `index.html`

- [x] Update `meta`, `valueLabel`, `overview`, `approachTitle`, `approachText`, `result`, `contributions.2`, `details.*` in `translations.de` and `translations.en`
- [x] Mirror DE strings as HTML fallbacks in `index.html`
- [x] Run `node scripts/check-i18n.js`
- [x] Mark spec status approved/implemented; update `CLAUDE.md` open point
