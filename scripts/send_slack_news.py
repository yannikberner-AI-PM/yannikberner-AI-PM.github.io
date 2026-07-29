#!/usr/bin/env python3
"""Fetch the latest career news from several free RSS sources and post them to Slack."""
import os
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from urllib.parse import quote

import requests

# Direct RSS feeds from relevant trade sites, weighted towards German/European
# energy and regulation coverage, with AI/PM as a smaller share.
FEEDS = [
    ("PV Magazine Deutschland", "https://www.pv-magazine.de/feed/", 3),
    ("IWR", "https://www.iwr.de/news/rss", 2),
    ("Erneuerbare Energien Magazin", "https://www.erneuerbareenergien.de/rss.xml", 2),
    ("Tagesschau Wirtschaft", "https://www.tagesschau.de/wirtschaft/index~rss2.xml", 2),
    ("Mind the Product", "https://www.mindtheproduct.com/feed/", 1),
    ("Lenny's Newsletter", "https://www.lennysnewsletter.com/feed", 1),
    ("SaaStr", "https://www.saastr.com/feed/", 1),
]

# Broader topic searches via Google News (German results), to catch things the
# trade feeds miss. Weighted towards Germany/Europe, energy and regulation.
QUERIES = [q.strip() for q in os.environ.get(
    "NEWS_QUERIES",
    "Energiewende Regulierung Deutschland:3|"
    "Smart Meter Rollout Deutschland:2|"
    "EU Energiepolitik Regulierung:2|"
    "Bundesnetzagentur Energie:2|"
    "B2B SaaS Produktstrategie:1|"
    "AI Produktmanagement:1",
).split("|")]

MAX_AGE_DAYS = 7
MAX_TOTAL_ITEMS = 12

SLACK_CHANNEL_ID = os.environ["SLACK_CHANNEL_ID"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]


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
    cutoff = datetime.now(timezone.utc) - timedelta(days=MAX_AGE_DAYS)
    try:
        items = fetch_feed_items(url)
    except (requests.RequestException, ET.ParseError) as exc:
        print(f"Skipping feed {name} ({url}): {exc}", file=sys.stderr)
        return []
    fresh = [(t, l, name) for t, l, d in items if d is None or d >= cutoff]
    return fresh[:limit]


def recent_items_from_query(query: str, limit: int) -> list[tuple[str, str, str]]:
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


def build_message() -> str:
    seen_titles = set()
    lines = []

    sources = [recent_items_from_feed(name, url, limit) for name, url, limit in FEEDS]
    sources += [
        recent_items_from_query(*parse_weighted_query(q)) for q in QUERIES
    ]

    for items in sources:
        for title, link, source in items:
            if title in seen_titles:
                continue
            seen_titles.add(title)
            lines.append(f"• <{link}|{title}> _({source})_")
            if len(lines) >= MAX_TOTAL_ITEMS:
                return "\n".join(lines)
    return "\n".join(lines)


def post_to_slack(text: str) -> None:
    resp = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"},
        json={"channel": SLACK_CHANNEL_ID, "text": text},
        timeout=30,
    )
    resp.raise_for_status()
    body = resp.json()
    if not body.get("ok"):
        raise RuntimeError(f"Slack API error: {body.get('error')}")


def main() -> None:
    news_lines = build_message()
    if not news_lines:
        print("No news items found, aborting.", file=sys.stderr)
        sys.exit(1)
    post_to_slack(f"*Latest Career News* :newspaper:\n\n{news_lines}")
    print("Posted to Slack successfully.")


if __name__ == "__main__":
    main()
