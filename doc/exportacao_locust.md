# 📈 Exportar e Analisar Dados de Testes Locust

Guia completo para extrair, exportar e analisar dados de performance coletados durante testes com Locust.

---

## 1. Formatos de Exportação Disponíveis

| Formato        | Descrição                     | Quando usar                              | Limitações                 |
| -------------- | ----------------------------- | ---------------------------------------- | -------------------------- |
| **CSV**        | Valores separados por vírgula | Análise em Excel, importação em BI       | Sem estrutura hierárquica  |
| **HTML**       | Relatório web interativo      | Compartilhar com stakeholders            | Arquivo grande             |
| **JSON**       | Formato estruturado           | Integração com scripts/APIs              | Menos legível manualmente  |
| **XML**        | Formato hierárquico           | Integração com sistemas enterprise       | Verboso                    |
| **Prometheus** | Métricas para monitoramento   | Integração com stacks de observabilidade | Requer servidor Prometheus |

---

## 2. Métodos de Exportação

### 2.1 Export via Interface Web do Locust

**Passo a passo:**

1. Execute o Locust com interface web

```bash
locust -f locustfile.py --host=http://seu-app.com
```

2. Acesse `http://localhost:8089`

3. Configure e execute o teste

4. Após conclusão, clique em **"Download Data"**

5. Selecione os formatos desejados:
   - Statistics (CSV)
   - Response time distribution (CSV)
   - Exceptions (CSV)
   - HTML Report

**Arquivos gerados:**

- `stats.csv` - Estatísticas principais
- `stats_history.csv` - Histórico de estatísticas
- `response_times_percentile.csv` - Percentis de resposta
- `response_times.csv` - Distribuição de tempos
- `failures.csv` - Falhas e exceções
- `report_*.html` - Relatório HTML completo

---

### 2.2 Export via CLI (Headless Mode)

**Comando básico com export automático:**

```bash
locust -f locustfile.py \
  -u 300 \
  --spawn-rate 20 \
  --run-time 20m \
  --headless \
  --csv=resultados \
  --html=relatorio.html
```

**Parâmetros importantes:**

- `--csv=PREFIX` - Exporta CSV com prefixo (gera stats, history, times, etc)
- `--html=FILE` - Gera relatório HTML
- `--csv-prefix=PATH` - Define caminho para arquivos CSV
- `--only-summary` - Apenas resumo final (sem histórico)

**Exemplo com caminho customizado:**

```bash
locust -f locustfile.py \
  -u 300 \
  --spawn-rate 20 \
  --run-time 20m \
  --headless \
  --csv=/resultados/teste_20250101 \
  --html=/relatorios/teste_20250101.html \
  --loglevel=INFO
```

---

### 2.3 Export Programático (Python)

**Usando events do Locust para capturar dados em tempo real:**

```python
from locust import HttpUser, task, between, events
from datetime import datetime
import json
import csv

# Variáveis globais para coleta
dados_colhidos = {
    'respostas': [],
    'falhas': [],
    'usuarios': []
}

@events.request.add_listener
def on_request(request_type, name, response_time, response_length,
               response, context, exception, **kwargs):
    """Captura cada requisição individualmente"""
    evento = {
        'timestamp': datetime.now().isoformat(),
        'tipo': request_type,
        'endpoint': name,
        'tempo_resposta_ms': response_time,
        'tamanho_resposta': response_length,
        'sucesso': exception is None,
        'exceção': str(exception) if exception else None,
        'status_code': response.status_code if response else None
    }
    dados_colhidos['respostas'].append(evento)

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Executado quando o teste termina"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Export JSON
    with open(f'dados_{timestamp}.json', 'w') as f:
        json.dump(dados_colhidos, f, indent=2)

    # Export CSV
    with open(f'dados_{timestamp}.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=dados_colhidos['respostas'][0].keys())
        writer.writeheader()
        writer.writerows(dados_colhidos['respostas'])

    print(f"✅ Dados exportados: dados_{timestamp}.json e .csv")

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def index(self):
        self.client.get("/")
```

---

### 2.4 Export com InfluxDB e Prometheus

**Configurar Locust para enviar métricas em tempo real:**

```bash
locust -f locustfile.py \
  --headless \
  --users 300 \
  --spawn-rate 20 \
  --run-time 20m \
  --loglevel=INFO \
  2>&1 | tee teste.log
```

**Coletar métricas via script Python:**

