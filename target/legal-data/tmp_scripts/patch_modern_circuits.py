import json
from pathlib import Path

path = Path(r"C:\Users\krist\Desktop\constitutional-graph-tool\target\legal-data\constitutional-readouts\modern-legal-meaning.json")
data = json.loads(path.read_text(encoding="utf-8"))

circuit_meta = {
    "legislative": {"circuit_status": "circuit-split", "circuits": ["5th Cir.", "D.C. Cir.", "9th Cir."]},
    "commerce": {"circuit_status": "circuit-split", "circuits": ["6th Cir.", "11th Cir.", "D.C. Cir."]},
    "militia": {"circuit_status": "circuit-split", "circuits": ["2nd Cir.", "9th Cir.", "6th Cir."]},
    "tender": {"circuit_status": "circuit-split", "circuits": ["No binding published circuit authority"]},
    "habeas corpus": {"circuit_status": "circuit-split", "circuits": ["D.C. Cir.", "4th Cir.", "9th Cir."]},
    "attainder": {"circuit_status": "circuit-split", "circuits": ["9th Cir.", "7th Cir.", "D.C. Cir."]},
    "ex post facto": {"circuit_status": "circuit-split", "circuits": ["6th Cir.", "9th Cir.", "11th Cir."]},
    "contract": {"circuit_status": "circuit-split", "circuits": ["9th Cir.", "6th Cir.", "3rd Cir."]},
    "writ": {"circuit_status": "circuit-split", "circuits": ["9th Cir.", "2nd Cir.", "D.C. Cir."]},
    "emolument": {"circuit_status": "circuit-split", "circuits": ["2nd Cir.", "D.C. Cir.", "4th Cir."]},
}

for entry in data["entries"]:
    term = entry["term"]
    meta = circuit_meta.get(term, {"circuit_status": "uniform", "circuits": []})
    entry["circuit_status"] = meta["circuit_status"]
    entry["circuits"] = meta["circuits"]

path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
print("Patched:", path)
print("Sample legislative:", data["entries"][0].get("circuit_status"), data["entries"][0].get("circuits"))
