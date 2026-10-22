---
slug: artigo-ic
titulo: Viés linguístico em material didático gerado por LLM
sub: Iniciação científica, coautoria com o Prof. Osmar Ventura Gomes
data: 2026-08-18
stack: [Python, pandas, ANOVA, Ollama, embeddings]
competencias: [pesquisa, estatística, desenho experimental, escrita científica]
areas: [IA aplicada, Dados e estatística, Pesquisa]
---

## Contexto

Boa parte da pesquisa brasileira sobre IA na educação segue um formato parecido: escolhe-se um modelo, aplica-se uma prova e reporta-se a taxa de acerto. É útil, mas deixa de lado duas perguntas que importam para quem dá aula em português. Qual é o viés linguístico do texto gerado? E quanto a arquitetura do prompt, que é uma escolha de quem usa, interfere nesse viés?

Esse foi o espaço que eu quis estudar. A orientação é do Prof. Osmar Ventura Gomes, que vem da área de algoritmos e não de IA aplicada ou estatística, então escrevi o protocolo para ser auditável por alguém de fora: glossário curto e justificativa explícita para cada decisão de método. Uma observação dele mudou o texto logo no começo. Onde eu escrevia "pedagógico", passei a escrever "didático", porque no ensino superior brasileiro os dois termos tratam de coisas diferentes (a prática docente e a formação do educador).

## O que eu fiz

Um experimento fatorial de três vias. A arquitetura tinha quatro níveis (one-shot, few-shot, RAG sobre o material da própria disciplina e agente com memória persistente), o segundo fator era o modelo, e o terceiro, a disciplina, em três perfis epistêmicos: programação orientada a objetos, estatística e ciência de dados. Com as réplicas, foram 192 amostras de material didático geradas e medidas.

As variáveis resposta eram seis. Três automáticas: percentual de inglês não traduzido, medido por dicionário técnico; distância léxica até um corpus de PT-BR técnico, por embeddings; e inversão de notação, como o ponto que aparece como separador decimal numa tabela em português. As outras três eram rubricas humanas de 0 a 5 para neutralidade cultural, cobertura curricular e alucinação factual, com parte das amostras anotada duas vezes para medir concordância.

Sobre isso rodei ANOVA fatorial com correção de Bonferroni. A versão 1.0 saiu em 30 de maio de 2026 com um achado que me agradou: viés lexical e viés cultural pareciam dimensões independentes, com correlação perto de zero.

## O que aprendi

Em 12 de agosto, antes de submeter, auditei o artigo inteiro. Encontrei oito fragilidades, e três delas eram graves.

Uma das referências não existia. Estava bem formatada e encaixada no argumento, mas não correspondia a nenhum trabalho real. O pipeline também não era reprodutível em 84 das 192 amostras, porque o índice das combinações vinha de um hash que mudava a cada execução. A terceira foi um erro de leitura estatística, e não de código. Eu tinha escrito que "o RAG zerou as inversões de notação" com base num p de 0,0704, que não rejeita a hipótese nula. O achado central da v1.0 tinha o mesmo problema: não rejeitar a nula indica ausência de evidência, e eu tinha tratado isso como prova de independência.

Houve ainda um resultado que eu gostaria que tivesse dado certo. O painel de juízes LLM montado para pontuar neutralidade cultural teve concordância intraclasse perto de zero, ou seja, cinco modelos avaliando o mesmo texto concordavam entre si tanto quanto um sorteio. Sem medir a confiabilidade do juiz, a nota que ele dá não serve como medida.

Diante disso, reduzi o artigo ao que os dados de fato sustentavam.

## Resultados

- A v2 defende um único achado, com a sustentação necessária: **modelos de raciocínio anglicizam mais o português técnico**. Entre 16 modelos avaliados, os três com maior taxa de anglicismo são de raciocínio, com p = 0,00179 no nível do modelo, que é o que o desenho permite afirmar.
- Reprodutibilidade resolvida: o índice de combinação passou a ser determinístico, e uma nova execução completa devolve os mesmos números nas 192 amostras.
- Submissão prevista para o CTIC 2027, no template da SBC.
- Todas as referências do texto novo foram conferidas na fonte, uma a uma.
