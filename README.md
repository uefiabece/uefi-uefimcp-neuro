# uefi-uefimcp-neuro

Servidor MCP de **Bacharelado em Neurociência**, UFABC. Nível: **curso**.

## Origem

Derivado de [`uefi-uefimcp`](https://github.com/uefiabece/uefi-uefimcp) por cópia da estrutura,
sem importar materiais acadêmicos. O commit de origem está registrado em `config/subject.json`.
O suporte opcional a PDF foi espelhado do repositório irmão `uefi-uefimcp-bct`.

```text
uefi-uefimcp
  ├── uefi-uefimcp-bct
  │   └── uefi-uefimcp-femec
  └── uefi-uefimcp-neuro
      └── uefi-uefimcp-introducao-a-neuro
```

## Executar

Requer Python 3.11 ou superior. No diretório deste repositório:

```sh
python -m venv .venv
.venv/Scripts/python -m pip install -e ".[pdf]"
.venv/Scripts/python run.py
```

O processo usa transporte **stdio**: deve ser iniciado por um cliente MCP.
Em Linux/macOS, use `.venv/bin/python`.

## Conectar

No campo `mcpServers` do cliente, adicione a entrada abaixo substituindo os caminhos:

```json
{
  "uefi-mcp-neuro": {
    "command": "CAMINHO_ABSOLUTO/uefi-uefimcp-neuro/.venv/Scripts/python.exe",
    "args": ["CAMINHO_ABSOLUTO/uefi-uefimcp-neuro/run.py"]
  }
}
```

O caminho absoluto para `run.py` permite iniciar o servidor de qualquer diretório.
O exemplo completo está em `config/mcp.example.json`.

## Conteúdo e ferramentas

As pastas `content/syllabus`, `bibliography`, `exams`, `exercises`, `notes` e `media`
estão vazias, prontas para receber seus materiais. Complete os metadados em
`config/subject.json` quando as informações da turma estiverem disponíveis.

O servidor oferece as 11 ferramentas gerais de conteúdo, ensino e exercícios,
além dos prompts `teach` e `solve`. Não inclui regras curriculares específicas
nem ementas inventadas. Sem materiais, as consultas retornam a ausência de conteúdo.

Teste de conexão real, incluindo inicialização, ferramentas, prompts e recursos:

```sh
.venv/Scripts/python scripts/check_mcp.py
```
