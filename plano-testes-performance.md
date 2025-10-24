# Plano de Testes de Performance - Locust

## Sistema Sob Teste (SUT)
- **Nome da Aplicação**: _[Preencher]_
- **Versão**: _[Preencher]_
- **Ambiente**: _[Preencher: Produção/Staging/Desenvolvimento]_
- **Data dos Testes**: _[Preencher]_
- **Responsável**: _[Preencher]_

---

## 1. Teste de Carga (Load Test)

### 1.1 Objetivo
Validar que o sistema suporta a carga esperada em condições normais de operação e medir o comportamento sob demanda típica.

### 1.2 Configuração do Teste

```bash
locust -f locustfile.py -u 300 --spawn-rate 20 --run-time 20m --headless -c 4
```

**Parâmetros:**
- Usuários simultâneos: 300
- Taxa de spawn: 20 usuários/seg
- Duração: 20 minutos
- Processos paralelos: 4
- Think time: 1-3 segundos

### 1.3 Critérios de Aceitação

| Critério                      | Meta          | Resultado | Status |
| ----------------------------- | ------------- | --------- | ------ |
| Response time médio           | < 1s          | _[ms]_    | ⬜      |
| Response time p95             | < 2s          | _[ms]_    | ⬜      |
| Response time p99             | < 3s          | _[ms]_    | ⬜      |
| Taxa de erro                  | < 0.1%        | _%_       | ⬜      |
| CPU média                     | < 70%         | _%_       | ⬜      |
| Memória média                 | < 80%         | _%_       | ⬜      |
| Estabilidade (desvio padrão)  | < 500ms       | _[ms]_    | ⬜      |
| Requisições por segundo (RPS) | > _[definir]_ | _[RPS]_   | ⬜      |

**Legenda Status:**
- ✅ = Aprovado
- ❌ = Reprovado
- ⚠️ = Aprovado com ressalvas
- ⬜ = Não executado

### 1.4 Métricas Principais

**Response Time:**
- Mínimo: _[ms]_
- Médio: _[ms]_
- Máximo: _[ms]_
- Mediana (p50): _[ms]_
- p95: _[ms]_
- p99: _[ms]_

**Taxa de Requisições:**
- Total de requisições: _[número]_
- Requisições bem-sucedidas: _[número]_
- Requisições com falha: _[número]_
- Taxa de falha: _[%]_
- RPS médio: _[req/s]_
- RPS pico: _[req/s]_

**Recursos do Sistema:**
- CPU média: _[%]_
- CPU pico: _[%]_
- Memória média: _[MB / %]_
- Memória pico: _[MB / %]_
- I/O disco: _[MB/s]_
- Rede entrada: _[MB/s]_
- Rede saída: _[MB/s]_

**Banco de Dados:**
- Conexões ativas: _[número]_
- Tempo médio de query: _[ms]_
- Queries por segundo: _[número]_
- Pool de conexões: _[usado/total]_

### 1.5 Padrão de Conexão Observado
_[Descrever se a conexão foi estável e consistente durante todo o teste]_

### 1.6 Resultado Final

**Status Geral: ⬜**

**SUT atendeu aos critérios?**
- ⬜ SIM - Sistema aprovado para carga esperada
- ⬜ NÃO - Sistema apresentou problemas (descrever abaixo)
- ⬜ PARCIAL - Alguns critérios não atendidos (descrever abaixo)

**Observações:**
_[Preencher com observações, problemas encontrados, gargalos identificados]_

**Recomendações:**
_[Preencher com sugestões de otimização ou melhorias]_

---

## 2. Teste de Stress (Stress Test)

### 2.1 Objetivo
Encontrar o limite máximo do sistema e entender como ele se comporta sob carga extrema, identificando o ponto de degradação e falha.

### 2.2 Configuração do Teste

```bash
locust -f locustfile.py -u 2000 --spawn-rate 100 --run-time 30m --headless -c 8
```

**Parâmetros:**
- Usuários simultâneos: 2000
- Taxa de spawn: 100 usuários/seg
- Duração: 30 minutos
- Processos paralelos: 8
- Think time: 0-1 segundo

