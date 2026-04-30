# Converting Company Knowledge into Skills
*A guide for Peak&Peak (Salesforce Consulting Company)*

---

## Why Convert Company Documents into Skills?

At Peak&Peak, every engagement generates valuable knowledge — proposals, contracts, presentations, requirements — that gets used once and then sits in a folder. Converting these into **actionable skills** means your AI agents can:

- Instantly reference past decisions and architecture choices
- Draft client communications with the right context
- Accelerate new project onboarding by reusing proven patterns
- Never lose the "why" behind technical decisions

The goal: turn static documents into **active intelligence** that guides the agent during each project phase.

---

## The Document-to-Skill Pipeline

```
Raw Document → Extract Knowledge → Structure → Skill
     ↓              ↓                  ↓          ↓
  Proposal    Key facts,            SKILL.md   Ready to use
  Contract    decisions,            + refs/    by agents
  Slides      workflows             + assets/
```

---

## Priority Matrix: What to Convert First

### Highest Value (do first)

| Document Type | Why | Expected Skill Output |
|---|---|---|
| **Winning proposals** | Contains your proven methodology, pricing, solution architecture | Workflow skill + client background references |
| **Client contracts / MSAs** | SLAs, terms, obligations you reference repeatedly | Reference skill (load when checking terms) |
| **SOWs (Statements of Work)** | Scope boundaries, deliverables, timeline | Project management workflow skill |
| **Internal delivery playbooks** | Your actual step-by-step processes | Pure workflow skill — highest ROI |
| **Discovery session notes** | Client pain points, stakeholder priorities, requirements | Client context reference skill |

### Medium Value

| Document Type | Why | Expected Skill Output |
|---|---|---|
| **Project presentations** | Messaging, positioning, competitive analysis | Presentation template + key messages |
| **Post-mortems / lessons learned** | What went wrong, what to avoid | Checklist skill (anti-patterns) |
| **Change requests** | Common scope change patterns | Change management workflow |
| **Status reports** | Reporting templates and cadence | Output template skill |

### Low Value (skip)

| Document Type | Why not |
|---|---|
| **Meeting notes (tactical)** | Too specific, changes too fast |
| **Generic training materials** | Agent already knows this |
| **Salesforce documentation** | Agent can read the official docs |
| **Old / superseded proposals** | Stakeholders and scope are outdated |
| **One-off client emails** | Not enough structure to extract |

---

## Real Examples for Peak&Peak

### Example 1: Converting a Winning Proposal (High Priority)

**Source:** Proposal for Acme Corp — Sales Cloud + Service Cloud implementation, €450K

**What to extract:**

```
acme-corp-project/
├── SKILL.md                         ← Workflow for this engagement
├── references/
│   ├── client-background.md         ← Industry (manufacturing), size, pain points
│   ├── solution-architecture.md     ← Sales Cloud + Service Cloud design decisions
│   ├── pricing-methodology.md       ← Rate card, phases, value drivers
│   ├── risks-and-mitigations.md     ← Known risks (data migration, change management)
│   ├── deliverables-timeline.md     ← Phases, milestones, acceptance criteria
│   └── stakeholder-map.md           ← Key people, their priorities, decision style
└── assets/
    └── proposal-deck.pptx           ← Original proposal for reference
```

**Sample SKILL.md:**

```yaml
---
name: acme-corp-engagement
description: Manage the Acme Corp Salesforce implementation engagement. Activate
  when user refers to Acme Corp, needs client-specific deliverables, status reports,
  or communications for this account. Use for timeline questions, scope decisions,
  and team coordination.
---
```

```markdown
# Acme Corp — Sales Cloud + Service Cloud Implementation

## Project Snapshot
- **Client:** Acme Corp (manufacturing, mid-market)
- **Budget:** €450K
- **Timeline:** Jan 2026 — Aug 2026 (8 months)
- **Team:** PM + 1 Tech Lead + 2 Developers + 1 BA
- **Products:** Sales Cloud, Service Cloud, Experience Cloud

## When to Load References

| Reference | Load when |
|---|---|
| [client-background.md](references/client-background.md) | Drafting client communications, understanding stakeholders |
| [solution-architecture.md](references/solution-architecture.md) | Discussing features, design decisions, technical approach |
| [pricing-methodology.md](references/pricing-methodology.md) | Budget discussions, change requests, scope changes |
| [risks-and-mitigations.md](references/risks-and-mitigations.md) | Status reports, risk register reviews, escalation prep |
| [deliverables-timeline.md](references/deliverables-timeline.md) | Scheduling, milestone tracking, deadline questions |
| [stakeholder-map.md](references/stakeholder-map.md) | Preparing for client meetings, understanding decision makers |

## Engagement Workflows

### Weekly Status Report
1. Check deliverables-timeline.md for this week's milestones
2. Review risks-and-mitigations.md for any active risks
3. Load the project tracker from Paperclip
4. Follow the status report template (see assets/)
5. Use client-background.md to set the right tone

### Change Request Handling
1. Check if request is in scope → solution-architecture.md
2. If out of scope, estimate impact → pricing-methodology.md
3. Identify affected stakeholders → stakeholder-map.md
4. Create change request document using standard template
5. Route through PM for client approval

### Client Meeting Prep
1. Load stakeholder-map.md — who's attending, what they care about
2. Check deliverables-timeline.md for recent progress
3. Review risks-and-mitigations.md for anything to raise
4. Draft agenda and talking points
```
```

### Example 2: Converting a Contract / MSA (High Priority)

**Source:** Master Services Agreement with TechVentures

**What to extract:**

```
techventures-msa/
├── SKILL.md                         ← When to check which terms
└── references/
    ├── payment-terms.md             ← Rates, invoicing, payment schedule
    ├── sla-obligations.md           ← Response times, penalties, credits
    ├── scope-and-deliverables.md    ← What's included, what's excluded
    ├── compliance-and-data.md       ← GDPR, security, data handling
    └── termination-and-notice.md    ← Notice periods, exit conditions
