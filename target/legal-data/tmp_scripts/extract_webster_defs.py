
import json, re
from pathlib import Path
from html import unescape

ROOT = Path(r'C:\Users\krist\Desktop\constitutional-graph-tool\target\legal-data')
CACHE = Path(r'C:\Users\krist\AppData\Local\hermes\cache\web')
INVENTORY = ROOT / 'constitution-complete-word-inventory.json'
TIMELINE = ROOT / 'timelined-dictionary-diff.json'

SECTION_FILES = [
    ('A-B', CACHE / 'www.gutenberg.org-2e70926e5b.md'),
    ('C', CACHE / 'www.gutenberg.org-pg661-c-section.md'),
    ('D-E', CACHE / 'www.gutenberg.org-pg662-de-section.md'),
    ('F-G-H', CACHE / 'www.gutenberg.org-pg663-fgh-section.md'),
    ('I-partial', CACHE / 'www.gutenberg.org-355c4c959d.md'),
    ('M-N-O', CACHE / 'www.gutenberg.org-pg665-mno-section.md'),
    ('P-Q', CACHE / 'www.gutenberg.org-pg666-pq-section.md'),
    ('R', CACHE / 'www.gutenberg.org-pg667-r-section.md'),
    ('S', CACHE / 'www.gutenberg.org-pg668-s-section.md'),
    ('T-U-V-W', CACHE / 'www.gutenberg.org-00e3e8e1b8.md'),
    ('X-Y-Z', CACHE / 'www.gutenberg.org-dbc62300e1.md'),
]
START = '*** START OF THE PROJECT GUTENBERG EBOOK'
WORD_CONTEXT_BEFORE = 90
WORD_CONTEXT_AFTER = 260

inv = json.loads(INVENTORY.read_text(encoding='utf-8'))
items = inv['word_inventory']
lookup = {item['word']: item for item in items}

sections = []
for label, path in SECTION_FILES:
    text = path.read_text(encoding='utf-8', errors='ignore')
    idx = text.find(START)
    body = text[idx:] if idx != -1 else text
    body = re.sub(r'<[^>]+>', ' ', body)
    body = unescape(body)
    body = re.sub(r'[ \t]+', ' ', body)
    body = re.sub(r'\n{3,}', '\n\n', body)
    sections.append((label, body))


def extract_for_word(word):
    item = lookup.get(word)
    if item is None:
        return None
    found_1913 = []
    found_1789 = None
    for label, body in sections:
        idx = body.find(word)
        if idx == -1:
            continue
        start = max(0, idx - WORD_CONTEXT_BEFORE)
        end = min(len(body), idx + len(word) + WORD_CONTEXT_AFTER)
        snippet = body[start:end].strip()
        snippet = ' '.join(snippet.split())
        found_1913.append({'section': label, 'snippet': snippet, 'char_index': idx})

    if found_1913:
        best = sorted(found_1913, key=lambda x: x['char_index'])[0]
        item['webster_1913_definition'] = best['snippet']
        item['webster_1913_source_section'] = best['section']
        item['webster_1913_source_file'] = [path.name for label2, path in SECTION_FILES if label2 == best['section']][0]
        item['webster_1913_provenance'] = 'FOUND_IN_1913_SECTION'
    else:
        item['webster_1913_provenance'] = 'NOT_FOUND_IN_LOCAL_CACHE'
    # 1789 source was a dissertation; leave provenance explicit; partial hits may be unavailable.
    if item.get('webster_1789_definition', '').startswith('NO DEFINITION FOUND'):
        item['webster_1789_provenance'] = 'NO_1789_LEXICON_ENTRY'
    else:
        item['webster_1789_provenance'] = 'FOUND_IN_1789_ONLY'
    # Recompute drift classification
    a = item.get('webster_1789_provenance')
    b = item.get('webster_1913_provenance')
    if a == 'FOUND_IN_1789_ONLY' and b == 'FOUND_IN_1913_SECTION':
        item['drift_classification'] = 'found_in_both'
    elif b == 'FOUND_IN_1913_SECTION':
        item['drift_classification'] = 'found_in_1913_only'
    elif a == 'FOUND_IN_1789_ONLY':
        item['drift_classification'] = 'found_in_1789_only'
    else:
        item['drift_classification'] = 'not_found_in_local_cache'
    if found_1913:
        sections_used = sorted({x['section'] for x in found_1913})
        item['webster_1913_sections_used'] = sections_used
        item['webster_1913_hit_count'] = len(found_1913)
    else:
        item['webster_1913_sections_used'] = []
        item['webster_1913_hit_count'] = 0
    return item

for item in items:
    extract_for_word(item['word'])

INVENTORY.write_text(json.dumps(inv, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# Build aligned timelined diff
word_mapping = {}
for item in inv['word_inventory']:
    word_mapping[item['word']] = {
        'word': item['word'],
        'frequency_in_constitution': item.get('frequency_in_constitution'),
        'webster_1789_definition': item.get('webster_1789_definition'),
        'webster_1789_provenance': item.get('webster_1789_provenance'),
        'webster_1913_definition': item.get('webster_1913_definition'),
        'webster_1913_provenance': item.get('webster_1913_provenance'),
        'webster_1913_sections_used': item.get('webster_1913_sections_used', []),
        'webster_1913_hit_count': item.get('webster_1913_hit_count', 0),
        'drift_classification': item.get('drift_classification'),
        'meaning_drift': item.get('meaning_drift'),
    }
timeline = {'word_mapping': word_mapping, 'meta': {
    'total_words': len(word_mapping),
    'sources': [p.name for _, p in SECTION_FILES] + ['www.gutenberg.org-acbbf766e7.md'],
    'generated_from': 'local_gutenberg_cache_only'
}}
TIMELINE.write_text(json.dumps(timeline, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('updated_inventory=' + str(INVENTORY))
print('updated_timeline=' + str(TIMELINE))
