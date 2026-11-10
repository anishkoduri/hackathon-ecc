# hackathon-ecc marketplace

A one-plugin marketplace containing `hackathon-ecc`: the hackathon version of ECC as a Cursor plugin.

## Layout

- `.cursor-plugin/marketplace.json` — the marketplace manifest (one plugin).
- `hackathon-ecc/` — the plugin itself (manifest, rules, skills, agents, commands).
- `build.sh` — reassembles `hackathon-ecc/` from its sources.

## Install

- **From the GitHub repo link (no Teams plan needed):** in Cursor, Customize → Plugins → add a plugin from a GitHub repo and paste `https://github.com/anishkoduri/hackathon-ecc`. Then install `hackathon-ecc` with **project scope** in a hackathon project.
- **From a Team Marketplace (Teams/Enterprise plan):** Dashboard → Plugins & MCPs → Team Marketplaces → Add Marketplace → Import from Repo → paste the repo URL → add and review the plugins with **Add to Marketplace** → find `hackathon-ecc` in Customize and install it with **project scope**.
- **From this local folder:** install the plugin from this directory directly in Cursor.

See `hackathon-ecc/README.md` for what's inside and what was left out on purpose.
