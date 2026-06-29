# iHaveStandards

## English

**This is a template repository.** It is not an application — it is a
battle-tested starting point. Clone it, rename the example domain, and build
your product inside a structure whose architecture and quality gates are already
decided for you. The worked example resource is `items`: a single CRUD domain
threaded through every layer so the pattern is obvious and copyable.

### How to run

You need four tools installed: **git**, **Python 3.12**, **Bun**, and **make**.
There is no Docker and no database to install — the data lives in a single SQLite
file, created automatically on first run.

Install the dependencies once:

```sh
cp .env.example .env
make back-install
make front-install
```

Then start the whole app with a single command:

```sh
make dev
```

The backend runs at http://localhost:8000 and the interface at
http://localhost:5173, talking to each other automatically. Press Ctrl-C to stop.

### Checking quality

A single command runs every check (code style, build, and tests):

```sh
make check
```

These are the same checks that run automatically on GitHub for every Pull
Request, so what passes here passes there too.

## Português

**Este é um repositório de modelo.** Não se trata de uma aplicação pronta, mas
sim de um ponto de partida já validado na prática. Clone-o, renomeie o domínio de
exemplo e desenvolva seu produto dentro de uma estrutura cuja arquitetura e
critérios de qualidade já foram definidos para você. O recurso utilizado como
exemplo prático é `items`: um domínio CRUD simples implementado em todas as
camadas, tornando o padrão evidente e fácil de replicar.

### Como rodar

Você precisa de quatro ferramentas instaladas: **git**, **Python 3.12**, **Bun**
e **make**. Não há Docker nem banco de dados para instalar — os dados ficam em um
único arquivo SQLite, criado sozinho na primeira execução.

Instale as dependências uma única vez:

```sh
cp .env.example .env
make back-install
make front-install
```

Depois, inicie o aplicativo inteiro com um único comando:

```sh
make dev
```

O backend roda em http://localhost:8000 e a interface em http://localhost:5173,
conversando entre si automaticamente. Pressione Ctrl-C para parar.

### Conferindo a qualidade

Um único comando roda todas as verificações (estilo de código, build e testes):

```sh
make check
```

São as mesmas verificações que rodam automaticamente no GitHub a cada Pull
Request, então o que passa aqui passa lá também.
