# Teste de Carga com Locust - Amazon.com

Este projeto contém um teste de carga para a Amazon.com utilizando o Locust.

## 📋 Pré-requisitos

```bash
uv add locust
```

## 🚀 Como executar

### Modo Interface Web (Recomendado)

```bash
uv run locust
```

Depois acesse: http://localhost:8089

Configure:

- **Number of users**: quantidade de usuários simultâneos (ex: 10, 50, 100)
- **Spawn rate**: taxa de criação de usuários por segundo (ex: 1, 5, 10)
- **Host**: já está configurado como https://www.amazon.com

### Modo Headless (Linha de Comando)

```bash
uv run locust --headless --users 10 --spawn-rate 1 -t 1m
```

Parâmetros:

- `--users`: número de usuários simultâneos
- `--spawn-rate`: taxa de criação de usuários por segundo
- `-t`: duração do teste (ex: 1m, 5m, 1h)

## 📊 Tarefas Simuladas

O teste simula um usuário navegando na Amazon com as seguintes ações:

1. **Visualizar Homepage** (peso 3) - Acessa a página inicial
2. **Buscar Produtos** (peso 2) - Realiza buscas por diferentes termos
3. **Ver Mais Vendidos** (peso 1) - Acessa a página de best sellers
4. **Ver Ofertas** (peso 1) - Acessa a página de ofertas

Os pesos indicam a frequência relativa de cada tarefa.

## 📈 Métricas Coletadas

O Locust irá coletar:

- Número de requisições por segundo (RPS)
- Tempo de resposta (mínimo, máximo, médio, mediana)
- Taxa de falhas
- Número de usuários ativos
- Distribuição de tempos de resposta

## ⚠️ Notas Importantes

- Este teste é apenas para fins educacionais
- Não execute testes de carga muito agressivos contra sites de terceiros
- A Amazon pode bloquear requisições excessivas
- Use com moderação e responsabilidade

## 📝 Personalização

Para modificar o teste:

- Ajuste os `wait_time` para mudar o intervalo entre requisições
- Modifique os pesos das `@task` para alterar a frequência
- Adicione novas tarefas conforme necessário
