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

O Ibmec BH publica a ocupação das salas numa planilha que a coordenação atualiza ao longo do dia. Correta e ilegível. Para saber se a 204 está livre às 15h, é preciso abrir o arquivo, achar a aba do dia, cruzar o horário com a coluna da sala e esperar que nada tenha mudado nos últimos minutos. Na prática, a maioria desistia e ia procurar sala andando pelo prédio.

Comecei o `app-salas` em 6 de março de 2026 com um escopo pequeno: uma página que mostrasse quais salas estão livres agora. O restante veio de pedidos dos próprios alunos.

## O que eu fiz

Duas versões completas. A segunda existe porque a primeira resolveu o problema certo sobre uma base que não aguentaria crescer.

A primeira era Flask em contêiner numa VM da GCP, com Google Sheets como banco. Funcionava. Ganhou cadastro com Google OAuth, notificações por web push, painel administrativo, página de privacidade, exportação e exclusão da própria conta para atender à LGPD, além de uma suíte de 263 testes rodando em CI com `gitleaks` e `pip-audit`. O `pip-audit` encontrou 16 CVEs em dependências transitivas numa única rodada, e a partir daí o CI passou a bloquear merge com dependência vulnerável.

Usar a planilha como banco, porém, tinha um custo crescente. Cada consulta era uma chamada de API com cota, cada escrita simultânea podia gerar conflito, e a captura da grade, agendada no GitHub Actions para 48 execuções por dia, rodava de 6 a 10 vezes. O Actions não garante horário, e lá um agendamento de meia em meia hora vira sugestão.

Em 23 de julho comecei a reescrita: Postgres no Supabase, autenticação e funções de borda no mesmo lugar, frontend estático no Cloudflare Pages e a captura movida para `pg_cron` dentro do banco. A migração para produção aconteceu em 10 de agosto de 2026, com 70 alunos migrados e um email de recadastro enviado a todos.

## Como funciona

A lista de salas deixou de depender do que o scraper encontra. Ela vem de um repertório fixo e versionado, com 58 salas oficiais, 22 apelidos conhecidos e 11 grafias que devem ser ignoradas. Grafia desconhecida não vira sala nova: vai para uma fila de quarentena, que eu reviso depois com calma, uma por uma.

Ela veio de um bug. A planilha escreve pares de salas separados por barra, como `302/303`, e havia uma regra que dividia tudo o que tinha barra. Aí veio `114 LAB QUIMICA/FISICA`. A regra da barra rodava antes do repertório, dividia o nome como se fossem duas salas, e a 114 passou a aparecer como livre com aula acontecendo. Nem a quarentena pegou, porque para o código nada ali parecia estranho. Invertemos a ordem: sala oficial e apelido têm prioridade sobre a regra da barra.

O aviso é um PWA instalável com web push, inclusive no iOS, onde há mais detalhes a cuidar. No iPhone o push só funciona com o app na tela de início, o `ServiceWorkerContainer` segura as mensagens do worker até alguém chamar `startMessages()`, e um clique simulado não aciona a vibração. Descobri cada um desses pontos testando num aparelho real. O simulador não mostrava nenhum deles.

## O que aprendi

Duas lições.

A primeira veio de uma auditoria de segurança no banco novo. Eu tinha escrito uma policy de RLS que permitia ao aluno atualizar a própria linha, e ela estava correta na parte que eu tinha revisado. No Postgres, uma policy de `UPDATE` tem duas partes: o `USING`, que define quais linhas podem ser alteradas, e o `WITH CHECK`, que define como a linha pode ficar depois da alteração. Sem o `WITH CHECK`, o aluno só via e alterava a própria linha, mas podia mudar o próprio papel no sistema, inclusive o campo `role`. A correção foi uma migration com `WITH CHECK` explícito e um trigger protegendo as colunas sensíveis. Desde então, em toda policy de escrita, confiro as duas partes.

A segunda não era código.

Quatro dias depois da migração, um aluno que já tinha cancelado o cadastro recebeu uma notificação. O sistema novo estava correto: a exclusão em cascata apagava os dados em dois níveis, os testes confirmavam e o banco também. O antigo continuava rodando. A VM seguia ligada, o contêiner do agendador tinha `restart: always`, e ele continuava lendo a aba de inscrições da planilha antiga e enviando push todos os dias, para uma base que eu considerava desativada. Eu tinha apontado o DNS para o sistema novo e considerado o antigo desligado.

Trocar o DNS não desliga um serviço. Desligar é parar o processo na máquina e conferir depois que ele parou.

## Resultados

- No ar em `ibsala.com.br` desde março de 2026, com a migração para a nova arquitetura em 10 de agosto e 70 alunos migrados sem perda de conta.
- A captura da grade passou de 6 a 10 execuções por dia para as 48 previstas, com o agendamento movido para o `pg_cron` dentro do banco.
- O repertório fixo reduziu a lista de salas livres de 49 para 31 e fez as duas versões devolverem exatamente a mesma resposta, sala por sala, nos seis horários do dia.
- 263 testes verdes em CI, com verificação de segredos e auditoria de dependências como etapas obrigatórias, e 16 CVEs corrigidas numa rodada.
- Conformidade com a LGPD no ar: relatório de impacto, exportação e exclusão da própria conta, retenção com expurgo agendado e registro de auditoria das ações administrativas.
