Todos os elementos deste programa são de autoria de Arthur Luiz Lima De Araújo e Lucas Issamu Hashimoto

Este Programa Implementa 3 algoritmos de emparelhamento de nós com o objetivo de resolver o problema de alocação Alunos-Projeto.

Os seguintes algoritmos são utilizados:
- Project-Proposing (Adaptação do Gale-Shapley em que os Projetos pedem aos Alunos para realizar a alocação)
- Student-Proposing (Adaptação do Gale-Shapley em que os Alunos pedem aos Projetos para realizar a alocação)
- Max-Cardinality-Stable-Matching (Utiliza um solver com restrições para encontrar um emparelhamento estável de maior cardinalidade)

O programa também implementa uma interface de terminal para escolha de qual algoritmo executar, bem como para leitura e visualização dos
dados gerados após a execução, como:
- Visualização das Gerações de Grafos de cada Iteração do Algoritmo
- Visualização de Dados sobre o emparelhamento final de cada Iteração
- Visualização de Matriz de emparelhamento de cada Iteração
- Visualização de Índice de preferência por Projeto


Este código foi realizado utilizando Python 3.12.10, 
O código necessita das seguintes dependências:
1. re;
2. networkx;
3. matplotlib;
4. deepcopy;
5. seaborn;
6. pandas;
7. random.
Caso alguma dessas dependências esteja faltando, utilize o pip para as instalar (no terminal: pip install "nome da dependencia")

Para rodar o código inteiro utilize no terminal: python main.py (MANEIRA RECOMENDADA)

Para a análise do código de forma separada foi utilizado o arquivo Emparelhamento.ipynb (Notebook)
Foi utilizado a extensão do Jupyter no Visual Studio Code + Pacote ipyKernel

Passo a Passo:
1. Instale as Dependências;
2. Abra o Visual Studio Code;
3. Instale a extensão do Jupyter (na aba extensões);
4. Rode um dos blocos de código no Notebook;
5. Aceite a instalação do pacote ipyKernel;
6. Rode o bloco de código novamente.

O cógigo necessita do dadosAlunos.txt e dadosProjetos.txt estarem no mesmo diretório de execução.

É possível que este arquivo também rode no Jupyter Notebook nativo.

Passo a passo:
1. Abra o terminal;
2. digite (pip install jupyterlab) e espere a instalação;
3. utilize (cd "Caminho para este diretório") para chegar até PROJETO2TAG;
4. digite (python -m jupyterlab) (ou algum desses outros comandos: jupyter lab, python -m lab, python -m jupyter-lab, python -m jupyter lab);
5. utilize o Jupyter no navegador;
6. Instale as Dependências antes de rodar o código.

Também é possível utilizar o código dentro de um ambiente do Google Collab, em https://colab.research.google.com (basta fazer upload de Emparelhamento.ipynb, dadosAlunos.txt e dadosProjetos.txt em um diretório)
