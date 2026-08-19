---
slug: ibsala
titulo: ibsala
sub: Reserva e consulta de salas do Ibmec BH, no ar para os alunos
data: 2026-08-15
stack: [Flask, Docker, PostgreSQL, Supabase, Web Push, Cloudflare Pages]
competencias: [backend, PWA, banco de dados, segurança, deploy, produto]
link: https://ibsala.com.br
---

## Contexto

O Ibmec BH publica a ocupação das salas numa planilha que a coordenação atualiza durante o dia. Ela é correta e é ilegível. Para saber se a 204 está livre às 15h você abre o arquivo, acha a aba do dia, cruza a linha do horário com a coluna da sala e torce para ninguém ter mexido nos últimos dez minutos. Todo mundo desistia no segundo passo e saía andando pelo prédio.

Comecei o `app-salas` em 6 de março de 2026 com um escopo minúsculo: uma página que responde quais salas estão livres agora. O resto veio porque os alunos pediram.

## O que eu fiz

Duas versões inteiras, e a segunda existe porque a primeira acertou o problema e errou a fundação.

A primeira foi Flask em contêiner numa VM da GCP, com Google Sheets como banco. Funcionava. Ela ganhou cadastro com Google OAuth, notificação por web push, painel administrativo, página de privacidade, exportação e autoexclusão de conta para atender à LGPD, e uma suíte que chegou a 263 testes rodando em CI junto com `gitleaks` e `pip-audit`. Só o `pip-audit` apontou 16 CVEs em dependências transitivas numa única rodada, e o CI passou a barrar merge com dependência vulnerável.

O problema é que a planilha como banco cobra juros. Cada consulta virava chamada de API com cota, cada escrita concorrente era uma corrida, e a captura da grade rodava no GitHub Actions entregando de 6 a 10 execuções por dia quando o agendamento pedia 48. O Actions simplesmente não garante horário.

Em 23 de julho comecei a reescrita. Postgres de verdade no Supabase, autenticação e funções de borda no mesmo lugar, frontend estático no Cloudflare Pages, e a captura movida para `pg_cron` dentro do próprio banco. O corte para produção foi em 10 de agosto de 2026, com 70 alunos migrados e email de recadastro enviado para todos.

## Como funciona

O universo de salas deixou de ser subproduto do scraper. Ele vem de um repertório fixo e versionado, com 58 salas canônicas, 22 apelidos conhecidos e 11 grafias que devem ser ignoradas. Grafia que ninguém reconhece não vira sala nova: cai numa fila de quarentena para eu olhar depois.

Essa decisão nasceu de um bug bonito. A origem escreve pares de sala concatenados com barra, tipo `302/303`, então havia uma regra que quebrava tudo que tinha barra. Aí apareceu `114 LAB QUIMICA/FISICA`. A regra da barra rodava antes do repertório, engolia o nome como se fossem duas salas, e a 114 passou a ser servida como livre com aula dentro. Nem quarentena gerava, porque nada ali parecia estranho ao código. A ordem inverteu: canônica e apelido ganham da barra.

O aviso é PWA instalável com web push, incluindo iOS, que é onde a coisa dói. No iPhone o push só existe se o app estiver na tela de início, o `ServiceWorkerContainer` segura a fila de mensagens do worker até alguém chamar `startMessages()`, e um clique sintético não vibra. Cada uma dessas eu descobri quebrando a cara num aparelho real, nunca no simulador.

## O que aprendi

Duas coisas que eu não teria aprendido lendo.

A primeira veio de uma auditoria de segurança no banco novo. Eu tinha escrito uma policy de RLS que deixava o aluno atualizar a própria linha, e ela estava certa na metade que eu olhei. Policy de `UPDATE` no Postgres tem duas metades: o `USING`, que decide quais linhas você enxerga para escrever, e o `WITH CHECK`, que decide como a linha pode ficar depois. Sem o `WITH CHECK`, o aluno enxergava só a própria linha, escrevia só na própria linha, e podia escrever o próprio papel. Aluno logado alterando o próprio `role`. A correção foi uma migration com `WITH CHECK` explícito mais um trigger de guarda nas colunas sensíveis, e desde então eu leio toda policy de escrita procurando a metade que falta.

A segunda foi pior, porque não era código.

Quatro dias depois do corte, um aluno que tinha se descadastrado e saído recebeu uma notificação. Eu já tinha conferido o sistema novo: o cascade apagava em dois níveis, os testes provavam, o banco confirmava. O sistema novo estava certo. Só que o antigo nunca parou. A VM continuava lá, o contêiner do agendador continuava com `restart: always`, e ele seguia lendo a aba de inscrições da planilha velha e disparando push, sozinho, todo dia, para uma base que eu considerava morta. Eu tinha virado o DNS e chamado aquilo de desligar.

Virar o DNS não desliga nada. Desligar é `stop` no processo, com a mão, na máquina, e conferir depois.

## Resultados

- No ar em `ibsala.com.br` desde março de 2026, com o corte para a arquitetura nova em 10 de agosto e 70 alunos migrados sem perda de conta.
- A captura da grade saiu de 6 a 10 execuções por dia para as 48 previstas, ao trocar o agendador externo por `pg_cron` dentro do banco.
- O repertório fixo derrubou a lista de salas livres de 49 para 31 e fez as duas versões passarem a devolver exatamente a mesma resposta, sala por sala, nos seis horários do dia.
- 263 testes verdes em CI, com verificação de segredo e auditoria de dependência como jobs obrigatórios. 16 CVEs corrigidas numa rodada.
- Conformidade com a LGPD implementada e no ar: relatório de impacto, exportação e exclusão da própria conta, retenção com expurgo agendado e log de auditoria das ações administrativas.
