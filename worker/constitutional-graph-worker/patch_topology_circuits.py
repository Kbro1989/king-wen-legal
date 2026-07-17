"""Patch diff-graph-topology with circuit metadata from modern readout."""
from pathlib import Path
import json

ROOT = Path(r"C:\Users\krist\Desktop\constitutional-graph-tool\target\legal-data\constitutional-readouts")
MOD_PATH = ROOT / "modern-legal-meaning.json"
TOPOLOGY_PATH = ROOT / "diff-graph-topology.json"

modern = json.loads(MOD_PATH.read_text(encoding="utf-8"))
topo = json.loads(TOPOLOGY_PATH.read_text(encoding="utf-8"))

mod_map = {e["term"]: e for e in modern.get("entries", [])}

for term, right in mod_map.items():
    node = next((n for n in topo["nodes"] if n["id"] == f"modern_meaning_node_{term}"), None)
    if node is None:
        continue
    node["circuit_status"] = right.get("circuit_status", "")
    node["circuits"] = right.get("circuits", [])
    edge = next((e for e in topo["edges"] if e["source"] == f"original_meaning_node_{term}" and e["target"] == f"modern_meaning_node_{term}"), None)
    if edge:
        edge["circuit_status"] = node["circuit_status"]
        edge["circuits"] = node["circuits"]

TOPOLOGY_PATH.write_text(json.dumps(topo, indent=2, ensure_ascii=False), encoding="utf-8")
print("Patched:", TOPOLOGY_PATH)
