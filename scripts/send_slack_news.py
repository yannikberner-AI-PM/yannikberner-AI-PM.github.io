#!/usr/bin/env python3
"""Fetch recent DE/EU energy-industry news from RSS and post unseen items to Slack."""
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import quote

FEEDS = [
    ("PV Magazine Deutschland", "https://www.pv-magazine.de/feed/", 3),
    ("IWR", "https://www.iwr.de/news/rss", 2),
    ("Erneuerbare Energien Magazin", "https://www.erneuerbareenergien.de/rss.xml", 2),
    ("Handelsblatt Energie", "https://www.handelsblatt.com/contentexport/feed/energie", 3),
    ("Clean Energy Wire", "https://www.cleanenergywire.org/rss.xml", 3),
    (
        "BNetzA Pressemitteilungen",
        "https://www.bundesnetzagentur.de/SiteGlobals/Functions/RSSFeed/DE/RSSNewsfeed/RSSNewsfeed_Pressemitteilungen.xml",
        2,
    ),
    (
        "BNetzA EEG-Ausschreibungen",
        "https://www.bundesnetzagentur.de/SiteGlobals/Functions/RSSFeed/DE/RSSNewsfeed/RSSNewsfeed_EEG.xml",
        2,
    ),
]

QUERIES = [q.strip() for q in os.environ.get(
    "NEWS_QUERIES",
    "Energiewende Regulierung Deutschland:3|"
    "Smart Meter Gateway Rollout Deutschland:2|"
    "Bundesnetzagentur Strom Netz:2|"
    "EU Strommarkt Redispatch Speicher:2|"
    "B2B SaaS Plattform API Produktmanagement:1",
).split("|")]

MAX_AGE_DAYS = 7
MAX_TOTAL_ITEMS = 8
MAX_PM_ITEMS = 2
MAX_CACHE_ENTRIES = 1000
SLACK_HEADER = "*Energie-News*"

CACHE_PATH = Path(os.environ.get("NEWS_CACHE_PATH", "scripts/.news_cache.json"))

ENERGY_ALLOW = (
    "strom",
    "netz",
    "netzentgelt",
    "redispatch",
    "regelenergie",
    "smart meter",
    "smgw",
    "messstellen",
    "eeg",
    "enwg",
    "msbg",
    "bnetza",
    "bundesnetzagentur",
    "energiewende",
    "photovoltaik",
    "pv-anlage",
    "windkraft",
    "offshore",
    "onshore",
    "speicher",
    "batteriespeicher",
    "hems",
    "wärmepumpe",
    "fernwärme",
    "co2",
    "kohleausstieg",
    "kapazitätsmarkt",
    "stromreserve",
    "gasspeicher",
    "gasnetz",
    "versorgungssicherheit",
)

ENERGY_DENY = (
    "opec",
    "ölpreis",
    "rohöl",
    "spritpreis",
    "öl-exporteur",
    "autobauer",
    "lufthansa",
    "boeing",
    "rente",
    "immobilien",
    "dax",
    "telekom",
    "eisenbahn",
    "bahninfrastruktur",
    "ki-verordnung",
    "chatgpt",
    "codex",
    "shopify",
)

PM_ALLOW = (
    "b2b",
    "plattform",
    "platform",
    "saas",
    "produktstrategie",
    "produktmanagement",
)

WASSERSTOFF_HINTS = (
    "strom",
    "netz",
    "elektrolyse",
    "kraftwerk",
    "energiewende",
    "stromsystem",
)

AUSSCHREIBUNG_HINTS = (
    "solar",
    "wind",
    "pv",
    "biomasse",
    "eeg",
    "photovoltaik",
)

_WORD = r"(?<![a-zäöüß]){}(?![a-zäöüß])"


def _has_word(text: str, token: str) -> bool:
    return re.search(_WORD.format(re.escape(token)), text) is not None


def _denied(text: str) -> bool:
    if any(token in text for token in ENERGY_DENY):
        return True
    return _has_word(text, "post")


def _energy_allowed(text: str) -> bool:
    if any(token in text for token in ENERGY_ALLOW):
        return True
    if _has_word(text, "ems"):
        return True
    if "wasserstoff" in text and any(hint in text for hint in WASSERSTOFF_HINTS):
        return True
    if "ausschreibung" in text and any(hint in text for hint in AUSSCHREIBUNG_HINTS):
        return True
    return False


def _pm_allowed(text: str) -> bool:
    if any(token in text for token in PM_ALLOW):
        return True
    if _has_word(text, "api"):
        return True
    if "product-led" in text or "product led" in text:
        return any(token in text for token in ("b2b", "platform", "plattform", "saas"))
    return False


