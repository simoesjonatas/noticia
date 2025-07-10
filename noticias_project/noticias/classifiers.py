import re

REGRAS_CLASSIFICACAO = {
    'Tributos': {
        'palavras_chave': ['imposto', 'tributo', 'IR', 'isenção fiscal', 'receita federal'],
        'subcategorias': {
            'Aposta da Semana': ['aposta', 'destaque', 'semana'],
            'Radar': ['radar', 'monitoramento']
        }
    },
    'Saúde': {
        'palavras_chave': ['saúde', 'sus', 'hospitais', 'vacina'],
        'subcategorias': {
            'Matinal': ['matinal', 'manhã', 'resumo'],
        }
    },
    'Trabalhista': {
        'palavras_chave': ['CLT', 'reforma trabalhista', 'sindicato'],
        'subcategorias': {}
    }
}

def normalizar_texto(texto):
    return texto.lower()

def classificar(texto):
    texto = normalizar_texto(texto)
    categoria_resultado = None
    subcategoria_resultado = None
    tags_resultado = set()

    for categoria, regras in REGRAS_CLASSIFICACAO.items():
        for palavra in regras['palavras_chave']:
            if re.search(rf'\b{re.escape(palavra)}\b', texto):
                categoria_resultado = categoria
                tags_resultado.add(palavra)
                for sub, palavras_sub in regras['subcategorias'].items():
                    for palavra_sub in palavras_sub:
                        if re.search(rf'\b{re.escape(palavra_sub)}\b', texto):
                            subcategoria_resultado = sub
                            tags_resultado.add(palavra_sub)
                break
        if categoria_resultado:
            break

    return {
        'categoria': categoria_resultado,
        'subcategoria': subcategoria_resultado,
        'tags': list(tags_resultado)
    }
