import json
import google.generativeai as genai
import os
import time
from google.api_core import exceptions as google_exceptions
from googletrans import Translator
import requests

# Função para obter a cotação do dólar
def obter_cotacao_dolar():
    url = 'https://economia.awesomeapi.com.br/json/last/USD-BRL'
    response = requests.get(url)

    if response.status_code == 200:
        dados = response.json()
        cotacao = dados['USDBRL']['bid']
        return float(cotacao)
    else:
        print("Não foi possível obter a cotação do dólar.")
        return None

# Configuração da chave da API
api_key = 'AIzaSyCdUc8hHD_Uf6yior7ujtW5wvPYMepoh5I'  # Substitua pela sua chave de API
os.environ["API_KEY"] = api_key
genai.configure(api_key=os.environ["API_KEY"])

# Inicializando o tradutor
translator = Translator()

# Função para escolher o idioma
def escolher_idioma():
    idiomas = {'pt': 'Português', 'en': 'Inglês', 'es': 'Espanhol', 'zh-cn': 'Mandarim'}
    print("Escolha um idioma:")
    for codigo, nome in idiomas.items():
        print(f"{codigo}: {nome}")

    while True:
        idioma_escolhido = input("Digite o código do idioma: ").lower()
        if idioma_escolhido in idiomas:
            return idioma_escolhido
        else:
            print("Escolha um idioma válido.")
            for codigo, nome in idiomas.items():
                print(f"{codigo}: {nome}")

# Função para carregar o conteúdo das páginas a partir de um arquivo JSON
def carregar_conteudo(pasta):
    todos_conteudos = []
    for arquivo in os.listdir(pasta):
        caminho_completo = os.path.join(pasta, arquivo)
        if os.path.isfile(caminho_completo):
            try:
                with open(caminho_completo, 'r', encoding='utf-8') as f:
                    conteudo = json.load(f)
                    todos_conteudos.append({"arquivo": arquivo, "conteudo": conteudo})
            except UnicodeDecodeError:
                print(f"Erro de codificação ao ler o arquivo {arquivo}. Tentando com ISO-8859-1.")
                with open(caminho_completo, 'r', encoding='ISO-8859-1') as f:
                    conteudo = json.load(f)
                    todos_conteudos.append({"arquivo": arquivo, "conteudo": conteudo})
            except json.JSONDecodeError:
                print(f"Erro ao decodificar JSON do arquivo {arquivo}. Pulando...")
    return todos_conteudos

# Função para verificar se a língua é válida
def lingua_valida(lingua):
    valid_languages = ['en', 'pt', 'es', 'zh-cn']
    return lingua in valid_languages

