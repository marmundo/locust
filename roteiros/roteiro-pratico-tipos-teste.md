# Roteiro Prático: Tipos de Teste de Performance com Locust

## Informações do Roteiro
- **Disciplina**: Avaliação de Desempenho de Sistemas
- **Professor**: Marcelo Damasceno de Melo
- **Objetivo**: Dominar os 3 tipos de teste de performance: Carga, Stress e Pico
- **Duração estimada**: 4-5 horas
- **Pré-requisitos**:
  - Python 3.8+
  - Locust instalado
  - Conhecimento básico de Locust

---

## Estrutura do Roteiro

Este roteiro aborda os **3 tipos principais de teste de performance**:

1. **Teste de Carga** - Validar comportamento com carga esperada
2. **Teste de Stress** - Encontrar limite máximo do sistema
3. **Teste de Pico** - Simular aumento repentino de carga

Cada tipo possui:
- Teoria e conceitos
- Configuração específica
- Exercícios práticos progressivos
- Critérios de aceitação
- Análise de resultados

---

## Sistema Sob Teste (SUT)

Para este roteiro, vamos criar um servidor Flask que simula uma API REST de e-commerce com endpoints de diferentes complexidades.

### Preparação do Ambiente

**1. Criar pasta do projeto:**

```bash
mkdir lab-testes-locust
cd lab-testes-locust
```

**2. Criar ambiente virtual:**

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

**3. Instalar dependências:**

```bash
pip install locust flask pandas matplotlib
```

**4. Criar servidor de teste (`servidor_api.py`):**

```python
from flask import Flask, jsonify, request
import time
import random
import threading

app = Flask(__name__)

# Métricas internas
metricas = {
    "requisicoes_totais": 0,
    "usuarios_ativos": 0,
    "cpu_simulada": 0
}

# Simular banco de dados
produtos_db = [
    {"id": i, "nome": f"Produto {i}", "preco": random.randint(10, 1000)}
    for i in range(1, 101)
]

def calcular_latencia_base():
    """Calcula latência base considerando carga do sistema"""
    carga = metricas["usuarios_ativos"]

    # Simular degradação com aumento de carga
    if carga < 50:
        return random.uniform(0.05, 0.15)
    elif carga < 150:
        return random.uniform(0.1, 0.3)
    elif carga < 300:
        return random.uniform(0.2, 0.5)
    else:
        # Sistema sob stress - degradação significativa
        return random.uniform(0.5, 2.0)

@app.before_request
def antes_requisicao():
    """Incrementa métricas antes de cada requisição"""
    metricas["requisicoes_totais"] += 1
    metricas["usuarios_ativos"] += 1

@app.after_request
def depois_requisicao(response):
    """Decrementa métricas após requisição"""
    metricas["usuarios_ativos"] = max(0, metricas["usuarios_ativos"] - 1)
    return response

@app.route('/')
def home():
    """Endpoint leve - página inicial"""
    time.sleep(random.uniform(0.01, 0.05))
    return jsonify({
        "mensagem": "API E-commerce de Teste",
        "versao": "1.0"
    })

@app.route('/produtos')
def listar_produtos():
    """Endpoint médio - listagem com paginação"""
    latencia = calcular_latencia_base()
    time.sleep(latencia)

    pagina = int(request.args.get('pagina', 1))
    por_pagina = int(request.args.get('por_pagina', 10))

    inicio = (pagina - 1) * por_pagina
    fim = inicio + por_pagina

    return jsonify({
        "produtos": produtos_db[inicio:fim],
        "pagina": pagina,
        "total": len(produtos_db)
    })

@app.route('/produto/<int:produto_id>')
def detalhe_produto(produto_id):
    """Endpoint leve - detalhe de produto"""
    latencia = calcular_latencia_base() * 0.5
    time.sleep(latencia)

    produto = next((p for p in produtos_db if p["id"] == produto_id), None)

    if produto:
        return jsonify(produto)
    return jsonify({"erro": "Produto não encontrado"}), 404

@app.route('/carrinho', methods=['POST'])
def adicionar_carrinho():
    """Endpoint médio - operação de escrita"""
    latencia = calcular_latencia_base() * 1.2
    time.sleep(latencia)

    dados = request.json or {}
    produto_id = dados.get('produto_id')
    quantidade = dados.get('quantidade', 1)

    if not produto_id:
        return jsonify({"erro": "produto_id obrigatório"}), 400

    return jsonify({
        "mensagem": "Produto adicionado ao carrinho",
        "produto_id": produto_id,
        "quantidade": quantidade
    }), 201

@app.route('/checkout', methods=['POST'])
def finalizar_compra():
    """Endpoint pesado - processamento complexo"""
    latencia = calcular_latencia_base() * 2.5

    # Simular processamento de pagamento
    time.sleep(latencia)

    # Simular falha sob alta carga (>10% de chance se muitos usuários)
    if metricas["usuarios_ativos"] > 200 and random.random() < 0.1:
        return jsonify({"erro": "Sistema temporariamente indisponível"}), 503

    dados = request.json or {}

    return jsonify({
        "mensagem": "Compra finalizada com sucesso",
        "pedido_id": random.randint(10000, 99999),
        "valor_total": dados.get("valor_total", 0)
    }), 201

@app.route('/busca')
def buscar_produtos():
    """Endpoint médio/pesado - busca com filtros"""
    latencia = calcular_latencia_base() * 1.5
    time.sleep(latencia)

    termo = request.args.get('q', '')

    resultados = [
        p for p in produtos_db
        if termo.lower() in p['nome'].lower()
    ]

    return jsonify({
        "termo": termo,
        "resultados": resultados,
        "total": len(resultados)
    })

@app.route('/metricas')
def obter_metricas():
    """Endpoint para monitorar o sistema"""
    metricas["cpu_simulada"] = min(100, (metricas["usuarios_ativos"] / 3))

    return jsonify(metricas)

if __name__ == '__main__':
    print("=" * 80)
    print("SERVIDOR API DE TESTE INICIADO")
    print("=" * 80)
    print("URL: http://localhost:5000")
    print("Endpoints disponíveis:")
    print("  GET  /              - Página inicial")
    print("  GET  /produtos      - Listar produtos")
    print("  GET  /produto/<id>  - Detalhe produto")
    print("  POST /carrinho      - Adicionar ao carrinho")
    print("  POST /checkout      - Finalizar compra")
    print("  GET  /busca?q=      - Buscar produtos")
    print("  GET  /metricas      - Métricas do sistema")
    print("=" * 80)

    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
```

**5. Executar o servidor (em um terminal separado):**

```bash
python servidor_api.py
```

Mantenha este terminal aberto durante todos os testes.

---

## Parte 1: Teste de Carga (Load Test)

### 1.1 Teoria e Conceitos

