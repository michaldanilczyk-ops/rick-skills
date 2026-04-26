#!/usr/bin/env python3
"""
Consulting Frameworks Analyzer

Applies 5 core consulting frameworks to dissect a problem or dataset:
1. MECE (Mutually Exclusive, Collectively Exhaustive) — decompose into clean, non-overlapping categories
2. Issue Tree — break the problem into hierarchical component parts
3. Hypothesis-Driven Problem Solving — propose, test, and refine hypotheses
4. Pareto Principle (80/20 Rule) — identify the vital few drivers
5. "What's the So What?" — extract actionable insight

Input: JSON problem description or CSV/JSON data file path
Output: Structured markdown analysis
"""

import json
import sys
import csv
import os
import collections
import re
from typing import Any

def read_input(source: str) -> dict:
    """Read problem/data from stdin, a file path, or inline JSON."""
    if source == "-" or source is None:
        raw = sys.stdin.read()
    elif os.path.isfile(source):
        with open(source) as f:
            raw = f.read()
    else:
        raw = source

    # Try JSON first
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    # Try CSV (expects structured data)
    try:
        lines = raw.strip().split("\n")
        reader = csv.DictReader(lines)
        rows = list(reader)
        if rows:
            return {"type": "tabular", "headers": reader.fieldnames, "rows": rows}
    except Exception:
        pass

    # Treat as free-form text problem description
    return {"type": "text", "content": raw.strip()}


def analyze_mece(data: dict) -> dict:
    """Apply MECE framework — find non-overlapping, exhaustive categories."""
    results = {"categories": [], "coverage_gaps": []}

    if data.get("type") == "tabular":
        headers = data.get("headers", [])
        rows = data.get("rows", [])
        # Identify categorical columns as potential MECE categories
        for h in headers:
            vals = [r.get(h, "") for r in rows if r.get(h, "")]
            unique = list(set(vals))
            if len(unique) <= len(rows) * 0.5 and len(unique) <= 20:
                results["categories"].append({
                    "field": h,
                    "values": unique,
                    "count": len(unique)
                })
    elif data.get("type") == "text":
        text = data.get("content", "")
        results["raw_text"] = text[:500]

    return results


def build_issue_tree(data: dict) -> dict:
    """Build an issue tree — hierarchical breakdown of the problem."""
    tree = {"root": "", "branches": []}

    if data.get("type") == "text":
        text = data.get("content", "")
        # Extract possible sub-problem categories from text markers
        lines = text.split("\n")
        candidates = []
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith("#") and len(stripped) > 10 and stripped.endswith(":"):
                candidates.append(stripped.rstrip(":"))
        tree["root"] = "Main Problem / Question"
        tree["branches"] = candidates if candidates else ["(No explicit subcategories found - text appears unstructured)"]
    elif data.get("type") == "tabular":
        headers = data.get("headers", [])
        tree["root"] = "Data Structure Analysis"
        for h in headers:
            tree["branches"].append({"dimension": h})
        tree["total_rows"] = len(data.get("rows", []))

    return tree


def analyze_hypothesis(data: dict) -> dict:
    """Hypothesis-driven analysis — propose what's driving the issue."""
    result = {
        "initial_hypothesis": None,
        "supporting_evidence": [],
        "contradicting_evidence": [],
        "refined_hypothesis": None,
    }

    if data.get("type") == "tabular":
        rows = data.get("rows", [])
        if rows:
            # Look for metrics columns (numeric) to find patterns
            for h in data.get("headers", []):
                vals = []
                for r in rows:
                    try:
                        vals.append(float(r.get(h, 0)))
                    except (ValueError, TypeError):
                        pass
                if len(vals) > 1:
                    avg = sum(vals) / len(vals)
                    max_v = max(vals)
                    min_v = min(vals)
                    if max_v > avg * 1.5:
                        result["supporting_evidence"].append(
                            f"'{h}' has high variance (min={min_v:.1f}, max={max_v:.1f}, avg={avg:.1f}) — potential key driver"
                        )
    elif data.get("type") == "text":
        text = data.get("content", "").lower()
        # Look for problem indicators
        indicators = ["problem", "issue", "challenge", "decline", "slow", "expensive", "late", "error", "failure"]
        found = [i for i in indicators if i in text]
        if found:
            result["initial_hypothesis"] = f"The core issue may relate to: {', '.join(found)}"
            result["supporting_evidence"].append("Problem indicators detected in description")

    return result


