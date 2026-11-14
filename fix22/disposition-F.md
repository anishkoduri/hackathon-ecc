# Fix #22 — Group F disposition (backgrounds, verification only)

Source skill: `~/workspace/cursor-skills/less-flat-ui/SKILL.md` (standalone global skill, outside the plugin).
Built copy: `~/workspace/hackathon-plugin/hackathon-ecc/skills/less-flat-ui/SKILL.md` (copied from the global skill by `build.sh:256-258`, plus 4 documented patch hunks — verified by `fix15/verify15.py`, 44/44 PASS).
Method: each treatment checked by its `### N. <name>` heading (word-boundary match on the full name). No treatment text was copied into the plugin — verification only, per SPEC §3.

| Item | Treatment | Global skill location | Built-tree location | Status |
|---|---|---|---|---|
| F1 | Felt texture | `less-flat-ui/SKILL.md:103` | `hackathon-ecc/skills/less-flat-ui/SKILL.md:107` | verified |
| F2 | Fluted glass | `less-flat-ui/SKILL.md:119` | `hackathon-ecc/skills/less-flat-ui/SKILL.md:123` | verified |
| F3 | Thermal gradients | `less-flat-ui/SKILL.md:141` | `hackathon-ecc/skills/less-flat-ui/SKILL.md:145` | verified |
| F4 | Water ripples | `less-flat-ui/SKILL.md:157` | `hackathon-ecc/skills/less-flat-ui/SKILL.md:161` | verified |
| F5 | Speckled graphite | `less-flat-ui/SKILL.md:172` | `hackathon-ecc/skills/less-flat-ui/SKILL.md:176` | verified |
| F6 | Single-hue landscapes | `less-flat-ui/SKILL.md:186` | `hackathon-ecc/skills/less-flat-ui/SKILL.md:190` | verified |
| F7 | Blueprint grids | `less-flat-ui/SKILL.md:198` | `hackathon-ecc/skills/less-flat-ui/SKILL.md:202` | verified |
| F8 | Halftone | `less-flat-ui/SKILL.md:216` | `hackathon-ecc/skills/less-flat-ui/SKILL.md:220` | verified |
| F9 | Grainy gradients | `less-flat-ui/SKILL.md:230` | `hackathon-ecc/skills/less-flat-ui/SKILL.md:234` | verified |
| F10 | Grass texture | `less-flat-ui/SKILL.md:242` | `hackathon-ecc/skills/less-flat-ui/SKILL.md:246` | verified |
| F11 | Dithered images | `less-flat-ui/SKILL.md:257` | `hackathon-ecc/skills/less-flat-ui/SKILL.md:261` | verified |
| F12 | Paper texture | `less-flat-ui/SKILL.md:275` | `hackathon-ecc/skills/less-flat-ui/SKILL.md:279` | verified |
| F13 | Contour lines | `less-flat-ui/SKILL.md:291` | `hackathon-ecc/skills/less-flat-ui/SKILL.md:295` | verified |
| F14 | Cloud sky | `less-flat-ui/SKILL.md:306` | `hackathon-ecc/skills/less-flat-ui/SKILL.md:310` | verified |
| F15 | Pixel mosaics | `less-flat-ui/SKILL.md:322` | `hackathon-ecc/skills/less-flat-ui/SKILL.md:326` | verified |
| F16 | Lens distortion | `less-flat-ui/SKILL.md:336` | `hackathon-ecc/skills/less-flat-ui/SKILL.md:340` | verified |
| F17 | Stippled gradients | `less-flat-ui/SKILL.md:360` | `hackathon-ecc/skills/less-flat-ui/SKILL.md:364` | verified |
| F18 | Square-dot grids | `less-flat-ui/SKILL.md:376` | `hackathon-ecc/skills/less-flat-ui/SKILL.md:380` | verified |
| F19 | Blurred photos | `less-flat-ui/SKILL.md:393` | `hackathon-ecc/skills/less-flat-ui/SKILL.md:397` | verified |
| F20 | Iridescent shapes | `less-flat-ui/SKILL.md:414` | `hackathon-ecc/skills/less-flat-ui/SKILL.md:418` | verified |
| F21 | Impressionist paintings | `less-flat-ui/SKILL.md:430` | `hackathon-ecc/skills/less-flat-ui/SKILL.md:434` | verified |
| F22 | ASCII and pixels | `less-flat-ui/SKILL.md:448` | `hackathon-ecc/skills/less-flat-ui/SKILL.md:452` | verified |
| #23 | Soft shadow | `less-flat-ui/SKILL.md:484` | `hackathon-ecc/skills/less-flat-ui/SKILL.md:488` | verified |

Notes:
- The skill's frontmatter (`less-flat-ui/SKILL.md:3`) and its source line (`:8`) both state 23 treatments; the catalogue heading is `## The 23 treatments` (`:101` global, `:104` built). No reference anywhere in the plugin states a stale count of 22 (see f-report.md §b).
- Built-tree heading lines are +4 vs the global file (design-decision pointer patch + wow-moment rule patch); the treatment bodies are otherwise identical — the only global-vs-built diffs are the 4 documented patch hunks (verify15 patch checks 1–4 PASS).
- All 23 verified present in both the global skill and the built tree. 23/23.
