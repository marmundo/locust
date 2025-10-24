# Roteiro de Estudo: Testes de Carga com Locust

## Objetivo do Roteiro

Aprender a utilizar o Locust para realizar testes de carga e performance em aplicações web, compreendendo conceitos de teste de stress, throughput e comportamento de usuários simultâneos.

---

## ⚠️ AVISO IMPORTANTE SOBRE ÉTICA E LEGALIDADE

**ATENÇÃO:** Realizar testes de carga em sites que você NÃO possui ou NÃO tem permissão explícita é:

- **ILEGAL** - Pode ser considerado ataque DDoS
- **ANTIÉTICO** - Viola termos de serviço
- **CRIMINOSO** - Pode resultar em processo judicial

**Para este roteiro:**

- Use APENAS sites de demonstração
- Crie seu próprio ambiente de testes local
- Use sites explicitamente criados para prática (listados abaixo)

---

## Parte 1: Instalação do Locust

### Pré-requisitos

- Python 3.8 ou superior instalado
- pip (gerenciador de pacotes do Python)
- Terminal/Prompt de Comando

### Passo 1.1: Verificar Python

```bash
python --version
# ou
python3 --version
```

### Passo 1.2: Criar ambiente virtual (recomendado)

```bash
# Windows
python -m venv venv_locust
venv_locust\Scripts\activate

# Linux/Mac
python3 -m venv venv_locust
source venv_locust/bin/activate
```

### Passo 1.3: Instalar Locust

```bash
pip install locust
```

### Passo 1.4: Verificar instalação

```bash
locust --version
```

---

## Parte 2: Sites Seguros para Prática

### Opção 1: Sites de Demonstração (RECOMENDADO)

- **DemoQA**: https://demoqa.com/books
- **Swagger Petstore**: https://petstore.swagger.io/
- **ReqRes**: https://reqres.in/
- **JSONPlaceholder**: https://jsonplaceholder.typicode.com/

### Opção 2: Criar Servidor Local (MELHOR PRÁTICA)

Vamos criar um servidor Flask simples para testar:

**Arquivo: `app_teste.py`**

```python
from flask import Flask, jsonify, request
import time
import random

app = Flask(__name__)

# Simulando banco de dados de produtos
produtos = [
    {"id": 1, "nome": "Notebook", "preco": 2500.00, "estoque": 10},
    {"id": 2, "nome": "Mouse", "preco": 50.00, "estoque": 100},
    {"id": 3, "nome": "Teclado", "preco": 150.00, "estoque": 50},
    {"id": 4, "nome": "Monitor", "preco": 800.00, "estoque": 20},
]

@app.route('/')
def home():
    return jsonify({"mensagem": "Bem-vindo ao E-commerce de Teste"})

@app.route('/produtos')
def listar_produtos():
    # Simula latência do banco de dados
    time.sleep(random.uniform(0.1, 0.3))
    return jsonify(produtos)

@app.route('/produto/<int:produto_id>')
def detalhes_produto(produto_id):
    time.sleep(random.uniform(0.05, 0.15))
    produto = next((p for p in produtos if p["id"] == produto_id), None)
    if produto:
        return jsonify(produto)
    return jsonify({"erro": "Produto não encontrado"}), 404

@app.route('/carrinho', methods=['POST'])
def adicionar_carrinho():
    time.sleep(random.uniform(0.2, 0.4))
    dados = request.json
    return jsonify({
        "mensagem": "Produto adicionado ao carrinho",
        "produto_id": dados.get("produto_id"),
        "quantidade": dados.get("quantidade", 1)
    })

@app.route('/checkout', methods=['POST'])
def checkout():
    # Simula processamento de pagamento
    time.sleep(random.uniform(0.5, 1.0))
    return jsonify({
        "mensagem": "Compra realizada com sucesso",
        "pedido_id": random.randint(1000, 9999)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

**Instalar Flask:**

```bash
pip install flask
```

**Executar o servidor:**

```bash
python app_teste.py
```

O servidor estará disponível em: `http://localhost:5000`

---

## Parte 3: Criar Arquivo de Teste do Locust

### Passo 3.1: Criar arquivo locustfile.py

**Arquivo: `locustfile.py`**

