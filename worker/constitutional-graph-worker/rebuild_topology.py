"""Rebuild diff-graph-topology.json using only pre-existing readouts."""
from pathlib import Path
import json
from datetime import date

ROOT = Path(r"C:\Users\krist\Desktop\constitutional-graph-tool\target\legal-data\constitutional-readouts")
MOD_PATH = ROOT / "modern-legal-meaning.json"
ORIG_PATH = ROOT / "originalist-meaning.json"
TOPOLOGY_PATH = ROOT / "diff-graph-topology.json"

orig = json.loads(ORIG_PATH.read_text(encoding="utf-8"))
mod = json.loads(MOD_PATH.read_text(encoding="utf-8"))

left_map = {e["term"]: e for e in orig.get("entries", [])}
right_map = {e["term"]: e for e in mod.get("entries", [])}

nodes = []
edges = []
inject_sites = []
parse_sites = []

for term, left in left_map.items():
    right = right_map[term]
    sens = term.replace(" ", "_")
    nodes.append({
        "term": term,
        "id": f"original_meaning_node_{term}",
        "side": "left",
        "label": f"Original Meaning — {term}",
        "drift_classification": left["drift_classification"],
        "definition": left["originalist_definition"],
        "dictionary_source": left.get("dictionary_sources", []),
        "inject_site": left["inject_site"],
        "parse_site": left["parse_site"],
        "sensitivity": sens,
    })
    nodes.append({
        "term": term,
        "id": f"modern_meaning_node_{term}",
        "side": "right",
        "label": f"Modern Legal Meaning — {term}",
        "drift_classification": right["drift_classification"],
        "definition": right["modern_legal_meaning"],
        "dictionary_source": [],
        "inject_site": "",
        "parse_site": "",
        "circuit_status": right.get("circuit_status", ""),
        "circuits": right.get("circuits", []),
        "sensitivity": sens,
    })
    edges.append({
        "source": f"original_meaning_node_{term}",
        "target": f"modern_meaning_node_{term}",
        "label": "diff",
        "drift": right["drift_classification"],
        "circuit_status": right.get("circuit_status", ""),
        "circuits": right.get("circuits", []),
    })
    parse_sites.append({
        "id": left["parse_site"],
        "term": term,
        "mode": "parse_site",
        "constitution_locations": left["constitution_locations"],
    })
    inject_sites.append({
        "id": left["inject_site"],
        "term": term,
        "mode": "inject_site",
        "target_node": f"original_meaning_node_{term}",
        "constitution_locations": left["constitution_locations"],
    })

topology = {
    "readout_name": "diff-graph-topology",
    "generated_at": date.today().isoformat(),
    "description": "Left-right diff graph topology connecting originalist meaning nodes to modern legal meaning nodes, with inject/parse sites bound to the classified constitutional string.",
    "center": {
        "title": "Constitution Source Text",
        "source_path": "C:\\Users\\krist\\AppData\\Local\\hermes\\cache\\web\\www.gutenberg.org-48ab8abb9a.md",
        "source_description": "Project Gutenberg eBook #5",
        "note": "Exact character offsets are derivable from the classified term constitutional_text mappings against the Gutenberg plain text."
    },
    "nodes": nodes,
    "edges": edges,
    "inject_sites": inject_sites,
    "parse_sites": parse_sites,
    "conclusion": {
        "summary": "14-classified-term left-right diff topology. inject_site_* IDs mark left-originalist nodes; parse_site_* IDs mark terms parsed from the classified constitutional string.",
        "source": "constitutional-structural-truth-graph.json + originalist-meaning.json + modern-legal-meaning.json"
    }
}
TOPOLOGY_PATH.write_text(json.dumps(topology, indent=2, ensure_ascii=False), encoding="utf-8")
print("Rebuilt:", TOPOLOGY_PATH)
print("Nodes:", len(nodes))
print("Edges:", len(edges))
print("Legislative modern circuit:", [n.get("circuit_status") for n in nodes if n["id"]=="modern_meaning_node_legislative"])
