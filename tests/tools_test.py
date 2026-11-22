"""Tool directory stays crawlable and its real official links survive both languages."""
import sys
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from tools_pages import TOOLS
class Page(HTMLParser):
 def __init__(self,text):super().__init__();self.cards=[];self.links=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='article':self.cards.append(a)
  if tag=='a':self.links.append(a['href'])
for path in ['tools/index.html','en/tools/index.html']:
 text=(ROOT/path).read_text();page=Page(text)
 assert len(page.cards)==8 and all('hidden' not in c for c in page.cards)
 assert all(tool[4] in page.links for tool in TOOLS)
 assert 'https://heihei.run/' in page.links
 assert 'id="tool-empty" hidden' in text
 assert 'hreflang="en"' in text and 'hreflang="zh-Hans"' in text
assert 'href="tools/" data-i18n="navTools"' in (ROOT/'index.html').read_text()
assert 'href="en/tools/" data-i18n="navTools"' in (ROOT/'en/index.html').read_text()
print('PASS: 8 crawlable tools, official/source links, language pairs and homepage entry points')
