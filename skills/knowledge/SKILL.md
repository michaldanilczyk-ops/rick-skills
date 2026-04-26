---
name: knowledge
description: Knowledge management with wiki‑llm pattern and instinct‑based learning. Use when you need to capture, organize, synthesize, and continuously improve knowledge across sessions. Combines the llm‑wiki pattern (structured knowledge base) with instinct‑based learning (procedural knowledge compounding). Suitable for integration with Paperclip AI company OS or standalone use.
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

# Knowledge Management Skill

## Overview

This skill implements a complete knowledge management system combining:

1. **Wiki‑LLM Pattern** – Structured knowledge base with entities, topics, sources, and cross‑references
2. **Instinct‑Based Learning** – Continuous improvement through pattern extraction and application
3. **Paperclip Integration** – Optional integration with Paperclip AI company OS for team knowledge sharing

The system enables compounding knowledge: each new piece of information enriches the entire knowledge base, and each successful interaction creates reusable patterns for future efficiency.

## Installing on Paperclip

This skill can be installed on your Paperclip AI company OS instance to enable knowledge management across all Paperclip agents.

### Method 1: OpenClaw Integration (Recommended)

If you're using OpenClaw with Paperclip integration:

1. Ensure the skill is in your OpenClaw skills directory:
   ```bash
   cp -r knowledge /opt/homebrew/lib/node_modules/openclaw/skills/
   # or
   ln -s /path/to/knowledge /opt/homebrew/lib/node_modules/openclaw/skills/
   ```

2. Paperclip agents can now use the knowledge skill through OpenClaw.

### Method 2: Paperclip Plugin System

Paperclip has a plugin API (`/api/plugins`). To install as a Paperclip plugin:

1. Package the skill as a plugin (see `knowledge_paperclip.py` for API integration)
2. Install via Paperclip admin interface or file system

### Method 3: Standalone with Paperclip API

The skill works standalone with Paperclip API integration:

1. Set environment variables:
   ```bash
   export PAPERCLIP_URL="http://localhost:3101"
   export PAPERCLIP_COMPANY_ID="85c5e8e2-0767-4f04-851c-0e2d6d105397"
   export KNOWLEDGE_REPOSITORY="/path/to/knowledge-base"
   ```

2. Use the `knowledge_paperclip.py` script for Paperclip integration.

Once installed, Paperclip agents (CEO, Directors, etc.) can create knowledge tasks, query the knowledge base, and apply instincts through the skill.

## Core Concepts

### 1. Wiki‑LLM Pattern (Content Knowledge)

Inspired by Andrej Karpathy's llm‑wiki pattern, this approach treats the knowledge base as a **persistent, compounding artifact**:

- **Raw sources** – Immutable documents, articles, conversations
- **Structured wiki** – LLM‑generated markdown files (entities, topics, summaries)
- **Cross‑references** – Automated linking between related concepts
- **Contradiction tracking** – Flagged and resolved inconsistencies

### 2. Instinct‑Based Learning (Procedural Knowledge)

Adapted from Everything Claude Code's continuous learning system:

- **Pattern extraction** – Capture successful knowledge management patterns
- **Instinct formalization** – Convert patterns into reusable "instincts"
- **Confidence scoring** – Rate instinct reliability (0‑100)
- **Automatic application** – Apply relevant instincts to new situations
- **Continuous evolution** – Update instincts based on outcomes

### 3. Paperclip Integration (Team Knowledge)

Optional integration with Paperclip AI company OS:

- **Shared knowledge base** – Team‑wide access to compiled knowledge
- **Agent‑specific insights** – Domain knowledge for different roles (CEO, Operations, Technology, etc.)
- **Task‑contextual knowledge** – Relevant knowledge surfaced during task execution
- **Knowledge assignment** – Assign knowledge curation tasks to appropriate agents

## Quick Start

### Standalone Usage (OpenClaw)

```bash
# Initialize knowledge repository
knowledge init --path ~/my-knowledge-base

# Add a source
knowledge add-source --url https://example.com/article --tags ai,research

# Query knowledge base
knowledge query "What is the llm-wiki pattern?"

# Capture a pattern as instinct
knowledge capture-instinct --title "Academic paper processing" --action "Extract abstract, authors, citations"
```

### Paperclip Integration

```bash
# Register knowledge base with Paperclip
knowledge paperclip-register --company-id <ID> --api-key <KEY>

# Create knowledge task for Paperclip agent
knowledge paperclip-task --agent "Director of Research" --task "Curate AI safety literature"
```

## Knowledge Repository Structure

```
knowledge-base/
├── sources/          # Raw/original documents (immutable)
├── entities/         # People, companies, concepts
├── topics/           # Broad subjects/themes
├── instincts/        # Procedural patterns (instinct files)
├── queries/          # Saved questions and answers
├── meta/             # Metadata, indexes, statistics
└── integrations/     # Paperclip and other integrations
```

## Workflows

### 1. Source Ingestion

