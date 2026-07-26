/* o documento não espera o toque: a hora corre, o quadro respira e o GitHub reporta sozinho */

const MESES = ['jan.','fev.','mar.','abr.','maio','jun.','jul.','ago.','set.','out.','nov.','dez.'];
const parado = matchMedia('(prefers-reduced-motion: reduce)').matches;

const dataABNT = d => d.getDate() + ' ' + MESES[d.getMonth()] + ' ' + d.getFullYear();
const hora = d => String(d.getHours()).padStart(2, '0') + ':' + String(d.getMinutes()).padStart(2, '0');

/* 1. data de acesso das referências e relógio da sessão */

const marcarHora = () => {
  const agora = new Date();
  document.querySelectorAll('.acesso').forEach(el => el.textContent = dataABNT(agora));
  const rel = document.getElementById('agora');
  if (rel) rel.textContent = dataABNT(agora) + ', ' + hora(agora);
};

marcarHora();
setInterval(marcarHora, 20000);

/* 2. quadro que respira: uma linha acende de cada vez, sem ninguém tocar */

const linhas = [...document.querySelectorAll('.linha[href]')];

if (linhas.length && !parado) {
  const visiveis = new Set();
  const io = new IntersectionObserver(es => {
    for (const e of es) e.isIntersecting ? visiveis.add(e.target) : visiveis.delete(e.target);
  }, { threshold: .6 });
  linhas.forEach(l => io.observe(l));

  let i = 0, pausaAte = 0, aceso = null;

  const apagar = () => { if (aceso) { aceso.classList.remove('viva'); aceso = null; } };

  const bater = () => {
    apagar();
    if (document.hidden || Date.now() < pausaAte) return;
    const fila = linhas.filter(l => visiveis.has(l));
    if (!fila.length) return;
    aceso = fila[i++ % fila.length];
    aceso.classList.add('viva');
    setTimeout(() => { if (aceso) aceso.classList.remove('viva'); }, 1500);
  };

  /* quem interage manda: o ciclo se cala por 12 segundos */
  const calar = () => { pausaAte = Date.now() + 12000; apagar(); };
  addEventListener('pointerdown', calar, { passive: true });
  addEventListener('pointermove', calar, { passive: true });
  addEventListener('keydown', calar);
  document.addEventListener('visibilitychange', apagar);

  setTimeout(() => { bater(); setInterval(bater, 3400); }, 2200);
}

/* 3. correr de leitura: mostra em que seção o leitor está */

const aqui = document.querySelector('.correr .aqui');
const secoes = [...document.querySelectorAll('section[data-titulo]')];

if (aqui && secoes.length) {
  const io = new IntersectionObserver(es => {
    for (const e of es) if (e.isIntersecting) aqui.textContent = e.target.dataset.titulo;
  }, { rootMargin: '-25% 0px -60% 0px' });
  secoes.forEach(s => io.observe(s));
}

/* 4. citação, referência e linha do quadro acendem juntas */

const grupo = alvo => {
  const ref = document.getElementById(alvo);
  if (!ref) return [];
  const lin = ref.dataset.linha ? document.getElementById(ref.dataset.linha) : null;
  const cits = [...document.querySelectorAll('.cit[href="#' + alvo + '"]')];
  return [ref, lin, ...cits].filter(Boolean);
};

const ligar = (el, alvo) => {
  const acende = () => grupo(alvo).forEach(x => x.classList.add('viva'));
  const apaga  = () => grupo(alvo).forEach(x => x.classList.remove('viva'));
  el.addEventListener('pointerenter', acende);
  el.addEventListener('pointerleave', apaga);
  el.addEventListener('focus', acende);
  el.addEventListener('blur', apaga);
  return { acende, apaga };
};

document.querySelectorAll('.cit').forEach(c => {
  const alvo = c.getAttribute('href').slice(1);
  const { acende, apaga } = ligar(c, alvo);
  c.addEventListener('click', () => { acende(); setTimeout(apaga, 3200); });
});