**Objetivo**: Validar que o sistema suporta a carga esperada em condições normais de operação.

**Quando usar**:
- Validar capacidade antes do deploy
- Estabelecer baseline de performance
- Garantir SLAs são atendidos
- Comparar versões diferentes da aplicação

**Características**:
- Simula carga real esperada
- Duração prolongada (15-30 min)
- Think time realista (1-3s)
- Spawn rate gradual (10-50 usuários/seg)

**Critérios de sucesso**:
- Response time médio < 1s
- P95 < 2s
- Taxa de erro < 0.1%
- CPU < 70%
- Estabilidade ao longo do tempo

---

### 1.2 Exercício 1: Teste de Carga Básico

**Objetivo**: Executar primeiro teste de carga e entender as métricas.

**Passo 1 - Criar locustfile (`teste_carga.py`):**

```python
from locust import HttpUser, task, between
import random

class UsuarioCarga(HttpUser):
    """
    Simula comportamento realista de usuário navegando no e-commerce
    """
    # Think time realista: usuário lê, pensa, navega
    wait_time = between(1, 3)

    def on_start(self):
        """Executado quando usuário inicia - acessa home"""
        self.client.get("/")

    @task(5)
    def navegar_produtos(self):
        """
        Tarefa mais comum - navegar produtos
        Peso 5: executada 5x mais que outras
        """
        pagina = random.randint(1, 5)
        self.client.get(f"/produtos?pagina={pagina}&por_pagina=10")

    @task(3)
    def ver_detalhes(self):
        """
        Ver detalhes de produto específico
        Peso 3: segunda tarefa mais comum
        """
        produto_id = random.randint(1, 100)
        self.client.get(f"/produto/{produto_id}")

    @task(2)
    def buscar_produto(self):
        """
        Usar sistema de busca
        Peso 2: menos comum que navegação
        """
        termos = ["Produto 1", "Produto 2", "Produto 5"]
        termo = random.choice(termos)
        self.client.get(f"/busca?q={termo}")

    @task(1)
    def adicionar_carrinho(self):
        """
        Adicionar produto ao carrinho
        Peso 1: poucos usuários adicionam
        """
        self.client.post("/carrinho", json={
            "produto_id": random.randint(1, 100),
            "quantidade": random.randint(1, 3)
        })

    @task(1)
    def finalizar_compra(self):
        """
        Finalizar compra
        Peso 1: muito poucos finalizam compra
        """
        self.client.post("/checkout", json={
            "valor_total": random.uniform(50, 500)
        })
```

**Passo 2 - Executar teste de carga:**

```bash
locust -f teste_carga.py \
  --host=http://localhost:5000 \
  -u 100 \
  --spawn-rate 20 \
  --run-time 5m \
  --headless \
  --csv=resultados/teste_carga_basico \
  --html=resultados/teste_carga_basico.html
```

**Parâmetros**:
- `-u 100`: 100 usuários simultâneos (carga esperada)
- `--spawn-rate 20`: adiciona 20 usuários/seg (gradual)
- `--run-time 5m`: duração de 5 minutos
- `--headless`: sem interface web
- `--csv` e `--html`: exportar resultados

**Passo 3 - Analisar resultados:**

Após o teste, verifique os arquivos gerados em `resultados/`:

```bash
ls -lh resultados/
```

Abra o relatório HTML no navegador.

---

### 1.3 Exercício 2: Análise de Resultados do Teste de Carga

**Objetivo**: Analisar os dados e determinar se o sistema passou nos critérios.

**Criar script de análise (`analisar_carga.py`):**

```python
import pandas as pd

# Carregar dados
stats = pd.read_csv('resultados/teste_carga_basico_stats.csv')

print("=" * 80)
print("ANÁLISE DO TESTE DE CARGA")
print("=" * 80)

# Dados agregados
total = stats[stats['Name'] == 'Aggregated'].iloc[0]

print(f"\nMÉTRICAS GERAIS:")
print(f"  Total de requisições: {int(total['Request Count']):,}")
print(f"  Falhas: {int(total['Failure Count']):,}")
print(f"  Taxa de erro: {(total['Failure Count'] / total['Request Count'] * 100):.3f}%")
print(f"  RPS médio: {total['Requests/s']:.2f}")

print(f"\nTEMPOS DE RESPOSTA:")
print(f"  Médio: {total['Average Response Time']:.2f}ms")
print(f"  Mínimo: {total['Min Response Time']:.2f}ms")
print(f"  Máximo: {total['Max Response Time']:.2f}ms")
print(f"  Mediana (P50): {total['50%']:.2f}ms")
print(f"  P95: {total['95%']:.2f}ms")
print(f"  P99: {total['99%']:.2f}ms")

print(f"\nAVALIAÇÃO DOS CRITÉRIOS:")
print(f"  Response time médio < 1000ms: ", end="")
if total['Average Response Time'] < 1000:
    print("✅ PASSOU")
else:
    print(f"❌ FALHOU ({total['Average Response Time']:.0f}ms)")

print(f"  P95 < 2000ms: ", end="")
if total['95%'] < 2000:
    print("✅ PASSOU")
else:
    print(f"❌ FALHOU ({total['95%']:.0f}ms)")

print(f"  Taxa de erro < 0.1%: ", end="")
taxa_erro = (total['Failure Count'] / total['Request Count'] * 100)
if taxa_erro < 0.1:
    print("✅ PASSOU")
else:
    print(f"❌ FALHOU ({taxa_erro:.2f}%)")

print("\n" + "=" * 80)
print("ANÁLISE POR ENDPOINT")
print("=" * 80)

endpoints = stats[stats['Name'] != 'Aggregated']
for idx, row in endpoints.iterrows():
    print(f"\n{row['Name']}")
    print(f"  Requisições: {int(row['Request Count']):,}")
    print(f"  Tempo médio: {row['Average Response Time']:.2f}ms")
    print(f"  P95: {row['95%']:.2f}ms")
    taxa = (row['Failure Count'] / row['Request Count'] * 100) if row['Request Count'] > 0 else 0
    print(f"  Taxa de erro: {taxa:.3f}%")
```

**Executar análise:**

```bash
python analisar_carga.py
```

---

### 1.4 Exercício 3: Teste de Carga Progressivo

**Objetivo**: Executar múltiplos testes com cargas crescentes para encontrar capacidade ideal.

**Criar script de teste progressivo (`teste_carga_progressivo.sh`):**

