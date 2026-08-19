---
slug: artigo-ic
titulo: Viés linguístico em material didático gerado por LLM
sub: Iniciação científica, coautoria com o Prof. Osmar Ventura Gomes
data: 2026-08-18
stack: [Python, pandas, ANOVA, Ollama, embeddings]
competencias: [pesquisa, estatística, desenho experimental, escrita científica]
---

## Contexto

A literatura brasileira de IA em educação tem um formato quase único: pegar um modelo, aplicar uma prova, reportar que ele acertou 73% das questões. É útil e é raso. Quase ninguém cruza duas coisas que interessam a quem dá aula em português: o viés linguístico do texto gerado, e a arquitetura do prompt como variável que se pode escolher.

Era o buraco que eu queria ocupar. A orientação é do Prof. Osmar Ventura Gomes, que é da área de algoritmos, não de IA aplicada nem de estatística, então o protocolo foi escrito para ser auditável por quem não convive com LLM: glossário curto e justificativa explícita de cada decisão metodológica. Uma exigência dele mudou o texto inteiro logo no começo. Onde eu escrevia "pedagógico", passou a ser "didático", porque no ensino superior brasileiro a distinção entre prática docente e formação do educador não é sinônimo.

## O que eu fiz

Um fatorial de três vias. Arquitetura em quatro níveis (one-shot, few-shot, RAG sobre o material da própria disciplina, agente com memória persistente), modelo, e disciplina em três perfis epistêmicos distintos: programação orientada a objetos, estatística e ciência de dados. Cada célula replicada, 192 amostras de material didático geradas e medidas.

Seis variáveis resposta, três automáticas e três humanas. As automáticas: percentual de inglês não traduzido por dicionário técnico, distância léxica contra um corpus de PT-BR técnico via embeddings, e inversão de notação anglo-saxã, aquele ponto que vira separador decimal no meio de uma tabela em português. As humanas eram rubricas de 0 a 5 para neutralidade cultural, cobertura curricular e alucinação factual, com um subconjunto anotado em duplo para calcular concordância.

Sobre isso rodou ANOVA fatorial com correção de Bonferroni. A versão 1.0 foi entregue em 30 de maio de 2026, com um achado que me pareceu bonito: viés lexical e viés cultural apareciam como dimensões dissociadas, correlação perto de zero.

## O que aprendi

Em 12 de agosto eu auditei o próprio artigo antes de submeter. Achei oito fragilidades. Três eram graves o bastante para matar o texto.

A primeira: uma das referências não existia. Estava formatada, plausível, no lugar certo do argumento, e não correspondia a nenhum trabalho real. A segunda: o pipeline não era reprodutível em 84 das 192 amostras, porque o índice das combinações era derivado de hash e não sobrevivia a uma re-execução. A terceira era a mais desconfortável, porque não era erro de código, era erro meu de leitura estatística: eu escrevi que "o RAG zerou as inversões de notação" apoiado num p de 0,0704. Isso não rejeita nada. E o achado central da v1.0, as duas dimensões dissociadas, tinha o mesmo defeito de fundo: não rejeitar a hipótese nula não é prova de independência, é ausência de evidência. Eu tinha transformado um teste que não deu em uma descoberta.

Junto veio o resultado que eu mais queria que fosse verdade e não era. O painel de juízes-LLM que eu montei para pontuar neutralidade cultural teve concordância intraclasse perto de zero. Cinco modelos julgando o mesmo texto não concordavam entre si mais do que sorteio. Um juiz automático que ninguém mediu é um gerador de números, não um instrumento.

Cortei o artigo. Não revisei, cortei.

## Resultados

- A v2 sustenta um achado só, e sustenta de verdade: **modelos de raciocínio anglicizam mais o português técnico**. Entre 16 modelos avaliados, os três com maior taxa de anglicismo são de raciocínio, com p = 0,00179 no nível do modelo, que é o mínimo que o desenho permite afirmar.
- Reprodutibilidade fechada: índice de combinação determinístico, e uma re-execução completa devolve os mesmos números nas 192 amostras.
- Alvo de submissão: CTIC 2027, no template da SBC.
- Toda referência do texto novo foi conferida na fonte, uma a uma, antes de entrar.
