# Energie-Labor screenshot reproduction

These images show the actual local prototype with synthetic assumptions. English labels are translated in the capture DOM. The underlying prototype currently uses German. Cost values come from the original calculation code.

## Capture

Requires macOS, Swift/WebKit, Python 3 and Pillow. From the portfolio root:

1. Create an empty scratch directory outside the private app.
2. Copy only these files from the sibling `energie-labor/public/`: `index.html`, `styles.css`, `app.mjs`, `model.mjs`, `equipment-ui.mjs`, `journey.mjs`. Compare their SHA-256 hashes with `docs/energie-labor-image-provenance.json`.
3. Start `python3 -m http.server 4198 --bind 127.0.0.1` inside that directory. This is a static server. Private stores, caches and the app API backend stay outside the capture environment.
4. Capture each language with:

   ```sh
   swift scripts/energy-capture/energy-capture.swift http://127.0.0.1:4198/ scripts/energy-capture/energy-capture-de.js /absolute/scratch/energy-de.png
   swift scripts/energy-capture/energy-capture.swift http://127.0.0.1:4198/ scripts/energy-capture/energy-capture-en.js /absolute/scratch/energy-en.png
   ```

5. Convert PNG to RGB, thumbnail to at most 1400 × 1400 using Pillow, and save WebP with `quality=90, method=6`. Saving a new RGB image strips metadata. Verify WebP contains only image chunks, then update the asset hashes in the provenance JSON.
6. Inspect both final images. Confirm sample-data disclosure, labels, full cards, chart, legend, currency and absence of private information.
7. With the portfolio server on port 4188, run `python3 scripts/check-localized-images.py` and `node scripts/check-i18n.js`.
8. Stop the isolated capture server after completing the captures.

The scripts hide the detailed table for this focused analysis view. Scenario cards and chart values are original application output. No private inputs are read.
