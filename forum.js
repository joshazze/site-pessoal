/* filtro e busca do índice. o único JavaScript do fórum, e ele é opcional:
   sem script a barra fica escondida e a tabela aparece inteira, que é o
   comportamento correto de um fórum estático. */

const controles = document.getElementById('controles');
const tabela = document.getElementById('tabela');
const contagem = document.getElementById('contagem');

if (controles && tabela && contagem) {
  const filtro = document.getElementById('filtro');
  const busca = document.getElementById('busca');
  const corpo = tabela.tBodies[0];
  const linhas = [...corpo.rows];
  const total = linhas.length;

  /* a zebra é nth-child no CSS, e nth-child conta linha escondida. com o script
     ligado quem pinta é a classe, senão filtrar deixa duas linhas claras juntas */
  tabela.classList.add('js');
  controles.hidden = false;

  const vazio = corpo.insertRow();
  vazio.className = 'nada';
  vazio.hidden = true;
  const celula = vazio.insertCell();
  celula.colSpan = 3;
  celula.textContent = 'Nenhum tópico encontrado.';

  const semAcento = t => t.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');

  const aplicar = () => {
    const termo = semAcento(busca.value.trim());
    const tag = filtro.value;
    let vistas = 0;

    for (const linha of linhas) {
      const casaTag = !tag || linha.dataset.tags.split('|').includes(tag);
      const casaTermo = !termo || linha.dataset.busca.includes(termo);
      const mostra = casaTag && casaTermo;
      linha.hidden = !mostra;
      if (mostra) {
        linha.classList.toggle('par', vistas % 2 === 1);
        vistas++;
      }
    }

    vazio.hidden = vistas > 0;
    contagem.textContent = vistas === total
      ? `${total} tópico${total === 1 ? '' : 's'} no total`
      : `${vistas} de ${total} tópicos`;

    /* o endereço acompanha, então o resultado é compartilhável e o voltar funciona */
    const url = new URL(location.href);
    termo ? url.searchParams.set('q', busca.value.trim()) : url.searchParams.delete('q');
    tag ? url.searchParams.set('tag', tag) : url.searchParams.delete('tag');
    history.replaceState(null, '', url.pathname + url.search);
  };

  /* estado inicial vem do endereço: link de busca abre já filtrado */
  const inicial = new URLSearchParams(location.search);
  busca.value = inicial.get('q') || '';
  const tagInicial = inicial.get('tag');
  if (tagInicial && [...filtro.options].some(o => o.value === tagInicial)) filtro.value = tagInicial;

  filtro.addEventListener('change', aplicar);
  busca.addEventListener('input', aplicar);

  /* o Ir não é enfeite: aplica e tira o teclado da frente no celular */
  controles.addEventListener('submit', e => {
    e.preventDefault();
    aplicar();
    busca.blur();
  });

  aplicar();
}
