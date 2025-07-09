 # 🧬 Otimizador de Times Pokémon com Algoritmo Genético
 
 ## 📝 Descrição
 
 Este projeto utiliza um **Algoritmo Genético** para descobrir o time de 6 Pokémon ideal para vencer todos os líderes de ginásio de uma região específica do universo Pokémon. A aplicação possui uma interface web interativa construída com **Streamlit**, que permite ao usuário escolher a região, configurar os parâmetros do algoritmo e acompanhar a evolução do melhor time em tempo real.  Para otimizar a performance e evitar sobrecarregar a [PokeAPI](https://pokeapi.co/), o sistema cria um banco de dados local em um arquivo `pokemon_database.json` na primeira execução.
 
 ---
 
 ## 🚀 Como Funciona
 
 O núcleo do projeto é o algoritmo genético, um processo inspirado na teoria da evolução de Darwin. Ele funciona em ciclos (gerações) para "evoluir" uma solução ótima.
 
 1.  **População Inicial**: O algoritmo começa criando uma população de times de Pokémon completamente aleatórios. Cada time é um "indivíduo".
 2.  **Função de Aptidão (Fitness)**: Cada time da população é avaliado por uma "função de aptidão", que calcula uma pontuação baseada na sua vantagem de tipo contra todos os Pokémon de todos os líderes de ginásio da região escolhida. Times com maior vantagem recebem uma pontuação maior. 3.  **Seleção**: Os times com as melhores pontuações são "selecionados" para se reproduzir, passando seus "genes" (Pokémon) para a próxima geração. 4.  **Cruzamento (Crossover)**: Dois times "pais" são combinados para criar um novo time "filho", que herda uma mistura de Pokémon de ambos. 5.  **Mutação**: Para introduzir diversidade e novas possibilidades, há uma pequena chance de um Pokémon em um time "filho" ser trocado aleatoriamente por outro. 6.  **Evolução Contínua**: Este ciclo se repete continuamente. A cada geração, a pontuação média da população tende a aumentar, e o algoritmo converge para um time altamente otimizado. O processo pode ser interrompido a qualquer momento pelo usuário.  ---  ## 📂 Estrutura do Projeto  O código é modularizado em 4 arquivos principais para melhor organização:  -   **`app.py`**: O arquivo principal que executa a aplicação Streamlit. Ele é responsável pela interface do usuário (UI), pelo controle de estado (iniciar/parar) e por orquestrar a chamada dos outros módulos.
 -   **`genetic_algorithm.py`**: Contém toda a lógica do algoritmo genético: `calculate_fitness`, `crossover`, `mutate` e a função principal `evolve_population`.
 -   **`database_manager.py`**: Gerencia a criação e o carregamento do banco de dados local (`pokemon_database.json`), interagindo com a PokeAPI apenas quando necessário.
 -   **`regions_data.py`**: Um arquivo de dados estático que armazena os times dos líderes de ginásio de todas as regiões, mantendo o código principal mais limpo.
 
 --- 
 ## 🛠️ Como Executar o Projeto
 
 Siga os passos abaixo para rodar a aplicação em sua máquina local.
 
 ### Pré-requisitos
 
 -   Python 3.7 ou superior
 -   Pip (gerenciador de pacotes do Python)
 
 ### 1. Crie os Arquivos
 
 Crie os 4 arquivos (`app.py`, `genetic_algorithm.py`, `database_manager.py`, `regions_data.py`) no mesmo diretório e copie o conteúdo correspondente em cada um deles.
 
 ### 2. Instale as Dependências
 
 Abra um terminal no diretório do projeto e instale as bibliotecas necessárias com o seguinte comando:
 
 ```bash
 pip install streamlit pandas requests
 ```
 
 ### 3\. Execute a Aplicação 
 Ainda no terminal, execute o comando:
 
 ```bash
 streamlit run app.py
 ```
 
 Seu navegador padrão abrirá automaticamente com a interface da aplicação.
 
 ### 4\. Primeira Execução (Criação do Banco de Dados)
 
 Na primeira vez que você rodar o projeto (ou se o arquivo `pokemon_database.json` for deletado), a aplicação irá automaticamente buscar todos os dados necessários da PokeAPI e criar o banco de dados local. **Este processo pode levar alguns minutos**, mas só precisa ser feito uma vez.
 
 ### 5\. Use o Otimizador
 
   - Na barra lateral, escolha a região e ajuste os parâmetros do algoritmo.
   - Clique em **"🚀 Iniciar"** para começar a evolução.
   - Acompanhe o gráfico e o melhor time sendo atualizados em tempo real.
   - Quando estiver satisfeito, clique em **"⏹️ Parar"**. O melhor resultado encontrado será mantido na tela.
 
 -----
 
 ## ✨ Funcionalidades
 
   - **Interface Interativa**: Construída com Streamlit para uma experiência de usuário amigável.
   - **Seleção de Região**: Suporte para todas as 9 gerações de Pokémon.
   - **Parâmetros Configuráveis**: Ajuste o tamanho da população, taxa de mutação e elitismo.
   - **Evolução Infinita**: Deixe o algoritmo rodar pelo tempo que quiser e pare quando encontrar um bom resultado.
   - **Visualização em Tempo Real**: Gráfico de aptidão e exibição do melhor time atualizados a cada geração.
   - **Banco de Dados Local**: Performance otimizada através da criação de um cache local em JSON, minimizando as chamadas à API.
 
 <!-- end list -->
