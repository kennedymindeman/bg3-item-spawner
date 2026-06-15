"""Populate `acts` (first-appears-in act) on the equipment tier lists from
Cephalopocalypse's item spreadsheet (saved as review/sheet_act{1,2,3}.csv,
each tab = one act). Items not found in the sheet (generic +N / base gear that
has no fixed act) are left without an act and show only under 'All acts'."""
import csv, re, json, unicodedata

SHEETS = {"Act 1": "review/sheet_act1.csv",
          "Act 2": "review/sheet_act2.csv",
          "Act 3": "review/sheet_act3.csv"}
PATH = "src/data/tierlists.json"
EQUIP = ["amulets", "rings", "helmets", "gloves", "boots", "cloaks", "shields",
         "staves", "light_armor", "medium_armor", "heavy_armor", "cloth_armor",
         "finesse_weapons", "one_handed_weapons", "two_handed_weapons",
         "versatile_weapons", "polearms", "ranged_weapons", "simple_weapons"]


def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = s.lower().replace("&", " and ")
    s = re.sub(r"\((?:rare|act\s*\d|epic|legendary|common|uncommon)\)", "", s)
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]+", " ", s)).strip()


# name -> earliest act
name2act, sheet_names = {}, []
for act, path in SHEETS.items():
    for r in csv.DictReader(open(path)):
        nm = norm(r.get("Name", ""))
        if not nm:
            continue
        sheet_names.append((nm, act))
        name2act.setdefault(nm, act)


def lookup(name, wname):
    for cand in (norm(wname), norm(name)):
        if cand in name2act:
            return name2act[cand]
    # substring fallback for minor wording diffs (length-guarded to avoid noise)
    cand = norm(wname) or norm(name)
    if len(cand) >= 12:
        for sn, act in sheet_names:
            if len(sn) >= 12 and (cand in sn or sn in cand):
                return act
    return None


data = json.load(open(PATH))
total = matched = 0
for x in data:
    if x["key"] not in EQUIP:
        continue
    wn = x.get("wnames", {}) or {}
    acts = dict(x.get("acts", {}))  # preserve existing hand-curated acts
    for name in x["ratings"]:
        total += 1
        if name in acts:
            matched += 1
            continue
        a = lookup(name, wn.get(name, name))
        if a:
            acts[name] = a
            matched += 1
    if acts:
        x["acts"] = acts

with open(PATH, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print(f"populated acts on {sum(1 for x in data if x['key'] in EQUIP and x.get('acts'))} lists; "
      f"matched {matched}/{total} equipment items")
