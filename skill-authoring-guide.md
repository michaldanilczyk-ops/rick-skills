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
9. [The 6-Step Skill Creation Process](#9-the-6-step-skill-creation-process)
10. [Progressive Disclosure Pattern](#10-progressive-disclosure-pattern)
11. [Best Practices & Tips](#11-best-practices--tips)
12. [Testing, Validating & Packaging](#12-testing-validating--packaging)
13. [Converting Company Knowledge into Skills](#13-converting-company-knowledge-into-skills)
14. [Glossary](#14-glossary)

---

## 1. What Is a Skill?

A **skill** is a self-contained package that extends what an AI agent can do. Think of it as an "onboarding manual" for a specific task or domain.

### What Skills Provide

1. **Specialized workflows** — Multi-step procedures for specific domains
2. **Tool integrations** — Instructions for working with specific file formats or APIs
3. **Domain expertise** — Company-specific knowledge, schemas, business logic, client context
4. **Bundled resources** — Scripts, references, and assets for complex/repetitive tasks

### Who Creates Skills?

- **Technical users** (developers): Write scripts, define structured outputs, build complex workflows
- **Non-technical users** (domain experts, PMs, analysts, sales): Write the instructions, define processes, capture client requirements and company knowledge

Both roles matter — a developer might write the scripts while a project manager writes the workflow instructions from client proposals.

### Skills vs. Company Knowledge Base

Skills are different from a knowledge base:

| Knowledge Base | Skill |
|---|---|
| Static documentation to be retrieved | Active instructions telling the agent *what to do* |
| "Here is our company policy" | "When a client asks about pricing, follow these steps" |
| Read-only reference | Actionable guide with workflows |
| May be hundreds of pages | Compact, token-efficient instructions |

Many skills use company knowledge as **reference material** (put in `references/`), but the SKILL.md itself tells the agent *how* to use that knowledge.

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
| `references/` | Documentation the agent might need to reference | Schemas, policies, API docs, full guides, company docs |
| `assets/` | Files used in the agent's output, not read as context | Templates, images, boilerplate code |

### Rules of thumb

- **Keep SKILL.md under 500 lines** — ideally 30–80 for simple skills. If it's longer, split content into `references/` files.
- **Don't create extra files** like README.md, CHANGELOG.md, or INSTALL.md. The skill is for the AI agent, not for humans browsing GitHub.
- **Scripts are optional** — many excellent skills have no code at all. They're pure instructions.
- **Name the folder exactly the same as the skill name.**
- **Only create directories you actually use** — don't keep empty `references/` or `scripts/` dirs.
- **No symlinks in packages** — the packager rejects them for security.

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

```yaml
---
name: skill-name-here
description: Clear description of what this skill does and when an agent should activate it.
---
```

**Only these fields are allowed:**

| Field | Required | Max length | Rules |
|---|---|---|---|
| `name` | ✅ Yes | 64 chars | Lowercase letters, digits, and hyphens only. No consecutive or leading/trailing hyphens. Verb-led preferred. |
| `description` | ✅ Yes | 1024 chars | Cannot contain angle brackets `<` or `>`. Include both WHAT and WHEN. |
| `license` | ❌ No | — | For distributed skills |
| `allowed-tools` | ❌ No | — | Restrict which tools the skill can use |
| `metadata` | ❌ No | — | Additional structured metadata |

Other fields will cause validation failure. Never add fields like `version`, `author`, `tags`, or `category` — those go in the agent system's configuration.

### Part 2: Markdown Body (everything after the second `---`)

Standard Markdown with step-by-step instructions. The agent reads this content only after the skill is activated.

---

## 4. Writing Effective Frontmatter

The frontmatter `description` is **the single most important part of your skill**. It's the only text the AI agent reads before deciding whether to use your skill.

### The Golden Rule

> **Tell the agent WHEN to use this skill, not just WHAT it does.**

### Good description

```yaml
description: >
  Review pull requests for code quality, security issues, and best practices.
  Activate when the user asks for code review, PR feedback, or says "review
  this PR". Also for pull request summaries and change analysis.
```

### Bad description

```yaml
description: Reviews code
```

### Pattern for descriptions

```
[What the skill does]. Activate when [specific triggers]. Also for [edge cases].
```

### Skill Naming

- Use lowercase letters, digits, and hyphens only
- Keep under 64 characters
- Use verb-led phrases that describe the action (e.g., `review-pull-requests`, `generate-reports`)
- Namespace by tool when it improves clarity (e.g., `linear-address-issue`, `gh-address-comments`)
- Name the folder exactly the same as the skill name

### Examples by type

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

### Set the Right Degrees of Freedom

Match the level of specificity to the task's fragility. Think of the agent as exploring a path: a narrow bridge with cliffs needs guardrails (low freedom), while an open field allows many routes (high freedom).

| Freedom | When to use | Example |
|---|---|---|
| **High freedom** (text instructions) | Multiple approaches valid, decisions depend on context | "Analyze this CSV and show key trends" |
| **Medium freedom** (pseudocode + parameters) | Preferred pattern exists, some variation acceptable | Python pseudocode with configurable parameters |
| **Low freedom** (specific scripts, few parameters) | Fragile operations, consistency critical | Exact bash commands, strict step sequences |

### Structure with headings

```markdown
# Skill Name

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

### Imperative Mood

Always write in imperative/infinitive form:
- ✅ "Run this command" / "Check for errors" / "Do this"
- ❌ "The agent should do this" / "This skill does X"

### Include What's Non-Obvious

A skill is for another AI agent to use. Include information that would be beneficial but non-obvious. Consider:
- What procedural knowledge would help?
- What domain-specific details matter?
- What reusable assets would make execution more efficient?

---

## 6. Linking References

References let you keep SKILL.md lean while providing deep knowledge when needed.

### How references work

- References go in `references/` directory
- Reference files are **NOT loaded automatically** — the agent reads them ONLY when it decides it needs more information
- You **must tell the agent** which references exist and when to load them

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

**☝️ CRITICAL:** Tell the agent which references exist and when to load them. The agent won't discover them on its own.

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
5. **Avoid duplication** — Information lives in SKILL.md OR references, not both
6. **Large files (>10K words)** — Include grep search patterns in SKILL.md so the agent can find what it needs

### Domain-specific organization

When a skill covers multiple domains, organize by domain:

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

| Variable | Source | Example |
|---|---|---|
| {incident_id} | Ask user or auto-generate | INC-2026-042 |
| {severity} | From incident classification | SEV1 / SEV2 / SEV3 |
| {impact} | Ask user for description | "3 hours of downtime" |
| {timeline} | Build from events | "12:00 — Detected\n12:05 — Paged" |
| {root_cause} | From investigation | "Certificate expired" |
| {action_items} | From resolution steps | "1. Renew cert\n2. Add monitoring" |

## Output Template

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
- ✅ Correctness, readability, documentation

### Step 4: Write the Review
Format your review like this:

```
## Overview
[1-2 sentence summary]

## Feedback

### Critical
- [Issue] — [file:line] — [explanation]

### Suggestions
- [Issue 2]

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
- **Bug report** → Go to Bug Workflow
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

## 9. The 6-Step Skill Creation Process

Follow these steps when creating a new skill from scratch. Skip a step ONLY when there is a clear reason why it doesn't apply (e.g., no scripts to write, no packaging needed).

### Step 1: Understand with Concrete Examples

Before writing anything, understand *exactly* what the skill should do.

**Ask these questions (don't overwhelm — ask the most important ones first):**
- What functionality should this skill support?
- What are concrete usage examples?
- What would a user say that should trigger this skill?
- Who will maintain this skill?

**For example**, when building an image-editor skill:
- "What functionality should it support? Editing, rotating, anything else?"
- "Can you give some examples of how this skill would be used?"
- "I can imagine users asking for things like 'Remove the red-eye' or 'Rotate this image'. Are there other ways you imagine this skill being used?"

**Conclude when** you have a clear sense of the functionality and trigger phrases.

### Step 2: Plan Reusable Contents

For each concrete example, analyze:
1. How would you execute this from scratch?
2. What scripts, references, and assets would help when repeating this?

**Example analysis for a PDF editor:**
- "Help me rotate this PDF" → Re-writing PDF rotation code each time → Create `scripts/rotate_pdf.py`

**Example analysis for a frontend webapp builder:**
- "Build me a todo app" → Same boilerplate HTML/React each time → Create `assets/hello-world/` template

**Example analysis for BigQuery:**
- "How many users logged in today?" → Re-discovering schemas each time → Create `references/schema.md`

**Compile the list of reusable resources:**
```
scripts/   → For repetitive code
references/ → For documentation that answers questions
assets/    → For templates and boilerplate
```

### Step 3: Initialize the Skill

**Never create the skill directory manually.** Always use the init script.

```bash
scripts/init_skill.py my-skill --path skills/public
scripts/init_skill.py my-skill --path skills/public --resources scripts,references,assets
scripts/init_skill.py my-skill --path skills/public --resources scripts --examples
```

The script creates:
- Skill directory with proper structure
- SKILL.md template with frontmatter and TODO placeholders
- Resource directories based on `--resources`
- Optional example files with `--examples`

### Step 4: Edit the Skill

**Start with reusable resources** (scripts, references, assets), then update SKILL.md.

**Testing scripts:** After writing any script, test it by running it to ensure no bugs and correct output. If there are many similar scripts, test a representative sample.

**Cleaning up:** If you used `--examples`, delete placeholder files that aren't needed. Only keep directories that are actually used.

**Writing SKILL.md:**
- Use imperative/infinitive form
- Keep frontmatter to `name` and `description` (plus optional `license`, `allowed-tools`, `metadata`)
- Put all "When to use" info in the description, NOT in the body
- The body is only loaded after triggering, so sections like "When to Use This Skill" in the body are useless to the agent
- Consult the design patterns in this guide for structure

### Step 5: Package the Skill (Optional — for distribution)

For skills that will be distributed to other agents or uploaded to ClawHub:

```bash
scripts/package_skill.py path/to/skill-folder
scripts/package_skill.py path/to/skill-folder ./dist
```

The packaging script:
1. **Validates automatically** — checks frontmatter format, naming conventions, description quality, directory structure
2. **Packages** into a `.skill` file (zip format) if validation passes
3. **Rejects symlinks** — doesn't package them for security

If validation fails, fix errors and run again.

### Step 6: Iterate

After using the skill on real tasks:
1. Notice struggles or inefficiencies
2. Identify what to update in SKILL.md or bundled resources
3. Implement changes and test again

Iteration often happens right after using the skill, with fresh context of how it performed.

---

## 10. Progressive Disclosure Pattern

This is the most important design pattern for skills. The context window is a shared resource — everything in it competes for attention.

### The Three Levels

```
Level 1: Frontmatter (~100 words)  ← ALWAYS loaded in context
  ↓  (only if user's request matches the description)
Level 2: SKILL.md body (<500 lines)  ← Loaded when skill triggers
  ↓  (only if the agent needs more detail)
Level 3: references/ files (unlimited) ← Loaded on demand
```

**Challenge every line:** "Does this justify its token cost?"

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
...
```

### When to split content

- SKILL.md approaching 500 lines? → Split into references
- Content used only for specific scenarios? → Move to references
- Content is reference material (schemas, policies)? → Put in references
- Core workflow and decision logic? → Keep in SKILL.md

### Multiple-variant pattern

When a skill supports multiple frameworks or providers, organize by variant:

```
cloud-deploy/
├── SKILL.md (workflow + provider selection)
└── references/
    ├── aws.md (AWS deployment patterns)
    ├── gcp.md (GCP deployment patterns)
    └── azure.md (Azure deployment patterns)
```

When the user says "deploy to AWS", the agent loads `aws.md`. GCP content stays out of context.

---

## 11. Best Practices & Tips

### Do's

✅ **Describe WHEN to use** — Not just what the skill does

✅ **Be specific in triggers** — List exact user phrases that should activate the skill

✅ **Use concrete examples** — Show inputs and expected outputs

✅ **Define exact output format** — If needed, provide templates

✅ **Tell the agent about references** — Explain when to load each reference file

✅ **Keep it short** — Every line costs tokens. If you don't need it, delete it.

✅ **Use the right level of control** — High freedom for flexible tasks, low freedom for fragile operations

✅ **Start with reusable resources** — Implement scripts/references/assets before writing SKILL.md

✅ **Test scripts by running them** — Don't rely on static analysis alone

✅ **Organize references by domain** — When a skill covers multiple domains, split across files

✅ **Include non-obvious info** — What would help another agent execute better?

### Don'ts

❌ **Don't explain basic concepts** — The agent already knows what a PDF is

❌ **Don't create README files** — Skills are for agents, not humans browsing GitHub

❌ **Don't put "When to use" in the body** — That's what the frontmatter description is for

❌ **Don't create deeply nested references** — Keep everything one level from SKILL.md

❌ **Don't duplicate information** — If it's in references, don't repeat it in SKILL.md

❌ **Don't write filler** — Skip "Great question! I'd be happy to help!"

❌ **Don't create the skill directory manually** — Always use the init script

❌ **Don't include extra YAML fields** — Only `name`, `description` (+ optional `license`, `allowed-tools`, `metadata`)

❌ **Don't use angle brackets in descriptions** — Validator will reject them

### Checklist for a Good Skill

```
□ Frontmatter has a clear, specific description with trigger phrases
□ SKILL.md is under 500 lines (prefer 30-80 for simple skills)
□ Each reference file has a table of contents (if over 100 lines)
□ SKILL.md tells the agent WHEN to load each reference
□ Workflows are step-by-step and unambiguous
□ Output formats have exact templates or examples
□ No duplicate information between SKILL.md and references
□ No unnecessary files (README, CHANGELOG, etc.)
□ Test prompts exist (in evals.json)
□ The skill follows progressive disclosure
□ Scripts have been tested by actually running them
□ Naming is valid (hyphen-case, ≤64 chars, no leading/trailing hyphens)
□ Description is ≤1024 chars with no angle brackets
```

---

## 12. Testing, Validating & Packaging

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

### Quick Validation

```bash
# Using the OpenClaw skill-creator
python scripts/quick_validate.py ./my-skill

# Using our skillctl
skillctl validate ./my-skill
skillctl audit
skillctl eval ./my-skill
```

### Validation Rules Summary

The validator checks:

| Check | What it validates |
|---|---|
| Frontmatter format | Must have opening/closing `---` lines |
| YAML validity | Must parse as valid YAML (PyYAML preferred, fallback parser available) |
| Allowed fields | Only `name`, `description`, `license`, `allowed-tools`, `metadata` |
| Name format | Hyphen-case, ≤64 chars, a-z0-9-, no leading/trailing/consecutive hyphens |
| Description | Required, ≤1024 chars, no `<` or `>` characters |
| SKILL.md exists | File must exist in root |

### Packaging for Distribution

```bash
# Validate + package into .skill file
scripts/package_skill.py ./my-skill
scripts/package_skill.py ./my-skill ./dist
```

The `.skill` file is a standard ZIP file with a `.skill` extension. It can be:
- Uploaded to ClawHub for public distribution
- Shared within your team
- Installed directly into an agent's skills directory

**Security note:** Symlinks are rejected during packaging. All resources must be real files.

---

## 13. Converting Company Knowledge into Skills

This section describes how to turn real business documents — proposals, contracts, presentations, requirements — into actionable skills for your team's AI agents.

### Why Convert Company Documents into Skills?

Many companies have valuable knowledge locked in documents that get used once and forgotten:

- **Proposals** — Contain deep understanding of client needs, solution architecture, pricing models
- **Contracts** — Define terms, deliverables, SLAs, obligations
- **Presentations** — Contain messaging, positioning, competitive analysis
- **Requirement specifications** — Define scope, workflows, user stories
- **Meeting notes** — Capture decisions, stakeholder preferences, context
- **Industry reports** — Contain domain expertise and benchmarks

Instead of keeping these as static PDFs, convert them into skills that guide the agent when working on similar projects.

### The Document-to-Skill Pipeline

```
Raw Document → Extract Knowledge → Structure → Skill
     ↓              ↓                  ↓          ↓
  Proposal    Key facts,            SKILL.md   Ready to use
  Contract    decisions,            + refs/    by agents
  Slides      workflows             + assets/
```

### Step 1: Inventory Your Documents

Start by identifying which documents are worth converting:

| Document Type | Skill Potential | Priority |
|---|---|---|
| Winning proposals | High — defines your consulting methodology | ⭐ High |
| Client contracts | High — terms, SLAs, obligations to reference | ⭐ High |
| Project presentations | Medium — messaging, positioning, deliverables | Medium |
| Internal process docs | High — repeatable workflows | ⭐ High |
| Meeting notes (strategic) | Medium — key decisions and context | Medium |
| Meeting notes (tactical) | Low — too specific, situational | Low |
| Competitive analysis | Medium — reference for positioning | Medium |

### Step 2: Extract What Matters

Don't put the entire document into a skill. Extract ONLY what the agent needs:

```markdown
# Converting a Proposal into a Skill

## Source: Proposal for Acme Corp (Salesforce Implementation)

### Extract these elements:
1. **Client context** → references/client-background.md
   - Industry, size, pain points
   - Key stakeholders and their priorities
2. **Solution architecture** → references/solution-design.md
   - What was proposed, why
   - Technical decisions and rationale
3. **Methodology** → SKILL.md workflow
   - The step-by-step approach used
   - Phases, milestones, deliverables
4. **Pricing model** → references/pricing.md
   - Rate cards, package options
   - Value drivers and ROI calculations
5. **Risk assessment** → references/risks.md
   - Identified risks and mitigations
   - Assumptions and constraints

### Discard:
- Boilerplate company overview (the agent should infer this)
- Generic methodology descriptions the agent already knows
- Formatting and branding elements
- Appendices with standard terms
```

### Step 3: Create the Skill Structure

A company knowledge skill has a different anatomy from a pure workflow skill:

```
acme-corp-project/
├── SKILL.md                    ← Workflow for working with this client
├── references/
│   ├── client-background.md    ← Client context, industry, stakeholders
│   ├── solution-design.md      ← Technical architecture decisions
│   ├── pricing.md              ← Pricing model and value drivers
│   ├── risks.md                ← Known risks and mitigations
│   └── deliverables.md         ← What was promised and when
└── assets/
    └── proposal-template.pptx  ← Template for