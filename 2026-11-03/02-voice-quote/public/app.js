/* Voice quote: the page.
   Talk through a job (or upload a voice note, or type it), add site photos, press Build the quote.
   Whisper writes the voice note down, the LLM reads it into the job sheet, and this file prices the job sheet
   from price-list.json. Pricing is plain code below (priceJob). Nothing here invents a number: a fact that was
   not said is asked for, and anything not on the price list becomes a Needs a price line at zero. */

const S = { pl: null, health: null, photos: [], audio: null, audioSecs: 0, example: null, rec: null, quoteNo: 0 };
const root = document.getElementById('app');
const side = document.getElementById('side');

/* ---------- a tiny element builder: text always goes in as text, never as HTML ---------- */
function h(tag, attrs, ...kids) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v == null || v === false) continue;
    if (k.startsWith('on')) el.addEventListener(k.slice(2).toLowerCase(), v);
    else if (k === 'class') el.className = v;
    else el.setAttribute(k, v === true ? '' : v);
  }
  for (const kid of kids.flat(Infinity)) if (kid != null && kid !== false) el.append(kid instanceof Node ? kid : String(kid));
  return el;
}
const fill = (el, ...kids) => el.replaceChildren(...kids.flat(Infinity).filter((k) => k != null && k !== false));
const money = (n) => new Intl.NumberFormat(S.pl.locale || 'en-AU', { style: 'currency', currency: S.pl.currency || 'AUD' }).format(n || 0);
const esc = (v) => String(v ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const cap1 = (t) => String(t || '').charAt(0).toUpperCase() + String(t || '').slice(1);
const mmss = (s) => Math.floor(s / 60) + ':' + String(Math.round(s) % 60).padStart(2, '0');

async function getJSON(url, opts) {
  let r;
  try { r = await fetch(url, opts); } catch { throw new Error('The quote app is not running on this computer. Start it (node server.mjs), then refresh this page.'); }
  const j = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(j.error || 'Something went wrong. Try again.');
  return j;
}

/* ---------- the job sheet to facts, by the type each fact has in the price list ---------- */
function factsOf(sheet, jobKey) {
  const job = S.pl.jobs[jobKey], facts = {}, said = {};
  for (const f of sheet.facts || []) {
    const [k, name] = String(f.name).split('.');
    const d = job.facts && Object.hasOwn(job.facts, name) ? job.facts[name] : null;
    if (k !== jobKey || !d) continue;
    const raw = String(f.value).trim();
    let v = null;
    if (d.type === 'number') { const n = parseFloat(raw.replace(/[^0-9.]/g, '')); v = Number.isFinite(n) && n > 0 ? n : null; }
    else if (d.type === 'count') { const n = parseInt(raw.replace(/[^0-9]/g, ''), 10); v = Number.isFinite(n) ? n : null; }
    else if (d.type === 'yes_no') v = /^(y|yes|true)$/i.test(raw);
    else v = raw || null;
    if (v != null) { facts[name] = v; said[name] = f.said; }
  }
  return { facts, said };
}
const labelOf = (jobKey, n) => ((S.pl.jobs[jobKey].facts || {})[n] || {}).label || cap1(n.replace(/_/g, ' '));
const shown = (v) => (v === true ? 'Yes' : v === false ? 'No' : String(v));
const missingOf = (jobKey, facts) => Object.entries(S.pl.jobs[jobKey].facts || {}).filter(([n, d]) => d.needed && facts[n] == null).map(([n, d]) => [n, d]);

/* ---------- the pricing: facts to lines, from the price list only ---------- */
function qtyOf(q, facts) {
  if (typeof q === 'number') return q;
  if (typeof q === 'string') { const v = facts[q]; return v === true ? 1 : typeof v === 'number' ? v : 0; }
  let v = typeof facts[q.of] === 'number' ? facts[q.of] : 0;
  if (!v) return 0;
  if (q.times) v *= q.times;
  if (q.every) v = Math.ceil(v / q.every);
  if (q.plus) v += q.plus;
  return v;
}
function priceJob(jobKey, facts, said, notPriced) {
  const job = S.pl.jobs[jobKey], lines = [];
  for (const l of job.lines) {
    if (l.only_if && !facts[l.only_if]) continue;
    const qty = Math.round(qtyOf(l.qty, facts) * 100) / 100;
    if (!(qty > 0)) continue;
    const from = typeof l.qty === 'string' ? l.qty : l.only_if || (l.qty && l.qty.of);
    lines.push({ item: l.item, unit: l.unit, qty, rate: l.rate, tag: l.tag || null, said: (from && said[from]) || null });
  }
  for (const u of notPriced || []) lines.push({ item: cap1(u.item), unit: 'lot', qty: 1, rate: 0, tag: 'Needs a price', said: u.said || null });
  return lines;
}
function totalsOf(lines) {
  const m = S.pl.markup_percent || 0, t = (S.pl.tax && S.pl.tax.percent) || 0, d = S.pl.deposit_percent || 0;
  const cost = lines.reduce((a, l) => a + l.qty * l.rate, 0);
  const ex = cost * (1 + m / 100), tax = ex * t / 100, inc = ex + tax;
  return { cost, markup: ex - cost, ex, tax, inc, deposit: inc * d / 100 };
}
const sellEach = (l) => l.rate * (1 + (S.pl.markup_percent || 0) / 100);

/* ---------- a site photo, shrunk on this computer to a size models read well ---------- */
async function shrink(file) {
  const bmp = await createImageBitmap(file);
  const k = Math.min(1, 1568 / Math.max(bmp.width, bmp.height));
  const cv = document.createElement('canvas');
  cv.width = Math.round(bmp.width * k); cv.height = Math.round(bmp.height * k);
  cv.getContext('2d').drawImage(bmp, 0, 0, cv.width, cv.height);
  const url = cv.toDataURL('image/jpeg', 0.85);
  return { name: file.name, url, media_type: 'image/jpeg', data: url.split(',')[1] };
}

/* ---------- screen 1: the voice note and the photos ---------- */
function composeScreen() {
  const words = h('textarea', { class: 'words', rows: 6, placeholder: 'Record, upload, or type the job here: what it is, how big, any extras.', 'aria-label': 'The words of the voice note' });
  words.addEventListener('input', () => { S.example = null; ready(); });
  const status = h('p', { class: 'status' });
  const recBtn = h('button', { type: 'button', class: 'btn round', onClick: () => (S.rec ? stopRec() : startRec()) }, 'Record');
  const pickAudio = h('input', { type: 'file', accept: 'audio/*', hidden: true });
  const pickPhotos = h('input', { type: 'file', accept: 'image/*', multiple: true, hidden: true });
  const photos = h('div', { class: 'photos' });
  const build = h('button', { type: 'button', class: 'btn primary wide', disabled: true }, 'Build the quote');
  const ready = () => { build.disabled = !(words.value.trim() || S.audio); };

  async function startRec() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mr = new MediaRecorder(stream), chunks = [], t0 = Date.now();
      mr.ondataavailable = (e) => e.data.size && chunks.push(e.data);
      mr.onstop = () => { stream.getTracks().forEach((t) => t.stop()); S.audio = new Blob(chunks, { type: mr.mimeType || 'audio/webm' }); S.audioSecs = (Date.now() - t0) / 1000; status.textContent = 'Recorded ' + mmss(S.audioSecs) + '. The speech tool Whisper writes it down when you build.'; ready(); };
      const tick = setInterval(() => { if (!S.rec) return clearInterval(tick); status.textContent = 'Recording ' + mmss((Date.now() - t0) / 1000); }, 250);
      mr.start(); S.rec = mr; S.example = null;
      recBtn.textContent = 'Stop'; recBtn.classList.add('live');
    } catch { status.textContent = 'The microphone is blocked. Upload a voice note or type the words instead.'; }
  }
  function stopRec() { S.rec.stop(); S.rec = null; recBtn.textContent = 'Record'; recBtn.classList.remove('live'); }

  pickAudio.addEventListener('change', () => {
    const f = pickAudio.files[0];
    if (!f) return;
    S.audio = f; S.example = null;
    status.textContent = f.name + ', ' + (f.size / 1048576).toFixed(1) + ' MB. The speech tool Whisper writes it down when you build.';
    ready();
  });
  const drawPhotos = () => fill(photos, 
    ...S.photos.map((p, i) => h('div', { class: 'ph' }, h('img', { src: p.url, alt: 'Site photo ' + (i + 1) }),
      h('button', { type: 'button', class: 'ph-x', 'aria-label': 'Remove photo', onClick: () => { S.photos.splice(i, 1); drawPhotos(); } }, '×'))),
    S.photos.length < 6 ? h('button', { type: 'button', class: 'ph-add', onClick: () => pickPhotos.click() }, '+ Add photos') : null);
  pickPhotos.addEventListener('change', async () => {
    for (const f of [...pickPhotos.files].slice(0, 6 - S.photos.length)) { try { S.photos.push(await shrink(f)); } catch { status.textContent = 'That photo could not be read. Use a JPEG or PNG.'; } }
    pickPhotos.value = ''; drawPhotos();
  });
  const useExample = async () => {
    const ex = await getJSON('/api/example');
    S.audio = null; words.value = ex.transcript; S.example = ex;
    status.textContent = S.health.key ? 'Example words in. Your LLM reads them when you build.' : 'Example words in. No LLM is connected yet, so a saved reading of them is used.';
    ready();
  };
  build.addEventListener('click', () => buildQuote(words.value.trim()));
  drawPhotos();
  fill(root, 
    h('h1', null, 'New quote'),
    engineLine(),
    h('h2', null, 'Voice note'),
    h('div', { class: 'row' }, recBtn, h('button', { type: 'button', class: 'btn', onClick: () => pickAudio.click() }, 'Upload'), h('button', { type: 'button', class: 'btn', onClick: useExample }, 'Use the example')),
    status, words, pickAudio,
    h('h2', null, 'Site photos'),
    h('p', { class: 'muted' }, 'Up to six. Photos add notes and questions to check. They never change a size or a price.'),
    photos, pickPhotos,
    h('div', { class: 'bar' }, build));
  sideIntro();
}
function engineLine() {
  const e = S.health, on = e.key && e.whisper;
  const bits = [e.key ? 'LLM connected (' + e.model + ')' : 'No LLM connected yet', e.whisper ? 'Whisper ready' : 'Whisper not set up'];
  return h('p', { class: 'engine ' + (on ? 'on' : 'off') }, h('i'), bits.join(' · '));
}
function sideIntro() {
  fill(side, h('h3', null, 'How it works'),
    h('ol', { class: 'how' },
      h('li', null, 'Talk through the job, upload a voice note, or type it.'),
      h('li', null, 'Add photos of the site if you have them.'),
      h('li', null, 'Whisper writes the voice note down on this computer.'),
      h('li', null, 'Your LLM reads it into a job sheet and quotes your exact words for every fact.'),
      h('li', null, 'Your price list prices it. Nothing is guessed, and nothing goes out until you send it.')));
}

