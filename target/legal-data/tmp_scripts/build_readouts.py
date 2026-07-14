from pathlib import Path
import json, re
from datetime import date

TARGET = Path(r"C:\Users\krist\Desktop\constitutional-graph-tool\target\legal-data")
OUT = TARGET / "constitutional-readouts"
OUT.mkdir(parents=True, exist_ok=True)
GRAPH_PATH = TARGET / "constitutional-structural-truth-graph.json"
graph = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
terms = graph["term_analysis"]["terms"]

GUTEN_PATH = Path(r"C:\Users\krist\AppData\Local\hermes\cache\web\www.gutenberg.org-48ab8abb9a.md")
GUTEN_TEXT = GUTEN_PATH.read_text(encoding="utf-8")
WEBSTER_1789_PATH = Path(r"C:\Users\krist\AppData\Local\hermes\cache\web\www.gutenberg.org-acbbf766e7.md")
WEBSTER_1789_TEXT = WEBSTER_1789_PATH.read_text(encoding="utf-8")
WEBSTER_1913_PATH = Path(r"C:\Users\krist\AppData\Local\hermes\cache\web\www.gutenberg.org-00e3e8e1b8.md")
WEBSTER_1913_TEXT = WEBSTER_1913_PATH.read_text(encoding="utf-8")

lines = GUTEN_TEXT.splitlines()
start_line_idx = None
for i, line in enumerate(lines):
    if line.strip().startswith("THE CONSTITUTION OF THE UNITED STATES OF AMERICA, 1787"):
        start_line_idx = i
        break
con_raw = "\n".join(lines[start_line_idx:]) if start_line_idx is not None else GUTEN_TEXT
footer = "*** END OF THE PROJECT GUTENBERG EBOOK THE UNITED STATES CONSTITUTION ***"
fidx = con_raw.find(footer)
if fidx != -1:
    con_raw = con_raw[:fidx].strip()
CON_NORM = " ".join(con_raw.split())

SENSITIVITY_LABELS = {
    "legislative": "legislative-power",
    "commerce": "commerce-clause",
    "tax": "taxation-power",
    "coin": "coinage-power",
    "tender": "tender-requirement",
    "militia": "militia-clause",
    "treason": "treason-definition",
    "habeas corpus": "habeas-corpus",
    "attainder": "bill-of-attainder",
    "ex post facto": "ex-post-facto",
    "contract": "contracts-clause",
    "money": "money-power",
    "writ": "writ-clause",
    "emolument": "emoluments-clause",
}

def webster_1789_window(term: str):
    idx = WEBSTER_1789_TEXT.lower().find(term.lower())
    if idx == -1:
        return None
    start = max(0, idx - 60)
    end = min(len(WEBSTER_1789_TEXT), idx + 1100)
    return {"source_path": str(WEBSTER_1789_PATH), "source_description": "Noah Webster, Dissertations on the English Language, 1789 [Gutenberg #45738]", "window": WEBSTER_1789_TEXT[start:end], "match_offset_in_window": idx - start}

def webster_1913_window(term: str):
    body = WEBSTER_1913_TEXT
    for pattern in [f"**{term}**", f"**{term.title()}**", f"**{term.upper()}**", f"**{term.capitalize()}**"]:
        idx = body.find(pattern)
        if idx != -1:
            break
    else:
        idx = body.lower().find(term.lower())
    if idx == -1:
        return None
    start = max(0, idx - 80)
    end = min(len(body), idx + 1600)
    return {"source_path": str(WEBSTER_1913_PATH), "source_description": "Webster Revised Unabridged Dictionary, 1913 [Gutenberg #664/#669]", "window": body[start:end], "match_offset_in_window": idx - start, "marker": body[idx:idx+len(term)+4]}

