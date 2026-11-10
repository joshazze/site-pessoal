---
slug: setup-claude
titulo: Setup por um link
sub: Um roteiro que o próprio assistente lê e executa para instalar memória, personas e editor na máquina de outra pessoa
data: 2026-08-10
stack: [Bash, jq, Claude Code, Obsidian, Markdown]
competencias: [ferramenta de desenvolvedor, instalação não destrutiva, documentação, distribuição]
areas: [Ferramentas de desenvolvedor, IA aplicada, Código aberto]
repo: https://github.com/joshazze/setup-claude
---

## Contexto

Eu já tinha publicado duas peças do meu ambiente de trabalho: o Cérebro, que dá memória entre sessões ao assistente de código, e os heterónimos, personas estreitas com gatilho próprio. Cada uma tinha instalador e documentação.

Instalar tudo na máquina de outra pessoa era o problema. Eram três repositórios, uma ordem certa de instalação e uma parte que não morava em repositório nenhum: o editor Obsidian com um plugin de captura e o assistente rodando dentro dele.

Ninguém ia seguir aquilo.

## O que eu fiz

Um repositório guarda-chuva com duas entradas. A primeira é uma frase que a pessoa cola no assistente, pedindo que ele leia um roteiro e execute. Para quem prefere, existe um script de shell que faz a mesma instalação sem gastar token.

O roteiro tem sete passos. O assistente faz cinco perguntas numa mensagem só, instala as três camadas em ordem, verifica o resultado e termina explicando o que a pessoa ganhou e o que digitar no dia seguinte.

Esse repositório não reimplementa as outras duas camadas. Ele chama os instaladores delas e acrescenta a terceira.

## Como funciona

O roteiro é um arquivo de texto escrito para um leitor que não é humano. Cada passo diz o que rodar, como conferir que deu certo e o que fazer se falhar. O último passo, explicar, é obrigatório.

A instalação não destrói nada. Quem chega já tem arquivo de configuração e notas próprias. Todo JSON existente é mesclado com `jq`, com backup datado antes de qualquer escrita, e nenhuma nota do cofre é sobrescrita. Rodar duas vezes não duplica.

Um script de diagnóstico confere as três camadas e diz qual está quebrada. Outro desinstala ganchos e scripts e deixa o cofre onde está, porque as notas são da pessoa.

## O que aprendi

O arquivo de instruções do assistente entra no contexto em todo turno de toda sessão. Com quatro personas descritas por inteiro, ele chegava a 25 KB, cerca de 6 mil tokens pagos a cada mensagem, usando a persona ou não.

A saída foi separar ativação de especificação. No arquivo fica só o gatilho de cada persona e o caminho do arquivo completo, que o assistente lê quando o gatilho dispara. Um script faz esse corte numa instalação existente.

Escrever para um agente executar é diferente de escrever documentação. Onde um humano improvisa, o agente segue a frase ao pé da letra. "Configurar o cofre" não é um comando. Cada passo precisa ser uma ação com uma verificação.

Mantive o caminho por script de propósito. Ele faz a mesma instalação de forma determinística, e serve de prova de que o roteiro não depende de o modelo interpretar bem um texto.

## Resultados

- Três repositórios instalados por uma frase colada, em 10 a 15 minutos.
- Arquivo de instruções reduzido de 25 KB para 5,8 KB.
- Índice de sessão de cerca de 1.100 tokens, com as notas abertas sob demanda.
- Dependências: `git`, `jq`, `curl` e `awk`.
- Licença MIT.
