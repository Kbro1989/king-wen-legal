from pathlib import Path
import json

text_path = Path(r"C:\Users\krist\AppData\Local\hermes\cache\web\www.gutenberg.org-48ab8abb9a.md")
text = text_path.read_text(encoding="utf-8")

graph_path = Path(r"C:\Users\krist\Desktop\constitutional-graph-tool\target\legal-data\constitutional-structural-truth-graph.json")
graph = json.loads(graph_path.read_text(encoding="utf-8"))
terms = graph["term_analysis"]["terms"]

anchors = {
    "legislative": "Section 1. All legislative Powers",
    "commerce": "To regulate Commerce with foreign Nations, and among the several States, and with the Indian Tribes.",
    "tax": "To lay and collect Taxes, Duties, Imposts and Excises, to pay the Debts and provide for the common Defence and general Welfare of the United States; but all Duties, Imposts and Excises shall be uniform throughout the United States;",
    "coin": "To coin Money, regulate the Value thereof, and of foreign Coin, and fix the Standard of Weights and Measures;",
    "tender": "make any Thing but gold and silver Coin a Tender in Payment of Debts",
    "militia": "To provide for calling forth the Militia to execute the Laws of the Union, suppress Insurrections and repel Invasions;",
    "treason": "Treason against the United States, shall consist only in levying War against them, or in adhering to their Enemies, giving them Aid and Comfort. No Person shall be convicted of Treason unless on the Testimony of two Witnesses to the same overt Act, or on Confession in open Court.",
    "habeas corpus": "The Privilege of the Writ of Habeas Corpus shall not be suspended, unless when in Cases of Rebellion or Invasion the public Safety may require it.",
    "attainder": "No Bill of Attainder or ex post facto Law shall be passed.",
    "ex post facto": "ex post facto Law shall be passed.",
    "contract": "Law impairing the Obligation of Contracts",
    "money": "To coin Money, regulate the Value thereof, and of foreign Coin, and fix the Standard of Weights and Measures;",
    "writ": "The Privilege of the Writ of Habeas Corpus shall not be suspended, unless when in Cases of Rebellion or Invasion the public Safety may require it.",
    "emolument": "Emoluments whereof shall have been increased during such time"
}

# Find section/area fallbacks if exact anchor not searchable from term needle
area_bases = {
    "tax": "Section 8. The Congress shall have Power to lay and collect Taxes",
    "tender": "Section 10. No State shall enter into any Treaty, Alliance, or Confederation",
    "ex post facto": "Section 9. The Migration or Importation",
    "contract": "Section 10. No State shall enter into any Treaty, Alliance, or Confederation",
    "money": "Section 8. The Congress shall have Power to lay and collect Taxes",
    "emolument": "Section 6. The Senators and Representatives shall receive a Compensation",
    "writ": "Section 9. The Migration or Importation",
}

rows = {}
for term in terms:
    name = term["term"]
    needle = anchors[name]
    idx = text.find(needle)
    if idx != -1:
        rows[name] = {"start": idx, "end": idx + len(needle), "mode": "exact"}
        continue
    base = area_bases[name]
    base_idx = text.find(base)
    if base_idx == -1:
        raise SystemExit(f"base not found {name}: {base!r}")
    idx2 = text.find(needle, base_idx)
    if idx2 == -1:
        idx2 = text.find(" ".join(needle.split()), base_idx)
    if idx2 == -1:
        raise SystemExit(f"needle not found {name}")
    rows[name] = {"start": idx2, "end": idx2 + len(needle.split() if text[idx2:idx2+len(needle)].replace(" ","") != "".join(needle.split()) else needle), "mode": "section-base"}

print(json.dumps(rows, indent=2))
