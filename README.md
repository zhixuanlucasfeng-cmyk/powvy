# Powvy

[访问网站 / Visit the website](https://zhixuanlucasfeng-cmyk.github.io/powvy/)

## 中文

Lucas（Powvy）的中英双语个人网站，采用漫画墨线、网点纸和黑红配色。

- **产品与开源**：AI 工具、学习应用、企业网站及公开 GitHub 仓库。
- **项目文章**：Power、Powy、Restar Solar 和 A-Level Survival Bureau 的介绍。
- **关于我**：个人简介、学习与项目经历；社交入口目前仅保留 GitHub。
- 支持中英切换、项目与文章详情、保存和分享；星标请求失败时显示兜底状态。

### 本地预览

需要 Git 和 Python 3，无需安装前端依赖或执行构建。

```sh
git clone https://github.com/zhixuanlucasfeng-cmyk/powvy.git
cd powvy
python3 -m http.server 8765 --bind 127.0.0.1
```

打开 [本地页面](http://127.0.0.1:8765/)，按 `Ctrl+C` 停止服务。

### 文件与部署

- `index.html`：页面、内联 CSS、原生 JavaScript 及中英双语内容。
- `hero.png`：首屏透明插画。
- `csm.png`：“关于我”透明插画。

GitHub Pages 从 `main` 分支根目录发布，推送后自动更新。图片使用相对路径，部署时需与 HTML 一起保留。字体与 GitHub 星标需要联网；前端不包含 GitHub token。

## English

Lucas (Powvy)'s bilingual personal website, with manga-inspired ink lines, halftone textures and a black-and-red palette.

- **Products and open source:** AI tools, study apps, company websites and public GitHub repositories.
- **Project articles:** introductions to Power, Powy, Restar Solar and A-Level Survival Bureau.
- **About:** a short biography, education and project experience. GitHub is currently the only social link.
- Chinese/English switching, product and article details, saving and sharing, and a fallback when GitHub star counts are unavailable.

### Local preview

Requires Git and Python 3. No frontend dependencies or build step are needed.

```sh
git clone https://github.com/zhixuanlucasfeng-cmyk/powvy.git
cd powvy
python3 -m http.server 8765 --bind 127.0.0.1
```

Open [the local page](http://127.0.0.1:8765/). Press `Ctrl+C` to stop the server.

### Files and deployment

- `index.html`: the page, inline CSS, vanilla JavaScript and bilingual content.
- `hero.png`: transparent hero illustration.
- `csm.png`: transparent illustration in the About section.

GitHub Pages publishes from the root of `main` and updates after a push. Keep the images alongside the HTML so relative paths work. Fonts and GitHub star counts need an internet connection; no GitHub token is included in the frontend.
