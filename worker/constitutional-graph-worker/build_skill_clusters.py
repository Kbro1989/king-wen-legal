#!/usr/bin/env python3
"""
Build skill-clusters manifest.json from constitutional dictionary sources.
Clusters per-dictionary learn artifacts by semantic domain and prepares
constitution-parser bindings as placeholders pending diff-graph-topology.
"""
import json, os, re
from collections import defaultdict
from pathlib import Path

LEGAL_DATA = Path(r"C:\Users\krist\Desktop\constitutional-graph-tool\target\legal-data")
OUT_DIR = LEGAL_DATA / "skill-clusters"
OUT_DIR.mkdir(exist_ok=True)
OUT_PATH = OUT_DIR / "manifest.json"

# Semantic domain definitions based on constitutional text context and existing truth-graph terms.
# These are heuristic mappings; actual parser bindings will slot in real character-offset ranges.
DOMAIN_RULES = {
    "legislative": {
        "keywords": [
            "legislative", "legislature", "congress", "senate", "representative",
            "house", "bill", "law", "enact", "statute", "resolution", "quorum",
            "yeas", "nays", "vote", "elect", "election", "impeachment",
            "trial", "witness", "oath", "affirmation", "ratify", "convention",
            "amendment", "propose", "majority", " presiding officer"
        ],
        "articles": ["Article I", "Article V"],
    },
    "commerce": {
        "keywords": [
            "commerce", "trade", "exchange", "impost", "duty", "excise", "tonnage",
            "export", "import", "navigation", "inspection", "coasting", "vessel",
            "port", "state duty", "uniformity", "foreign nation", "indian tribe"
        ],
        "articles": ["Article I", "Article I, Section 8", "Article I, Section 9", "Article I, Section 10"],
    },
    "monetary": {
        "keywords": [
            "coin", "money", "tender", "gold", "silver", "currency", "bank",
            "bill of credit", "value", "weight", "measure", "coinage", "mint",
            "Treasury", "payment", "debt", "contract", "obligation", "excise",
            "capitation", "direct tax", "income", "duty", "impost"
        ],
        "articles": ["Article I, Section 8", "Article I, Section 9", "Article I, Section 10"],
    },
    "military": {
        "keywords": [
            "militia", "army", "navy", "war", "invasion", "insurrection",
            "rebellion", "commander in chief", "troop", "garrison", "fort",
            "arms", "bear arms", "piracy", "capture", "felony", "high seas",
            "military", "troops", "writ", "habeas corpus", "suspension"
        ],
        "articles": ["Article I, Section 8", "Article II, Section 2", "Amendment II", "Article I, Section 9"],
    },
    "judicial": {
        "keywords": [
            "court", "judge", "judicial", "trial", "jury", "verdict", "offense",
            "crime", "criminal", "felony", "treason", "confront", "witness",
            "compulsory", "assistance", "counsel", "due process", "habeas corpus",
            "supreme", "inferior", "jurisdiction", "appeal", "writ", "attorney",
            "bail", "fine", "excessive", "cruel", "unusual", "search", "warrant",
            "probable", "seizure", "fourth", "fifth", "sixth", "seventh", "eighth",
            "fourteenth", "equal protection", "citizenship", "deprivation", "privilege", "immunity"
        ],
        "articles": [
            "Article III", "Amendment IV", "Amendment V", "Amendment VI",
            "Amendment VII", "Amendment VIII", "Amendment XIV"
        ],
    },
    "procedural": {
        "keywords": [
            "time", "place", "manner", "rules", "proceed", "procedure",
            "motion", "adjourn", "session", "meeting", "journal", "enter",
            "publish", "secret", "attendance", "compensation", "privilege",
            "arrest", "priviledege from arrest", "freedom of speech", "petition",
            "assemble", "redress", "grievance", "establishment", "religion",
            "speech", "press", "first amendment", "due process", "equal protection"
        ],
        "articles": ["Amendment I", "Article I, Section 5", "Amendment XIV"],
    },
    "sovereignty": {
        "keywords": [
            "sovereign", "sovereignty", "state", "united", "federal", "union",
            "confederation", "full faith", "credit", "privilege", "immunity",
            "extradition", "guarantee", "republican", "form of government",
            "domestic violence", "invasion", "section 10", "compact",
            "title of nobility", "emolument", "treaty", "alliance", "confederation",
            "constitution", "ordain", "establish", "ordained", "preamble",
            "we the people", "perfect union", "justice", "domestic tranquility",
            "common defence", "general welfare", "posterity"
        ],
        "articles": ["Preamble", "Article I, Section 10", "Article IV", "Article VI", "Amendment I", "Amendment X", "Amendment XI"],
    },
}

