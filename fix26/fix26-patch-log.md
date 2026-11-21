# fix26 run log

## Errors (0)
- none

## Changes (16)
- /home/hatch/workspace/hackathon-plugin/fix35/fakehome35/workspace/hackathon-plugin/hackathon-ecc/skills/ck/hooks/session-start.mjs — ' * Injects ~100 tokens (not ~2,500 like v1).\n * SKILL.md is injected separately ' -> ' * Injects ~1k tokens per session (not ~2,500 like v1): the full SKILL.md\n * (~1'
- /home/hatch/workspace/hackathon-plugin/fix35/fakehome35/workspace/hackathon-plugin/hackathon-ecc/skills/ck/hooks/session-start.mjs — '  // Load skill (always inject — now only ~50 lines)' -> '  // Load skill (always inject the full SKILL.md, ~170 lines, ~1k tokens/session'
- /home/hatch/workspace/hackathon-plugin/fix35/fakehome35/workspace/hackathon-plugin/hackathon-ecc/skills/ck/SKILL.md — 'The hook injects ~100 tokens per session (compact 5-line summary). It also detec' -> 'The hook injects ~1k tokens per session (the full SKILL.md plus the compact 5-li'
- /home/hatch/workspace/hackathon-plugin/fix35/fakehome35/workspace/hackathon-plugin/hackathon-ecc/skills/django-verification/SKILL.md — 'pip install ruff black mypy pytest pytest-django pytest-cov bandit safety pip-au' -> 'pip install ruff==0.17.5 black==26.10.1 mypy==2.4.1 pytest==9.2.0 pytest-django='
- /home/hatch/workspace/hackathon-plugin/fix35/fakehome35/workspace/hackathon-plugin/hackathon-ecc/skills/frontend-slides/html-template.md — '**Dependency:** `pip install Pillow`' -> '**Dependency:** `pip install Pillow==13.0.0`'
- /home/hatch/workspace/hackathon-plugin/fix35/fakehome35/workspace/hackathon-plugin/hackathon-ecc/skills/frontend-slides/scripts/extract-pptx.py — 'Requires: pip install python-pptx' -> 'Requires: pip install python-pptx==1.0.2'
- /home/hatch/workspace/hackathon-plugin/fix35/fakehome35/workspace/hackathon-plugin/hackathon-ecc/skills/django-celery/SKILL.md — "pip install 'celery[redis]' django-celery-results django-celery-beat" -> "pip install 'celery[redis]==5.7.0' django-celery-results==2.6.0 django-celery-be"
- /home/hatch/workspace/hackathon-plugin/fix35/fakehome35/workspace/hackathon-plugin/hackathon-ecc/skills/django-celery/SKILL.md — 'pip install flower' -> 'pip install flower==2.2.0'
- /home/hatch/workspace/hackathon-plugin/fix35/fakehome35/workspace/hackathon-plugin/hackathon-ecc/skills/generating-python-installer/SKILL.md — 'pip install opencv-python-headless' -> 'pip install opencv-python-headless==5.0.0.93'
- /home/hatch/workspace/hackathon-plugin/fix35/fakehome35/workspace/hackathon-plugin/hackathon-ecc/skills/plankton-code-quality/SKILL.md — 'py -m pip install uv ruff' -> 'py -m pip install uv==0.13.8 ruff==0.17.5'
- /home/hatch/workspace/hackathon-plugin/fix35/fakehome35/workspace/hackathon-plugin/hackathon-ecc/skills/windows-desktop-e2e/SKILL.md — 'pip install pywinauto pytest pytest-html Pillow pytest-timeout' -> 'pip install pywinauto==0.6.9 pytest==9.2.0 pytest-html==4.2.0 Pillow==13.0.0 pyt'
- /home/hatch/workspace/hackathon-plugin/fix35/fakehome35/workspace/hackathon-plugin/hackathon-ecc/skills/windows-desktop-e2e/SKILL.md — '      run: pip install pywinauto pytest pytest-html Pillow' -> '      run: pip install pywinauto==0.6.9 pytest==9.2.0 pytest-html==4.2.0 Pillow='
- /home/hatch/workspace/hackathon-plugin/fix35/fakehome35/workspace/hackathon-plugin/hackathon-ecc/skills/windows-desktop-e2e/SKILL.md — 'pip install pyautogui Pillow opencv-python' -> 'pip install pyautogui==0.9.54 Pillow==13.0.0 opencv-python==5.0.0.93'
- /home/hatch/workspace/hackathon-plugin/fix35/fakehome35/workspace/hackathon-plugin/hackathon-ecc/skills/windows-desktop-e2e/SKILL.md — 'pip install pytest-repeat' -> 'pip install pytest-repeat==0.9.4'
- /home/hatch/workspace/hackathon-plugin/fix35/fakehome35/workspace/hackathon-plugin/hackathon-ecc/scripts/hooks/gateguard-fact-force.js — ' * Full package with config support: pip install gateguard-ai' -> ' * Full package with config support: pip install gateguard-ai==0.6.2'
- /home/hatch/workspace/hackathon-plugin/fix35/fakehome35/workspace/hackathon-plugin/hackathon-ecc/scripts/hooks/insaits-security-monitor.py — '  pip install insa-its' -> '  pip install insa-its==4.9.10'