/* ---------- screen 2: the build, one row per step, then the quote ---------- */
async function buildQuote(typed) {
  const list = h('ol', { class: 'steps' });
  fill(root, h('h1', null, 'Building your quote'), list);
  fill(side, h('h3', null, 'What each step found'));
  const R = { text: typed, sheet: null, jobKey: null, facts: null, said: null, lines: null };
  const steps = [];
  if (S.audio) steps.push({ t: 'Voice note written down', tool: 'Whisper, on this computer',
    run: async () => { const r = await getJSON('/api/transcribe', { method: 'POST', body: S.audio, headers: { 'Content-Type': S.audio.type || 'application/octet-stream' } }); R.text = r.text; if (!R.text) throw new Error('Whisper heard no words in the voice note.'); return mmss(r.secs) + ' of voice, ' + R.text.split(/\s+/).length + ' words'; },
    detail: () => h('blockquote', null, R.text) });
  const saved = S.example && !S.health.key && !S.audio && typed === S.example.transcript;
  steps.push({ t: 'Job read from your words' + (S.photos.length ? ' and photos' : ''), tool: saved ? 'A saved reading of the example (no LLM connected yet)' : 'Your LLM',
    run: async () => {
      if (saved) R.sheet = S.example.job;
      else R.sheet = (await getJSON('/api/read', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ transcript: R.text, photos: S.photos.map((p) => ({ media_type: p.media_type, data: p.data })) }) })).job;
      if (!Object.hasOwn(S.pl.jobs, R.sheet.job)) R.sheet.job = 'unclear';
      // every quoted phrase must be in the voice note word for word; any that is missing or not found goes on the confirm list
      const norm = (t) => String(t || '').toLowerCase().replace(/[^a-z0-9.]+/g, ' ').trim();
      const heard = norm(R.text);
      const quotes = [
        ...(R.sheet.facts || []).map((f) => ({ what: labelOf(R.sheet.job, String(f.name).split('.')[1] || '') + ' (' + f.value + ')', said: f.said, must: true })),
        ...(R.sheet.not_priced || []).map((u) => ({ what: u.item, said: u.said, must: true })),
        { what: 'the job type', said: R.sheet.job_said, must: false },
        { what: 'the timing', said: R.sheet.timing_said, must: false },
      ];
      const off = quotes.filter((q) => (q.said ? !heard.includes(norm(q.said)) : q.must));
      if (off.length) R.sheet.to_confirm = [...(R.sheet.to_confirm || []), ...off.map((q) => 'Check ' + q.what + ': the words quoted for it are not in the voice note word for word.')];
      return R.sheet.job === 'unclear' ? 'The job type was not said' : (R.sheet.facts || []).length + ' facts, each tied to your words';
    },
    detail: () => sheetDetail(R.sheet) });
  steps.push({ t: 'Anything missing asked for', waiting: 'Waiting for you', skip: () => R.sheet.job !== 'unclear' && !missingOf(R.sheet.job, factsOf(R.sheet, R.sheet.job).facts).length,
    run: async () => { await askMissing(list, R); return 'Filled in by you'; } });
  steps.push({ t: 'Priced from your price list', tool: 'price-list.json, in code',
    run: async () => {
      R.jobKey = R.jobKey || R.sheet.job;
      if (!R.facts) Object.assign(R, factsOf(R.sheet, R.jobKey));
      R.lines = priceJob(R.jobKey, R.facts, R.said, R.sheet.not_priced);
      return R.lines.length + ' lines, ' + money(totalsOf(R.lines).cost) + ' cost';
    },
    detail: () => priceTable(R.lines) });
  steps.push({ t: 'Quote laid out', tool: 'Markup ' + (S.pl.markup_percent || 0) + '%, ' + ((S.pl.tax && S.pl.tax.label) || 'tax'),
    run: async () => money(totalsOf(R.lines).inc) + ' total', detail: () => totalsDetail(R.lines) });

  for (const st of steps) {
    if (st.skip && st.skip()) continue;
    const icon = h('span', { class: 'si run' }), line = h('span', { class: 'ss' }, st.waiting || 'Working'), secs = h('span', { class: 'st' });
    const li = h('li', { class: 'step' }, icon, h('div', null, h('b', null, st.t), st.tool ? h('span', { class: 'tool' }, st.tool) : null, line), secs);
    list.append(li);
    const t0 = performance.now();
    try { line.textContent = await st.run(); } catch (e) {
      icon.className = 'si bad'; line.textContent = e.message || 'This step did not finish.';
      list.after(h('div', { class: 'bar' }, h('button', { type: 'button', class: 'btn wide', onClick: composeScreen }, 'Back to the voice note')));
      return;
    }
    icon.className = 'si ok'; secs.textContent = ((performance.now() - t0) / 1000).toFixed(1) + ' s';
    const d = st.detail && st.detail();
    if (d) side.append(h('section', { class: 'det' }, h('h4', null, st.t), d));
  }
  quoteScreen(R);
}