document.querySelectorAll('.ref').forEach(r => ligar(r, r.id));
document.querySelectorAll('.ref[data-linha]').forEach(r => {
  const lin = document.getElementById(r.dataset.linha);
  if (lin) ligar(lin, r.id);
});

/* 5. pulso: última atividade pública no GitHub, buscada e reescrita sozinha */

const pulso = document.getElementById('pulso');

if (pulso) {
  const VERBO = {
    PushEvent: 'push', PullRequestEvent: 'pull request', CreateEvent: 'branch nova',
    ReleaseEvent: 'release', IssuesEvent: 'issue', IssueCommentEvent: 'comentário',
    ForkEvent: 'fork', WatchEvent: 'star', DeleteEvent: 'remoção de branch'
  };

  const desde = ms => {
    const s = Math.max(0, Math.round(ms / 1000));
    if (s < 90) return 'agora há pouco';
    const min = Math.round(s / 60);
    if (min < 60) return 'há ' + min + ' min';
    const h = Math.round(min / 60);
    if (h < 24) return 'há ' + h + (h === 1 ? ' hora' : ' horas');
    const d = Math.round(h / 24);
    if (d < 30) return 'há ' + d + (d === 1 ? ' dia' : ' dias');
    const m = Math.round(d / 30);
    return 'há ' + m + (m === 1 ? ' mês' : ' meses');
  };

  let ultimo = null;

  const escrever = () => {
    if (!ultimo) return;
    const verbo = VERBO[ultimo.tipo] || 'atividade';
    const link = document.createElement('a');
    link.href = 'https://github.com/' + ultimo.repo;
    link.textContent = ultimo.repo;
    pulso.textContent = verbo + ' em ';
    pulso.append(link, ', ' + desde(Date.now() - ultimo.quando));
  };

  const buscar = async () => {
    if (document.hidden) return;
    try {
      const r = await fetch('https://api.github.com/users/joshazze/events/public?per_page=10');
      if (!r.ok) return;
      const e = (await r.json())[0];
      if (!e) return;
      ultimo = { tipo: e.type, repo: e.repo.name, quando: Date.parse(e.created_at) };
      escrever();
    } catch (_) { /* sem rede: a linha fica com o texto que já veio no HTML */ }
  };

  buscar();
  setInterval(buscar, 120000);
  setInterval(escrever, 30000);
}

/* contagem de repositórios públicos: vem da fonte, não de um número digitado à mão */

const nrepos = document.getElementById('nrepos');

if (nrepos) {
  fetch('https://api.github.com/users/joshazze')
    .then(r => r.ok ? r.json() : null)
    .then(d => { if (d && d.public_repos) nrepos.textContent = d.public_repos; })
    .catch(() => {});
}

/* 6. o documento entrega a própria referência */

const copiar = async (botao, texto, rotulo) => {
  try {
    await navigator.clipboard.writeText(texto);
  } catch (_) {
    const cx = document.createElement('textarea');
    cx.value = texto;
    cx.style.position = 'fixed';
    cx.style.opacity = '0';
    document.body.appendChild(cx);
    cx.select();
    document.execCommand('copy');
    cx.remove();
  }
  botao.textContent = 'copiado';
  setTimeout(() => botao.textContent = rotulo, 2200);
};

const abnt = document.getElementById('copiar-abnt');
const bib = document.getElementById('copiar-bib');

if (abnt) abnt.addEventListener('click', () => copiar(abnt,
  'DISTEL, J. A. Registro profissional e acadêmico de J. A. Distel. [S. l.], 2026. '
  + 'Disponível em: https://jadistel.com. Acesso em: ' + dataABNT(new Date()) + '.',
  'copiar citação ABNT'));

if (bib) bib.addEventListener('click', () => copiar(bib,
  '@misc{distel2026,\n'
  + '  author       = {Distel, J. A.},\n'
  + '  title        = {Registro profissional e acadêmico de J. A. Distel},\n'
  + '  year         = {2026},\n'
  + '  howpublished = {\\url{https://jadistel.com}},\n'
  + '  urldate      = {' + new Date().toISOString().slice(0, 10) + '}\n'
  + '}',
  'copiar BibTeX'));