```bash
#!/bin/bash

echo "TESTE DE CARGA PROGRESSIVO"
echo "=========================="

# Criar pasta de resultados
mkdir -p resultados

# Testes com carga crescente
usuarios=(50 100 200 300)

for u in "${usuarios[@]}"
do
    echo ""
    echo "Executando teste com $u usuários..."

    locust -f teste_carga.py \
        --host=http://localhost:5000 \
        -u $u \
        --spawn-rate 20 \
        --run-time 3m \
        --headless \
        --csv=resultados/carga_${u}u \
        --html=resultados/carga_${u}u.html \
        --loglevel WARNING

    echo "Aguardando 30 segundos para sistema estabilizar..."
    sleep 30
done

echo ""
echo "Testes concluídos! Resultados em resultados/"
```

**Dar permissão de execução e executar:**

```bash
# Linux/Mac
chmod +x teste_carga_progressivo.sh
./teste_carga_progressivo.sh

# Windows - criar arquivo .bat ou executar manualmente
```

**Criar script de comparação (`comparar_cargas.py`):**

```python
import pandas as pd
import matplotlib.pyplot as plt

usuarios = [50, 100, 200, 300]
dados_comparacao = []

for u in usuarios:
    try:
        df = pd.read_csv(f'resultados/carga_{u}u_stats.csv')
        total = df[df['Name'] == 'Aggregated'].iloc[0]

        dados_comparacao.append({
            'Usuários': u,
            'RPS': total['Requests/s'],
            'Tempo_Médio': total['Average Response Time'],
            'P95': total['95%'],
            'P99': total['99%'],
            'Taxa_Erro': (total['Failure Count'] / total['Request Count'] * 100)
        })
    except Exception as e:
        print(f"Erro ao processar {u} usuários: {e}")

df_comp = pd.DataFrame(dados_comparacao)

print("=" * 80)
print("COMPARAÇÃO DE TESTES DE CARGA")
print("=" * 80)
print(df_comp.to_string(index=False))

# Gráficos
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Análise Comparativa de Testes de Carga', fontsize=16, fontweight='bold')

# 1. RPS vs Usuários
axes[0, 0].plot(df_comp['Usuários'], df_comp['RPS'], marker='o', linewidth=2, color='green')
axes[0, 0].set_title('Requisições por Segundo')
axes[0, 0].set_xlabel('Usuários')
axes[0, 0].set_ylabel('RPS')
axes[0, 0].grid(True, alpha=0.3)

# 2. Tempo Médio vs Usuários
axes[0, 1].plot(df_comp['Usuários'], df_comp['Tempo_Médio'], marker='o', linewidth=2, color='blue')
axes[0, 1].axhline(y=1000, color='red', linestyle='--', label='Limite 1000ms')
axes[0, 1].set_title('Tempo de Resposta Médio')
axes[0, 1].set_xlabel('Usuários')
axes[0, 1].set_ylabel('Tempo (ms)')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# 3. Percentis
axes[1, 0].plot(df_comp['Usuários'], df_comp['Tempo_Médio'], marker='o', label='Médio')
axes[1, 0].plot(df_comp['Usuários'], df_comp['P95'], marker='s', label='P95')
axes[1, 0].plot(df_comp['Usuários'], df_comp['P99'], marker='^', label='P99')
axes[1, 0].axhline(y=2000, color='red', linestyle='--', alpha=0.5)
axes[1, 0].set_title('Evolução dos Percentis')
axes[1, 0].set_xlabel('Usuários')
axes[1, 0].set_ylabel('Tempo (ms)')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

# 4. Taxa de Erro
axes[1, 1].bar(df_comp['Usuários'], df_comp['Taxa_Erro'], color='red', alpha=0.7)
axes[1, 1].axhline(y=0.1, color='orange', linestyle='--', label='Limite 0.1%')
axes[1, 1].set_title('Taxa de Erro')
axes[1, 1].set_xlabel('Usuários')
axes[1, 1].set_ylabel('Taxa de Erro (%)')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('resultados/comparacao_cargas.png', dpi=300, bbox_inches='tight')
print("\n✅ Gráfico salvo: resultados/comparacao_cargas.png")
plt.show()
```

**Executar comparação:**

```bash
python comparar_cargas.py
```

**Questões de análise:**
1. Com quantos usuários o sistema começou a degradar?
2. O tempo de resposta aumentou linearmente ou exponencialmente?
3. Qual é a capacidade recomendada para produção?

---

## Parte 2: Teste de Stress (Stress Test)

### 2.1 Teoria e Conceitos

**Objetivo**: Encontrar o ponto de quebra do sistema e entender como ele degrada sob carga extrema.

**Quando usar**:
- Descobrir limites máximos
- Validar tratamento de erros
- Identificar recursos críticos
- Planejar escalabilidade

**Características**:
- Carga acima do esperado
- Duração média/longa (20-45 min)
- Think time mínimo (0-1s)
- Spawn rate rápido (50-200 usuários/seg)
- Aumentar até falha

**Critérios de avaliação**:
- Identificar ponto de falha
- Response time sob stress < 5-10s
- CPU < 90%
- Degradação gradual (não abrupta)
- Mensagens de erro adequadas

---

### 2.2 Exercício 4: Teste de Stress Básico

**Objetivo**: Executar teste de stress e identificar o ponto de quebra.

**Criar locustfile (`teste_stress.py`):**

```python
from locust import HttpUser, task, between
import random

class UsuarioStress(HttpUser):
    """
    Simula usuários sob stress - mínimo think time
    """
    # Think time mínimo para maximizar carga
    wait_time = between(0.1, 0.5)

    def on_start(self):
        self.client.get("/")

    @task(4)
    def navegar_produtos(self):
        pagina = random.randint(1, 10)
        self.client.get(f"/produtos?pagina={pagina}")

    @task(3)
    def ver_detalhes(self):
        produto_id = random.randint(1, 100)
        self.client.get(f"/produto/{produto_id}")

    @task(2)
    def buscar(self):
        termo = f"Produto {random.randint(1, 100)}"
        self.client.get(f"/busca?q={termo}")

    @task(2)
    def adicionar_carrinho(self):
        self.client.post("/carrinho", json={
            "produto_id": random.randint(1, 100),
            "quantidade": random.randint(1, 5)
        })

    @task(1)
    def checkout(self):
        # Endpoint mais pesado - maior probabilidade de falha
        self.client.post("/checkout", json={
            "valor_total": random.uniform(100, 1000)
        })
```

**Executar teste de stress:**

```bash
locust -f teste_stress.py \
  --host=http://localhost:5000 \
  -u 500 \
  --spawn-rate 100 \
  --run-time 10m \
  --headless \
  --csv=resultados/teste_stress \
  --html=resultados/teste_stress.html
```

**Parâmetros**:
- `-u 500`: 500 usuários (muito acima da carga normal)
- `--spawn-rate 100`: escalada rápida
- `--run-time 10m`: duração de 10 minutos

---

### 2.3 Exercício 5: Análise de Degradação

**Objetivo**: Analisar como o sistema degradou sob stress.