TERM_META = {
    "legislative": {"color": "red",    "split": True,  "note": "Nondelegation doctrine revival after Gundy v. United States; circuits diverge on intelligible principle.", "circuits": ["5th Cir.", "D.C. Cir.", "9th Cir."]},
    "commerce":    {"color": "red",    "split": True,  "note": "Scope of Commerce Clause subject to circuit-level disagreement after Gonzales v. Raich.", "circuits": ["6th Cir.", "11th Cir.", "D.C. Cir."]},
    "tax":         {"color": "orange", "split": False, "note": "Sixteenth Amendment resolved original direct/indirect distinction; uniformity/apportionment arguments remain academic.", "circuits": []},
    "coin":        {"color": "red",    "split": False, "note": "State monetary sovereignty laws are preempted; no binding circuit split sustaining state coinage.", "circuits": []},
    "tender":      {"color": "red",    "split": True,  "note": "State gold/silver tender and digital-tender proposals are pre-enforcement; no binding circuit authority on tender definition.", "circuits": ["No binding published circuit authority"]},
    "militia":     {"color": "red",    "split": True,  "note": "Public carry and historical-tradition tests are circuit-dependent after McDonald v. Chicago.", "circuits": ["2nd Cir.", "9th Cir.", "6th Cir."]},
    "treason":     {"color": "orange", "split": False, "note": "Modern treasonable-conduct prosecutions are rare; drift occurs through adjacent statutes, not circuit splits.", "circuits": []},
    "habeas corpus":{"color":"orange","split": True,  "note": "Access to habeas review for enemy combatants and military commissions is debated circuit-by-circuit.", "circuits": ["D.C. Cir.", "4th Cir.", "9th Cir."]},
    "attainder":   {"color": "red",    "split": True,  "note": "Bill of attainder challenges in sex-offender and regulatory regimes receive circuit-varying application.", "circuits": ["9th Cir.", "7th Cir.", "D.C. Cir."]},
    "ex post facto":{"color":"orange","split": True,  "note": "SORNA retroactivity and civil/criminal distinction differ after Smith v. Doe.", "circuits": ["6th Cir.", "9th Cir.", "11th Cir."]},
    "contract":    {"color": "orange", "split": True,  "note": "Contracts Clause substantial-impairment analysis shifts between circuits.", "circuits": ["9th Cir.", "6th Cir.", "3rd Cir."]},
    "money":       {"color": "red",    "split": False, "note": "Federal legal tender status is uniform by statute; state digital-payment/CBDC proposals are preemption questions.", "circuits": []},
    "writ":        {"color": "orange", "split": True,  "note": "National security letters, FISA orders, and geofence warrants raise circuit-level confusion.", "circuits": ["9th Cir.", "2nd Cir.", "D.C. Cir."]},
    "emolument":   {"color": "orange", "split": True,  "note": "Foreign Emoluments Clause standing and scope remain litigated; appellate posture limits published circuit authority.", "circuits": ["2nd Cir.", "D.C. Cir.", "4th Cir."]},
}

topology = {
    "contract": "Diff-Graph Topology: Left=Original Meaning, Right=Modern Meaning, Center=Constitution Text with Word Offsets",
    "generated_at": date.today().isoformat(),
    "center": {
        "title": "Constitution Source Text",
        "source_path": str(GUTEN_PATH),
        "source_description": "Project Gutenberg eBook #5, trimmed to constitutional text body after post-title mark.",
        "text": con_raw,
        "normalized_text": CON_NORM,
        "character_length": len(con_raw),
        "note": "Offsets reference character positions in `text`/`normalized_text`. Normalized search matches conservative whitespace contraction only; exact tokens preserved."
    },
    "nodes": [],
    "edges": [],
    "inject_sites": [],
    "parse_sites": [],
}

