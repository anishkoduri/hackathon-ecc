# Design Glossary — fix #22 Group G

Anchor token: `GLOSSARY_F22`

Vocabulary for the design package: one-line definitions so agents use these
words correctly (kerning vs tracking vs leading; stagger vs shared element
transition). Terms are VOCABULARY, not rules — a term's owning skill is where
the concept is applied; this glossary is where it is defined. Nothing here
adds enforcement. Each owning skill carries a one-line pointer back to this
file (see `fix22/g-pointers.md`); terms are NOT duplicated into the owning
skills. Source: the "20 Design Terms You Should Know" reel (fix #22 SPEC §1,
Group G). Home: `skills/design-taste-frontend/references/design-glossary.md`
— alongside the design-taste-frontend references, where the design package's
vocabulary lives; `build.sh` copies `new-skills/design-taste-frontend/`
verbatim, so this file lands in the built tree with no `build.sh` edit and no
new skill.

| Term | Definition | Owning skill |
|---|---|---|
| G1 Kerning | The space between a specific pair of characters, adjusted so that pair looks evenly spaced. | ui-ux-pro-max (font rules / type scale) |
| G2 Optical centre | The visual centre of a shape or layout, placed slightly above the geometric centre so it looks balanced rather than sitting low. | ui-ux-pro-max (font rules / type scale) |
| G3 Tabular numbers | Figures that all share the same width, so columns of numbers align and a changing digit does not shift the layout. | ui-ux-pro-max (type rules) |
| G4 Layout shift | Visible content moving after it first appears, usually because something above it loaded late or resized. | ui-ux-pro-max + the existing layout-shift QA flag ("Flag layout shifts > 5px") |
| G5 Tracking | Uniform letter-spacing applied across a whole run of text, as opposed to the spacing between one pair of characters. | ui-ux-pro-max (font rules / type scale) |
| G6 Optimistic update | Showing the expected result of an action at once, before the server confirms it, and rolling it back visibly if the action fails. | ui-ux-pro-max |
| G7 x-height | The height of a typeface's lowercase letters without ascenders or descenders — the height of the letter x. | ui-ux-pro-max (font rules / type scale) |
| G8 Touch target | The tappable area of a control, sized so a finger can hit it reliably (44x44px minimum on the plugin's craft floor; the visible mark may stay smaller with an enlarged hit area). | ui-ux-pro-max (Fitts's law, A13; 44x44px minimum (the plugin floor, W2-C4)) |
| G9 Leading | The vertical space between lines of text, measured baseline to baseline. | ui-ux-pro-max (font rules / type scale) |
| G10 Origin-aware animation | Motion that starts from, or returns to, the element that triggered it, so the eye can follow where it came from and where it goes back to. | motion-patterns (enter/exit from the trigger, B11/B12) |
| G11 OKLCH | A perceptually uniform color space (lightness, chroma, hue) in which equal numeric steps look like equal visual steps. | ui-ux-pro-max (color tokens) |
| G12 Widow | A single word, or a very short line, left alone at the end of a paragraph or at the top of a new page or column. | ui-ux-pro-max (font rules / type scale) |
| G13 Safe area | The region of a phone screen clear of the notch, home indicator, and rounded corners, where content and controls stay usable. | ui-ux-pro-max + `references/pro-rules.md` (safe areas) |
| G14 Stagger | Starting a series of similar animations a short beat apart (30ms between list rows) instead of all at once. | motion-patterns (stagger example + 30ms token) |
| G15 Line length | The number of characters per line of running text, kept readable by capping prose at about 65–75 characters. | ui-ux-pro-max (font rules / type scale) |
| G16 Affordance | A visible clue in a control's appearance that suggests what it does and how to use it. | ui-ux-pro-max |
| G17 Combobox | A text field combined with a dropdown list, letting the user type to filter the options or pick one from the list. | ui-ux-pro-max |
| G18 Interruptible animation | An animation that can be retargeted or reversed mid-flight from its current on-screen position, instead of restarting or locking input until it finishes. | motion-foundations (retarget mid-flight; cf. B14, don't tween while held) |
| G19 Progressive disclosure | Showing only what is needed now, and revealing further detail or options when the user asks for them. | ui-ux-pro-max |
| G20 Shared element transition | One element appearing to move and resize between two screens or states, carried across by a shared identifier rather than replaced by a new element. | motion-patterns (shared-element example; `layoutId` reuse, B20) |

## Dedupe cross-references (SPEC §5 — one concept, one home)

- G20 = B20 (reuse `layoutId`): primary home is the motion-patterns
  shared-element example plus this glossary entry; B20 points at it.
- G14 = B3/B6 (stagger): primary home is the motion-patterns stagger
  example + 30ms token plus this glossary entry.
- G3 = D18 (tabular numbers): primary home is the ui-ux-pro-max type
  rules plus this glossary entry.
- G8 = A14 (bigger hit areas) = the 44x44px floor (W2-C4):
  primary home is the existing hit-area rule, now named as Fitts's law
  (A13); this glossary entry points at it.
- G10 = B11/B12 (enter/exit from the trigger): primary home is
  motion-patterns; this glossary entry points at it.
- G18 ~ B14 (don't tween while held): related, keep both, cross-reference.
