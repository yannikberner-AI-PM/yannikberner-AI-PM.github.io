# Design: Energy Industry News Slack feed

**Datum:** 2026-08-19
**Status:** Draft (awaiting spec review)
**Repo:** `~/Projects/portfolio` (not career-intelligence)
**Channel:** `energy-latest-industrie-news`
**Code today:** `scripts/send_slack_news.py`, `.github/workflows/slack-news.yml`

## Ziel

The daily Slack post should read as **DE/EU power, grid, digital energy, and energy policy**, plus at most two B2B/platform product-management items. It must stop mixing in generic economy, oil-commodity, auto, airline, pension, and AI-coding headlines.

## Entscheidungen (fest)

| Thema | Entscheidung |
|-------|----------------|
| Approach | Specialist RSS + title keyword gate + quotas. No LLM. Same GitHub Action. |
| Handelsblatt | Keep, switch URL from Schlagzeilen to Energie feed. |
| Career/PM blogs | Drop Lenny, SaaStr, Mind the Product as sources. |
| Tagesschau | Drop. |
| Slash command copy | Leave `/latest-news` Cloudflare worker text as “Career News”. Do not deploy the worker in this change. |
| Slack post header | `*Energie-News*` (replace `*Latest Career News*`). |
| Volume | Max **8** items. Energy first. At most **2** of those 8 may be B2B/platform PM. |
| Empty run | If nothing new passes the gate, post nothing (current behaviour). |
| Secrets | Unchanged (`SLACK_BOT_TOKEN`, `SLACK_CHANNEL_ID`). |

## Why the feed is broad today

`collect_new_items` takes the first N items from each feed with **no topic filter**. Tagesschau Wirtschaft and Handelsblatt Schlagzeilen fill the list with auto, Lufthansa, pensions, DAX. Lenny/SaaStr add career/AI-tool posts. `MAX_TOTAL_ITEMS = 12` is reached before the Google News energy queries run.

## Architecture

Unchanged runtime:

```text
05:00 UTC GitHub Action  (or /latest-news → slack-news.yml)
  → scripts/send_slack_news.py
       fetch RSS → filter/classify → quota
       post Slack → update scripts/.news_cache.json
```

Changed units (all in `send_slack_news.py`, testable without Slack):

1. **Sources** — feed list and Google queries.
2. **`classify_title(title) -> "energy" | "pm" | None`** — allow/deny on the title string (case-insensitive, DE+EN).
3. **`select_items(candidates, already_sent)`** — unseen links only; fill energy up to 8; then PM until 2 or total 8.
4. **Poster** — new header; same channel; same URL cache.

A dead feed is skipped and logged to stderr. Slack API errors still fail the job.

## Sources

### Keep

| Source | URL | Weight |
|--------|-----|--------|
| PV Magazine Deutschland | `https://www.pv-magazine.de/feed/` | 3 |
| IWR | `https://www.iwr.de/news/rss` | 2 |
| Erneuerbare Energien Magazin | `https://www.erneuerbareenergien.de/rss.xml` | 2 |
| Handelsblatt Energie | `https://www.handelsblatt.com/contentexport/feed/energie` | 3 |

Handelsblatt Energie is verified `application/rss+xml`. It still contains oil-exporter stories, so the keyword gate applies to this feed too.

### Add

| Source | URL | Weight |
|--------|-----|--------|
| Clean Energy Wire | `https://www.cleanenergywire.org/rss.xml` | 3 |
| BNetzA Pressemitteilungen | `https://www.bundesnetzagentur.de/SiteGlobals/Functions/RSSFeed/DE/RSSNewsfeed/RSSNewsfeed_Pressemitteilungen.xml` | 2 |
| BNetzA EEG-Ausschreibungen | `https://www.bundesnetzagentur.de/SiteGlobals/Functions/RSSFeed/DE/RSSNewsfeed/RSSNewsfeed_EEG.xml` | 2 |

BNetzA press also publishes Bahn, Telekom, and KI-Verordnung. Those must fail the energy allowlist.

### Drop