```python
from locust import HttpUser, task, between
import random

class EcommerceUser(HttpUser):
    """
    Classe que simula o comportamento de um usuário no e-commerce
    """
    # Tempo de espera entre cada tarefa (em segundos)
    wait_time = between(1, 3)

    def on_start(self):
        """
        Método executado uma vez quando o usuário inicia
        Simula o acesso inicial à página principal
        """
        self.client.get("/")

    @task(3)  # Peso 3 - tarefa executada 3x mais que outras
    def visualizar_produtos(self):
        """
        Simula usuário navegando pela lista de produtos
        """
        self.client.get("/produtos")

    @task(2)  # Peso 2
    def visualizar_produto_especifico(self):
        """
        Simula usuário clicando em um produto específico
        """
        produto_id = random.randint(1, 4)
        self.client.get(f"/produto/{produto_id}")

    @task(1)  # Peso 1
    def adicionar_ao_carrinho(self):
        """
        Simula usuário adicionando produto ao carrinho
        """
        produto_id = random.randint(1, 4)
        quantidade = random.randint(1, 3)

        self.client.post("/carrinho", json={
            "produto_id": produto_id,
            "quantidade": quantidade
        })

    @task(1)
    def realizar_checkout(self):
        """
        Simula usuário finalizando a compra
        """
        self.client.post("/checkout", json={
            "metodo_pagamento": "credito",
            "endereco": "Rua Exemplo, 123"
        })
```

---

## Parte 4: Executar o Teste

### Passo 4.1: Modo Interface Web (Recomendado para Iniciantes)

**Terminal 1 - Iniciar o servidor de teste:**

```bash
python app_teste.py
```

**Terminal 2 - Iniciar o Locust:**

```bash
locust -f locustfile.py
```

**Acessar Interface Web:**

1. Abra o navegador
2. Acesse: `http://localhost:8089`
3. Configure:
   - **Number of users**: 10 (começar com poucos usuários)
   - **Spawn rate**: 2 (usuários por segundo)
   - **Host**: `http://localhost:5000`
4. Clique em **Start swarming**

### Passo 4.2: Modo Linha de Comando (Headless)

```bash
locust -f locustfile.py --headless -u 50 -r 10 -t 30s --host=http://localhost:5000
```

**Parâmetros:**

- `-f`: arquivo do locust
- `--headless`: sem interface web
- `-u 50`: 50 usuários simultâneos
- `-r 10`: spawn rate de 10 usuários/segundo
- `-t 30s`: duração do teste (30 segundos)
- `--host`: URL do servidor alvo

---

## Parte 5: Interpretar Resultados

### Métricas Principais:

1. **RPS (Requests Per Second)**

   - Quantidade de requisições por segundo
   - Indica throughput do sistema

2. **Response Time**

   - **Average**: Tempo médio de resposta
   - **Median (50%)**: Metade das requisições são mais rápidas
   - **95%**: 95% das requisições são mais rápidas que este valor
   - **99%**: 99% das requisições são mais rápidas

3. **Failures**
   - Porcentagem de requisições que falharam
   - Tipos de erro

### Exemplo de Análise:

```
Name                    # reqs  # fails  Avg    Min    Max    Median  95%   99%   RPS
---------------------------------------------------------------------------------
GET /produtos            1500      0     120ms   45ms  350ms   110ms  200ms 280ms  50.0
GET /produto/{id}        1000      0     80ms    30ms  200ms   75ms   150ms 180ms  33.3
POST /carrinho           500       2     200ms   80ms  450ms   180ms  350ms 420ms  16.7
POST /checkout           500       5     600ms   300ms 1200ms  550ms  950ms 1100ms 16.7
```

**Análise:**

- GET /produtos: Boa performance, sem falhas
- POST /checkout: Tempo alto, algumas falhas (potencial gargalo)

---

## 🎓 Parte 6: Exercícios Práticos

### Exercício 1: Teste Básico

1. Configure o teste com 5 usuários simultâneos
2. Execute por 1 minuto
3. Anote o RPS médio e tempo de resposta médio

### Exercício 2: Aumentar Carga

1. Aumente gradualmente: 10, 25, 50, 100 usuários
2. Identifique em que ponto o sistema começa a degradar
3. Qual é o tempo de resposta no 95º percentil?

### Exercício 3: Teste de Stress

