import unittest
import json
import os
from unittest.mock import patch, MagicMock
from Main import carregar_conteudo, lingua_valida, recomenda_investimento


class TestIAInvestimento(unittest.TestCase):

    # Testa a função carregar_conteudo
    def test_carregar_conteudo(self):
        # Cria um arquivo JSON de exemplo
        test_data = {"arquivo": "teste.json", "conteudo": {"investimento": "Projeto Teste"}}
        os.makedirs('DADOS_TEST', exist_ok=True)
        with open('DADOS_TEST/teste.json', 'w', encoding='utf-8') as f:
            json.dump(test_data['conteudo'], f)

        # Chama a função e verifica se o conteúdo foi carregado corretamente
        conteudos = carregar_conteudo('DADOS_TEST')
        self.assertEqual(len(conteudos), 1)
        self.assertEqual(conteudos[0]['conteudo'], test_data['conteudo'])

        # Limpa os arquivos temporários
        os.remove('DADOS_TEST/teste.json')
        os.rmdir('DADOS_TEST')

    # Testa a função lingua_valida
    def test_lingua_valida(self):
        self.assertTrue(lingua_valida('pt'))
        self.assertTrue(lingua_valida('en'))
        self.assertFalse(lingua_valida('fr'))

    @patch('Main.analise_page', return_value=(9.5, "Relevante"))
    def test_recomenda_investimento_falha(self, mock_analise_page):
        conteudos = [
            {"arquivo": "projeto1.json", "conteudo": [{"url": "http://exemplo.com/projeto1"}]},
            {"arquivo": "projeto2.json", "conteudo": [{"url": "http://exemplo.com/projeto2"}]},
        ]

        # Inputs incorretos
        inputs = {
            "nome": "",  # Nome vazio
            "projeto": "",  # Projeto vazio
            "tema": "",  # Tema vazio
            "area": "TI",
            "esboco": "",  # Esboço vazio
            "orcamento": "miguel",  # Orçamento inválido (não numérico)
            "extensao": "Local",  # Extensão inválida
            "tempo": -5,  # Tempo inválido (negativo)
            "lucro": 200000,
            "CNPJ": "invalid_cnpj",  # CNPJ inválido
            "publicoalvo": "",  # Público alvo vazio
            "lfreembolso": "Maybe",  # Resposta inválida
            "itensfianciaveis": "Unsure",  # Resposta inválida
        }

        melhor_opcao, melhor_url = recomenda_investimento(conteudos, inputs)

        # Esperamos que o teste falhe, pois os inputs são inválidos
        self.assertEqual(melhor_opcao, "projeto1.json")
        self.assertEqual(melhor_url, "http://exemplo.com/projeto1")


if __name__ == '__main__':
    unittest.main()