```python
from locust import events
import time
from datetime import datetime

class MetricasCollector:
    def __init__(self):
        self.metricas = {
            'timestamp': [],
            'usuarios_ativos': [],
            'rps': [],
            'tempo_resposta_medio': [],
            'taxa_erro': []
        }

    def collect(self, stats):
        self.metricas['timestamp'].append(datetime.now())
        self.metricas['usuarios_ativos'].append(stats.num_clients)
        self.metricas['rps'].append(stats.total_rps)
        self.metricas['tempo_resposta_medio'].append(stats.get_response_time_percentile(0.5))
        self.metricas['taxa_erro'].append(stats.total_fail_ratio)

collector = MetricasCollector()

@events.test_stats.add_listener
def on_stats_update(environment, **kwargs):
    collector.collect(environment.stats)

# Enviar para InfluxDB
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

def enviar_influxdb(host, token, org, bucket):
    client = influxdb_client.InfluxDBClient(url=host, token=token, org=org)
    write_api = client.write_api(write_type=SYNCHRONOUS)

    for i, ts in enumerate(collector.metricas['timestamp']):
        point = {
            "measurement": "locust_teste",
            "time": ts,
            "fields": {
                "usuarios": collector.metricas['usuarios_ativos'][i],
                "rps": collector.metricas['rps'][i],
                "tempo_medio": collector.metricas['tempo_resposta_medio'][i],
                "taxa_erro": collector.metricas['taxa_erro'][i]
            }
        }
        write_api.write(bucket=bucket, record=point)
```

---

## 3. Análise de Dados com Python (Pandas)

### 3.1 Script de Análise Básica

```python
import pandas as pd
import numpy as np
from datetime import datetime

# Carregar dados
stats_df = pd.read_csv('stats.csv')
response_times_df = pd.read_csv('response_times.csv')
history_df = pd.read_csv('stats_history.csv')

print("=" * 80)
print("ANÁLISE DE DADOS - TESTE DE PERFORMANCE")
print("=" * 80)

# 1. Resumo Geral
print("\n📊 RESUMO GERAL")
print("-" * 80)
print(f"Total de endpoints testados: {stats_df['Name'].nunique()}")
print(f"Total de requisições: {stats_df['Requests'].sum():,}")
print(f"Total de falhas: {stats_df['Failures'].sum():,}")
print(f"Taxa de erro geral: {(stats_df['Failures'].sum() / stats_df['Requests'].sum() * 100):.2f}%")

# 2. Análise por Endpoint
print("\n📍 ANÁLISE POR ENDPOINT")
print("-" * 80)
for idx, row in stats_df.iterrows():
    print(f"\n{row['Name']}")
    print(f"  Requisições: {row['Requests']:,}")
    print(f"  Falhas: {row['Failures']:,}")
    print(f"  Taxa de erro: {(row['Failures'] / row['Requests'] * 100):.2f}%")
    print(f"  Tempo médio: {row['Average (ms)']:.2f}ms")
    print(f"  P50: {row['50%ile (ms)']:.2f}ms")
    print(f"  P95: {row['95%ile (ms)']:.2f}ms")
    print(f"  P99: {row['99%ile (ms)']:.2f}ms")
    print(f"  Mín: {row['Min (ms)']:.2f}ms")
    print(f"  Máx: {row['Max (ms)']:.2f}ms")

# 3. Evolução ao Longo do Tempo
print("\n⏱️  EVOLUÇÃO DO TESTE")
print("-" * 80)
print(f"Duração total: {history_df['Timestamp'].max() - history_df['Timestamp'].min()}")
print(f"\nTempo de resposta médio (evolução):")
print(history_df[['Timestamp', 'Total Average Response Time']].head(10))

# 4. Percentis Importantes
print("\n📈 DISTRIBUIÇÃO DE TEMPOS DE RESPOSTA")
print("-" * 80)
for endpoint in response_times_df['Name'].unique():
    subset = response_times_df[response_times_df['Name'] == endpoint]
    print(f"\n{endpoint}:")
    for col in ['50', '66', '75', '80', '90', '95', '98', '99', '100']:
        if f'{col}%ile' in subset.columns:
            print(f"  {col}%ile: {subset[f'{col}%ile'].values[0]:.2f}ms")

# 5. Estatísticas Descritivas
print("\n📊 ESTATÍSTICAS DESCRITIVAS")
print("-" * 80)
print(f"Resposta mais rápida: {stats_df['Min (ms)'].min():.2f}ms")
print(f"Resposta mais lenta: {stats_df['Max (ms)'].max():.2f}ms")
print(f"Tempo médio geral: {stats_df['Average (ms)'].mean():.2f}ms")
print(f"Desvio padrão: {stats_df['Average (ms)'].std():.2f}ms")
print(f"Mediana: {stats_df['Average (ms)'].median():.2f}ms")
```