1. Configure 200 usuários com spawn rate de 20/s
2. Execute por 2 minutos
3. Quantas falhas ocorreram?
4. O sistema se recuperou depois?

### Exercício 4: Cenário Realista

Modifique o `locustfile.py` para simular:

- 70% dos usuários apenas navegam
- 20% adicionam ao carrinho
- 10% finalizam compra

**Dica:** Ajuste os `@task(peso)` apropriadamente

### Exercício 5: Teste com Dados Dinâmicos

Adicione ao locustfile:

```python
import json

@task
def buscar_produto(self):
    termos_busca = ["notebook", "mouse", "teclado"]
    termo = random.choice(termos_busca)
    self.client.get(f"/busca?q={termo}")
```

---

## Parte 7: Conceitos Avançados

### 7.1 Classes de Usuário Diferentes

```python
from locust import HttpUser, task, between

class UsuarioNavegador(HttpUser):
    """Usuário que apenas navega"""
    weight = 7  # 70% dos usuários
    wait_time = between(2, 5)

    @task
    def navegar(self):
        self.client.get("/produtos")

class UsuarioComprador(HttpUser):
    """Usuário que compra"""
    weight = 3  # 30% dos usuários
    wait_time = between(3, 8)

    @task
    def comprar(self):
        self.client.post("/checkout", json={"item": 1})
```

### 7.2 Eventos do Locust

```python
from locust import events

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print(" Teste iniciado!")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print(" Teste finalizado!")
```

### 7.3 Gerar Relatório HTML

```bash
locust -f locustfile.py --headless -u 50 -r 10 -t 1m --host=http://localhost:5000 --html=relatorio.html
```

---

## Parte 8: Troubleshooting

### Problema: "Connection refused"

**Solução:** Verifique se o servidor está rodando na porta correta

### Problema: Muitas falhas (>5%)

**Soluções:**

- Reduza número de usuários
- Aumente recursos do servidor
- Verifique logs de erro no servidor

### Problema: Locust lento

**Solução:** Execute em modo headless para melhor performance

---

## Recursos Adicionais

### Documentação Oficial

- https://docs.locust.io/

### Tutoriais Recomendados

- https://docs.locust.io/en/stable/quickstart.html
- https://www.blazemeter.com/blog/locust-load-testing

### Ferramentas Complementares

- **Grafana + InfluxDB**: Visualização avançada de métricas
- **Docker**: Para isolar ambientes de teste

---

## Checklist de Conclusão

Ao final deste roteiro, você deve ser capaz de:

- [ ] Instalar e configurar o Locust
- [ ] Criar um arquivo locustfile.py básico
- [ ] Executar testes via interface web
- [ ] Executar testes via linha de comando
- [ ] Interpretar métricas de performance
- [ ] Identificar gargalos em aplicações
- [ ] Criar cenários realistas de teste
- [ ] Gerar relatórios de teste
- [ ] Compreender conceitos de RPS, latência e percentis
- [ ] Aplicar testes de carga de forma ética e legal

---

## Projeto Final

### Desafio: Criar Teste Completo

**Objetivo:** Criar um teste de carga que simule um cenário real de Black Friday

**Requisitos:**

1. Servidor local com pelo menos 5 endpoints
2. 3 tipos diferentes de usuários:
   - Navegadores (50%)
   - Compradores rápidos (30%)
   - Compradores cautelosos (20%)
3. Teste progressivo: começar com 10 usuários e chegar a 200
4. Gerar relatório HTML completo
5. Documento de análise com:
   - Gargalos identificados
   - Recomendações de otimização
   - Capacidade máxima do sistema

---

## Considerações Finais Éticas

### Boas Práticas:

- Sempre tenha permissão por escrito
- Use ambientes de teste/homologação
- Configure rate limiting apropriado
- Documente todos os testes
- Avise equipes envolvidas

### NUNCA:

- Teste sites de produção sem autorização
- Execute testes durante horário de pico sem coordenação
- Use Locust para ataques maliciosos
- Ignore termos de serviço

---

**Professor:** Marcelo Damasceno de Melo

**Disciplina:** Avaliação de Desempenho de Sistemas

**Data:** Outubro 2025

---

**Dúvidas?** Consulte a documentação oficial

**Bons estudos! **
