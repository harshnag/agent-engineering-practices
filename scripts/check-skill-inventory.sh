#!/bin/sh

set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$root"

expected='agent-concurrency
agent-handover
checking-claims
coordinating-agents
cross-model-review
durable-project-memory
external-data-claims
measured-changes
project-agent-instructions
resource-safe-tooling
shipping-changes
verify-in-the-real-thing'

actual=$(
  find skills -mindepth 1 -maxdepth 1 -type d -exec basename {} \; |
    LC_ALL=C sort
)

if [ "$actual" != "$expected" ]; then
  printf '%s\n' 'Skill inventory mismatch.' >&2
  printf '%s\n%s\n' 'Expected:' "$expected" >&2
  printf '%s\n%s\n' 'Actual:' "$actual" >&2
  exit 1
fi

count=0
for skill in $expected; do
  if [ ! -f "skills/$skill/SKILL.md" ]; then
    printf 'Missing skills/%s/SKILL.md\n' "$skill" >&2
    exit 1
  fi
  count=$((count + 1))
done

printf 'Skill inventory OK: %s expected skills.\n' "$count"
