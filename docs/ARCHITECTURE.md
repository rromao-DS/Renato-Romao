# Arquitetura de Skills - R2 Consultoria

## Visão Geral

Cada skill é uma unidade independente e reutilizável que pode ser adaptada para diferentes clientes mantendo a lógica core.

## Estrutura de um Skill

```
skills/accounting/nf-processing/
├── README.md              # Documentação do skill
├── config.json           # Configurações padrão
├── prompts.md            # Prompts do Claude
├── examples/             # Exemplos de entrada/saída
│   ├── input/
│   └── output/
├── tests/                # Testes e validações
│   └── test-data.json
└── utils/                # Funções auxiliares (se aplicável)
    └── parser.js
```

## Configuração por Cliente

Cada cliente tem sua pasta em `clients/<nome>/`:

```
clients/cliente-a/
├── config.json           # Overrides da config padrão
├── customizations/       # Customizações específicas
│   ├── prompts.md        # Prompts customizados
│   └── rules.json        # Regras de negócio
└── data/                 # Dados do cliente
    ├── sample-input.json
    └── settings.json
```

## Fluxo de Desenvolvimento

### 1. Criar Skill Base
- Definir propósito claro
- Criar estrutura padrão
- Documentar decisões

### 2. Implementar
- Escrever prompts robustos
- Criar exemplos de teste
- Testar com dados variados

### 3. Adaptar para Cliente
- Copiar skill base
- Customizar config.json
- Ajustar prompts se necessário
- Validar com dados reais do cliente

### 4. Manter
- Coletar feedback
- Melhorar prompts
- Compartilhar aprendizados (atualizar skill base)

## Padrão de Nomenclatura

- **Skills:** snake_case (ex: `nf-processing`, `expense-tracking`)
- **Clientes:** Cliente-Name (ex: `cliente-a`, `escritorio-xyz`)
- **Variáveis:** camelCase (ex: `invoiceNumber`, `clientId`)
- **Funções:** snake_case (ex: `parse_nf`, `validate_amount`)

## Dependências Compartilhadas

Em `skills/shared/utils/` colocamos:
- Parsers comuns
- Validadores
- Formatadores
- Conversores de moeda/data

Exemplo uso:
```javascript
const { parseDate, formatCurrency } = require('../../shared/utils');
```

## Versionamento de Skills

Cada skill mantém `version.txt` com semântica:
- `1.0.0` - Versão inicial
- `1.1.0` - Nova feature
- `1.0.1` - Bug fix

## Integração com Claude

### Via Prompts
Cada skill tem `prompts.md` com:
- System prompt padrão
- Exemplos de entrada
- Formato esperado de saída
- Edge cases conhecidos

### Via API
Potenciais integrações futuras:
- Webhooks para processamento assíncrono
- API REST para skills
- Job queue para processos em batch

---

**Design Principle:** Reutilização + Customização = Escalabilidade