### 2.3 Critérios de Aceitação

| Critério                           | Meta        | Resultado   | Status |
| ---------------------------------- | ----------- | ----------- | ------ |
| Response time sob carga moderada   | < 5s        | _[ms]_      | ⬜      |
| Response time no limite            | < 10s       | _[ms]_      | ⬜      |
| CPU máxima                         | < 90%       | _%_         | ⬜      |
| Memória máxima                     | < 95%       | _%_         | ⬜      |
| Sistema não trava/crash            | Sim         | _[S/N]_     | ⬜      |
| Ponto de falha identificado        | Sim         | _[usuários]_| ⬜      |
| Degradação é gradual (não abrupta) | Sim         | _[S/N]_     | ⬜      |
| Mensagens de erro adequadas        | Sim         | _[S/N]_     | ⬜      |

### 2.4 Métricas Principais

**Response Time por Fase:**
- Fase 1 (0-500 usuários):
  - Médio: _[ms]_
  - p95: _[ms]_
- Fase 2 (500-1000 usuários):
  - Médio: _[ms]_
  - p95: _[ms]_
- Fase 3 (1000-1500 usuários):
  - Médio: _[ms]_
  - p95: _[ms]_
- Fase 4 (1500-2000 usuários):
  - Médio: _[ms]_
  - p95: _[ms]_

**Taxa de Erro por Fase:**
- Fase 1 (0-500 usuários): _[%]_
- Fase 2 (500-1000 usuários): _[%]_
- Fase 3 (1000-1500 usuários): _[%]_
- Fase 4 (1500-2000 usuários): _[%]_

**Ponto de Degradação:**
- Número de usuários quando response time > 5s: _[usuários]_
- Número de usuários quando taxa erro > 1%: _[usuários]_
- Número de usuários quando taxa erro > 5%: _[usuários]_
- Número de usuários quando sistema falha: _[usuários]_

**Recursos Críticos:**
- Recurso mais saturado: _[CPU/Memória/Disco/Rede/BD]_
- Momento da saturação: _[minuto do teste / número de usuários]_
- Valor no momento da saturação: _[%/valor]_

**Tipos de Erro Observados:**
1. _[Código/tipo de erro]_: _[quantidade]_ ocorrências
2. _[Código/tipo de erro]_: _[quantidade]_ ocorrências
3. _[Código/tipo de erro]_: _[quantidade]_ ocorrências

### 2.5 Padrão de Conexão Observado
_[Descrever como foi o aumento gradual até a falha - linear, exponencial, etc.]_

### 2.6 Análise de Degradação

**Comportamento do Sistema:**
_[Descrever se a degradação foi linear ou abrupta, se o sistema se recuperou após redução de carga, etc.]_

**Gargalos Identificados:**
1. _[Recurso/componente]_: _[descrição do gargalo]_
2. _[Recurso/componente]_: _[descrição do gargalo]_
3. _[Recurso/componente]_: _[descrição do gargalo]_

### 2.7 Resultado Final

**Status Geral: ⬜**

**SUT atendeu aos critérios?**
- ⬜ SIM - Limites identificados e comportamento aceitável
- ⬜ NÃO - Sistema falhou prematuramente ou comportamento inadequado
- ⬜ PARCIAL - Alguns critérios não atendidos (descrever abaixo)

**Limite máximo recomendado:** _[número de usuários simultâneos]_

**Observações:**
_[Preencher com observações sobre o comportamento sob stress]_

**Recomendações:**
_[Preencher com sugestões para aumentar capacidade ou melhorar degradação]_

---

## 3. Teste de Pico (Spike Test)

### 3.1 Objetivo
Simular aumento repentino de carga e validar a capacidade de recuperação do sistema, testando elasticidade e resiliência.

### 3.2 Configuração do Teste

```bash
locust -f locustfile.py -u 500 --spawn-rate 150 --run-time 25m --headless -c 6
```

