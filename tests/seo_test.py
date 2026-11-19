"""SEO contract: crawlable URLs, correct language metadata, share assets and noindex exclusions."""
import json
import subprocess
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class Head(HTMLParser):
 def __init__(self,text):
  super().__init__();self.meta={};self.links=[];self.title='';self.in_title=False;self.feed(text.split('</head>',1)[0])
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='meta':self.meta[a.get('name',a.get('property'))]=a.get('content')
  if tag=='link':self.links.append(a)
  if tag=='title':self.in_title=True
 def handle_endtag(self,tag):
  if tag=='title':self.in_title=False
 def handle_data(self,text):
  if self.in_title:self.title+=text
class SEO(unittest.TestCase):
 def test_indexable_pages_and_sitemap(self):
  tree=ET.parse(ROOT/'sitemap.xml');ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
  urls=[n.text for n in tree.findall('s:url/s:loc',ns)]
  self.assertEqual(len(urls),44);self.assertEqual(len(set(urls)),44)
  self.assertEqual(sum('/projects/' in u for u in urls),32)
  self.assertEqual(sum('/articles/' in u for u in urls),8)
  for url in urls:
   self.assertNotIn('#',url)
   h=Head((ROOT/(url.removeprefix('https://powvy.org/')+'index.html')).read_text())
   self.assertEqual(h.title,h.meta['og:title']);self.assertEqual(h.meta['description'],h.meta['og:description'])
   self.assertEqual(h.meta['twitter:title'],h.title);self.assertEqual(h.meta['og:url'],url)
   self.assertIn({'rel':'canonical','href':url},h.links)
   self.assertTrue((ROOT/h.meta['og:image'].removeprefix('https://powvy.org/')).is_file())
   self.assertNotIn('live in 7 days',h.title)
 def test_bilingual_static_content_and_reproducibility(self):
  zh=(ROOT/'index.html').read_text();en=(ROOT/'en/index.html').read_text()
  self.assertIn('hreflang="en" href="https://powvy.org/en/"',zh)
  self.assertIn('hreflang="zh-Hans" href="https://powvy.org/"',en)
  self.assertIn("Hi, I'm Lucas",en[:en.index('<script>')])
  self.assertIn('<html lang="en">',en);self.assertIn('<base href="../">',en)
  self.assertNotIn('<a href="#',en)
  subprocess.run(['python3',str(ROOT/'scripts/build-seo.py')],check=True,capture_output=True)
  self.assertEqual(en,(ROOT/'en/index.html').read_text())
 def test_detail_content_and_language_pairs(self):
  for folder in ['projects','articles']:
   for file in (ROOT/folder).glob('*/index.html'):
    relative=file.relative_to(ROOT).as_posix()
    zh=file.read_text();en=(ROOT/'en'/relative).read_text()
    for text,language in [(zh,'zh-CN'),(en,'en')]:
     self.assertIn('<html lang="'+language+'">',text)
     self.assertIn('<h1>',text);self.assertIn('<div class="prose">',text)
     self.assertIn('application/ld+json',text)
     self.assertIn('hreflang="en"',text);self.assertIn('hreflang="zh-Hans"',text)
     self.assertNotIn('#/product/',text)
    self.assertNotEqual(Head(zh).meta['description'],Head(en).meta['description'])
  for home in ['index.html','en/index.html']:
   text=(ROOT/home).read_text().split('<script>')[0]
   self.assertIn('projects/power/',text);self.assertIn('articles/',text)
 def test_robots_and_private_pages(self):
  self.assertIn('Sitemap: https://powvy.org/sitemap.xml',(ROOT/'robots.txt').read_text())
  for name in ['inbox.html','connection.html']:
   self.assertIn('noindex',Head((ROOT/name).read_text()).meta['robots'])
  self.assertEqual(Head((ROOT/'index.html').read_text()).meta['google-site-verification'],'1JMtVifQAb0XnGrBBIRrITAheRsJ78Os9gnW_eOlF04')
if __name__=='__main__':unittest.main()
