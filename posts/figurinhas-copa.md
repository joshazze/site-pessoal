---
slug: figurinhas-copa
titulo: Figurinhas Copa 2026
sub: PWA para acompanhar o álbum, com OCR lendo o código da figurinha na foto
data: 2026-05-20
stack: [JavaScript, Capacitor, OCR, FastAPI, PostgreSQL, Caddy]
competencias: [PWA, visão computacional aplicada, backend, iOS]
repo: https://github.com/joshazze/figurinhas-copa
---

## Contexto

O álbum da Copa de 2026 tem 980 figurinhas: 912 normais e 68 douradas metalizadas. O pacote vem com 7 e custa 7 reais. A primeira Copa com 48 seleções é também a primeira em que a conta de quanto falta virou um problema de verdade.

Quem coleciona resolve isso com uma lista no papel ou uma planilha, e as duas quebram no mesmo ponto: na hora de conferir. Você abre o pacote, tem sete cromos na mão, e precisa descobrir se cada um é novo ou repetido. Sete consultas manuais por pacote, e um pacote leva quinze segundos para abrir.

## O que eu fiz

Um app instalável que responde três perguntas: o que eu tenho, o que falta, e o que está repetido para trocar. Mais quanto já foi gasto para chegar até ali, que é a pergunta que ninguém quer fazer e todo mundo faz.

A parte que mudou o app foi o escaneamento. Em vez de digitar o código de cada figurinha, você fotografa e o app lê. O reconhecimento roda no navegador, não no servidor, então funciona com a conexão ruim de um pátio de escola. O empacotamento para iOS é feito com Capacitor, o que dá acesso à câmera nativa mantendo o mesmo código do app web.

Atrás disso existe um backend próprio: FastAPI em Python, PostgreSQL 16 e Caddy como proxy reverso, que resolve HTTPS sozinho via Let's Encrypt. Ele guarda o catálogo canônico, as coleções e o histórico, para o álbum não morrer com o navegador do aparelho.

## Como funciona

O reconhecimento é simples de descrever e cheio de armadilha: fotografa a costa da figurinha, extrai o texto, e casa o que foi lido contra o dicionário de códigos canônicos com comparação aproximada, porque OCR erra.

O que faz o pipeline funcionar não é o reconhecedor, é a normalização antes da comparação. Códigos da Panini são letras coladas em dígitos, sem separador. Todo espaço que o reconhecedor lê é artefato do papel, da luz ou do ângulo, e não carrega informação nenhuma.

## O que aprendi

"COL 4" não casava com "COL4".

A foto estava cristalina, o código legível a olho nu, e o app dizia "não lido". Eu tinha escrito a normalização colapsando espaços múltiplos em um só, que é o que se faz com texto de gente. Só que aqui o espaço não é separador de palavra, é sujeira, e a comparação aproximada entre "COL 4" e "COL4" ficava logo abaixo do corte. Um caractere invisível derrubando um acerto óbvio. A correção foi trocar colapsar por remover, e ela vale para qualquer domínio em que o rótulo é um token contíguo: SKU, placa de carro, código de peça. Se o reconhecimento está falhando em caso fácil, desconfie da normalização antes de desconfiar do modelo.

A segunda lição é a que eu gosto mais, porque ela é sobre o limite do automático.

Existem cromos promocionais de uma rede de fast food que compartilham a numeração com os regulares. Eu tinha o reconhecimento escolhendo entre um e outro por pontuação de semelhança, e ele acertava às vezes. Fui olhar por que ele errava, e a resposta era humilhante: a costa dos dois é idêntica. Não parecida, idêntica. Só quem está com o cromo na mão, vendo a frente, sabe qual é qual. Nenhuma quantidade de ajuste de limiar ia resolver, porque a informação não estava na imagem.

Tirei esses códigos do dicionário do reconhecedor. O backend passou a não poder emitir aquele código automaticamente, nunca, e a decisão virou um botão no app para a pessoa marcar. Ensinar o sistema a não adivinhar foi mais trabalho do que ensinar a adivinhar, e foi a coisa certa: um palpite errado com cara de certeza custa mais que uma pergunta honesta.

## Resultados

- Catálogo completo das 980 figurinhas (912 normais e 68 douradas), com controle de repetidas e cálculo de gasto acumulado.
- Reconhecimento de código por foto rodando no próprio navegador, sem depender de rede para o escaneamento.
- Empacotado para iOS com Capacitor, mantendo uma base de código só entre web e app.
- Backend em FastAPI e PostgreSQL 16, com HTTPS automático por Caddy, mantendo a coleção fora do aparelho.
- Correção de normalização que devolveu ao reconhecimento os casos fáceis que ele estava perdendo por um espaço.
