#!/usr/bin/env python3
"""Fetch the latest career news via free Google News RSS feeds and post them to Slack."""
import os
import sys
import xml.etree.ElementTree as ET
from urllib.parse import quote

import requests

QUERIES = [q.strip() for q in os.environ.get(
    "NEWS_QUERIES",
    "AI product management|"
    "connected energy OR smart metering OR HEMS home energy management|"
    "B2B SaaS product strategy|"
    "software product modernization OR platform transformation",
).split("|")]

MAX_ITEMS_PER_QUERY = 2
MAX_TOTAL_ITEMS = 8

SLACK_CHANNEL_ID = os.environ["SLACK_CHANNEL_ID"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]


def fetch_items_for_query(query: str) -> list[tuple[str, str]]:
    url = f"https://news.google.com/rss/search?q={quote(query)}+when:7d&hl=de&gl=DE&ceid=DE:de"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)
    items = []
    for item in root.findall("./channel/item")[:MAX_ITEMS_PER_QUERY]:
        title = item.findtext("title", "").strip()
        link = item.findtext("link", "").strip()
        if title and link:
            items.append((title, link))
    return items


def build_message() -> str:
    seen_titles = set()
    lines = []
    for query in QUERIES:
        for title, link in fetch_items_for_query(query):
            if title in seen_titles:
                continue
            seen_titles.add(title)
            lines.append(f"• <{link}|{title}>")
            if len(lines) >= MAX_TOTAL_ITEMS:
                break
        if len(lines) >= MAX_TOTAL_ITEMS:
            break
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
