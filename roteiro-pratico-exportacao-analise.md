# 🎯 Roteiro Prático: Exportação e Análise de Dados Locust

## Informações do Roteiro
- **Disciplina**: Avaliação de Desempenho de Sistemas
- **Objetivo**: Aprender a exportar, analisar e interpretar resultados de testes de performance
- **Duração estimada**: 3-4 horas
- **Pré-requisitos**:
  - Python 3.8+
  - Locust instalado
  - Conhecimento básico de pandas
  - Ter completado testes básicos com Locust

---

## 📋 Parte 1: Exportação Básica de Dados (30 min)

### Exercício 1.1: Exportação via Interface Web

**Objetivo**: Aprender a exportar dados através da interface gráfica do Locust.

**Passos:**

1. Crie um locustfile simples (`locustfile_basico.py`):

```python
from locust import HttpUser, task, between

class UsuarioBasico(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def pagina_inicial(self):
        self.client.get("/")

    @task(2)
    def sobre(self):
        self.client.get("/about")

    @task(1)
    def contato(self):
        self.client.get("/contact")
```

2. Execute o Locust com interface web:

```bash
locust -f locustfile_basico.py --host=https://httpbin.org
```

3. Acesse `http://localhost:8089`

4. Configure o teste:
   - Usuários: 50
   - Spawn rate: 10
   - Execute por 3 minutos

5. Após o teste, clique em "Download Data" e baixe todos os arquivos disponíveis

**Resultado esperado:**
- `stats.csv`
- `stats_history.csv`
- `failures.csv`
- `report_*.html`

**Questões para reflexão:**
1. Quantas requisições foram feitas no total?
2. Qual endpoint teve o maior tempo de resposta médio?
3. Houve alguma falha durante o teste?

---

### Exercício 1.2: Exportação via CLI (Headless)

**Objetivo**: Automatizar a exportação de dados sem interface gráfica.

**Passos:**

1. Crie uma pasta para organizar os resultados:

```bash
mkdir -p resultados/teste_$(date +%Y%m%d_%H%M%S)
```

2. Execute o Locust em modo headless com exportação automática:

```bash
locust -f locustfile_basico.py \
  --host=https://httpbin.org \
  -u 100 \
  --spawn-rate 20 \
  --run-time 5m \
  --headless \
  --csv=resultados/teste_cli \
  --html=resultados/teste_cli.html \
  --loglevel=INFO
```

3. Verifique os arquivos gerados:

```bash
ls -lh resultados/
```

**Resultado esperado:**
- Múltiplos arquivos CSV com prefixo `teste_cli_`
- Arquivo HTML `teste_cli.html`
- Teste executado sem interação manual

**Questões para reflexão:**
1. Qual a vantagem de usar o modo headless?
2. Em que situações você usaria cada método (web vs CLI)?

---

## 📊 Parte 2: Análise Básica com Pandas (45 min)

### Exercício 2.1: Leitura e Inspeção de Dados

**Objetivo**: Carregar e entender a estrutura dos dados exportados.

Crie um script `analise_basica.py`:

```python
import pandas as pd
import numpy as np

# Carregar dados
print("=" * 80)
print("ANÁLISE BÁSICA DE DADOS LOCUST")
print("=" * 80)

# 1. Carregar stats.csv
stats_df = pd.read_csv('resultados/teste_cli_stats.csv')

print("\n📁 Estrutura do DataFrame (stats.csv):")
print(stats_df.info())

print("\n📋 Primeiras linhas:")
print(stats_df.head())

print("\n📊 Estatísticas descritivas:")
print(stats_df.describe())

# 2. Análise de colunas importantes
print("\n🔍 Colunas disponíveis:")
for col in stats_df.columns:
    print(f"  - {col}")

# 3. Verificar valores ausentes
print("\n⚠️  Valores ausentes por coluna:")
print(stats_df.isnull().sum())
```

**Execute:**

```bash
python analise_basica.py
```

**Tarefa:**
Identifique e anote:
1. Quantas colunas existem no DataFrame?
2. Quais colunas contêm informações de tempo de resposta?
3. Como as falhas são representadas?

---

### Exercício 2.2: Cálculo de Métricas Principais

**Objetivo**: Calcular e interpretar métricas de performance.

Adicione ao seu script `analise_basica.py`:

