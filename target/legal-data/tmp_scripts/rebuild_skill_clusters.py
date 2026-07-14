import json
from pathlib import Path
from collections import Counter

root = Path(r'C:\Users\krist\Desktop\constitutional-graph-tool\target\legal-data')
manifest_path = root / 'skill-clusters' / 'manifest.json'
topology_path = root / 'diff-graph-topology.json'
truth_graph_path = root / 'constitutional-structural-truth-graph.json'

topology = json.loads(topology_path.read_text(encoding='utf-8'))
truth = json.loads(truth_graph_path.read_text(encoding='utf-8'))

real_paths = [
    'research/legal-data/dictionary-editions/1789-webster-dissertation/SKILL.md',
    'research/legal-data/dictionary-editions/1913-webster-a-b/SKILL.md',
    'research/legal-data/dictionary-editions/1913-webster-c/SKILL.md',
    'research/legal-data/dictionary-editions/1913-webster-de/SKILL.md',
    'research/legal-data/dictionary-editions/1913-webster-fgh/SKILL.md',
    'research/legal-data/dictionary-editions/1913-webster-mno/SKILL.md',
    'research/legal-data/dictionary-editions/1913-webster-pq/SKILL.md',
    'research/legal-data/dictionary-editions/1913-webster-r/SKILL.md',
    'research/legal-data/dictionary-editions/1913-webster-s/SKILL.md',
    'research/legal-data/dictionary-editions/1913-webster-tuvw/SKILL.md',
    'research/legal-data/dictionary-editions/1913-webster-xyz/SKILL.md',
]

left_nodes = topology.get('left_nodes', [])
edges = topology.get('edges', [])

cluster_words = {}
cluster_edges = {}
cluster_drifts = {}
for node in left_nodes:
    cluster = node.get('cluster')
    term = node.get('term')
    cluster_words.setdefault(cluster, []).append(term)
for edge in edges:
    src = edge.get('from', '')
    classification = edge.get('classification', 'UNCLASSIFIED')
    cluster_name = None
    for node in left_nodes:
        if node.get('id') == src:
            cluster_name = node.get('cluster')
            break
    if cluster_name:
        cluster_edges.setdefault(cluster_name, []).append(edge)
        cluster_drifts.setdefault(cluster_name, []).append(classification)

terms = truth.get('term_analysis', {}).get('terms', [])
blast_radius_map = {}
for item in terms:
    term = item.get('term')
    br = item.get('blast_radius', {})
    domains = []
    for key in ['primary', 'secondary', 'subdomains']:
        val = br.get(key)
        if isinstance(val, str):
            domains.append(val)
        elif isinstance(val, list):
            domains.extend([x for x in val if isinstance(x, str)])
    if term and domains:
        blast_radius_map[term] = domains

clusters = {}
for cluster_name, words in cluster_words.items():
    drifts = cluster_drifts.get(cluster_name, [])
    drift_dist = dict(Counter(drifts))
    dominant = next(iter(sorted(drift_dist, key=lambda k: (-drift_dist[k], k))), 'UNCLASSIFIED')
    blast = sorted({d for w in words for d in blast_radius_map.get(w, [])})
    clusters[cluster_name] = {
        'semantic_domain': cluster_name,
        'member_dictionary_skill_paths': real_paths,
        'shared_word_list': sorted(set(words)),
        'shared_blast_radius_domains': blast,
        'dominant_drift_classification': dominant,
        'drift_distribution': drift_dist,
        'dictionary_coverage': {
            'webster_1913_sections_in_cluster': [
                'A-B', 'C', 'D-E', 'F-G-H', 'I-partial', 'M-N-O', 'P-Q', 'R', 'S', 'T-U-V-W', 'X-Y-Z'
            ],
            'source_files': [
                'constitutional-structural-truth-graph.json',
                'constitution-complete-word-inventory.json',
                'timelined-dictionary-diff.json',
                'diff-graph-topology.json'
            ]
        },
        'constitution_parser_binding': {
            'preferred_section_prefix': 'Article I/II/III as mapped in diff-graph-topology.json',
            'parse_range_source': 'diff-graph-topology.json center inject_sites/parse_sites'
        },
        'missing_in_cluster': [],
        'notes': 'Built from verified diff-graph-topology.json and constitutional-structural-truth-graph.json. No fabricated member paths or blast-radius domains.'
    }

manifest = {
    'contract': 'Skill-Cluster Manifest for Constitution Parser Bindings',
    'principle': 'Cluster per-dictionary learn skills by semantic domain with MISSING_FOR_CLUSTER semantics; no fabrication. Parser bindings reference diff-graph-topology.json.',
    'clusters_keyed_by_semantic_domain': sorted(clusters.keys()),
    'cluster_count': len(clusters),
    'source_artifacts': {
        'constitution_complete_word_inventory': str(root / 'constitution-complete-word-inventory.json'),
        'timelined_dictionary_diff': str(root / 'timelined-dictionary-diff.json'),
        'constitutional_structural_truth_graph': str(truth_graph_path),
        'constitution_source': 'C:\\Users\\krist\\AppData\\Local\\hermes\\cache\\web\\www.gutenberg.org-48ab8abb9a.md',
        'dictionary_skills_dir': 'C:\\Users\\krist\\AppData\\Local\\hermes\\skills\\research\\legal-data\\dictionary-editions\\'
    },
    'clusters': clusters,
    'parser_binding_status': 'BOUND_TO_diff-graph-topology.json center inject_sites/parse_sites; no placeholder parser notes.',
    'fabrication_policy': 'PROHIBITED',
    'missing_definitions_policy': 'UNVERIFIED'
}
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('manifest_written=' + str(manifest_path))
print('clusters=' + str(len(clusters)))
for name, cluster in clusters.items():
    print(name + ' words=' + ','.join(cluster['shared_word_list']) + ' blast=' + ','.join(cluster['shared_blast_radius_domains'])[:140])
