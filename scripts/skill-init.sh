#!/usr/bin/env bash
# skill-init.sh — Scaffold a new skill interactively
# Usage: skill-init.sh <name> [path]

NAME="$1"
[[ -z "$NAME" ]] && { echo "Usage: $0 <skill-name> [output-path]"; exit 1; }

REGISTRY_DIR="$(dirname "$0")/.."
REGISTRY="$REGISTRY_DIR/skills-registry.json"
TEMPLATES="$REGISTRY_DIR/templates"

# Interactive template selection
echo "Select template:"
select TEMPLATE in basic with-scripts with-references full; do
  [[ -n "$TEMPLATE" ]] && break
  echo "Invalid selection"
done

OUTPUT="${2:-$HOME/.openclaw/workspace/.agents/skills/$NAME}"

if [[ -d "$OUTPUT" ]]; then
  echo "Error: $OUTPUT already exists"
  exit 1
fi

mkdir -p "$OUTPUT"
cp -r "$TEMPLATES/$TEMPLATE/"* "$OUTPUT/"
[[ -f "$OUTPUT/SKILL.md.template" ]] && mv "$OUTPUT/SKILL.md.template" "$OUTPUT/SKILL.md"

echo ""
echo "✓ Created skill '$NAME' from '$TEMPLATE' template"
echo "  Location: $OUTPUT"
echo ""
echo "Next:"
echo "  1. Edit $OUTPUT/SKILL.md"
echo "  2. $REGISTRY_DIR/skillctl validate $OUTPUT"
echo "  3. $REGISTRY_DIR/skillctl promote $OUTPUT draft"
