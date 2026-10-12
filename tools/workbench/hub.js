let token = '';
let signature = '';
const cards = new Map();
const $ = id => document.getElementById(id);
function node(tag, text, cls) {
  const n = document.createElement(tag);
  if (text !== undefined) n.textContent = text;
  if (cls) n.className = cls;
  return n;
}
async function action(path, body) {
  const r = await fetch(path, {method: 'POST', headers: {'Content-Type': 'application/json', 'X-Combine-Token': token}, body: JSON.stringify(body)});
  if (!r.ok) throw new Error('Request refused. Refresh and check the selected scenario.');
  return r.json();
}
async function refresh() {
  try {
    const response = await fetch('/api/state', {cache: 'no-store'});
    if (!response.ok) throw new Error('Private connection unavailable');
    const state = await response.json(); token = state.token;
    $('connection').textContent = 'Connected · refreshed ' + new Date().toLocaleTimeString();
    const c = state.candidate;
    $('title').textContent = c.title; $('question').textContent = c.question;
    $('source-checks').textContent = c.source_checks;
    $('revision').textContent = 'Candidate source: ' + c.source_revision;
    $('next').textContent = c.next_experiment;
    $('issues').replaceChildren(...c.issues.map(number => {const a = node('a', '#' + number + ' '); a.href = 'https://github.com/Jpatching/combine/issues/' + number; a.target = '_blank'; a.rel = 'noreferrer'; return a;}));
    $('criteria').replaceChildren(...c.criteria.map(x => node('li', x.status + ' — ' + x.text)));
    $('blockers').replaceChildren(...c.blockers.map(x => node('li', x)));
    if (!$('scenario').options.length) $('scenario').replaceChildren(...Object.entries(state.scenarios).map(([key, text]) => {const o = node('option', text); o.value = key; return o;}));
    $('batches').replaceChildren(...state.batches.map(b => {
      const row = node('div', undefined, 'batch');
      row.append(node('span', b.scenario + ' · ' + b.status + ' · ' + b.completed + '/' + b.requested + (b.reason ? ' · ' + b.reason : '')));
      if (['pending', 'running'].includes(b.status)) {const button = node('button', 'Stop'); button.type = 'button'; button.onclick = async () => {try {await action('/api/stop', {id:b.id}); await refresh();} catch (e) {$('feedback').textContent=e.message;}}; row.append(button);}
      return row;
    }));
    const changed = JSON.stringify(state.attempts);
    if (changed !== signature) {
      signature = changed; $('count').textContent = state.attempts.length + ' recorded';
      $('evidence').replaceChildren(...state.attempts.map(a => {
        if (cards.has(a.id)) return cards.get(a.id);
        const card = node('article', undefined, 'attempt');
        const title = node('h3', a.scenario); title.prepend(node('span', a.verdict, 'badge ' + a.verdict)); card.append(title);
        const details = node('dl');
        for (const [label, value] of [['Boundary',a.boundary],['Observation',a.reason],['Changed variable',a.changed_variable],['Cleanup',a.cleanup],['Tested source',a.source_revision],['Controller source',a.controller_revision],['Runtime identity',a.runtime_identity],['Recorded',a.recorded_at],['Limitations',a.limitations]]) {details.append(node('dt',label), node('dd',value || 'Unknown'));}
        card.append(details);
        for (const m of a.media) {const item = node(/\.(mp4|webm)$/i.test(m.name) ? 'video' : 'img'); item.src = '/media/' + m.id; item.controls = true; item.preload = 'metadata'; item.alt = 'Evidence for ' + a.scenario; card.append(item);}
        cards.set(a.id, card); return card;
      }));
      if (!state.attempts.length) $('evidence').append(node('p','No attempts recorded yet.'));
    }
  } catch (e) {$('connection').textContent = 'Disconnected — retained evidence will return on reconnect.';}
}
$('request').addEventListener('submit', async event => {
  event.preventDefault(); const button = event.submitter; button.disabled = true;
  const retained = localStorage.getItem('combine-pending-request');
  const body = retained ? JSON.parse(retained) : {id: crypto.randomUUID(), scenario: $('scenario').value, attempts: Number($('attempts').value)};
  localStorage.setItem('combine-pending-request',JSON.stringify(body));
  try {await action('/api/requests',body); localStorage.removeItem('combine-pending-request'); $('feedback').textContent = 'Request saved. The guarded runner will report progress here.'; await refresh();}
  catch (e) {$('feedback').textContent = e.message + ' Retry will use the saved request identity.';}
  finally {button.disabled = false; button.textContent = localStorage.getItem('combine-pending-request') ? 'Retry saved request' : 'Request tests';}
});
async function reconnect() {await refresh(); const saved = localStorage.getItem('combine-pending-request'); if(saved && token){try {await action('/api/requests',JSON.parse(saved)); localStorage.removeItem('combine-pending-request'); await refresh();} catch {}}}
reconnect(); setInterval(refresh,5000);
