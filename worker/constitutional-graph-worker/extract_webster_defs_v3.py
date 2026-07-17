
import json, re
from pathlib import Path

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


def extract_word_from_body(body: str, word: str):
 sensors = []
 flagged_words_to_track = []
 # strip tags, newlines collapsed; keep body between start marker and a later practical cut if needed
    text = re.sub(r'<[^>]+>', ' ', body)
    text = text.replace('&amp;', '&').replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>')
    text = re.sub(r'[ \t]+', ' ', text, flags=re.MULTILINE)
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    # Find occurrences of capitalized isolate headword form only, with minimal entropy around it
    # Look for line starts or paragraph starts beginning with word followed by space/punct/etc
    best = None
    best_score = -1
    occurrences = []
    pattern = re.compile(r'(?:(?<=^)|(?<=\n)|(?<=[.!?]\s))(' + re.escape(word) + r')(?=[\s,.;:(\[]|[A-Z][a-z])', re.IGNORECASE)
    for m in pattern.finditer(text):
        start = max(0, m.start()-120)
        end = min(len(text), m.end()+340)
        ctx = text[start:end]
        if re.search(r'\b\d+\.\s', ctx):
            score = 3
        elif re.search(r'\b(n\.|v\. t\.|v\. i\.|a\.|p\. p\.|adv\.|prep\.|conj\.|pron\.|interj\.)\b', ctx):
            score = 4
        else:
            score = 1
        occurrences.append((score, m.start(), ctx))
    if not occurrences:
        return None, 0
    occurrences.sort(reverse=True, key=lambda x: (x[0], x[1]))
    for score, idx, ctx in occurrences[:5]:
        snippet = ' '.join(ctx.split())
        if score > best_score and len(snippet) >= 60:
            best_score = score
            best = snippet
    if not best and occurrences:
        snippet = ' '.join(occurrences[0][2].split())
        if len(snippet) >= 30:
            best = snippet
    return best, len(occurrences)

inv = json.loads(INVENTORY.read_text(encoding='utf-8'))
items = inv['word_inventory']
word_written = 0
word_not_found = 0
maybe_suspect = []
for item in items:
    word = item['word']
    found = None
    source = None
    hit_count = 0
    for label, path in SECTION_FILES:
        text = path.read_text(encoding='utf-8', errors='ignore')
        idx_marker = text.find(START)
        body = text[idx_marker:] if idx_marker != -1 else text
        snippet, hits = extract_word_from_body(body, word)
        if snippet:
            found = snippet
            source = label
            hit_count += hits
    if found and found not in ('', None):
        item['webster_1913_definition'] = found
        item['webster_1913_provenance'] = 'FOUND_IN_1913_SECTION'
        item['webster_1913_source_section'] = source
        item['webster_1913_hit_count'] = hit_count
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
if maybe_suspect:
    print('maybe_suspect=' + str(len(maybe_suspect)))