**Criar script (`analisar_stress.py`):**

```python
import pandas as pd
import matplotlib.pyplot as plt

# Carregar dados
stats = pd.read_csv('resultados/teste_stress_stats.csv')
history = pd.read_csv('resultados/teste_stress_stats_history.csv')
failures = pd.read_csv('resultados/teste_stress_failures.csv')

print("=" * 80)
print("ANÁLISE DO TESTE DE STRESS")
print("=" * 80)

# Métricas gerais
total = stats[stats['Name'] == 'Aggregated'].iloc[0]

print(f"\nMÉTRICAS FINAIS:")
print(f"  Total de requisições: {int(total['Request Count']):,}")
print(f"  Falhas: {int(total['Failure Count']):,}")
print(f"  Taxa de erro: {(total['Failure Count'] / total['Request Count'] * 100):.2f}%")
print(f"  Tempo médio: {total['Average Response Time']:.2f}ms")
print(f"  P95: {total['95%']:.2f}ms")
print(f"  P99: {total['99%']:.2f}ms")

# Converter timestamp
history['Timestamp'] = pd.to_datetime(history['Timestamp'], unit='s')

# Análise de degradação
print(f"\nANÁLISE DE DEGRADAÇÃO:")
inicial = history.iloc[:10]['Total Average Response Time'].mean()
final = history.iloc[-10:]['Total Average Response Time'].mean()
variacao_pct = ((final - inicial) / inicial * 100)

print(f"  Tempo médio inicial: {inicial:.2f}ms")
print(f"  Tempo médio final: {final:.2f}ms")
print(f"  Degradação: {variacao_pct:+.1f}%")

# Análise de falhas
if len(failures) > 0:
    print(f"\nTIPOS DE FALHA:")
    for idx, row in failures.iterrows():
        print(f"  {row['Name']}: {int(row['Occurrences'])} ocorrências")
        print(f"    Erro: {row['Error']}")
else:
    print(f"\n✅ Nenhuma falha registrada")

# Identificar ponto de degradação
print(f"\nPONTO DE DEGRADAÇÃO:")
for idx, row in history.iterrows():
    if row['Total Average Response Time'] > 2000:  # Limite de 2s
        print(f"  Sistema degradou aos {row['User Count']} usuários")
        print(f"  Timestamp: {row['Timestamp']}")
        break
else:
    print(f"  Sistema não atingiu degradação significativa")

# Gráfico de evolução
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Análise de Teste de Stress', fontsize=16, fontweight='bold')

# 1. Usuários ao longo do tempo
axes[0, 0].plot(history['Timestamp'], history['User Count'], color='blue', linewidth=2)
axes[0, 0].set_title('Usuários Ativos')
axes[0, 0].set_xlabel('Tempo')
axes[0, 0].set_ylabel('Usuários')
axes[0, 0].grid(True, alpha=0.3)
plt.setp(axes[0, 0].xaxis.get_majorticklabels(), rotation=45)

# 2. Tempo de resposta ao longo do tempo
axes[0, 1].plot(history['Timestamp'], history['Total Average Response Time'], color='red', linewidth=2)
axes[0, 1].axhline(y=2000, color='orange', linestyle='--', label='Limite 2s')
axes[0, 1].set_title('Tempo de Resposta Médio')
axes[0, 1].set_xlabel('Tempo')
axes[0, 1].set_ylabel('Tempo (ms)')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)
plt.setp(axes[0, 1].xaxis.get_majorticklabels(), rotation=45)

# 3. RPS ao longo do tempo
axes[1, 0].plot(history['Timestamp'], history['Total Requests/s'], color='green', linewidth=2)
axes[1, 0].set_title('Requisições por Segundo')
axes[1, 0].set_xlabel('Tempo')
axes[1, 0].set_ylabel('RPS')
axes[1, 0].grid(True, alpha=0.3)
plt.setp(axes[1, 0].xaxis.get_majorticklabels(), rotation=45)

# 4. Failure Rate ao longo do tempo
if 'Total Failure Rate' in history.columns:
    axes[1, 1].plot(history['Timestamp'], history['Total Failure Rate'], color='red', linewidth=2)
    axes[1, 1].set_title('Taxa de Erro ao Longo do Tempo')
    axes[1, 1].set_xlabel('Tempo')
    axes[1, 1].set_ylabel('Taxa de Erro (%)')
    axes[1, 1].grid(True, alpha=0.3)
    plt.setp(axes[1, 1].xaxis.get_majorticklabels(), rotation=45)

plt.tight_layout()
plt.savefig('resultados/analise_stress.png', dpi=300, bbox_inches='tight')
print("\n✅ Gráfico salvo: resultados/analise_stress.png")
plt.show()
```

**Executar análise:**

```bash
python analisar_stress.py
```

**Questões de análise:**
1. Com quantos usuários o sistema começou a falhar?
2. A degradação foi gradual ou abrupta?
3. Quais endpoints apresentaram mais falhas?
4. O sistema consegue se recuperar após redução de carga?

---

### 2.4 Exercício 6: Teste de Stress por Fases

**Objetivo**: Executar teste de stress em fases crescentes para identificar exatamente onde o sistema quebra.

**Criar script (`teste_stress_fases.sh`):**

```bash
#!/bin/bash

echo "TESTE DE STRESS POR FASES"
echo "========================"

mkdir -p resultados

fases=(100 200 300 400 500 600 800 1000)

for usuarios in "${fases[@]}"
do
    echo ""
    echo "FASE: $usuarios usuários"
    echo "-------------------"

    locust -f teste_stress.py \
        --host=http://localhost:5000 \
        -u $usuarios \
        --spawn-rate 100 \
        --run-time 2m \
        --headless \
        --csv=resultados/stress_fase_${usuarios} \
        --html=resultados/stress_fase_${usuarios}.html \
        --loglevel WARNING

    echo "Aguardando sistema estabilizar (60s)..."
    sleep 60
done

echo ""
echo "Teste por fases concluído!"
```

**Criar análise das fases (`analisar_fases_stress.py`):**