/* never a guess: when the job type or a needed fact was not said, the owner fills it in */
function askMissing(list, R) {
  return new Promise((ok, bad) => {
    const box = h('div', { class: 'ask' });
    list.after(box);
    const factsForm = () => {
      const got = factsOf(R.sheet, R.jobKey);
      R.facts = got.facts; R.said = got.said;
      const miss = missingOf(R.jobKey, R.facts);
      if (!miss.length) { box.remove(); return ok(); }
      const inputs = miss.map(([n, d]) => [n, h('input', { type: 'number', step: 'any', min: '0', 'aria-label': d.means })]);
      const go = h('button', { type: 'button', class: 'btn primary' }, 'Price it');
      go.addEventListener('click', () => {
        for (const [n, i] of inputs) { const v = parseFloat(i.value); if (!(v > 0)) { i.focus(); return; } R.facts[n] = v; }
        box.remove(); ok();
      });
      fill(box, h('p', null, 'This was not in the voice note. Fill it in and it gets priced.'),
        ...inputs.map(([n, i]) => h('label', { class: 'field' }, h('span', null, labelOf(R.jobKey, n) + ': ' + S.pl.jobs[R.jobKey].facts[n].means), i)), go);
    };
    if (R.sheet.job === 'unclear') {
      fill(box, h('p', null, 'What is the job? It was not in the voice note.'),
        h('div', { class: 'row wrap' }, Object.entries(S.pl.jobs).map(([k, j]) => h('button', { type: 'button', class: 'btn', onClick: () => { R.jobKey = k; factsForm(); } }, j.label))),
        h('button', { type: 'button', class: 'btn ghost', onClick: () => { box.remove(); bad(new Error('No job type was picked, so nothing was priced.')); } }, 'Cancel'));
    } else { R.jobKey = R.sheet.job; factsForm(); }
  });
}

