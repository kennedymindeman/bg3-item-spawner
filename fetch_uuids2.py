"""Second pass: resolve the items fetch_uuids.py couldn't, using bg3.wiki's
search API to find the real page title, then extracting the first `| uuid =`.

Writes results back into review/wiki_uuids.json (upgrading statuses). Variant-
qualified names ("(Rare)", "(Act 3)") and generic category placeholders are
left flagged rather than guessed.
"""
import json, re, subprocess, time, urllib.parse

UA = "Mozilla/5.0"
API = "https://bg3.wiki/w/api.php"

# Confirmed exact titles (already verified by hand) and known renames.
OVERRIDES = {
    "Hoarfrost Shoes": "Hoarfrost Boots",
    "Sleeping Potion": "Potion of Sleep",
    "Render of Body and Mind": "Render of Mind and Body",
    "Greater Arcane Cultivation": "Elixir of Greater Arcane Cultivation",
    "Superior Arcane Cultivation": "Elixir of Superior Arcane Cultivation",
    "Supreme Arcane Cultivation": "Elixir of Supreme Arcane Cultivation",
}
# Generic category placeholders / family entries — not a single spawnable item.
SKIP = {"Ring", "Shield", "Amulet (non-magical)", "Hat", "Resistance"}


def curl(url):
    return subprocess.run(["curl", "-sS", "--max-time", "25", "-A", UA, url],
                          capture_output=True, text=True).stdout


def wikitext(title):
    url = (API + "?action=parse&prop=wikitext&format=json&redirects=1&page="
           + urllib.parse.quote(title.replace(' ', '_')))
    try:
        d = json.loads(curl(url))
        return d['parse']['wikitext']['*'], d['parse']['title']
    except Exception:
        return None, None


def search_title(term):
    url = (API + "?action=query&list=search&format=json&srlimit=5&srsearch="
           + urllib.parse.quote(term))
    try:
        hits = json.loads(curl(url))['query']['search']
    except Exception:
        return []
    return [h['title'] for h in hits]


def first_uuid(wt):
    return re.findall(r'\|\s*uuid\s*=\s*([0-9a-fA-F-]{36})', wt)


def main():
    report = json.load(open('review/wiki_uuids.json'))
    todo = [(k, n) for k in report for n, e in report[k].items()
            if e['status'] in ('not_found', 'page_no_uuid', 'needs_review_variant')]

    for key, name in todo:
        if name in SKIP:
            report[key][name]['status'] = 'skip_category'
            print(f"[skip_category      ] {key}/{name}")
            continue
        variant = bool(re.search(r'\((rare|act\s*\d|rrr|legendary|very rare)\)', name, re.I))
        # candidate titles: override, then the plain name, then search hits
        cands = []
        if name in OVERRIDES:
            cands.append(OVERRIDES[name])
        clean = re.sub(r'^\([^)]*\)\s*', '', name)
        clean = re.sub(r'\s*\([^)]*\)\s*$', '', clean).strip()
        for t in search_title(clean):
            cands.append(t)
            time.sleep(0)  # search already one call
        time.sleep(0.2)

        chosen = None
        for cand in cands:
            wt, title = wikitext(cand)
            time.sleep(0.2)
            if not wt:
                continue
            us = first_uuid(wt)
            if not us:
                continue
            # avoid obviously-wrong category/disambig titles
            if title.lower() in {'rings', 'amulets', 'headwear', 'shields', 'resistances'}:
                continue
            if variant:
                report[key][name].update(status='needs_review_variant', title=title,
                                         n_uuids=len(us), uuid=None,
                                         all_uuids=us)
                chosen = 'flagged'
                print(f"[needs_review_variant] {key}/{name} -> page {title} has {len(us)} uuids")
                break
            report[key][name].update(uuid=us[0], title=title, n_uuids=len(us),
                                     status='ok' if len(us) == 1 else 'ok_first_of_many')
            chosen = us[0]
            print(f"[{'ok' if len(us)==1 else 'ok_first_of_many':17}] {key}/{name} -> {us[0]} ({title}, n={len(us)})")
            break
        if chosen is None:
            print(f"[STILL UNRESOLVED   ] {key}/{name}  (searched: {cands[:3]})")

    json.dump(report, open('review/wiki_uuids.json', 'w'), ensure_ascii=False, indent=2)
    from collections import Counter
    c = Counter(e['status'] for k in report for e in report[k].values())
    print("\n=== summary ===")
    for s, n in c.most_common():
        print(f"{s}: {n}")


if __name__ == "__main__":
    main()
