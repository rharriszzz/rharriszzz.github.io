'use strict';

(() => {
  const form = document.querySelector('#filters');
  const search = document.querySelector('#search');
  const buttons = [...document.querySelectorAll('[data-filter]')];
  const cards = [...document.querySelectorAll('[data-project]')];
  if (!form || !search || !cards.length) return;

  let category = 'all';
  const query = new URLSearchParams(location.search);
  if (buttons.some(button => button.dataset.filter === query.get('category'))) {
    category = query.get('category');
  }
  search.value = query.get('q') || '';

  function update() {
    const terms = search.value.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
    let count = 0;
    for (const card of cards) {
      const categories = card.dataset.categories.split(' ');
      const categoryMatches = category === 'all' || (category === 'browser'
        ? card.dataset.browser === 'true' : categories.includes(category));
      const text = card.dataset.search.toLocaleLowerCase();
      card.hidden = !categoryMatches || !terms.every(term => text.includes(term));
      if (!card.hidden) count++;
    }
    for (const button of buttons) button.setAttribute('aria-pressed', String(button.dataset.filter === category));
    for (const id of ['featured-section', 'more-section']) {
      const section = document.getElementById(id);
      section.hidden = ![...section.querySelectorAll('[data-project]')].some(card => !card.hidden);
    }
    document.querySelector('#empty-state').hidden = count > 0;
    const filtered = category !== 'all' || terms.length > 0;
    document.querySelector('.collection').classList.toggle('is-filtered', filtered);
    document.querySelector('#results').textContent = filtered
      ? `${count} of ${cards.length} projects` : `${cards.length} projects · ${document.querySelectorAll('.project-card').length} selected below`;
    const url = new URL(location.href);
    if (category === 'all') url.searchParams.delete('category');
    else url.searchParams.set('category', category);
    if (search.value.trim()) url.searchParams.set('q', search.value.trim());
    else url.searchParams.delete('q');
    history.replaceState(null, '', url);
  }

  buttons.forEach(button => button.addEventListener('click', () => { category = button.dataset.filter; update(); }));
  search.addEventListener('input', update);
  form.addEventListener('submit', event => { event.preventDefault(); update(); });
  document.querySelector('#reset').addEventListener('click', () => {
    category = 'all'; search.value = ''; update(); search.focus();
  });
  update();
  form.hidden = false;
})();