const factList = (rows) => h('dl', { class: 'facts' }, rows.map(([k, v]) => [h('dt', null, k), h('dd', null, v)]));
function sheetDetail(j) {
  if (j.job === 'unclear') return h('p', null, 'The voice note did not say what the job is.');
  const job = S.pl.jobs[j.job];
  const rows = [['Job', [job.label, j.job_said ? h('q', null, j.job_said) : null]]];
  for (const f of j.facts || []) { const n = f.name.split('.')[1]; if ((job.facts || {})[n]) rows.push([labelOf(j.job, n), [f.value, h('q', null, f.said)]]); }
  if (j.client) rows.push(['Client', j.client]);
  if (j.site) rows.push(['Site', j.site]);
  if (j.timing) rows.push(['Wanted', [j.timing, j.timing_said ? h('q', null, j.timing_said) : null]]);
  for (const u of j.not_priced || []) rows.push([cap1(u.item), ['Not on the price list: needs a price', h('q', null, u.said)]]);
  return h('div', null, factList(rows),
    (j.photo_notes || []).length ? [h('h5', null, 'What the photos show'), h('ul', null, j.photo_notes.map((n) => h('li', null, h('b', null, 'Photo ' + n.photo + ': '), n.shows, n.matters ? ' ' + n.matters : '')))] : null,
    (j.to_confirm || []).length ? [h('h5', null, 'Confirm before it goes'), h('ul', null, j.to_confirm.map((c) => h('li', null, c)))] : null);
}
const priceTable = (lines) => h('table', null, h('tbody', null, lines.map((l) => h('tr', null,
  h('td', null, l.item, l.tag ? h('span', { class: 'tag' }, l.tag) : null), h('td', { class: 'r' }, l.qty + ' ' + l.unit), h('td', { class: 'r' }, money(l.qty * l.rate))))));
