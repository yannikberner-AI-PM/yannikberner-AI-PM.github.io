# Energy Industry News Slack Feed Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans (tasks share one script; do not split across subagents). Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the daily Slack post on `energy-latest-industrie-news` energy-sector (DE/EU power, grid, digital energy, policy) with at most two B2B/platform PM items.

**Architecture:** Keep GitHub Action `slack-news.yml` and `scripts/send_slack_news.py`. Add `classify_title` and `select_items`, swap RSS sources, drop module-level Slack env reads so tests can import the script. No LLM. No Cloudflare worker change.

**Tech Stack:** Python 3.12, stdlib `unittest`, `requests` (already used for RSS/Slack).

## Global Constraints

- Slack header is `*Energie-News*` (not `*Latest Career News*`)
- Max **8** items; energy first; at most **2** of those 8 may be `pm`
- Handelsblatt URL is `https://www.handelsblatt.com/contentexport/feed/energie` (not `schlagzeilen`)
- Drop Tagesschau, Lenny, SaaStr, Mind the Product
- Do not change Cloudflare worker copy or deploy wrangler
- Do not rename `.github/workflows/slack-news.yml`
- Secrets unchanged; empty filter result posts nothing
- Tests: `scripts/test_send_slack_news.py` via `python3 -m unittest scripts/test_send_slack_news.py`
- Move `SLACK_CHANNEL_ID` / `SLACK_BOT_TOKEN` reads out of module import so unittest can load the file

## File map

- Modify: `scripts/send_slack_news.py` — sources, classify, select, header, lazy Slack creds
- Create: `scripts/test_send_slack_news.py` — stdlib unittest
- Unchanged: `.github/workflows/slack-news.yml`, `cloudflare/slack-news-worker/`

---

### Task 1: `classify_title` (TDD)

**Files:**
- Create: `scripts/test_send_slack_news.py`
- Modify: `scripts/send_slack_news.py`

**Interfaces:**
- Consumes: none
- Produces: `classify_title(title: str) -> Literal["energy", "pm"] | None`

- [ ] **Step 1: Move Slack env reads off import**

In `send_slack_news.py`, delete module-level `SLACK_CHANNEL_ID` / `SLACK_BOT_TOKEN`. Read them inside `post_to_slack`:

```python
def post_to_slack(text: str) -> None:
    token = os.environ["SLACK_BOT_TOKEN"]
    channel = os.environ["SLACK_CHANNEL_ID"]
    resp = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": f"Bearer {token}"},
        json={"channel": channel, "text": text},
        timeout=30,
    )
```

- [ ] **Step 2: Write failing tests**

Create `scripts/test_send_slack_news.py`:

