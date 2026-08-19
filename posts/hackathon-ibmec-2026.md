---
slug: hackathon-ibmec-2026
titulo: Anatomia de três choques
sub: Hackathon Nacional Ibmec 2026, equipe Os Terríveis, etapa Belo Horizonte
data: 2026-05-22
stack: [Python, statsmodels, Prophet, scikit-learn, VAR, weasyprint]
competencias: [econometria, análise de dados, pitch, trabalho em equipe]
---

## Contexto

O manual do desafio pedia uma coisa específica: o Brasil de 2014 a 2024, três choques (a recessão de 2015 e 2016, a COVID em 2020, a espiral inflacionária de 2021 e 2022), quatro perguntas obrigatórias, e a correlação entre o macro e o balanço das empresas, com o varejo como setor recomendado.

Nós tínhamos uma tese pronta antes de ler o manual. Painel comparando S&P e Ibovespa, IA como quinto fator de precificação. Bonita, ambiciosa e completamente fora do que foi pedido. Quando o manual finalmente foi lido, com o cronômetro já correndo, jogamos fora as mil e trezentas linhas de briefing que tínhamos escrito em cima dela. Um dia principal, das nove às dezoito, e o pitch às dezessete para a banca regional.

## O que eu fiz

A tese que entregamos tem uma frase: três choques, um transmissor, e a transmissão é defasada. O transmissor é o câmbio.

A regressão de Okun contemporânea, aquela que liga produto e desemprego, explica pouco no Brasil do período. R² de 0,16. A leitura preguiçosa disso é que o modelo falhou. A leitura que sustentamos é que ele está medindo no instante errado: o choque cambial leva de dois a quatro trimestres para chegar ao emprego, e nesse caminho ele passa primeiro pelo balanço das empresas. Um VAR com doze defasagens captura o que a regressão contemporânea perde. O câmbio antecipa desemprego com p = 0,0001 e inflação com p = 0,005, e a decomposição da variância mostra a série 92,5% exógena. O teste de Chow não rejeita estabilidade estrutural, então não há quebra em 2014 servindo de muleta.

A parte micro veio de 129 empresas listadas na B3, com demonstrações da CVM Dados Abertos. O câmbio não empobrece o país de modo uniforme, ele redistribui: o ROE do varejo cai de 7,4% para 0,9%, praticamente zerando, enquanto o agroexportador ganha 18,9 pontos percentuais. Sobre isso rodaram K-Means para separar três regimes, validado por silhueta, e Prophet para a predição de 2024, com erro percentual médio de 8,9% no câmbio.

## O que aprendi

O R² inicial não era 0,16. Era 0,67, e o câmbio aparecia dominando tudo com uma força que me deixou eufórico por uns quarenta minutos.

Era mentira. A série de PIB que eu tinha puxado era número-índice de nível, não variação. Uma série não estacionária que sobe ao longo do tempo, colocada dentro de uma regressão, funciona como tendência temporal disfarçada, e o modelo casa qualquer outra série que também suba com o tempo. Regressão espúria clássica, a coisa que aparece no primeiro capítulo de qualquer livro de séries temporais, e que eu produzi ao vivo por não ter olhado o que a variável era antes de usá-la. Troquei pela variação percentual do PIB da tabela 5932 do SIDRA, rodei ADF em tudo, e o R² desabou para 0,16.

O achado verdadeiro era mais fraco e mais interessante que o falso.

A segunda lição veio de um mentor, umas três horas antes do pitch, e foram dois furos. O PDF acabava em "Limitações", sem fechamento: dezoito páginas de rigor e nenhuma frase que dissesse o que aquilo significa para quem lê. E o pitch estava técnico demais para jurado leigo. Reescrevi a fala inteira em cima de uma loja de roupas e um produtor de soja, e o jargão migrou todo para o cartão de perguntas e respostas, onde ele defende sob demanda em vez de atrapalhar. Comprimi ao mínimo a parte do problema, que era igual para todos os grupos, e alonguei o diferencial. Tempo de pitch é do que só você tem.

## Resultados

- Entrega de 18 páginas mais pitch e roteiro, aprovada na banca regional da etapa Belo Horizonte.
- Cadeia macro para micro fechada com número: câmbio antecipando desemprego (p = 0,0001) e o ROE do varejo caindo de 7,4% para 0,9% no mesmo período.
- 129 empresas da B3 processadas a partir da CVM Dados Abertos. Nós tínhamos acesso a um terminal financeiro pago e não precisamos dele: dado público e auditável resolveu, e ainda deixou a análise reproduzível por qualquer banca.
- Limitação declarada no próprio texto: o câmbio real efetivo do Banco Central estava fora do ar, então usamos o nominal deflacionado pelo IPCA.