def classify_title(title: str) -> str | None:
    text = title.casefold()
    if _denied(text):
        return None
    if _energy_allowed(text):
        return "energy"
    if _pm_allowed(text):
        return "pm"
    return None


def parse_pub_date(raw: str) -> datetime | None:
    if not raw:
        return None
    try:
        dt = parsedate_to_datetime(raw)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except (TypeError, ValueError):
        return None


def fetch_feed_items(url: str) -> list[tuple[str, str, datetime | None]]:
    import requests

    resp = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
    resp.raise_for_status()
    root = ET.fromstring(resp.content)
    items = []
    for item in root.findall("./channel/item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub_date = parse_pub_date(item.findtext("pubDate") or "")
        if title and link:
            items.append((title, link, pub_date))
    return items


def recent_items_from_feed(name: str, url: str, limit: int) -> list[tuple[str, str, str]]:
    import requests

    cutoff = datetime.now(timezone.utc) - timedelta(days=MAX_AGE_DAYS)
    try:
        items = fetch_feed_items(url)
    except (requests.RequestException, ET.ParseError) as exc:
        print(f"Skipping feed {name} ({url}): {exc}", file=sys.stderr)
        return []
    fresh = [(t, l, name) for t, l, d in items if d is None or d >= cutoff]
    return fresh[:limit]


def recent_items_from_query(query: str, limit: int) -> list[tuple[str, str, str]]:
    import requests

    url = f"https://news.google.com/rss/search?q={quote(query)}+when:{MAX_AGE_DAYS}d&hl=de&gl=DE&ceid=DE:de"
    try:
        items = fetch_feed_items(url)
    except (requests.RequestException, ET.ParseError) as exc:
        print(f"Skipping query '{query}': {exc}", file=sys.stderr)
        return []
    return [(t, l, "Google News") for t, l, _ in items[:limit]]


def parse_weighted_query(entry: str) -> tuple[str, int]:
    query, _, weight = entry.rpartition(":")
    if query and weight.isdigit():
        return query, int(weight)
    return entry, 1


def load_cache() -> set[str]:
    if not CACHE_PATH.exists():
        return set()
    try:
        return set(json.loads(CACHE_PATH.read_text()))
    except (json.JSONDecodeError, OSError):
        return set()


def save_cache(links: set[str]) -> None:
    trimmed = list(links)[-MAX_CACHE_ENTRIES:]
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(trimmed, indent=2))


def select_items(
    candidates: list[tuple[str, str, str]],
    already_sent: set[str],
    max_total: int = MAX_TOTAL_ITEMS,
    max_pm: int = MAX_PM_ITEMS,
) -> list[tuple[str, str, str]]:
    energy: list[tuple[str, str, str]] = []
    pm: list[tuple[str, str, str]] = []
    seen_titles: set[str] = set()

    for title, link, source in candidates:
        if link in already_sent or title in seen_titles:
            continue
        kind = classify_title(title)
        if kind is None:
            continue
        seen_titles.add(title)
        if kind == "energy":
            energy.append((title, link, source))
        else:
            pm.append((title, link, source))

    selected = energy[:max_total]
    remaining = max_total - len(selected)
    selected.extend(pm[: min(max_pm, remaining)])
    return selected


def collect_new_items(already_sent: set[str]) -> list[tuple[str, str, str]]:
    candidates: list[tuple[str, str, str]] = []
    for name, url, limit in FEEDS:
        candidates.extend(recent_items_from_feed(name, url, limit))
    for query in QUERIES:
        candidates.extend(recent_items_from_query(*parse_weighted_query(query)))
    return select_items(candidates, already_sent, MAX_TOTAL_ITEMS, MAX_PM_ITEMS)


def post_to_slack(text: str) -> None:
    import requests

    token = os.environ["SLACK_BOT_TOKEN"]
    channel = os.environ["SLACK_CHANNEL_ID"]
    resp = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": f"Bearer {token}"},
        json={"channel": channel, "text": text},
        timeout=30,
    )
    resp.raise_for_status()
    body = resp.json()
    if not body.get("ok"):
        raise RuntimeError(f"Slack API error: {body.get('error')}")


def main() -> None:
    already_sent = load_cache()
    new_items = collect_new_items(already_sent)

    if not new_items:
        print("No new items since last run, nothing to post.")
        return

    lines = [f"• <{link}|{title}> _({source})_" for title, link, source in new_items]
    post_to_slack(f"{SLACK_HEADER} :newspaper:\n\n" + "\n".join(lines))
    print(f"Posted {len(new_items)} new item(s) to Slack.")

    save_cache(already_sent | {link for _, link, _ in new_items})


if __name__ == "__main__":
    main()