```python
import unittest
from pathlib import Path
import importlib.util

def load_news():
    path = Path(__file__).with_name("send_slack_news.py")
    spec = importlib.util.spec_from_file_location("send_slack_news", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

CASES = [
    ("Bundesnetzagentur startet Konsultation zur Reform der Netzentgeltsystematik Strom", "energy"),
    ("Überzeichnung der Ausschreibung für PV-Freiflächenanlagen", "energy"),
    ("Streit um Deutschlands Stromreserve", "energy"),
    ("Peter Thiel steigt bei Argentiniens größtem Öl-Exporteur ein", None),
    ("Lufthansa und Air France geben Angebote für TAP ab", None),
    ("Rente: Traumland im Ruhestand", None),
    ("Bundesnetzagentur legt Bedingungen für Leerrohre der Telekom fest", None),
    ("How we redesigned our B2B platform API for enterprise customers", "pm"),
    ("Build an AI code review bot in 30 minutes", None),
]

class ClassifyTitleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.news = load_news()

    def test_spec_fixtures(self):
        for title, expected in CASES:
            with self.subTest(title=title):
                self.assertEqual(self.news.classify_title(title), expected)

if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `python3 -m unittest scripts/test_send_slack_news.py -v`
Expected: FAIL (`classify_title` missing)

- [ ] **Step 4: Implement `classify_title`**

Normalize with `title.casefold()`. Deny wins. Then energy allow (substring), with specials: `wasserstoff` only if also strom/netz/elektrolyse/kraftwerk/energiewende/stromsystem; `ausschreibung` only if also solar/wind/pv/biomasse/eeg/photovoltaik; `ems` via regex `(?<![a-zäöüß])ems(?![a-zäöüß])`. Then PM allow: b2b, plattform, platform, api, saas, produktstrategie, produktmanagement; `product-led` / `product led` only if also b2b/platform/plattform/saas. `post` deny uses the same word-boundary regex so it does not fire inside longer words.

Token lists (casefold):

Energy allow: strom, netz, netzentgelt, redispatch, regelenergie, smart meter, smgw, messstellen, eeg, enwg, msbg, bnetza, bundesnetzagentur, energiewende, photovoltaik, pv-anlage, windkraft, offshore, onshore, speicher, batteriespeicher, hems, wärmepumpe, fernwärme, co2, kohleausstieg, kapazitätsmarkt, stromreserve, gasspeicher, gasnetz, versorgungssicherheit.

Energy deny: opec, ölpreis, rohöl, spritpreis, öl-exporteur, autobauer, lufthansa, boeing, rente, immobilien, dax, telekom, eisenbahn, bahninfrastruktur, ki-verordnung, chatgpt, codex, shopify.

- [ ] **Step 5: Run tests to verify they pass**

Run: `python3 -m unittest scripts/test_send_slack_news.py -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add scripts/send_slack_news.py scripts/test_send_slack_news.py
git commit -m "Add energy/PM title classifier for Slack news."
```

---

### Task 2: `select_items` quotas (TDD)

**Files:**
- Modify: `scripts/test_send_slack_news.py`
- Modify: `scripts/send_slack_news.py`

**Interfaces:**
- Consumes: `classify_title(title: str) -> Literal["energy", "pm"] | None`
- Produces: `select_items(candidates: list[tuple[str, str, str]], already_sent: set[str], max_total: int = 8, max_pm: int = 2) -> list[tuple[str, str, str]]`

- [ ] **Step 1: Write failing tests**

Append:

```python
class SelectItemsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.news = load_news()

    def test_energy_before_pm_and_caps(self):
        candidates = [
            (f"B2B platform API item {i}", f"https://pm/{i}", "PM")
            for i in range(4)
        ] + [
            (f"Stromnetz Reform {i}", f"https://en/{i}", "Energy")
            for i in range(10)
        ]
        selected = self.news.select_items(candidates, already_sent=set())
        self.assertLessEqual(len(selected), 8)
        pm_count = sum(1 for title, _, _ in selected if self.news.classify_title(title) == "pm")
        self.assertLessEqual(pm_count, 2)
        kinds = [self.news.classify_title(t) for t, _, _ in selected]
        if "pm" in kinds and "energy" in kinds:
            self.assertLess(kinds.index("energy"), kinds.index("pm"))

    def test_skips_already_sent_and_offtopic(self):
        candidates = [
            ("Lufthansa Streik", "https://x/1", "HB"),
            ("Stromreserve Streit", "https://x/2", "HB"),
            ("Stromreserve Streit copy", "https://x/2", "HB"),
        ]
        selected = self.news.select_items(candidates, already_sent={"https://x/2"})
        self.assertEqual(selected, [])
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m unittest scripts/test_send_slack_news.py -v`
Expected: FAIL (`select_items` missing)

- [ ] **Step 3: Implement `select_items`**

Walk candidates in order. Skip if `link in already_sent` or title already seen. Classify. Bucket energy vs pm. Return `energy[:max_total] + pm[:min(max_pm, max_total - len(energy))]`.

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m unittest scripts/test_send_slack_news.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/send_slack_news.py scripts/test_send_slack_news.py
git commit -m "Select at most eight energy items and two PM items."
```

---

### Task 3: Swap sources, wire collect, rename Slack header

**Files:**
- Modify: `scripts/send_slack_news.py`
- Modify: `scripts/test_send_slack_news.py`

