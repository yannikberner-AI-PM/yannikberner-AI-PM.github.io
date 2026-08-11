# Cyber Security Connector Portfolio Case — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans (inline; user asked to implement). Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a fourth `#projects` case study “Cyber Security Connector” (no Lotse, no live demo link) with collage, DE/EN copy, and a broadened section intro.

**Architecture:** Mirror Predictive Mentoring case markup; extend `translations.de/en.projects.cyberSecurityConnector`; broaden `projects.heading`/`intro`; add one 1600×900 collage from `.demo-shots` with Lotse redacted.

**Tech Stack:** Static HTML/CSS/JS (no build tools); Pillow for collage.

## Global Constraints

- Never use the workname Lotse in HTML, JS copy, alt/aria text, or the image asset.
- No external repo/live-demo link.
- Identical i18n keys in `de` and `en`.
- Reuse `.case-study.project` patterns; no new CSS unless broken.
- Copy style: no em dashes; no negations; no “nicht X, sondern Y”. Emphasize automation and push. Agentic Connections is a core signal.
- Honesty: frame as research prototype with runnable dual demos.

## File map

| File | Responsibility |
|------|----------------|
| `index.html` | Section intro fallbacks; fourth project `<article id="cyber-security-connector">` after Predictive Mentoring |
| `script.js` | Broadened `projects.heading`/`intro`; `projects.cyberSecurityConnector` in `de` + `en` |
| `assets/images/cyber-security-connector-case-study-collage.png` | Preview image 1600×900, no Lotse |
| `docs/superpowers/plans/2026-08-11-cyber-security-connector-portfolio.md` | This plan |

---

### Task 1: Collage asset

**Files:**
- Create: `assets/images/cyber-security-connector-case-study-collage.png`
- Sources: `/Users/yannikberner/Projects/Cyber-Security-SaaS/.demo-shots/kmu-demo.png`, `b2b2b-demo.png` (mobile optional)

- [x] **Step 1:** Build 1600×900 PNG collage (KMU + Partner surfaces). Cover or crop any “Lotse” wordmark/body text so the asset contains no Lotse.
- [x] **Step 2:** Confirm dimensions 1600×900 (`sips` or Pillow). Visually verify no Lotse.

### Task 2: HTML case study + intro fallbacks

**Files:**
- Modify: `index.html`

- [x] **Step 1:** Update section heading/intro fallbacks to broadened wording.
- [x] **Step 2:** Insert mirror `<article class="case-study project reveal" id="cyber-security-connector">` after Predictive Mentoring with `data-i18n` keys under `projects.cyberSecurityConnector.*`.
- [x] **Step 3:** Image `src="assets/images/cyber-security-connector-case-study-collage.png"` width/height 1600/900.
- [x] **Step 4:** Five contribution `<li>` keys `.0`–`.4`; tags mix of hardcoded + i18n; details toggle `details-cyber-security-connector`.
- [x] **Step 5:** No external links.

### Task 3: i18n copy (de + en)

**Files:**
- Modify: `script.js`

Final DE copy (apply verbatim unless a hard conflict appears):

```js
heading: 'KI-Praxis und Produktprototypen vertiefen',
intro: 'Private Projekte, um KI-Nutzung und eigene Produkt- sowie Plattformprototypen mit echtem Mehrwert voranzubringen.',
cyberSecurityConnector: {
  eyebrow: 'Eigenes Projekt',
  title: 'Cyber Security Connector',
  meta: 'B2B2B- und KMU-Surfaces mit Connector-Marketplace und Agentic Connections.',
  valueLabel: 'Mehrwert: Automatisierte Übergabe aus HR- und QM-Daten, mit Push in Maßnahmenplan und Tickets',
  overview: 'Eine Plattform für zwei Surfaces. Im Partner-Portal übernimmt der Berater Kunden aus dem CRM. Im KMU- und Partner-Flow verbinden Organigramm- und QM-Connectoren die Datenquellen. Daraus entsteht ein regelbasierter Maßnahmenplan mit Verantwortlichen und erkannten Prozessen. Angebundene Ticketing-Systeme erhalten die Maßnahmen per Push, der Status kommt per Sync zurück.',
  approachTitle: 'Von Connectoren zu automatisiertem Push',
  approachText: 'Shared Connector-Framework mit den Kategorien Organigramm/HR, QM/Prozess, Ticketing und Partner-CRM. Der Multi-Source-Generator baut den Maßnahmenplan aus Onboarding und verbundenen Quellen. Agentic Connections Engineer ist das Betriebsmodell: Cursor übernimmt die Connector-Entwicklung entlang API-Docs und Skills.',
  periodLocation: 'Privates Research-Prototyp-Projekt (Next.js Monorepo)',
  imageAlt: 'Collage der Cyber-Security-Connector-Demos: KMU-Onboarding und Partner-Portal mit Connector-Flächen',
  mediaAriaLabel: 'Collage der Cyber-Security-Connector-Demos: KMU-Onboarding und Partner-Portal mit Connector-Flächen',
  result: 'Ergebnis: Lauffähiger Dual-Demo-Kern von Onboarding und Marketplace über Maßnahmenplan bis Push und Status-Sync, inklusive Partner-CRM-Import und Embed-Widget.',
  contributions: [
    'Zwei Surfaces auf einem Connector-Kern: Partner-Portal mit CRM-Kundenübernahme und KMU-Onboarding mit Marketplace.',
    'Connector-Interface und Marketplace für Organigramm/HR, QM/Prozess, Ticketing und Partner-CRM.',
    'Multi-Source-Maßnahmenplan: Onboarding plus verbundene HR- und QM-Daten liefern Verantwortliche und erkannte Prozesse.',
    'Automation und Push: Maßnahmen als Tickets ausspielen und Status per Sync zurückspiegeln.',
    'Agentic Connections Engineer als Betriebsmodell: Connector-Arbeit in Cursor mit API-Docs und Skills.'
  ],
  tags: ['Next.js', 'TypeScript', 'Connector Framework', 'Agentic Connections', 'Multi-Source', 'B2B2B'],
  details: {
    context: 'NIS2 und ISO 27001 erzeugen Beratungsbedarf. KMUs liefern HR- und QM-Kontext über Connectoren; Partner steuern Expertise und Maßnahmenplan. Die Plattform automatisiert Übergabe, Plananreicherung und Push in die Arbeitswerkzeuge.',
    approach: 'Was: Connector-Plattform für Partner und KMU. Warum: strukturierte Übergabe und automatisierter Push beschleunigen Beratung. Wie: Shared Framework, Multi-Source-Generator und Agentic Connections für Connector-Entwicklung.',
    value: 'Ein Research-Prototyp, der Dual-Surface, Automation und Agenten-Betriebsmodell in einem greifbaren Demo-Kern zeigt.',
    next: 'Weitere Connectoren im Marketplace schärfen, Live-Auth vertiefen und Persistenz über Demo-LocalStorage hinaus ausbauen.'
  }
}
```

