# Slack News Trigger Worker

Cloudflare Worker that lets `/latest-news` in Slack trigger the
`Slack Career News` GitHub Actions workflow on demand, in addition to
its Monday schedule.

## Setup

1. Install Wrangler and log in:
   ```bash
   npm install -g wrangler
   wrangler login
   ```

2. From this directory, set the secrets (you'll be prompted for each value):
   ```bash
   wrangler secret put SLACK_SIGNING_SECRET
   wrangler secret put GITHUB_TOKEN
   wrangler secret put GITHUB_OWNER   # e.g. yannikberner-AI-PM
   wrangler secret put GITHUB_REPO    # e.g. yannikberner-AI-PM.github.io
   wrangler secret put GITHUB_REF     # branch to run on, e.g. main
   ```

   - `SLACK_SIGNING_SECRET`: Slack app → **Basic Information** → "Signing Secret"
   - `GITHUB_TOKEN`: a fine-grained GitHub PAT scoped to this repo only, with
     **Actions: Read and write** permission

3. Deploy:
   ```bash
   wrangler deploy
   ```
   This prints the Worker URL, e.g. `https://slack-news-trigger.<you>.workers.dev`.

4. In the Slack app (**api.slack.com/apps → Latest-Career-News**):
   - Go to **Slash Commands** → **Create New Command**
   - Command: `/latest-news`
   - Request URL: the Worker URL from step 3
   - Short description: "Send the latest career news now"
   - Save, then reinstall the app to the workspace if prompted

5. Test in the channel: type `/latest-news`. You should get an ephemeral
   "fetching..." reply immediately, then the news message from the bot
   within a minute or two (GitHub Actions run time).
