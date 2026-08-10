# Design: Predictive Mentoring als Portfolio-Projekt

**Datum:** 2026-08-10  
**Status:** Approved (Brainstorming)  
**Quelle:** Eigenes Prototyp-Projekt `~/Projects/predictive-app` (öffentliches Repo existiert, wird hier nicht verlinkt)

## Ziel

Dritter Case Study in der bestehenden `#projects`-Sektion, parallel zu Career Intelligence und Stakeholder Intelligence. Zeigt eigenständige Consumer-/Mobile-Produktarbeit: Ziel-Wahrscheinlichkeit und Mentoring/Coaching gleichgewichtet — ohne Produktmarkennamen.

## Entscheidungen (fest)

| Thema | Entscheidung |
|-------|--------------|
| Ansatz | Mirror-Case (gleiches Case-Study-Muster wie die bestehenden eigenen Projekte) |
| Titel | Predictive Mentoring |
| Markenname | **AUGUVIO komplett weglassen** — Text, Alt-Texte, Aria-Labels und Vorschaubild |
| Externer Link | Keiner (wie Career/Stakeholder Intelligence) |
| Framing | Prediction-Loop und Mentoring gleichgewichtet („Predictive Mentoring“) |
| Reifegrad | Prototyp, kein fertiges Store-Produkt |
| Platzierung | Dritter Eintrag unter Stakeholder Intelligence |
| Bild | Collage aus App-/Design-Screens, ohne Markennamen |

## Struktur

- **Section:** `#projects` (Intro unverändert)
- **Article ID:** `predictive-mentoring`
- **i18n-Prefix:** `projects.predictiveMentoring.*` (identische Keys in `de` und `en`)
- **Markup-Blöcke** (Reihenfolge wie bestehende Project-Cases):
  1. Header (eyebrow, title, meta)
  2. Value label
  3. Overview
  4. Approach (label + title + text)
  5. Setup (`experience.common.setupLabel` + periodLocation)
  6. Result
  7. Contributions list + media shell
  8. Tags
  9. Details toggle (context, approach, value, next)

Keine neuen CSS-Klassen, sofern `.case-study.project` und bestehende Utilities greifen.

## Inhaltsrahmen (Copy-Richtung)

| Feld | Richtung |
|------|----------|
| Title | Predictive Mentoring |
| Meta | Mobile App: Ziel-Wahrscheinlichkeit + positives Coaching |
| Value | Eigenständiges Consumer-Produkt end-to-end: von Vision/Onboarding bis Prediction-Loop und Mentoring-Impulsen |
| Overview | Habit-/Ziel-Apps oft nur retrospektiv; diese App verbindet live nachvollziehbare Erreichungs-Wahrscheinlichkeit mit positiv gerahmten Gegenvorschlägen und Mentoring (Vision → Teilziele, Coaching-Chat). |
| Approach | React Native (Expo); Verhaltensdaten lokal (SQLite); Auth/Push leichtgewichtig; Prediction klassisch (nicht LLM); LLM nur für Formulierung/Coaching hinter austauschbarer Schicht. |
| Setup | Privates Prototyp-Projekt (iOS/Android) |
| Result | Funktionsfähiger Kern-Loop im Prototyp: Ziele, Logging, Prediction-Framing, Onboarding inkl. Vision, Coaching-Einstieg — ohne Cloud-Zwang für Verhaltensdaten. |
| Contributions | Flexibles Ziel-Datenmodell; Prediction vs. LLM getrennt; Vision-Onboarding; lokales SQLite + Privacy-Baseline; Mentoring-Oberfläche (Chat/Impulse). Ca. 4–5 Punkte. |
| Details | Kontext / Ansatz / Wert / Next (z. B. Store-Validierung, Prediction-Genauigkeit, Coaching-Scope) |
| Tags | React Native, Expo, SQLite, Prediction Engine, LLM Layer, Coaching UX. Kein HealthKit/Health Connect-Tag, solange das Vorschaubild und der Case das nicht klar belegen. |

Finale Formulierung entsteht im Implementation Plan / bei der Umsetzung; dieses Dokument fixiert Framing und Faktengrenze, nicht jeden Satz.

## Vorschaubild

- **Pfad:** `assets/images/predictive-mentoring-case-study-collage.png`
- **Format:** 1600×900, analog zu den anderen Case-Collagen
- **Quellen:** Design-Deck unter `predictive-app/designs/` sowie vorhandene Screenshots (u. a. Quick-Log ohne Markennamen)
- **Regel:** Kein AUGUVIO-Logo oder -Titel im Bild; bei sichtbarem Markentext crop/retouch oder anderen Screen wählen
- **Hinweis:** Aktuell nur ein klarer Phone-Screenshot im Quellrepo; Collage braucht ggf. zusätzliche Renders aus dem Design-Deck

## Technische Umsetzung

1. `index.html` — dritten Project-`<article>` ergänzen
2. `script.js` — `projects.predictiveMentoring` in `translations.de` und `translations.en`
3. Collage-Asset erzeugen und referenzieren
4. QA: `node --check script.js`, DE/EN, Details-Toggle, kein horizontaler Overflow

## Out of Scope

- Öffentlicher Repo-/Store-Link
- Änderung von Section-Intro, Nav oder Experience
- Änderungen an Career Intelligence / Stakeholder Intelligence
- Produkt-Rename in `predictive-app` selbst
- Neue CSS-/JS-Frameworks oder Build-Tools

## Erfolgskriterien

- Dritter Project-Case sichtbar und sprachumschaltbar
- Kein Vorkommen von „AUGUVIO“ in Portfolio-Texten oder dem neuen Bildasset
- Optisch und strukturell konsistent mit den beiden bestehenden eigenen Projekten
- `node --check script.js` grün
