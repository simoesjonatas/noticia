import requests
import random
import time
from datetime import datetime

URL = "http://localhost:8000/api/webhook/noticia/"

CATEGORIAS = ["Tributos", "Saúde", "Trabalhista", "Poder"]
SUBCATEGORIAS = ["Aposta da Semana", "Matinal", "Radar", "Resumo Diário"]
TAGS = [
    "Imposto de Renda", "Congresso", "Isenção Fiscal",
    "SUS", "INSS", "Teto de Gastos", "Orçamento", "STF"
]

def gerar_noticia(i):
    categoria = random.choice(CATEGORIAS)
    subcategoria = random.choice(SUBCATEGORIAS)
    tags = random.sample(TAGS, k=random.randint(1, 3))

    return {
        "titulo": f"[{i}] Notícia automática sobre {categoria}",
        "corpo": f"Essa é uma notícia simulada para teste sobre {categoria}, com destaque para {', '.join(tags)}.",
        "fonte": f"https://www.exemplo.com/noticia-{i}",
        "data_publicacao": datetime.utcnow().isoformat() + "Z",
        "categoria": categoria,
        "subcategoria": subcategoria,
        "tags": tags,
        "urgente": random.choice([True, False])
    }

def enviar_requisicoes(total=50, intervalo=0.1):
    print(f"Enviando {total} requisições para {URL}...")
    for i in range(total):
        dados = gerar_noticia(i)
        try:
            r = requests.post(URL, json=dados)
            print(f"[{i}] Status: {r.status_code}")
        except Exception as e:
            print(f"[{i}] Erro: {e}")
        time.sleep(intervalo)

if __name__ == "__main__":
    enviar_requisicoes(total=500, intervalo=0.05)