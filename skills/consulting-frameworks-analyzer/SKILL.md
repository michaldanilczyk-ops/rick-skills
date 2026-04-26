---
name: consulting-frameworks-analyzer
description: Apply 5 core consulting frameworks (MECE, Issue Trees, Hypothesis-Driven, Pareto/80-20, What's the So What) to dissect problems and data. Use when the user asks to: analyze data with consulting frameworks, break down a problem, find root causes, structure messy information, prioritize solutions, communicate insights, or "consultant-mode" analysis. Trigger on phrases like "framework analysis", "consulting framework", "MECE", "issue tree", "80/20 analysis", "Pareto", "hypothesis-driven", "so what".
---

# Consulting Frameworks Analyzer

Analyze problems and data using 5 core consulting frameworks. The script applies all frameworks to any input — structured data (CSV/JSON) or free-text problem descriptions.

## Frameworks

| # | Framework | What it does |
|---|-----------|-------------|
| 1 | **MECE** | Splits data into Mutually Exclusive, Collectively Exhaustive categories |
| 2 | **Issue Tree** | Builds hierarchical breakdown of the problem into component parts |
| 3 | **Hypothesis-Driven** | Proposes what's driving the issue, finds supporting/contradicting evidence |
| 4 | **Pareto 80/20** | Identifies the vital few items driving most of the impact |
| 5 | **So What** | Distills findings into actionable insight and recommendation |

## Usage

### From a CSV file (tabular data):

```bash
python3 scripts/analyze.py path/to/data.csv
```

### From a JSON file:

```bash
python3 scripts/analyze.py path/to/data.json
```

### From inline JSON:

```bash
python3 scripts/analyze.py '{"type":"text","content":"Sales are declining. We have 500 customers..."}'
```

### From stdin:

```bash
cat data.csv | python3 scripts/analyze.py
```

### JSON output:

```bash
python3 scripts/analyze.py data.csv --json
```

## Input formats

- **CSV**: Auto-detected with headers as field names. Numeric columns get Pareto analysis; columns with few unique values get MECE categorization.
- **JSON**: Supports `{"type": "tabular", "headers": [...], "rows": [...]}` or `{"type": "text", "content": "..."}`
- **Raw text**: Any text that isn't valid JSON or CSV is treated as a free-form problem description.

## Output

Markdown report (default) or JSON (`--json` flag). Each framework gets its own section with findings specific to the input.
