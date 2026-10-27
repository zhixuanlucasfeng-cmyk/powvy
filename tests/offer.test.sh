#!/bin/sh
set -eu

page=${1:-index.html}

grep -Fq '让 AI 客服替你接住客户' "$page"
grep -Fq 'Deploy AI customer service' "$page"
grep -Fq 'AI 客服部署' "$page"
grep -Fq 'AI customer service deployment' "$page"
grep -Fq 'https://wa.me/8618707737002?text=' "$page"
grep -Fq 'target="_blank" rel="noopener"' "$page"
grep -Fq '<meta property="og:image" content="https://powvy.org/assets/social/ai-customer-service.png">' "$page"
test -s assets/social/ai-customer-service.png
