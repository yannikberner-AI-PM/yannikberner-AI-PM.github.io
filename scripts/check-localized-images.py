"""Safari regression check for the portfolio's DE/EN project images.
Usage: python3 scripts/check-localized-images.py [http://127.0.0.1:4188/]
Requires Safari's existing Allow JavaScript from Apple Events permission.
"""
import json
import subprocess
import sys
import time
import urllib.request

base = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:4188/'


def apple(script):
    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, check=True)
    return result.stdout.strip()


def js(script):
    return apple('tell application "Safari" to do JavaScript ' + json.dumps(script) + ' in current tab of front window')


def state():
    return json.loads(js('''JSON.stringify((()=>{
      const img=document.querySelector('#energie-labor .energy-lab-media img');
      const link=img.closest('a');
      return {lang:document.documentElement.lang,src:img.getAttribute('src'),
        href:link.getAttribute('href'),loaded:img.complete&&img.naturalWidth>0,
        width:img.naturalWidth,height:img.naturalHeight,alt:img.alt,
        caption:document.querySelector('#energie-labor figcaption').textContent,
        urlLang:new URLSearchParams(location.search).get('lang'),
        energyCTA:document.querySelectorAll('#energie-labor a[href*="github.com"],a[data-i18n="projects.energyLab.cta"]').length,
        showcases:document.querySelectorAll('a[href*="-showcase"]').length,
        overflow:document.documentElement.scrollWidth>innerWidth,viewport:innerWidth,
        hidden:getComputedStyle(img).display==='none',
        cropped:img.getBoundingClientRect().bottom>img.closest('.media-shell').getBoundingClientRect().bottom};
    })())'''))


def expect(lang):
    value = state()
    for _ in range(50):
        value = state()
        if value['loaded'] and value['lang'] == lang and value['src'].endswith('-'+lang+'.webp') and value['width'] == 1400:
            break
        time.sleep(.1)
    assert value['loaded'] and value['lang'] == lang and value['src'].endswith('-'+lang+'.webp'), value
    assert value['src'] == value['href'], value
    assert value['urlLang'] == lang, value
    assert value['energyCTA'] == 0 and value['showcases'] == 4, value
    assert not value['overflow'] and not value['hidden'] and not value['cropped'], value
    assert value['width'] == 1400 and value['height'] == 1294, value
    assert ('Beispieldaten' if lang == 'de' else 'sample data') in value['alt'], value
    assert ('Vergrößern' if lang == 'de' else 'closer look') in value['caption'], value
    print(json.dumps(value, ensure_ascii=False))
    return value


for lang in ['de', 'en']:
    url = base+'?lang='+lang+'#energie-labor'
    assert urllib.request.urlopen(url).status == 200
    apple('tell application "Safari" to make new document with properties {URL:'+json.dumps(url)+'}')
    time.sleep(.7)
    expect(lang)
    other = 'en' if lang == 'de' else 'de'
    js('document.querySelector(\'.lang-button[data-lang="'+other+'"]\').click()')
    expect(other)
    js('document.querySelector(\'.lang-button[data-lang="'+lang+'"]\').click()')
    expect(lang)

for width in [1440, 768, 390, 360]:
    apple('tell application "Safari" to set bounds of front window to {0,33,'+str(width)+',950}')
    time.sleep(.2)
    expect('en')

js('document.querySelector("#energie-labor .energy-lab-media a").focus()')
assert js('document.activeElement.matches("#energie-labor .energy-lab-media a")') == 'true'
apple('tell application "Safari" to set bounds of front window to {0,33,1512,982}')
print('PASS: DE/EN deep links, live language switches, images, captions, full-size links, focus and responsive layout.')
