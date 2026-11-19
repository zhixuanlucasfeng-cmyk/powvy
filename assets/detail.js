// Reading and language navigation work without JavaScript; sharing is optional.
const share = document.getElementById('share');
share.hidden = false;
share.addEventListener('click', async () => {
  const en = document.documentElement.lang === 'en';
  const url = document.querySelector('link[rel="canonical"]').href;
  try {
    if (navigator.share) await navigator.share({title:document.title,url});
    else { await navigator.clipboard.writeText(url); document.getElementById('share-status').textContent=en?'Link copied':'链接已复制'; }
  } catch(error) {
    if(error.name!=='AbortError')document.getElementById('share-status').textContent=en?'Please copy the address from your browser.':'请复制浏览器地址栏中的链接。';
  }
});
