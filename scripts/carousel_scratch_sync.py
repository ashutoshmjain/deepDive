"""One-time scratch routine: correct the 248/249/250 carousels from
published state (deepdive-spec-carousel-scratch-sync.md).

Per episode (248, 249, 250, in order):
  1. published set = clips with a local mp4 AND a live-200 mp4;
     plan `published` flags are cross-checked and every
     disagreement is reported (mp4-exists is the tiebreaker --
     a card with a dead video is never allowed).
  2. rebuilds the carousel in src/<ep>.md to exactly that set
     (sorted by clip number, titles from the plan, byte-exact
     card format verified against the file's own first card).
  3. prints before/after counts, removed/added lists, disagreements.

Idempotent: a second run with the same published state changes
nothing and reports "already correct" per episode.
Not wired into any flow; run by hand.
"""
import io
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'src')
CLIPS = os.path.join(SRC, 'ddma', 'docs', 'episodes')
LIVE = ('https://deepdive.shutri.com/ddma/docs/episodes/'
        '%d/clips/%d-%d.mp4')
EPISODES = (248, 249, 250)

CARD_OPEN = ('  <div style="flex: 0 0 60%; scroll-snap-align: center; '
             'position: relative; border-radius: 12px; overflow: hidden; '
             'background: #000; aspect-ratio: 1/1; display: flex; '
             'flex-direction: column; '
             'box-shadow: 0 4px 15px rgba(0,0,0,0.3);">')
VIDEO = ('    <video src="ddma/docs/episodes/{ep}/clips/{ep}-{n}.mp4" '
         'style="width: 100%; height: 85%; object-fit: contain;" '
         'playsinline loop preload="auto" muted autoplay></video>')
LABEL = ('    <div style="height: 15%; background: #1a1a1a; color: #ccc; '
         'display: flex; align-items: center; justify-content: center; '
         'font-family: monospace; font-size: 12px; '
         'border-top: 1px solid #333;">{ep}-{n} {title}</div>')
BUTTON = ('    <button class="vid-toggle" '
          'onclick="window.oph_play_toggle(this)" style="position: absolute; '
          'top: 10px; right: 10px; background: rgba(0,0,0,0.8); '
          'color: white; border: 2px solid white; border-radius: 50%; '
          'width: 45px; height: 45px; cursor: pointer; font-size: 22px; '
          'z-index: 100;">\U0001f507</button>')
CARD_CLOSE = '  </div>'
NL = '\r\n'


def card(ep, n, title):
    return NL.join([CARD_OPEN, VIDEO.format(ep=ep, n=n),
                    LABEL.format(ep=ep, n=n, title=title),
                    BUTTON, CARD_CLOSE])


def live_head_ok(ep, n):
    try:
        req = urllib.request.Request(LIVE % (ep, ep, n), method='HEAD')
        return urllib.request.urlopen(req, timeout=30).status == 200
    except Exception:
        return False


def parse_carousel(text, ep):
    m = re.search(r'(<div class="video-carousel-container"[^>]*>'
                  r'\r\n)(.*?)(\r\n</div>\r\n\r\n<center>)',
                  text, re.DOTALL)
    if not m:
        return None
    cards = re.findall(
        r'<video src="ddma/docs/episodes/%d/clips/%d-(\d+)\.mp4"'
        % (ep, ep), m.group(2))
    labels = re.findall(r'>%d-(\d+) (.*?)</div>' % ep, m.group(2))
    return {'head': m.group(1), 'body': m.group(2),
            'tail': m.group(3),
            'nums': [int(n) for n in cards],
            'labels': {int(n): lab for n, lab in labels}}


def sync_episode(ep):
    plan = json.load(io.open(
        os.path.join(ROOT, 'ddma', 'projects', 'episode_%d' % ep,
                     'plan.json'),
        encoding='utf-8-sig'))
    info = {c.get('num'): c for c in plan}
    nums = sorted(info)
    flags = {n for n in nums if info[n].get('published')}
    local = {n for n in nums if os.path.isfile(
        os.path.join(CLIPS, str(ep), 'clips', '%d-%d.mp4' % (ep, n)))}
    live = {n for n in nums if live_head_ok(ep, n)}
    # Include rule: mp4 must exist locally AND live (dead video never
    # allowed). Flags are the cross-check; mp4-exists tiebreaks.
    keep = sorted(local & live)
    disag = []
    for n in nums:
        if info[n].get('published') and n not in keep:
            disag.append('%d-%d flagged published but mp4 missing '
                         '(local=%s live=%s)' % (
                             ep, n, n in local, n in live))
        if n in keep and n not in flags:
            disag.append('%d-%d kept on mp4-exists tiebreak '
                         '(no published flag)' % (ep, n))
        if n in local and n not in live:
            disag.append('%d-%d local mp4 exists but live 404' % (ep, n))
        if n in live and n not in local:
            disag.append('%d-%d live 200 but no local mp4' % (ep, n))

    path = os.path.join(SRC, '%d.md' % ep)
    text = io.open(path, encoding='utf-8', newline='').read()
    assert text.count('\n') == text.count('\r\n'), 'bare LF in %s' % path
    parsed = parse_carousel(text, ep)
    assert parsed is not None, 'no carousel block in %s' % path
    before = parsed['nums']
    # Verify our template against the file's own first card.
    first = before[0]
    expect_first = card(ep, first,
                        parsed['labels'][first])
    assert parsed['body'].lstrip('\r\n').startswith(expect_first), \
        'card format drift in %s' % path
    # Titles for kept cards must equal the plan (no silent alteration).
    for n in keep:
        if n in parsed['labels']:
            assert parsed['labels'][n] == info[n].get('title'), (
                ep, n, parsed['labels'][n])
    titles = {n: info[n].get('title') for n in keep}
    assert all(t for t in titles.values()), (ep, titles)
    new_body = (NL.join(card(ep, n, titles[n]) for n in keep)
                if keep else '')
    if before == keep and parsed['body'] == new_body:
        print('ep %d: already correct (%d cards: %s)' % (
            ep, len(keep), keep))
        for d in disag:
            print('  disagreement: %s' % d)
        return {'ep': ep, 'before': before, 'after': keep,
                'removed': [], 'added': [], 'disag': disag,
                'changed': False}
    new_text = text.replace(parsed['head'] + parsed['body'] + parsed['tail'],
                            parsed['head'] + new_body + parsed['tail'], 1)
    io.open(path, 'w', encoding='utf-8', newline='').write(new_text)
    removed = [n for n in before if n not in keep]
    added = [n for n in keep if n not in before]
    print('ep %d: %d -> %d cards; removed %s; added %s' % (
        ep, len(before), len(keep), removed, added))
    for d in disag:
        print('  disagreement: %s' % d)
    return {'ep': ep, 'before': before, 'after': keep,
            'removed': removed, 'added': added, 'disag': disag,
            'changed': True}


def main():
    results = [sync_episode(ep) for ep in EPISODES]
    changed = [r['ep'] for r in results if r['changed']]
    print('changed episodes:', changed if changed else 'none')
    return 0 if True else 1


if __name__ == '__main__':
    sys.exit(main())
