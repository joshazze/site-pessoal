/* oqojfr? — os mostradores não esperam ninguém tocar.
   present time corre sozinho, destination percorre o arquivo em ciclo.
   quem interage manda: o primeiro toque cala o ciclo por 12 segundos. */

const MES = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN',
             'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ'];

const parado = matchMedia('(prefers-reduced-motion: reduce)').matches;
const dd = n => String(n).padStart(2, '0');

/* ---------- mostradores ---------- */

const acesos = circuito => circuito ? [...circuito.querySelectorAll('.led .on')] : [];

/* [mês, dia, ano, hora, min]. valor vazio deixa a célula escura, que é o certo
   quando o dado não existe: post tem data, não tem hora. */
const pintar = (circuito, valores) => {
  const celulas = acesos(circuito);
  celulas.forEach((cel, i) => {
    const novo = valores[i] || '';
    if (cel.textContent !== novo) cel.textContent = novo;
  });
};

const daData = iso => {
  /* meia-noite local, não UTC: new Date('2026-08-15') volta um dia no Brasil */
  const [a, m, d] = iso.split('-').map(Number);
  return [MES[m - 1], dd(d), String(a), '', ''];
};

/* ---------- present time: o único que conta sozinho ---------- */

const presente = document.getElementById('c-presente');

if (presente) {
  const bater = () => {
    const a = new Date();
    pintar(presente, [MES[a.getMonth()], dd(a.getDate()), String(a.getFullYear()),
                      dd(a.getHours()), dd(a.getMinutes())]);
  };
  bater();
  setInterval(bater, 1000);
}

/* ---------- destination e last time departed percorrem o arquivo ---------- */

const destino = document.getElementById('c-destino');
const partida = document.getElementById('c-partida');
const topicos = [...document.querySelectorAll('.topico[data-data]')];

if (destino && partida && topicos.length) {
  const datas = topicos.map(t => t.dataset.data);

  /* a lista desce do mais novo pro mais velho: 'de onde vim' é o item seguinte */
  const mostrar = i => {
    pintar(destino, daData(datas[i]));
    pintar(partida, i + 1 < datas.length ? daData(datas[i + 1]) : ['', '', '', '', '']);
  };

  const visiveis = new Set();
  const io = new IntersectionObserver(entradas => {
    for (const e of entradas) e.isIntersecting ? visiveis.add(e.target) : visiveis.delete(e.target);
  }, { threshold: .55 });
  topicos.forEach(t => io.observe(t));

  let i = 0, pausaAte = 0, aceso = null;

  const apagar = () => {
    if (!aceso) return;
    const t = aceso;
    aceso = null;
    t.classList.remove('viva');
    t.classList.add('saindo');
    setTimeout(() => t.classList.remove('saindo'), 620);
  };

  const bater = () => {
    apagar();
    if (document.hidden || Date.now() < pausaAte) return;
    const fila = topicos.filter(t => visiveis.has(t));
    if (!fila.length) return;
    aceso = fila[i++ % fila.length];
    aceso.classList.add('viva');
    mostrar(topicos.indexOf(aceso));
    setTimeout(apagar, 1700);
  };

  /* quem interage manda */
  const calar = () => { pausaAte = Date.now() + 12000; apagar(); };
  addEventListener('pointerdown', calar, { passive: true });
  addEventListener('keydown', calar);
  document.addEventListener('visibilitychange', apagar);

  /* apontar para um tópico é escolher o destino */
  topicos.forEach((t, n) => {
    const mirar = () => { calar(); mostrar(n); };
    t.addEventListener('pointerenter', mirar);
    t.addEventListener('focus', mirar);
  });

  if (!parado) setTimeout(() => { bater(); setInterval(bater, 3400); }, 1800);
}
