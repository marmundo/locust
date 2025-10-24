# 📊 Parâmetros Locust para Testes de Performance

Guia completo de configuração para diferentes tipos de testes de carga, stress e pico.

---

## 1. Parâmetros Principais por Tipo de Teste

| Tipo de Teste       | Objetivo                               | Usuários (users)                   | Taxa de Spawn (spawn_rate) | Duração (run_time)       | Think Time     |
| ------------------- | -------------------------------------- | ---------------------------------- | -------------------------- | ------------------------ | -------------- |
| **Teste de Carga**  | Medir comportamento com carga esperada | 100-500 usuários                   | 10-50 usuários/seg         | 15-30 minutos            | 1-3 segundos   |
| **Teste de Stress** | Encontrar limite máximo do sistema     | 500-5000+ usuários                 | 50-200 usuários/seg        | 20-45 minutos            | 0-1 segundo    |
| **Teste de Pico**   | Simular aumento repentino de carga     | Normal: 100-300<br>Pico: 1000-3000 | 100-500 usuários/seg       | 5-10 min + pico 5-15 min | 0.5-2 segundos |

---

## 2. Critérios de Aceitação e Métricas

| Tipo de Teste       | Critérios de Aceitação                                                   | Métrica Principal         | Padrão de Conexão               |
| ------------------- | ------------------------------------------------------------------------ | ------------------------- | ------------------------------- |
| **Teste de Carga**  | • Response time: < 1-2s<br>• Taxa de erro: < 0.1%<br>• CPU: < 70%        | Tempo de resposta médio   | Estável e consistente           |
| **Teste de Stress** | • Identificar ponto de falha<br>• Response time: < 5-10s<br>• CPU: < 90% | Taxa de erro e degradação | Aumento gradual até falha       |
| **Teste de Pico**   | • Recovery time: < 2-5 min<br>• Sem travamentos<br>• Taxa de erro: < 1%  | Tempo de recuperação      | Escalada rápida e estabilização |

---

## 3. Exemplos de Comando Locust

### Teste de Carga

```bash
locust -f locustfile.py -u 300 --spawn-rate 20 --run-time 20m --headless -c 4
```

- Simula 300 usuários simultâneos
- Adiciona 20 usuários por segundo
- Executa por 20 minutos
- Usa 4 processos paralelos

### Teste de Stress

```bash
locust -f locustfile.py -u 2000 --spawn-rate 100 --run-time 30m --headless -c 8
```

- Simula 2000 usuários simultâneos
- Adiciona 100 usuários por segundo
- Executa por 30 minutos
- Usa 8 processos paralelos

### Teste de Pico

```bash
locust -f locustfile.py -u 500 --spawn-rate 150 --run-time 25m --headless -c 6
```

- Simula 500 usuários base + escala até 1500-3000
- Adiciona 150 usuários por segundo durante pico
- Executa por 25 minutos totais
- Usa 6 processos paralelos

---

## 4. Glossário de Parâmetros

### Usuários (users)

Número total de usuários simultâneos simulados. Comece com valores conservadores e aumente progressivamente até encontrar gargalos.

### Taxa de Spawn (spawn_rate)

Quantos usuários por segundo são adicionados ao teste. Valores menores criam um aumento mais gradual da carga, valores maiores simulam picos repentinos.

### Duração (run_time)

Tempo total do teste. Deve ser suficiente para estabilizar métricas iniciais e coletar dados significativos. Recomenda-se aguardar 2-3 minutos iniciais antes de analisar resultados.

### Think Time

Tempo de espera entre requisições sucessivas. Simula o tempo que um usuário real leva navegando e lendo conteúdo antes de fazer a próxima ação.

### -c (cores)

Número de processos paralelos que o Locust usará. Recomendação: 1-2 processos por CPU disponível para melhor distribuição de carga.

### --headless

Executa o teste sem interface gráfica web. Ideal para automação, CI/CD pipelines e execução em servidores sem GUI.

---

## 5. Detalhamento por Tipo de Teste

### 🔵 Teste de Carga (Load Test)

**Quando usar:** Em ambientes de produção estáveis ou pré-produção quando você conhece a carga esperada normal.

**Configuração:**

- Usuários: 100-500 (ou baseado no número real esperado)
- Spawn Rate: 10-50 usuários/seg (gradual)
- Duração: 15-30 minutos
- Think Time: 1-3 segundos (realista)

**Objetivos:**

- Validar que o sistema suporta a carga esperada
- Medir tempos de resposta em condições normais
- Identificar gargalos antes de críticos
- Estabelecer baseline de performance

**Métricas a monitorar:**

- Response time médio e percentis (p95, p99)
- Taxa de erro/falha
- Taxa de requisições por segundo
- Uso de CPU, memória e I/O

---

### 🟠 Teste de Stress (Stress Test)

**Quando usar:** Para descobrir os limites da aplicação e entender como ela degrada sob carga extrema.

**Configuração:**