**When:** New document, article, conversation, or insight arrives.

**Steps:**
1. **Capture source** – Save to `sources/` with metadata
2. **Extract entities** – Identify people, companies, concepts
3. **Create/update pages** – Generate entity/topic pages in wiki
4. **Cross‑reference** – Link to related existing knowledge
5. **Update index** – Rebuild navigation and statistics

**Example:**
```bash
knowledge ingest --file research_paper.pdf --tags ai-safety,academic
```

### 2. Knowledge Query

**When:** Need information on a topic.

**Steps:**
1. **Parse query** – Identify entities, topics, intent
2. **Search wiki** – Find relevant entity/topic pages
3. **Synthesize answer** – Combine information from multiple pages
4. **Provide citations** – Reference source pages
5. **Optionally save** – Store useful Q&A in `queries/`

**Example:**
```bash
knowledge query "How does instinct-based learning differ from RAG?"
```

### 3. Pattern Capture (Instinct Creation)

**When:** Successful knowledge management pattern identified.

**Steps:**
1. **Identify pattern** – What worked well? (e.g., "Academic paper → extract abstract first")
2. **Formalize instinct** – Create instinct file with Action, Evidence, Examples
3. **Set confidence** – Initial confidence based on evidence (start 50‑80)
4. **Store instinct** – Save to `instincts/` repository
5. **Apply automatically** – Future similar situations trigger instinct

**Example:**
```bash
knowledge capture-instinct \
  --title "Academic paper processing" \
  --action "Extract abstract, authors, citations before full text" \
  --evidence "Processed 5 papers successfully with this pattern" \
  --tags academic,processing,extraction
```

### 4. Paperclip Knowledge Task

**When:** Need Paperclip agent to curate or analyze knowledge.

**Steps:**
1. **Identify agent** – Which Paperclip role is best suited?
2. **Create task** – Use Paperclip API to create knowledge curation issue
3. **Provide context** – Include relevant existing knowledge
4. **Monitor completion** – Track task progress
5. **Integrate results** – Add agent's work to knowledge base

**Example:**
```bash
knowledge paperclip-task \
  --agent "Director of Research" \
  --task "Summarize recent AI safety papers" \
  --priority high \
  --deadline 2026-04-15
```

## Instinct File Format

Instincts are markdown files with YAML frontmatter:

```yaml
---
title: "Academic paper processing"
author: "knowledge-system"
confidence: 75
tags: [academic, processing, extraction]
created: "2026-04-08"
updated: "2026-04-08"
---

# Action

When processing academic papers, extract abstract, authors, and citations first before reading full text.

# Evidence

- Successfully processed 5 AI safety papers
- Reduced processing time by 40%
- Improved citation accuracy

# Examples

## Metadata extraction
```python
def extract_paper_metadata(pdf_path):
    # Extract title, authors, abstract, citations
    ...
```

## Command line
```bash
pdfgrep -n "Abstract" paper.pdf
```
```

## Paperclip Integration

The skill includes full Paperclip AI company OS integration through the `knowledge_paperclip.py` script.

### Available Paperclip Actions

```bash
# Register knowledge base with Paperclip
knowledge_paperclip.py --path ~/knowledge --action register --name "Company Wiki"

# Create knowledge curation task for Paperclip agent
knowledge_paperclip.py --path ~/knowledge --action task \
  --agent "Director of Research" \
  --title "Curate AI safety literature" \
  --priority high

# Check Paperclip integration status
knowledge_paperclip.py --path ~/knowledge --action status

# Sync knowledge updates (future enhancement)
knowledge_paperclip.py --path ~/knowledge --action sync
```

### Paperclip API Endpoints Used

The integration uses actual Paperclip API endpoints:

1. **`POST /api/companies/{companyId}/issues`** – Create knowledge curation tasks
2. **`GET /api/plugins`** – Check plugin system (for future enhancements)
3. **Health check** – Verify Paperclip is running

### Agent Assignment

Tasks can be assigned to any Paperclip agent:
- **CEO** – Strategic knowledge, decision patterns
- **Director of Operations** – Process documentation, SOPs  
- **Director of Technology** – Technical architecture, stack decisions
- **Director of Research** – Research literature, insights
- **Salesforce Technical Lead** – Salesforce patterns, best practices
- **And more** – All agents from the paperclip-assign skill

### Example: Creating a Knowledge Task

```bash
# Direct API call (what the script does internally)
curl -X POST http://localhost:3101/api/companies/85c5e8e2-0767-4f04-851c-0e2d6d105397/issues \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Document Q3 sales process",
    "description": "Create comprehensive documentation of our Q3 sales process",
    "assigneeAgentId": "5b3c71fc-3c46-4587-a940-e56797b5838d",
    "priority": "high",
    "type": "knowledge-curation"
  }'
```

### Integration Benefits

1. **Team knowledge sharing** – All Paperclip agents access the same knowledge base
2. **Domain specialization** – Agents contribute domain-specific knowledge
3. **Task contextualization** – Knowledge surfaced during task execution
4. **Continuous improvement** – Agents update knowledge base with their work