```python
# 4. Métricas principais
print("\n" + "=" * 80)
print("MÉTRICAS PRINCIPAIS")
print("=" * 80)

# Total de requisições
total_requisicoes = stats_df['Request Count'].sum()
print(f"\n📈 Total de requisições: {total_requisicoes:,}")

# Total de falhas
total_falhas = stats_df['Failure Count'].sum()
print(f"❌ Total de falhas: {total_falhas:,}")

# Taxa de erro
taxa_erro = (total_falhas / total_requisicoes * 100) if total_requisicoes > 0 else 0
print(f"📊 Taxa de erro geral: {taxa_erro:.2f}%")

# Tempo de resposta médio
tempo_medio_geral = stats_df['Average Response Time'].mean()
print(f"⏱️  Tempo de resposta médio: {tempo_medio_geral:.2f}ms")

# P95 e P99
p95_geral = stats_df['95%'].mean()
p99_geral = stats_df['99%'].mean()
print(f"📊 P95 médio: {p95_geral:.2f}ms")
print(f"📊 P99 médio: {p99_geral:.2f}ms")

# 5. Análise por endpoint
print("\n" + "=" * 80)
print("ANÁLISE POR ENDPOINT")
print("=" * 80)

for idx, row in stats_df.iterrows():
    if row['Name'] != 'Aggregated':
        taxa_erro_endpoint = (row['Failure Count'] / row['Request Count'] * 100) if row['Request Count'] > 0 else 0

        print(f"\n🔹 {row['Name']}")
        print(f"   Requisições: {row['Request Count']:,}")
        print(f"   Falhas: {row['Failure Count']:,}")
        print(f"   Taxa de erro: {taxa_erro_endpoint:.2f}%")
        print(f"   Tempo médio: {row['Average Response Time']:.2f}ms")
        print(f"   P50 (mediana): {row['50%']:.2f}ms")
        print(f"   P95: {row['95%']:.2f}ms")
        print(f"   P99: {row['99%']:.2f}ms")
        print(f"   Min: {row['Min Response Time']:.2f}ms")
        print(f"   Max: {row['Max Response Time']:.2f}ms")
```

**Tarefa de análise:**
Responda com base nos resultados:
1. Qual endpoint teve o melhor desempenho? Por quê?
2. Qual endpoint teve o pior desempenho? Por quê?
3. A taxa de erro está dentro do aceitável (< 0.1%)?
4. Há grande diferença entre P50 e P99? O que isso indica?

---

### Exercício 2.3: Análise de Evolução Temporal

**Objetivo**: Entender como as métricas evoluíram durante o teste.

Crie um novo script `analise_temporal.py`:

```python
import pandas as pd
import matplotlib.pyplot as plt

# Carregar histórico
history_df = pd.read_csv('resultados/teste_cli_stats_history.csv')

print("=" * 80)
print("ANÁLISE TEMPORAL")
print("=" * 80)

# Converter timestamp
history_df['Timestamp'] = pd.to_datetime(history_df['Timestamp'], unit='s')

print(f"\n📅 Início do teste: {history_df['Timestamp'].min()}")
print(f"📅 Fim do teste: {history_df['Timestamp'].max()}")
print(f"⏱️  Duração total: {history_df['Timestamp'].max() - history_df['Timestamp'].min()}")

# Estatísticas ao longo do tempo
print("\n📊 Evolução das métricas:")
print(history_df[['Timestamp', 'User Count', 'Total Request Count',
                  'Total Average Response Time', 'Total Requests/s']].tail(10))

# Identificar tendências
print("\n📈 Análise de tendências:")
tempo_inicio = history_df['Total Average Response Time'].iloc[:5].mean()
tempo_fim = history_df['Total Average Response Time'].iloc[-5:].mean()
variacao_pct = ((tempo_fim - tempo_inicio) / tempo_inicio * 100)

print(f"   Tempo médio no início: {tempo_inicio:.2f}ms")
print(f"   Tempo médio no fim: {tempo_fim:.2f}ms")
print(f"   Variação: {variacao_pct:+.2f}%")

if variacao_pct > 10:
    print("   ⚠️  ATENÇÃO: Sistema apresentou degradação significativa")
elif variacao_pct < -10:
    print("   ✅ Sistema melhorou performance (possível efeito de cache)")
else:
    print("   ✅ Sistema manteve performance estável")
```

**Execute e analise:**

```bash
python analise_temporal.py
```

**Questões para reflexão:**
1. O sistema manteve performance estável ao longo do teste?
2. Houve degradação? Em que momento?
3. O que pode ter causado variações na performance?

---

## 📈 Parte 3: Visualização de Dados (45 min)

### Exercício 3.1: Gráficos Básicos

**Objetivo**: Criar visualizações para facilitar a interpretação dos dados.

Crie o script `visualizacao_basica.py`:

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurar estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)

# Carregar dados
stats_df = pd.read_csv('resultados/teste_cli_stats.csv')
history_df = pd.read_csv('resultados/teste_cli_stats_history.csv')
history_df['Timestamp'] = pd.to_datetime(history_df['Timestamp'], unit='s')

# Filtrar apenas endpoints (sem total)
endpoints_df = stats_df[stats_df['Name'] != 'Aggregated'].copy()

