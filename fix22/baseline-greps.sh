#!/bin/bash
# Word-boundary baseline greps for fix #22 Groups C + D. Searches build.sh, built tree, staged sources.
cd ~/workspace/hackathon-plugin
OUT=fix22/baseline-greps.txt
: > "$OUT"
check() {
  local label="$1"; shift
  echo "=== $label ===" >> "$OUT"
  for pat in "$@"; do
    echo "--- pattern: $pat" >> "$OUT"
    grep -rniP --exclude-dir=node_modules --exclude='*.bundle' "$pat" build.sh hackathon-ecc/ round2-skills/ new-skills/ 2>/dev/null | head -12 >> "$OUT"
    echo "(hits above, max 12 per pattern)" >> "$OUT"
  done
}
check "C1 tags&pills" '\bpill\b' '\bbadge\b' '\btag\b'
check "C2 italics" '\bitalic\b' '\bitalics\b'
check "C3 Instrument Serif" 'Instrument Serif'
check "C4 kerning" '\bkerning\b' 'negative kerning'
check "C5 detailed UI" 'over-the-top' 'overly detailed'
check "C6 dividers" '\bdivider\b' '\bdividers\b'
check "C7 shades/opacities" '\bshade\b' '\bshades\b' '\bopacity\b'
check "C8 bordered containers" '\bbordered\b' 'containers with borders'
check "C9 diagrams" '\bdiagram\b' '\bdiagrams\b' '\bflowchart\b'
check "C10 verbose/redundant" '\bverbose\b' '\bredundant\b'
check "C11 breadcrumbs" '\bbreadcrumb\b'
check "C12 section numbering" 'section number' 'numbered section'
check "C13 eyebrows" '\beyebrow\b' '\bkicker\b'
check "C14 dithering" '\bdither'
check "C15 ASCII" '\bASCII\b'
check "C16 squircles" '\bsquircle\b'
check "C17 mono" '\bmonospace\b' '\bmono\b'
check "C18 ALL CAPS" 'all-caps' 'ALL CAPS' 'all caps'
check "C19 gradient" '\bgradient\b'
check "C20 periods in titles" '\bperiod\b'
check "D1 filler badges" 'filler badge' 'filler'
check "D2 redundant labels" 'redundant label'
check "D3 unitalicize" 'unitalic'
check "D5 design system" 'design system'
check "D6 actual product" 'actual product' 'show the product'
check "D7 enlarge main feature" '\benlarge\b' 'main feature'
check "D8 spacing grouping" 'group with spacing'
check "D9 specific headlines" 'specific headline' 'headline.*specific'
check "D10 emphasize CTA" 'emphasize.*CTA|CTA.*emphas'
check "D11 accent colour" 'accent colo(u)?r'
check "D12 icons consistent" 'consistent icon' 'icon.*consisten'
check "D13 embellishments" '\bembellish'
check "D14 inner radius" 'inner radius'
check "D15 contrast 4.5" '4\.5:1'
check "D16 wrap headlines" 'text-wrap: balance' 'wrap.*headline|headline.*wrap'
check "D17 align by eye" 'align by eye' 'optical align' 'optical centre|optical center'
check "D18 tabular nums" 'tabular-nums' 'tabular num'
check "D19 loading states" 'loading state'
check "D20 useful feedback" 'useful feedback' 'animate.*feedback|feedback.*animat'
echo DONE
