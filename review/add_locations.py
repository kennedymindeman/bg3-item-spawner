"""Populate `locations` (how/where to acquire) on the equipment tier lists from
Cephalopocalypse's item spreadsheet (review/sheet_act{1,2,3}.csv). Mirrors the
name-matching in add_acts.py, but captures the "Act Area" + "Location" columns
into a short acquisition string shown under each item's card. Items with no
fixed source (generic +N / base gear) are left without a location."""
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


def clean(s):
    # collapse whitespace/newlines from the spreadsheet cells
    return re.sub(r"\s+", " ", (s or "").replace("\n", " ")).strip()


def acquisition(area, location):
    area, location = clean(area), clean(location)
    if area and location:
        return f"{area} — {location}"
    return location or area


# name -> earliest-act acquisition string
name2loc, sheet_names = {}, []
for act, path in SHEETS.items():
    for r in csv.DictReader(open(path)):
        nm = norm(r.get("Name", ""))
        if not nm:
            continue
        loc = acquisition(r.get("Act Area", ""), r.get("Location", ""))
        if not loc:
            continue
        sheet_names.append((nm, loc))
        name2loc.setdefault(nm, loc)


def lookup(name, wname):
    for cand in (norm(wname), norm(name)):
        if cand in name2loc:
            return name2loc[cand]
    cand = norm(wname) or norm(name)
    if len(cand) >= 12:
        for sn, loc in sheet_names:
            if len(sn) >= 12 and (cand in sn or sn in cand):
                return loc
    return None


data = json.load(open(PATH))
total = matched = 0
for x in data:
    if x["key"] not in EQUIP:
        continue
    wn = x.get("wnames", {}) or {}
    locs = dict(x.get("locations", {}))  # preserve any hand-curated entries
    for name in x["ratings"]:
        total += 1
        if name in locs:
            matched += 1
            continue
        loc = lookup(name, wn.get(name, name))
        if loc:
            locs[name] = loc
            matched += 1
    if locs:
        x["locations"] = locs

with open(PATH, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print(f"populated locations on {sum(1 for x in data if x['key'] in EQUIP and x.get('locations'))} lists; "
      f"matched {matched}/{total} equipment items")
