#!/usr/bin/env bash
# Fetch one reviewed Python Contrib release tag without overwriting its saved identity.
set -euo pipefail

fail() {
  printf 'Error: %s\n' "$*" >&2
  exit 1
}

[[ $# == 2 ]] || fail 'Usage: bash beacon/scripts/fetch-upstream-tag.sh vX.YbZ EXPECTED_COMMIT'
tag=$1
expected=$2
[[ $tag =~ ^v[0-9]+\.[0-9]+(b[0-9]+|\.[0-9]+)$ ]] || fail 'Only Python Contrib release tags are accepted'
[[ $expected =~ ^[0-9a-f]{40}$ ]] || fail 'Expected commit must be a full lowercase SHA-1'
git rev-parse --git-dir >/dev/null
git remote get-url upstream >/dev/null || fail 'Configure and verify the upstream remote first'

target_ref="refs/upstream-tags/$tag"
temporary_ref="refs/beacon-fetch/$tag-$$"
git show-ref --verify --quiet "$temporary_ref" && fail 'Temporary ref already exists'
previous=$(git rev-parse --verify --quiet "$target_ref" || true)

cleanup() {
  git update-ref -d "$temporary_ref"
}
trap cleanup EXIT

git fetch --no-tags --no-write-fetch-head --refmap= upstream "refs/tags/$tag:$temporary_ref"
candidate=$(git rev-parse --verify "$temporary_ref")
actual=$(git rev-parse --verify "$temporary_ref^{commit}")
[[ $actual == "$expected" ]] || fail "Tag $tag resolves to $actual, expected $expected; baseline was not updated"
if [[ -n $previous && $previous != "$candidate" ]]; then
  fail "Tag $tag object changed ($previous -> $candidate); baseline was not updated"
fi

git update-ref "$target_ref" "$candidate" "${previous:-0000000000000000000000000000000000000000}"
printf 'Verified %s: commit=%s tag-object=%s\n' "$target_ref" "$actual" "$candidate"
