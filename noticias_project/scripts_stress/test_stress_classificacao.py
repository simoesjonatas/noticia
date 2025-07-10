import requests
import random
import time
from datetime import datetime

URL = "http://localhost:8000/api/webhook/noticia/"

TITULOS_CORPOS = [
    ("Nova proposta de isenção do IR entra na pauta do Congresso",
     "A proposta pode modificar o teto de dedução e afetar a arrecadação tributária."),
    ("Vacinação contra a gripe começa amanhã em todo o país",
     "A campanha do SUS inicia com prioridade para idosos e profissionais da saúde."),
    ("Sindicatos pressionam governo por revisão da CLT",
     "A reforma trabalhista de 2017 está sendo questionada por várias entidades."),
    ("Resumo matinal: principais decisões do STF hoje",
     "Veja os destaques jurídicos do dia e as pautas econômicas relacionadas."),
    ("Radar fiscal detecta novo aumento em tributos federais",
     "A Receita Federal divulgou alterações que podem impactar empresas do Simples Nacional."),
]

def gerar_noticia(i):
    titulo, corpo = random.choice(TITULOS_CORPOS)
    return {
        "titulo": f"[{i}] {titulo}",
        "corpo": corpo,
        "fonte": f"https://www.jota.info/teste-{i}",
        "data_publicacao": datetime.utcnow().isoformat() + "Z",
        "urgente": random.choice([True, False])
    }

def enviar_requisicoes(total=50, intervalo=0.1):
    print(f"Enviando {total} requisições para {URL} com classificação automática...")
    for i in range(total):
        dados = gerar_noticia(i)
        try:
            r = requests.post(URL, json=dados)
            print(f"[{i}] Status: {r.status_code}")
        except Exception as e:
            print(f"[{i}] Erro: {e}")
        time.sleep(intervalo)

if __name__ == "__main__":
    enviar_requisicoes(total=100, intervalo=0.05)