- Usuários: 500-5000+ (aumento contínuo)
- Spawn Rate: 50-200 usuários/seg (rápido)
- Duração: 20-45 minutos
- Think Time: 0-1 segundo (sem delays)

**Objetivos:**

- Encontrar o ponto de falha do sistema
- Entender como a aplicação se comporta sob stress
- Identificar limites de recursos
- Validar tratamento de erros e timeouts

**Métricas a monitorar:**

- Quando começa a degradação
- Ponto exato de falha/crash
- Taxa de aumento de erros
- Tempos de resposta máximos
- Recursos mais críticos (CPU, memória, conexões BD)

---

### 🔴 Teste de Pico (Spike Test)

**Quando usar:** Para simular eventos de pico repentino (Black Friday, lançamento de produto, evento viral).

**Configuração:**

- Usuários base: 100-300
- Usuários pico: 1000-3000
- Spawn Rate: 100-500 usuários/seg (muito rápido)
- Duração total: 5-10 min base + 5-15 min pico
- Think Time: 0.5-2 segundos

**Objetivos:**

- Simular aumento repentino de carga
- Validar tempo de recuperação
- Testar auto-scaling e load balancers
- Garantir que o sistema se recupera sem travamentos

**Métricas a monitorar:**

- Tempo de resposta durante pico
- Taxa de erro durante transição
- Tempo para recuperar valores normais
- Comportamento de cache
- Efetividade de rate limiting

---

## 6. Dicas de Boas Práticas

### ✅ Planejamento

- Comece com testes de carga antes de stress e pico
- Execute em ambiente isolado sem outras aplicações
- Estabeleça métricas baseline antes de otimizações
- Documente configurações e resultados para comparação

### ✅ Execução

- Aguarde 2-3 minutos iniciais para estabilização antes de analisar
- Repita cada teste 2-3 vezes para validar consistência dos resultados
- Monitore sistema alvo durante toda a execução (CPU, memória, disco, rede)
- Acompanhe logs de aplicação para erros específicos

### ✅ Análise

- Compare resultados com execuções anteriores
- Identifique tendências (degradação linear vs exponencial)
- Corrija gargalos encontrados
- Re-execute após otimizações para validar melhoria

### ✅ Infraestrutura

- Use máquinas com recursos adequados para gerar carga
- Distribua Locust em múltiplas máquinas para testes maiores
- Configure network adequadamente (considere latência)
- Teste em ambiente que simule produção

---

## 7. Exemplo de Locustfile Básico

```python
from locust import HttpUser, task, between
import random

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)  # Think time

    @task
    def index(self):
        self.client.get("/")

    @task(3)
    def product_page(self):
        product_id = random.randint(1, 100)
        self.client.get(f"/products/{product_id}")

    @task(2)
    def about(self):
        self.client.get("/about")

    def on_start(self):
        # Executado quando um usuário inicia
        pass

    def on_stop(self):
        # Executado quando um usuário para
        pass
```

---

## 8. Matriz de Decisão

| Pergunta                         | Teste de Carga      | Teste de Stress         | Teste de Pico            |
| -------------------------------- | ------------------- | ----------------------- | ------------------------ |
| Qual é a carga esperada?         | Sim, use esse valor | Aumente acima disso     | Use valor normal + pico  |
| Preciso encontrar o limite?      | Não                 | Sim, objetivo principal | Não, validar recuperação |
| Devo manter think time realista? | Sim                 | Não, minimize           | Parcialmente             |
| Duração deve ser longa?          | Sim, 15-30 min      | Sim, 20-45 min          | Não, 20-25 min no total  |
| Spawn rate deve ser rápido?      | Não                 | Sim                     | Sim                      |

---

## 9. Interpretação de Resultados

### Teste de Carga bem-sucedido

- ✅ Response time < 2s em p95
- ✅ Taxa de erro < 0.1%
- ✅ Estabilidade ao longo do tempo
- ✅ CPU < 70%, memória < 80%

### Teste de Stress revelando problemas

- ⚠️ Response time > 5s
- ⚠️ Taxa de erro aumentando gradualmente
- ⚠️ Identifica ponto exato de falha
- ⚠️ Mostra qual recurso é gargalo

### Teste de Pico bem-sucedido

- ✅ Tempo de recuperação < 5 min
- ✅ Taxa de erro durante pico < 1%
- ✅ Sem deadlocks ou travamentos
- ✅ Retorna a baseline após pico

---

## 10. Checklist pré-teste

- [ ] Ambiente de teste isolado e limpo
- [ ] Aplicação em estado conhecido e previsível
- [ ] Database com dados realistas
- [ ] Network simulando latência real
- [ ] Monitoramento ativado (Prometheus, CloudWatch, etc)
- [ ] Logs de aplicação disponíveis
- [ ] Caches limpos/resetados
- [ ] Locust atualizado para versão estável
- [ ] Locustfile testado e validado
- [ ] Documentação de configuração pronta
