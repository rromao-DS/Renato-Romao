# Guia de Skills - Como Criar e Adaptar

## Para Criar um Novo Skill

### 1. Defina o Propósito
- Qual problema resolve?
- Quais dados de entrada?
- Qual saída esperada?

### 2. Crie a Estrutura Base
```bash
mkdir -p skills/accounting/seu-skill/{examples/{input,output},tests}
cd skills/accounting/seu-skill
```

### 3. Crie os Arquivos Essenciais

**README.md** - Documentação
```markdown
# Nome do Skill

## Propósito
Descrição clara do que faz.

## Entrada
- Formato esperado
- Exemplos

## Saída
- Formato dos resultados
- Tratamento de erros

## Como Usar
Instruções claras.
```

**config.json** - Configuração Padrão
```json
{
  "name": "seu-skill",
  "version": "1.0.0",
  "description": "Descrição breve",
  "model": "claude-opus-5",
  "inputs": {
    "file_format": ["json", "csv"],
    "max_file_size_mb": 10
  },
  "outputs": {
    "format": "json"
  }
}
```

**prompts.md** - Instruções para Claude
```markdown
# Prompts - Seu Skill

## System Prompt
Você é um especialista em [domínio]. Seu trabalho é...

## Exemplos de Entrada
```json
{
  "example": "data"
}
```

## Formato Esperado de Saída
```json
{
  "result": "processed data"
}
```

## Edge Cases
- Valores nulos
- Dados malformados
- Valores fora do range
```

### 4. Crie Exemplos e Testes
```bash
# examples/input/exemplo1.json
{
  "data": "exemplo"
}

# examples/output/exemplo1.json
{
  "resultado": "processado"
}

# tests/test-data.json
{
  "test_cases": [
    {
      "name": "Teste 1",
      "input": {...},
      "expected_output": {...}
    }
  ]
}
```

### 5. Documente Decisões
Crie `.decisions` com:
- Por que essa abordagem?
- Trade-offs considerados
- Limitações conhecidas

## Para Adaptar um Skill para Novo Cliente

### 1. Copie o Skill Base
```bash
cp -r skills/accounting/nf-processing clients/cliente-novo/nf-processing
```

### 2. Customize o config.json
```json
{
  "client_name": "cliente-novo",
  "region": "SP",
  "tax_regime": "lucro_real",
  "integrations": {
    "erp_system": "sistema_x",
    "email_domain": "cliente-novo.com.br"
  }
}
```

### 3. Customize Prompts (se necessário)
Crie `customizations/prompts.md` com variações específicas:
- Formato de saída customizado
- Regras de negócio específicas
- Campos adicionais

### 4. Teste com Dados Reais
```bash
# Coloque sample data em
clients/cliente-novo/data/sample-input.json

# Teste manualmente
```

### 5. Documente Customizações
Crie `clients/cliente-novo/README.md`:
```markdown
# Cliente Novo - NF Processing

## Customizações
- Campo X mapeado para Y
- Regra Z aplicada automaticamente

## Dados de Teste
Ver pasta `data/`

## Contato
Nome do responsável: X
Email: y@z.com
```

## Checklist para Novo Skill

- [ ] README completo e claro
- [ ] config.json com todos os parâmetros
- [ ] prompts.md com exemplos reais
- [ ] examples/ com input e output
- [ ] tests/ com casos de teste
- [ ] Decisões documentadas em `.decisions`
- [ ] Testado com dados variados
- [ ] Pronto para reutilização

## Checklist para Adaptar Skill

- [ ] Copiado para pasta do cliente
- [ ] config.json customizado
- [ ] Prompts ajustados (se necessário)
- [ ] Testado com dados do cliente
- [ ] README do cliente preenchido
- [ ] Contato do cliente documentado
- [ ] Aprovado pelo cliente

---

**Dúvidas?** Consulte `examples/` em cada skill para referência.
