"""Build the English entry from the existing homepage translations.
Run python3 scripts/build-seo.py after changing index.html; no third-party packages.
"""
import json
import re
import subprocess
from html import escape
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / 'index.html').read_text()
# The site already owns these translations; don't maintain a second copy.
js = source[source.index('const INK ='):source.index("let lang = 'zh';") if "let lang = 'zh';" in source else source.index('let lang = document.documentElement.lang')]
result = subprocess.run(['node', '-e', 'const vm=require(\'node:vm\');let s=\'\';process.stdin.on(\'data\',c=>s+=c);process.stdin.on(\'end\',()=>console.log(JSON.stringify(vm.runInNewContext(s+";let lang=\'zh\';({ui:EN.ui, EN, products, posts, covers:Object.fromEntries(products.map(p=>[p.id,productArt(p.id,true)])), postCovers:Object.fromEntries(posts.map(p=>[p.id,buddy(p.prop,p.bg)]))})",{}, {timeout:1000}))));'],input=js,text=True,capture_output=True,check=True)
data = json.loads(result.stdout)
translations = data['ui']

class TranslatedContent(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=False)
        self.text, self.stack, self.targets, self.edits = text, [], [], []
        self.lines = [0]
        for line in text.splitlines(keepends=True): self.lines.append(self.lines[-1] + len(line))
    def position(self):
        row, col = self.getpos()
        return self.lines[row - 1] + col
    def handle_starttag(self, tag, attrs):
        if tag in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}: return
        self.stack.append(tag)
        key = dict(attrs).get('data-i18n')
        if key:
            assert key in translations, key
            self.targets.append((len(self.stack), tag, self.position()+len(self.get_starttag_text()), key))
    def handle_endtag(self, tag):
        if self.targets and self.targets[-1][:2] == (len(self.stack),tag):
            _,_,start,key = self.targets.pop()
            self.edits.append((start,self.position(),translations[key]))
        if self.stack and self.stack[-1] == tag: self.stack.pop()

parser = TranslatedContent(source); parser.feed(source)
assert not parser.targets
text = source
for start,end,replacement in sorted(parser.edits,reverse=True):text=text[:start]+replacement+text[end:]
title = 'Powvy · Products, Open Source & Writing by Lucas Feng'
desc = 'Explore AI tools, open-source projects, badminton and study products by Lucas Feng (Powvy), with project introductions and notes on building them.'
text=text.replace('<html lang="zh-CN">','<html lang="en">',1).replace('<head>','<head>\n<base href="../">',1)
text=text.replace('Powvy · Lucas Feng 的产品、开源项目与文章',title).replace('Lucas Feng（Powvy）的个人网站：探索 AI 工具、开源项目、羽毛球与学习产品，阅读项目介绍和制作笔记。',desc)
for attr in ['<link rel="canonical" href=', '<meta property="og:url" content=']:
 text=text.replace(attr+'"https://powvy.org/"',attr+'"https://powvy.org/en/"',1)
text=text.replace('property="og:locale" content="zh_CN"','property="og:locale" content="en_US"',1).replace('property="og:locale:alternate" content="en_US"','property="og:locale:alternate" content="zh_CN"',1)
# A base URL fixes assets, while hash links must remain on the English page.
text=text.replace('href="#','href="en/#')
text=text.replace('id="langBtn" aria-label="切换语言 / Switch language">EN','id="langBtn" aria-label="切换语言 / Switch language">中',1)
text=text.replace('href="tools/"','href="en/tools/"')
(ROOT/'en').mkdir(exist_ok=True)
(ROOT/'en/index.html').write_text(text)
# Standalone pages and crawlable homepage lists share the same project data.
from seo_pages import build_pages
build_pages(ROOT, source, text, data)
print('Built English homepage:',len(parser.edits),'translated elements')

from tools_pages import build_tools
build_tools(ROOT)