**Parâmetros:**
- Usuários base: 100-300
- Usuários pico: 1500-3000
- Taxa de spawn durante pico: 150 usuários/seg
- Duração: 25 minutos (5 min base + 15 min pico + 5 min recovery)
- Processos paralelos: 6
- Think time: 0.5-2 segundos

**Estrutura do Teste:**
- **0-5 min**: Carga base (100-300 usuários)
- **5-6 min**: Escalada rápida para pico (1500-3000 usuários)
- **6-20 min**: Manutenção do pico
- **20-21 min**: Redução rápida para carga base
- **21-25 min**: Observação da recuperação

### 3.3 Critérios de Aceitação

| Critério                          | Meta      | Resultado | Status |
| --------------------------------- | --------- | --------- | ------ |
| Response time na carga base       | < 2s      | _[ms]_    | ⬜      |
| Response time durante pico        | < 5s      | _[ms]_    | ⬜      |
| Taxa de erro durante pico         | < 1%      | _%_       | ⬜      |
| Taxa de erro na escalada          | < 5%      | _%_       | ⬜      |
| Tempo de recuperação              | < 2-5 min | _[min]_   | ⬜      |
| Sistema não trava                 | Sim       | _[S/N]_   | ⬜      |
| Retorna ao baseline após pico     | Sim       | _[S/N]_   | ⬜      |
| Auto-scaling funciona (se aplicável)| Sim     | _[S/N]_   | ⬜      |

### 3.4 Métricas Principais

**Response Time por Fase:**
- Carga base (0-5 min):
  - Médio: _[ms]_
  - p95: _[ms]_
- Escalada (5-6 min):
  - Médio: _[ms]_
  - p95: _[ms]_
  - Máximo: _[ms]_
- Pico (6-20 min):
  - Médio: _[ms]_
  - p95: _[ms]_
  - Desvio padrão: _[ms]_
- Redução (20-21 min):
  - Médio: _[ms]_
  - p95: _[ms]_
- Recuperação (21-25 min):
  - Médio: _[ms]_
  - p95: _[ms]_

**Taxa de Erro por Fase:**
- Carga base (0-5 min): _[%]_
- Escalada (5-6 min): _[%]_
- Pico (6-20 min): _[%]_
- Redução (20-21 min): _[%]_
- Recuperação (21-25 min): _[%]_

**Tempo de Recuperação:**
- Tempo até response time voltar ao baseline: _[min:seg]_
- Tempo até taxa de erro voltar ao baseline: _[min:seg]_
- Tempo até recursos do sistema normalizarem: _[min:seg]_

**Auto-scaling (se aplicável):**
- Instâncias antes do pico: _[número]_
- Instâncias durante o pico: _[número]_
- Tempo para escalar: _[min:seg]_
- Tempo para desescalar: _[min:seg]_

**Cache e Rate Limiting:**
- Taxa de cache hit durante pico: _[%]_
- Requisições bloqueadas por rate limiting: _[número / %]_
- Efetividade de cache: _[descrever]_

### 3.5 Padrão de Conexão Observado
_[Descrever como foi a escalada rápida e a estabilização durante e após o pico]_

### 3.6 Análise de Comportamento

**Durante a Escalada:**
_[Descrever o comportamento do sistema durante o aumento repentino de carga]_

**Durante o Pico:**
_[Descrever a estabilidade e comportamento durante a manutenção do pico]_

**Durante a Recuperação:**
_[Descrever como o sistema se recuperou após a redução da carga]_

**Problemas Identificados:**
1. _[Problema]_: _[descrição e momento de ocorrência]_
2. _[Problema]_: _[descrição e momento de ocorrência]_
3. _[Problema]_: _[descrição e momento de ocorrência]_

### 3.7 Resultado Final

**Status Geral: ⬜**

**SUT atendeu aos critérios?**
- ⬜ SIM - Sistema demonstrou resiliência adequada
- ⬜ NÃO - Sistema não se recuperou ou apresentou falhas graves
- ⬜ PARCIAL - Alguns critérios não atendidos (descrever abaixo)

