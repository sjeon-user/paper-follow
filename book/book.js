/* 지식 책 — 동작. index.html의 <section class="chapter"> 구조를 읽어
   목차·번호·검색·용어 풍선·역참조·표지를 자동으로 만든다. 내용 추가 시 이 파일은 손댈 필요 없음. */
(function () {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const esc = s => s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const reEsc = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

  const book = $('#book'), home = $('#home'), toc = $('#toc'), results = $('#results');
  const q = $('#q'), pager = $('#pager'), tip = $('#tip');
  const bookTitle = $('.book-title').textContent.trim();
  const chapters = $$('section.chapter', book);

  /* ── 1. 번호 매기기 ── */
  const parts = $$('.part', book);
  const counters = new Map();
  chapters.forEach(ch => {
    const app = ch.classList.contains('appendix');
    const h2 = $('h2', ch);
    ch._part = ch.closest('.part');
    ch._partTitle = ch._part ? ch._part.dataset.title : '부록';
    const key = ch._part || book;
    if (!app) counters.set(key, (counters.get(key) || 0) + 1);
    ch._title = h2.textContent.trim();
    ch._num = app ? '' : String(counters.get(key));
    ch._label = (ch._num ? ch._num + '. ' : '') + ch._title;
    ch._full = ch._partTitle + ' ' + ch._label;
    if (ch._num) h2.insertAdjacentHTML('afterbegin', `<span class="num">${ch._num}</span>`);
    ch._topics = $$('section.topic', ch);
    ch._topics.forEach((t, i) => {
      const h3 = $('h3', t);
      t._title = h3.textContent.trim();
      t._num = app ? '' : `${ch._num}.${i + 1}`;
      t._label = (t._num ? t._num + ' ' : '') + t._title;
      t._full = ch._partTitle + ' ' + t._label;
      if (t._num) h3.insertAdjacentHTML('afterbegin', `<span class="num">${t._num}</span>`);
      if (t.id) h3.insertAdjacentHTML('beforeend', `<a class="anchor" href="#${t.id}" title="이 항목으로 가는 링크">#</a>`);
    });
  });
  const mainCh = chapters.filter(c => !c.classList.contains('appendix'));
  const appCh = chapters.filter(c => c.classList.contains('appendix'));

  /* ── 2. 목차 ── */
  const tocCh = ch => `<div class="toc-ch" data-id="${ch.id}"><a href="#${ch.id}"><span class="num">${ch._num || '·'}</span><span>${esc(ch._title)}</span></a>` +
    (ch._topics.length ? '<ul>' + ch._topics.map(t => `<li><a href="#${t.id}">${esc(t._label)}</a></li>`).join('') + '</ul>' : '') + '</div>';
  const groups = parts.map(p => ({ id: p.id, title: p.dataset.title, desc: p.dataset.desc || '', chs: chapters.filter(c => c._part === p) }))
    .concat([{ id: 'appendix', title: '부록', desc: '', chs: appCh }]);
  toc.innerHTML = '<div class="tabs">' + groups.map(g => `<button type="button" data-tab="${g.id}">${esc(g.title)}</button>`).join('') + '</div>' +
    groups.map(g => `<div class="toc-part" data-part="${g.id}">` +
      (g.chs.length ? g.chs.map(tocCh).join('') : '<div class="toc-empty">아직 장이 없습니다.</div>') + '</div>').join('');
  function setTab(id) {
    if (!groups.some(g => g.id === id)) id = groups[0].id;
    $$('.tabs button', toc).forEach(b => b.classList.toggle('on', b.dataset.tab === id));
    $$('.toc-part', toc).forEach(d => { d.hidden = d.dataset.part !== id; });
    try { localStorage.setItem('book-tab', id); } catch (e) { }
  }
  toc.addEventListener('click', e => { const b = e.target.closest('.tabs button'); if (b) setTab(b.dataset.tab); });
  let savedTab = ''; try { savedTab = localStorage.getItem('book-tab') || ''; } catch (e) { }
  setTab(savedTab);

  /* ── 3. 검색 색인 (역참조를 붙이기 전에 만든다) ── */
  const units = [];
  chapters.forEach(ch => {
    const lead = $('.lead', ch);
    units.push({ id: ch.id, where: ch._partTitle, title: ch._label, text: ch._title + ' ' + (lead ? lead.textContent : '') });
    const where = ch._partTitle === '부록' ? ch._label : ch._partTitle + ' › ' + ch._label;
    $$('section.topic, dl.glossary > dt, ol.sources > li', ch).forEach(el => {
      if (!el.id) return;
      let title, text;
      if (el.tagName === 'DT') { title = el.textContent.trim(); text = title + ' ' + (el.nextElementSibling ? el.nextElementSibling.textContent : ''); }
      else if (el.tagName === 'LI') { const b = $('b', el); title = b ? b.textContent.trim() : el.textContent.trim().slice(0, 40); text = el.textContent; }
      else { title = el._label; text = el.textContent; }
      units.push({ id: el.id, where, title, text: text.replace(/\s+/g, ' ') });
    });
  });
  units.forEach(u => { u.low = u.text.toLowerCase(); });

  /* ── 4. 용어·자료 역참조 + 인용 번호 ── */
  const srcItems = $$('ol.sources > li');
  $$('a.cite').forEach(a => {
    const i = srcItems.findIndex(li => '#' + li.id === a.getAttribute('href'));
    if (i >= 0 && !a.textContent.trim()) a.textContent = i + 1;
  });
  const refs = new Map();
  $$('a.t, a.cite', book).forEach(a => {
    if (a.closest('dl.glossary, ol.sources')) return;
    const unit = a.closest('section.topic') || a.closest('section.chapter');
    const id = (a.getAttribute('href') || '').slice(1);
    if (!unit || !unit.id || !id) return;
    if (!refs.has(id)) refs.set(id, new Set());
    refs.get(id).add(unit);
  });
  refs.forEach((set, id) => {
    const el = document.getElementById(id);
    if (!el) return;
    const host = el.tagName === 'DT' ? el.nextElementSibling : el;
    if (host) host.insertAdjacentHTML('beforeend', '<div class="backrefs">나오는 곳: ' +
      [...set].map(u => `<a href="#${u.id}">${esc(u._full || u._label)}</a>`).join('') + '</div>');
  });

  /* ── 5. 표지 ── */
  const card = ch => `<a class="card" href="#${ch.id}">${ch._num ? `<span class="num">${ch._num}장</span>` : ''}<b>${esc(ch._title)}</b>` +
    `<p>${esc(($('.lead', ch) || {}).textContent || '')}</p>` +
    (ch._topics.length ? `<span class="cnt">항목 ${ch._topics.length}개</span>` : '') + '</a>';
  const recent = $$('[data-added][id]', book).map(el => ({
    id: el.id, date: el.dataset.added,
    label: el._full || el._label || ($('b', el) || el).textContent.trim().slice(0, 60)
  })).sort((a, b) => b.date.localeCompare(a.date)).slice(0, 8);
  $('#home-body').innerHTML =
    groups.map(g => `<div class="home-h">${esc(g.title)}</div>` + (g.desc ? `<p class="part-desc">${esc(g.desc)}</p>` : '') +
      (g.chs.length ? `<div class="cards">${g.chs.map(card).join('')}</div>` : '<div class="empty">아직 장이 없습니다.</div>')).join('') +
    (recent.length ? '<div class="home-h">최근 추가</div><ul class="recent">' +
      recent.map(r => `<li><time>${r.date}</time><a href="#${r.id}">${esc(r.label)}</a></li>`).join('') + '</ul>' : '');
  $('#stat').textContent = `주제 ${parts.length}개 · ${mainCh.length}장 · 항목 ${mainCh.reduce((s, c) => s + c._topics.length, 0)}개 · 용어 ${$$('dl.glossary > dt').length}개 · 자료 ${srcItems.length}건`;

  /* ── 6. 화면 전환 (주소의 #id 기준) ── */
  let current = null;
  function route() {
    let id = '';
    try { id = decodeURIComponent(location.hash.slice(1)); } catch (e) { }
    const el = id ? document.getElementById(id) : null;
    const ch = el ? el.closest('section.chapter') : null;
    document.body.classList.remove('menu-open');
    $$('.toc-ch').forEach(d => d.classList.toggle('active', !!ch && d.dataset.id === ch.id));
    if (ch) setTab(ch._part ? ch._part.id : 'appendix');
    if (!ch) {
      current = null; home.hidden = false; pager.hidden = true;
      chapters.forEach(c => { c.hidden = true; });
      document.title = bookTitle; window.scrollTo(0, 0); return;
    }
    current = ch; home.hidden = true;
    chapters.forEach(c => { c.hidden = c !== ch; });
    const i = chapters.indexOf(ch), p = chapters[i - 1], nx = chapters[i + 1];
    pager.hidden = false;
    pager.innerHTML = (p ? `<a class="prev" href="#${p.id}"><small>← 이전</small>${esc(p._label)}</a>` : '') +
      (nx ? `<a class="next" href="#${nx.id}"><small>다음 →</small>${esc(nx._label)}</a>` : '');
    document.title = ch._title + ' — ' + ch._partTitle + ' — ' + bookTitle;
    if (el === ch) window.scrollTo(0, 0);
    else {
      el.scrollIntoView();
      el.classList.remove('flash'); void el.offsetWidth; el.classList.add('flash');
    }
    highlight(el === ch ? ch : el);
    spy();
  }
  function spy() {
    if (!current) return;
    let here = null;
    current._topics.forEach(t => { if (t.getBoundingClientRect().top < 140) here = t; });
    $$('.toc-ch li a').forEach(a => a.classList.toggle('here', !!here && a.getAttribute('href') === '#' + here.id));
  }
  window.addEventListener('hashchange', route);
  window.addEventListener('scroll', spy, { passive: true });

  /* ── 7. 검색 ── */
  let tokens = [];
  function search() {
    tokens = q.value.toLowerCase().split(/\s+/).filter(Boolean);
    clearMarks();
    if (!tokens.length) { results.hidden = true; toc.hidden = false; return; }
    const re = new RegExp('(' + tokens.map(reEsc).join('|') + ')', 'gi');
    const hits = units.filter(u => tokens.every(t => u.low.includes(t)))
      .map(u => ({ u, score: tokens.reduce((s, t) => s + (u.title.toLowerCase().includes(t) ? 10 : 0) + Math.min(u.low.split(t).length - 1, 5), 0) }))
      .sort((a, b) => b.score - a.score).slice(0, 40);
    results.innerHTML = `<div class="res-count">${hits.length ? `결과 ${hits.length}건` : '결과가 없습니다'}</div>` +
      hits.map(({ u }) => {
        const pos = Math.max(0, u.low.indexOf(tokens[0]) - 30);
        const snip = (pos ? '…' : '') + u.text.slice(pos, pos + 110) + '…';
        return `<a href="#${u.id}">${u.where ? `<div class="res-where">${esc(u.where)}</div>` : ''}` +
          `<div class="res-title">${esc(u.title).replace(re, '<mark>$1</mark>')}</div>` +
          `<div class="res-snip">${esc(snip).replace(re, '<mark>$1</mark>')}</div></a>`;
      }).join('');
    results.hidden = false; toc.hidden = true;
  }
  function clearMarks() {
    $$('mark.hl', book).forEach(m => { const p = m.parentNode; p.replaceChild(document.createTextNode(m.textContent), m); p.normalize(); });
  }
  function highlight(root) {
    clearMarks();
    if (!tokens.length || !root) return;
    const re = new RegExp(tokens.map(reEsc).join('|'), 'gi');
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(node => {
      if (!node.nodeValue.trim() || node.parentNode.closest('svg, script, style')) return;
      const text = node.nodeValue; re.lastIndex = 0;
      if (!re.test(text)) return;
      const frag = document.createDocumentFragment(); let last = 0; re.lastIndex = 0; let m;
      while ((m = re.exec(text))) {
        if (m.index > last) frag.appendChild(document.createTextNode(text.slice(last, m.index)));
        const mk = document.createElement('mark'); mk.className = 'hl'; mk.textContent = m[0]; frag.appendChild(mk);
        last = m.index + m[0].length;
      }
      if (last < text.length) frag.appendChild(document.createTextNode(text.slice(last)));
      node.parentNode.replaceChild(frag, node);
    });
  }
  q.addEventListener('input', search);
  q.addEventListener('keydown', e => {
    if (e.key === 'Escape') { q.value = ''; search(); q.blur(); }
    if (e.key === 'Enter') { const a = $('a', results); if (a && !results.hidden) a.click(); }
  });
  document.addEventListener('keydown', e => {
    if (e.key === '/' && !/INPUT|TEXTAREA/.test(document.activeElement.tagName)) { e.preventDefault(); document.body.classList.add('menu-open'); q.focus(); q.select(); }
  });

  /* ── 8. 용어 풍선 ── */
  document.addEventListener('mouseover', e => {
    const a = e.target.closest && e.target.closest('a.t');
    if (!a) return;
    const dt = document.getElementById((a.getAttribute('href') || '').slice(1));
    const dd = dt && dt.nextElementSibling;
    if (!dd) return;
    const body = dd.cloneNode(true); $$('.backrefs', body).forEach(b => b.remove());
    tip.innerHTML = `<b>${esc(dt.textContent.trim())}</b>${esc(body.textContent.trim())}`;
    tip.hidden = false;
    const r = a.getBoundingClientRect();
    const left = Math.min(Math.max(8, r.left + window.scrollX), window.scrollX + document.documentElement.clientWidth - tip.offsetWidth - 8);
    let top = r.bottom + window.scrollY + 6;
    if (r.bottom + tip.offsetHeight + 12 > window.innerHeight) top = r.top + window.scrollY - tip.offsetHeight - 6;
    tip.style.left = left + 'px'; tip.style.top = top + 'px';
  });
  document.addEventListener('mouseout', e => { if (e.target.closest && e.target.closest('a.t')) tip.hidden = true; });

  /* ── 9. 메뉴 · 테마 ── */
  $('#menu-btn').addEventListener('click', () => document.body.classList.toggle('menu-open'));
  const root = document.documentElement;
  try { const t = localStorage.getItem('book-theme'); if (t) root.dataset.theme = t; } catch (e) { }
  $('#theme-btn').addEventListener('click', () => {
    const dark = root.dataset.theme ? root.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
    root.dataset.theme = dark ? 'light' : 'dark';
    try { localStorage.setItem('book-theme', root.dataset.theme); } catch (e) { }
  });

  route();
})();
