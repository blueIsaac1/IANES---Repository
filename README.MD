# IANES - Sistema de Recomendação de Investimentos

## Integrantes do Grupo
- Miguel
- Isaac
- Breno
- Luiz Francisco
- Renan
- Pedro

## Objetivo
O IANES é um sistema de recomendação de investimentos que analisa oportunidades de financiamento e as compara com os parâmetros fornecidos pelo usuário. O objetivo principal é ajudar empreendedores e pesquisadores a encontrar as melhores opções de investimento para seus projetos de inovação.

## Funcionalidades
1. Coleta de dados de páginas web sobre oportunidades de investimento
2. Análise de conteúdo usando a API Gemini da Google
3. Interface de usuário para inserção de parâmetros do projeto
4. Recomendação da melhor opção de investimento com base na análise

## Dependências
- Python 3.x
- Bibliotecas Python:
  - google.generativeai
  - requests
  - beautifulsoup4
  - json

## Como usar
1. Execute o script `Analisar.py` para coletar e armazenar dados de páginas web.
2. Execute o script `Main.py` para iniciar o sistema de recomendação.
3. Insira os parâmetros do seu projeto quando solicitado.
4. O sistema analisará as opções e recomendará a melhor oportunidade de investimento.

## Configuração
Certifique-se de substituir a chave da API Gemini no arquivo `Main.py` pela sua própria chave antes de executar o programa.

## Notas
Este projeto está em desenvolvimento e pode requerer ajustes adicionais para melhorar a precisão e eficiência das recomendações.