# Função para obter os parâmetros do usuário com seleção de tema e vertente (subtema)
def obter_parametros_usuario(lingua):
    respostas = {}

    # Obtém a cotação do dólar
    cotacao_dolar = obter_cotacao_dolar()
    if cotacao_dolar is None:
        print("Não foi possível obter a cotação do dólar. Usando valor padrão.")
        cotacao_dolar = 5.00

    # Perguntas relacionadas à empresa
    perguntas_empresa = {
        "nome": "Por favor, insira o nome da pessoa responsável: ",
        "nome_empresa": "Por favor, insira o nome da empresa responsável: ",
        "lucro": f"Qual é o lucro bruto da empresa em reais (R$)?",
        "numero_colaboradores": "Por favor, insira o número de colaboradores: ",
        "CNPJ": "Por favor, forneça o CNPJ da empresa (se não possuir, informe 'Não'): ",
        "Email": "Por favor, insira o e-mail do responsável pelo projeto: "
    }

    # Perguntar os dados da empresa
    for chave, pergunta in perguntas_empresa.items():
        while True:
            try:
                resposta = input(pergunta)
                respostas[chave] = resposta
                break
            except ValueError:
                print("Por favor, insira uma resposta válida.")

    # Perguntar a área de atuação da empresa
    temas = {
        1: "Tecnologia da Informação (TI)",
        2: "Indústria",
        3: "Engenharia Civil e Infraestrutura",
        4: "Meio Ambiente",
        5: "Educação",
        6: "Saúde",
        7: "Finanças e Investimentos",
        8: "Agropecuária e Agroindústria",
        9: "Marketing e Comunicação",
        10: "Desenvolvimento Social e Humano",
        11: "Setor Público e Governança",
        12: "Entretenimento e Cultura"
    }

    print("Escolha a área de atuação da empresa:")
    for codigo, nome in temas.items():
        print(f"{codigo}: {nome}")

    while True:
        try:
            escolha_area = int(input("Digite o número da área escolhida: "))
            if escolha_area in temas:
                respostas["area_atuacao"] = temas[escolha_area]
                break
            else:
                print("Escolha um número válido para a área de atuação.")
        except ValueError:
            print("Por favor, insira um número válido.")

    # Perguntas relacionadas ao projeto
    perguntas_projeto = {
        "projeto": "Por favor, informe o nome do projeto: ",
        "orcamento": f"Cotação atual do dólar: R$ {cotacao_dolar:.2f} \nQual é o orçamento previsto para o projeto em reais (R$)?",
        "extensao": "Qual é a extensão geográfica do projeto? (Regional, Nacional, Mundial): ",
        "tempo": "Qual é a duração prevista do projeto em meses? ",
        "publicoalvo": "Quem é o público-alvo do projeto? ",
        "itensfianciaveis": "Os itens do projeto podem ser financiados? (Sim ou Não): "
    }

    # Perguntar o nome do projeto
    for chave, pergunta in perguntas_projeto.items():
        while True:
            try:
                resposta = input(pergunta)
                respostas[chave] = resposta
                break
            except ValueError:
                print("Por favor, insira uma resposta válida.")

    # Perguntar o tema do projeto
    print("\nEscolha o tema do projeto:")
    for codigo, nome in temas.items():
        print(f"{codigo}: {nome}")

    while True:
        try:
            escolha_tema = int(input("Digite o número do tema escolhido: "))
            if escolha_tema in temas:
                respostas["tema"] = temas[escolha_tema]
                break
            else:
                print("Escolha um número válido para o tema.")
        except ValueError:
            print("Por favor, insira um número válido.")

    # Perguntar a vertente (subtema) do tema escolhido
    vertentes = {
        1: ["Desenvolvimento de Software", "Infraestrutura de TI", "Segurança da Informação", "Transformação Digital", "Computação em Nuvem"],
        2: ["Manufatura", "Logística e Cadeia de Suprimentos", "Energia", "Engenharia de Produto"],
        3: ["Construção Civil", "Urbanismo", "Saneamento Básico", "Infraestrutura de Transportes"],
        4: ["Gestão de Resíduos", "Conservação de Recursos Naturais", "Energias Renováveis", "Sustentabilidade"],
        5: ["Educação a Distância (EAD)", "Capacitação e Treinamento", "Desenvolvimento de Currículo", "Inovação Educacional"],
        6: ["Infraestrutura de Saúde", "Tecnologia em Saúde (HealthTech)", "Pesquisa Biomédica", "Gestão de Saúde Pública"],
        7: ["Finanças Corporativas", "Gestão de Ativos", "Finanças Sustentáveis", "Criptomoedas e Blockchain"],
        8: ["Agricultura de Precisão", "Pecuária", "Agroindústria", "Desenvolvimento Rural Sustentável"],
        9: ["Marketing Digital", "Branding e Posicionamento de Marca", "Comunicação Corporativa", "Análise de Dados de Mercado"],
        10: ["Programas de Inclusão Social", "Empreendedorismo Social", "Direitos Humanos e Igualdade de Gênero", "Segurança Alimentar"],
        11: ["Políticas Públicas", "Modernização Administrativa", "Transparência e Compliance", "Planejamento Urbano e Regional"],
        12: ["Produção Audiovisual", "Artes Cênicas e Performáticas", "Indústria de Jogos", "Preservação do Patrimônio Cultural"]
    }

    print(f"\nVocê escolheu o tema '{temas[escolha_tema]}'. Agora escolha uma vertente (subtema):")
    for i, vertente in enumerate(vertentes[escolha_tema], 1):
        print(f"{i}. {vertente}")

    while True:
        try:
            escolha_vertente = int(input("Digite o número da vertente escolhida: "))
            if 1 <= escolha_vertente <= len(vertentes[escolha_tema]):
                respostas["vertente"] = vertentes[escolha_tema][escolha_vertente - 1]
                break
            else:
                print(f"Escolha um número entre 1 e {len(vertentes[escolha_tema])}.")
        except ValueError:
            print("Por favor, insira um número válido.")

    return respostas



