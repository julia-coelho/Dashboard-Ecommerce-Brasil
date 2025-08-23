Nome do Projeto

Projeto Integrador I: Dashboard Ecommerce Brasil


Descrição do Projeto

Este projeto tem como objetivo analisar dados de e-commerce no Brasil com foco no problema de desequilíbrio entre vendas e estoque. Através da criação de um Dashboard interativo, será possível identificar padrões de ruptura de estoque (quando a demanda supera a oferta) e excesso de estoque (quando o produto permanece parado), auxiliando na tomada de decisão de empresas que atuam no comércio eletrônico. Dessa forma, será feito um extenso levantamento de dados para apoiar o projeto https://github.com/julia-coelho/ecommerce (Projeto Integrador II)


Objetivos Iniciais

- Criar um dashboard interativo para visualização de dados de vendas e estoque.

- Identificar rupturas de estoque e produtos com baixo giro.

- Implementar indicadores de desempenho como taxa de ruptura, cobertura de estoque e curva ABC.

- Promover análise exploratória de dados, destacando sazonalidade e tendências de compra.

- Entregar uma solução que apoie a gestão estratégica de estoque no e-commerce brasileiro.


Membros

Júlia Coelho Rodrigues (Líder e Desenvolvedora BackEnd)

Ricardo Souza Moraes (Analista de Dados e Tester)

Maria Eduarda Jardim (Desenvolvedora FrontEnd e Documentadora)

Letícia Mascarenhas (Desenvolvedora FrontEnd)

Victor Rithelly (Desenvolvedor BackEnd)


Estrutura do Repositório

 Dashboard-Ecommerce-Brasil
│── 📄 README.md                -> Descrição geral do projeto (nome, objetivos, papéis, estrutura, etc.)
│── 📄 .gitignore               -> Definir arquivos/pastas a serem ignorados pelo Git
│
├── 📂 docs                     -> Documentação e relatórios
│   │── 📄 mapa_empatia.md       -> Versão detalhada do mapa de empatia
│   │── 📄 apresentacao.pptx     -> Slides da apresentação final (quando estiver pronto)
│
├── 📂 data                     -> Dados brutos e tratados
│   │── 📄 dataset.csv           -> Arquivo base de dados
│   │── 📄 dicionario_dados.md   -> Explicação de cada coluna do dataset
│   └── 📂 processed             -> Dados tratados para análise
│
├── 📂 src                      -> Código-fonte
│   │── 📂 analysis              -> Scripts de análise exploratória (ex: notebooks Python)
│   │
│   │── 📂 dashboard             -> Implementação do dashboard
│   │
│   └── 📂 utils                 -> Funções auxiliares (ex.: limpeza de dados, validações)
│
├── 📂 prototypes               -> Protótipos e wireframes
│
└── 📂 tests                    -> Testes de código e validação

Explicação da Estrutura

    README.md → principal ponto de entrada (descrição, objetivos, papéis, instruções de uso).

    docs/ → toda a documentação e relatórios.

    data/ → datasets (originais e tratados).

    src/ → código do projeto separado em análise, dashboard e utilitários.

    prototypes/ → esboços visuais do dashboard (Figma, imagens, mockups).

    tests/ → scripts para validar se o código e análises funcionam corretamente.