- Tagesschau Wirtschaft
- Handelsblatt Schlagzeilen (`contentexport/feed/schlagzeilen`)
- Mind the Product
- Lenny's Newsletter
- SaaStr

### Google News queries (DE)

Replace the current mix with:

- `Energiewende Regulierung Deutschland:3`
- `Smart Meter Gateway Rollout Deutschland:2`
- `Bundesnetzagentur Strom Netz:2`
- `EU Strommarkt Redispatch Speicher:2`
- `B2B SaaS Plattform API Produktmanagement:1`

`NEWS_QUERIES` env override stays. Every query result still goes through `classify_title`.

## Title gate

Match on title only (lowercase). A title is **energy** if it matches at least one energy allow token **and** no deny token. A title is **pm** if it matches at least one PM allow token **and** no deny token **and** is not already energy. Otherwise drop.

### Energy allow (power, digital energy, DE/EU policy)

Strom, Netz, Netzentgelt, Redispatch, Regelenergie, Smart Meter, SMGW, Messstellen, EEG, EnWG, MsbG, BNetzA, Bundesnetzagentur, Energiewende, Photovoltaik, PV-Anlage, Windkraft, Offshore, Onshore, Speicher, Batteriespeicher, HEMS, EMS, Wärmepumpe, Fernwärme, Wasserstoff (with Strom/Netz/Elektrolyse/Kraftwerk in the same title, or standalone “Wasserstoff” plus Energiewende/Stromsystem), CO2, Kohleausstieg, Kapazitätsmarkt, Stromreserve, Gasspeicher, Gasnetz, Versorgungssicherheit, Ausschreibung (with Solar/Wind/PV/Biomasse/EEG).

### Energy deny (commodities, other sectors)

OPEC, Ölpreis, Rohöl, Spritpreis, Öl-Exporteur, Autobauer, Lufthansa, Boeing, Rente, Immobilien, DAX, Telekom, Post, Eisenbahn, Bahninfrastruktur, KI-Verordnung, ChatGPT, Codex, Shopify.

Gas **policy** (Gasspeicher, Gasnetz, Verzinsung Gasnetz) is allowed. Gas/oil **commodity price** headlines are denied.

### PM allow (max 2)

B2B, Plattform, Platform, API, SaaS, Product-Led (only with B2B/platform/SaaS), Produktstrategie, Produktmanagement — and not matching energy deny. Consumer growth-hacks, AI coding assistants, and Shopify-style consumer SaaS are deny (already listed).

## Tests

Add `scripts/test_send_slack_news.py` (stdlib `unittest`, no extra CI job).

Fixtures (keep / drop / pm):

| Title | Class |
|-------|--------|
| Bundesnetzagentur startet Konsultation zur Reform der Netzentgeltsystematik Strom | energy |
| Überzeichnung der Ausschreibung für PV-Freiflächenanlagen | energy |
| Streit um Deutschlands Stromreserve | energy |
| Peter Thiel steigt bei Argentiniens größtem Öl-Exporteur ein | drop |
| Lufthansa und Air France geben Angebote für TAP ab | drop |
| Rente: Traumland im Ruhestand | drop |
| Bundesnetzagentur legt Bedingungen für Leerrohre der Telekom fest | drop |
| How we redesigned our B2B platform API for enterprise customers | pm |
| Build an AI code review bot in 30 minutes | drop |

Also assert: `select_items` returns at most 8, at most 2 `pm`, energy before pm; Schlagzeilen URL is absent; Energie URL is present.

The daily workflow does not run these tests.

## Out of scope

- Cloudflare worker copy or `wrangler deploy`
- Career-intelligence-agent-private
- LLM classification
- Changing Slack channel ID or bot token
- Renaming the workflow file `slack-news.yml` (slash command dispatch depends on it)

## Erfolgskriterien

- A typical daily post is mostly Strom/Netz/EEG/Smart-Meter/policy, not auto/airline/pension.
- Handelsblatt still appears, via the Energie feed, with oil-commodity titles removed.
- At most two B2B/platform PM items; zero is fine.
- Failed RSS does not fail the Action.
- Unit tests cover the table above.
