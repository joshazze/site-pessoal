---
slug: limites
titulo: Limites
sub: App de barra de menus para macOS com os limites de uso do Claude Code e do Codex
data: 2026-09-18
stack: [Swift, SwiftUI, swift-testing, AppleScript, GitHub Actions]
competencias: [macOS nativo, engenharia reversa, privacidade, ferramenta de desenvolvedor]
repo: https://github.com/joshazze/limites
---

## Contexto

Uso o Claude Code e o Codex todos os dias, e os dois têm janelas de uso: uma de cinco horas e outra semanal. Para saber quanto restava, eu abria cada uma. Com várias abas de terminal abertas, também perdia o momento em que uma delas terminava uma tarefa ou esperava minha resposta.

A ideia veio de um executável de Windows que chegou a mim por WhatsApp, um app chamado "AI Limits". Não uso Windows, e binário de origem desconhecida eu não rodo. Li as strings do arquivo para entender o que ele fazia e escrevi do zero, em Swift, uma versão nativa para o Mac que faz a mesma coisa e mais um pouco.

## O que eu fiz

Um app de barra de menus em SwiftUI, cujo ícone é um medidor com ponteiro que mostra o maior uso entre as janelas de cinco horas das duas ferramentas. Ao clicar, abre um painel com cada janela, o percentual e o horário de renovação. As semanais ficam ali, sem mexer no ponteiro.

A segunda função é o aviso de aba. Quando uma sessão termina ou pede permissão, o app toca um som e um sino balança na barra de menus, com o nome da conversa ao lado. Volto para a aba, ele some.

## Como funciona

Os dados vêm das próprias ferramentas. Sem raspar página, sem chave de API. No Claude Code, o app roda `claude -p /usage` com flags que impedem o carregamento de hooks e servidores MCP; a consulta é local, com zero turnos e custo zero, e caiu de 2,3 para 1,4 segundo com essas flags. No Codex, ele abre o `codex app-server` e conversa por JSON-RPC até receber os limites.

O aviso usa hooks. Um pequeno executável dentro do app sobe a árvore de processos até achar o `claude` ou o `codex`, descobre o terminal da aba e descarta sessões sem tela. Para saber se já voltei à aba, o app olha o horário de acesso do terminal (o mesmo dado que o comando `w` usa para medir inatividade), que muda quando digito ou dou foco na janela. O executável roda em cerca de 10 milissegundos e não escreve nada na saída, então não acrescenta nada ao contexto da conversa.

## O que aprendi

Publicar exige cuidado com o que vai junto.

O app nasceu cheio de detalhes meus: identificador de pacote com meu nome, fuso horário de São Paulo nos testes, interface só em português. Antes do primeiro push, troquei o identificador por `io.github.joshazze.limites`, passei os textos para inglês com a tradução em português num arquivo separado, mudei o fuso dos testes para Nova York e criei um modo de demonstração com dados fictícios para gerar o screenshot. O commit saiu com email anônimo. Por fim, rodei uma varredura com uma lista de 116 termos pessoais, guardada fora do repositório, e ela só encontrou falsos positivos.

A tradução ganhou teste: um script extrai as chaves direto do compilador e falha se alguma estiver faltando ou sobrando, e confirmei que ele funciona quebrando o arquivo de propósito.

## Resultados

- Repositório público sob licença MIT, com CI no macOS 15 verde desde o primeiro push.
- 11 testes em swift-testing, cobrindo o parser do `/usage`, fusos, virada de ano, o retorno do Codex e a escolha do maior percentual.
- 58 textos de interface traduzidos, com checagem automática de chaves.
- Consulta de uso sem gasto de tokens e aviso de aba em cerca de 10 ms, sem nada entrando no contexto da conversa.