function totalsDetail(lines) {
  const t = totalsOf(lines), tx = S.pl.tax || { label: 'Tax', percent: 0 };
  return factList([['Cost', money(t.cost)], ['Markup ' + (S.pl.markup_percent || 0) + '%', money(t.markup)], ['Price ex ' + tx.label, money(t.ex)], [tx.label + ' ' + tx.percent + '%', money(t.tax)], ['Total', h('b', null, money(t.inc))]]);
}

/* ---------- screen 3: the finished quote ---------- */
function quoteScreen(R) {
  const j = R.sheet, job = S.pl.jobs[R.jobKey], t = totalsOf(R.lines), tx = S.pl.tax || { label: 'Tax', percent: 0 };
  const no = 'Q-' + new Date().toISOString().slice(2, 10).replace(/-/g, '') + '-' + (++S.quoteNo);
  const q = { no, job: job.label, who: j.client || 'New client', site: j.site || 'Not said', lines: R.lines, t, confirm: j.to_confirm || [], checks: job.checks || [], details: Object.entries(R.facts).filter(([, v]) => v !== false).map(([n, v]) => [labelOf(R.jobKey, n), shown(v)]), timing: j.timing, photo: S.photos[0] && S.photos[0].url };
  fill(root, 
    h('p', { class: 'kicker' }, 'Quote ' + no + ' · Draft'),
    h('h1', null, q.job),
    h('p', { class: 'muted' }, q.who + ' · ' + q.site + (q.timing ? ' · Wanted ' + q.timing : '')),
    q.photo ? h('img', { class: 'qpic', src: q.photo, alt: 'Site photo' }) : null,
    q.confirm.length ? h('div', { class: 'warn' }, h('b', null, 'Confirm before it goes'), h('ul', null, q.confirm.map((c) => h('li', null, c)))) : null,
    q.details.length ? [h('h2', null, 'Job details'), factList(q.details)] : null,
    h('h2', null, 'What is included'),
    h('div', { class: 'lines' }, q.lines.map((l) => h('div', { class: 'line' },
      h('div', null, l.item, l.tag ? h('span', { class: 'tag' }, l.tag) : null, h('span', { class: 'qty' }, l.qty + ' ' + l.unit), l.said ? h('q', null, l.said) : null),
      h('div', { class: 'amt' }, money(l.qty * sellEach(l)))))),
    h('div', { class: 'lines' },
      h('div', { class: 'line' }, h('div', null, 'Price ex ' + tx.label), h('div', { class: 'amt' }, money(t.ex))),
      h('div', { class: 'line' }, h('div', null, tx.label + ' ' + tx.percent + '%'), h('div', { class: 'amt' }, money(t.tax))),
      h('div', { class: 'line total' }, h('div', null, 'Total'), h('div', { class: 'amt' }, money(t.inc))),
      S.pl.deposit_percent ? h('div', { class: 'line' }, h('div', null, 'Deposit on signing, ' + S.pl.deposit_percent + '%'), h('div', { class: 'amt' }, money(t.deposit))) : null),
    q.checks.length ? [h('h2', null, 'Checks for this job'), h('ul', null, q.checks.map((c) => h('li', null, c)))] : null,
    h('div', { class: 'bar' },
      h('button', { type: 'button', class: 'btn wide', onClick: () => { S.audio = null; S.photos = []; S.example = null; composeScreen(); } }, 'Start again'),
      h('button', { type: 'button', class: 'btn primary wide', onClick: () => printQuote(q) }, 'Save as PDF')));
  side.prepend(h('p', { class: 'end' }, 'Every price comes from your price list. Nothing goes to the client until you send it.'));
}

