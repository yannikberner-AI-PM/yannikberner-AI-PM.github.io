# Portfolio copy alignment QA

## Scope

Updated `script.js` in German and English and synchronized `index.html` text, alt/aria fallbacks and metadata with the German strings. Positioning now follows AI, connected energy, IoT and complex software/hardware products. Professional results retain contribution-level attribution; independent prototypes describe intended benefits and implementation limits. The existing Energie-Labor project, images, layout changes and other working-tree additions are retained.

Sources: live GitHub profile `yannikberner-AI-PM/yannikberner-AI-PM`, `README.de.md` and `README.md`, retrieved using the GitHub API. These current descriptions supersede historical prototype framing in the August design specs for the requested alignment. Added localized links to movur, Stakeholder Intelligence, Predictive Mentoring and Cyber Security Connector showcases. Their German README targets resolve through the API.

## Current correction: remove all project showcase links

The follow-up user instruction supersedes the earlier four-link decision: removed the four remaining project CTA paragraphs from `index.html` and the shared showcase label/aria translation keys from both languages in `script.js`. The general GitHub profile contact, all projects, images and other copy remain unchanged from published baseline `8ee1f0d0dc5c5decc94a04b2e99e91347a7246bd`.

The updated regression first failed against that baseline with `Project showcase links must be absent in DE/EN: found 4`, then passed after the removal. It checks all link attributes, including localized DE/EN URLs, for showcase references and retains the GitHub profile contact assertion. No browser was opened or automated for this correction. Historical browser results below describe only the earlier release.

## Verified static checks (current correction)

- `node scripts/check-i18n.js`: 429 keys resolve in DE/EN; JavaScript syntax passes.
- `python3 scripts/check-copy.py`: 510 German text/alt/aria fallback instances match; DE/EN translation shape, metadata, zero showcase links, retained GitHub profile contact, anchors, maturity disclosures and public German voice pass. Date ranges and privacy copy are outside the rhetorical-dash/voice scan.
- `git diff --check`: passes.

## Browser verification (historical; completed before browser stop instruction)

Parent verification reran all three static checks successfully. `python3 scripts/check-localized-images.py` passed in native Safari against `http://127.0.0.1:4188/`: DE/EN deep links and live language switches, loaded localized images and captions, full-size links and focus. English responsive checks passed at 1440, 768, 390 and 360 px with no page overflow or image cropping. This is DOM/layout verification, not a full visual acceptance of every section. The server's index response was verified against the working-tree file before the copy pass.

The inherited Energie-Labor showcase returned GitHub API 404. In the earlier release, this was resolved by deliberately removing only that CTA, as then requested, in both languages. At that time, four other showcase links remained; the current correction removes them. The changed copy regression first failed with five links and passed after removing the energy CTA. Historical native Safari checks confirmed zero energy GitHub CTAs and four remaining showcases in DE/EN. One rerun encountered transient language state; the subsequent full run passed. No further browser opening, navigation or automation is permitted after the user's stop instruction; release verification uses static checks and HTTP source readback.

Production release is explicitly authorized for the complete approved DE/EN working-tree content. Reviewed CSS changes only add the energy media figure/caption layout; localized source updates preserve full-size image links. Synthetic image provenance and capture sources are included. Private `.hermes/` session material is excluded. Deployment completion and exact committed-source HTTP readback are reported with the release PR rather than assumed here.
