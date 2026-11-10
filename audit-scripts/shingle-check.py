import re, sys, pathlib

def prose_text(path):
    txt = pathlib.Path(path).read_text(errors='ignore')
    # strip frontmatter
    txt = re.sub(r'^---\n.*?\n---\n', '', txt, flags=re.S)
    # strip code blocks
    txt = re.sub(r'```.*?```', '', txt, flags=re.S)
    # strip inline code
    txt = re.sub(r'`[^`]*`', '', txt)
    # strip tables, headings, lists markers
    lines = []
    for ln in txt.splitlines():
        if ln.strip().startswith('|') or ln.strip().startswith('#'):
            continue
        lines.append(ln)
    txt = ' '.join(lines)
    # sentence-bounded: split into sentences
    sents = re.split(r'(?<=[.!?])\s+', txt)
    return sents

def grams(sents, n=10):
    out = set()
    for s in sents:
        words = re.findall(r"[a-z0-9']+", s.lower())
        for i in range(len(words)-n+1):
            out.add(tuple(words[i:i+n]))
    return out

def load_dir(d):
    g = set()
    for p in pathlib.Path(d).rglob('*.md'):
        g |= grams(prose_text(p))
    return g

src = load_dir('/tmp/orch-cand/claude-code-orchestrate')
ours = load_dir('/home/hatch/workspace/hackathon-plugin/new-skills/orchestrate')
shared = src & ours
print(f"source grams: {len(src)}")
print(f"ours grams: {len(ours)}")
print(f"shared: {len(shared)}")
for s in list(shared)[:15]:
    print(' '.join(s))