```python
import pandas as pd
import matplotlib.pyplot as plt

fases = [100, 200, 300, 400, 500, 600, 800, 1000]
dados_fases = []

for usuarios in fases:
    try:
        df = pd.read_csv(f'resultados/stress_fase_{usuarios}_stats.csv')
        total = df[df['Name'] == 'Aggregated'].iloc[0]

        dados_fases.append({
            'Usuários': usuarios,
            'Tempo_Médio': total['Average Response Time'],
            'P95': total['95%'],
            'Taxa_Erro': (total['Failure Count'] / total['Request Count'] * 100),
            'RPS': total['Requests/s']
        })
    except Exception as e:
        print(f"Erro ao processar fase {usuarios}: {e}")

df_fases = pd.DataFrame(dados_fases)

print("=" * 80)
print("ANÁLISE DE STRESS POR FASES")
print("=" * 80)
print(df_fases.to_string(index=False))

# Identificar ponto de quebra
print("\n" + "=" * 80)
print("IDENTIFICAÇÃO DO PONTO DE QUEBRA")
print("=" * 80)

for idx, row in df_fases.iterrows():
    if row['Taxa_Erro'] > 1:
        print(f"Sistema começou a falhar com {row['Usuários']} usuários")
        print(f"  Taxa de erro: {row['Taxa_Erro']:.2f}%")
        print(f"  Tempo médio: {row['Tempo_Médio']:.0f}ms")
        break
else:
    print("Sistema não atingiu ponto de quebra nos testes realizados")

# Gráfico
plt.figure(figsize=(14, 8))

plt.subplot(2, 2, 1)
plt.plot(df_fases['Usuários'], df_fases['Tempo_Médio'], marker='o', linewidth=2, color='blue')
plt.axhline(y=5000, color='red', linestyle='--', alpha=0.5, label='Limite 5s')
plt.title('Tempo de Resposta Médio por Fase')
plt.xlabel('Usuários')
plt.ylabel('Tempo (ms)')
plt.grid(True, alpha=0.3)
plt.legend()

plt.subplot(2, 2, 2)
plt.plot(df_fases['Usuários'], df_fases['P95'], marker='s', linewidth=2, color='orange')
plt.title('P95 por Fase')
plt.xlabel('Usuários')
plt.ylabel('Tempo (ms)')
plt.grid(True, alpha=0.3)

plt.subplot(2, 2, 3)
plt.plot(df_fases['Usuários'], df_fases['Taxa_Erro'], marker='^', linewidth=2, color='red')
plt.axhline(y=1, color='orange', linestyle='--', alpha=0.5, label='Limite 1%')
plt.title('Taxa de Erro por Fase')
plt.xlabel('Usuários')
plt.ylabel('Taxa de Erro (%)')
plt.grid(True, alpha=0.3)
plt.legend()

plt.subplot(2, 2, 4)
plt.plot(df_fases['Usuários'], df_fases['RPS'], marker='d', linewidth=2, color='green')
plt.title('RPS por Fase')
plt.xlabel('Usuários')
plt.ylabel('Requisições/s')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('resultados/stress_fases.png', dpi=300, bbox_inches='tight')
print("\n✅ Gráfico salvo: resultados/stress_fases.png")
plt.show()
```

---

## Parte 3: Teste de Pico (Spike Test)

### 3.1 Teoria e Conceitos

**Objetivo**: Validar comportamento do sistema durante aumento repentino e temporário de carga.

**Quando usar**:
- Simular Black Friday
- Lançamento de produto
- Evento viral
- Horário de pico específico

**Características**:
- Escalada muito rápida
- Pico temporário
- Foco na recuperação
- Spawn rate muito alto (100-500 usuários/seg)

**Critérios de sucesso**:
- Sistema não trava
- Recovery time < 2-5 min
- Taxa de erro durante pico < 1%
- Retorna ao baseline após pico
- Auto-scaling funciona (se aplicável)

**Estrutura típica**:
1. **Carga base** (5-10 min): 100-300 usuários
2. **Escalada** (30-60s): Subida rápida
3. **Pico** (5-15 min): 1000-3000 usuários
4. **Redução** (30-60s): Volta rápida
5. **Recuperação** (5 min): Observar normalização

---

### 3.2 Exercício 7: Teste de Pico Manual com Interface Web

**Objetivo**: Executar teste de pico controlado manualmente para entender o comportamento.

**Passo 1 - Criar locustfile (`teste_pico.py`):**

```python
from locust import HttpUser, task, between
import random

class UsuarioPico(HttpUser):
    """
    Simula usuários durante evento de pico
    Think time reduzido mas não zero
    """
    wait_time = between(0.5, 2)

    def on_start(self):
        self.client.get("/")

    @task(5)
    def navegar_produtos(self):
        self.client.get(f"/produtos?pagina={random.randint(1, 5)}")

    @task(3)
    def ver_detalhes(self):
        self.client.get(f"/produto/{random.randint(1, 100)}")

    @task(2)
    def buscar(self):
        self.client.get(f"/busca?q=Produto {random.randint(1, 50)}")

    @task(2)
    def adicionar_carrinho(self):
        self.client.post("/carrinho", json={
            "produto_id": random.randint(1, 100),
            "quantidade": random.randint(1, 3)
        })

    @task(1)
    def checkout(self):
        self.client.post("/checkout", json={
            "valor_total": random.uniform(50, 500)
        })
```

**Passo 2 - Iniciar Locust com interface:**

```bash
locust -f teste_pico.py --host=http://localhost:5000
```

**Passo 3 - Acessar http://localhost:8089 e executar manualmente:**

1. **Fase 1 - Carga Base (3 minutos)**:
   - Usuários: 100
   - Spawn rate: 20
   - Clicar "Start"
   - Observar estabilização

2. **Fase 2 - Pico (5 minutos)**:
   - Clicar "Edit"
   - Alterar para 500 usuários
   - Spawn rate: 200 (escalada rápida!)
   - Observar impacto

3. **Fase 3 - Redução (2 minutos)**:
   - Clicar "Edit"
   - Voltar para 100 usuários
   - Observar recuperação

4. **Baixar dados**: Clicar em "Download Data" > "Download statistics"

**Observar durante o teste:**
- Gráficos de RPS
- Gráficos de tempo de resposta
- Número de falhas
- Como o sistema reage na escalada
- Quanto tempo leva para se recuperar

---

### 3.3 Exercício 8: Teste de Pico Automatizado

**Objetivo**: Automatizar teste de pico com múltiplas execuções.

**Criar script shell (`teste_pico_automatizado.sh`):**

```bash
#!/bin/bash

echo "TESTE DE PICO AUTOMATIZADO"
echo "=========================="

mkdir -p resultados

echo "FASE 1: Carga base (100 usuários, 3 min)"
locust -f teste_pico.py \
    --host=http://localhost:5000 \
    -u 100 \
    --spawn-rate 20 \
    --run-time 3m \
    --headless \
    --csv=resultados/pico_fase1_base \
    --html=resultados/pico_fase1_base.html \
    --loglevel WARNING

echo ""
echo "FASE 2: Pico (600 usuários, 5 min)"
locust -f teste_pico.py \
    --host=http://localhost:5000 \
    -u 600 \
    --spawn-rate 200 \
    --run-time 5m \
    --headless \
    --csv=resultados/pico_fase2_pico \
    --html=resultados/pico_fase2_pico.html \
    --loglevel WARNING

echo ""
echo "Aguardando sistema se recuperar (60s)..."
sleep 60

echo ""
echo "FASE 3: Pós-pico / Recuperação (100 usuários, 3 min)"
locust -f teste_pico.py \
    --host=http://localhost:5000 \
    -u 100 \
    --spawn-rate 20 \
    --run-time 3m \
    --headless \
    --csv=resultados/pico_fase3_recuperacao \
    --html=resultados/pico_fase3_recuperacao.html \
    --loglevel WARNING

echo ""
echo "Teste de pico concluído!"
```