Final EN copy:

```js
heading: 'Deepening AI practice and product prototypes',
intro: 'Personal projects to advance hands-on AI use and my own product and platform prototypes with real value.',
cyberSecurityConnector: {
  eyebrow: 'Personal Project',
  title: 'Cyber Security Connector',
  meta: 'B2B2B and SME surfaces with a connector marketplace and Agentic Connections.',
  valueLabel: 'Value: Automated handoff from HR and QM data, with push into the measure plan and tickets',
  overview: 'One platform with two surfaces. In the partner portal, the consultant pulls customers from CRM. In the SME and partner flow, org-chart and QM connectors attach the data sources. That yields a rule-based measure plan with owners and recognised processes. Connected ticketing tools receive measures via push; status returns via sync.',
  approachTitle: 'From connectors to automated push',
  approachText: 'A shared connector framework with org/HR, QM/process, ticketing and partner-CRM categories. The multi-source generator builds the measure plan from onboarding and connected sources. Agentic Connections Engineer is the operating model: Cursor owns connector development along API docs and skills.',
  periodLocation: 'Personal research prototype project (Next.js monorepo)',
  imageAlt: 'Collage of the Cyber Security Connector demos: SME onboarding and partner portal with connector surfaces',
  mediaAriaLabel: 'Collage of the Cyber Security Connector demos: SME onboarding and partner portal with connector surfaces',
  result: 'Outcome: A runnable dual-demo core from onboarding and marketplace through measure plan to push and status sync, including partner CRM import and an embed widget.',
  contributions: [
    'Two surfaces on one connector core: partner portal with CRM customer intake and SME onboarding with a marketplace.',
    'Connector interface and marketplace for org/HR, QM/process, ticketing and partner CRM.',
    'Multi-source measure plan: onboarding plus connected HR and QM data supply owners and recognised processes.',
    'Automation and push: ship measures as tickets and mirror status back via sync.',
    'Agentic Connections Engineer as operating model: connector work in Cursor with API docs and skills.'
  ],
  tags: ['Next.js', 'TypeScript', 'Connector Framework', 'Agentic Connections', 'Multi-Source', 'B2B2B'],
  details: {
    context: 'NIS2 and ISO 27001 drive advisory demand. SMEs supply HR and QM context through connectors; partners steer expertise and the measure plan. The platform automates handoff, plan enrichment and push into work tools.',
    approach: 'What: a connector platform for partners and SMEs. Why: structured handoff and automated push speed up advisory work. How: shared framework, multi-source generator and Agentic Connections for connector development.',
    value: 'A research prototype that makes dual-surface design, automation and an agent operating model tangible in one demo core.',
    next: 'Sharpen further marketplace connectors, deepen live auth and extend persistence beyond demo localStorage.'
  }
}
```

- [x] **Step 1:** Update `translations.de.projects.heading`/`intro` and add `cyberSecurityConnector`.
- [x] **Step 2:** Matching EN keys.
- [x] **Step 3:** `node scripts/check-i18n.js`

### Task 4: Local preview + QA

- [x] **Step 1:** Grep `index.html`, `script.js`, and confirm collage path for `Lotse` / `—` / forbidden negation patterns in the new copy block.
- [x] **Step 2:** `python3 -m http.server 4173` and open `#cyber-security-connector` in DE/EN if feasible.
- [ ] **Step 3:** Commit only when user asks (default: leave ready on branch).
