# fix31 run log

## Errors (0)
- none

## Changes (11)
- census: all 5 new skills present with SKILL.md + frontmatter; hairline engine/checks/examples/LICENSE vendored
- census: DESIGNPKG-AUTO block byte-identical in orchestrate + hackathon-mode
- census: pin census holds (grok-4.7-extra-high x49, 'Grok 4.7 Extra High' x22, cursor-grok-4.6-high-fast x70, grok-4.7-high x0, 'Grok 4.7 High' x0); zero pin text in the 5 new skills
- license: no MCP calls / no frozen GetLayers counts; react-bits + gsap + getlayers skill dirs contain only their SKILL.md (no vendored source)
- README.md: substituted '67 skills, 45 agents, 48 rules, and 55 commands in' ...
- README.md: substituted '67 skills widen the routing surface' ...
- README.md: substituted '56 MB and 67 skills against a minimal set' ...
- README.md: substituted 'structured process — 67 skills, 45 agents, 55 comm' ...
- README: fix31 provenance note added after the codebase-memory line
- trigger coverage.skills 67 -> 72 (withTriggers stays 49 — no trigger keys for the new skills)
- post: README 72 in all 4 lines, zero '67 skills' tree-wide; trigger coverage 72/49; DESIGNPKG-AUTO + GLOBAL-ROUTING blocks byte-identical

## Command decisions (7)
- DECISION-31-1 (SPEC scope): five new skills, not four — Hairline is two skills (hairline-create + hairline-adopt) per the SPEC; GetLayers, GSAP, and React Bits are one skill each. Skills 67 -> 72; agents 45, rules 48, commands 55, hooks 15, triggers 49 unchanged.
- DECISION-31-2 (GSAP version): the SPEC's 3.15.0 (Apr 2026) is superseded — npm latest is 3.15.1 (verified Nov 17, 2026), matching the inventory's existing pin. The skill pins gsap@3.15.1. The SPEC is corrected with a strikethrough note (audit #97-A to confirm).
- DECISION-31-3 (GetLayers counts): live counts drifted in one day (llms.txt Nov 17: 62 templates / 222 3D scenes / 54 sections / 530 backgrounds / 1,088 gradients vs the SPEC's 50 / 114 / 10 / 276 / 1,088) — the SPEC's own no-frozen-counts rule is confirmed necessary. The skill carries NO counts; verify31 forbids the frozen Nov 16 figures.
- DECISION-31-4 (staged weave, not built-tree patching): the palette / DESIGNPKG-AUTO / inventory edits are staged sources (fix31/weave31.py, run once) flowing through the STEP 2 copy — the same pattern as fix29's staged halves. fix31.py only asserts the built tree + updates the generated files (README, trigger) that no staged source owns.
- DECISION-31-5 (GSAP skills not vendored): the official gsap-skills repo (8 skills, MIT) is reference, not vendored — vendoring 8 skills would take the count to 80 for API detail this plugin's single gsap skill routes to by link. The skill's reference table names the skill per need. If a future fix finds agents need the API text in-tree, vendoring is a separate decision.
- DECISION-31-6 (React Bits install): the CLI installs from the live repo (per the SPEC), not the fix22 pinned commit — the installed copy in the project IS the pin, recorded in the decision record. The fix22 commit stays as the reviewed baseline in the skill and the inventory.
- DECISION-31-7 (GetLayers weight — direction update, Anish Nov 16 ~10:02 PM): GetLayers prompts are a first-class, high-priority source in the palette-first flow — consulted FIRST, before the other palette sources, and the direction leans on the layers heavily as its foundation. Visible three ways: ordering (getlayers first in every palette list), priority language (in the skill + the DESIGNPKG-AUTO gloss + the inventory §12), and the citation check (the direction names the GetLayers layers USED or CONSIDERED-AND-REJECTED with a D19 reason, same as every inventory entry). Weight is about consultation order and foundation weight, NOT about forcing a layer: a surface with no fitting free layer records `not considered — <reason>`, same as any entry. Constraints unchanged: free set only, no vendored content, foundation not finished brand.

## OWED (4)
- OWED-31-1 (SPEC Honest limits): live behavior of the four resources is unverified until real project use — the live smoke test is still skipped since Nov 15. The dry-run design leg (dry-run #46) is static + install-verified, not a live Cursor build.
- OWED-31-2 (GetLayers MCP): the MCP stays unwired — it requires the Full Stack Lifetime plan. If Anish ever buys Full Stack, MCP wiring is a separate decision; the skill's prompt path is the free path.
- OWED-31-3 (call map, same as OWED-30-4): the call map (skills/orchestrate/references/call-map.md) is generator-owned and NOT regenerated in this fix — the new skills are leaf resources (invoked by the design-lead), not dispatchers; no new orchestration edges, so the fix28 map stands. If the audit finds the DESIGNPKG-AUTO additions are dispatch edges, regeneration is the fix.
- OWED-31-4 (Hairline 'six figures' text): the vendored hairline-create SKILL.md says 'The six figures of @lucasmarkes/hairline are the bar' — upstream's text about the original six; the library now ships 33 figures. Left as upstream wrote it (the vendored copy is unmodified apart from the framing header).
