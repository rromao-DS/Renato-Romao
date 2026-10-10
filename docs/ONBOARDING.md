# Onboarding - Novo Cliente R2 Consultoria

Guia completo para integrar um novo cliente e configurar seus skills.

## Fase 1: Levantamento (Reunião Inicial)

### Informações Básicas
- [ ] Nome da empresa
- [ ] Regime de tributação (Lucro Real, Presumido, MEI)
- [ ] Segmento (Restaurante, Comércio, Serviço)
- [ ] Localização (Estado para prazos fiscais)
- [ ] Responsável técnico (nome, email, telefone)

### Processos Atuais
- [ ] Como processam notas fiscais hoje?
- [ ] Sistema ERP/Contábil em uso (SAP, Soptis, ContaAzul, etc.)
- [ ] Frequência de emissão de NFs (diária, semanal)
- [ ] Quantidade aproximada por mês

### Dores Principais
- [ ] Qual processo causa mais problemas?
- [ ] Quanto tempo leva hoje?
- [ ] Qual seria o ganho com automação?

### Dados Sensíveis
- [ ] Onde estão armazenados os arquivos?
- [ ] Restrições de segurança/compliance?
- [ ] LGPD compliance necessário?

---

## Fase 2: Seleção de Skills

Baseado nas necessidades, recomende skills:

### Recomendação Padrão (Quick Win)
1. **NF Processing** - Leitura e processamento de notas
2. **Expense Tracking** - Categorização de despesas

### Recomendação Completa
1. NF Processing
2. Expense Tracking  
3. Bank Reconciliation
4. Tax Calculation (se Lucro Real)

### Recomendação Customizada
Discussão com cliente sobre:
- Integração com ERP
- Frequência de processamento
- Formato de saída desejado

---

## Fase 3: Implementação

### 1. Criar Pasta do Cliente
```bash
mkdir -p clients/CLIENTE-NOME/{data,customizations}
```

### 2. Copiar Skills Base
```bash
# Se escolheu NF Processing
cp -r skills/accounting/nf-processing clients/CLIENTE-NOME/

# Se escolheu mais skills, repita para cada
```

### 3. Customizar Configuração

**clients/CLIENTE-NOME/nf-processing/config.json:**
```json
{
  "client_name": "CLIENTE-NOME",
  "client_id": "CLI-001",
  "region": "SP",
  "tax_regime": "lucro_real",
  "language": "pt-BR",
  
  "integrations": {
    "erp_system": "soptis",
    "email_domain": "cliente.com.br"
  },
  
  "customizations": {
    "nf_type": ["nf-e", "nfs-e"],
    "default_cost_center": "01",
    "auto_categorize": true
  },
  
  "contacts": {
    "technical": {
      "name": "João Silva",
      "email": "joao@cliente.com.br",
      "phone": "+55 11 9XXXX-XXXX"
    },
    "accounting": {
      "name": "Maria Santos",
      "email": "maria@cliente.com.br"
    }
  }
}
```

### 4. Adaptar Prompts (se necessário)

Se o skill precisa customização para regras específicas:

**clients/CLIENTE-NOME/customizations/prompts.md:**
```markdown
# Customizações de Prompts - CLIENTE-NOME

## Variações por Regime
O cliente está em Lucro Real, então:
- Sempre separar ICMS ST
- Calcular crédito de ICMS por operação
- Alertar para operações de ICMS

## Mapeamento de Contas
- Código ERP XYZ = Conta contábil ABC
- ...

## Regras de Negócio
- Despesas com viagem devem ir para "6.2.1.02"
- ...
```

### 5. Preparar Dados de Teste

**clients/CLIENTE-NOME/data/README.md:**
```markdown
# Dados de Teste - CLIENTE-NOME

## Estrutura
- `sample-input.json` - Exemplo de dados reais
- `sample-output.json` - Saída esperada
- `edge-cases.json` - Casos especiais

## Instruções
1. Colocar amostra real (sem dados sensíveis) em `sample-input.json`
2. Validar saída manualmente
3. Guardar resultado em `sample-output.json`
```

---

## Fase 4: Testes e Validação

### Testes Funcionais
- [ ] Executar skill com dados de exemplo
- [ ] Validar formato de saída
- [ ] Testar edge cases (valores nulos, datas inválidas)
- [ ] Testar com grande volume

### Testes de Integração
- [ ] Integração com ERP (se aplicável)
- [ ] Envio de email com resultados
- [ ] Persistência de dados

### Testes de Usabilidade
- [ ] Cliente consegue usar sem suporte?
- [ ] Interface é clara?
- [ ] Documentação é suficiente?

### Approval do Cliente
- [ ] Reunião de validação
- [ ] Sign-off formal (email)
- [ ] Captura de feedback

---

## Fase 5: Deploiement

### Checklist Pré-Deploy
- [ ] Código em produção testado
- [ ] Prompts finalizados
- [ ] Dados de teste OK
- [ ] Documentação atualizada
- [ ] Contatos documentados

### Pós-Deploy
- [ ] Notificar cliente (data/hora de ativação)
- [ ] Primeiros testes em produção
- [ ] Suporte 24h primeiro dia
- [ ] Feedback collection

---

## Fase 6: Suporte e Evolução

### Monitoramento (Primeiras 2 semanas)
- [ ] Executar skill diariamente
- [ ] Monitorar taxa de erro
- [ ] Responder rapidamente a problemas
- [ ] Ajustar prompts conforme necessário

### Feedback Loop
- [ ] Coletar feedback do cliente
- [ ] Identificar melhorias
- [ ] Priorizar mudanças
- [ ] Iterar e comunicar

### Documentação de Lições Aprendidas
- [ ] Atualizar skill base com aprendizados
- [ ] Compartilhar customizações reutilizáveis
- [ ] Melhorar prompts gerais

---

## Documentação do Cliente

Crie **clients/CLIENTE-NOME/README.md:**

```markdown
# CLIENTE-NOME

## Overview
- **Empresa:** [Nome]
- **Responsável:** [Nome, email]
- **Skills Ativados:** NF Processing, Expense Tracking
- **Go-live:** [Data]

## Customizações
1. [Descrição]
2. [Descrição]

## Dados de Teste
Ver pasta `data/`

## Histórico de Mudanças
- v1.0 (2026-09-19): Implementação inicial
- ...

## Contatos
- Técnico: João - joao@...
- Contábil: Maria - maria@...
```

---

## Timeline Recomendado

| Fase | Duração | Início |
|------|---------|--------|
| Levantamento | 1-2 dias | -2 semanas |
| Implementação | 3-5 dias | -1.5 semanas |
| Testes | 3-5 dias | -1 semana |
| Approval | 1-2 dias | -3 dias |
| Deploy | 1 dia | -1 dia |
| Suporte Intensivo | 2 semanas | Dia 1 |

**Total: ~4 semanas** (pode variar conforme complexidade)

---

## Dúvidas Comuns

**P: Cliente tem ERP customizado, conseguimos integrar?**
R: Depende. Consulte `docs/ARCHITECTURE.md` sobre integrações.

**P: Dados do cliente têm LGPD?**
R: Sim, sempre. Garantir que dados de teste não tenham PII, usar anonimização.

**P: Como treinar o cliente?**
R: Reunião de 1h explicando cada skill, depois documentação escrita + suporte por 2 semanas.

---

**Documento criado:** 2026-09-19
**Versão:** 1.0.0