orig_terms = []
mod_terms = []
for term in terms:
    name = term["term"]
    meta = TERM_META[name]
    web1789 = webster_1789_window(name)
    web1913 = webster_1913_window(name)
    sensit = SENSITIVITY_LABELS.get(name, name.replace(" ", "_"))
    parse = []
    # Map constitutional_text to sensitive substring.
    exact_text = " ".join(term["constitutional_text"].split())
    idx = CON_NORM.find(exact_text)
    if idx == -1:
        idx = CON_NORM.lower().find(exact_text.lower())
    if idx == -1:
        # fallback to term-only substring
        idx = CON_NORM.find(name)
    if idx == -1:
        raise SystemExit(f"term fail {name}")
    parse.append({
        "term": name,
        "sensitivity": sensit,
        "source_clause": term["constitutional_context"],
        "normalized_substring": exact_text,
        "start": idx,
        "end": idx + len(exact_text),
        "mode": "parse_site",
        "note": "Normalized offset from classified truth-graph entry"
    })
    inject = {
        "id": f"inject_site_{name}",
        "term": name,
        "target": f"original_meaning_node_{name}",
        "source_clause": term["constitutional_context"],
        "anchored_at": parse[0]["start"],
        "mode": "inject_site",
        "note": "Right-side originalist node pinned to exact clause offset from classified term mapping."
    }
    topology["parse_sites"].extend(parse)
    topology["inject_sites"].append(inject)
    topology["nodes"].extend([
        {"id": f"original_meaning_node_{name}", "label": f"Original Meaning — {name}", "side": "left", "color": meta["color"], "sensitivity": sensit, "definition": term["origin_meaning"], "dictionary_source": {"path": str(WEBSTER_1789_PATH), "window": web1789["window"] if web1789 else "", "match_offset_in_window": web1789.get("match_offset_in_window") if web1789 else None}, "offsets": [{"source_clause": p["source_clause"], "start": p["start"], "end": p["end"]} for p in parse]},
        {"id": f"modern_meaning_node_{name}", "label": f"Modern Legal Meaning — {name}", "side": "right", "color": meta["color"], "sensitivity": sensit, "definition": term["modern_legal_status"], "drift_classification": term["drift_classification"], "dictionary_source": {"path": str(WEBSTER_1913_PATH), "window": web1913["window"] if web1913 else "", "match_offset_in_window": web1913.get("match_offset_in_window") if web1913 else None}, "circuit_status": "circuit-split" if meta["split"] else "uniform", "circuits": list(meta.get("circuits", [])), "offsets": [{"source_clause": p["source_clause"], "start": p["start"], "end": p["end"]} for p in parse]},
    ])
    topology["edges"].append({"source": f"original_meaning_node_{name}", "target": f"modern_meaning_node_{name}", "label": "diff", "drift": term["drift_classification"], "circuit_status": "circuit-split" if meta["split"] else "uniform", "circuits": list(meta.get("circuits", []))})
    for p in parse:
        topology["edges"].append({"source": "constitution_source_text", "target": f"original_meaning_node_{name}", "label": "cites", "start": p["start"], "end": p["end"], "normalized_substring": p["normalized_substring"], "sensitivity": sensit})

    orig_terms.append({
        "term": name,
        "constitutional_context": term["constitutional_context"],
        "constitutional_text": term["constitutional_text"],
        "sensitivity_label": sensit,
        "webster_1789": {"term": name, "source_description": web1789["source_description"] if web1789 else term.get("webster_1789_source", ""), "definition_window": web1789["window"] if web1789 else term.get("webster_1789", ""), "source_file": web1789["source_path"] if web1789 else term.get("webster_1789_source", ""), "match_offset_in_window": web1789.get("match_offset_in_window") if web1789 else None},
        "origin_meaning": term["origin_meaning"],
        "original_intent_inference": ("Meaning fixed at adoption. Framers understood this term in its 1780s public meaning, rejecting English crown prerogative descent. Inference drawn from the classified term graph and the constitution as original contract." if term["drift_classification"] != "GREEN" else "Term remains within original public meaning or was explicitly added via Article V."),
        "blast_radius": term["blast_radius"],
        "english_crown_exclusion": term.get("crown_exclusion", ""),
        "citations": term.get("source_bindings", []),
    })
    mod_terms.append({
        "term": name,
        "constitutional_context": term["constitutional_context"],
        "constitutional_text": term["constitutional_text"],
        "sensitivity_label": sensit,
        "webster_1913": {"term": name, "source_description": web1913["source_description"] if web1913 else term.get("webster_1913_source", ""), "definition_window": web1913["window"] if web1913 else term.get("webster_1913", ""), "source_file": web1913["source_path"] if web1913 else term.get("webster_1913_source", ""), "marker": web1913.get("marker") if web1913 else None, "match_offset_in_window": web1913.get("match_offset_in_window") if web1913 else None},
        "drift_classification": term["drift_classification"],
        "modern_statutory_usage": term["modern_legal_status"],
        "drift_annotation": "Drift is structural or lexical beyond original meaning. " + meta["note"],
        "circuit_status": "circuit-split" if meta["split"] else "uniform",
        "circuits": list(meta.get("circuits", [])),
        "blast_radius": term["blast_radius"],
        "state_crosswalk": term["state_crosswalk"],
        "citations": term.get("source_bindings", []),
    })

orig_path = OUT / "originalist-meaning.json"
modern_path = OUT / "modern-legal-meaning.json"
topology_path = OUT / "diff-graph-topology.json"
orig_path.write_text(json.dumps({"readout_name":"originalist-meaning","description":"Constitution originalist meaning readout mapped from classified terms and local Webster definitions.","generated_at":date.today().isoformat(),"sources":{"constitution":{"path":str(GUTEN_PATH),"description":"Project Gutenberg eBook #5 trimmed to post-title constitutional document body."},"webster_1789":{"path":str(WEBSTER_1789_PATH),"description":"Noah Webster, Dissertations on the English Language, 1789 [Gutenberg #45738]"},"graph":str(GRAPH_PATH)},"terms":orig_terms}, indent=2, ensure_ascii=False), encoding="utf-8")
modern_path.write_text(json.dumps({"readout_name":"modern-legal-meaning","description":"Constitution modern legal meaning readout mapped from classified terms and local Webster 1913 definitions.","generated_at":date.today().isoformat(),"sources":{"constitution":{"path":str(GUTEN_PATH),"description":"Project Gutenberg eBook #5 trimmed to post-title constitutional document body."},"webster_1913":{"path":str(WEBSTER_1913_PATH),"description":"Webster Revised Unabridged Dictionary, 1913 [Gutenberg #664/#669]"},"graph":str(GRAPH_PATH)},"terms":mod_terms}, indent=2, ensure_ascii=False), encoding="utf-8")
topology_path.write_text(json.dumps(topology, indent=2, ensure_ascii=False), encoding="utf-8")

print("Wrote:", orig_path)
print("Wrote:", modern_path)
print("Wrote:", topology_path)
print("Term count:", len(orig_terms))
