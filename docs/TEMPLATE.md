# Template - Novo Skill

Copie esta estrutura como base para criar um novo skill.

## Passo 1: Crie a Pasta
```bash
mkdir -p skills/accounting/seu-skill/{examples/{input,output},tests}
```

## Passo 2: Crie README.md

```markdown
# Seu Skill

## Propósito
Uma linha clara: O que esse skill faz?

## Características
- Feature 1
- Feature 2
- Feature 3

## Entrada (Input)
Descreva o formato esperado:

**Formato:** JSON
**Campos Obrigatórios:**
- `campo1` (tipo): Descrição
- `campo2` (tipo): Descrição

**Exemplo:**
\`\`\`json
{
  "campo1": "valor",
  "campo2": 123
}
\`\`\`

## Saída (Output)
Descreva o formato de retorno:

**Formato:** JSON
**Campos:**
- `resultado` (tipo): Descrição
- `status` (string): "sucesso" | "erro"

**Exemplo:**
\`\`\`json
{
  "resultado": "processado",
  "status": "sucesso"
}
\`\`\`

## Como Usar

1. **Básico:**
   ```
   Use este skill quando você precisar [fazer algo]
   ```

2. **Customizações:**
   Para adaptar para um cliente, modifique `config.json`

3. **Limitações:**
   - Limitação 1
   - Limitação 2

## Histórico de Versões

### v1.0.0 (2026-09-19)
- Versão inicial
```

## Passo 3: Crie config.json

```json
{
  "name": "seu-skill",
  "version": "1.0.0",
  "description": "Breve descrição",
  "author": "Seu Nome",
  "created_at": "2026-09-19",
  "updated_at": "2026-09-19",
  
  "model": "claude-opus-5",
  "temperature": 0.3,
  
  "inputs": {
    "formats": ["json"],
    "max_file_size_mb": 10,
    "encoding": "utf-8"
  },
  
  "outputs": {
    "format": "json",
    "compression": false
  },
  
  "performance": {
    "avg_response_time_seconds": 5,
    "error_rate_percent": 0
  },
  
  "tags": ["contabilidade", "processamento"]
}
```

## Passo 4: Crie prompts.md

```markdown
# Prompts - Seu Skill

## System Prompt
Você é um especialista em [domínio específico]. 

Seu trabalho é:
1. Analisar dados fornecidos
2. Aplicar regras de negócio
3. Retornar resultados estruturados

Sempre retorne JSON válido.

## Regras Importantes
- Regra 1
- Regra 2
- Regra 3

## Exemplos

### Exemplo 1
**Entrada:**
\`\`\`json
{
  "campo": "valor"
}
\`\`\`

**Saída Esperada:**
\`\`\`json
{
  "resultado": "processado",
  "status": "sucesso"
}
\`\`\`

### Exemplo 2
**Entrada:**
\`\`\`json
{
  "campo": "valor2"
}
\`\`\`

**Saída Esperada:**
\`\`\`json
{
  "resultado": "processado",
  "status": "sucesso"
}
\`\`\`

## Tratamento de Erros
- Se [condição], retorne: {"status": "erro", "message": "..."}
- Se [condição], retorne: {"status": "erro", "message": "..."}

## Edge Cases
- Valores nulos: [descrição]
- Dados vazios: [descrição]
- Valores fora do range: [descrição]
```

## Passo 5: Crie Exemplos

**examples/input/exemplo1.json:**
```json
{
  "campo1": "valor1",
  "campo2": 123
}
```

**examples/output/exemplo1.json:**
```json
{
  "resultado": "processado",
  "status": "sucesso"
}
```

## Passo 6: Crie Testes

**tests/test-data.json:**
```json
{
  "test_cases": [
    {
      "name": "Caso de Teste 1",
      "description": "Teste com dados válidos",
      "input": {
        "campo1": "valor1"
      },
      "expected_output": {
        "status": "sucesso"
      }
    },
    {
      "name": "Caso de Teste 2",
      "description": "Teste com dados inválidos",
      "input": {
        "campo1": null
      },
      "expected_output": {
        "status": "erro",
        "message": "Campo obrigatório ausente"
      }
    }
  ]
}
```

## Passo 7: Documente Decisões

Crie `.decisions`:
```
# Decisões Arquiteturais

## Escolha 1: Por que usar [tecnologia]?
- Razão 1
- Razão 2
- Trade-off: X vs Y

## Escolha 2: ...
```

## Checklist Final

- [ ] README completo
- [ ] config.json validado
- [ ] prompts.md com exemplos reais
- [ ] Pasta examples/ com input/output
- [ ] tests/test-data.json preenchido
- [ ] .decisions documentado
- [ ] Testado manualmente
- [ ] Pronto para usar

---

**Template Version:** 1.0.0
**Last Updated:** 2026-09-19
