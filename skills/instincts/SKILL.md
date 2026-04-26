---
name: instincts
description: Manage instinct‑based learning for OpenClaw agents—capture successful patterns, formalize them into reusable instincts, and apply them to future tasks. Use when: (1) you want the agent to learn from successful patterns across sessions, (2) you need to create, import, export, or manage instinct files, (3) you want to apply previously learned instincts to new tasks, (4) you're implementing continuous learning similar to Everything Claude Code's instinct system.
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "os": ["darwin", "linux"],
        "requires": { "bins": [] },
        "install": [],
      },
  }
---

# Instincts

## Overview

Instinct‑based learning enables OpenClaw agents to capture successful patterns from their own work, formalize them into reusable "instincts" (structured documents with examples and evidence), and apply these instincts to future similar tasks. This creates **compounding procedural knowledge**—where each successful session makes future sessions more efficient and reliable.

Inspired by **Everything Claude Code's instinct system**, this skill provides the tools and workflows to implement continuous learning within OpenClaw, turning sporadic successes into repeatable expertise.

## Core Concepts

### What Is an Instinct?

An **instinct** is a captured pattern of successful agent behavior, structured as a markdown file with:

- **YAML frontmatter:** Metadata (title, author, confidence, tags, created/updated dates)
- **Action:** The core pattern or rule to apply
- **Evidence:** Examples where this pattern succeeded
- **Examples:** Concrete code/command examples
- **Confidence score:** 0‑100 based on success rate

### How Instincts Work

1. **Observation:** Agent completes a task successfully
2. **Extraction:** Identify the pattern that led to success
3. **Formalization:** Structure the pattern into an instinct file
4. **Storage:** Save to the instincts repository
5. **Retrieval:** When similar context appears, relevant instincts are recalled
6. **Application:** Agent applies the instinct (or overrides if low confidence)
7. **Evolution:** Instincts are updated based on new evidence

### Repository Structure

By default, instincts are stored in:

```
/Users/peakpeak/.openclaw/workspace/instincts/
├── instincts/           # Individual instinct files (.md)
├── templates/          # Template files
└── metadata.json       # Repository metadata
```

## Quick Start

### 1. Create Your First Instinct

```bash
# Use the instinct template
cp /Users/peakpeak/.openclaw/workspace/skills/instincts/references/instinct_template.md /Users/peakpeak/.openclaw/workspace/instincts/my_pattern.md

# Edit with your pattern
```

### 2. Import an Existing Instinct

```bash
# From a file
openclaw instinct import /path/to/instinct.md

# From a directory
openclaw instinct import /path/to/instincts/
```

### 3. List Available Instincts

```bash
openclaw instinct list
openclaw instinct search "markdown"
```

### 4. Apply Instincts to a Task

When working on a task, ask the agent: "Check for relevant instincts" or "Apply instincts for [domain]."

The agent will search the instincts repository for patterns matching the current context and suggest applications.

## Workflows

### Capturing New Instincts

**When to capture:** After successfully completing a non‑trivial task where you notice a reusable pattern.

**Steps:**
1. Identify the successful pattern (e.g., "When parsing markdown, always extract YAML frontmatter first")
2. Create a new instinct file using the template
3. Fill in:
   - **Title:** Clear, descriptive name
   - **Action:** The pattern to apply
   - **Evidence:** 2‑3 examples where this worked
   - **Examples:** Concrete code/command snippets
   - **Confidence:** Initial confidence (start at 50‑70)
4. Save to the instincts repository
5. Optional: Run validation with `scripts/validate_instinct.py`

### Applying Instincts

**When working on a task:**
1. Agent analyzes task context
2. Searches instincts repository for matching tags/keywords
3. Reads relevant instinct files
4. Decides whether to apply (based on confidence & fit)
5. If applied, follows the instinct's Action and Examples
6. After completion, updates instinct confidence (↑ if successful, ↓ if not)

### Managing the Repository

- **Validation:** Check instinct file structure and completeness
- **Pruning:** Remove low‑confidence or outdated instincts
- **Merging:** Combine similar instincts
- **Versioning:** Track changes to instincts over time

## Instinct File Format

See [instinct_template.md](references/instinct_template.md) for the complete template with examples.