## Configuration

### Environment Variables
```bash
# Knowledge repository location
export KNOWLEDGE_REPOSITORY="/path/to/knowledge-base"

# Paperclip integration (localhost:3101 in local_trusted mode)
export PAPERCLIP_URL="http://localhost:3101"
export PAPERCLIP_COMPANY_ID="85c5e8e2-0767-4f04-851c-0e2d6d105397"
# export PAPERCLIP_API_KEY=""  # Optional, not needed for local_trusted mode

# Instinct confidence threshold
export INSTINCT_MIN_CONFIDENCE=70
```

### Configuration File
`~/.knowledge/config.yaml`:
```yaml
repository: "/path/to/knowledge-base"
paperclip:
  url: "http://localhost:3101"
  company_id: "85c5e8e2-0767-4f04-851c-0e2d6d105397"
  # api_key: ""  # Optional, not needed for local_trusted mode
instincts:
  min_confidence: 70
  auto_apply: true
wiki:
  auto_cross_reference: true
  contradiction_checking: true
```

## Example Use Cases

### 1. Research Project Knowledge Base
```bash
# Initialize
knowledge init --path ~/research/ai-safety

# Add sources
knowledge add-source --url https://arxiv.org/abs/2306.xxxx --tags ai-safety,alignment
knowledge add-source --file conference_notes.md --tags workshop,discussion

# Query
knowledge query "What are the main approaches to AI alignment?"

# Capture pattern
knowledge capture-instinct --title "arXiv paper processing" --action "Extract abstract, authors, TL;DR first"
```

### 2. Company Internal Wiki
```bash
# Register with Paperclip
knowledge paperclip-register --name "Peak&Peak Internal Wiki"

# Assign curation tasks
knowledge paperclip-task --agent "Director of Operations" --task "Document Q2 processes"
knowledge paperclip-task --agent "Director of Technology" --task "Update tech stack documentation"

# Query company knowledge
knowledge query "What is our current tech stack for Salesforce?"
```

### 3. Personal Learning Journal
```bash
# Daily learning capture
knowledge add-source --text "Learned about vector databases today. Pinecone vs Weaviate." --tags learning,vectors

# Weekly review
knowledge query "What did I learn this week about AI?"

# Pattern extraction
knowledge capture-instinct --title "Learning consolidation" --action "Review and summarize weekly learnings every Friday"
```

## Integration with Existing Systems

### OpenClaw Skills
- **`instincts` skill** – Shared instinct repository
- **`wiki` skill** – Compatible wiki structure
- **`paperclip-assign` skill** – Task assignment integration

### Paperclip Agents
- **CEO** – Strategic knowledge, decision patterns
- **Director of Operations** – Process documentation, SOPs
- **Director of Technology** – Technical architecture, stack decisions
- **Director of Research** – Research literature, insights
- **Salesforce Technical Lead** – Salesforce patterns, best practices

### External Tools
- **Obsidian** – Browse knowledge base with graph view
- **Notion** – Export summaries to Notion pages
- **Git** – Version control for knowledge repository
- **API endpoints** – REST API for programmatic access

## Maintenance

### Regular Tasks
```bash
# Validate knowledge base integrity
knowledge validate --recursive

# Update confidence scores
knowledge update-confidence --success instinct1.md
knowledge update-confidence --failure instinct2.md

# Archive low-confidence instincts
knowledge archive --min-confidence 30

# Rebuild indexes
knowledge rebuild-index
```

### Monitoring
```bash
# Show statistics
knowledge stats

# Recent changes
knowledge log --last 7days

# Orphan detection
knowledge orphans --fix
```

## Troubleshooting

**Problem:** Knowledge base corruption
**Solution:** `knowledge validate --fix --backup`

**Problem:** Paperclip connection failed
**Solution:** Check `PAPERCLIP_URL` and Paperclip service status

**Problem:** Instincts not applying
**Solution:** Check `INSTINCT_MIN_CONFIDENCE`, validate instinct files

**Problem:** Cross‑references broken
**Solution:** `knowledge rebuild-links --verbose`

## Future Enhancements

1. **Multi‑user collaboration** – Concurrent editing, change tracking
2. **Advanced search** – Semantic search, vector embeddings
3. **Automated ingestion** – Watch folders, email parsing, web scraping
4. **Knowledge graphs** – Visual relationship mapping
5. **Export formats** – PDF, HTML, Notion, Confluence
6. **API‑first design** – REST API for all operations
7. **Plugin system** – Custom processors, exporters, integrations

## Getting Help

- **Documentation:** `knowledge --help`
- **Examples:** `knowledge examples`
- **Debug mode:** `knowledge --debug <command>`
- **Issue tracking:** Paperclip issues with label "knowledge"

---
*Knowledge Skill v1.0 – Combines wiki‑llm pattern and instinct‑based learning*
