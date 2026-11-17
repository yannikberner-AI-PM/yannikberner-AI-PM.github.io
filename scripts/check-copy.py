#!/usr/bin/env python3
"""Static copy, maturity and German fallback regressions. No browser dependency."""
import json
import re
import subprocess
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.joinpath('script.js').read_text()
probe = "const fs=require('fs'),vm=require('vm');const s=fs.readFileSync('script.js','utf8');console.log(JSON.stringify(vm.runInNewContext(s.slice(0,s.indexOf('let activeLanguage'))+';translations',{document:{addEventListener(){}}})));"
T = json.loads(subprocess.check_output(['node', '-e', probe], cwd=ROOT, text=True))


def flatten(value, prefix=''):
    if isinstance(value, dict):
        return {k: v for name, item in value.items() for k, v in flatten(item, prefix + name + '.').items()}
    if isinstance(value, list):
        return {k: v for n, item in enumerate(value) for k, v in flatten(item, prefix + str(n) + '.').items()}
    return {prefix.rstrip('.'): value}


DE, EN = flatten(T['de']), flatten(T['en'])
assert DE.keys() == EN.keys(), 'DE/EN translation shape differs'


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.active = None
        self.text = ''
        self.count = 0
        self.ids = []
        self.links = []
        self.meta = {}

    def handle_starttag(self, tag, attrs):
        a = {key: value or '' for key, value in attrs}
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'meta':
            self.meta[a.get('name', a.get('property'))] = a.get('content')
        if tag == 'a':
            self.links.append(a)
        for attr, keyattr in [('alt', 'data-i18n-alt'), ('aria-label', 'data-i18n-aria')]:
            if keyattr in a:
                assert a.get(attr) == DE[a[keyattr]], (keyattr, a[keyattr])
                self.count += 1
        if 'data-i18n' in a:
            assert self.active is None, 'Nested translation element'
            self.active = (tag, a['data-i18n'])
            self.text = ''

    def handle_data(self, data):
        if self.active:
            self.text += data

    def handle_endtag(self, tag):
        if self.active and self.active[0] == tag:
            key = self.active[1]
            assert self.text.strip() == DE[key], (key, self.text, DE[key])
            self.count += 1
            self.active = None


page = Page()
page.feed(ROOT.joinpath('index.html').read_text())
assert len(page.ids) == len(set(page.ids)), 'Duplicate ID'
for name, key in [('description', 'metaDescription'), ('og:title', 'documentTitle'), ('twitter:title', 'documentTitle'), ('og:description', 'socialDescription'), ('twitter:description', 'socialDescription'), ('og:image:alt', 'socialImageAlt'), ('twitter:image:alt', 'socialImageAlt')]:
    assert page.meta[name] == T['de'][key], name
links = [link for link in page.links if '-showcase' in link.get('href', '')]
assert len(links) == 4, 'Expected the four non-energy showcases'
assert not any('energyLab.cta' in link.get('data-i18n', '') or 'energie-labor-showcase' in link.get('href', '') for link in page.links), 'Energie-Labor showcase CTA must be absent'
for link in links:
    assert link.get('target') == '_blank'
    assert {'noopener', 'noreferrer'} <= set(link.get('rel', '').split())
    assert link['data-url-de'].endswith('/blob/main/README.de.md')
    assert 'aria-label' in link
for link in page.links:
    if link.get('href', '').startswith('#'):
        assert link['href'][1:] in page.ids, link['href']
for lang in ['de', 'en']:
    p = T[lang]['projects']
    assert 'energyLab' in p
    assert ('geplant' if lang == 'de' else 'planned') in p['visualWorkspace']['result']
    assert ('ohne Erinnerungsfunktion' if lang == 'de' else 'without reminder functionality') in p['stakeholderIntelligence']['narrative']['tradeoffs']
    assert ('regelbasiert' if lang == 'de' else 'rule-based') in p['predictiveMentoring']['approachText']
    assert ('stehen aus' if lang == 'de' else 'outstanding') in p['predictiveMentoring']['result']
    assert ('simuliert' if lang == 'de' else 'simulated') in p['cyberSecurityConnector']['result']
    assert ('Compliance' if lang == 'de' else 'compliance') in p['cyberSecurityConnector']['result']
    assert ('reproduzierbar' if lang == 'de' else 'reproducible') in p['research']
public_de = '\n'.join(v for k, v in DE.items() if not k.startswith('privacy.') and not k.endswith('periodLocation'))
assert not re.search(r'\b(nicht|aber)\b|[—–]', public_de, re.I), 'German public copy voice regression'
assert not re.search(r'smart.metering|iMSys|Messstellenbetrieb', ROOT.joinpath('index.html').read_text(), re.I), 'Unsupported expertise'
print(f'OK: {page.count} German text/alt/aria fallbacks; DE/EN key parity; metadata; four showcases; no Energie-Labor CTA; anchors; maturity limits; German voice.')
