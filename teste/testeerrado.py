from unittest import TestCase
from unittest.mock import patch

from Main import obter_parametros_usuario, recomenda_investimento


class TestRecomendaInvestimento(TestCase):

    @patch('Main.analise_page', return_value=(9.5, "Relevante"))
    @patch('builtins.input', side_effect=[
        "",  # Nome vazio
        "",  # Projeto vazio
        "",  # Tema vazio
        "TI",  # Área válida
        "",  # Esboço vazio
        "miguel",  # Orçamento inválido (não numérico)
        "Local",  # Extensão inválida
        -5,  # Tempo inválido (negativo)
        200000,  # Lucro válido
        "invalid_cnpj",  # CNPJ inválido
        "",  # Público alvo vazio
        "Maybe",  # Resposta inválida para reembolso
        "Unsure",  # Resposta inválida para itens financiáveis
    ])
    def test_recomenda_investimento_falha(self, mock_input, mock_analise_page):
        conteudos = [
            {"arquivo": "projeto1.json", "conteudo": [{"url": "http://exemplo.com/projeto1"}]},
            {"arquivo": "projeto2.json", "conteudo": [{"url": "http://exemplo.com/projeto2"}]},
        ]

        # Simula a chamada para obter parâmetros do usuário
        inputs_usuario = obter_parametros_usuario("pt")

        # Verifica se as entradas foram capturadas corretamente (ou não)
        self.assertFalse(inputs_usuario)  # Esperamos que não tenha entradas válidas

        # Chama a função com entradas inválidas
        melhor_opcao, melhor_url = recomenda_investimento(conteudos, inputs_usuario)

        # Teste deve resultar em "None" ou um valor padrão, dependendo da implementação
        self.assertIsNone(melhor_opcao)
        self.assertIsNone(melhor_url)