def classify_domain(term: str, context: str = "") -> str:
    text = f"{term} {context}".lower()
    scores = {}
    for domain, rules in DOMAIN_RULES.items():
        score = 0
        for kw in rules["keywords"]:
            if kw.lower() in text:
                score += 1
        for art in rules.get("articles", []):
            if art.lower() in text:
                score += 2
        scores[domain] = score
    sorted_domains = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
    best_domain, best_score = sorted_domains[0]
    if best_score == 0 or (best_domain == "sovereignty" and any(d != "sovereignty" and s == best_score for d, s in sorted_domains)):
        # Prefer any non-sovereignty domain if available, only fall back to sovereignty
        for d, s in sorted_domains:
            if s > 0 and d != "sovereignty":
                return d
        return "sovereignty"
    return best_domain

def extract_term_context(term_obj: dict) -> str:
    ctx = term_obj.get("constitutional_context", "")
    text = term_obj.get("constitutional_text", "")
    return f"{ctx} {text}"

def drift_weight(clazz: str) -> int:
    order = {"RED": 4, "ORANGE": 3, "YELLOW": 2, "GREEN": 1, "found_in_1913_only": 0, "UNCLASSIFIED": 0}
    return order.get(clazz, 0)

def dominant_drift(entries):
    best = None
    best_w = -1
    for e in entries:
        w = drift_weight(e.get("drift_classification", "UNCLASSIFIED"))
        if w > best_w:
            best_w = w
            best = e.get("drift_classification", "UNCLASSIFIED")
    return best or "UNCLASSIFIED"

# Load sources
truth_graph_path = LEGAL_DATA / "constitutional-structural-truth-graph.json"
word_inventory_path = LEGAL_DATA / "constitution-complete-word-inventory.json"
diff_path = LEGAL_DATA / "timelined-dictionary-diff.json"

with open(truth_graph_path, "r", encoding="utf-8") as f:
    truth_data = json.load(f)
with open(word_inventory_path, "r", encoding="utf-8") as f:
    inventory_data = json.load(f)
with open(diff_path, "r", encoding="utf-8") as f:
    diff_data = json.load(f)

# Build quick lookup from truth graph
term_lookup = {}
for t in truth_data.get("term_analysis", {}).get("terms", []):
    term_lookup[t["term"]] = t

# Load constitution text for parser binding placeholder data
constitution_text_path = Path(r"C:\Users\krist\AppData\Local\hermes\cache\web\www.gutenberg.org-48ab8abb9a.md")
constitution_text = ""
if constitution_text_path.exists():
    constitution_text = constitution_text_path.read_text(encoding="utf-8", errors="ignore")
else:
    constitution_text = ""

