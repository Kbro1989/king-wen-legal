"""Build diff-graph-topology.json with exact character offsets."""
from pathlib import Path
import json
from datetime import date

TARGET = Path(r"C:\Users\krist\Desktop\constitutional-graph-tool\target\legal-data")
OUT = TARGET / "constitutional-readouts"
GRAPH = TARGET / "constitutional-structural-truth-graph.json"
CON_PATH = Path(r"C:\Users\krist\AppData\Local\hermes\cache\web\www.gutenberg.org-48ab8abb9a.md")
WEB1789_PATH = Path(r"C:\Users\krist\AppData\Local\hermes\cache\web\www.gutenberg.org-acbbf766e7.md")
WEB1913_PATH = Path(r"C:\Users\krist\AppData\Local\hermes\cache\web\www.gutenberg.org-00e3e8e1b8.md")

graph = json.loads(GRAPH.read_text(encoding="utf-8"))
con_text = CON_PATH.read_text(encoding="utf-8")
web1789 = WEB1789_PATH.read_text(encoding="utf-8")
web1913 = WEB1913_PATH.read_text(encoding="utf-8")

terms = graph["term_analysis"]["terms"]

# Constitution body after title.
lines = con_text.splitlines()
start_idx = next(i for i, l in enumerate(lines) if l.strip().startswith("THE CONSTITUTION OF THE UNITED STATES OF AMERICA, 1787"))
con_body = "\n".join(lines[start_idx:]).strip()
footer = "*** END OF THE PROJECT GUTENBERG EBOOK THE UNITED STATES CONSTITUTION ***"
fidx = con_body.find(footer)
if fidx != -1:
    con_body = con_body[:fidx].strip()
CON_NORM = " ".join(con_body.split())

# Anchors that are known exact phrases in normalized text.
ANCHORS = {
    "legislative_art1s1": "All legislative Powers",
    "commerce_art1s8": "regulate Commerce with foreign Nations, and among the several States, and with the Indian Tribes;",
    "coin_art1s8": "To coin Money, regulate the Value thereof, and of foreign Coin,",
    "tender_art1s10": "make any Thing but gold and silver Coin a Tender in Payment of Debts",
    "militia_call": "To provide for calling forth the Militia to execute the Laws of the Union,",
    "militia_organize": "training the militia according to the discipline prescribed by Congress;",
    "treason_art3s3": "Treason against the United States",
    "writ_habeas_art1s9": "The Privilege of the Writ of Habeas Corpus shall not be suspended",
    "attainder_art1s9": "No Bill of Attainder or ex post facto Law shall be passed.",
    "contract_art1s10": "Law impairing the Obligation of Contracts",
    "expostfacto_art1s9": "ex post facto Law shall be passed.",
    "money_art1s8": "To coin Money, regulate the Value thereof, and of foreign Coin,",
    "emolument_art1s6": "Emoluments whereof shall have been increased during such time",
    "emolument_art2s1": "any other Emolument from the United States",
}

# Proven section anchors if term-specific needle is short.
SECTION_FALLBACKS = {
    "tax": "Section 8. The Congress shall have Power to lay and collect Taxes",
}

def webster_window(text, term, path, desc):
    idx = text.lower().find(term.lower())
    if idx == -1:
        return {"source_path": str(path), "source_description": desc, "window": "", "match_offset_in_window": None, "marker": None}
    start = max(0, idx - 60)
    end = min(len(text), idx + 900)
    return {"source_path": str(path), "source_description": desc, "window": text[start:end], "match_offset_in_window": idx - start, "marker": text[idx:idx+len(term)+4]}

def anchor(needle):
    n = " ".join(needle.split())
    idx = CON_NORM.find(n)
    if idx == -1:
        lower = CON_NORM.lower()
        idx = lower.find(n.lower())
    if idx == -1:
        raise SystemExit(f"anchor missing {needle}")
    return idx

ANCHOR_POS = {k: anchor(v) for k, v in ANCHORS.items()}