# Criar figura com 4 subplots
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Análise de Performance - Teste Locust', fontsize=16, fontweight='bold')

# 1. Tempo de Resposta por Endpoint
ax1 = axes[0, 0]
endpoints = endpoints_df['Name'].values
tempos = endpoints_df['Average Response Time'].values
bars = ax1.barh(endpoints, tempos, color='steelblue')
ax1.set_xlabel('Tempo de Resposta Médio (ms)')
ax1.set_title('Tempo de Resposta por Endpoint')
ax1.grid(axis='x', alpha=0.3)

# Adicionar valores nas barras
for i, bar in enumerate(bars):
    width = bar.get_width()
    ax1.text(width, bar.get_y() + bar.get_height()/2,
             f'{width:.0f}ms', ha='left', va='center', fontweight='bold')

# 2. Taxa de Erro por Endpoint
ax2 = axes[0, 1]
endpoints_df['Taxa_Erro'] = (endpoints_df['Failure Count'] /
                             endpoints_df['Request Count'] * 100)
taxa_erro = endpoints_df['Taxa_Erro'].values
colors_erro = ['red' if x > 1 else 'orange' if x > 0.1 else 'green'
               for x in taxa_erro]
bars = ax2.barh(endpoints, taxa_erro, color=colors_erro)
ax2.set_xlabel('Taxa de Erro (%)')
ax2.set_title('Taxa de Erro por Endpoint')
ax2.grid(axis='x', alpha=0.3)

# 3. Evolução do Tempo de Resposta
ax3 = axes[1, 0]
ax3.plot(history_df['Timestamp'], history_df['Total Average Response Time'],
         marker='o', linewidth=2, markersize=3, label='Tempo Médio', color='blue')
ax3.fill_between(history_df['Timestamp'],
                 history_df['Total Average Response Time'],
                 alpha=0.3, color='blue')
ax3.set_xlabel('Tempo')
ax3.set_ylabel('Tempo de Resposta (ms)')
ax3.set_title('Evolução do Tempo de Resposta')
ax3.legend()
ax3.grid(True, alpha=0.3)
plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)

# 4. RPS e Usuários ao Longo do Tempo
ax4 = axes[1, 1]
ax4_twin = ax4.twinx()
line1 = ax4.plot(history_df['Timestamp'], history_df['Total Requests/s'],
                 marker='o', linewidth=2, markersize=3, label='RPS', color='green')
line2 = ax4_twin.plot(history_df['Timestamp'], history_df['User Count'],
                      marker='s', linewidth=2, markersize=3, label='Usuários',
                      color='orange')
ax4.set_xlabel('Tempo')
ax4.set_ylabel('Requisições por Segundo', color='green')
ax4_twin.set_ylabel('Número de Usuários', color='orange')
ax4.set_title('RPS e Usuários Ativos')
ax4.grid(True, alpha=0.3)
plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45)

# Combinar legendas
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax4.legend(lines, labels, loc='upper left')

plt.tight_layout()
plt.savefig('resultados/analise_performance.png', dpi=300, bbox_inches='tight')
print("✅ Gráfico salvo: resultados/analise_performance.png")
plt.show()
```

**Execute:**

```bash
python visualizacao_basica.py
```

**Tarefa:**
Analise os gráficos gerados e responda:
1. Qual padrão você observa na evolução do tempo de resposta?
2. A taxa de RPS foi constante ou variou?
3. Há correlação entre número de usuários e tempo de resposta?

---

### Exercício 3.2: Gráfico de Percentis

**Objetivo**: Visualizar a distribuição de tempos de resposta.

Adicione ao script `visualizacao_basica.py`:

```python
# Gráfico adicional: Distribuição de Percentis
fig2, ax = plt.subplots(figsize=(12, 6))

percentis = ['50%', '66%', '75%', '80%', '90%', '95%', '99%']
x = range(len(endpoints))
width = 0.12

for i, percentil in enumerate(percentis):
    if percentil in endpoints_df.columns:
        valores = endpoints_df[percentil].values
        offset = (i - len(percentis)/2) * width
        ax.bar([p + offset for p in x], valores, width,
               label=f'P{percentil.replace("%", "")}', alpha=0.8)

ax.set_xlabel('Endpoints')
ax.set_ylabel('Tempo de Resposta (ms)')
ax.set_title('Distribuição de Percentis por Endpoint')
ax.set_xticks(x)
ax.set_xticklabels(endpoints, rotation=45, ha='right')
ax.legend()
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('resultados/distribuicao_percentis.png', dpi=300, bbox_inches='tight')
print("✅ Gráfico de percentis salvo: resultados/distribuicao_percentis.png")
plt.show()
```

---

## 🔬 Parte 4: Análise Avançada (60 min)

### Exercício 4.1: Comparação de Múltiplos Testes

**Objetivo**: Comparar resultados de diferentes execuções de teste.

1. Execute 3 testes diferentes:

```bash
# Teste 1: Baixa carga
locust -f locustfile_basico.py --host=https://httpbin.org \
  -u 50 --spawn-rate 10 --run-time 3m --headless \
  --csv=resultados/teste_baixa_carga --html=resultados/teste_baixa_carga.html

