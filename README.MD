## Fluxo de Trabalho com Git

### Criação de Branches

- `feature/nome-da-feature`: Para novas funcionalidades.
- `bugfix/nome-do-bug`: Correções de bugs identificados em dev.
- `hotfix/nome-do-hotfix`: Correções urgentes diretamente no main.
- `release/x.y.z`: Preparação de uma nova versão.

### Regras para Pull Requests

- Sempre abrir um PR para `dev` ou `main`.
- Pelo menos **1 revisão** obrigatória.
- Commits no padrão [Conventional Commits](https://www.conventionalcommits.org/pt-br/v1.0.0/).
- Usar **merge** com *squash* para manter histórico limpo.

### Estratégia de Merge

- Devs trabalham em branches de feature e abrem PRs para `dev`.
- Quando `dev` estiver estável, abrir PR para `main` (geralmente numa release).

### Configuração Local

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
````

### Conventional Commits:
- `feat:` – nova funcionalidade
- `fix:` – correção de bug
- `docs:` – mudanças na documentação
- `style:` – formatação, sem mudança de código
- `refactor:` – refatoração sem alterar comportamento
- `test:` – testes adicionados ou corrigidos