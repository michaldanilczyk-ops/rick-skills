# Skill Authoring Guide

*A comprehensive guide for technical and non-technical users on creating skills for AI agents and LLMs.*

---

## Table of Contents

1. [What Is a Skill?](#1-what-is-a-skill)
2. [Skill Directory Structure](#2-skill-directory-structure)
3. [Anatomy of SKILL.md](#3-anatomy-of-skillmd)
4. [Writing Effective Frontmatter](#4-writing-effective-frontmatter)
5. [Writing the Skill Body](#5-writing-the-skill-body)
6. [Linking References](#6-linking-references)
7. [Building Skills for Structured Output](#7-building-skills-for-structured-output)
8. [Building Skills for Workflows](#8-building-skills-for-workflows)
9. [Progressive Disclosure Pattern](#9-progressive-disclosure-pattern)
10. [Best Practices & Tips](#10-best-practices--tips)
11. [Testing & Evaluating Skills](#11-testing--evaluating-skills)
12. [Glossary](#12-glossary)

---

## 1. What Is a Skill?

A **skill** is a self-contained package that extends what an AI agent can do. Think of it as an "onboarding manual" for a specific task or domain.

### What Skills DO:

| Capability | Example |
|---|---|
| Teach the agent a workflow | "How to review a pull request step by step" |
| Give the agent domain knowledge | "Our company's data schema in BigQuery" |
| Define output formats | "Generate a compliance report in this exact format" |
| Provide executable scripts | "Run this Python script to rotate a PDF" |
| Link external reference docs | "Load this API documentation when needed" |

### Who Creates Skills?

- **Technical users** (developers): Write scripts, define structured outputs, build complex workflows
- **Non-technical users** (domain experts, PMs, analysts): Write the instructions, define processes, capture knowledge

Both roles matter — a developer might write the scripts while a project manager writes the workflow instructions.

---

## 2. Skill Directory Structure

Every skill follows this directory structure:

```
skill-name/
├── SKILL.md              ← REQUIRED: The main instructions
├── scripts/              ← Optional: Executable code (Python, Bash, etc.)
│   └── rotate-pdf.py
├── references/           ← Optional: Reference docs loaded on demand
│   ├── schema.md
│   └── api-docs.md
└── assets/               ← Optional: Templates, images, output resources
    ├── logo.png
    └── report-template.html
```

### What goes where?

| Directory | What to put there | Example |
|---|---|---|
| `SKILL.md` | Instructions the agent reads when the skill activates | Workflow steps, formatting rules, commands |
| `scripts/` | Code the agent should run (not read line-by-line) | Python, Bash, Node.js scripts |
| `references/` | Documentation the agent might need to reference | Schemas, policies, API docs, full guides |
| `assets/` | Files used in the agent's output, not read as context | Templates, images, boilerplate code |

### Rules of thumb:

- **Keep SKILL.md under 500 lines.** If it's longer, split content into `references/` files.
- **Don't create extra files** like README.md, CHANGELOG.md, or INSTALL.md. The skill is for the AI agent, not for humans browsing GitHub.
- **Scripts are optional** — many excellent skills have no code at all. They're pure instructions.

---

## 3. Anatomy of SKILL.md

Every `SKILL.md` file has exactly two parts:

```
┌─────────────────────────────────────────────────────┐
│  ---                                                │
│  name: my-skill                                     │
│  description: What this skill does and when to use  │
│  it. This is the only part the agent reads before   │
│  deciding if the skill matches the user's request.  │
│  ---                                                │
│                                                     │
│  # My Skill                                         │
│                                                     │
│  Instructions start here. This content only loads   │
│  AFTER the agent decides the skill is relevant.     │
│                                                     │
│  ## Step 1: First step                              │
│  ...                                                │
│                                                     │
│  ## Step 2: Second step                             │
│  ...                                                │
└─────────────────────────────────────────────────────┘
```

### Part 1: YAML Frontmatter (between `---` lines)

```
---
name: skill-name-here
description: Clear description of what this skill does and when an agent should activate it.
---
```

Only two fields:

- **`name`**: Hyphenated lowercase name (e.g., `pull-request-reviewer`)
- **`description`**: The TRIGGER — describes both what the skill does AND when to use it

### Part 2: Markdown Body (everything after the second `---`)

Standard Markdown with step-by-step instructions. The agent reads this content only after the skill is activated.

---

## 4. Writing Effective Frontmatter

The frontmatter `description` is **the single most important part of your skill**. It's the only text the AI agent reads before deciding whether to use your skill.

### The Golden Rule:

> **Tell the agent WHEN to use this skill, not just WHAT it does.**

### Good description:

```yaml
description: >
  Review pull requests for code quality, security issues, and best practices.
  Activate when the user asks for code review, PR feedback, or says "review
  this PR". Also for pull request summaries and change analysis.
```

### Bad description:

```yaml
description: Reviews code
```

### Pattern for descriptions:

```
[What the skill does]. Activate when [specific triggers]. Also for [edge cases].
```

### Examples by type:

**Workflow skill:**
```yaml
description: >
  Generates weekly status reports from project data. Activate when user asks
  for "weekly report", "status update", "sprint review", or "project summary".
  Use when creating written reports, email summaries, or Slack updates.
```

**Output skill:**
```yaml
description: >
  Creates standardized compliance reports in PDF format. Activate when user
  mentions "compliance report", "audit document", or "regulatory filing".
  Follows SEC and GDPR reporting requirements.
```

**Reference skill:**
```yaml
description: >
  Company data schema and query patterns for BigQuery. Activate when user
  asks about database schema, tables, metrics, or wants to write SQL queries
  for business analytics.
```

---

## 5. Writing the Skill Body

### Keep it concise

The AI agent is already smart. Don't explain basic concepts. Only add information the agent wouldn't already know.

**Don't write:**
```markdown
## What is a PDF?

A PDF (Portable Document Format) is a file format developed by Adobe...
```

**Do write:**
```markdown
## PDF Processing

Extract text using pdfplumber:
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = "\n".join(page.extract_text() for page in pdf.pages)
```
```

### Use the right level of detail

| Task Type | Level of Detail | Example |
|---|---|---|
| Simple, flexible | High freedom | "Analyze this CSV and show key trends" |
| Complex, needs guidance | Medium freedom | Python pseudocode + parameters |
| Fragile, error-prone | Low freedom | Exact scripts, strict steps |

### Structure with headings

Use clear hierarchical headings:

```markdown
# Skill Name

## When to use
...trigger conditions...

## Quick start
...simplest usage...

## Detailed workflow
...step by step...

## Advanced features
...links to references/...
```

### Use examples

Show, don't just tell:

```markdown
## Example

User: "Generate a weekly status report for Project Alpha"

Agent should:
1. Fetch tasks from the project tracker
2. Group by status (done/in progress/blocked)
3. Format as a table with dates
4. Output to the requested channel (email/Slack)
```

---

## 6. Linking References

References let you keep SKILL.md lean while providing deep knowledge when needed.

### How references work

- References go in `references/` directory
- Reference files are NOT loaded automatically
- The agent reads them ONLY when it decides it needs more information
- You must **tell the agent WHEN to load each reference** in SKILL.md

### Directory structure

```
my-skill/
├── SKILL.md
└── references/
    ├── schema.md          ← Database schema (50+ lines)
    ├── deployment.md      ← Deployment steps (100+ lines)
    └── examples.md        ← Example outputs (30+ lines)
```

### How to reference in SKILL.md

**☝️ CRITICAL:** You must tell the agent which references exist and when to load them. The agent won't discover them on its own.

```markdown
# Deployment Workflow

## Quick Steps
1. Build the Docker image
2. Push to registry
3. Update Kubernetes manifest

## Full Deployment Guide
For the complete step-by-step deployment with rollback procedures,
infrastructure details, and troubleshooting:
→ See [references/deployment.md](references/deployment.md)

Load this file when:
- The user asks for detailed deployment instructions
- Something goes wrong during deployment
- You need infrastructure-specific details

## Database Schema
When you need to write SQL queries or understand table relationships:
→ See [references/schema.md](references/schema.md)
```

### Best practices for references

1. **Explain WHEN to load each reference** — Never just link it
2. **Keep references one level deep** — Don't have references that link to other references
3. **Add a table of contents** — For files over 100 lines, put a TOC at the top
4. **Reference files are for DETAILS** — Core workflow stays in SKILL.md
5. **Multiple references for different domains** — If a skill covers finance AND sales AND product, split them:

```
bigquery/
├── SKILL.md
└── references/
    ├── finance.md    ← Revenue, billing metrics
    ├── sales.md      ← Opportunities, pipeline
    ├── product.md    ← API usage, features
    └── marketing.md  ← Campaigns, attribution
```

In SKILL.md:
```markdown
## Available references

- **Finance queries**: [references/finance.md](references/finance.md) — load when user asks about revenue, billing
- **Sales queries**: [references/sales.md](references/sales.md) — load when user asks about pipeline
- **Product queries**: [references/product.md](references/product.md) — load when user asks about usage
- **Marketing queries**: [references/marketing.md](references/marketing.md) — load when user asks about campaigns
```

---

## 7. Building Skills for Structured Output

Skills that generate specific output formats (tables, documents, reports, emails) need precise instructions.

### Pattern 1: Table Output

```markdown
# Project Status Reporter

## Output Format

When generating a status report table, use this exact format:

```
| Task | Owner | Status | ETA | Notes |
|------|-------|--------|-----|-------|
| ...  | ...   | ...    | ... | ...   |
```

### Status values (use exactly these):
- 🟢 On Track
- 🟡 At Risk
- 🔴 Blocked
- ⚪ Not Started

### Rules:
1. Sort by status: Blocked → At Risk → On Track → Not Started
2. Each task gets exactly one row
3. Add emoji prefix to status column
```

### Pattern 2: Structured Document Output

```markdown
# Compliance Report Generator

## Report Structure

Generate reports with these sections IN ORDER:

```
────────────────────────────────────────
     [CLIENT NAME] - Compliance Report
     Prepared: [DATE]
────────────────────────────────────────

1. EXECUTIVE SUMMARY
   - Overall compliance score
   - Key findings (3-5 bullet points)
   - Critical items requiring immediate action

2. DETAILED FINDINGS
   - For each finding:
     * Finding ID: [ID]
     * Severity: [Critical/High/Medium/Low]
     * Description
     * Current status
     * Recommendation
     * Target resolution date

3. COMPLIANCE SCORECARD
   | Category | Score | Target | Gap |
   |----------|-------|--------|-----|

4. ACTION ITEMS
   Numbered list with owners and due dates
────────────────────────────────────────
```

### Pattern 3: Email / Message Output

```markdown
# Client Communication Skill

## Email Template

Use this template for client update emails:

```
Subject: [PROJECT] - Weekly Update [DATE]

Hi [CLIENT],

Here's this week's update for [PROJECT]:

✅ Completed:
- [Item 1]
- [Item 2]

🔄 In Progress:
- [Item 3]

🚧 Blocked:
- [Item 4] — needs your input on [topic]

Next steps:
- [Next milestone]

Best,
[YOUR NAME]
```

## Tone Guidelines
- Professional but warm
- Use emojis sparingly (max 3 per email)
- Lead with completed items before blocked items
- Keep under 200 words
```

### Pattern 4: Template + Variables

For more complex outputs, define variables the agent should fill in:

```markdown
# Incident Report Writer

## Variables

When writing an incident report, identify and fill these fields:

| Variable | Source | Example |
|---|---|---|
| {incident_id} | Ask user or auto-generate | INC-2026-042 |
| {severity} | From incident classification | SEV1 / SEV2 / SEV3 |
| {impact} | Ask user for description | "3 hours of downtime" |
| {timeline} | Build from events | "12:00 — Detected\n12:05 — Paged" |
| {root_cause} | From investigation | "Certificate expired" |
| {action_items} | From resolution steps | "1. Renew cert\n2. Add monitoring" |

## Output Template

Generate the report using this structure:

```
────────────────────────
INCIDENT REPORT: {incident_id}
Date: {date}
Severity: {severity}
────────────────────────

1. SUMMARY
{one paragraph overview}

2. TIMELINE
{timestamped events in chronological order}

3. IMPACT
{affected systems, users, duration}

4. ROOT CAUSE
{technical explanation}

5. RESOLUTION
{what was done to fix}

6. ACTION ITEMS
{preventive measures with owners}

────────────────────────
```
```

---

## 8. Building Skills for Workflows

Workflow skills guide the agent through a multi-step process. They're the most common type of skill and the most valuable for non-technical authors.

### Anatomy of a Workflow Skill

```markdown
# Pull Request Reviewer

## When to Activate
- User asks to review a PR
- User says "check this code"
- User requests code quality feedback

## Workflow

### Step 1: Fetch the PR diff
Run `gh pr view <number> --json files,additions,deletions`

### Step 2: Analyze Changed Files
For each changed file:
1. Check if file is in a language the agent knows
2. Read the diff chunk by chunk
3. Note any patterns (large refactors, new features, bug fixes)

### Step 3: Review Criteria
Check each file for:
- ❌ Security vulnerabilities (SQL injection, XSS, hardcoded secrets)
- ❌ Performance issues (N+1 queries, missing indexes)
- ❌ Code style violations (inconsistent naming, dead code)
- ❌ Missing tests
- ✅ Correctness
- ✅ Readability
- ✅ Documentation (comments, README updates)

### Step 4: Write the Review

Format your review like this:

```
## Overview
[1-2 sentence summary of the change]

## Feedback

### Critical
- [Issue 1] — [file:line] — [explanation]

### Suggestions
- [Issue 2] — [optional improvement]

## Nitpicks
- [Minor style comments]

## ✅ What's good
- [Thing done well]
```

### Step 5: Submit
Use `gh pr review <number> --body - < review.txt`
```

### Workflow Patterns

#### Linear Workflow (do steps 1→2→3→4)

```markdown
## Workflow

Follow these steps IN ORDER:

1. **Discover** — Find relevant information
2. **Analyze** — Process and understand it
3. **Plan** — Decide what to do
4. **Execute** — Do it
5. **Verify** — Check the result
```

#### Conditional Workflow (if this, do that)

```markdown
## Workflow

### Step 1: Classify the request
Determine what type of request this is:

- **Bug report** → Go to Bug Workflow below
- **Feature request** → Go to Feature Workflow
- **Question** → Go to Support Workflow

### Bug Workflow
1. Reproduce the issue
2. Check logs for errors
3. Identify root cause
4. Propose fix

### Feature Workflow
1. Clarify requirements
2. Check feasibility
3. Estimate effort
4. Create implementation plan
```

#### Checklist Workflow (verify items)

```markdown
## Deployment Checklist

Before deploying, verify ALL items:

- [ ] All tests pass
- [ ] No security vulnerabilities in new code
- [ ] Database migrations are backward compatible
- [ ] Feature flags are configured
- [ ] Monitoring alerts are set up
- [ ] Rollback plan documented
- [ ] Change approved by lead
```

#### Decision Tree Workflow

```markdown
## Troubleshooting Decision Tree

User says "the app is slow"

1. Is it slow for everyone?
   - YES → Check server metrics → Go to #2
   - NO  → Check user's network

2. Check server metrics
   - CPU > 80%? → Scale up instances
   - Memory > 90%? → Check for memory leak
   - Disk I/O high? → Optimize queries
   - None of the above → Check external API latency
```

---

## 9. Progressive Disclosure Pattern

This is the most important design pattern for skills. It keeps the agent's context window from being bloated.

### The Three Levels

```
Level 1: Frontmatter (~100 words)  ← ALWAYS loaded in context
  ↓  (only if user's request matches the description)
Level 2: SKILL.md body (<500 lines)  ← Loaded when skill triggers
  ↓  (only if the agent needs more detail)
Level 3: references/ files (unlimited) ← Loaded on demand
```

### How to use this in practice

**Level 1 — Frontmatter (the hook):**

```yaml
description: >
  Manages cloud infrastructure on AWS. Activate when user asks about
  EC2, S3, Lambda, RDS, or any AWS service. Use for deployments,
  troubleshooting, cost optimization, and security reviews.
```

**Level 2 — SKILL.md (the essentials):**

```markdown
# AWS Infrastructure Manager

## Quick Reference
- **EC2 instances**: Use these commands for listing, starting, stopping
- **S3 buckets**: Use these commands for upload, download, sync
- **IAM roles**: Follow this naming convention

## Full workflows
See references/ for detailed deployment and troubleshooting guides.
```

**Level 3 — References (the details):**

```markdown
# references/deployment.md

## ECS Deployment (full)

### Prerequisites
- AWS CLI configured
- Docker installed
- ECR repository exists

### Steps
1. Build Docker image
2. Tag and push to ECR
3. Update task definition
4. Deploy to ECS service
... (100+ lines of detailed steps)
```

---

## 10. Best Practices & Tips

### Do's

✅ **Describe WHEN to use** — Not just what the skill does

✅ **Be specific in triggers** — List exact user phrases that should activate the skill

✅ **Use concrete examples** — Show inputs and expected outputs

✅ **Define exact output format** — If needed, provide templates

✅ **Tell the agent about references** — Explain when to load each reference file

✅ **Keep it short** — Every line costs tokens. If you don't need it, delete it.

✅ **Use the right level of control** — High freedom for flexible tasks, low freedom for fragile operations

### Don'ts

❌ **Don't explain basic concepts** — The agent already knows what a PDF is

❌ **Don't create README files** — Skills are for agents, not humans browsing GitHub

❌ **Don't put "When to use" in the body** — That's what the frontmatter description is for. The body only loads after activation.

❌ **Don't create deeply nested references** — Keep everything one level from SKILL.md

❌ **Don't duplicate information** — If it's in references, don't repeat it in SKILL.md

❌ **Don't write "Great question! I'd be happy to help!"** — Skip the filler

### Checklist for a Good Skill

```
□ Frontmatter has a clear, specific description with trigger phrases
□ SKILL.md is under 500 lines
□ Each reference file has a table of contents (if over 100 lines)
□ SKILL.md tells the agent WHEN to load each reference
□ Workflows are step-by-step and unambiguous
□ Output formats have exact templates or examples
□ No duplicate information between SKILL.md and references
□ No unnecessary files (README, CHANGELOG, etc.)
□ Test prompts exist (in evals.json)
□ The skill follows progressive disclosure
```

---

## 11. Testing & Evaluating Skills

### Create evals.json

Place this in your skill directory to define test prompts:

```json
{
  "triggers": [
    "Review this pull request for me",
    "Can you check my code for bugs?",
    "What do you think of this PR?"
  ],
  "non_triggers": [
    "What's the weather today?",
    "Write a poem about code"
  ],
  "tests": [
    {
      "prompt": "Review the PR at https://github.com/org/repo/pull/42",
      "expected": "Should activate the PR review skill and analyze the diff"
    }
  ]
}
```

### Validate Your Skill

Use the `skillctl` tool:

```bash
# Validate structure
skillctl validate ./my-skill

# Full audit
skillctl audit

# Run evaluation tests
skillctl eval ./my-skill
```

---

## 12. Glossary

| Term | Definition |
|---|---|
| **Skill** | A self-contained package (SKILL.md + optional resources) that extends an agent's capabilities |
| **SKILL.md** | The main instructions file — the only file an agent reads automatically |
| **Frontmatter** | YAML metadata at the top of SKILL.md (`name` and `description`) |
| **Trigger** | A phrase or condition that causes the agent to activate a skill |
| **Reference** | A supplemental file in `references/` that's loaded on demand |
| **Script** | An executable file (Python, Bash) in `scripts/` that the agent can run |
| **Asset** | A file in `assets/` used in the agent's output (templates, images) |
| **Progressive Disclosure** | Loading content in layers (frontmatter → SKILL.md → references) to save context |
| **Context Window** | The total amount of text the AI agent can "see" at once |
| **Evals** | Test prompts that verify a skill works as expected |
