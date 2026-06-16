"""Set the exact `video_url` (and real `video` title) on each tier list by
matching its primary source transcript title to Cephalopocalypse's channel
uploads (resolved with yt-dlp). Mapping captured in /tmp/key2vid.json +
transcript filenames."""
import os, re, json, unicodedata

PRIM = {
    'arrows': '030', 'barrels': '032', 'boots': '046', 'cantrips': '078', 'cloaks': '042',
    'cloth_armor': '036', 'elixirs': '027', 'finesse_weapons': '060', 'gloves': '043',
    'grenades': '029', 'helmets': '047', 'light_armor': '037', 'medium_armor': '038',
    'one_handed_weapons': '066', 'poisons_oils': '031', 'polearms': '064', 'potions': '028',
    'ranged_weapons': '059', 'rings': '053', 'shields': '041', 'simple_weapons': '063',
    'skills': '001', 'staves': '062', 'two_handed_weapons': '065', 'versatile_weapons': '067',
    'amulets': '050', 'heavy_armor': '039', 'feats': '093', 'classes': '015', 'subclasses': '016',
    'illithid_powers': '034', 'multiclasses': '073', 'spells_level_1': '079',
    'spells_level_2': '081', 'spells_level_3': '083', 'spells_level_4': '085',
    'spells_level_5': '087', 'spells_level_6': '088',
}
TD = "transcripts"
PATH = "src/data/tierlists.json"


def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", s)).strip()


num2title = {}
for f in os.listdir(TD):
    m = re.match(r"(\d{3})-(.*)\.txt$", f)
    if m:
        num2title[m.group(1)] = m.group(2)

chan = {}
for line in open("/tmp/chan.txt"):
    if "|" not in line:
        continue
    vid, title = line.rstrip("\n").split("|", 1)
    chan[norm(title)] = vid

data = json.load(open(PATH))
n = 0
for x in data:
    num = PRIM.get(x["key"])
    if not num:
        continue
    title = num2title.get(num)
    vid = chan.get(norm(title or ""))
    if vid:
        x["video"] = title
        x["video_url"] = "https://www.youtube.com/watch?v=" + vid
        n += 1
assert n == len(PRIM), f"only matched {n}/{len(PRIM)}"
with open(PATH, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print(f"set video_url on {n} lists")
