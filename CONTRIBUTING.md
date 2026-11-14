# Adding your mod to the cuckywucky pack (instructions for your Claude)

This repo is a packwiz modpack manifest. Players' launchers fetch `pack.toml` and download only the jars that changed. Mods live in two places:

- **Modrinth mods** are listed by hash and CDN link (`mods/<slug>.pw.toml`). Nothing is hosted here.
- **Our own mods** (not on Modrinth) are uploaded as assets on this repo's GitHub release `mods`, and `mods/<slug>.pw.toml` points at the asset.

You are adding or updating **your own mod's jar**. Do not touch anyone else's files.

## 0. Get access (once)
The pack owner (`kiinect`) must invite your GitHub account as a collaborator with **Write** access. Tell your human to send the owner their GitHub username, then have them accept the invite at https://github.com/kiinect/cuckywucky-pack/invitations (or from the invite email).

Check access: `gh repo view kiinect/cuckywucky-pack --json viewerPermission` should say `WRITE` or `ADMIN`. If it doesn't, stop and tell your human; do not try to work around it.

## 1. Clone and set your identity
```
git clone https://github.com/kiinect/cuckywucky-pack.git
cd cuckywucky-pack
git config user.name "<your github username>"
git config user.email "<your username>@users.noreply.github.com"   # use the noreply address, not a private email; this repo is public
```

## 2. Publish your mod jar
Build your mod for **Minecraft 1.21.1, NeoForge 21.1.264** first. Then, from the repo root:

```
git pull --rebase
python3 tools/own_jars.py /path/to/yourmod-1.2.3.jar
python3 tools/refresh.py
git add mods index.toml pack.toml
git commit -m "yourmod 1.2.3"
git push
```

What that does:
- uploads the jar to the `mods` release (replacing the old jar of the same filename),
- writes `mods/<slug>.pw.toml` (the slug is the filename before the first `-<digit>`; `yourmod-1.2.3.jar` becomes `yourmod`),
- rebuilds `index.toml` and `pack.toml` so launchers see the change.

To ship an update later, rebuild the jar and repeat the same steps. Bumping the version in the filename is cleaner; a changed hash is what makes players re-download.

## Rules
- **Only your own mods.** Don't upload other authors' jars; if a mod is on Modrinth, the owner adds it with `tools/lookup.py` and nothing is hosted.
- **Don't run `tools/lookup.py`.** It scans the owner's Prism instance and rewrites every Modrinth entry. It's the owner's tool.
- **Never commit `.jar` files.** They are gitignored on purpose; jars go to the release only.
- **Don't edit other people's `mods/*.pw.toml`, and don't change `pack.toml`'s `[versions]`** without asking the owner.
- **If `git pull --rebase` conflicts** in `index.toml` or `pack.toml`, resolve by taking either side and re-running `python3 tools/refresh.py`; those two files are generated. Conflicts in any `mods/*.pw.toml` that isn't yours: stop and ask.
- **Mods must load with the rest of the pack.** Mixed versions break joining a shared server, so check that your mod's `neoforge.mods.toml` declares NeoForge 21.1 and Minecraft 1.21.1.
- **Don't put secrets or personal info in the repo.** It's public.

## 3. Check it worked
```
gh release view mods -R kiinect/cuckywucky-pack --json assets --jq '.assets[].name'   # your jar is listed
curl -s https://raw.githubusercontent.com/kiinect/cuckywucky-pack/main/mods/<slug>.pw.toml   # points at the release asset
```
Players pick it up on their next launch; they don't need to do anything.

## Owner note: inviting a friend
```
gh api -X PUT repos/kiinect/cuckywucky-pack/collaborators/<their-github-username> -f permission=push
```
Remove access later with `gh api -X DELETE repos/kiinect/cuckywucky-pack/collaborators/<username>`.
