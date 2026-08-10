#!/usr/bin/env node
/**
 * Assert every data-i18n / data-i18n-alt / data-i18n-aria key in HTML
 * resolves to a string in both translations.de and translations.en.
 *
 * Usage (from repo root):
 *   node --check script.js && node scripts/check-i18n.js
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..');
const SCRIPT_JS = path.join(ROOT, 'script.js');
const HTML_FILES = ['index.html', 'datenschutz.html'].map((f) => path.join(ROOT, f));
const ATTR_PATTERN = /data-i18n(?:-alt|-aria)?=["']([^"']+)["']/g;

function getByPath(object, keyPath) {
  return keyPath.split('.').reduce((current, segment) => current?.[segment], object);
}

function extractTranslations(source) {
  const marker = 'const translations = ';
  const start = source.indexOf(marker);
  if (start === -1) {
    throw new Error('Could not find `const translations = ` in script.js');
  }

  const braceStart = source.indexOf('{', start);
  if (braceStart === -1) {
    throw new Error('Could not find opening brace for translations object');
  }

  let depth = 0;
  let inSingle = false;
  let inDouble = false;
  let inTemplate = false;
  let escaped = false;

  for (let i = braceStart; i < source.length; i += 1) {
    const ch = source[i];

    if (escaped) {
      escaped = false;
      continue;
    }

    if ((inSingle || inDouble || inTemplate) && ch === '\\') {
      escaped = true;
      continue;
    }

    if (inSingle) {
      if (ch === "'") inSingle = false;
      continue;
    }
    if (inDouble) {
      if (ch === '"') inDouble = false;
      continue;
    }
    if (inTemplate) {
      if (ch === '`') inTemplate = false;
      continue;
    }

    if (ch === "'") {
      inSingle = true;
      continue;
    }
    if (ch === '"') {
      inDouble = true;
      continue;
    }
    if (ch === '`') {
      inTemplate = true;
      continue;
    }

    if (ch === '{') depth += 1;
    else if (ch === '}') {
      depth -= 1;
      if (depth === 0) {
        const objectLiteral = source.slice(braceStart, i + 1);
        return vm.runInNewContext(`(${objectLiteral})`, Object.create(null), {
          timeout: 5000,
        });
      }
    }
  }

  throw new Error('Unbalanced braces while extracting translations object');
}

function collectKeys(htmlPath) {
  if (!fs.existsSync(htmlPath)) {
    return [];
  }

  const html = fs.readFileSync(htmlPath, 'utf8');
  const keys = new Set();
  let match;
  ATTR_PATTERN.lastIndex = 0;
  while ((match = ATTR_PATTERN.exec(html)) !== null) {
    keys.add(match[1]);
  }
  return [...keys].map((key) => ({ key, file: path.basename(htmlPath) }));
}

function runSyntaxCheck() {
  const result = spawnSync(process.execPath, ['--check', SCRIPT_JS], {
    encoding: 'utf8',
  });
  if (result.status !== 0) {
    const detail = (result.stderr || result.stdout || '').trim();
    console.error('FAIL: node --check script.js\n' + detail);
    process.exit(result.status || 1);
  }
}

function main() {
  runSyntaxCheck();

  const source = fs.readFileSync(SCRIPT_JS, 'utf8');
  let translations;
  try {
    translations = extractTranslations(source);
  } catch (error) {
    console.error(`FAIL: could not load translations from script.js\n${error.message}`);
    process.exit(1);
  }

  if (!translations?.de || !translations?.en) {
    console.error('FAIL: translations.de and translations.en are both required');
    process.exit(1);
  }

  const entries = HTML_FILES.flatMap(collectKeys);
  if (entries.length === 0) {
    console.error('FAIL: no data-i18n attributes found in HTML files');
    process.exit(1);
  }

  const missing = [];
  const seen = new Set();

  for (const { key, file } of entries) {
    const dedupe = `${file}::${key}`;
    if (seen.has(dedupe)) continue;
    seen.add(dedupe);

    for (const lang of ['de', 'en']) {
      const value = getByPath(translations[lang], key);
      if (typeof value !== 'string') {
        missing.push({ file, key, lang, actual: value === undefined ? 'undefined' : typeof value });
      }
    }
  }

  if (missing.length > 0) {
    console.error(`FAIL: ${missing.length} missing or non-string i18n key(s):\n`);
    for (const item of missing) {
      console.error(`  [${item.lang}] ${item.file}: ${item.key} (${item.actual})`);
    }
    console.error('\nAdd matching string values under translations.de and translations.en in script.js.');
    process.exit(1);
  }

  const uniqueKeys = new Set(entries.map((e) => e.key));
  console.log(
    `OK: ${uniqueKeys.size} i18n key(s) resolve to strings in de and en ` +
      `(checked ${HTML_FILES.map((f) => path.basename(f)).join(', ')}).`
  );
  console.log('OK: node --check script.js');
}

main();
