#!/usr/bin/env python3
"""Publishes our own mods (not on Modrinth): uploads each jar to the GitHub release `mods` and writes its packwiz file.
Usage: python3 tools/own_jars.py <jar> [<jar> ...]   Re-run with a rebuilt jar to ship an update."""
import hashlib, os, re, subprocess, sys
REPO = 'kiinect/cuckywucky-pack'
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

for jar in sys.argv[1:]:
    fn = os.path.basename(jar)
    slug = re.split(r'-\d|-1\.21', fn)[0].lower().replace('_', '-')
    h = hashlib.sha512(open(jar, 'rb').read()).hexdigest()
    if subprocess.run(['gh', 'release', 'view', 'mods', '-R', REPO], capture_output=True).returncode:
        subprocess.run(['gh', 'release', 'create', 'mods', '-R', REPO, '--title', 'Mod jars', '--notes', 'Jars that are not on Modrinth. Served to the packwiz installer by pack.toml.'], check=True)
    subprocess.run(['gh', 'release', 'upload', 'mods', jar, '--clobber', '-R', REPO], check=True)
    open(f'{ROOT}/mods/{slug}.pw.toml', 'w').write(f"""name = '{slug}'
filename = '{fn}'
side = 'both'

[download]
url = 'https://github.com/{REPO}/releases/download/mods/{fn}'
hash-format = 'sha512'
hash = '{h}'
""")
    print('published', slug, fn)
