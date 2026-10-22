---
slug: cifra-local
titulo: Dados cifrados no aparelho
sub: Um padrão de app pessoal que não tem servidor para vazar, com o myco como caso
data: 2026-06-02
stack: [WebCrypto, PBKDF2, AES-GCM, IndexedDB, Vite]
competencias: [criptografia aplicada, privacidade por desenho, PWA]
repo: https://github.com/joshazze/myco
---

## Contexto

Todo app pessoal começa do mesmo jeito: você quer registrar algo seu, num lugar seu. Plantas, treinos, gastos.

Onde isso mora? A resposta habitual é um banco num servidor, com login e senha, o que cria um servidor com os seus dados dentro e faz de você o responsável pelo backup, pela atualização de dependências e, um dia, por um vazamento. Para um app de uma pessoa só, é muita responsabilidade para pouco ganho.

A outra resposta é guardar tudo em texto puro no navegador. Some o servidor. Mas qualquer script na página, extensão ou pessoa com o aparelho na mão lê tudo.

## O que eu fiz

Um padrão que usei em mais de um app: os dados são cifrados no próprio aparelho e nunca saem dele em texto puro. Não há conta nem servidor, e por isso não há nada do meu lado que possa vazar.

O exemplo aqui é o **myco**, um app de jardinagem que registra vasos, setores, adubação e compostagem. É público e simples, e a simplicidade ajuda: se o padrão funciona para um caderno de plantas, funciona para outros casos. O mesmo módulo de criptografia roda hoje em outro app pessoal meu, com dados mais sensíveis.

## Como funciona

A senha nunca é armazenada e nunca vira a chave diretamente.

Ela passa por PBKDF2 com 250.000 iterações e SHA-256, junto de um sal aleatório gerado na criação da base, e o resultado é uma chave AES-GCM de 256 bits. As iterações encarecem cada palpite: quem conseguir a base cifrada precisa calcular 250 mil derivações por tentativa, e um ataque de dicionário deixa de ser viável.

Cada gravação é cifrada com AES-GCM e um vetor de inicialização novo, o que garante confidencialidade e integridade na mesma operação: se um byte for alterado no armazenamento, a decifragem falha em vez de devolver dados corrompidos sem aviso. Tudo usa a WebCrypto do navegador, sem biblioteca externa de criptografia, e o resultado fica guardado no IndexedDB.

Há também um verificador curto, cifrado com a mesma chave, que serve para avisar "senha incorreta" logo na abertura.

## O que aprendi

O backup foi a parte mais difícil.

Sem servidor, não há recuperação de senha. Esqueceu, perdeu. É consequência direta da promessa do app. Foi o que mais demorei a aceitar, e cheguei a considerar um servidor só para oferecer um "esqueci minha senha".

A solução foi exportar a base cifrada como arquivo, que a pessoa guarda onde preferir. Sem a senha ele não serve para nada. O app deixa claro que não protege contra o esquecimento da senha, em vez de manter uma porta dos fundos que também estaria disponível para um atacante. Prefiro um sistema que declara seus limites a um que depende de o usuário nunca errar.

## Resultados

- Padrão em produção em dois apps pessoais, que compartilham o mesmo módulo de criptografia.
- PBKDF2 com 250.000 iterações e SHA-256 derivando chave AES-GCM de 256 bits, tudo pela WebCrypto nativa, sem biblioteca externa de criptografia.
- Nenhum servidor e nenhuma conta: os dados do usuário existem apenas no aparelho dele.
- Exportação da base cifrada como backup, que pode ser guardada em qualquer lugar sem virar risco.
- O `myco` é público, sob licença aberta, instalável como app e com o código de cifra num único arquivo, fácil de ler.
