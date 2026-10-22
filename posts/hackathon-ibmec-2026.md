---
slug: hackathon-ibmec-2026
titulo: Anatomia de três choques
sub: Hackathon Nacional Ibmec 2026, equipe Os Terríveis, etapa Belo Horizonte
data: 2026-05-22
stack: [Python, statsmodels, Prophet, scikit-learn, VAR, weasyprint]
competencias: [econometria, análise de dados, pitch, trabalho em equipe]
areas: [Dados e estatística, Competições e prêmios, Pesquisa]
---

## Contexto

O manual do desafio pedia algo específico: o Brasil de 2014 a 2024, três choques (a recessão de 2015 e 2016, a COVID em 2020 e a alta da inflação em 2021 e 2022), quatro perguntas obrigatórias e a relação entre a macroeconomia e o balanço das empresas, com o varejo como setor recomendado.

Chegamos com uma tese pronta antes de ler o manual com atenção: um painel comparando S&P e Ibovespa, com IA como quinto fator de precificação. Era ambiciosa. Não respondia ao pedido. Quando lemos o manual com o cronômetro já correndo, deixamos de lado as mil e trezentas linhas de briefing escritas sobre ela. Tínhamos um dia de trabalho, das nove às dezoito, com o pitch para a banca regional às dezessete.

## O que eu fiz

A tese entregue cabe numa frase: três choques, um transmissor, e a transmissão é defasada.

O transmissor é o câmbio.

A regressão de Okun contemporânea, que relaciona produto e desemprego, explica pouco no Brasil do período, com R² de 0,16, e isso poderia ser lido como falha do modelo. Para nós ele media no momento errado. O choque cambial leva de dois a quatro trimestres para chegar ao emprego e passa antes pelo balanço das empresas. Um VAR com doze defasagens capta o que a regressão contemporânea perde. O câmbio antecipa o desemprego com p = 0,0001 e a inflação com p = 0,005, e a decomposição da variância mostra a série 92,5% exógena. O teste de Chow não rejeita a estabilidade estrutural, então não há uma quebra em 2014 explicando o resultado.

![Decomposição da variância do VAR](/img/hackathon/var_fevd.png)

*Decomposição da variância em 12 meses: o câmbio se explica quase só por choques nele mesmo.*

A parte micro usou 129 empresas listadas na B3, com demonstrações da CVM Dados Abertos. O câmbio não empobrece o país por igual. Redistribui. O ROE do varejo cai de 7,4% para 0,9%, enquanto o agroexportador ganha 18,9 pontos percentuais. Sobre esses dados rodamos K-Means para separar três regimes, validado por silhueta, e Prophet para prever 2024, com erro percentual médio de 8,9% no câmbio.

![Resiliência por setor da B3](/img/hackathon/mapa_transmissao_setorial.png)

*Quem resiste e quem sofre nos três choques, por setor da B3.*

![Três regimes econômicos do K-Means](/img/hackathon/kmeans_clusters_timeline.png)

*Os três regimes que o K-Means separou sem rótulo humano.*

![Previsão do câmbio para 2024](/img/hackathon/q2_prophet_cambio_nominal_brl_usd.png)

*Previsão do câmbio para 2024 com Prophet, contra o valor real.*

## O que aprendi

O primeiro R² não foi 0,16. Foi 0,67, com o câmbio dominando tudo, e por uns quarenta minutos achei que tínhamos um resultado forte.

Não era. A série de PIB que eu tinha baixado era um número-índice de nível, e não de variação. Uma série não estacionária que cresce com o tempo funciona, dentro de uma regressão, como uma tendência disfarçada, e o modelo se ajusta a qualquer outra série que também cresça. É a regressão espúria descrita no primeiro capítulo dos livros de séries temporais, e caí nela por não verificar a variável antes de usá-la. Troquei pela variação percentual do PIB da tabela 5932 do SIDRA, rodei o teste ADF em todas as séries e o R² caiu para 0,16.

O resultado verdadeiro era mais fraco e mais interessante.

A segunda lição veio de um mentor, umas três horas antes do pitch, e apontou dois problemas. O PDF terminava em "Limitações", sem fechamento: dezoito páginas de análise e nenhuma frase dizendo o que aquilo significava para o leitor. E o pitch estava técnico demais para uma banca de não especialistas. Reescrevi a apresentação em torno de uma loja de roupas e de um produtor de soja, e os termos técnicos foram para o cartão de perguntas e respostas, usados só quando alguém pedisse. Encurtei a explicação do problema, que era igual para todos os grupos, e dei mais tempo ao que só o nosso trabalho tinha.

## Resultados

- Entrega de 18 páginas, mais pitch e roteiro, aprovada pela banca regional da etapa Belo Horizonte.
- Cadeia da macro à micro sustentada por números: câmbio antecipando o desemprego (p = 0,0001) e ROE do varejo caindo de 7,4% para 0,9% no mesmo período.
- 129 empresas da B3 processadas a partir da CVM Dados Abertos. Tínhamos acesso a um terminal financeiro pago e não foi preciso usá-lo: dados públicos resolveram e deixaram a análise reproduzível por qualquer banca.
- Limitação declarada no texto: o câmbio real efetivo do Banco Central estava fora do ar, então usamos o nominal deflacionado pelo IPCA.
- Gráficos produzidos pela equipe Os Terríveis para a entrega.
