#!/usr/bin/env bash
# skill-audit.sh — Full health report on all skills in workspace
# Usage: skill-audit.sh

WORKSPACE_SKILLS="$HOME/.openclaw/workspace/.agents/skills"
WORKSPACE_LOCAL="$HOME/.openclaw/workspace/skills"
BUILTIN_SKILLS="/opt/homebrew/lib/node_modules/openclaw/skills"

echo "═══════════════════════════════════════════"
echo "  SKILL HEALTH AUDIT"
echo "  $(date)"
echo "═══════════════════════════════════════════"
echo ""

# Workspace skills (agent-level)
echo "── Agent Skills (workspace/.agents/skills/) ──"
if [[ -d "$WORKSPACE_SKILLS" ]]; then
  count=0
  for skill in "$WORKSPACE_SKILLS"/*/; do
    [[ -d "$skill" ]] || continue
    name=$(basename "$skill")
    if [[ -f "$skill/SKILL.md" ]]; then
      size=$(wc -c < "$skill/SKILL.md" | tr -d ' ')
      desc=$(sed -n '/^description:/{s/description: *//;p}' "$skill/SKILL.md" 2>/dev/null | head -1 | cut -c1-60)
      echo "  ✓ $name (${size}B) ${desc:+"— $desc"}"
    else
      echo "  ✗ $name (missing SKILL.md)"
    fi
    ((count++))
  done
  echo "  Total: $count"
else
  echo "  (empty)"
fi
echo ""

# Local workspace skills
echo "── Local Skills (workspace/skills/) ──"
if [[ -d "$WORKSPACE_LOCAL" ]]; then
  count=0
  for skill in "$WORKSPACE_LOCAL"/*/; do
    [[ -d "$skill" ]] || continue
    name=$(basename "$skill")
    if [[ -f "$skill/SKILL.md" ]]; then
      size=$(wc -c < "$skill/SKILL.md" | tr -d ' ')
      desc=$(sed -n '/^description:/{s/description: *//;p}' "$skill/SKILL.md" 2>/dev/null | head -1 | cut -c1-60)
      echo "  ✓ $name (${size}B) ${desc:+"— $desc"}"
    else
      echo "  ✗ $name (missing SKILL.md)"
    fi
    ((count++))
  done
  echo "  Total: $count"
else
  echo "  (empty)"
fi
echo ""

# Compare to built-in for gap analysis
echo "── Built-in Skills (overview) ──"
built_count=0
if [[ -d "$BUILTIN_SKILLS" ]]; then
  for dir in "$BUILTIN_SKILLS"/*/; do
    [[ -d "$dir" ]] && ((built_count++))
  done
  echo "  $built_count installed from OpenClaw"
fi

echo ""
echo "── Quick Health Summary ──"
echo "  ✓ Run: skillctl audit for full inventory + validation"
echo "  ✓ Run: skillctl registry to view lifecycle tracking"
echo "═══════════════════════════════════════════"
