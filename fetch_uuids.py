"""Look up bg3.wiki RootTemplate UUIDs for tier-list items that aren't in
items.json (and so render no spawn button).

The wiki infobox `| uuid = ...` field is the same UUID `TemplateAddTo` wants —
validated against items.json for several items. For pages with multiple uuids
(item variants), the FIRST is the base item. Items whose tier name names a
specific variant ("(Rare)", "(Act 3)", ...) are flagged for review, not guessed.

Output: review/wiki_uuids.json with {key: {name: {uuid, title, n_uuids, status}}}.
Run, eyeball the report, then merge confident matches into tierlists.json `uuids`.
"""
import json, re, subprocess, time, urllib.parse

UA = "Mozilla/5.0"
API = "https://bg3.wiki/w/api.php"
SPELL_CANON = [('armour','armor'),('defence','defense'),('colour','color'),
               ('jewellery','jewelry'),('sceptre','scepter'),('centre','center'),
               ('mould','mold'),('grey','gray')]


def canon(s):
    s = (s or '').lower()
    for a, b in SPELL_CANON:
        s = s.replace(a, b)
    s = re.sub(r'[^a-z0-9 ]+', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return re.sub(r'^the ', '', s)


def loose(s):
    toks = [t for t in canon(s).split() if t != 'armor']
    d = [t for t in toks if t.isdigit()]
    r = [t for t in toks if not t.isdigit()]
    return ' '.join(r + d)


def build_indexes(items):
    LINK = ['potion of ', 'elixir of ', 'scroll of ', 'oil of ', 'coating of ']
    name_index, lf, li = {}, {}, {}
    for i in items:
        k = canon(i['n'])
        name_index.setdefault(k, i)
        for p in LINK:
            if k.startswith(p):
                sh = k[len(p):].strip()
                if sh:
                    name_index.setdefault(sh, i)
                break
        lk = loose(i['n'])
        if lk:
            if lk in lf:
                if lf[lk] != i['n']:
                    li.pop(lk, None)
            else:
                lf[lk] = i['n']
                li[lk] = i
    return name_index, li


def candidate_titles(name):
    """Wiki page-title guesses for a tier-list item name."""
    cands = []
    base = name
    # strip a leading "(Rare) " or trailing " (Act 3)" / " (RRR)" qualifier
    stripped = re.sub(r'^\([^)]*\)\s*', '', base)
    stripped = re.sub(r'\s*\([^)]*\)\s*$', '', stripped).strip()
    variants = [base]
    if stripped != base:
        variants.append(stripped)
    out = []
    for v in variants:
        out.append(v)
        m = re.match(r'^\+(\d+)\s+(.*)$', v)      # "+1 Mace" -> "Mace +1"
        if m:
            out.append(f"{m.group(2)} +{m.group(1)}")
    # de-dup, preserve order
    seen = set()
    for t in out:
        if t not in seen:
            seen.add(t)
            cands.append(t)
    return cands


def fetch_wikitext(title):
    url = (API + "?action=parse&prop=wikitext&format=json&redirects=1&page="
           + urllib.parse.quote(title.replace(' ', '_')))
    out = subprocess.run(["curl", "-sS", "--max-time", "25", "-A", UA, url],
                         capture_output=True, text=True).stdout
    try:
        data = json.loads(out)
        return data['parse']['wikitext']['*'], data['parse']['title']
    except Exception:
        return None, None


def main():
    items = json.load(open('src/data/items.json'))
    tls = json.load(open('src/data/tierlists.json'))
    name_index, loose_index = build_indexes(items)
    refonly = {'skills', 'cantrips'}

    report = {}
    for tl in tls:
        key = tl['key']
        if key in refonly:
            continue
        uuids = tl.get('uuids', {})
        for name in tl['ratings']:
            if name in uuids or canon(name) in name_index or loose(name) in loose_index:
                continue
            # genuinely missing -> look up on the wiki
            wt, title = None, None
            for cand in candidate_titles(name):
                wt, title = fetch_wikitext(cand)
                time.sleep(0.25)
                if wt:
                    break
            entry = {"uuid": None, "title": title, "n_uuids": 0, "status": "not_found"}
            if wt:
                found = re.findall(r'\|\s*uuid\s*=\s*([0-9a-fA-F-]{36})', wt)
                entry["n_uuids"] = len(found)
                has_variant_qualifier = bool(re.search(r'\((rare|act\s*\d|rrr|legendary|very rare)\)',
                                                       name, re.I))
                if found and not has_variant_qualifier:
                    entry["uuid"] = found[0]
                    entry["status"] = "ok" if len(found) == 1 else "ok_first_of_many"
                elif found:
                    entry["status"] = "needs_review_variant"
                else:
                    entry["status"] = "page_no_uuid"
            report.setdefault(key, {})[name] = entry
            print(f"[{entry['status']:20}] {key}/{name}  -> {entry['uuid']} "
                  f"(title={title}, n={entry['n_uuids']})")

    json.dump(report, open('review/wiki_uuids.json', 'w'), ensure_ascii=False, indent=2)
    # summary
    from collections import Counter
    c = Counter(e['status'] for k in report for e in report[k].values())
    print("\n=== summary ===")
    for s, n in c.most_common():
        print(f"{s}: {n}")


if __name__ == "__main__":
    main()
