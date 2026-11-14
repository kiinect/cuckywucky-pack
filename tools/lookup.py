#!/usr/bin/env python3
"""Matches every jar in the instance to Modrinth by hash and writes packwiz .pw.toml metafiles.
Jars Modrinth doesn't know are reported (custom jars are handled by tools/own_jars.py)."""
import glob, hashlib, json, os, sys, urllib.parse, urllib.request

INST = os.path.expanduser('~/.var/app/org.prismlauncher.PrismLauncher/data/PrismLauncher/instances/cuckywucky/minecraft')
OUT = os.path.join(os.path.dirname(__file__), '..')

def post(path, body):
    r = urllib.request.Request('https://api.modrinth.com/v2' + path, json.dumps(body).encode(), {'Content-Type': 'application/json', 'User-Agent': 'cuckywucky-pack/1.0'})
    return json.load(urllib.request.urlopen(r, timeout=60))

def get(path):
    r = urllib.request.Request('https://api.modrinth.com/v2' + path, headers={'User-Agent': 'cuckywucky-pack/1.0'})
    return json.load(urllib.request.urlopen(r, timeout=60))

def sha512(p):
    h = hashlib.sha512()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''): h.update(c)
    return h.hexdigest()

def run():
    files = sorted(glob.glob(INST + '/mods/*.jar'))
    hashes = {sha512(f): f for f in files}
    found = post('/version_files', {'hashes': list(hashes), 'algorithm': 'sha512'})
    proj_ids = sorted({v['project_id'] for v in found.values()})
    projs = {}
    for i in range(0, len(proj_ids), 100):
        for p in get('/projects?ids=' + urllib.parse.quote(json.dumps(proj_ids[i:i + 100]))): projs[p['id']] = p
    os.makedirs(OUT + '/mods', exist_ok=True)
    for h, v in found.items():
        p = projs[v['project_id']]
        fobj = next(f for f in v['files'] if f['hashes'].get('sha512') == h)
        side = 'both' if p['client_side'] != 'unsupported' and p['server_side'] != 'unsupported' else ('client' if p['server_side'] == 'unsupported' else 'server')
        name = p['title'].replace("'", "")
        toml = f"""name = '{name}'
filename = '{fobj['filename']}'
side = '{side}'

[download]
url = '{fobj['url']}'
hash-format = 'sha512'
hash = '{h}'

[update.modrinth]
mod-id = '{p['id']}'
version = '{v['id']}'
"""
        open(f"{OUT}/mods/{p['slug']}.pw.toml", 'w').write(toml)
    miss = [os.path.basename(f) for h, f in hashes.items() if h not in found]
    print(f'{len(found)} of {len(files)} matched on Modrinth')
    print('NOT on Modrinth:', *miss, sep='\n  ')

if __name__ == '__main__':
    run()