def apply_pareto(data: dict) -> dict:
    """Apply the 80/20 principle — find the vital few."""
    result = {"vital_few": [], "trivial_many_count": 0}

    if data.get("type") == "tabular":
        rows = data.get("rows", [])
        headers = data.get("headers", [])

        # Find numeric columns
        for h in headers:
            pairs = []
            for r in rows:
                try:
                    pairs.append((r.get(h, ""), float(r.get(h, 0))))
                except (ValueError, TypeError):
                    pass

            if pairs:
                pairs.sort(key=lambda x: x[1], reverse=True)
                total = sum(p[1] for p in pairs)
                cumulative = 0
                top20pct = max(1, len(pairs) // 5)
                for i in range(top20pct):
                    cumulative += pairs[i][1]
                if total > 0:
                    pct = (cumulative / total) * 100
                    if pct >= 50:
                        result["vital_few"].append({
                            "field": h,
                            "top_count": top20pct,
                            "total_count": len(pairs),
                            "cumulative_share_pct": round(pct, 1),
                            "driver_items": [str(p[0]) for p in pairs[:min(5, top20pct)]]
                        })

        result["trivial_many_count"] = max(0, len(rows) - sum(v["top_count"] for v in result["vital_few"]))

    elif data.get("type") == "text":
        text = data.get("content", "")
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        freq = collections.Counter(words).most_common()
        if freq:
            top20pct = max(1, len(freq) // 5)
            top = freq[:top20pct]
            total = sum(f for _, f in freq)
            top_sum = sum(f for _, f in top)
            pct = (top_sum / total) * 100 if total > 0 else 0
            result["vital_few"].append({
                "field": "Word Frequency",
                "top_count": top20pct,
                "total_count": len(freq),
                "cumulative_share_pct": round(pct, 1),
                "driver_items": [w for w, _ in top[:10]]
            })

    return result


def extract_insight(data: dict, analyses: dict) -> dict:
    """'What's the So What?' — distill into actionable insight."""
    insight = {
        "finding": "",
        "insight": "",
        "actionable_recommendation": "",
    }

    # Synthesize across all frameworks
    pareto = analyses.get("pareto", {})
    hypothesis = analyses.get("hypothesis", {})
    mece = analyses.get("mece", {})

    if pareto.get("vital_few"):
        for vf in pareto["vital_few"]:
            insight["finding"] = (
                f"{vf['top_count']} out of {vf['total_count']} items "
                f"account for {vf['cumulative_share_pct']}% of the total in '{vf['field']}'"
            )
            insight["insight"] = (
                f"This is a Pareto effect: a minority of items drive the majority of impact. "
                f"Focus effort on the top drivers rather than spreading resources thin."
            )
            insight["actionable_recommendation"] = (
                f"Immediately prioritize the top {vf['top_count']} items in '{vf['field']}'. "
                f"Consider deprioritizing or automating the remaining {max(0, vf['total_count'] - vf['top_count'])} items. "
                f"Set up monitoring to ensure the Pareto ratio doesn't shift unfavorably."
            )
            break

    if hypothesis.get("initial_hypothesis"):
        if not insight["finding"]:
            insight["finding"] = f"Hypothesis: {hypothesis['initial_hypothesis']}"
        if hypothesis.get("refined_hypothesis"):
            insight["insight"] = f"Original hypothesis refined to: {hypothesis['refined_hypothesis']}"
        if not insight["actionable_recommendation"]:
            insight["actionable_recommendation"] = (
                "Design targeted experiments to validate or invalidate this hypothesis. "
                "Collect data on the specific areas identified before committing to broad solutions."
            )

    if not any([insight["finding"], insight["insight"], insight["actionable_recommendation"]]):
        insight["finding"] = "Data analyzed for structural patterns"
        insight["insight"] = "No dominant patterns detected — consider collecting more granular data"
        insight["actionable_recommendation"] = "Expand the dataset or refine the problem statement"

    return insight


def generate_report(data: dict) -> str:
    """Apply all 5 frameworks and generate a structured report."""
    mece = analyze_mece(data)
    tree = build_issue_tree(data)
    hypothesis = analyze_hypothesis(data)
    pareto = apply_pareto(data)
    analyses = {"mece": mece, "tree": tree, "hypothesis": hypothesis, "pareto": pareto}
    insight = extract_insight(data, analyses)

    lines = []
    lines.append("# Consulting Frameworks Analysis\n")
    lines.append("_Generated by consulting-frameworks-analyzer_\n")

    # 1. MECE
    lines.append("## 1. MECE Framework\n")
    lines.append("*Mutually Exclusive, Collectively Exhaustive — decompose into clean, non-overlapping categories*\n")
    if mece.get("categories"):
        lines.append("| Field | Values | Count |")
        lines.append("|-------|--------|-------|")
        for cat in mece["categories"]:
            vals = ", ".join(str(v) for v in cat["values"][:5])
            if len(cat["values"]) > 5:
                vals += f"... +{len(cat['values'])-5} more"
            lines.append(f"| {cat['field']} | {vals} | {cat['count']} |")
    else:
        lines.append("No clear categorical breakdown detected in the data.\n")
        if mece.get("raw_text"):
            lines.append(f"> Sample: _{mece['raw_text'][:200]}_\n")
    lines.append("")

    # 2. Issue Tree
    lines.append("## 2. Issue Tree\n")
    lines.append("*Hierarchical breakdown of the problem into component parts*\n")
    lines.append(f"**Root:** {tree.get('root', 'Unknown')}\n")
    branches = tree.get("branches", [])
    if branches:
        lines.append("**Branches:**")
        for i, b in enumerate(branches):
            if isinstance(b, dict):
                lines.append(f"  {i+1}. {b.get('dimension', str(b))}")
            else:
                lines.append(f"  {i+1}. {b}")
    lines.append("")

    # 3. Hypothesis-Driven
    lines.append("## 3. Hypothesis-Driven Problem Solving\n")
    lines.append("*Start with a hypothesis, gather evidence, refine*\n")
    if hypothesis.get("initial_hypothesis"):
        lines.append(f"**Initial hypothesis:** {hypothesis['initial_hypothesis']}\n")
    else:
        lines.append("**Initial hypothesis:** No hypothesis proposed — data may lack context.\n")

    if hypothesis.get("supporting_evidence"):
        lines.append("**Supporting evidence:**")
        for e in hypothesis["supporting_evidence"]:
            lines.append(f"  ✅ {e}")
    if hypothesis.get("contradicting_evidence"):
        lines.append("**Contradicting evidence:**")
        for e in hypothesis["contradicting_evidence"]:
            lines.append(f"  ⚠️ {e}")
    if hypothesis.get("refined_hypothesis"):
        lines.append(f"\n**Refined hypothesis:** {hypothesis['refined_hypothesis']}\n")
    lines.append("")

    # 4. Pareto
    lines.append("## 4. Pareto Principle (80/20 Rule)\n")
    lines.append("*Identify the vital few that drive the majority of impact*\n")
    if pareto.get("vital_few"):
        for vf in pareto["vital_few"]:
            lines.append(f"**{vf['field']}:**")
            lines.append(f"- Top {vf['top_count']} items ({vf['cumulative_share_pct']}% of total)")
            lines.append(f"- Total items in category: {vf['total_count']}")
            if vf.get("driver_items"):
                lines.append(f"- Top drivers: {', '.join(vf['driver_items'][:5])}")
            lines.append("")
    else:
        lines.append("No significant Pareto distribution detected — values may be evenly distributed.\n")
    lines.append("")

    # 5. So What
    lines.append("## 5. What's the So What?\n")
    lines.append("*Distill findings into actionable insight*\n")
    if insight.get("finding"):
        lines.append(f"**Finding:** {insight['finding']}\n")
    if insight.get("insight"):
        lines.append(f"**Insight (why it matters):** {insight['insight']}\n")
    if insight.get("actionable_recommendation"):
        lines.append(f"**Actionable recommendation:** {insight['actionable_recommendation']}\n")

    lines.append("---")
    lines.append("_Analysis complete — review each section, refine hypotheses, and iterate._")

    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Apply 5 consulting frameworks to analyze a problem or dataset")
    parser.add_argument("input", nargs="?", default="-",
                        help="Input: file path, JSON string, or '-' for stdin")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON instead of markdown report")
    args = parser.parse_args()

    data = read_input(args.input)
    mece = analyze_mece(data)
    tree = build_issue_tree(data)
    hypothesis = analyze_hypothesis(data)
    pareto = apply_pareto(data)
    analyses = {"mece": mece, "tree": tree, "hypothesis": hypothesis, "pareto": pareto}
    insight = extract_insight(data, analyses)

    full = {
        "frameworks_used": [
            "MECE (Mutually Exclusive, Collectively Exhaustive)",
            "Issue Tree",
            "Hypothesis-Driven Problem Solving",
            "Pareto Principle (80/20 Rule)",
            "What's the So What?"
        ],
        "input_type": data.get("type", "unknown"),
        "analyses": analyses,
        "insight": insight
    }

    if args.json:
        print(json.dumps(full, indent=2))
    else:
        report = generate_report(data)
        print(report)


if __name__ == "__main__":
    main()