# Teste 2: Média carga
locust -f locustfile_basico.py --host=https://httpbin.org \
  -u 150 --spawn-rate 30 --run-time 3m --headless \
  --csv=resultados/teste_media_carga --html=resultados/teste_media_carga.html

# Teste 3: Alta carga
locust -f locustfile_basico.py --host=https://httpbin.org \
  -u 300 --spawn-rate 50 --run-time 3m --headless \
  --csv=resultados/teste_alta_carga --html=resultados/teste_alta_carga.html
```

2. Crie o script `comparacao_testes.py`:

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def carregar_teste(nome, arquivo_csv):
    """Carrega dados de um teste e retorna métricas principais"""
    df = pd.read_csv(arquivo_csv)

    # Filtrar linha agregada
    total_row = df[df['Name'] == 'Aggregated']

    if len(total_row) > 0:
        total_row = total_row.iloc[0]
        return {
            'Nome': nome,
            'Requisições': total_row['Request Count'],
            'Falhas': total_row['Failure Count'],
            'Taxa_Erro_%': (total_row['Failure Count'] / total_row['Request Count'] * 100) if total_row['Request Count'] > 0 else 0,
            'Tempo_Médio_ms': total_row['Average Response Time'],
            'P50_ms': total_row['50%'],
            'P95_ms': total_row['95%'],
            'P99_ms': total_row['99%'],
            'RPS': total_row['Requests/s']
        }
    return None

# Carregar todos os testes
testes = [
    carregar_teste('Baixa Carga (50u)', 'resultados/teste_baixa_carga_stats.csv'),
    carregar_teste('Média Carga (150u)', 'resultados/teste_media_carga_stats.csv'),
    carregar_teste('Alta Carga (300u)', 'resultados/teste_alta_carga_stats.csv')
]

# Criar DataFrame comparativo
df_comparacao = pd.DataFrame(testes)
df_comparacao.set_index('Nome', inplace=True)

print("=" * 80)
print("COMPARAÇÃO ENTRE TESTES")
print("=" * 80)
print(df_comparacao.to_string())
print("\n")

# Análise de impacto da carga
print("=" * 80)
print("ANÁLISE DE IMPACTO DA CARGA")
print("=" * 80)

baixa = df_comparacao.loc['Baixa Carga (50u)']
alta = df_comparacao.loc['Alta Carga (300u)']

print(f"\nAumento de carga: {(alta['Requisições'] / baixa['Requisições']):.1f}x")
print(f"Impacto no tempo médio: {((alta['Tempo_Médio_ms'] - baixa['Tempo_Médio_ms']) / baixa['Tempo_Médio_ms'] * 100):+.1f}%")
print(f"Impacto no P95: {((alta['P95_ms'] - baixa['P95_ms']) / baixa['P95_ms'] * 100):+.1f}%")
print(f"Impacto no P99: {((alta['P99_ms'] - baixa['P99_ms']) / baixa['P99_ms'] * 100):+.1f}%")
print(f"Variação na taxa de erro: {(alta['Taxa_Erro_%'] - baixa['Taxa_Erro_%']):+.2f} pontos percentuais")

# Visualizações
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Comparação de Testes de Carga', fontsize=16, fontweight='bold')

# 1. Tempos de Resposta
ax1 = axes[0, 0]
df_comparacao[['Tempo_Médio_ms', 'P95_ms', 'P99_ms']].plot(kind='bar', ax=ax1)
ax1.set_title('Tempos de Resposta por Nível de Carga')
ax1.set_ylabel('Tempo (ms)')
ax1.set_xlabel('')
ax1.legend(['Médio', 'P95', 'P99'])
ax1.grid(axis='y', alpha=0.3)
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

# 2. Taxa de Erro
ax2 = axes[0, 1]
df_comparacao['Taxa_Erro_%'].plot(kind='bar', ax=ax2, color='red', alpha=0.7)
ax2.set_title('Taxa de Erro por Nível de Carga')
ax2.set_ylabel('Taxa de Erro (%)')
ax2.set_xlabel('')
ax2.grid(axis='y', alpha=0.3)
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')

# 3. RPS
ax3 = axes[1, 0]
df_comparacao['RPS'].plot(kind='bar', ax=ax3, color='green', alpha=0.7)
ax3.set_title('Requisições por Segundo')
ax3.set_ylabel('RPS')
ax3.set_xlabel('')
ax3.grid(axis='y', alpha=0.3)
plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha='right')

# 4. Total de Requisições
ax4 = axes[1, 1]
df_comparacao['Requisições'].plot(kind='bar', ax=ax4, color='blue', alpha=0.7)
ax4.set_title('Total de Requisições Processadas')
ax4.set_ylabel('Número de Requisições')
ax4.set_xlabel('')
ax4.grid(axis='y', alpha=0.3)
plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45, ha='right')

plt.tight_layout()
plt.savefig('resultados/comparacao_testes.png', dpi=300, bbox_inches='tight')
print("\n✅ Gráfico de comparação salvo: resultados/comparacao_testes.png")
plt.show()
```

