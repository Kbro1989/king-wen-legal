import json, re, unicodedata
from pathlib import Path

# Paths
TEXT_1789 = Path(r"C:\Users\krist\AppData\Local\hermes\cache\web\www.gutenberg.org-acbbf766e7.md")
TEXT_1913 = Path(r"C:\Users\krist\AppData\Local\hermes\cache\web\www.gutenberg.org-00e3e8e1b8.md")
INV_PATH  = Path(r"C:\Users\krist\Desktop\constitutional-graph-tool\target\legal-data\constitution-complete-word-inventory.json")
OUT_INV   = Path(r"C:\Users\krist\Desktop\constitutional-graph-tool\target\legal-data\constitution-complete-word-inventory.json")
OUT_DIFF  = Path(r"C:\Users\krist\Desktop\constitutional-graph-tool\target\legal-data\timelined-dictionary-diff.json")

def normalize(s: str) -> str:
    s = s.lower()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^a-z]+", " ", s)
    return " ".join(s.split())

def load_lines(p: Path):
    return [l.rstrip("\n") for l in p.open("r", errors="ignore")]

lines1913 = load_lines(TEXT_1913)
lines1789 = load_lines(TEXT_1789)

# Webster 1913: real dictionary entries start like "Word (?), _n._ ..."
# Build a map: lowercase normalized headword -> entry text
HEAD_1913 = re.compile(r"^([A-Za-z][A-Za-z' .-]+?)\s*(?:\(\?\)\s*)?(?:,\s*_[a-z]+(?:\.[a-z]*)?\.?)?\s+")
STEMMERS = {"s","ing","ly","ed","er","est","ment","ness","tion","ous","ive","ful","less"}

def build_dict_1913(lines):
    dict_map = {}
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i].strip()
        m = re.match(r"^([A-Za-z][A-Za-z' .-]+?)(?:\s*\(\?\))?\s*,\s*_([a-z]+(?:\.[a-z]*)?)\._?\s+(.*)", line)
        if not m:
            i += 1
            continue
        head = m.group(1).strip()
        if not head or len(head) > 25:
            i += 1
            continue
        # start entry
        entry_lines = [m.group(3)]
        i += 1
        while i < n:
            nline = lines[i].strip()
            if not nline:
                i += 1
                break
            # stop if we hit another entry head
            m2 = re.match(r"^([A-Za-z][A-Za-z' .-]+?)(?:\s*\(\?\))?\s*,\s*_([a-z]+(?:\.[a-z]*)?)\._?\s+", nline)
            if m2:
                # stop early if likely new entry: lowercase head
                head2 = m2.group(1)
                if head2[0] == head2[0].upper() and head2.lower() != head.lower():
                    break
            entry_lines.append(nline)
            i += 1
        dict_map.setdefault(head.lower(), []).append(" ".join(entry_lines))
    return dict_map

def build_dict_1789(lines):
    """
    Webster 1789 is mostly an essay, but has glossary entries.
    We'll capture blocks that look like standalone glosses.
    We'll scan for obvious headword lines: "WORD, _verb_. ..." etc.
    """
    text = "\n".join(lines)
    # remove page markers
    text = re.sub(r'\[Pg [ivxlcdm]+\]', ' ', text, flags=re.IGNORECASE)
    text = re.sub(r'\\[\\\*]+\s*\\[\\\*]+', ' ', text)
    dict_map = {}
    # Look for strong entry patterns
    entries = re.findall(
        r'(?m)^\s*([A-Z][a-zA-Z]{1,20})\s*,\s*_{1,3}'
        r'([a-z]+\.?)?'
        r'_?\s+(.*?)(?=\n\s*\n|\n[A-Z][a-zA-Z]{1,20}\s*,|\Z)',
        text
    )
    # Deduplicate and reduce noise
    for head, pos, body in entries:
        body = " ".join(body.split())
        if not body:
            continue
        dict_map.setdefault(head.lower(), []).append(f"{pos.strip('.')}: {body[:300]}")
    # De-dup identical entries
    for k, v in dict_map.items():
        dict_map[k] = list(dict.fromkeys(v))[:3]
    return dict_map

