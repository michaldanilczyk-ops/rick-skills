# Skill Specification v1

## Overview

A **skill** is a self-contained directory that provides instructions + resources for an AI agent. Skills transform a general-purpose agent into a domain specialist.

## Directory Structure

```
skill-name/
├── SKILL.md              # Required: metadata + instructions
├── scripts/              # Optional: executable code
│   └── do-thing.sh
├── references/           # Optional: detailed docs (loaded on demand)
│   └── deep-reference.md
└── assets/               # Optional: files used in output (templates, etc.)
    └── template.txt
```

## Required: SKILL.md

### Frontmatter (YAML, --- delimited)

Only two fields allowed:

```yaml
---
name: skill-name              # lowercase-hyphenated, matches directory name
description: When to use this skill, what triggers it, what it provides
---
```

- `name`: Must match the directory name. Lowercase letters, digits, hyphens only.
- `description`: Primary trigger mechanism. Include ALL "when to use" info here — the body loads only after triggering. 20-200 chars recommended.

### Body

Clear, concise instructions. Assume the agent is already smart. Only add context the agent doesn't already have.

## Optional: scripts/

Deterministic, executable code for tasks that need exact correctness.

- Scripts must be executable (`chmod +x`)
- Document usage and dependencies in SKILL.md
- Test scripts before committing

## Optional: references/

Detailed reference material loaded only when needed.

- Reference from SKILL.md explicitly ("See references/advanced.md for X")
- Keep SKILL.md lean; move schemas, API refs, complex examples here
- Files under 500 lines preferred; include TOC for longer files

## Optional: assets/

Files used in output (templates, logos, boilerplate).

- Not loaded into agent context — used as output base files
- Reference in SKILL.md when and how to use them

## What NOT to Include

No auxiliary docs: README.md, CHANGELOG.md, INSTALLATION_GUIDE.md, QUICK_REFERENCE.md.

## Lifecycle Stages

```
draft → proposed → reviewed → staged → released → deprecated
```

| Stage | Meaning |
|-------|---------|
| draft | Initial creation, author iterating |
| proposed | PR opened, awaiting review |
| reviewed | Domain expert + steward approved |
| staged | Deployed to test environment |
| released | Live in production, versioned |
| deprecated | Still readable, marked as replaced |

## Naming Convention

- Lowercase letters, digits, and hyphens only
- No leading or trailing hyphens
- Prefer short, verb-led phrases
- Namespace by tool when helpful: `gh-address-comments`, `linear-address-issue`

## Quality Checks

Every PR to a skill should check:

1. Frontmatter YAML is valid
2. `name` and `description` present
3. Description triggers when it should and doesn't when it shouldn't
4. No unnecessary files
5. No symlinks
6. Scripts are executable
7. References are actually referenced from SKILL.md
8. Skill under 50KB total (soft limit)