---

### 3.2 Script de Análise Avançada com Visualizações

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Configurar estilo
sns.set_style("darkgrid")
plt.rcParams['figure.figsize'] = (14, 10)

# Carregar dados
stats_df = pd.read_csv('stats.csv')
history_df = pd.read_csv('stats_history.csv')
response_times_df = pd.read_csv('response_times.csv')

# Criar figura com subplots
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Análise de Performance - Teste Locust', fontsize=16, fontweight='bold')

# 1. Tempo de Resposta por Endpoint
ax1 = axes[0, 0]
endpoints = stats_df['Name'].values
tempos = stats_df['Average (ms)'].values
colors = plt.cm.viridis(np.linspace(0, 1, len(endpoints)))
bars = ax1.barh(endpoints, tempos, color=colors)
ax1.set_xlabel('Tempo de Resposta (ms)')
ax1.set_title('Tempo Médio por Endpoint')
ax1.grid(axis='x', alpha=0.3)
for i, bar in enumerate(bars):
    width = bar.get_width()
    ax1.text(width, bar.get_y() + bar.get_height()/2,
             f'{width:.0f}ms', ha='left', va='center', fontweight='bold')

# 2. Taxa de Erro por Endpoint
ax2 = axes[0, 1]
taxa_erro = (stats_df['Failures'] / stats_df['Requests'] * 100).values
colors_erro = ['red' if x > 1 else 'orange' if x > 0.1 else 'green' for x in taxa_erro]
bars = ax2.barh(endpoints, taxa_erro, color=colors_erro)
ax2.set_xlabel('Taxa de Erro (%)')
ax2.set_title('Taxa de Erro por Endpoint')
ax2.grid(axis='x', alpha=0.3)
for i, bar in enumerate(bars):
    width = bar.get_width()
    ax2.text(width, bar.get_y() + bar.get_height()/2,
             f'{width:.2f}%', ha='left', va='center', fontweight='bold')

# 3. Evolução do Tempo de Resposta
ax3 = axes[1, 0]
history_df['Timestamp'] = pd.to_datetime(history_df['Timestamp'])
ax3.plot(history_df['Timestamp'], history_df['Total Average Response Time'],
         marker='o', linewidth=2, markersize=4, label='Tempo Médio')
ax3.plot(history_df['Timestamp'], history_df['Total95th Response Time'],
         marker='s', linewidth=2, markersize=4, alpha=0.7, label='P95')
ax3.plot(history_df['Timestamp'], history_df['Total99th Response Time'],
         marker='^', linewidth=2, markersize=4, alpha=0.7, label='P99')
ax3.set_xlabel('Tempo')
ax3.set_ylabel('Tempo de Resposta (ms)')
ax3.set_title('Evolução do Tempo de Resposta')
ax3.legend()
ax3.grid(True, alpha=0.3)
plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)

# 4. Distribuição de Requisições
ax4 = axes[1, 1]
requisicoes = stats_df['Requests'].values
falhas = stats_df['Failures'].values
x = range(len(endpoints))
width = 0.35
ax4.bar([i - width/2 for i in x], requisicoes, width, label='Sucesso', color='green', alpha=0.7)
ax4.bar([i + width/2 for i in x], falhas, width, label='Falhas', color='red', alpha=0.7)
ax4.set_ylabel('Número de Requisições')
ax4.set_title('Distribuição de Requisições')
ax4.set_xticks(x)
ax4.set_xticklabels(endpoints)
ax4.legend()
ax4.grid(axis='y', alpha=0.3)
plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45)

plt.tight_layout()
plt.savefig('analise_performance.png', dpi=300, bbox_inches='tight')
print("✅ Gráfico salvo: analise_performance.png")
plt.show()