**Dar permissão e executar:**

```bash
chmod +x teste_pico_automatizado.sh
./teste_pico_automatizado.sh
```

---

### 3.4 Exercício 9: Análise do Teste de Pico

**Objetivo**: Analisar comportamento em cada fase do pico.

**Criar script (`analisar_pico.py`):**

```python
import pandas as pd
import matplotlib.pyplot as plt

print("=" * 80)
print("ANÁLISE DO TESTE DE PICO")
print("=" * 80)

# Carregar dados das 3 fases
fases_dados = {}
fases = ['base', 'pico', 'recuperacao']
nomes = ['Carga Base', 'Pico', 'Recuperação']

for fase, nome in zip(fases, nomes):
    try:
        df = pd.read_csv(f'resultados/pico_fase{"123"[fases.index(fase)]}_{fase}_stats.csv')
        total = df[df['Name'] == 'Aggregated'].iloc[0]

        fases_dados[nome] = {
            'Requisições': int(total['Request Count']),
            'Falhas': int(total['Failure Count']),
            'Taxa_Erro_%': (total['Failure Count'] / total['Request Count'] * 100),
            'Tempo_Médio_ms': total['Average Response Time'],
            'P95_ms': total['95%'],
            'P99_ms': total['99%'],
            'RPS': total['Requests/s']
        }
    except Exception as e:
        print(f"Erro ao carregar {nome}: {e}")

df_fases = pd.DataFrame(fases_dados).T

print("\nCOMPARAÇÃO ENTRE FASES:")
print(df_fases.to_string())

# Análise de recuperação
print("\n" + "=" * 80)
print("ANÁLISE DE RECUPERAÇÃO")
print("=" * 80)

tempo_base = df_fases.loc['Carga Base', 'Tempo_Médio_ms']
tempo_pico = df_fases.loc['Pico', 'Tempo_Médio_ms']
tempo_recup = df_fases.loc['Recuperação', 'Tempo_Médio_ms']

impacto_pico = ((tempo_pico - tempo_base) / tempo_base * 100)
recuperacao_pct = ((tempo_recup - tempo_base) / tempo_base * 100)

print(f"\nTempo de resposta:")
print(f"  Base: {tempo_base:.0f}ms")
print(f"  Pico: {tempo_pico:.0f}ms (variação: {impacto_pico:+.1f}%)")
print(f"  Recuperação: {tempo_recup:.0f}ms (variação: {recuperacao_pct:+.1f}%)")

if abs(recuperacao_pct) < 10:
    print("\n✅ Sistema se recuperou completamente")
elif abs(recuperacao_pct) < 25:
    print("\n⚠️ Sistema se recuperou parcialmente")
else:
    print("\n❌ Sistema não se recuperou adequadamente")

# Taxa de erro durante pico
taxa_erro_pico = df_fases.loc['Pico', 'Taxa_Erro_%']
print(f"\nTaxa de erro durante pico: {taxa_erro_pico:.2f}%")

if taxa_erro_pico < 1:
    print("✅ Taxa de erro aceitável (< 1%)")
elif taxa_erro_pico < 5:
    print("⚠️ Taxa de erro elevada mas tolerável")
else:
    print("❌ Taxa de erro muito alta")

# Visualização
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Análise de Teste de Pico', fontsize=16, fontweight='bold')

fases_labels = df_fases.index.tolist()
x_pos = range(len(fases_labels))

# 1. Tempo de Resposta
axes[0, 0].bar(x_pos, df_fases['Tempo_Médio_ms'], color=['green', 'red', 'blue'], alpha=0.7)
axes[0, 0].set_xticks(x_pos)
axes[0, 0].set_xticklabels(fases_labels)
axes[0, 0].set_title('Tempo de Resposta Médio por Fase')
axes[0, 0].set_ylabel('Tempo (ms)')
axes[0, 0].grid(axis='y', alpha=0.3)

# Adicionar valores nas barras
for i, v in enumerate(df_fases['Tempo_Médio_ms']):
    axes[0, 0].text(i, v + 20, f'{v:.0f}ms', ha='center', fontweight='bold')

# 2. Taxa de Erro
axes[0, 1].bar(x_pos, df_fases['Taxa_Erro_%'], color=['green', 'orange', 'blue'], alpha=0.7)
axes[0, 1].axhline(y=1, color='red', linestyle='--', label='Limite 1%')
axes[0, 1].set_xticks(x_pos)
axes[0, 1].set_xticklabels(fases_labels)
axes[0, 1].set_title('Taxa de Erro por Fase')
axes[0, 1].set_ylabel('Taxa de Erro (%)')
axes[0, 1].legend()
axes[0, 1].grid(axis='y', alpha=0.3)

# 3. RPS
axes[1, 0].bar(x_pos, df_fases['RPS'], color=['green', 'purple', 'blue'], alpha=0.7)
axes[1, 0].set_xticks(x_pos)
axes[1, 0].set_xticklabels(fases_labels)
axes[1, 0].set_title('Requisições por Segundo')
axes[1, 0].set_ylabel('RPS')
axes[1, 0].grid(axis='y', alpha=0.3)

# 4. Percentis no Pico
percentis = ['Tempo_Médio_ms', 'P95_ms', 'P99_ms']
valores_pico = [df_fases.loc['Pico', col] for col in percentis]
axes[1, 1].bar(range(len(percentis)), valores_pico, color=['blue', 'orange', 'red'], alpha=0.7)
axes[1, 1].set_xticks(range(len(percentis)))
axes[1, 1].set_xticklabels(['Médio', 'P95', 'P99'])
axes[1, 1].set_title('Distribuição de Tempos Durante Pico')
axes[1, 1].set_ylabel('Tempo (ms)')
axes[1, 1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('resultados/analise_pico.png', dpi=300, bbox_inches='tight')
print("\n✅ Gráfico salvo: resultados/analise_pico.png")
plt.show()
```

**Executar análise:**

```bash
python analisar_pico.py
```

**Questões de análise:**
1. O sistema aguentou o pico sem travar?
2. Quanto tempo levou para se recuperar?
3. A taxa de erro foi aceitável durante o pico?
4. O sistema voltou ao baseline após o pico?

---

## Parte 4: Comparação Final dos 3 Tipos de Teste

### Exercício 10: Análise Comparativa Completa

