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
