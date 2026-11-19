"""Static project/article output using only the content already on the homepage."""
import json
import re
from html import escape
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree, register_namespace

ORIGIN = 'https://powvy.org/'
S = 'http://www.sitemaps.org/schemas/sitemap/0.9'
X = 'http://www.w3.org/1999/xhtml'

def page_path(kind, key, language):
    return ('en/' if language == 'en' else '') + kind + '/' + key + '/'

def alternates(kind, key):
    zh = ORIGIN + page_path(kind, key, 'zh')
    en = ORIGIN + page_path(kind, key, 'en')
    return [('zh-Hans',zh),('en',en),('x-default',zh)]

def build_pages(root, zh_home, en_home, data):
    register_namespace('', S);register_namespace('xhtml', X)
    sitemap = Element('{'+S+'}urlset')
    def add_url(path, languages=()):
        node=SubElement(sitemap,'{'+S+'}url');SubElement(node,'{'+S+'}loc').text=ORIGIN+path
        for language,url in languages:SubElement(node,'{'+X+'}link',{'rel':'alternate','hreflang':language,'href':url})
    home_alts=[('zh-Hans',ORIGIN),('en',ORIGIN+'en/'),('x-default',ORIGIN)]
    for path in ('','en/'):add_url(path,home_alts)
    for path in ('trending/','credit/'):add_url(path)
    for language,home in [('zh',zh_home),('en',en_home)]:
        english=language=='en';home_url=ORIGIN+('en/' if english else '')
        for kind,source_key,container in [('projects','products','productList'),('articles','posts','postList')]:
            cards=[]
            for original in data[source_key]:
                item={**original,**(data['EN'][source_key].get(original['id'],{}) if english else {})}
                key=item['id'];assert re.fullmatch(r'[\w-]+',key)
                path=page_path(kind,key,language);url=ORIGIN+path
                heading=item.get('title',item.get('name'))
                desc=item.get('summary',item.get('desc',''))
                title=heading+' · Powvy'
                cover=data['postCovers' if kind=='articles' else 'covers'].get(key,'')
                if kind=='articles':
                    cover=re.sub(r'<use href="#csm"[^>]*/>', '<image href="csm.png" x="28" y="5" width="130" height="120" preserveAspectRatio="xMidYMid meet"/>',cover)
                    cover=re.sub(r'<use href="#dog"[^>]*/>', '',cover)
                if english and key=='restsolar':cover=cover.replace('转人工客服 →','Talk to an agent →')
                if kind=='articles':
                    body=item['body'];stamp=f'<time datetime="{escape(item["date"])}">{escape(item["date"])}</time> · Lucas Feng'
                else:
                    links=item.get('links') or [{'name':item['name'],'url':item['url']}]
                    for link in links:assert not re.match(r'(?!https?:)[a-zA-Z]+:',link['url']),link['url']
                    body='<p>'+escape(desc)+'</p><h2>'+('Key features' if english else '核心功能')+'</h2><ul>'+''.join('<li>'+escape(f)+'</li>' for f in item['features'])+'</ul><div class="project-links">'+''.join('<a class="btn" href="'+escape(link['url'],quote=True)+'" target="_blank" rel="noopener">'+('Open ' if english else '打开 ')+escape(link['name'])+' →</a>' for link in links)+'</div>'
                    stamp='PROJECT / 项目'
                    if all('github.com/' in link['url'] for link in links):body='<p class="notice">'+('Source code / installation instructions. This project needs installation or setup before use.' if english else '此入口提供源码或安装说明，需要安装或配置后使用。')+'</p>'+body
                schema={'@context':'https://schema.org','@type':'Article' if kind=='articles' else 'WebPage','name':heading,'headline':heading,'description':desc,'url':url,'inLanguage':'en' if english else 'zh-Hans','author':{'@type':'Person','name':'Lucas Feng'},'isPartOf':{'@type':'WebSite','name':'Powvy','url':ORIGIN}}
                if kind=='articles':schema['datePublished']=item['date']
                alts=alternates(kind,key)
                other=page_path(kind,key,'zh' if english else 'en')
                image=ORIGIN+'assets/social/powvy.png'
                html=f'''<!doctype html>
<html lang="{'en' if english else 'zh-CN'}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<base href="{'../' * len(path.strip('/').split('/'))}">
<title>{escape(title)}</title><meta name="description" content="{escape(desc,quote=True)}">
<link rel="canonical" href="{url}">
{''.join(f'<link rel="alternate" hreflang="{lang}" href="{href}">' for lang,href in alts)}
<link rel="icon" href="favicon.ico?v=2"><link rel="apple-touch-icon" href="favicon.png?v=2">
<link rel="stylesheet" href="assets/detail.css">
<meta property="og:type" content="{'article' if kind=='articles' else 'website'}"><meta property="og:site_name" content="Powvy">
<meta property="og:title" content="{escape(title,quote=True)}"><meta property="og:description" content="{escape(desc,quote=True)}"><meta property="og:url" content="{url}">
<meta property="og:locale" content="{'en_US' if english else 'zh_CN'}"><meta property="og:locale:alternate" content="{'zh_CN' if english else 'en_US'}">
<meta property="og:image" content="{image}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Powvy makes things.">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{escape(title,quote=True)}"><meta name="twitter:description" content="{escape(desc,quote=True)}"><meta name="twitter:image" content="{image}">
<script type="application/ld+json">{json.dumps(schema,ensure_ascii=False).replace('<',chr(92)+'u003c')}</script>
<script src="assets/detail.js" defer></script></head>
<body><header class="site-nav"><a class="brand" href="{'en/' if english else './'}">POWVY!</a><nav aria-label="{'Navigation' if english else '导航'}"><a href="{'en/' if english else './'}#products">{'Products' if english else '产品'}</a><a href="{'en/' if english else './'}#articles">{'Writing' if english else '文章'}</a><a href="trending/">Trending</a><a class="language" hreflang="{'zh-Hans' if english else 'en'}" href="{other}">{'中文' if english else 'EN'}</a></nav></header>
<main><div class="toolbar"><a href="{'en/' if english else './'}#{'articles' if kind=='articles' else 'products'}">{'← Back to homepage' if english else '← 返回首页'}</a><button id="share" type="button" hidden>{'Share' if english else '分享'}</button></div>
<article><div class="cover">{cover}</div><p class="eyebrow">{escape(item['tag'])} / {stamp}</p><h1>{escape(heading)}</h1><div class="prose">{body}</div></article>
<p id="share-status" role="status"></p>
<section class="related"><h2>{'Explore more' if english else '继续阅读'}</h2><ul>{''.join('<li><a href="'+page_path(kind,p['id'],language)+'">'+escape(({**p,**(data['EN'][source_key].get(p['id'],{}) if english else {})}).get('title',data['EN'][source_key].get(p['id'],{}).get('name',p.get('name','')) if english else p.get('name','')))+'</a></li>' for p in data[source_key] if p['id']!=key)}</ul></section>
</main><footer>Powvy · Lucas Feng / <a href="{'en/' if english else './'}">{'Home' if english else '首页'}</a></footer></body></html>'''
                target=root/path/'index.html';target.parent.mkdir(parents=True,exist_ok=True);target.write_text('\n'.join(line.rstrip() for line in html.split('\n')))
                add_url(path,alts)
                cards.append(f'<a class="card reveal in" href="{path}" data-{"product" if kind=="projects" else "post"}="{key}"><div class="cover">{cover}</div><div class="body"><span class="tag red">{escape(item["tag"])}</span><h3 class="title">{escape(heading)}</h3><p>{escape(desc)}</p></div></a>')
            block=f'<!-- seo:{container} -->\n<div class="grid" id="{container}">'+''.join(cards)+f'</div>\n<!-- /seo:{container} -->'
            pattern=f'<!-- seo:{container} -->.*?<!-- /seo:{container} -->'
            if re.search(pattern,home,re.S):home=re.sub(pattern,lambda _:block,home,flags=re.S)
            else:home=home.replace(f'<div class="grid" id="{container}"></div>',block)
        (root/('en/index.html' if english else 'index.html')).write_text('\n'.join(line.rstrip() for line in home.split('\n')))
    ElementTree(sitemap).write(root/'sitemap.xml',encoding='UTF-8',xml_declaration=True)
    print('Built',len(data['products'])*2,'project pages and',len(data['posts'])*2,'article pages;',len(sitemap),'sitemap URLs')
