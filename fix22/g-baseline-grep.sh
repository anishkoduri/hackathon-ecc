#!/bin/bash
# Word-boundary baseline greps for Group G (fix #22). Hyphen-joined compounds do NOT count.
# Scopes: B=build.sh, T=built tree hackathon-ecc/, S=staged sources (new-skills + round2-skills)
declare -A P=(
 [G1_kerning]='(?<![\w-])kerning(?![\w-])'
 [G2_optical_centre]='(?<![\w-])optical\s+cent(re|er)(?![\w-])'
 [G3_tabular_numbers]='(?<![\w-])tabular\s+(numbers|nums|numerals)(?![\w-])'
 [G4_layout_shift]='(?<![\w-])layout\s+shifts?(?![\w-])'
 [G5_tracking]='(?<![\w-])tracking(?![\w-])'
 [G6_optimistic_update]='(?<![\w-])optimistic\s+updates?(?![\w-])'
 [G7_x_height]='(?<![\w-])x-height(?![\w-])'
 [G8_touch_target]='(?<![\w-])touch\s+targets?(?![\w-])'
 [G9_leading]='(?<![\w-])leading(?![\w-])'
 [G10_origin_aware]='(?<![\w-])origin-aware\s+animation(?![\w-])'
 [G11_oklch]='(?<![\w-])oklch(?![\w-])'
 [G12_widow]='(?<![\w-])widows?(?![\w-])'
 [G13_safe_area]='(?<![\w-])safe\s+areas?(?![\w-])'
 [G14_stagger]='(?<![\w-])stagger\w*(?![\w-])'
 [G15_line_length]='(?<![\w-])line\s+length(?![\w-])'
 [G16_affordance]='(?<![\w-])affordances?(?![\w-])'
 [G17_combobox]='(?<![\w-])combobox(?![\w-])'
 [G18_interruptible]='(?<![\w-])interruptible(?![\w-])'
 [G19_progressive_disclosure]='(?<![\w-])progressive\s+disclosure(?![\w-])'
 [G20_shared_element]='(?<![\w-])shared\s+element\s+transition(?![\w-])'
)
for k in "${!P[@]}"; do echo "=== $k : /${P[$k]}/"; echo "-- build.sh:"; grep -P -i -n "${P[$k]}" build.sh | head -n 20; echo "-- built tree:"; grep -P -i -r -n "${P[$k]}" hackathon-ecc/ 2>/dev/null | head -n 20; echo "-- staged:"; grep -P -i -r -n "${P[$k]}" new-skills/ round2-skills/ 2>/dev/null | head -n 20; done