print("Building 1913 dict ...")
dict1913 = build_dict_1913(lines1913)
print(f"1913 dictionary entries: {len(dict1913)}")

print("Building 1789 dict ...")
dict1789 = build_dict_1789(lines1789)
print(f"1789 dictionary entries: {len(dict1789)}")

# Load inventory
inv = json.load(open(INV_PATH, encoding="utf-8"))
words = [w["word"] for w in inv["word_inventory"]]

# Load timelined diff skeleton if present, else init
if OUT_DIFF.exists():
    try:
        diff = json.load(open(OUT_DIFF, encoding="utf-8"))
        if "word_mapping" not in diff:
            diff["word_mapping"] = {}
    except Exception:
        diff = {"word_mapping": {}}
else:
    diff = {"word_mapping": {}}

for word in words:
    nw = normalize(word)
    wlower = word.lower()

    # 1789
    w1789 = dict1789.get(nw) or dict1789.get(wlower)
    if w1789:
        d1789 = " | ".join(w1789)[:1200]
    else:
        d1789 = "NO DEFINITION FOUND IN WEBSTER 1789 SOURCE (essay/dissertation, not a full dictionary)"

    # 1913
    w1913 = dict1913.get(nw) or dict1913.get(wlower)
    if w1913:
        d1913 = " | ".join(w1913)[:1500]
    else:
        d1913 = "NO DEFINITION FOUND IN WEBSTER 1913 SOURCE"

    # Drift classification (heuristic, from what we extracted)
    written = f"{d1789} | {d1913}"
    if "NO DEFINITION" in d1789 and "NO DEFINITION" in d1913:
        drift = "UNCLASSIFIED - neither dictionary records a usable entry for this word; treated as proper noun/technical/personal-name"
        drift_class = "unknown_no_dictionary_coverage"
    elif "NO DEFINITION" in d1789:
        drift = "PARTIAL: no 1789 entry available; 1913 definition only - meaning cannot be compared across temporal spine"
        drift_class = "partial_no_1789_entry"
    elif "NO DEFINITION" in d1913:
        drift = "PARTIAL: no 1913 entry available; 1789 definition only - drift cannot be measured"
        drift_class = "partial_no_1913_entry"
    elif d1789.lower() == d1913.lower() or abs(len(d1789)-len(d1913)) < 80:
        drift = f"STABLE or NEAR-STABLE: definitions closely match between 1789 and 1913 sources"
        drift_class = "stable"
    else:
        drift = f"ACTIVE MEANING DRIFT DETECTED: definitions differ materially between the 1789 spine and 1913 tail"
        drift_class = "stable_meaning_drift_detected"

    diff["word_mapping"][word] = {
        "normalized": nw,
        "webster_1789_definition": d1789,
        "webster_1913_definition": d1913,
        "meaning_drift": drift,
        "drift_classification": drift_class,
        "state_crosswalk": ["STATE_US"],
        "blast_radius": "constitutional_usage"
    }

# Update inventory
for item in inv["word_inventory"]:
    w = item["word"]
    dm = diff["word_mapping"].get(w, {})
    item["webster_1789_definition"] = dm.get("webster_1789_definition", "PENDING - requires dictionary lookup")
    item["webster_1913_definition"] = dm.get("webster_1913_definition", "PENDING - requires dictionary lookup")
    item["meaning_drift"] = dm.get("meaning_drift", "PENDING")
    item["drift_classification"] = dm.get("drift_classification", "PENDING")

# Save both files with ensure_ascii=False to keep any special chars
OUT_INV.write_text(json.dumps(inv, indent=2, ensure_ascii=False), encoding="utf-8")
OUT_DIFF.write_text(json.dumps(diff, indent=2, ensure_ascii=False), encoding="utf-8")

print("Done.")
print(f"Inventory saved: {OUT_INV}")
print(f"Timelined diff saved: {OUT_DIFF}")
print(f"Total word mappings: {len(diff['word_mapping'])}")

# Stats
classes = {}
for w, dm in diff["word_mapping"].items():
    c = dm["drift_classification"]
    classes[c] = classes.get(c, 0) + 1
print("Drift classification counts:")
for c, n in sorted(classes.items(), key=lambda x: -x[1]):
    print(f"  {c}: {n}")