# Função para obter análise da API Gemini
def get_gemini_analysis_with_retry(content, user_inputs, max_retries=5, initial_delay=1):
    for attempt in range(max_retries):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = (
                f"Analise o seguinte conteúdo com base nas entradas do usuário fornecidas:"
                f"\n\nConteúdo: {content}\n\n"
                f"Entradas do usuário:\n"
                f"- Nome do Projeto: {user_inputs.get('projeto', 'N/A')}\n"
                f"- Orçamento em reais (R$): {user_inputs.get('orcamento', 'N/A')}\n"
                f"- Número de Colaboradores: {user_inputs.get('numero_colaboradores', 'N/A')}\n"
                f"- Extensão Geográfica: {user_inputs.get('extensao', 'N/A')}\n"
                f"- Duração do Projeto: {user_inputs.get('tempo', 'N/A')} meses\n"
                f"- Setor: {user_inputs.get('tema', 'N/A')}\n"
                f"- Vertente ou Subtema: {user_inputs.get('vertente', 'N/A')}\n"
                f"- Itens Financiáveis: {user_inputs.get('itensfianciaveis', 'N/A')}\n"
                f"- Público-Alvo do Projeto: {user_inputs.get('publicoalvo', 'N/A')}\n"
                f"- Cotação Atual do Dólar: R$ {user_inputs.get('cotacao_dolar', 'N/A')}\n\n"
                f"Com base nesses dados, forneça:\n"
                f"- Uma pontuação de relevância de 0 a 10, onde 10 indica máxima adequação ao projeto e 0 irrelevância.\n"
                f"- Uma breve justificativa explicando a adequação e como o conteúdo pode contribuir para o projeto."
            )
            response = model.generate_content(prompt)
            return response.text
        except google_exceptions.ResourceExhausted:
            if attempt == max_retries - 1:
                print(f"Falha após {max_retries} tentativas. Retornando análise padrão.")
                return "0\nNão foi possível analisar devido a limitações da API."
            delay = initial_delay * (2 ** attempt)
            print(f"Limite de recursos atingido. Tentando novamente em {delay} segundos...")
            time.sleep(delay)
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return "0\nErro na análise."

def analise_page(content, inputs):
    analysis = get_gemini_analysis_with_retry(content, inputs)

    try:
        analysis_lines = analysis.split('\n')
        score = float(analysis_lines[0].split(':')[1].strip()) if ':' in analysis_lines[0] else float(analysis_lines[0])
        description = analysis_lines[1].strip()
    except Exception as e:
        print(f"Erro ao processar a análise: {e}")
        score = 0
        description = "Descrição não disponível"

    return score, description

def analise_melhor_json(melhor_conteudo, inputs):
    best_index = None
    best_score = 0
    best_url = None

    num_indices = len(melhor_conteudo)
    print(f"Número de índices presentes no JSON: {num_indices}")

    for index, item in enumerate(melhor_conteudo):
        content_str = json.dumps(item) if isinstance(item, dict) else str(item)
        score, _ = analise_page(content_str, inputs)
        print(f"Analisando index {index} de {num_indices}")

        if score > best_score:
            best_score = score
            best_index = index
            best_url = item.get('url', 'URL não encontrada') if isinstance(item, dict) else 'URL não encontrada'

        time.sleep(1)

    return best_index, best_score, best_url

def recomenda_investimento(conteudos, inputs):
    best_option = None
    best_score = 0
    best_content = None

    for pagina in conteudos:
        arquivo = pagina['arquivo']
        content = pagina['conteudo']

        if isinstance(content, list) and len(content) > 0:
            item = content[0]
        else:
            item = content

        content_str = json.dumps(item) if isinstance(item, dict) else str(item)

        score, description = analise_page(content_str, inputs)
        print(f"Arquivo: {arquivo} - Score: {score}.")

        if score > best_score:
            best_score = score
            best_option = arquivo
            best_content = content

        time.sleep(1.6)

    return best_option, best_score, best_content

def main():
    pasta_dados = './DADOS'

    if not os.path.exists(pasta_dados):
        print(f"A pasta '{pasta_dados}' não foi encontrada. Certifique-se de que ela existe e contém arquivos JSON.")
        return

    dados_paginas = carregar_conteudo(pasta_dados)

    lingua = escolher_idioma()

    if not lingua_valida(lingua):
        print("Língua inválida. Por favor, use uma das seguintes: 'en', 'pt', 'es', 'zh-cn'.")
        return

    inputs_usuario = obter_parametros_usuario(lingua)

    if not inputs_usuario:
        print("Nenhuma entrada do usuário foi fornecida. Encerrando o programa.")
        return

    melhor_opcao, melhor_score, melhor_conteudo = recomenda_investimento(dados_paginas, inputs_usuario)

    if melhor_opcao:
        print(f"\nA melhor opção para investimento é '{melhor_opcao}' com score {melhor_score:.2f}.")
        print("\nAnalisando os índices do melhor JSON...")
        melhor_index, melhor_index_score, melhor_url = analise_melhor_json(melhor_conteudo, inputs_usuario)
        print(f"\nO melhor índice é {melhor_index} com score {melhor_index_score:.2f}.")
        print(f"URL do melhor índice: {melhor_url}")
    else:
        print("Nenhuma opção relevante foi encontrada.")

if __name__ == "__main__":
    main()
