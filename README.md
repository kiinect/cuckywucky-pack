# cuckywucky pack

Auto-updating modpack for Prism Launcher (Minecraft 1.21.1, NeoForge 21.1.264). Every launch downloads only the mods that changed.

## Friends: one-time setup
1. Install [Prism Launcher](https://prismlauncher.org) and create an instance: **Minecraft 1.21.1 + NeoForge 21.1.264**.
2. Download [packwiz-installer-bootstrap.jar](https://github.com/packwiz/packwiz-installer-bootstrap/releases/latest) into the instance's `minecraft` folder (right-click the instance → Folder → Minecraft (`.minecraft`)).
3. Instance → Edit → Settings → **Custom commands** → tick *Custom commands* and set **Pre-launch command**:
   ```
   "$INST_JAVA" -jar packwiz-installer-bootstrap.jar -g -s client https://raw.githubusercontent.com/kiinect/cuckywucky-pack/main/pack.toml
   ```
4. Launch. The first run downloads everything (~500 MB, once). After that each launch only fetches changed mods.
5. Five mods are not redistributed here; the pack owner sends them once: `chromeware`, `grandsigil`, `let_it_walk`, `onepiececombat`, `walker-pistons` (put them in `mods/`).

## Owner: shipping an update
- **Own mod changed** (rebuilt jar): `python3 tools/own_jars.py path/to/new.jar && python3 tools/refresh.py && git add -A && git commit -m "update" && git push`
- **Modrinth mod added/updated** (in your instance): `python3 tools/lookup.py && python3 tools/refresh.py`, then commit and push.
- Friends get it next launch. Only the changed jars download.

`tools/lookup.py` matches the instance's jars to Modrinth by hash. `tools/own_jars.py` uploads our jars to the `mods` release. `tools/refresh.py` rebuilds `index.toml` and `pack.toml`.
