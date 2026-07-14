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
CONTEXT_BEFORE = 120
CONTEXT_AFTER = 320


def clean_section(text: str) -> str:
    idx = text.find(START)
    body = text[idx:] if idx != -1 else text
    body = re.sub(r'<[^>]+>', ' ', body)
    body = unescape(body)
    body = re.sub(r'[ \t]+', ' ', body)
    body = re.sub(r'\n{3,}', '\n\n', body)
    return body


def extract_snippet(body: str, word: str, max_len: int = 420):
    pattern = (
        r'.{0,' + str(CONTEXT_BEFORE) + r'}\b' +
        re.escape(word) + r'\b.{0,' + str(CONTEXT_AFTER) + r'}'
    )
    matches = list(re.finditer(pattern, body, flags=re.DOTALL | re.IGNORECASE))
    if not matches:
        return None, 0
    best = None
    best_score = -1
    for m in matches:
        ctx = m.group(0)
        score = 0
        if re.search(r'\b\d+\.\s', ctx):
            score += 2
        if re.search(r'\[(?:Obs|R|It|L|NL|Gr|OE|AS|F|MD|MHG|OHG|OF|Sk|Dan|Sw|D|G|Sp|Port|I|H|Cf|See|Also)\b', ctx):
            score += 1
        if re.search(r'\b(n\.|v\. t\.|v\. i\.|a\.|p\. p\.|adv\.|prep\.|conj\.|pron\.|interj\.)\b', ctx):
            score += 2
        if score > best_score:
            best_score = score
            best = ctx
    snippet = ' '.join((best or matches[0].group(0)).split())
    return snippet[:max_len] if snippet else None, len(matches)


inv = json.loads(INVENTORY.read_text(encoding='utf-8'))
items = inv['word_inventory']
word_written = 0
word_not_found = 0
for item in items:
    word = item['word']
    found_1913 = []
    for label, path in SECTION_FILES:
        text = path.read_text(encoding='utf-8', errors='ignore')
        body = clean_section(text)
        snippet, hits = extract_snippet(body, word)
        if snippet:
            found_1913.append((label, snippet, hits))
    if found_1913:
        label, snippet, _ = found_1913[0]
        item['webster_1913_definition'] = snippet
        item['webster_1913_provenance'] = 'FOUND_IN_1913_SECTION'
        item['webster_1913_source_section'] = label
        item['webster_1913_hit_count'] = sum(h for _, _, h in found_1913)
        word_written += 1
    else:
        item['webster_1913_provenance'] = 'NOT_FOUND_IN_LOCAL_CACHE'
        item['webster_1913_hit_count'] = 0
        word_not_found += 1
    if item.get('webster_1789_definition', '').startswith('NO DEFINITION FOUND'):
        item['webster_1789_provenance'] = 'NO_1789_LEXICON_ENTRY'
    else:
        item['webster_1789_provenance'] = 'FOUND_IN_1789_ONLY'
    p1789 = item.get('webster_1789_provenance')
    p1913 = item.get('webster_1913_provenance')
    if p1789 == 'FOUND_IN_1789_ONLY' and p1913 == 'FOUND_IN_1913_SECTION':
        item['drift_classification'] = 'found_in_both'
    elif p1913 == 'FOUND_IN_1913_SECTION':
        item['drift_classification'] = 'found_in_1913_only'
    elif p1789 == 'FOUND_IN_1789_ONLY':
        item['drift_classification'] = 'found_in_1789_only'
    else:
        item['drift_classification'] = 'not_found_in_local_cache'
INVENTORY.write_text(json.dumps(inv, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

word_mapping = {}
for item in inv['word_inventory']:
    word_mapping[item['word']] = {
        'word': item['word'],
        'frequency_in_constitution': item.get('frequency_in_constitution'),
        'webster_1789_definition': item.get('webster_1789_definition'),
        'webster_1789_provenance': item.get('webster_1789_provenance'),
        'webster_1913_definition': item.get('webster_1913_definition'),
        'webster_1913_provenance': item.get('webster_1913_provenance'),
        'webster_1913_hit_count': item.get('webster_1913_hit_count', 0),
        'drift_classification': item.get('drift_classification'),
        'meaning_drift': item.get('meaning_drift'),
    }
timeline = {'word_mapping': word_mapping, 'meta': {
    'total_words': len(word_mapping),
    'generated_from': 'local_gutenberg_cache_only',
    'note': 'Definitions are raw snippets from local cached Gutenberg sections. Provenance flags indicate source coverage; not all words have clean 1913 headword entries.'
}}
TIMELINE.write_text(json.dumps(timeline, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('updated_inventory=' + str(INVENTORY))
print('updated_timeline=' + str(TIMELINE))
print('word_written=' + str(word_written) + ' word_not_found=' + str(word_not_found))
