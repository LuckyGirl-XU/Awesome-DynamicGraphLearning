/* The complete catalogue is in the HTML; JavaScript adds filtering and pagination. */
(() => {
  'use strict';
  const catalog = JSON.parse(document.getElementById('catalog-data').textContent);
  const form = document.getElementById('filters');
  const search = document.getElementById('search');
  const year = document.getElementById('year');
  const topic = document.getElementById('topic');
  const code = document.getElementById('code');
  const sort = document.getElementById('sort');
  const list = document.getElementById('paper-list');
  const count = document.getElementById('results-count');
  const empty = document.getElementById('empty-state');
  const more = document.getElementById('load-more');
  const cards = new Map([...list.children].map(card => [card.dataset.paperId, card]));
  const searchable = new Map(catalog.papers.map(paper => [paper.id, [paper.title, paper.acronym, paper.venue, ...paper.topics.map(id => catalog.topics[id]), ...paper.links.map(link => link.url)].join(' ').normalize('NFKC').toLocaleLowerCase()]));
  const pageSize = 25;
  let limit = pageSize;

  function readURL() {
    const params = new URLSearchParams(location.search);
    search.value = params.get('q') || '';
    for (const [control, key] of [[year, 'year'], [topic, 'topic'], [code, 'code'], [sort, 'sort']]) {
      const value = params.get(key) || (key === 'sort' ? 'newest' : '');
      control.value = [...control.options].some(option => option.value === value) ? value : (key === 'sort' ? 'newest' : '');
    }
  }

  function writeURL() {
    const params = new URLSearchParams();
    const values = {q: search.value.trim(), year: year.value, topic: topic.value, code: code.value, sort: sort.value === 'newest' ? '' : sort.value};
    for (const [key, value] of Object.entries(values)) if (value) params.set(key, value);
    const query = params.toString();
    history.replaceState(null, '', location.pathname + (query ? '?' + query : '') + location.hash);
  }

  function render(updateURL = true) {
    const terms = search.value.trim().normalize('NFKC').toLocaleLowerCase().split(/\s+/).filter(Boolean);
    const matching = catalog.papers.filter(paper =>
      (!year.value || String(paper.year) === year.value) &&
      (!topic.value || paper.topics.includes(topic.value)) &&
      (!code.value || (code.value === 'with-code' ? paper.has_code : !paper.has_code)) &&
      terms.every(term => searchable.get(paper.id).includes(term))
    );
    matching.sort((a, b) => {
      if (sort.value === 'title') return a.title.localeCompare(b.title);
      const delta = sort.value === 'oldest' ? (a.year || 9999) - (b.year || 9999) : (b.year || 0) - (a.year || 0);
      return delta || a.title.localeCompare(b.title);
    });
    for (const card of cards.values()) card.hidden = true;
    const fragment = document.createDocumentFragment();
    matching.slice(0, limit).forEach(paper => {
      const card = cards.get(paper.id);
      card.hidden = false;
      fragment.append(card);
    });
    list.append(fragment);
    const visible = Math.min(limit, matching.length);
    count.textContent = matching.length === 0 ? '0 matching papers' : `Showing ${visible} of ${matching.length} paper records`;
    empty.hidden = matching.length !== 0;
    more.hidden = visible >= matching.length;
    more.textContent = `Show more papers (${matching.length - visible} remaining)`;
    if (updateURL) writeURL();
  }

  function clearFilters() {
    search.value = ''; year.value = ''; topic.value = ''; code.value = ''; sort.value = 'newest';
    limit = pageSize;
    render();
  }

  form.addEventListener('submit', event => event.preventDefault());
  form.addEventListener('input', () => { limit = pageSize; render(); });
  form.addEventListener('reset', event => { event.preventDefault(); clearFilters(); });
  sort.addEventListener('change', () => { limit = pageSize; render(); });
  document.getElementById('empty-reset').addEventListener('click', clearFilters);
  more.addEventListener('click', () => { limit += pageSize; render(); });
  list.addEventListener('click', event => {
    const button = event.target.closest('button[data-topic]');
    if (!button) return;
    topic.value = button.dataset.topic; limit = pageSize; render();
  });
  window.addEventListener('popstate', () => { readURL(); limit = pageSize; render(false); });
  readURL();
  render(false);
})();