```

**Sample frontmatter:**
```yaml
description: >
  TechVentures MSA terms and engagement workflows. Activate when working on
  TechVentures projects, creating SOWs, checking contract terms, handling
  billing, or managing scope changes for this client. Essential for any
  contractual decision-making.
```

### Example 3: Converting Internal Delivery Playbooks (High Priority)

This is where you get the most bang for your buck. Your team has processes that live in people's heads — put them in skills.

**Sources:**
- Salesforce implementation methodology steps
- Data migration playbook
- Testing and UAT process
- Go-live checklist
- Handover procedures

**Sample skill structure:**

```
salesforce-implementation-playbook/
├── SKILL.md                         ← Top-level workflow
└── references/
    ├── discovery-phase.md           ← Requirements gathering, workshops
    ├── design-phase.md              ← Solution design, architecture docs
    ├── build-phase.md               ← Configuration, Apex, LWC, flows
    ├── testing-uat.md               ← Test plans, user acceptance
    ├── deployment-and-go-live.md    ← CI/CD, sandbox progression, cutover
    └── handover-and-support.md      ← Documentation, training, hypercare
```

---

## Extraction Template

Use this template for every document you convert:

```markdown
# Extraction Template

## Source Document
[Title, type, date, author]

## What It's Useful For
[When would an agent need this knowledge?]

## Extract This

### Facts (put in references/)
- Key data points, dates, numbers
- Decisions made and rationale
- Stakeholders and their priorities
- Technical specifications

### Workflows (put in SKILL.md)
- Step-by-step processes described
- Decision trees or conditional logic
- Quality criteria or acceptance standards

### Templates (put in assets/)
- Document templates (SOWs, status reports)
- Spreadsheets with formulas
- Presentation decks

## Discard This
- Boilerplate and filler content
- Generic information the agent already knows
- Outdated or superseded information
- Formatting-only elements

## Trigger Phrases (for frontmatter description)
- [List 3-5 phrases that should activate this skill]
```

---

## Document Type: Quick Reference

| Document | Keep in SKILL.md | Put in references/ | Put in assets/ | Discard |
|---|---|---|---|---|
| **Proposal** | Methodology, workflow steps | Client context, architecture, pricing | Proposal deck | Boilerplate, generic positioning |
| **Contract / MSA** | "When to check what" workflow | Terms, SLAs, obligations | — | Legal boilerplate, definitions |
| **Presentation** | Key messages, talking points | Competitive intel, positioning | The deck itself | Generic company slides |
| **Requirements doc** | Workflow for implementing | User stories, acceptance criteria | — | Standard definitions |
| **SOW** | Scope management workflow | Deliverables, timeline, exclusions | SOW template | Generic legal terms |

---

## When NOT to Convert a Document

Not every document should become a skill. Skip if:

- **The information is generic** — The agent already knows it (e.g., "what is Sales Cloud")
- **The document is one-off** — A single meeting note for a single decision
- **The knowledge changes too fast** — Weekly updates mean you'll never catch up
- **The document is pure Salesforce reference** — Agent should read official docs

**A good rule:** If you find yourself searching for the same document more than twice, convert it to a skill.

---

## Maintenance

Company knowledge skills need periodic attention:

- **Refresh when:** contracts renew, project phases end, new stakeholders appear
- **Remove when:** a client relationship ends, information is superseded, architecture changes
- **Lifecycle:** Draft → Released (when engagement starts) → Deprecated (when engagement ends)

---

## Quick Start: Your First Skill in 10 Minutes

1. Pick your **most recent winning proposal**
2. Open the extraction template above
3. Spend 5 minutes extracting the essentials (client context, architecture, pricing)
4. Run the init script: `scripts/init_skill.py client-name-engagement --path skills/ --resources references`
5. Write the SKILL.md workflow (5 minutes — keep it simple)
6. Copy extracted content into references/
7. Run validation: `scripts/package_skill.py ./skills/client-name-engagement`

Done. Now your agent knows how to work with this client.