/* the quote as a clean printable page; the browser's own Save as PDF does the rest */
function printQuote(q) {
  const open = q.lines.filter((l) => l.tag === 'Needs a price').length;
  if (open && !window.confirm(open + (open === 1 ? ' line still needs' : ' lines still need') + ' a price and will print at $0. Print anyway?')) return;
  const b = S.pl.business, tx = S.pl.tax || { label: 'Tax', percent: 0 };
  const today = new Date().toLocaleDateString(S.pl.locale || 'en-AU', { day: 'numeric', month: 'long', year: 'numeric' });
  const rows = q.lines.map((l) => '<tr><td>' + esc(l.item) + (l.tag ? ' (' + esc(l.tag) + ')' : '') + '</td><td class="r">' + esc(l.qty) + ' ' + esc(l.unit) + '</td><td class="r">' + money(sellEach(l)) + '</td><td class="r">' + money(l.qty * sellEach(l)) + '</td></tr>').join('');
  const html = '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Quote ' + esc(q.no) + '</title><style>' +
    '@page{size:A4;margin:18mm}body{font:13px/1.5 Helvetica,Arial,sans-serif;color:#171717;margin:0;padding:28px}' +
    'header{display:flex;justify-content:space-between;border-bottom:2px solid #171717;padding-bottom:14px}h1{font-size:22px;font-weight:600;margin:0}h2{font-size:15px;margin:22px 0 6px}' +
    '.k{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#737373}.meta{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:16px 0}.meta b{display:block;font-size:11px;color:#737373;font-weight:400}' +
    'table{width:100%;border-collapse:collapse}th,td{padding:7px 6px;border-bottom:1px solid #e5e5e5;text-align:left}th{font-size:11px;color:#737373;font-weight:400}.r{text-align:right}' +
    '.tot{margin-left:auto;width:280px;margin-top:10px}.tot div{display:flex;justify-content:space-between;padding:4px 6px}.tot .big{font-size:16px;font-weight:600;border-top:2px solid #171717}' +
    '.pic{display:block;width:100%;height:200px;object-fit:cover;border-radius:6px;margin:10px 0}.sign{display:grid;grid-template-columns:1fr 1fr;gap:40px;margin-top:36px}.sign div{border-top:1px solid #171717;padding-top:4px;font-size:11px;color:#737373}' +
    '@media print{.noprint{display:none}}</style></head><body>' +
    '<p class="noprint" style="background:#171717;color:#fff;padding:10px 14px;border-radius:8px">Choose <b>Save as PDF</b> in the print window.</p>' +
    '<header><div><div class="k">Quote</div><h1>' + esc(b.name) + '</h1><div>' + [b.abn ? 'ABN ' + b.abn : '', b.email, b.phone].filter(Boolean).map(esc).join(' &middot; ') + '</div></div>' +
    '<div style="text-align:right"><div class="k">Quote number</div><h1>' + esc(q.no) + '</h1><div>' + esc(today) + '</div></div></header>' +
    '<div class="meta"><div><b>For</b>' + esc(q.who) + '</div><div><b>Site</b>' + esc(q.site) + '</div><div><b>Job</b>' + esc(q.job) + '</div><div><b>Valid for</b>' + esc(S.pl.valid_days || 30) + ' days</div></div>' +
    (q.photo ? '<img class="pic" src="' + esc(q.photo) + '" alt="Site photo">' : '') +
    (q.details.length ? '<h2>Job details</h2><table><tbody>' + q.details.map(([k, v]) => '<tr><td style="width:30%">' + esc(k) + '</td><td>' + esc(v) + '</td></tr>').join('') + '</tbody></table>' : '') +
    '<h2>What is included</h2><table><thead><tr><th>Item</th><th class="r">Qty</th><th class="r">Each</th><th class="r">Amount</th></tr></thead><tbody>' + rows + '</tbody></table>' +
    '<div class="tot"><div><span>Price ex ' + esc(tx.label) + '</span><span>' + money(q.t.ex) + '</span></div><div><span>' + esc(tx.label) + ' ' + esc(tx.percent) + '%</span><span>' + money(q.t.tax) + '</span></div>' +
    '<div class="big"><span>Total</span><span>' + money(q.t.inc) + '</span></div>' + (S.pl.deposit_percent ? '<div><span>Deposit on signing (' + esc(S.pl.deposit_percent) + '%)</span><span>' + money(q.t.deposit) + '</span></div>' : '') + '</div>' +
    (q.timing ? '<p>Wanted ' + esc(q.timing) + '.</p>' : '') +
    (q.checks.length ? '<h2>Checks for this job</h2><ul>' + q.checks.map((c) => '<li>' + esc(c) + '</li>').join('') + '</ul>' : '') +
    (S.pl.terms ? '<h2>Terms</h2><p>' + esc(S.pl.terms) + '</p>' : '') +
    '<div class="sign"><div>Client signature and date</div><div>For ' + esc(b.name) + '</div></div>' +
    '<script>setTimeout(function(){window.print()},400)<\/script></body></html>';
  const w = window.open('', '_blank');
  if (!w) return;
  w.document.open(); w.document.write(html); w.document.close();
}

/* ---------- start ---------- */
(async () => {
  try {
    [S.pl, S.health] = await Promise.all([getJSON('/api/price-list'), getJSON('/api/health')]);
    document.getElementById('biz').textContent = S.pl.business.name;
    composeScreen();
  } catch (e) { fill(root, h('h1', null, 'The quote app is not running'), h('p', null, e.message)); }
})();