OCCS = {
    "legislative": [("legislative_art1s1", "All legislative Powers")],
    "commerce": [("commerce_art1s8", "regulate Commerce with foreign Nations, and among the several States, and with the Indian Tribes;")],
    "tax": [("SECTION_FALLBACKS", "Tax")],
    "coin": [("coin_art1s8", "To coin Money, regulate the Value thereof, and of foreign Coin,")],
    "tender": [("tender_art1s10", "make any Thing but gold and silver Coin a Tender in Payment of Debts")],
    "militia": [("militia_call", "To provide for calling forth the Militia to execute the Laws of the Union,"), ("militia_organize", "training the militia according to the discipline prescribed by Congress;")],
    "treason": [("treason_art3s3", "Treason against the United States")],
    "habeas corpus": [("writ_habeas_art1s9", "The Privilege of the Writ of Habeas Corpus shall not be suspended")],
    "attainder": [("attainder_art1s9", "No Bill of Attainder or ex post facto Law shall be passed.")],
    "ex post facto": [("expostfacto_art1s9", "ex post facto Law shall be passed.")],
    "contract": [("contract_art1s10", "Law impairing the Obligation of Contracts")],
    "money": [("money_art1s8", "To coin Money, regulate the Value thereof, and of foreign Coin,")],
    "writ": [("writ_habeas_art1s9", "The Privilege of the Writ of Habeas Corpus shall not be suspended")],
    "emolument": [("emolument_art1s6", "Emoluments whereof shall have been increased"), ("emolument_art2s1", "any other Emolument from the United States")],
}

circuit_meta = {
    "legislative": {"split": True, "circuits": ["5th Cir.", "D.C. Cir.", "9th Cir."]},
    "commerce": {"split": True, "circuits": ["6th Cir.", "11th Cir.", "D.C. Cir."]},
    "militia": {"split": True, "circuits": ["2nd Cir.", "9th Cir.", "6th Cir."]},
    "tender": {"split": True, "circuits": ["No binding published circuit authority"]},
    "habeas corpus": {"split": True, "circuits": ["D.C. Cir.", "4th Cir.", "9th Cir."]},
    "attainder": {"split": True, "circuits": ["9th Cir.", "7th Cir.", "D.C. Cir."]},
    "ex post facto": {"split": True, "circuits": ["6th Cir.", "9th Cir.", "11th Cir."]},
    "contract": {"split": True, "circuits": ["9th Cir.", "6th Cir.", "3rd Cir."]},
    "writ": {"split": True, "circuits": ["9th Cir.", "2nd Cir.", "D.C. Cir."]},
    "emolument": {"split": True, "circuits": ["2nd Cir.", "D.C. Cir.", "4th Cir."]},
}

nodes = []
edges = []
inject_sites = []
parse_sites = []

offsets_by_term = {}

