#!/usr/bin/env bash
# validate-skill.sh — Deep validation of a skill directory
# Usage: validate-skill.sh <skill-directory>
# Exit code: 0 = all good, 1 = errors

DIR="$1"
[[ -z "$DIR" ]] && { echo "Usage: $0 <skill-directory>"; exit 1; }
[[ ! -d "$DIR" ]] && { echo "Error: $DIR not found"; exit 1; }

SKILL_MD="$DIR/SKILL.md"
[[ ! -f "$SKILL_MD" ]] && { echo "FAIL: Missing SKILL.md"; exit 1; }

errors=0

# 1. Frontmatter must be valid YAML
frontmatter=$(sed -n '/^---$/,/^---$/p' "$SKILL_MD" 2>/dev/null)
echo "$frontmatter" | python3 -c "import sys,yaml; yaml.safe_load(sys.stdin); print('OK: frontmatter YAML is valid')" 2>/dev/null || { echo "FAIL: Invalid YAML frontmatter"; ((errors++)); }

# 2. Required fields
name=$(echo "$frontmatter" | grep "^name:" | head -1 | sed 's/^name:[[:space:]]*//')
desc=$(echo "$frontmatter" | grep "^description:" | head -1 | sed 's/^description:[[:space:]]*//')
[[ -z "$name" ]] && { echo "FAIL: Missing 'name' in frontmatter"; ((errors++)); }
[[ -z "$desc" ]] && { echo "FAIL: Missing 'description' in frontmatter"; ((errors++)); }
[[ ${#desc} -lt 10 ]] && { echo "WARN: description very short"; }

# 3. No extra fields in frontmatter
extra=$(echo "$frontmatter" | grep -v "^---$" | grep -v "^name:" | grep -v "^description:" | grep -v "^$")
[[ -n "$extra" ]] && echo "WARN: Extra frontmatter fields: $(echo $extra)"

# 4. Check directory name matches skill name
dirname=$(basename "$DIR")
[[ "$dirname" != "$name" ]] && echo "WARN: Dir '$dirname' != name '$name'"

# 5. Check for forbidden files
for f in README.md INSTALLATION_GUIDE.md QUICK_REFERENCE.md; do
  [[ -f "$DIR/$f" ]] && { echo "WARN: Unnecessary file: $f"; }
done

# 6. Check symlinks
found=$(find "$DIR" -type l 2>/dev/null)
[[ -n "$found" ]] && { echo "FAIL: Symlinks in skill (can't package): $found"; ((errors++)); }

# 7. Check file sizes
total_size=$(find "$DIR" -type f -not -path "*/\.*" -exec stat -f%z {} + 2>/dev/null | paste -sd+ | bc)
[[ $total_size -gt 1000000 ]] && echo "WARN: Skill total size > 1MB ($((total_size/1024))KB)"

# 8. Check scripts are executable
if [[ -d "$DIR/scripts" ]]; then
  for script in "$DIR/scripts"/*; do
    [[ -f "$script" ]] && [[ ! -x "$script" ]] && echo "WARN: Script not executable: $script"
  done
fi

exit $errors
