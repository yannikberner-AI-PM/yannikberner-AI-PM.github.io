#!/usr/bin/env python3
"""Fetch the latest AI/PM career news via Claude's web search and post it to Slack."""
import os
import sys

import anthropic
import requests

NEWS_TOPIC = os.environ.get(
    "NEWS_TOPIC",
    "AI in product management; connected energy, HEMS (home energy management) "
    "and smart metering; B2B SaaS product strategy; software product "
    "modernization and platform transformation",
)
SLACK_CHANNEL_ID = os.environ["SLACK_CHANNEL_ID"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]


def fetch_news_summary() -> str:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=1024,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[
            {
                "role": "user",
                "content": (
                    f"Search the web for the most important news from the last 7 days "
                    f"about: {NEWS_TOPIC}. Summarize the 3-5 most relevant items as a "
                    "short Slack message in German, using bullet points with an emoji "
                    "prefix, one line per item, each with a source link. Keep it concise."
                ),
            }
        ],
    )
    return "".join(
        block.text for block in response.content if block.type == "text"
    ).strip()


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
    summary = fetch_news_summary()
    if not summary:
        print("No summary generated, aborting.", file=sys.stderr)
        sys.exit(1)
    post_to_slack(f"*Latest Career News* :newspaper:\n\n{summary}")
    print("Posted to Slack successfully.")


if __name__ == "__main__":
    main()
