#!/bin/sh
set -eu

root="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
page="$root/credit/index.html"

test -f "$page"
test -f "$root/credit/manifest.webmanifest"
test -f "$root/credit/sw.js"
test -f "$root/credit/power.webp"
test -x "$root/tools/publish-credit.sh"

grep -q 'powvy credit' "$page"
grep -q '494784b4d08df1191bf6a35a0820c9cb/raw/powvy-credit-data.json' "$page"
grep -q 'setInterval(loadUsage, 60000)' "$page"
grep -q 'Claude' "$page"
grep -q 'Codex' "$page"
grep -q 'DeepSeek' "$page"
grep -q 'rel="manifest"' "$page"
grep -q 'serviceWorker.register' "$page"
grep -q '494784b4d08df1191bf6a35a0820c9cb' "$root/tools/publish-credit.sh"
grep -q '\.top{inset:20px 20px auto}' "$page"
grep -Fq '.week{margin-bottom:16px;' "$page"
grep -q 'href="/credit/"' "$root/index.html"

echo "credit page checks passed"