**Execute:**

```bash
python comparacao_testes.py
```

**Questões de análise:**
1. O tempo de resposta aumentou linearmente com a carga?
2. Em que ponto o sistema começou a apresentar degradação significativa?
3. A taxa de erro aumentou com a carga? Por quê?

---

### Exercício 4.2: Análise de Outliers

**Objetivo**: Identificar requisições anômalas que afetam a performance.

Crie o script `analise_outliers.py`:

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Carregar dados
stats_df = pd.read_csv('resultados/teste_alta_carga_stats.csv')
endpoints_df = stats_df[stats_df['Name'] != 'Aggregated'].copy()

print("=" * 80)
print("ANÁLISE DE OUTLIERS")
print("=" * 80)

for idx, row in endpoints_df.iterrows():
    endpoint = row['Name']
    min_time = row['Min Response Time']
    avg_time = row['Average Response Time']
    max_time = row['Max Response Time']
    p99 = row['99%']

    # Calcular amplitude
    amplitude = max_time - min_time
    amplitude_p99_min = p99 - min_time

    # Calcular coeficiente de variação
    # Nota: precisaríamos do desvio padrão real, mas vamos estimar
    cv_estimado = (max_time - min_time) / avg_time

    print(f"\n🔹 {endpoint}")
    print(f"   Min: {min_time:.2f}ms")
    print(f"   Média: {avg_time:.2f}ms")
    print(f"   P99: {p99:.2f}ms")
    print(f"   Max: {max_time:.2f}ms")
    print(f"   Amplitude total: {amplitude:.2f}ms")
    print(f"   Amplitude P99-Min: {amplitude_p99_min:.2f}ms")
    print(f"   Coef. Variação estimado: {cv_estimado:.2f}")

    # Detectar outliers significativos
    if max_time > (p99 * 2):
        print(f"   ⚠️  OUTLIER DETECTADO: Máximo é {(max_time/p99):.1f}x maior que P99")

    # Verificar consistência
    if amplitude > (avg_time * 5):
        print(f"   ⚠️  ALTA VARIABILIDADE: Amplitude é {(amplitude/avg_time):.1f}x a média")

    # Avaliar distribuição
    ratio_p99_avg = p99 / avg_time
    if ratio_p99_avg > 2:
        print(f"   ⚠️  CAUDA LONGA: P99 é {ratio_p99_avg:.1f}x a média (distribuição assimétrica)")

# Visualização de box plot
fig, ax = plt.subplots(figsize=(12, 6))

endpoints = endpoints_df['Name'].values
data_for_boxplot = []

for idx, row in endpoints_df.iterrows():
    # Simular distribuição baseada nos percentis
    # (em um caso real, você teria os dados brutos)
    data_for_boxplot.append([
        row['Min Response Time'],
        row['50%'],
        row['Average Response Time'],
        row['95%'],
        row['99%'],
        row['Max Response Time']
    ])

# Criar gráfico
positions = range(len(endpoints))
for i, (endpoint, data) in enumerate(zip(endpoints, data_for_boxplot)):
    # Plotar linha mostrando range
    ax.plot([i, i], [data[0], data[5]], 'k-', linewidth=1, alpha=0.3)
    # Min
    ax.plot(i, data[0], 'go', markersize=8, label='Min' if i == 0 else '')
    # P50
    ax.plot(i, data[1], 'bo', markersize=8, label='P50' if i == 0 else '')
    # Avg
    ax.plot(i, data[2], 'yo', markersize=8, label='Avg' if i == 0 else '')
    # P95
    ax.plot(i, data[3], 'o', color='orange', markersize=8, label='P95' if i == 0 else '')
    # P99
    ax.plot(i, data[4], 'ro', markersize=8, label='P99' if i == 0 else '')
    # Max
    ax.plot(i, data[5], 'mo', markersize=10, marker='x', label='Max' if i == 0 else '')

