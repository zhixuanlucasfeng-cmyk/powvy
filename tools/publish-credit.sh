#!/bin/zsh
set -euo pipefail

data=$(/usr/bin/curl -fsS --max-time 10 http://127.0.0.1:8899/widget.json)
print -r -- "$data" | /usr/bin/jq -e . >/dev/null
/usr/bin/jq -n --arg content "$data" '{files:{"powvy-credit-data.json":{content:$content}}}' |
  /usr/local/bin/gh api --method PATCH /gists/494784b4d08df1191bf6a35a0820c9cb --input - >/dev/null
