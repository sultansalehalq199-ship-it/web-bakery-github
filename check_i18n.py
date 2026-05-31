import re
from pathlib import Path
path = Path('index.html')
text = path.read_text(encoding='utf-8')
keys = sorted(set(re.findall(r'data-i18n="([^"]+)"', text)))
placeholder_keys = sorted(set(re.findall(r'data-i18n-placeholder="([^"]+)"', text)))
obj_match = re.search(r'const translations = \{(.*?)\};', text, re.S)
if not obj_match:
    raise SystemExit('translations object not found')
obj = obj_match.group(1)
id_block_match = re.search(r'id:\s*\{(.*?)\}\s*,\s*en:\s*\{', obj, re.S)
en_block_match = re.search(r'en:\s*\{(.*?)\}\s*$', obj, re.S)
if not id_block_match or not en_block_match:
    raise SystemExit('could not parse id/en blocks')
id_block = id_block_match.group(1)
en_block = en_block_match.group(1)
keys_id = set(re.findall(r'([a-zA-Z0-9_]+):\s*\'', id_block))
keys_en = set(re.findall(r'([a-zA-Z0-9_]+):\s*\'', en_block))
missing = [k for k in keys if k not in keys_id and k not in keys_en]
missing_ph = [k for k in placeholder_keys if k not in keys_id and k not in keys_en]
print('data-i18n keys:', len(keys))
print('placeholder keys:', len(placeholder_keys))
print('id translation keys:', len(keys_id))
print('en translation keys:', len(keys_en))
print('missing data-i18n keys:', missing)
print('missing placeholder keys:', missing_ph)