# Relatório em texto
print("\n" + "="*80)
print("RELATÓRIO EXECUTIVO")
print("="*80)
print(f"Total de requisições: {stats_df['Requests'].sum():,}")
print(f"Taxa de erro total: {(stats_df['Failures'].sum() / stats_df['Requests'].sum() * 100):.2f}%")
print(f"Tempo de resposta médio: {stats_df['Average (ms)'].mean():.2f}ms")
print(f"P95: {stats_df['95%ile (ms)'].mean():.2f}ms")
print(f"P99: {stats_df['99%ile (ms)'].mean():.2f}ms")
```

---

## 4. Análise em Tempo Real (Monitoramento)

### 4.1 Script de Dashboard em Tempo Real

```python
from locust import events
from datetime import datetime
import time
import os

class DashboardEmTempoReal:
    def __init__(self):
        self.start_time = datetime.now()
        self.stats_history = []

    def limpar_tela(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def formatar_tempo(self, ms):
        return f"{ms:.0f}ms"

    def mostrar_dashboard(self, stats):
        self.limpar_tela()
        agora = datetime.now()
        elapsed = (agora - self.start_time).total_seconds()

        print("╔" + "═" * 78 + "╗")
        print("║" + " DASHBOARD LOCUST - ANÁLISE EM TEMPO REAL".center(78) + "║")
        print("╠" + "═" * 78 + "╣")

        # Informações gerais
        print(f"║ ⏱️  Tempo decorrido: {elapsed:.0f}s".ljust(79) + "║")
        print(f"║ 👥 Usuários ativos: {stats.num_clients}".ljust(79) + "║")
        print(f"║ 📊 Taxa de requisições: {stats.total_rps:.2f} req/s".ljust(79) + "║")
        print("╠" + "═" * 78 + "╣")

        # Estatísticas gerais
        print(f"║ {'ENDPOINT':<40} {'RPS':<12} {'TEMPO MÉDIO':<12} {'FALHAS':<12} ║")
        print("╠" + "═" * 78 + "╣")

        for name, stats_row in stats.entries.items():
            if name != "Total":
                rps = stats_row.total_rps
                tempo_medio = stats_row.avg_response_time
                falhas = stats_row.num_failures
                print(f"║ {name:<40} {rps:<12.2f} {tempo_medio:<12.0f} {falhas:<12} ║")

        # Total
        print("╠" + "═" * 78 + "╣")
        total = stats.entries.get("Total")
        if total:
            print(f"║ {'TOTAL':<40} {total.total_rps:<12.2f} {total.avg_response_time:<12.0f} {total.num_failures:<12} ║")

        print("╚" + "═" * 78 + "╝")

dashboard = DashboardEmTempoReal()

@events.test_stats.add_listener
def on_stats_update(environment, **kwargs):
    dashboard.mostrar_dashboard(environment.stats)

# Usar em locustfile.py
```

---

## 5. Comparação Entre Testes

### 5.1 Script para Comparar Múltiplos Testes

```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def comparar_testes(lista_testes):
    """
    Compara múltiplos testes

    Args:
        lista_testes: List[{'nome': str, 'arquivo_csv': str}]
    """

    resultados = {}

    for teste in lista_testes:
        df = pd.read_csv(teste['arquivo_csv'])
        resultados[teste['nome']] = {
            'tempo_medio': df['Average (ms)'].mean(),
            'p95': df['95%ile (ms)'].mean(),
            'p99': df['99%ile (ms)'].mean(),
            'taxa_erro': (df['Failures'].sum() / df['Requests'].sum() * 100),
            'total_requisicoes': df['Requests'].sum()
        }

    # Criar DataFrame comparativo
    df_comparacao = pd.DataFrame(resultados).T

    print("\n" + "="*80)
    print("COMPARAÇÃO ENTRE TESTES")
    print("="*80)
    print(df_comparacao.to_string())

    # Visualizar
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Gráfico 1: Tempos de Resposta
    ax1 = axes[0]
    df_comparacao[['tempo_medio', 'p95', 'p99']].plot(kind='bar', ax=ax1)
    ax1.set_title('Comparação - Tempos de Resposta')
    ax1.set_ylabel('Tempo (ms)')
    ax1.grid(True, alpha=0.3)

    # Gráfico 2: Taxa de Erro
    ax2 = axes[1]
    df_comparacao['taxa_erro'].plot(kind='bar', ax=ax2, color='red', alpha=0.7)
    ax2.set_title('Comparação - Taxa de Erro (%)')
    ax2.set_ylabel('Porcentagem (%)')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('comparacao_testes.png', dpi=300)
    print("\n✅ Gráfico de comparação salvo: comparacao_testes.png")

    return df_comparacao

# Usar
testes = [
    {'nome': 'Teste 1 (Carga)', 'arquivo_csv': 'stats_teste1.csv'},
    {'nome': 'Teste 2 (Stress)', 'arquivo_csv': 'stats_teste2.csv'},
    {'nome': 'Teste 3 (Pico)', 'arquivo_csv': 'stats_teste3.csv'}
]

df_resultado = comparar_testes(testes)
```

---

## 6. Análise com SQL (DuckDB)

### 6.1 Queries SQL para Análise

```python
import duckdb
import pandas as pd

# Conectar DuckDB
con = duckdb.connect(':memory:')

# Carregar dados
con.execute("CREATE TABLE stats AS SELECT * FROM read_csv_auto('stats.csv')")
con.execute("CREATE TABLE history AS SELECT * FROM read_csv_auto('stats_history.csv')")

# Query 1: Endpoints com pior performance
print("Endpoints com pior performance:")
resultado = con.execute("""
    SELECT
        Name as Endpoint,
        Requests,
        Failures,
        ROUND(Failures::FLOAT / Requests * 100, 2) as Taxa_Erro_Pct,
        ROUND("Average (ms)", 2) as Tempo_Medio_ms,
        ROUND("95%ile (ms)", 2) as P95_ms,
        ROUND("99%ile (ms)", 2) as P99_ms
    FROM stats
    WHERE Name != 'Total'
    ORDER BY "Average (ms)" DESC
""").df()
print(resultado)

# Query 2: Endpoints com maior taxa de erro
print("\nEndpoints com maior taxa de erro:")
resultado = con.execute("""
    SELECT
        Name,
        Requests,
        Failures,
        ROUND(Failures::FLOAT / Requests * 100, 2) as Taxa_Erro_Pct
    FROM stats
    WHERE Name != 'Total' AND Failures > 0
    ORDER BY Failures DESC
""").df()
print(resultado)

# Query 3: Análise de percentis
print("\nAnálise de Percentis:")
resultado = con.execute("""
    SELECT
        Name,
        "Min (ms)",
        "Average (ms)",
        "50%ile (ms)",
        "95%ile (ms)",
        "99%ile (ms)",
        "Max (ms)",
        ROUND("99%ile (ms)" - "50%ile (ms)", 2) as Amplitude_P50_P99
    FROM stats
    WHERE Name != 'Total'
""").df()
print(resultado)

# Query 4: Requisições por segundo ao longo do tempo
print("\nRequisições por segundo (últimos 10 registros):")
resultado = con.execute("""
    SELECT
        Timestamp,
        "Total Requests",
        "Total Failures",
        ROUND("Total Average Response Time", 2) as Tempo_Medio_ms,
        LAG("Total Requests") OVER (ORDER BY Timestamp) as Req_Anterior,
        "Total Requests" - LAG("Total Requests") OVER (ORDER BY Timestamp)
            as Req_Incremento
    FROM history
    ORDER BY Timestamp DESC
    LIMIT 10
""").df()
print(resultado)
```

---

## 7. Relatório HTML Customizado

### 7.1 Gerar Relatório HTML Profissional

```python
import pandas as pd
from datetime import datetime
import json

def gerar_relatorio_html(stats_csv, output_file='relatorio.html'):
    """Gera relatório HTML profissional a partir dos dados CSV"""

    # Carregar dados
    stats_df = pd.read_csv(stats_csv)

    # Preparar dados
    total_requisicoes = stats_df['Requests'].sum()
    total_falhas = stats_df['Failures'].sum()
    taxa_erro = (total_falhas / total_requisicoes * 100)

    endpoints_table = ""
    for idx, row in stats_df.iterrows():
        if row['Name'] != 'Total':
            erro_pct = (row['Failures'] / row['Requests'] * 100) if row['Requests'] > 0 else 0
            cor_erro = 'green' if erro_pct < 0.5 else 'orange' if erro_pct < 2 else 'red'

            endpoints_table += f"""
            <tr>
                <td>{row['Name']}</td>
                <td>{int(row['Requests']):,}</td>
                <td>{int(row['Failures'])}</td>
                <td><span style="color: {cor_erro}; font-weight: bold;">{erro_pct:.2f}%</span></td>
                <td>{row['Average (ms)']:.0f}ms</td>
                <td>{row['50%ile (ms)']:.0f}ms</td>
                <td>{row['95%ile (ms)']:.0f}ms</td>
                <td>{row['99%ile (ms)']:.0f}ms</td>
                <td>{row['Min (ms)']:.0f}ms</td>
                <td>{row['Max (ms)']:.0f}ms</td>
            </tr>
            """

    # HTML template
    html_content = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Relatório de Performance - Locust</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f5f5f5; padding: 20px; }}
            .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #333; margin-bottom: 10px; border-bottom: 3px solid #007bff; padding-bottom: 10px; }}
            h2 {{ color: #555; margin-top: 30px; margin-bottom: 15px; border-left: 4px solid #007bff; padding-left: 10px; }}
            .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }}
            .card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; }}
            .card.error {{ background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }}
            .card.success {{ background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }}
            .card-value {{ font-size: 28px; font-weight: bold; margin: 10px 0; }}
            .card-label {{ font-size: 12px; opacity: 0.9; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th {{ background: #007bff; color: white; padding: 12px; text-align: left; font-weight: 600; }}
            td {{ padding: 10px 12px; border-bottom: 1px solid #ddd; }}
            tr:hover {{ background: #f9f9f9; }}
            .timestamp {{ color: #999; font-size: 12px; text-align: right; margin-top: 30px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 Relatório de Performance - Teste Locust</h1>
            <p style="color: #999; margin: 10px 0;">Gerado em {datetime.now().strftime("%d/%m/%Y às %H:%M:%S")}</p>

            <h2>Resumo Executivo</h2>
            <div class="summary">
                <div class="card">
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
                    <div class="card-value">{stats_df[stats_df['Name'] == 'Total']['Average (ms)'].values[0]:.0f}ms</div>
                </div>
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

            <div class="timestamp">
                <p>Relatório gerado automaticamente por Locust | {datetime.now().isoformat()}</p>
            </div>
        </div>
    </body>
    </html>
    """

    # Salvar
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ Relatório HTML gerado: {output_file}")

# Usar
gerar_relatorio_html('stats.csv', 'relatorio_personalizado.html')
```

---

## 8. Checklist de Análise

### Antes de Analisar

- [ ] Todos os dados foram exportados corretamente?
- [ ] Arquivos CSV não estão corrompidos?
- [ ] Timestamps estão corretos?
- [ ] Há dados suficientes para análise (mínimo 5-10 min)?

### Durante a Análise

- [ ] Revisar taxa de erro geral e por endpoint
- [ ] Comparar tempos de resposta com baseline
- [ ] Identificar endpoints com pior performance
- [ ] Verificar evolução das métricas ao longo do tempo
- [ ] Detectar anomalias ou picos

### Análise de Resultados

- [ ] Taxa de erro dentro do esperado?
- [ ] Tempos de resposta aceitáveis?
- [ ] Algum recurso saturado?
- [ ] Necessários ajustes/otimizações?

---

## 9. Integração com Ferramentas Externas

### 9.1 Enviar para ELK Stack (Elasticsearch)

```python
from elasticsearch import Elasticsearch
import pandas as pd

es = Elasticsearch(['localhost:9200'])

stats_df = pd.read_csv('stats.csv')

for idx, row in stats_df.iterrows():
    doc = {
        'timestamp': pd.Timestamp.now(),
        'endpoint': row['Name'],
        'requests': int(row['Requests']),
        'failures': int(row['Failures']),
        'average_response': float(row['Average (ms)']),
        'p95': float(row['95%ile (ms)']),
        'p99': float(row['99%ile (ms)'])
    }
    es.index(index='locust-results', doc_type='_doc', body=doc)

print("✅ Dados enviados para Elasticsearch")
```

### 9.2 Integração com Grafana

Use o InfluxDB como data source no Grafana e crie dashboards personalizados.

---

## 10. Resumo dos Métodos de Exportação

| Método            | Vantagens                     | Desvantagens         | Melhor Para            |
| ----------------- | ----------------------------- | -------------------- | ---------------------- |
| **Interface Web** | Fácil, visual                 | Interativo apenas    | Análise rápida         |
| **CLI (CSV)**     | Automático, simples           | Pouco customizável   | Testes rotineiros      |
| **Programático**  | Total controle, em tempo real | Requer código        | Análises complexas     |
| **Prometheus**    | Integrado, métricas padrão    | Setup complexo       | Monitoramento contínuo |
| **InfluxDB**      | Série temporal, eficiente     | Infraestrutura extra | Histórico longo        |

---
