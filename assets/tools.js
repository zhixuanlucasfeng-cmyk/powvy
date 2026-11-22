const search = document.querySelector('#tool-search');
const category = document.querySelector('#tool-category');
const cards = [...document.querySelectorAll('.tool')];
const english = document.documentElement.lang === 'en';
document.querySelector('.filters').hidden = false;
function filterTools() {
  const query = search.value.trim().toLocaleLowerCase();
  let count = 0;
  for (const card of cards) {
    const matches = (category.value === 'all' || category.value === card.dataset.category) && card.textContent.toLocaleLowerCase().includes(query);
    card.hidden = !matches;
    if (matches) count++;
  }
  document.querySelector('#tool-count').textContent = english ? `${count} of ${cards.length} tools` : `${count} / ${cards.length} 款工具`;
  document.querySelector('#tool-empty').hidden = count !== 0;
}
search.addEventListener('input', filterTools);
category.addEventListener('change', filterTools);