for term in terms:
    name = term["term"]
    meta = circuit_meta.get(name, {"split": False, "circuits": []})
    sens = name.replace(" ", "_")
    parse_offsets = []
    offset_entries = []
    for anchor_key, needle in OCCS[name]:
        if anchor_key == "SECTION_FALLBACKS":
            base = CON_NORM.find(SECTION_FALLBACKS[name])
            search_base = base
        else:
            base = ANCHOR_POS[anchor_key]
            search_base = base
        raw_idx = CON_NORM.find(needle, search_base)
        if raw_idx == -1:
            # try broader start after section anchor marker
            marker = " ".join(ANCHORS[anchor_key].split())
            mstart = CON_NORM.find(marker)
            if mstart != -1:
                raw_idx = CON_NORM.find(needle, mstart)
        if raw_idx == -1:
            norm_needle = " ".join(needle.split())
            raw_idx = CON_NORM.find(norm_needle, search_base)
            needle = norm_needle
        if raw_idx == -1:
            raise SystemExit(f"needle fail {name} / {anchor_key} / {needle}")
        end = raw_idx + len(needle)
        entry = {"start": raw_idx, "end": end, "source_clause": anchor_key}
        parse_offsets.append(entry)
        offset_entries.append({"start": raw_idx, "end": end, "needle": needle})
    offsets_by_term[name] = offset_entries

    left = {
        "term": name,
        "id": f"original_meaning_node_{name}",
        "side": "left",
        "label": f"Original Meaning — {name}",
        "definition": term["origin_meaning"],
        "drift_classification": term["drift_classification"],
        "dictionary_source": webster_window(web1789, name, WEB1789_PATH, "Noah Webster, Dissertations on the English Language, 1789 [Gutenberg #45738]"),
        "inject_site": f"inject_site_{name}",
        "parse_site": f"parse_site_{name}",
        "sensitivity": sens,
        "offsets": parse_offsets,
        "blast_radius": term["blast_radius"],
        "english_crown_exclusion": term.get("crown_exclusion", ""),
    }
    right = {
        "term": name,
        "id": f"modern_meaning_node_{name}",
        "side": "right",
        "label": f"Modern Legal Meaning — {name}",
        "definition": term["modern_legal_status"],
        "drift_classification": term["drift_classification"],
        "dictionary_source": webster_window(web1913, name, WEB1913_PATH, "Webster Revised Unabridged Dictionary, 1913 [Gutenberg #664/#669]"),
        "inject_site": "",
        "parse_site": "",
        "sensitivity": sens,
        "offsets": parse_offsets,
        "circuit_status": "circuit-split" if meta.get("split") else "uniform",
        "circuits": list(meta.get("circuits", [])),
        "blast_radius": term["blast_radius"],
        "state_crosswalk": term["state_crosswalk"],
    }
    nodes.extend([left, right])
    edges.append({
        "source": left["id"],
        "target": right["id"],
        "label": "diff",
        "drift": term["drift_classification"],
        "circuit_status": right["circuit_status"],
        "circuits": right["circuits"],
    })
    for p in parse_offsets:
        edges.append({
            "source": "constitution_source_text",
            "target": left["id"],
            "label": "cites",
            "start": p["start"],
            "end": p["end"],
            "needle": next(entry["needle"] for entry in offset_entries if entry["start"] == p["start"]),
        })
    inject_sites.append({
        "id": f"inject_site_{name}",
        "term": name,
        "mode": "inject_site",
        "target_node": left["id"],
        "offsets": parse_offsets,
        "note": "Right-side originalist node pinned to exact clause offsets in normalized Constitution text."
    })
    parse_sites.append({
        "id": f"parse_site_{name}",
        "term": name,
        "mode": "parse_site",
        "source": CON_PATH,
        "offsets": parse_offsets,
        "note": "Exact parse sites for the sensitive classified term within the normalized Constitution body."
    })

topology = {
    "readout_name": "diff-graph-topology",
    "generated_at": date.today().isoformat(),
    "description": "Left-right diff graph topology connecting originalist meaning nodes to modern legal meaning nodes, with inject/parse sites tied to exact word offsets.",
    "center": {
        "title": "Constitution Source Text",
        "source_path": str(CON_PATH),
        "source_description": "Project Gutenberg eBook #5 trimmed to post-title constitutional document body.",
        "text": con_body,
        "normalized_text": CON_NORM,
        "character_length": len(con_body),
        "note": "Offsets refer to character positions in `text` and `normalized_text`."
    },
    "nodes": nodes,
    "edges": edges,
    "inject_sites": inject_sites,
    "parse_sites": parse_sites,
    "term_offsets": offsets_by_term,
    "conclusion": {
        "summary": "14-classified-term left-right diff topology.",
        "source": "constitutional-structural-truth-graph.json + Gutenberg cache sources"
    }
}

OUT.mkdir(parents=True, exist_ok=True)
TOPOLOGY_PATH = OUT / "diff-graph-topology.json"
TOPOLOGY_PATH.write_text(json.dumps(topology, indent=2, ensure_ascii=False), encoding="utf-8")
print("Wrote:", TOPOLOGY_PATH)
print("Nodes:", len(nodes))
print("Edges:", len(edges))
print("Inject sites:", len(inject_sites))
print("Parse sites:", len(parse_sites))
