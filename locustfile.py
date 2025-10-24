from locust import HttpUser, between, task


class AmazonUser(HttpUser):
    """
    Classe que simula um usuário navegando na Amazon.com
    """

    # Tempo de espera entre as tarefas (simula comportamento humano)
    wait_time = between(1, 5)

    # Define o host base
    host = "https://www.amazon.com"

    def on_start(self):
        """
        Executado quando um usuário virtual inicia
        """
        print("Usuário iniciado - simulando navegação na Amazon")

    @task(3)
    def view_homepage(self):
        """
        Acessa a página inicial da Amazon
        Peso 3: esta tarefa será executada 3x mais que as outras
        """
        with self.client.get("/", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Falha ao acessar homepage: {response.status_code}")

    @task(2)
    def search_products(self):
        """
        Realiza uma busca por produtos
        Peso 2: tarefa executada com frequência média
        """
        search_terms = ["laptop", "headphones", "books", "electronics", "toys"]
        import random

        term = random.choice(search_terms)

        with self.client.get(
            f"/s?k={term}", catch_response=True, name="/s?k=[search]"
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Falha na busca: {response.status_code}")

    @task(1)
    def view_best_sellers(self):
        """
        Acessa a página de mais vendidos
        Peso 1: tarefa menos frequente
        """
        with self.client.get("/gp/bestsellers/", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(
                    f"Falha ao acessar best sellers: {response.status_code}"
                )

    @task(1)
    def view_deals(self):
        """
        Acessa a página de ofertas
        Peso 1: tarefa menos frequente
        """
        with self.client.get("/deals", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Falha ao acessar deals: {response.status_code}")
