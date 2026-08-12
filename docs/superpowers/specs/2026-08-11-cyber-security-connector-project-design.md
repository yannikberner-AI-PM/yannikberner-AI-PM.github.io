# Design: Cyber Security Connector als Portfolio-Projekt

**Datum:** 2026-08-11  
**Status:** Approved (Brainstorming)  
**Quelle:** Eigenes Research-Prototyp-Projekt `~/Projects/Cyber-Security-SaaS` (Workname intern: Lotse; im Portfolio nicht nennen)

## Ziel

Vierter Case Study in der bestehenden `#projects`-Sektion, parallel zu Career Intelligence, Stakeholder Intelligence und Predictive Mentoring. Zeigt eigenständige B2B/B2B2B-Plattformarbeit: Dual-Surface (Partner + KMU), Connector-Framework und Agentic Connections Engineer als Kern-Betriebsmodell, mit Automation und Push in Maßnahmenplan und optionales Ticketing.

## Entscheidungen (fest)

| Thema | Entscheidung |
|-------|--------------|
| Ansatz | Mirror-Case + Agenten-Kern (Ansatz 1): gleiches Case-Study-Muster; Agentic Connections als zentrales Signal; ein Dual-Surface-Satz in Overview/Approach |
| Titel | Cyber Security Connector |
| Workname | **Lotse komplett weglassen** in Text, Alt-Texten, Aria-Labels und Vorschaubild |
| Externer Link | Keiner (wie die anderen eigenen Projekte); keine Live-Demo |
| Framing | Eine Plattform, zwei Surfaces (Partner-Portal + KMU-Onboarding), ein Connector-Kern |
| Agentic Connections | Kern-Signal in Value, Approach und Contributions |
| Automation / Push | Explizit betonen (CRM-Übernahme, Multi-Source-Plan, Ticket-Push, Status-Sync) |
| Copy-Stil | Keine Gedankenstriche (em dashes). Keine Negationen. Kein Muster „nicht X, sondern Y“. |
| Reifegrad | Research-Prototyp mit lauffähigen Dual-Demos |
| Platzierung | Vierter Eintrag unter Predictive Mentoring |
| Section-Intro | Leicht verbreitern: KI-Praxis und eigene Produkt-/Plattform-Prototypen |
| Bild | Collage aus lokalen Demo-Screens (`.demo-shots`) |

## Struktur

- **Section:** `#projects` (Intro-Keys `projects.heading` / `projects.intro` anpassen)
- **Article ID:** `cyber-security-connector`
- **i18n-Prefix:** `projects.cyberSecurityConnector.*` (identische Keys in `de` und `en`)
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
| Title | Cyber Security Connector |
| Meta | B2B2B- und KMU-Surfaces, Connector-Marketplace, Agentic Connections |
| Value | Automatisierte Übergabe aus HR-/QM-Daten an Partner; Push in Maßnahmenplan und optionale Tickets |
| Overview | Eine Plattform: Partner übernimmt Kunden aus CRM; KMU/Partner verbindet Organigramm und QM; regelbasierter Maßnahmenplan mit Verantwortlichen und erkannten Prozessen; Push in Ticketing wo angebunden |
| Approach | Shared Connector-Framework (Kategorien org_hr, qm_process, ticketing, partner_crm); Multi-Source-Generator; Agentic Connections Engineer als Betriebsmodell für Connector-Arbeit in Cursor |
| Setup | Privates Research-Prototyp-Projekt (Next.js Monorepo) |
| Result | Lauffähiger Dual-Demo-Kern: Onboarding/Marketplace zu Plan zu Push/Sync; Partner-CRM-Import und Embed-Widget |
| Contributions | Ca. 5 Punkte: Dual-Surface; Connector-Interface und Marketplace; Multi-Source-Maßnahmenplan; Automation/Push (Tickets und Status-Sync); Agentic Connections Engineer |
| Details | Kontext / Ansatz / Wert / Next (z. B. weitere Connectoren, Live-Auth, Persistenz) |
| Tags | Next.js, TypeScript, Connector Framework, Agentic Connections, Multi-Source, B2B2B |

Finale Formulierung entsteht im Implementation Plan / bei der Umsetzung; dieses Dokument fixiert Framing, Stilregeln und Faktengrenze, nicht jeden Satz.

### Faktengrenze (aus Quellprojekt)

Belegbar für den Case:

- Zwei Demo-Apps: KMU-Onboarding/Dashboard und B2B2B Partner-Portal/Connect/Dashboard/Embed
- Connector-Kategorien und Interface im shared Package
- Implementierte Demo-Adapter: Personio (org_hr), QM-CSV (qm_process), Jira (ticketing, optional), HubSpot (partner_crm)
- Multi-Source-Maßnahmenplan aus Onboarding plus verbundenen org_hr-/qm_process-Daten
- Marketplace-UI mit Kategorie-Slots; weitere Vendoren als „Bald verfügbar“-Slots
- Agentic Connections Engineer als dokumentiertes Betriebsmodell (Docs + Skill im Quellrepo)
- Design-Tokens: institutionell-ruhig, Teal-Akzent, Source Serif / IBM Plex (nur falls bildlich relevant)

Nicht behaupten:

- Fertiges SaaS-Produkt oder Store-/Kundenrollout
- Live-OAuth/Produktion ohne Demo-Hinweis, wo nur Demo läuft
- PDF-Export (Roadmap, nicht implementiert)
- Öffentliche Demo-URL oder öffentliches Repo (Out of Scope für diesen Portfolio-Schritt)

## Vorschaubild

- **Pfad:** `assets/images/cyber-security-connector-case-study-collage.png`
- **Format:** 1600×900, analog zu den anderen Case-Collagen
- **Quellen:** `/Users/yannikberner/Projects/Cyber-Security-SaaS/.demo-shots/` (`kmu-demo.png`, `b2b2b-demo.png`, Mobile-Varianten; `roadmap-tree` optional)
- **Regel:** Kein „Lotse“-Logo oder -Titel im Bild

## Technische Umsetzung

1. `index.html`: vierten Project-`<article>` ergänzen; Section-Intro-Fallbacktexte anpassen
2. `script.js`: `projects.cyberSecurityConnector` in `translations.de` und `translations.en`; `projects.heading` / `projects.intro` verbreitern
3. Collage-Asset erzeugen und referenzieren
4. QA: `node scripts/check-i18n.js`, DE/EN, Details-Toggle, kein horizontaler Overflow
5. `CLAUDE.md`: Offene Punkte nach Stand der Umsetzung aktualisieren

## Out of Scope

- Live-Demo-URL oder öffentlicher Repo-Link im Portfolio
- Rename, Publish oder Deploy des Quellprojekts `Cyber-Security-SaaS`
- Änderungen an Career Intelligence, Stakeholder Intelligence, Predictive Mentoring (außer gemeinsamer Section-Intro)
- Produkt- oder Markenarbeit im Quellrepo selbst
- Neue CSS-/JS-Frameworks oder Build-Tools im Portfolio

## Erfolgskriterien

- Vierter Project-Case sichtbar und sprachumschaltbar
- Kein Vorkommen von „Lotse“ in Portfolio-Texten oder dem neuen Bildasset
- Neue Copy ohne Gedankenstriche, ohne Negationen und ohne „nicht X, sondern Y“
- Automation/Push und Agentic Connections als Kern-Signal erkennbar
- Optisch und strukturell konsistent mit den bestehenden eigenen Projekten
- `node scripts/check-i18n.js` grün
