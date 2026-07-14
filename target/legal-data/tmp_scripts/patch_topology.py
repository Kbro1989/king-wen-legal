import json
from pathlib import Path
from datetime import date

TARGET = Path(r"C:\Users\krist\Desktop\constitutional-graph-tool\target\legal-data")
OUT = TARGET / "constitutional-readouts"
TOPOLOGY_PATH = OUT / "diff-graph-topology.json"
ORIG_PATH = OUT / "originalist-meaning.json"
MOD_PATH = OUT / "modern-legal-meaning.json"
GRAPH_PATH = TARGET / "constitutional-structural-truth-graph.json"

orig = json.loads(ORIG_PATH.read_text(encoding="utf-8"))
modern = json.loads(MOD_PATH.read_text(encoding="utf-8"))
graph = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
topo = json.loads(TOPOLOGY_PATH.read_text(encoding="utf-8"))

left_map = {e["term"]: e for e in orig.get("entries", [])}
right_map = {e["term"]: e for e in modern.get("entries", [])}
truth_terms = [t["term"] for t in graph["term_analysis"]["terms"]]

# Update existing topology schema to include modern metadata.
for term in truth_terms:
    left = left_map[term]
    right = right_map[term]
    left_node = next(n for n in topo["nodes"] if n["id"] == f"original_meaning_node_{term}")
    right_node = next(n for n in topo["nodes"] if n["id"] == f"modern_meaning_node_{term}")
    left_node["term"] = term
    left_node["definition"] = left["originalist_definition"]
    left_node["dictionary_source"] = left.get("dictionary_sources", [])
    left_node["inject_site"] = left.get("inject_site", "")
    left_node["parse_site"] = left.get("parse_site", "")
    left_node["sensitivity"] = term.replace(" ", "_")
    left_node["blast_radius"] = left.get("blast_radius", graph["term_analysis"]["terms"][truth_terms.index(term)]["blast_radius"])
    left_node["english_crown_exclusion"] = left.get("english_crown_exclusion", graph["term_analysis"]["terms"][truth_terms.index(term)].get("crown_exclusion", ""))
    right_node["term"] = term
    right_node["definition"] = right["modern_legal_meaning"]
    right_node["dictionary_source"] = right.get("dictionary_sources", [])
    right_node["inject_site"] = right.get("inject_site", "")
    right_node["parse_site"] = right.get("parse_site", "")
    right_node["sensitivity"] = term.replace(" ", "_")
    right_node["circuit_status"] = right.get("circuit_status", "")
    right_node["circuits"] = right.get("circuits", [])

    edge = next((e for e in topo["edges"] if e["source"] == f"original_meaning_node_{term}" and e["target"] == f"modern_meaning_node_{term}"), None)
    if edge:
        edge["drift"] = right["drift_classification"]
        edge["classification"] = right["drift_classification"]
        edge["circuit_status"] = right.get("circuit_status", "")
        edge["circuits"] = right.get("circuits", [])

topo["generated_at"] = date.today().isoformat()
topo["conclusion"] = {
    "summary": "14-classified-term left-right diff topology. inject_site_* IDs mark left/originalist nodes; parse_site_* IDs mark terms parsed from the classified constitutional string.",
    "source": "constitutional-structural-truth-graph.json + originalist-meaning.json + modern-legal-meaning.json"
}
TOPOLOGY_PATH.write_text(json.dumps(topo, indent=2, ensure_ascii=False), encoding="utf-8")
print("Updated:", TOPOLOGY_PATH)
print("Nodes:", len(topo["nodes"]))
print("Edges:", len(topo["edges"]))