ax.set_xticks(positions)
ax.set_xticklabels(endpoints, rotation=45, ha='right')
ax.set_ylabel('Tempo de Resposta (ms)')
ax.set_title('Distribuição de Tempos de Resposta por Endpoint')
ax.legend(loc='upper left')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('resultados/analise_outliers.png', dpi=300, bbox_inches='tight')
print("\n✅ Gráfico de outliers salvo: resultados/analise_outliers.png")
plt.show()
```

**Execute e analise:**

```bash
python analise_outliers.py
```

**Questões:**
1. Quais endpoints apresentam maior variabilidade?
2. Há requisições muito mais lentas que a média (outliers)?
3. O que pode causar esses outliers?

---

## 📝 Parte 5: Relatório Profissional (45 min)

### Exercício 5.1: Geração de Relatório HTML

**Objetivo**: Criar um relatório profissional para apresentar os resultados.

Crie o script `gerar_relatorio.py`:

```python
import pandas as pd
from datetime import datetime

def gerar_relatorio_html(stats_csv, history_csv, output_file='relatorio_final.html'):
    """Gera relatório HTML profissional"""

    # Carregar dados
    stats_df = pd.read_csv(stats_csv)
    history_df = pd.read_csv(history_csv)

    # Preparar dados agregados
    total_row = stats_df[stats_df['Name'] == 'Aggregated'].iloc[0]
    endpoints_df = stats_df[stats_df['Name'] != 'Aggregated']

    total_requisicoes = int(total_row['Request Count'])
    total_falhas = int(total_row['Failure Count'])
    taxa_erro = (total_falhas / total_requisicoes * 100) if total_requisicoes > 0 else 0
    tempo_medio = total_row['Average Response Time']
    p95 = total_row['95%']
    p99 = total_row['99%']
    rps_medio = total_row['Requests/s']

    # Duração do teste
    history_df['Timestamp'] = pd.to_datetime(history_df['Timestamp'], unit='s')
    duracao = history_df['Timestamp'].max() - history_df['Timestamp'].min()

    # Determinar status geral
    status_geral = "✅ APROVADO"
    cor_status = "green"
    if taxa_erro > 1:
        status_geral = "❌ REPROVADO"
        cor_status = "red"
    elif taxa_erro > 0.1 or p95 > 2000:
        status_geral = "⚠️ APROVADO COM RESSALVAS"
        cor_status = "orange"

    # Gerar tabela de endpoints
    endpoints_table = ""
    for idx, row in endpoints_df.iterrows():
        nome = row['Name']
        req = int(row['Request Count'])
        falhas = int(row['Failure Count'])
        erro_pct = (falhas / req * 100) if req > 0 else 0
        tempo_avg = row['Average Response Time']
        p50 = row['50%']
        p95_ep = row['95%']
        p99_ep = row['99%']
        min_time = row['Min Response Time']
        max_time = row['Max Response Time']

        cor_erro = 'green' if erro_pct < 0.5 else 'orange' if erro_pct < 2 else 'red'
        cor_tempo = 'green' if tempo_avg < 1000 else 'orange' if tempo_avg < 2000 else 'red'

        endpoints_table += f"""
        <tr>
            <td><strong>{nome}</strong></td>
            <td>{req:,}</td>
            <td>{falhas:,}</td>
            <td><span style="color: {cor_erro}; font-weight: bold;">{erro_pct:.2f}%</span></td>
            <td><span style="color: {cor_tempo};">{tempo_avg:.0f}ms</span></td>
            <td>{p50:.0f}ms</td>
            <td>{p95_ep:.0f}ms</td>
            <td>{p99_ep:.0f}ms</td>
            <td>{min_time:.0f}ms</td>
            <td>{max_time:.0f}ms</td>
        </tr>
        """

    # Template HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Relatório de Teste de Performance - Locust</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                line-height: 1.6;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            }}
            header {{
                border-bottom: 4px solid #667eea;
                padding-bottom: 20px;
                margin-bottom: 30px;
            }}
            h1 {{
                color: #333;
                margin-bottom: 10px;
                font-size: 32px;
            }}
            .subtitle {{
                color: #666;
                font-size: 14px;
                margin-bottom: 5px;
            }}
            .status-badge {{
                display: inline-block;
                padding: 8px 16px;
                border-radius: 20px;
                font-weight: bold;
                margin: 10px 0;
                background: {cor_status};
                color: white;
                font-size: 16px;
            }}
            h2 {{
                color: #555;
                margin-top: 40px;
                margin-bottom: 20px;
                border-left: 5px solid #667eea;
                padding-left: 15px;
                font-size: 24px;
            }}
            .summary {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }}
            .card {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 25px;
                border-radius: 12px;
                text-align: center;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                transition: transform 0.3s ease;
            }}
            .card:hover {{
                transform: translateY(-5px);
            }}
            .card.success {{ background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }}
            .card.error {{ background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%); }}
            .card.warning {{ background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }}
            .card.info {{ background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }}
            .card-value {{
                font-size: 36px;
                font-weight: bold;
                margin: 15px 0;
            }}
            .card-label {{
                font-size: 13px;
                opacity: 0.95;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            th {{
                background: #667eea;
                color: white;
                padding: 15px;
                text-align: left;
                font-weight: 600;
                font-size: 13px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            td {{
                padding: 12px 15px;
                border-bottom: 1px solid #e0e0e0;
            }}
            tr:hover {{
                background: #f5f7ff;
            }}
            .timestamp {{
                color: #999;
                font-size: 12px;
                text-align: right;
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #e0e0e0;
            }}
            .criterios {{
                background: #f9f9f9;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
            }}
            .criterios ul {{
                list-style-position: inside;
                margin-left: 10px;
            }}
            .criterios li {{
                padding: 5px 0;
            }}
            .observacoes {{
                background: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 15px;
                margin: 20px 0;
                border-radius: 4px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>📊 Relatório de Teste de Performance</h1>
                <p class="subtitle">Sistema testado com Locust</p>
                <p class="subtitle">Gerado em {datetime.now().strftime("%d/%m/%Y às %H:%M:%S")}</p>
                <div class="status-badge">{status_geral}</div>
            </header>

            <h2>Resumo Executivo</h2>
            <div class="summary">
                <div class="card info">
                    <div class="card-label">Total de Requisições</div>
                    <div class="card-value">{total_requisicoes:,}</div>
                </div>
                <div class="card error">
                    <div class="card-label">Falhas</div>
                    <div class="card-value">{total_falhas:,}</div>
                </div>
                <div class="card error">
                    <div class="card-label">Taxa de Erro</div>
                    <div class="card-value">{taxa_erro:.2f}%</div>
                </div>
                <div class="card success">
                    <div class="card-label">Tempo Médio</div>
                    <div class="card-value">{tempo_medio:.0f}ms</div>
                </div>
                <div class="card warning">
                    <div class="card-label">P95</div>
                    <div class="card-value">{p95:.0f}ms</div>
                </div>
                <div class="card warning">
                    <div class="card-label">P99</div>
                    <div class="card-value">{p99:.0f}ms</div>
                </div>
                <div class="card">
                    <div class="card-label">RPS Médio</div>
                    <div class="card-value">{rps_medio:.1f}</div>
                </div>
                <div class="card info">
                    <div class="card-label">Duração</div>
                    <div class="card-value">{duracao}</div>
                </div>
            </div>

            <h2>Critérios de Aceitação</h2>
            <div class="criterios">
                <ul>
                    <li>✅ Response time médio < 1000ms: <strong>{tempo_medio:.0f}ms</strong> {"✅" if tempo_medio < 1000 else "❌"}</li>
                    <li>✅ P95 < 2000ms: <strong>{p95:.0f}ms</strong> {"✅" if p95 < 2000 else "❌"}</li>
                    <li>✅ Taxa de erro < 0.1%: <strong>{taxa_erro:.2f}%</strong> {"✅" if taxa_erro < 0.1 else "❌"}</li>
                </ul>
            </div>

            <h2>Análise por Endpoint</h2>
            <table>
                <thead>
                    <tr>
                        <th>Endpoint</th>
                        <th>Requisições</th>
                        <th>Falhas</th>
                        <th>Taxa Erro</th>
                        <th>Média</th>
                        <th>P50</th>
                        <th>P95</th>
                        <th>P99</th>
                        <th>Mín</th>
                        <th>Máx</th>
                    </tr>
                </thead>
                <tbody>
                    {endpoints_table}
                </tbody>
            </table>

            <h2>Observações e Recomendações</h2>
            <div class="observacoes">
                <p><strong>Análise Geral:</strong></p>
                <p>O sistema foi submetido a um teste de carga durante {duracao}.
                   Durante este período, foram realizadas {total_requisicoes:,} requisições
                   com uma taxa de erro de {taxa_erro:.2f}%.</p>

                <p style="margin-top: 15px;"><strong>Recomendações:</strong></p>
                <ul>
                    {"<li>✅ Sistema apresentou performance satisfatória</li>" if taxa_erro < 0.1 and tempo_medio < 1000 else ""}
                    {"<li>⚠️ Monitorar taxa de erro em produção</li>" if taxa_erro > 0.1 else ""}
                    {"<li>⚠️ Considerar otimização de endpoints lentos</li>" if p95 > 2000 else ""}
                    {"<li>⚠️ Investigar causa das falhas</li>" if total_falhas > 0 else ""}
                </ul>
            </div>

            <div class="timestamp">
                <p>Relatório gerado automaticamente por Locust</p>
                <p>Data: {datetime.now().isoformat()}</p>
            </div>
        </div>
    </body>
    </html>
    """

    # Salvar arquivo
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ Relatório HTML gerado com sucesso: {output_file}")
    return output_file

# Executar
gerar_relatorio_html(
    'resultados/teste_alta_carga_stats.csv',
    'resultados/teste_alta_carga_stats_history.csv',
    'resultados/relatorio_final.html'
)
```

**Execute:**

```bash
python gerar_relatorio.py
```

**Abra o relatório no navegador:**

```bash
# Linux/Mac
open resultados/relatorio_final.html

# Windows
start resultados/relatorio_final.html
```

---

## 🎓 Parte 6: Projeto Final - Avaliação (60 min)

### Projeto: Análise Completa de Performance

**Objetivo**: Realizar uma análise completa de performance de uma API, documentando todos os passos e resultados.

**Requisitos:**

1. **Executar 3 tipos de teste**:
   - Teste de carga (100-300 usuários)
   - Teste de stress (até encontrar limite)
   - Teste de pico (escalada rápida)

2. **Exportar todos os dados**:
   - CSV de todos os testes
   - HTML reports
   - Logs de execução

3. **Análise completa**:
   - Métricas principais de cada teste
   - Comparação entre os 3 testes
   - Identificação de gargalos
   - Análise de outliers

4. **Visualizações**:
   - Gráficos de evolução temporal
   - Comparação de performance
   - Distribuição de percentis

5. **Relatório final**:
   - Relatório HTML profissional
   - Conclusões e recomendações
   - Status de aprovação/reprovação

**Entregáveis:**

```
projeto_final/
├── locustfile.py
├── README.md (documentação do projeto)
├── testes/
│   ├── teste_carga.sh
│   ├── teste_stress.sh
│   └── teste_pico.sh
├── resultados/
│   ├── teste_carga_*
│   ├── teste_stress_*
│   └── teste_pico_*
├── analises/
│   ├── analise_basica.py
│   ├── analise_comparativa.py
│   ├── analise_outliers.py
│   └── gerar_relatorio.py
└── relatorio_final.html
```

**Critérios de avaliação:**

| Critério                        | Peso |
| ------------------------------- | ---- |
| Execução correta dos 3 testes   | 20%  |
| Exportação completa dos dados   | 15%  |
| Análise de métricas             | 25%  |
| Qualidade das visualizações     | 20%  |
| Relatório final e conclusões    | 20%  |

---

## 📚 Recursos Adicionais

### Scripts Auxiliares

**1. Script de limpeza:**

```bash
#!/bin/bash
# limpar_resultados.sh
echo "Limpando resultados antigos..."
rm -rf resultados/*
mkdir -p resultados
echo "✅ Pasta de resultados limpa"
```

**2. Script de backup:**

```bash
#!/bin/bash
# backup_resultados.sh
DATA=$(date +%Y%m%d_%H%M%S)
echo "Fazendo backup dos resultados..."
tar -czf backup_$DATA.tar.gz resultados/
echo "✅ Backup criado: backup_$DATA.tar.gz"
```

### Comandos Úteis

```bash
# Ver tamanho dos arquivos de resultados
du -sh resultados/*

# Contar número de linhas em um CSV
wc -l resultados/*.csv

# Ver últimas linhas do histórico
tail -n 20 resultados/*_history.csv

# Procurar por erros específicos
grep -i "error" resultados/*.csv
```

### Checklist de Execução

- [ ] Ambiente Python configurado
- [ ] Locust instalado e atualizado
- [ ] Dependências instaladas (pandas, matplotlib, seaborn)
- [ ] Pasta de resultados criada
- [ ] Locustfile testado e validado
- [ ] Scripts de análise preparados
- [ ] Testes executados com sucesso
- [ ] Dados exportados corretamente
- [ ] Análises realizadas
- [ ] Visualizações geradas
- [ ] Relatório final criado
- [ ] Projeto documentado

---

## 🏁 Conclusão

Ao final deste roteiro, você deve ser capaz de:

1. ✅ Exportar dados de testes Locust de múltiplas formas
2. ✅ Analisar métricas de performance com Python/Pandas
3. ✅ Criar visualizações profissionais dos resultados
4. ✅ Comparar resultados de diferentes testes
5. ✅ Identificar gargalos e outliers
6. ✅ Gerar relatórios profissionais em HTML
7. ✅ Documentar e apresentar resultados de forma clara

---

**Dúvidas?**
- Consulte a documentação oficial do Locust: https://docs.locust.io
- Revise o documento de exportação: `exportacao_locust.md`
- Consulte o documento de tipos de teste: `tipo_teste_locust.md`

**Boa sorte com os testes!** 🚀
