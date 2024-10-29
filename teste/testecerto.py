from unittest import TestCase
from unittest.mock import patch

from Main import obter_parametros_usuario, recomenda_investimento


class TestRecomendaInvestimento(TestCase):

    @patch('Main.analise_page', return_value=(9.5, "Relevante"))
    @patch('builtins.input', side_effect=[
        "Miguel",  # Nome válido
        "Projeto Alpha",  # Nome do projeto válido
        "Tecnologia",  # Tema válido
        "TI",  # Área válida
        "Desenvolver um software inovador",  # Esboço válido
        "100000",  # Orçamento válido (numérico)
        "Nacional",  # Extensão válida
        12,  # Tempo válido (em meses)
        250000,  # Lucro válido
        "12.345.678/0001-95",  # CNPJ válido
        "Empresas de tecnologia",  # Público alvo válido
        "Sim",  # Resposta válida para reembolso
        "Sim",  # Resposta válida para itens financiáveis
    ])
    def test_recomenda_investimento_sucesso(self, mock_input, mock_analise_page):
        conteudos = [
            {"arquivo": "projeto1.json", "conteudo": [{"url": "http://exemplo.com/projeto1"}]},
            {"arquivo": "projeto2.json", "conteudo": [{"url": "http://exemplo.com/projeto2"}]},
        ]

        # Simula a chamada para obter parâmetros do usuário
        inputs_usuario = obter_parametros_usuario("pt")

        # Verifica se as entradas foram capturadas corretamente
        self.assertEqual(inputs_usuario["nome"], "Miguel")
        self.assertEqual(inputs_usuario["projeto"], "Projeto Alpha")
        self.assertEqual(inputs_usuario["tema"], "Tecnologia")
        self.assertEqual(inputs_usuario["area"], "TI")
        self.assertEqual(inputs_usuario["esboco"], "Desenvolver um software inovador")
        self.assertEqual(inputs_usuario["orcamento"], 100000)
        self.assertEqual(inputs_usuario["extensao"], "Nacional")
        self.assertEqual(inputs_usuario["tempo"], 12)
        self.assertEqual(inputs_usuario["lucro"], 250000)
        self.assertEqual(inputs_usuario["CNPJ"], "12.345.678/0001-95")
        self.assertEqual(inputs_usuario["publicoalvo"], "Empresas de tecnologia")
        self.assertTrue(inputs_usuario["lfreembolso"])  # Deve ser True
        self.assertTrue(inputs_usuario["itensfianciaveis"])  # Deve ser True

        # Chama a função com entradas válidas
        melhor_opcao, melhor_url = recomenda_investimento(conteudos, inputs_usuario)

        # Verifica se a melhor opção e a URL retornadas são as esperadas
        self.assertEqual(melhor_opcao, "projeto1.json")
        self.assertEqual(melhor_url, "http://exemplo.com/projeto1")
