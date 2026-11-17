---
name: hairline-adopt
description: Use when someone has an SVG (an icon, a logo, an illustration) and wants it as a Hairline figure, or runs /hairline-adopt with a file. Reads the drawing, rebuilds its object as an isometric line figure on the engine of @lucasmarkes/hairline, and gives it a gesture that answers the pointer.
argument-hint: "<file.svg> [what the pointer does]"
---

> **Hackathon-ecc note (fix #31, HAIRLINE_F31).** Vendored from Hairline (`github.com/lucasmarkes/hairline`, Lucas Marques, MIT — see LICENSE): the skill is unmodified apart from this header. It reads one SVG and rebuilds its object as a Hairline figure by invoking the `hairline-create` skill in this plugin (the upstream text says "Invoke `/hairline-create`" — in this plugin that means the `hairline-create` skill, invoked by name). The figure it writes follows the same rules as `hairline-create`: theme-matched, D19-recorded, hero art / section illustration / empty state. This is Hairline illustrations — NOT Hairline UI (hairlineui.com), a different product that is not in scope.

# Hairline: adopt a drawing

The person has a drawing and wants it alive, as a Hairline figure. This skill reads the drawing, rebuilds its object as solids on Hairline's engine, and gives it a gesture. It never animates the SVG itself, and it never traces it: the drawing gives the identity, and the figure is built new, with its proportions and its parts.

## What it needs

- One `.svg` file: an icon, a logo, an illustration. Given several, make one figure at a time: ask which comes first.
- Optionally, what the pointer should do to it. Without it, the concepts propose the gesture.

## What to do

Invoke `/hairline-create` with the file's path and, after it, whatever the person said about the gesture, in their words. Its step 0 reads the drawing and fixes the object and its parts; its concepts then keep them and differ in the gesture, or, when the gesture was given, in the form and the read-out. Everything after that, the build, the check and the hand-over, is that skill's.

## What to say

When you offer the concepts, say first, in one line, what you read the drawing as and which of its parts you kept. If the person corrects the reading, read it again their way before any concept is built.

If the drawing is a mark that belongs to someone else, say so at hand-over: the page shows another company's mark, and it is theirs to publish or not.
