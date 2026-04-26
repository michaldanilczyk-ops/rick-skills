---
name: paperclip-assign
description: Assign tasks to Paperclip AI agents (CEO, Director of Operations, Director of Projects, etc.) by creating issues in the Paperclip project management system. Use this when the user wants to delegate work, create a task for an agent, or assign an issue.
---

# Paperclip Task Assignment

You can create issues in Paperclip and assign them to any agent in the company.

## When to Use

Use this skill when the user asks you to:
- "Assign [task] to [agent]"
- "Tell [agent] to [do something]"
- "Create a task for [agent]"
- "Delegate [work] to [agent]"
- "Give [agent] a ticket/issue/task"

## Available Agents

| Name | Role |
|------|------|
| CEO | Chief Executive Officer |
| Director of Operations | Operations lead |
| Director of Projects | Project delivery lead |
| Director of Technology | Tech lead |
| Salesforce Technical Lead | Solution architecture, Apex/LWC, integrations |
| Salesforce BA | Requirements, client workshops, UAT |
| Salesforce Platform Developer | Apex, LWC, Flow development |
| Senior Salesforce Consultant | Senior delivery resource |
| Integration & DevOps Engineer | CI/CD, integrations, DevOps |
| Business Development Manager | Sales, BD, client relationships |

## How to Create a Task

Run the assignment script:

```bash
~/.openclaw/tools/paperclip-assign.sh "<agent_name>" "<task_title>" "<task_description>" "<priority>"
```

**Priority values:** `urgent`, `high`, `medium` (default), `low`

**Example:**
```bash
~/.openclaw/tools/paperclip-assign.sh "Director of Operations" "Prepare Q2 budget report" "Compile expenses and forecast for Q2 board presentation" "high"
```

## Interpreting Results

A successful response looks like:
```
Task created: PEA-14
Assigned to: Director of Operations
Title: Prepare Q2 budget report
Priority: high
Status: backlog
View at: http://localhost:3101/PEA/issues/PEA-14
```

Tell the user the issue identifier (e.g. PEA-14), who it was assigned to, and confirm it's in the Paperclip backlog.

## Name Matching

The script does case-insensitive and partial matching, so "CEO", "ceo", "director of ops", "operations" will all work. If ambiguous, use the closest full match.

## Error Handling

If the script fails:
- "Unknown agent" → Check the agent name against the table above
- Connection errors → Paperclip runs on localhost:3101; confirm it's running