**Key sections:**

```yaml
---
title: "Markdown YAML frontmatter extraction"
author: "agent-session-2026-04-07"
confidence: 85
tags: [markdown, parsing, frontmatter]
created: 2026-04-07
updated: 2026-04-08
---

Action: When processing markdown documents, always extract YAML frontmatter first before parsing content.

Evidence:
- Successfully extracted metadata from 12 documentation files
- Prevented parsing errors in 3 cases where frontmatter contained special characters

Examples:
- Input: "---\ntitle: Example\n---\n# Content"
- Output: {title: "Example", content: "# Content"}
```

## Integration with llm‑wiki

Instinct‑based learning complements the **llm‑wiki pattern**:

- **llm‑wiki** compounds **content knowledge** (facts, entities, relationships)
- **Instincts** compound **procedural knowledge** (how‑to, patterns, strategies)

**Combined workflow:**
1. Process a source document for the wiki
2. Capture successful extraction patterns as instincts
3. Future document processing uses those instincts
4. Compiled wiki content improves with each source
5. Instincts improve with each processing session

## Scripts

This skill includes Python scripts for managing instincts:

- **`scripts/validate_instinct.py`** – Validate instinct file structure
- **`scripts/search_instincts.py`** – Search repository by keyword/tag
- **`scripts/import_instincts.py`** – Import instincts from external sources
- **`scripts/confidence_update.py`** – Update confidence scores based on outcomes

See [scripts/README.md](scripts/README.md) for details.

## References

- **[instinct_template.md](references/instinct_template.md)** – Complete template with examples
- **[ecc_instinct_system.md](references/ecc_instinct_system.md)** – How Everything Claude Code implements instincts
- **[integration_patterns.md](references/integration_patterns.md)** – Integrating instincts with other OpenClaw skills

## Commands (Conceptual)

While OpenClaw doesn't have a built‑in `instinct` command yet, these are the envisioned commands:

```bash
openclaw instinct list [--tag TAG] [--confidence MIN]
openclaw instinct import <path>
openclaw instinct export <id|tag> <directory>
openclaw instinct validate <path>
openclaw instinct search "query"
openclaw instinct confidence <id> <new_score>
openclaw instinct apply <task_description>
```

For now, use the provided Python scripts or implement these as custom shell aliases.

## Examples

### Example 1: Wiki Entity Extraction

**Instinct:** `wiki_entity_extraction.md`

```yaml
---
title: "Wiki entity extraction from markdown headers"
confidence: 90
tags: [wiki, markdown, entity-extraction]
---

Action: When processing markdown for the wiki, extract H1 headers as entity names, H2 headers as entity attributes.

Evidence:
- Successfully created 15 entity pages from documentation
- Consistent naming improved cross‑referencing

Examples:
- Input: "# OpenAI\n## Founded: 2015\n## CEO: Sam Altman"
- Output: Entity "OpenAI" with attributes {Founded: "2015", CEO: "Sam Altman"}
```

### Example 2: Real Estate Listing Parsing

**Instinct:** `real_estate_parsing.md`

```yaml
---
title: "Extract apartment details from Swiss real estate listings"
confidence: 75
tags: [real-estate, parsing, web-scraping]
---

Action: When scanning real estate listings, look for price in CHF, rooms (Zimmer), square meters (m²), and location.

Evidence:
- Successfully parsed 8 listings from comparis.ch
- Extracted correct prices and room counts

Examples:
- Input: "3.5 Zimmer • 85 m² • CHF 2'300 pro Monat • Zürich"
- Output: {rooms: 3.5, area: 85, price: 2300, currency: CHF, location: Zürich}
```

## Next Steps

1. **Create the instincts directory:** `mkdir -p /Users/peakpeak/.openclaw/workspace/instincts`
2. **Copy templates:** From `references/` to the instincts directory
3. **Start capturing:** After successful tasks, create instinct files
4. **Integrate with workflows:** Add instinct checks to recurring tasks
5. **Share instincts:** Export useful instincts for team use

---

**Inspired by:** Everything Claude Code's instinct‑based learning system
**Related skills:** `wiki`, `coding-agent`, `skill-creator`
