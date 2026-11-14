#!/usr/bin/env python3
"""Rebuilds index.toml and pack.toml (what `packwiz refresh` does). Run after any change under mods/."""
import glob, hashlib, os, re
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sha = lambda b: hashlib.sha256(b).hexdigest()

files = sorted(os.path.relpath(p, ROOT).replace(os.sep, '/') for p in glob.glob(ROOT + '/**/*.pw.toml', recursive=True))
idx = 'hash-format = "sha256"\n\n' + ''.join(f'[[files]]\nfile = "{f}"\nhash = "{sha(open(os.path.join(ROOT, f), "rb").read())}"\nmetafile = true\n\n' for f in files)
open(ROOT + '/index.toml', 'w').write(idx)

pack = open(ROOT + '/pack.toml').read()
pack = re.sub(r'(\[index\][^\[]*?hash = )"[0-9a-f]*"', lambda m: m.group(1) + f'"{sha(idx.encode())}"', pack, flags=re.S)
open(ROOT + '/pack.toml', 'w').write(pack)
print(f'index: {len(files)} mods')

# README: just what is in the pack
own, other = [], []
for f in files:
    t = open(os.path.join(ROOT, f)).read()
    name = re.search(r"name = ['\"](.+?)['\"]", t).group(1)
    (own if 'releases/download/mods/' in t else other).append(name)
mc = re.search(r'minecraft = "(.+?)"', pack).group(1); nf = re.search(r'neoforge = "(.+?)"', pack).group(1)
extra = ['chromeware', 'grandsigil', 'let_it_walk', 'walker-pistons']
open(ROOT + '/README.md', 'w').write(f"# cuckywucky pack\n\nMinecraft {mc} - NeoForge {nf}\n\n## Custom mods\n\n" + ''.join(f'- {n}\n' for n in sorted(own, key=str.lower))
    + f"\n## Mods ({len(other)})\n\n" + ''.join(f'- {n}\n' for n in sorted(other, key=str.lower))
    + "\n## Not hosted here\n\n" + ''.join(f'- {n}\n' for n in extra))
