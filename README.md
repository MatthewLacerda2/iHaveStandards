# iHaveStandards

**Este é um repositório de modelo.** Não se trata de uma aplicação pronta, mas
sim de um ponto de partida já validado na prática. Clone-o, renomeie o domínio de
exemplo e desenvolva seu produto dentro de uma estrutura cuja arquitetura e
critérios de qualidade já foram definidos para você. O recurso utilizado como
exemplo prático é `items`: um domínio CRUD simples implementado em todas as
camadas, tornando o padrão evidente e fácil de replicar.

## Como rodar

Você só precisa de duas ferramentas instaladas: **Python 3.12** (para o servidor)
e **Bun** (para a interface). Não há Docker nem banco de dados para instalar — os
dados ficam em um único arquivo SQLite, criado sozinho na primeira execução.

Antes de tudo, copie o arquivo de configuração de exemplo:

```sh
cp .env.example .env
```

**Servidor (backend)** — instale uma vez e rode:

```sh
make back-install
cd backend && .venv/bin/uvicorn main:app --reload
```

O servidor fica disponível em http://localhost:8000.

**Interface (frontend)** — em outro terminal, instale uma vez e rode:

```sh
make front-install
cd frontend && bun run dev
```

A interface fica em http://localhost:5173 e já conversa com o servidor
automaticamente.

## Conferindo a qualidade

Um único comando roda todas as verificações (estilo de código, build e testes):

```sh
make check PYTHON=.venv/bin/python
```

São as mesmas verificações que rodam automaticamente no GitHub a cada Pull
Request, então o que passa aqui passa lá também.