**Observações:**
_[Preencher com observações sobre o comportamento durante pico e recuperação]_

**Recomendações:**
_[Preencher com sugestões para melhorar resiliência e recuperação]_

---

## 4. Resumo Executivo

### 4.1 Visão Geral dos Resultados

| Tipo de Teste   | Status | Principais Achados                     |
| --------------- | ------ | -------------------------------------- |
| Teste de Carga  | ⬜      | _[Resumo em 1-2 linhas]_               |
| Teste de Stress | ⬜      | _[Resumo em 1-2 linhas]_               |
| Teste de Pico   | ⬜      | _[Resumo em 1-2 linhas]_               |

### 4.2 Capacidade do Sistema

**Capacidade Recomendada:**
- Usuários simultâneos em operação normal: _[número]_
- Limite máximo antes de degradação: _[número]_
- Margem de segurança recomendada: _[%]_

**Principais Gargalos:**
1. _[Recurso/componente]_: _[descrição]_
2. _[Recurso/componente]_: _[descrição]_
3. _[Recurso/componente]_: _[descrição]_

### 4.3 Pontos Fortes Identificados
1. _[Ponto forte 1]_
2. _[Ponto forte 2]_
3. _[Ponto forte 3]_

### 4.4 Pontos de Melhoria Prioritários
1. **[CRÍTICO/ALTO/MÉDIO/BAIXO]** _[Problema]_
   - Impacto: _[descrição]_
   - Recomendação: _[ação sugerida]_

2. **[CRÍTICO/ALTO/MÉDIO/BAIXO]** _[Problema]_
   - Impacto: _[descrição]_
   - Recomendação: _[ação sugerida]_

3. **[CRÍTICO/ALTO/MÉDIO/BAIXO]** _[Problema]_
   - Impacto: _[descrição]_
   - Recomendação: _[ação sugerida]_

### 4.5 Próximos Passos
1. _[Ação recomendada 1]_
2. _[Ação recomendada 2]_
3. _[Ação recomendada 3]_

### 4.6 Conclusão Final

**O sistema está pronto para produção?**
- ⬜ SIM - Todos os critérios atendidos
- ⬜ SIM COM RESSALVAS - Aprovado com monitoramento próximo
- ⬜ NÃO - Requer melhorias antes de produção

**Justificativa:**
_[Preencher com justificativa detalhada da conclusão]_

---

## 5. Anexos

### 5.1 Configuração do Ambiente de Teste

**Sistema Sob Teste:**
- SO: _[Sistema Operacional]_
- CPU: _[Cores/Modelo]_
- Memória: _[GB]_
- Disco: _[Tipo/Capacidade]_
- Rede: _[Velocidade]_

**Máquina de Teste (Locust):**
- SO: _[Sistema Operacional]_
- CPU: _[Cores/Modelo]_
- Memória: _[GB]_
- Versão do Locust: _[versão]_
- Versão do Python: _[versão]_

**Banco de Dados:**
- Tipo: _[MySQL/PostgreSQL/etc]_
- Versão: _[versão]_
- Configuração: _[descrição]_
- Tamanho da base: _[GB/número de registros]_

**Load Balancer/CDN (se aplicável):**
- Tipo: _[tipo]_
- Configuração: _[descrição]_

### 5.2 Arquivos de Log
_[Listar caminhos dos arquivos de log gerados]_
- Locust reports: _[caminho]_
- Application logs: _[caminho]_
- System logs: _[caminho]_
- Database logs: _[caminho]_

### 5.3 Gráficos e Evidências
_[Listar capturas de tela, gráficos e outras evidências visuais]_
- Dashboard Locust: _[arquivo/link]_
- Monitoramento de recursos: _[arquivo/link]_
- Gráficos de response time: _[arquivo/link]_
- Gráficos de taxa de erro: _[arquivo/link]_

### 5.4 Locustfile Utilizado
```python
# Cole aqui o conteúdo do locustfile.py utilizado nos testes
```

---

**Documento gerado em:** _[Data]_
**Versão:** 1.0
**Próxima revisão:** _[Data]_