**Objetivo**: Comparar resultados dos 3 tipos de teste lado a lado.

**Criar script (`comparacao_completa.py`):**

```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

print("=" * 80)
print("COMPARAÇÃO COMPLETA: CARGA vs STRESS vs PICO")
print("=" * 80)

# Carregar dados dos 3 tipos
tipos_teste = {
    'Teste de Carga': 'resultados/teste_carga_basico_stats.csv',
    'Teste de Stress': 'resultados/teste_stress_stats.csv',
    'Teste de Pico': 'resultados/pico_fase2_pico_stats.csv'
}

dados_comparacao = {}

for nome, arquivo in tipos_teste.items():
    try:
        df = pd.read_csv(arquivo)
        total = df[df['Name'] == 'Aggregated'].iloc[0]

        dados_comparacao[nome] = {
            'Requisições': int(total['Request Count']),
            'Falhas': int(total['Failure Count']),
            'Taxa_Erro_%': (total['Failure Count'] / total['Request Count'] * 100),
            'Tempo_Médio_ms': total['Average Response Time'],
            'P50_ms': total['50%'],
            'P95_ms': total['95%'],
            'P99_ms': total['99%'],
            'RPS': total['Requests/s']
        }
    except Exception as e:
        print(f"Erro ao carregar {nome}: {e}")

df_comp = pd.DataFrame(dados_comparacao).T

print("\nRESUMO COMPARATIVO:")
print(df_comp.to_string())

# Matriz de decisão
print("\n" + "=" * 80)
print("MATRIZ DE DECISÃO")
print("=" * 80)

print("\nQuando usar cada tipo de teste:")
print("\nTeste de Carga:")
print("  ✓ Validar SLAs antes do deploy")
print("  ✓ Estabelecer baseline de performance")
print("  ✓ Comparar versões da aplicação")
print("  ✓ Você conhece a carga esperada")

print("\nTeste de Stress:")
print("  ✓ Descobrir limites máximos")
print("  ✓ Planejar escalabilidade")
print("  ✓ Validar comportamento sob falha")
print("  ✓ Identificar gargalos críticos")

print("\nTeste de Pico:")
print("  ✓ Preparar para Black Friday")
print("  ✓ Validar auto-scaling")
print("  ✓ Simular eventos virais")
print("  ✓ Testar recuperação do sistema")

# Visualização comparativa
fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

tipos = df_comp.index.tolist()
x_pos = np.arange(len(tipos))
cores = ['#2ecc71', '#e74c3c', '#f39c12']

# 1. Tempo de Resposta Médio
ax1 = fig.add_subplot(gs[0, 0])
bars = ax1.bar(x_pos, df_comp['Tempo_Médio_ms'], color=cores, alpha=0.7)
ax1.set_xticks(x_pos)
ax1.set_xticklabels(tipos, rotation=15, ha='right')
ax1.set_title('Tempo de Resposta Médio', fontweight='bold')
ax1.set_ylabel('Tempo (ms)')
ax1.grid(axis='y', alpha=0.3)
for i, v in enumerate(df_comp['Tempo_Médio_ms']):
    ax1.text(i, v + 20, f'{v:.0f}ms', ha='center', fontsize=9, fontweight='bold')

# 2. Percentis
ax2 = fig.add_subplot(gs[0, 1:])
x = np.arange(len(tipos))
width = 0.25
ax2.bar(x - width, df_comp['P50_ms'], width, label='P50', color='#3498db', alpha=0.8)
ax2.bar(x, df_comp['P95_ms'], width, label='P95', color='#e67e22', alpha=0.8)
ax2.bar(x + width, df_comp['P99_ms'], width, label='P99', color='#e74c3c', alpha=0.8)
ax2.set_xticks(x)
ax2.set_xticklabels(tipos, rotation=15, ha='right')
ax2.set_title('Distribuição de Percentis', fontweight='bold')
ax2.set_ylabel('Tempo (ms)')
ax2.legend()
ax2.grid(axis='y', alpha=0.3)

# 3. Taxa de Erro
ax3 = fig.add_subplot(gs[1, 0])
bars = ax3.bar(x_pos, df_comp['Taxa_Erro_%'], color=cores, alpha=0.7)
ax3.axhline(y=0.1, color='orange', linestyle='--', linewidth=1, label='Limite 0.1%')
ax3.axhline(y=1.0, color='red', linestyle='--', linewidth=1, label='Limite 1%')
ax3.set_xticks(x_pos)
ax3.set_xticklabels(tipos, rotation=15, ha='right')
ax3.set_title('Taxa de Erro', fontweight='bold')
ax3.set_ylabel('Taxa (%)')
ax3.legend(fontsize=8)
ax3.grid(axis='y', alpha=0.3)
for i, v in enumerate(df_comp['Taxa_Erro_%']):
    ax3.text(i, v + 0.05, f'{v:.2f}%', ha='center', fontsize=9)

# 4. RPS
ax4 = fig.add_subplot(gs[1, 1])
bars = ax4.bar(x_pos, df_comp['RPS'], color=cores, alpha=0.7)
ax4.set_xticks(x_pos)
ax4.set_xticklabels(tipos, rotation=15, ha='right')
ax4.set_title('Requisições por Segundo', fontweight='bold')
ax4.set_ylabel('RPS')
ax4.grid(axis='y', alpha=0.3)
for i, v in enumerate(df_comp['RPS']):
    ax4.text(i, v + 1, f'{v:.1f}', ha='center', fontsize=9, fontweight='bold')

# 5. Total de Requisições
ax5 = fig.add_subplot(gs[1, 2])
bars = ax5.bar(x_pos, df_comp['Requisições'], color=cores, alpha=0.7)
ax5.set_xticks(x_pos)
ax5.set_xticklabels(tipos, rotation=15, ha='right')
ax5.set_title('Total de Requisições', fontweight='bold')
ax5.set_ylabel('Quantidade')
ax5.grid(axis='y', alpha=0.3)
for i, v in enumerate(df_comp['Requisições']):
    ax5.text(i, v + 100, f'{int(v):,}', ha='center', fontsize=9)

# 6. Tabela resumo
ax6 = fig.add_subplot(gs[2, :])
ax6.axis('tight')
ax6.axis('off')

# Criar tabela formatada
tabela_dados = []
for tipo in tipos:
    row = df_comp.loc[tipo]
    tabela_dados.append([
        tipo,
        f"{int(row['Requisições']):,}",
        f"{row['Taxa_Erro_%']:.2f}%",
        f"{row['Tempo_Médio_ms']:.0f}ms",
        f"{row['P95_ms']:.0f}ms",
        f"{row['RPS']:.1f}"
    ])

tabela = ax6.table(
    cellText=tabela_dados,
    colLabels=['Tipo de Teste', 'Requisições', 'Taxa Erro', 'Tempo Médio', 'P95', 'RPS'],
    cellLoc='center',
    loc='center',
    colWidths=[0.2, 0.15, 0.15, 0.15, 0.15, 0.15]
)
tabela.auto_set_font_size(False)
tabela.set_fontsize(10)
tabela.scale(1, 2)

# Estilizar cabeçalho
for i in range(6):
    tabela[(0, i)].set_facecolor('#3498db')
    tabela[(0, i)].set_text_props(weight='bold', color='white')

# Estilizar linhas
cores_linhas = ['#2ecc71', '#e74c3c', '#f39c12']
for i in range(len(tipos)):
    for j in range(6):
        tabela[(i+1, j)].set_facecolor(cores_linhas[i])
        tabela[(i+1, j)].set_alpha(0.3)

fig.suptitle('Comparação Completa: Tipos de Teste de Performance',
             fontsize=18, fontweight='bold', y=0.98)

plt.savefig('resultados/comparacao_completa.png', dpi=300, bbox_inches='tight')
print("\n✅ Gráfico salvo: resultados/comparacao_completa.png")
plt.show()

# Recomendações finais
print("\n" + "=" * 80)
print("RECOMENDAÇÕES")
print("=" * 80)

# Baseado no teste de carga
carga_tempo = df_comp.loc['Teste de Carga', 'Tempo_Médio_ms']
if carga_tempo < 1000:
    print("\n✅ Teste de Carga: Sistema APROVADO para produção")
    print(f"   Performance excelente ({carga_tempo:.0f}ms médio)")
else:
    print(f"\n⚠️ Teste de Carga: Otimização recomendada ({carga_tempo:.0f}ms)")

# Baseado no teste de stress
stress_erro = df_comp.loc['Teste de Stress', 'Taxa_Erro_%']
if stress_erro < 5:
    print("\n✅ Teste de Stress: Sistema resiliente sob stress")
else:
    print(f"\n❌ Teste de Stress: Alta taxa de erro ({stress_erro:.1f}%)")
    print("   Revisar tratamento de erros e limites")

# Baseado no teste de pico
pico_tempo = df_comp.loc['Teste de Pico', 'Tempo_Médio_ms']
pico_erro = df_comp.loc['Teste de Pico', 'Taxa_Erro_%']
if pico_tempo < 2000 and pico_erro < 1:
    print("\n✅ Teste de Pico: Sistema pronto para eventos de pico")
else:
    print(f"\n⚠️ Teste de Pico: Considerar auto-scaling")
    print(f"   Tempo: {pico_tempo:.0f}ms | Erro: {pico_erro:.2f}%")

print("\n" + "=" * 80)
```

