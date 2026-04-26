---
name: skill-lifecycle
description: Full lifecycle management for OpenClaw skills — create, validate, audit, promote, eval, and track skills across draft → proposed → reviewed → staged → released → deprecated stages. Use when managing skill creation, validation, versioning, or lifecycle workflows. Use when asked to build a skill management system, scaffold a new skill, audit existing skills, or implement skill CI/evals.
---

# Skill Lifecycle Management

This skill provides a complete workflow for creating, validating, versioning, reviewing, and maintaining skills.

## Quick Reference

The system lives at `~/.openclaw/workspace/skill-lifecycle/`.

**CLI tool**: `skillctl <command> [options]`

```
Commands:
  init <name>        — Scaffold a new skill from template
  validate <path>    — Validate a skill's structure and frontmatter
  audit [path]       — Full inventory + health check of all skills
  promote <path>     — Advance skill lifecycle stage (draft→proposed→etc.)
  eval <path>        — Run/evaluate test prompts for a skill
  changelog <path>   — View changelog entries for a skill
  registry           — Show the skills registry with stages/versions
  status [path]      — Show lifecycle status for a skill
  install <path>     — Install a skill into OpenClaw's agents/skills/
  template           — List available templates for scaffolding
```

## Lifecycle Stages

```
draft → proposed → reviewed → staged → released → deprecated
```

- **draft**: Initial creation, author iterating
- **proposed**: Ready for review (automatically validates before promoting)
- **reviewed**: Domain expert + steward approved
- **staged**: Deployed to test environment
- **released**: Live, version bumped
- **deprecated**: Still readable, marked as replaced

## Skill Anatomy

Every skill directory has:
- `SKILL.md` — Required: frontmatter (name + description) + instructions
- `scripts/` — Optional: executable code
- `references/` — Optional: detailed docs loaded on demand
- `assets/` — Optional: output templates/resources

## Workflows

### Creating a new skill

```bash
skillctl init my-awesome-skill --template full
# Edit SKILL.md and scripts
skillctl validate ~/.openclaw/workspace/.agents/skills/my-awesome-skill
skillctl promote ~/.openclaw/workspace/.agents/skills/my-awesome-skill proposed
```

### Auditing all skills

```bash
skillctl audit
skillctl registry
```

### Adding evaluations (test prompts)

Create `evals.json` in the skill directory:

```json
{
  "triggers": ["User asks about X", "Request for Y"],
  "non_triggers": ["Related but different topic"],
  "tests": [
    {"prompt": "Can you help me with X?", "expected": "Should activate this skill"}
  ]
}
```

### Promoting through lifecycle

```bash
skillctl promote ./skills/my-skill reviewed
skillctl promote ./skills/my-skill released   # bumps version automatically
```

## Skill Specification

Full spec: see `~/.openclaw/workspace/skill-lifecycle/SPEC.md`

For detailed instructions on creating skills from scratch, see the `skill-creator` skill which covers the full authoring process including progressive disclosure, naming conventions, and resource planning.
