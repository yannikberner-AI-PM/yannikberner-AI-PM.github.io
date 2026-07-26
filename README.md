# Yannik Berner – Product Portfolio

Zweisprachige, statische Portfolio-Website für Bewerbungen auf Senior- und Mid-Senior-Product-Rollen. Die Positionierung verbindet zwei gleichwertige Schwerpunkte:

- Connected Energy, HEMS, Smart Metering und Energy Platforms
- Software Product Modernization, B2B SaaS sowie Enterprise- und Plattformtransformation

Produktions-URL: <https://yannikberner-ai-pm.github.io/>

## Projektstruktur

- `index.html` – Portfolio und Projektstationen
- `datenschutz.html` – zweisprachige Datenschutzerklärung
- `404.html` – Fehlerseite für GitHub Pages
- `robots.txt` und `sitemap.xml` – Suchmaschinen-Crawling
- `styles.css` – Designsystem und Responsive-Verhalten
- `script.js` – Übersetzungen, Sprachumschaltung, Navigation und Detailansichten
- `assets/images/` – Portrait und Projektbilder
- `.nojekyll` – verhindert die Jekyll-Verarbeitung auf GitHub Pages

Die Website verwendet bewusst keine Frameworks, Build Tools oder externen JavaScript-Abhängigkeiten.

`favicon-32.png` und `yannik-berner-social-preview.png` wurden ausschließlich aus bereits vorhandenen, freigegebenen Elementen erzeugt (Portraitfoto, echte Seitentexte, bestehende Marken-/Designfarben aus `styles.css`) – gerendert mit headless Chrome (`--screenshot`) und mit `sips` auf 32×32 verkleinert. Keine Bildrechte oder Logos Dritter wurden verwendet.

### Ungenutzte Bild-Assets (Nutzerentscheidung ausstehend)

Folgende Dateien in `assets/images/` werden aktuell in keiner HTML-Seite referenziert (vermutlich Reste einer früheren Mehrbild-Galerie je Case Study, seit der Umstellung auf je ein Collage-Bild pro Station nicht mehr verlinkt). Sie wurden bewusst nicht gelöscht:

`enertrag-digital-resilience-framework.png`, `enertrag-wind-power-curve.png`, `enertrag-wind-turbine.png`, `mercedes-ci-cd-pipeline.png`, `mercedes-online-code.jpg`, `mercedes-salesforce-service-console.png`, `remindme-kanban-board.jpg`, `remindme-mobile-app.png`, `remindme-platform-dashboard.png`, `senec-energy-storage-system.png`, `senec-hems-architecture.png`, `soniq-iot-building.jpg`, `soniq-iq-dashboard.png`, `soniq-product-roadmap.jpg`

Zusammen ca. 3,3 MB. Löschen oder weiterverwenden ist eine bewusste Entscheidung des Repository-Eigentümers.

## Lokal ansehen

Für lokale Entwicklung und realistische Tests mit relativen Links:

```sh
python3 -m http.server 4173
```

Anschließend ist das Portfolio unter `http://localhost:4173/` erreichbar.

## Inhalte und Sprache pflegen

Die sichtbaren Texte werden über `data-i18n`-Attribute in den HTML-Dateien mit den Sprachobjekten `translations.de` und `translations.en` in `script.js` verbunden.

Beim Ergänzen oder Ändern von Inhalten:

1. denselben Schlüssel in `de` und `en` pflegen,
2. vorhandene Projekt-IDs und interne Sprungmarken beibehalten,
3. externe Projektlinks mit `target="_blank"` sowie `rel="noopener noreferrer"` versehen,
4. neue Tabs mit einem lokalisierten zugänglichen Hinweis beschriften,
5. sprachabhängige Meta-Texte in `script.js` mitpflegen,
6. Datenschutztexte nur auf Basis belegter Technik und aktueller Primärquellen ändern.

Die Sprache ist über `?lang=de` beziehungsweise `?lang=en` teilbar. `localStorage` merkt ergänzend die zuletzt gewählte Sprache. Es gibt keine separaten HTML-Sprach-URLs und daher bewusst keine `hreflang`-Angaben.

## QA-Checkliste

- `node --check script.js`
- Deutsch und Englisch auf Haupt- und Datenschutzseite
- Navigation, Escape-Taste, Details und sichtbare Fokuszustände per Tastatur
- JavaScript-Ausfall und `prefers-reduced-motion`
- keine fehlenden Ressourcen, doppelten IDs oder i18n-Schlüssel
- kein horizontaler Overflow bei 1440×900, 1024×768, 768×1024, 390×844 und 360×800
- externe Links und neue-Tab-Hinweise
- Kontrast, Bildabmessungen und Browser-Konsole

## Rechtliche Hinweise (keine Rechtsberatung)

- Es wird bewusst kein Impressum veröffentlicht. Der Repository-Eigentümer stuft die Seite als private Bewerbungs-Portfolioseite ohne geschäftsmäßiges Telemedienangebot im Sinne von § 5 DDG ein. Diese Einschätzung ersetzt keine anwaltliche Prüfung und sollte bei Änderung des Nutzungszwecks erneut bewertet werden.
- Die Telefonnummer wurde auf ausdrücklichen Wunsch aus dem Kontaktbereich entfernt; E-Mail und LinkedIn bleiben als Kontaktwege bestehen.

## Veröffentlichung

Das Repository `yannikberner-AI-PM.github.io` ist als statische GitHub-Pages-Seite auf dem Branch `main` ausgelegt. Vor der Veröffentlichung:

1. vollständigen Diff und QA-Ergebnisse prüfen,
2. nur freigegebene Dateien explizit stagen,
3. erst nach finaler Nutzerfreigabe committen und pushen,
4. anschließend Deployment, HTTPS, Assets und Rechtstexte read-only verifizieren.

Für eine spätere eigene Domain zuerst Domain und DNS bestätigen. Danach kann ein `CNAME` mit exakt dieser Domain ergänzt und die GitHub-Pages-Domainkonfiguration separat vorgenommen werden. Ohne bestätigte Domain wird kein `CNAME` angelegt.
