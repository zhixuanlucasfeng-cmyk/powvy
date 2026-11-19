// Keep the rendered language and detail dialog metadata in sync.
// Social crawlers receive the static metadata in / and /en/ without JavaScript.
function updatePowvySEO(language, detail) {
  const en = language === 'en';
  const defaults = en ? {
    title: 'Powvy · Products, Open Source & Writing by Lucas Feng',
    description: 'Explore AI tools, open-source projects, badminton and study products by Lucas Feng (Powvy), with project introductions and notes on building them.'
  } : {
    title: 'Powvy · Lucas Feng 的产品、开源项目与文章',
    description: 'Lucas Feng（Powvy）的个人网站：探索 AI 工具、开源项目、羽毛球与学习产品，阅读项目介绍和制作笔记。'
  };
  const {title, description} = detail || defaults;
  document.title = title;
  for (const [selector, value] of [
    ['meta[name="description"]', description],
    ['meta[property="og:title"]', title], ['meta[name="twitter:title"]', title],
    ['meta[property="og:description"]', description], ['meta[name="twitter:description"]', description],
    ['meta[property="og:locale"]', en ? 'en_US' : 'zh_CN']
  ]) document.querySelector(selector)?.setAttribute('content', value);
}
