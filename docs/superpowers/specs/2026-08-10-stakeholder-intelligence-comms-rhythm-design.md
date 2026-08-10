# Stakeholder Intelligence — Use-Case-Reframe: Kommunikations-Rhythmus

**Datum:** 2026-08-10  
**Status:** Umgesetzt (Copy-Pass)  
**Scope:** Nur Portfolio-Copy (DE/EN) für die Case Study Stakeholder Intelligence

## Ziel

Den sichtbaren Produktkern (Kreis-Modell + Matrix-Board) beibehalten und den **Job-Mehrwert** neu rahmen: bewusste **Kommunikations-Unterstützung** für Product Manager:innen mit vielen Stakeholdern — z. B. wen ich wann und wie wieder anspreche, wenn lange nicht gesprochen wurde oder ein Follow-up vor einer Entscheidung ansteht.

Zielgruppe der Story: der Autor und Personen in vergleichbarer Situation (Senior/Mid-Senior Product in komplexen B2B-/Hardware-Software-Kontexten).

## Nicht-Ziele

- Kein neues UI, keine Feature-Erweiterung, kein Screenshot-Wechsel
- Kein „Next“-/Roadmap-Absatz
- Keine DSGVO-, Profiling-, „echte Kolleg:innen“- oder „keine personenbezogenen Daten“-Claims
- Keine Änderung an Career Intelligence / Predictive Mentoring (außer bereits umgesetzte Entschärfungen)

## Positionierung (verbindlich)

| Aspekt | Inhalt |
|--------|--------|
| Kern | Kreis (Nähe zum Auftrag: Core / Direct / Indirect) + 2×2-Matrix (Zusammenarbeitsbedarf) in einem Board |
| Nutzen | Aus beiden Einordnungen folgt ein greifbarer Kommunikations-Rhythmus: wen ansprechen, wann, mit welchem Ansatz |
| Framing | Werkzeug für **eigene** Vorbereitung und Planung — nicht Bewertung anderer |
| Betrieb | Privates Projekt, lokal betrieben (Local-First) — nur als Setup/Technik, ohne Rechtsversprechen |

## Copy-Schwerpunkte

Zu pflegen in `script.js` (`translations.de/en.projects.stakeholderIntelligence`) und HTML-Fallbacks in `index.html`.

| Feld | Richtung |
|------|----------|
| `meta` / `valueLabel` | Kommunikations-Rhythmus & Follow-ups, nicht nur „zwei Modelle verbunden“ |
| `overview` | Modelle kurz erklären; Punchline = bewusste Ansprache / Kontakte nicht aus dem Blick verlieren |
| `approachTitle` / `approachText` | Modelle bleiben; Rückschluss explizit auf Ansprache / Rhythmus |
| `result` | MVP mit verbundenen Modellen + lokal; Nutzen andeuten (Rhythmus sichtbar) |
| `contributions` | Modelle + Datenmodell/API + Notizfelder (Kontext, Kommunikationsansatz, Follow-ups / letzter Kontakt-Gedanke) + Code-Review — ohne Profiling-Sprache |
| `details.context` | PM-Alltag: viele Stakeholder, fragmentierte Pflege; privates lokales Board statt Cloud-Tool |
| `details.approach` | Board hält fest, wie ich kommunizieren will; lokal + Next.js/TS-Stack |
| `details.value` | Strategisches Stakeholder-Denken + Rhythmus sichtbar/wiederverwendbar |
| `details.next` | Entfällt (bleibt entfernt) |

## Akzeptanzkriterien

1. Kreis- und Matrix-Erklärung bleiben verständlich und technisch korrekt.
2. Primärer Mehrwert liest sich als Kommunikations-Rhythmus / Follow-up-Unterstützung.
3. Keine der verbotenen DSGVO-/Profiling-Formulierungen.
4. DE und EN inhaltlich parallel; `node scripts/check-i18n.js` grün.
5. HTML-Fallbacks in `index.html` matchen die DE-Strings.

## Umsetzungshinweis

Nach Freigabe dieser Spec: kurzer Implementation-Plan, dann Copy-Edit in einem Schritt (DE/EN + Fallbacks), i18n-Check.