# Pre-scan known section header patterns to fill placeholder ranges
SECTION_PATTERNS = [
    ("Preamble", r"\bWe the People\b"),
    ("Article I", r"\bArticle\s+I\b"),
    ("Article II", r"\bArticle\s+II\b"),
    ("Article III", r"\bArticle\s+III\b"),
    ("Article IV", r"\bArticle\s+IV\b"),
    ("Article V", r"\bArticle\s+V\b"),
    ("Article VI", r"\bArticle\s+VI\b"),
    ("Article VII", r"\bArticle\s+VII\b"),
    ("Amendment I", r"\bAmendment\s+I\b"),
    ("Amendment II", r"\bAmendment\s+II\b"),
    ("Amendment III", r"\bAmendment\s+III\b"),
    ("Amendment IV", r"\bAmendment\s+IV\b"),
    ("Amendment V", r"\bAmendment\s+V\b"),
    ("Amendment VI", r"\bAmendment\s+VI\b"),
    ("Amendment VII", r"\bAmendment\s+VII\b"),
    ("Amendment VIII", r"\bAmendment\s+VIII\b"),
    ("Amendment IX", r"\bAmendment\s+IX\b"),
    ("Amendment X", r"\bAmendment\s+X\b"),
    ("Amendment XI", r"\bAmendment\s+XI\b"),
    ("Amendment XII", r"\bAmendment\s+XII\b"),
]

placeholder_ranges = {}
for name, pat in SECTION_PATTERNS:
    m = re.search(pat, constitution_text, re.IGNORECASE)
    if m:
        placeholder_ranges[name] = {
            "start_char_offset": m.start(),
            "end_char_offset": m.end(),
            "note": "placeholder; replace with actual parse ranges once diff-graph-topology is available"
        }

# Assemble all known domain-relevant words from truth graph
# We supplement with word_inventory words that have blast radius matches.
all_domain_entries = defaultdict(list)

for t in truth_data.get("term_analysis", {}).get("terms", []):
    domain = classify_domain(t.get("term", ""), extract_term_context(t))
    all_domain_entries[domain].append(t)

# Additional words from inventory are collected but primary clustering uses truth graph.
# Inventory words not in truth graph are noted via MISSING_FOR_CLUSTER where they don't match.

