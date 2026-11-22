"""Bilingual, static tool directory. Descriptions checked against linked official sites."""
from html import escape as e

# id, name, category, platform, official URL, Chinese description, English description
TOOLS = [
 ('everything','Everything','files','Windows','https://www.voidtools.com/','记得文件名，却忘了存在哪？按名称查找本机文件和文件夹。','Find local files and folders by name when you remember the name but not the location.'),
 ('7zip','7-Zip','files','Windows · Linux · macOS','https://www.7-zip.org/','压缩与解压文件，支持 7z、ZIP 等格式。Windows 提供图形界面，其他平台提供命令行版本。','Pack and unpack archives including 7z and ZIP. Windows has a graphical interface; other platforms have command-line versions.'),
 ('wiztree','WizTree','files','Windows','https://diskanalyzer.com/','用可视化方块找出占空间的文件和文件夹，适合清理前先看清磁盘用量。授权条件以官网为准。','See which files and folders occupy your disk with a visual size map. Check the official site for licensing terms.'),
 ('pdf24','PDF24 Creator','documents','Windows','https://tools.pdf24.org/en/creator','在电脑上合并、拆分、压缩 PDF，也能使用虚拟 PDF 打印机。桌面版离线处理，文件留在本机。','Merge, split and compress PDFs, or use the virtual PDF printer. The desktop app processes files offline on your PC.'),
 ('sharex','ShareX','capture','Windows','https://getsharex.com/','截图、录屏和标注放在同一个工具里，也能按需要配置文件分享工作流。','Capture screenshots, record your screen and annotate images, with configurable file-sharing workflows.'),
 ('motrix','Motrix','transfer','Windows · macOS · Linux','https://motrix.app/','集中管理 HTTP、FTP、BitTorrent 和磁力链接下载，查看进度并暂停或继续任务。','Manage HTTP, FTP, BitTorrent and magnet downloads, track progress, and pause or resume tasks.'),
 ('localsend','LocalSend','transfer','Windows · macOS · Linux · iOS · Android','https://localsend.org/','在同一局域网的设备之间传文件，不需要注册账号。发送和接收设备都需要安装应用。','Send files between devices on the same local network without an account. Install the app on both devices.'),
 ('powertoys','Microsoft PowerToys','productivity','Windows','https://learn.microsoft.com/en-us/windows/powertoys/','一组 Windows 效率工具，包含窗口布局、键盘重映射、取色等功能，按需开启。','A collection of Windows utilities for window layouts, keyboard remapping, colour picking and more. Enable the tools you need.')
]
CATEGORIES = {'files':('文件与磁盘','Files & disks'),'documents':('文档','Documents'),'capture':('截图与录屏','Capture'),'transfer':('下载与传输','Transfers'),'productivity':('效率','Productivity')}

def build_tools(root):
 for en in (False, True):
  path='en/tools/' if en else 'tools/';home='en/' if en else './';other='tools/' if en else 'en/tools/'
  title='Useful tools · Powvy' if en else '精选工具 · Powvy'
  desc='A small directory of third-party tools for files, PDFs, screenshots and transfers, with links to their official sites.' if en else '整理文件、处理 PDF、截图和传文件的实用第三方工具，附用途说明和官网入口。'
  cards=[]
  for i,(key,name,category,platform,url,zh,eng) in enumerate(TOOLS,1):
   cards.append(f'<article class="tool" data-category="{category}" id="{key}"><span class="tool-number">{i:02d}</span><div><p class="eyebrow">{CATEGORIES[category][int(en)]}</p><h2>{e(name)}</h2><p>{e(eng if en else zh)}</p><p class="platform">{e(platform)}</p><a href="{url}" target="_blank" rel="noopener noreferrer">'+('Official site' if en else '前往官网')+f' <span aria-hidden="true">↗</span><span class="sr-only"> — {e(name)}</span></a></div></article>')
  options=''.join(f'<option value="{key}">{value[int(en)]}</option>' for key,value in CATEGORIES.items())
  html=f'''<!doctype html>
<html lang="{'en' if en else 'zh-CN'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><base href="{'../../' if en else '../'}">
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="https://powvy.org/{path}">
<link rel="alternate" hreflang="zh-Hans" href="https://powvy.org/tools/"><link rel="alternate" hreflang="en" href="https://powvy.org/en/tools/"><link rel="alternate" hreflang="x-default" href="https://powvy.org/tools/">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="https://powvy.org/{path}"><meta property="og:type" content="website"><meta property="og:image" content="https://powvy.org/assets/social/powvy.png"><meta property="og:locale" content="{'en_US' if en else 'zh_CN'}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title}"><meta name="twitter:description" content="{desc}"><meta name="twitter:image" content="https://powvy.org/assets/social/powvy.png">
<link rel="icon" href="favicon.ico?v=2"><link rel="stylesheet" href="assets/detail.css"><link rel="stylesheet" href="assets/tools.css"><script src="assets/tools.js" defer></script></head>
<body><header class="site-nav"><a class="brand" href="{home}">POWVY!</a><nav aria-label="{'Navigation' if en else '导航'}"><a href="{home}#products">{'Products' if en else '产品'}</a><a href="trending/">Trending</a><a href="{path}" aria-current="page">{'Tools' if en else '精选工具'}</a><a class="language" href="{other}" hreflang="{'zh-Hans' if en else 'en'}">{'中文' if en else 'EN'}</a></nav></header>
<main><div class="tools-intro"><div><p class="eyebrow">POWVY / TOOL SHELF</p><h1>{'Less friction.<br>Better tools.' if en else '工具选对了，<br>事情简单了。'}</h1><p>{desc}</p></div><img src="csm.png" width="1024" height="1024" alt="" aria-hidden="true"></div>
<p class="directory-note">{'Third-party software, not Powvy projects. Descriptions are based on official documentation, not hands-on reviews.' if en else '这里收录的是第三方软件，不是 Powvy 自研项目。介绍依据官方资料整理，不代表亲自安装评测。'}</p>
<div class="filters" hidden><label>{'Search tools' if en else '搜索工具'}<input type="search" id="tool-search" placeholder="{'Name or task, e.g. PDF' if en else '名称或用途，例如 PDF'}"></label><label>{'Category' if en else '分类'}<select id="tool-category"><option value="all">{'All categories' if en else '全部分类'}</option>{options}</select></label></div>
<p id="tool-count" role="status" aria-live="polite">{'8 tools' if en else '8 款工具'}</p><div class="tool-list">{''.join(cards)}</div>
<p id="tool-empty" hidden>{'No matching tools. Try another keyword or reset the category.' if en else '没有找到匹配的工具，试试其他关键词或切回全部分类。'}</p>
<aside class="source-note"><h2>{'About this collection' if en else '关于这份清单'}</h2><p>{'Inspired by the software directory at' if en else '这个栏目参考了'} <a href="https://heihei.run/" target="_blank" rel="noopener noreferrer">heihei.run · 悦宇玩机</a>{'. Descriptions were independently written using the linked official sites; the selection also includes additional tools.' if en else '的软件目录形式。内容根据各工具官网独立整理，并补充其他工具。'}</p><p>{'Links lead to the developers’ official sites. Powvy does not host installers. Check platform requirements and licensing there.' if en else '所有入口指向开发者官网，本站不托管安装包。具体系统要求和授权条件请以官网为准。'}</p></aside>
</main><footer><a href="{home}">{'← Back to Powvy' if en else '← 返回 Powvy 首页'}</a></footer></body></html>'''
  target=root/path/'index.html';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(html)