**Executar:**

```bash
python comparacao_completa.py
```

---

## Parte 5: Projeto Final

### Desafio: Análise Completa de Performance

**Objetivo**: Realizar análise completa de performance de um sistema, documentando todos os passos.

**Requisitos:**

1. **Executar os 3 tipos de teste**:
   - Teste de carga (validar operação normal)
   - Teste de stress (encontrar limites)
   - Teste de pico (validar resiliência)

2. **Documentação completa**:
   - Configuração de cada teste
   - Critérios de aceitação
   - Resultados obtidos
   - Análise comparativa
   - Recomendações

3. **Entregáveis**:
   ```
   projeto_final/
   ├── README.md
   ├── servidor_api.py
   ├── testes/
   │   ├── teste_carga.py
   │   ├── teste_stress.py
   │   └── teste_pico.py
   ├── scripts/
   │   ├── executar_todos_testes.sh
   │   ├── analisar_carga.py
   │   ├── analisar_stress.py
   │   ├── analisar_pico.py
   │   └── comparacao_completa.py
   ├── resultados/
   │   ├── [arquivos CSV e HTML]
   │   └── [gráficos PNG]
   └── relatorio_final.md
   ```

4. **Relatório final deve incluir**:
   - Resumo executivo
   - Metodologia
   - Resultados de cada teste
   - Análise comparativa
   - Gargalos identificados
   - Capacidade do sistema
   - Recomendações de otimização
   - Conclusão (aprovado/reprovado)

**Critérios de avaliação:**

| Critério                          | Peso |
| --------------------------------- | ---- |
| Execução correta dos 3 testes     | 25%  |
| Análise de métricas               | 25%  |
| Qualidade das visualizações       | 20%  |
| Documentação e relatório final    | 20%  |
| Recomendações e insights          | 10%  |

---

## Recursos Adicionais

### Checklist de Execução

**Antes de cada teste:**
- [ ] Servidor API rodando
- [ ] Ambiente virtual ativado
- [ ] Pasta resultados/ criada
- [ ] Locustfile validado
- [ ] Sistema em estado limpo

**Durante o teste:**
- [ ] Monitorar logs do servidor
- [ ] Observar métricas em tempo real
- [ ] Anotar comportamentos anômalos

**Após o teste:**
- [ ] Exportar dados (CSV + HTML)
- [ ] Executar scripts de análise
- [ ] Gerar visualizações
- [ ] Documentar observações

### Comandos Úteis

```bash
# Ver processos Python rodando
ps aux | grep python

# Monitorar uso de CPU/memória
top  # ou htop

# Verificar porta 5000
lsof -i :5000  # Mac/Linux
netstat -ano | findstr :5000  # Windows

# Matar processo na porta 5000
kill -9 $(lsof -t -i:5000)  # Mac/Linux
```

### Dicas de Troubleshooting

**Problema**: Servidor Flask não aguenta a carga
- **Solução**: Use Gunicorn com múltiplos workers:
  ```bash
  pip install gunicorn
  gunicorn -w 4 -b 0.0.0.0:5000 servidor_api:app
  ```

**Problema**: Locust consome muita CPU
- **Solução**: Use modo headless e reduza logging

**Problema**: Resultados inconsistentes
- **Solução**: Aguarde sistema estabilizar entre testes

---

## Conclusão

Ao final deste roteiro, você deve dominar:

1. ✅ **Teste de Carga**: Validar operação normal
2. ✅ **Teste de Stress**: Encontrar limites
3. ✅ **Teste de Pico**: Validar resiliência
4. ✅ Configurar parâmetros específicos para cada tipo
5. ✅ Analisar métricas e gráficos
6. ✅ Comparar resultados
7. ✅ Documentar findings
8. ✅ Propor otimizações

**Próximos passos:**
- Testar com aplicações reais
- Integrar com CI/CD
- Usar ferramentas de monitoramento (Grafana, Prometheus)
- Explorar testes distribuídos

---

**Dúvidas?**
- Consulte: https://docs.locust.io
- Revise a documentação de tipos de teste
- Experimente com diferentes configurações

**Bons testes!**
