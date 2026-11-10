import re, pathlib

def sentences(path):
    txt = pathlib.Path(path).read_text(errors='ignore')
    txt = re.sub(r'^---\n.*?\n---\n', '', txt, flags=re.S)
    txt = re.sub(r'```.*?```', '', txt, flags=re.S)
    txt = re.sub(r'`[^`]*`', '', txt)
    lines = []
    for ln in txt.splitlines():
        if ln.strip().startswith('|') or ln.strip().startswith('#'):
            continue
        lines.append(ln)
    txt = ' '.join(lines)
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', txt) if s.strip()]

def grams(sent, n=10):
    words = re.findall(r"[a-z0-9']+", sent.lower())
    return {tuple(words[i:i+n]) for i in range(len(words)-n+1)}

# build source gram -> (file, sentence)
src_map = {}
for p in pathlib.Path('/tmp/orch-cand/claude-code-orchestrate').rglob('*.md'):
    for s in sentences(p):
        for g in grams(s):
            src_map.setdefault(g, (str(p), s))

ours = []
for p in pathlib.Path('/home/hatch/workspace/hackathon-plugin/new-skills/orchestrate').rglob('*.md'):
    for s in sentences(p):
        for g in grams(s):
            if g in src_map:
                ours.append((str(p), s, src_map[g]))

# dedupe by our sentence
seen = set()
out = []
for f, s, (sf, ss) in ours:
    if s not in seen:
        seen.add(s)
        out.append((f, s, sf, ss))
print(f"our sentences with a shared 10-gram: {len(out)}")
for f, s, sf, ss in out[:12]:
    print("="*80)
    print(f"OURS [{pathlib.Path(f).name}]: {s[:300]}")
    print(f"SRC  [{pathlib.Path(sf).name}]: {ss[:300]}")