**Interfaces:**
- Consumes: `select_items`, `classify_title`
- Produces: updated `FEEDS`, `QUERIES`, `MAX_TOTAL_ITEMS = 8`, `MAX_PM_ITEMS = 2`, `collect_new_items` that gathers all sources then `select_items` (do not early-stop at 8 while fetching)

- [ ] **Step 1: Write failing source/header tests**

```python
class SourceAndHeaderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.news = load_news()

    def test_handelsblatt_energie_not_schlagzeilen(self):
        urls = [url for _, url, _ in self.news.FEEDS]
        self.assertIn("https://www.handelsblatt.com/contentexport/feed/energie", urls)
        self.assertTrue(all("schlagzeilen" not in u for u in urls))
        self.assertTrue(all("tagesschau.de" not in u for u in urls))
        self.assertTrue(all("lennysnewsletter.com" not in u for u in urls))
        self.assertTrue(all("saastr.com" not in u for u in urls))
        self.assertTrue(all("mindtheproduct.com" not in u for u in urls))

    def test_required_new_feeds(self):
        urls = [url for _, url, _ in self.news.FEEDS]
        self.assertIn("https://www.cleanenergywire.org/rss.xml", urls)
        self.assertTrue(any("RSSNewsfeed_Pressemitteilungen.xml" in u for u in urls))
        self.assertTrue(any("RSSNewsfeed_EEG.xml" in u for u in urls))

    def test_header_constant(self):
        self.assertEqual(self.news.SLACK_HEADER, "*Energie-News*")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m unittest scripts/test_send_slack_news.py -v`
Expected: FAIL (old feeds / missing header constant)

- [ ] **Step 3: Replace FEEDS, QUERIES, collect, header**

`FEEDS`:

```python
FEEDS = [
    ("PV Magazine Deutschland", "https://www.pv-magazine.de/feed/", 3),
    ("IWR", "https://www.iwr.de/news/rss", 2),
    ("Erneuerbare Energien Magazin", "https://www.erneuerbareenergien.de/rss.xml", 2),
    ("Handelsblatt Energie", "https://www.handelsblatt.com/contentexport/feed/energie", 3),
    ("Clean Energy Wire", "https://www.cleanenergywire.org/rss.xml", 3),
    ("BNetzA Pressemitteilungen", "https://www.bundesnetzagentur.de/SiteGlobals/Functions/RSSFeed/DE/RSSNewsfeed/RSSNewsfeed_Pressemitteilungen.xml", 2),
    ("BNetzA EEG-Ausschreibungen", "https://www.bundesnetzagentur.de/SiteGlobals/Functions/RSSFeed/DE/RSSNewsfeed/RSSNewsfeed_EEG.xml", 2),
]
```

Default `NEWS_QUERIES`:

```
Energiewende Regulierung Deutschland:3|
Smart Meter Gateway Rollout Deutschland:2|
Bundesnetzagentur Strom Netz:2|
EU Strommarkt Redispatch Speicher:2|
B2B SaaS Plattform API Produktmanagement:1
```

```python
MAX_TOTAL_ITEMS = 8
MAX_PM_ITEMS = 2
SLACK_HEADER = "*Energie-News*"

def collect_new_items(already_sent: set[str]) -> list[tuple[str, str, str]]:
    candidates: list[tuple[str, str, str]] = []
    for name, url, limit in FEEDS:
        candidates.extend(recent_items_from_feed(name, url, limit))
    for q in QUERIES:
        candidates.extend(recent_items_from_query(*parse_weighted_query(q)))
    return select_items(candidates, already_sent, MAX_TOTAL_ITEMS, MAX_PM_ITEMS)
```

In `main`, post `f"{SLACK_HEADER} :newspaper:\n\n" + ...`. Update the module docstring to say energy-industry news.

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m unittest scripts/test_send_slack_news.py -v`
Expected: all PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/send_slack_news.py scripts/test_send_slack_news.py
git commit -m "Point Slack news at energy sources and Energie-News header."
```
