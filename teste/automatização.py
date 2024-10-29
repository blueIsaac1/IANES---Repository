import unittest
from unittest.mock import patch
from Main import carregar_conteudo, obter_parametros_usuario, recomenda_investimento, analise_melhor_json


class TestRecomendacaoInvestimento(unittest.TestCase):

    @patch('builtins.input', side_effect=[
        '1',  # Escolha do tema (Tecnologia da Informação (TI))
        '1',  # Escolha da vertente (Desenvolvimento de Software)
        '10',  # Número de colaboradores
        'João Silva',  # Nome da pessoa responsável
        'Empresa X',  # Nome da empresa
        'Projeto Y',  # Nome do projeto
        '100000',  # Orçamento em reais
        'Nacional',  # Extensão do projeto
        '12',  # Tempo do projeto em meses
        '50000',  # Lucro da empresa
        '12345678901234',  # CNPJ
        'Público Z',  # Público-alvo
        'Sim'  # Itens financiáveis
    ])
    def test_recomenda_investimento_com_indices_json(self, mock_input):
        # Carrega os conteúdos JSON da pasta de dados
        conteudos_json = carregar_conteudo('./DADOS')

        # Obtém os inputs do usuário
        inputs_usuario = obter_parametros_usuario("pt")

        # Testa a recomendação de investimento
        melhor_opcao, melhor_score, melhor_conteudo = recomenda_investimento(conteudos_json, inputs_usuario)

        # Verifica se foi identificada uma melhor opção
        self.assertIsNotNone(melhor_opcao, "Nenhuma opção de investimento recomendada.")
        self.assertGreater(melhor_score, 0, "O score da melhor opção deveria ser maior que zero.")

        # Analisa os índices do melhor JSON e seleciona o de melhor score
        melhor_index, melhor_index_score, melhor_url = analise_melhor_json(melhor_conteudo, inputs_usuario)

        # Verificações finais para garantir que o índice e URL do melhor JSON foram encontrados
        self.assertIsNotNone(melhor_index, "Nenhum índice encontrado no melhor JSON.")
        self.assertGreater(melhor_index_score, 0, "O score do melhor índice deveria ser maior que zero.")
        self.assertIsNotNone(melhor_url, "URL do melhor índice não encontrada.")

        # Saídas para conferir os resultados no console
        print(f"\nMelhor opção: {melhor_opcao} com score {melhor_score:.2f}.")
        print(f"Melhor índice: {melhor_index} com score {melhor_index_score:.2f}.")
        print(f"URL do melhor índice: {melhor_url}")


if __name__ == "__main__":
    unittest.main()
