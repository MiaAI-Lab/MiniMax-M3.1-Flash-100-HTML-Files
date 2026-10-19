#!/usr/bin/env bash
# Publish from a clean temporary checkout so existing remote history is preserved.
set -euo pipefail
repo='MiaAI-Lab/MiniMax-M3.1-Flash-100-HTML-Files'
source_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
gh auth status
checkout_dir="$(mktemp -d /tmp/minimax-gallery-publish.XXXXXX)"
gh repo clone "$repo" "$checkout_dir"
cd "$checkout_dir"
if git rev-parse --verify HEAD >/dev/null 2>&1; then
  git switch main || git switch -c main
else
  git symbolic-ref HEAD refs/heads/main
fi
cp "$source_dir"/*.html "$source_dir"/*.txt "$source_dir/favicon.svg" "$source_dir/.nojekyll" .
mkdir -p scripts .github/workflows
cp "$source_dir"/scripts/*.py "$source_dir/scripts/publish.sh" scripts/
cp "$source_dir/.github/workflows/pages.yml" .github/workflows/
cp "$source_dir/README.md" .
if [ -d "$source_dir/thumbs" ]; then cp -r "$source_dir/thumbs" .; fi
git add -- '*.html' '*.txt' favicon.svg .nojekyll scripts .github/workflows/pages.yml README.md
if [ -d thumbs ]; then git add thumbs; fi
if ! git diff --cached --quiet; then
  git commit -m 'Add MiniMax-M3.1-Flash gallery with original prompts and screenshot deployment'
fi
# Set Pages to Actions before pushing, so the first workflow can deploy.
if gh api "repos/$repo/pages" >/dev/null 2>&1; then
  gh api --method PUT "repos/$repo/pages" -f build_type=workflow >/dev/null
else
  gh api --method POST "repos/$repo/pages" -f build_type=workflow >/dev/null
fi
git push -u origin main
printf 'Published source. Follow deployment: https://github.com/%s/actions\n' "$repo"
printf 'Pages URL after successful deployment: https://miaai-lab.github.io/MiniMax-M3.1-Flash-100-HTML-Files/\n'