# Build per-cluster manifest
clusters = {}
for domain in DOMAIN_RULES.keys():
    entries = all_domain_entries.get(domain, [])
    dict_skills = []
    shared_words = []
    shared_blast = set()
    drift_counts = defaultdict(int)
    coverage_gaps = []

    # track which sections covered
    sections_in_cluster = defaultdict(set)

    for e in entries:
        word = e.get("term", "")
        shared_words.append(word)
        sections_in_cluster["truth_graph"].add("constitutional-structural-truth-graph.json")
        # blast radius merge
        br = e.get("blast_radius", {})
        for sd in br.get("subdomains", []):
            shared_blast.add(sd)
        dc = e.get("drift_classification", "UNCLASSIFIED")
        drift_counts[dc] += 1
        # source bindings as learned-skill proxies
        for sb in e.get("source_bindings", []):
            dict_skills.append(str(sb))
        # dictionary coverage check
        inv_entry = next((w for w in inventory_data.get("word_inventory", []) if w.get("word") == word), None)
        if inv_entry is None:
            coverage_gaps.append({
                "word": word,
                "missing_from": ["constitution-complete-word-inventory.json"]
            })
        else:
            secs = inv_entry.get("webster_1913_sections_used", [])
            for s in secs:
                sections_in_cluster["webster-1913"].add(s)
            prov = inv_entry.get("webster_1789_provenance", "")
            if prov == "NO_1789_LEXICON_ENTRY":
                coverage_gaps.append({
                    "word": word,
                    "missing_from": ["webster_1789_dictionary_editions"],
                    "reason": "NO_1789_LEXICON_ENTRY"
                })

    # Dedup dict_skills list
    dict_skills = sorted(set(dict_skills))
    shared_blast = sorted(shared_blast)
    dom_drift = dominant_drift(entries) if entries else "UNCLASSIFIED"

    # Merge coverage gaps across clusters for missing words
    missing_inventory_words = []
    for w in inventory_data.get("word_inventory", []):
        word_text = w.get("word", "")
        # only include high-frequency domain words that are not already in shared_words
        if word_text not in shared_words and int(w.get("frequency_in_constitution", 0)) >= 10:
            # check if missing from cluster via 1913 coverage
            prov1789 = w.get("webster_1789_provenance", "")
            prov1913 = w.get("webster_1913_provenance", "")
            if prov1789 == "NO_1789_LEXICON_ENTRY" or prov1913 == "FOUND_IN_1913_SECTION":
                # heuristic: add only if keyword match suggests domain relevance
                domain_keywords = DOMAIN_RULES[domain]["keywords"]
                if any(kw.lower() in word_text.lower() for kw in domain_keywords):
                    missing_inventory_words.append({
                        "word": word_text,
                        "status": "MISSING_FOR_CLUSTER",
                        "webster_1913_provenance": prov1913,
                        "webster_1789_provenance": prov1789
                    })

    # Determine constitution parser binding placeholder
    # Use first matching section prefix in truth graph context
    relevant_sections = []
    for e in entries:
        ctx = e.get("constitutional_context", "")
        if ctx:
            relevant_sections.append(ctx.split(";")[0].strip())
    if relevant_sections:
        preferred_section = relevant_sections[0]
    else:
        preferred_section = list(DOMAIN_RULES[domain]["articles"])[0]

    # Try to resolve a placeholder range
    bind = placeholder_ranges.get(preferred_section)
    if bind is None:
        # try article prefix match
        for sname, bnd in placeholder_ranges.items():
            if preferred_section.startswith(sname.split(" ")[0]):
                bind = bnd
                break
    if bind is None:
        bind = {
            "start_char_offset": None,
            "end_char_offset": None,
            "note": "placeholder; diff-graph-topology needed for exact character-offset parse ranges"
        }

    clusters[domain] = {
        "semantic_domain": domain,
        "member_dictionary_skill_paths": dict_skills,
        "shared_word_list": shared_words,
        "shared_blast_radius_domains": shared_blast[:50],
        "dominant_drift_classification": dom_drift,
        "drift_distribution": dict(drift_counts),
        "dictionary_coverage": {
            "webster_1913_sections_in_cluster": sorted(sections_in_cluster.get("webster-1913", [])),
            "source_files": [truth_graph_path.name, word_inventory_path.name, diff_path.name]
        },
        "coverage_gaps": coverage_gaps,
        "constitution_parser_binding": {
            "preferred_section_prefix": preferred_section,
            "parse_range": bind
        },
        "missing_in_cluster": missing_inventory_words[:100],
        "notes": (
            "Coverage gaps marked MISSING_FOR_CLUSTER where dictionary section lacks definition. "
            "Parser bindings are placeholders pending diff-graph-topology availability."
        )
    }

manifest = {
    "contract": "Skill-Cluster Manifest for Constitution Parser Bindings",
    "principle": "Cluster per-dictionary learn skills by semantic domain with MISSING_FOR_CLUSTER semantics; no fabrication. Parser bindings require diff-graph-topology.",
    "clusters_keyed_by_semantic_domain": list(DOMAIN_RULES.keys()),
    "cluster_count": len(DOMAIN_RULES),
    "source_artifacts": {
        "constitution_complete_word_inventory": str(word_inventory_path),
        "timelined_dictionary_diff": str(diff_path),
        "constitutional_structural_truth_graph": str(truth_graph_path),
        "constitution_source": str(constitution_text_path),
        "dictionary_skills_dir": "C:\\Users\\krist\\AppData\\Local\\hermes\\skills\\research\\legal-data\\dictionary-editions\\"
    },
    "clusters": clusters,
    "parser_binding_status": "PLACEHOLDER — exact character-offset ranges require diff-graph-topology"
}

with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)

print(f"Wrote manifest to {OUT_PATH}")
print("Cluster summary:")
for domain, data in manifest["clusters"].items():
    print(f"  {domain}: {len(data['shared_word_list'])} terms, drift={data['dominant_drift_classification']}, gaps={len(data['coverage_gaps'])}")
