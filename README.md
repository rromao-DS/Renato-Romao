# R2 Consultoria - Automação e Integração Claude

Plataforma de skills reutilizáveis para automação de processos em escritórios de contabilidade e gestão.

## 📋 Visão Geral

Este projeto desenvolve e mantém skills Claude especializados em:
- **Processamento de Notas Fiscais** (NF-e, NFS-e)
- **Rastreamento de Despesas** (categorizações automáticas)
- **Reconciliação Bancária** (matching de transações)
- **Cálculo de Impostos** (apuração de ICMS, PIS, COFINS, IR)
- **Automações de Email** (integração com sistemas)

## 🏗️ Arquitetura

```
skills/
├── accounting/          # Skills específicos de contabilidade
│   ├── nf-processing/   # Processamento de notas fiscais
│   ├── expense-tracking/# Rastreamento de despesas
│   ├── reconciliation/  # Conciliação bancária
│   └── tax-calculation/ # Cálculo de impostos
├── automation/          # Automações gerais
│   └── email-integration/
└── shared/              # Código compartilhado
    └── utils/

clients/                # Configurações por cliente
docs/                   # Documentação e templates
```

## 🚀 Quick Start

1. **Explorar um skill existente:**
   ```bash
   ls -la skills/accounting/nf-processing/
   ```

2. **Adaptar skill para novo cliente:**
   - Copiar skill base
   - Customizar `config.json`
   - Testar com dados do cliente

3. **Criar novo skill:**
   - Usar template em `docs/TEMPLATE.md`
   - Seguir estrutura padrão
   - Documentar em `README.md` local

## 📚 Documentação

- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - Design de sistema
- [SKILLS_GUIDE.md](docs/SKILLS_GUIDE.md) - Como criar/adaptar skills
- [ONBOARDING.md](docs/ONBOARDING.md) - Guia de onboarding para clientes
- [TEMPLATE.md](docs/TEMPLATE.md) - Template para novo skill

## 👥 Parceria

- **Leandro Augusto** - Consultoria de Processos
- **Contadores Parceiros** - Feedback e casos de uso

## 📊 Clientes

| Cliente | Skills Ativos | Status |
|---------|--------------|--------|
| (em desenvolvimento) | - | - |

---

**Última atualização:** 2026-09-19
