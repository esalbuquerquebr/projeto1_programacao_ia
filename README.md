# Projeto 1 de Programaço 1 - Algoritmos de busca/otimização
### Disciplina: Inteligência Artificial
##### IFES | 2020/1

## Organização
-Código-fonte: ./scr/**
-Relatório: ./rel/relatorio.pdf
-Gráficos: ./rel/imgs/**
-Dados gerados: ./rel/csv/**

### Instruções para executar:

##### ./src/projeto_prog_1/runner.py

Responsável por executar um algoritmo para um determinado problema

Exemplos: 

- executar Genetic Algorithm para o problema 1 e código de execução (rodada | entradas definida) 5
```python
    result = execute_one("GeneticAlgorithm", problem_number=1, exec_code=5)
``` 

- executar o Hill Climbing simples para o problema 2 e execuções 1 até 10.

```python
    result = execute("SimpleHillClimbing", problem_number=2, exec_codes=[1,2,3,4,5,6,7,8,9,10])

##### ./src/projeto_prog_1/run_to_csv.py

Responsável por executar um algoritmo para um problema e gerar um CSV para todos códigos de execução (rodadas | entradas definidas)

Exemplos: 

- executar Simulated Annealing para o problema 1 e gerar o CSV em 'c:/Temp/resultados/'
```python
    result = run_to_csv("SimulatedAnnealing", problem_number=1, output_csvfile='c:/Temp/resultados/')
``` 

##### ./src/projeto_prog_1/run_to_chat.py

Responsável por executar um algoritmo para um problema e gerar um gráfico para todos códigos de execução (rodadas | entradas definidas)

Exemplos: 

- executar Hill Climbing com restart para o problema 3 e exibe o gráfico
```python
    run_to_chart("RestartHillClimbing", problem_number=3)
``` 


##### ./src/projeto_prog_1/show_comparative_chart.py

Responsável por exibir um gráfico compatativo entre todos os 4 algoritmos. O gráfico é construído a partir dos CSVs gerados pelo 'run_to_csv.py' com o melhor resultado a cada iteração e o desvio padrão entre todas as execuções

Exemplos: 

- contruir o gráfico comparativo para o problema 3gráfico
```python
    show_comp(problem_number=3)
``` 

## Extra

##### ./src/projeto_prog_1/p1_view_walking.py

Responsável por exibir a evolução de cada algoritmo para o problema 1

Exemplos: 

- Exibir a evolução do Hill Climbing com restart
```python
    #SimpleHillClimbing
    shc_params = {'algorithm_name': "SimpleHillClimbing",'exec_code' : 1,'qtt_iter' : 1000,'qtt_points' : 1,'interval' : 100,'show_neighbor' : True,'show_current' : True}
    #RestartHillClimbing
    rhc_params = {'algorithm_name': "RestartHillClimbing",'exec_code' : 1,'qtt_iter' : 1000,'qtt_points' : 1,'interval' : 100,'show_neighbor' : True,'show_current' : True}
    #SimulatedAnnealing
    sa_params = {'algorithm_name': "SimulatedAnnealing",'exec_code' : 1,'qtt_iter' : 1000,'qtt_points' : 1,'interval' : 100,'show_neighbor' : True,'show_current' : True}
    #GeneticAlgorithm
    ga_params = {'algorithm_name': "GeneticAlgorithm",'exec_code' : 1,'qtt_iter' : 50,'qtt_points' : 20,'interval' : 100,'show_neighbor' : True,'show_current' : True}

    if __name__ == '__main__':

        #execute_view(**shc_params)
        execute_view(**rhc_params)
        #execute_view(**sa_params)
        #execute_view(**ga_params)

``` 

##### ./src/projeto_prog_1/p2_view_walking.py

Responsável por exibir a evolução de cada algoritmo para o problema 2

Exemplos: 

- Exibir a evolução do Simulated Annealing
```python
    #SimpleHillClimbing
    shc_params = {'algorithm_name': "SimpleHillClimbing",'exec_code' : 1,'qtt_iter' : 1000,'qtt_points' : 1,'interval' : 100,'show_neighbor' : True,'show_current' : True}
    #RestartHillClimbing
    rhc_params = {'algorithm_name': "RestartHillClimbing",'exec_code' : 1,'qtt_iter' : 1000,'qtt_points' : 1,'interval' : 100,'show_neighbor' : True,'show_current' : True}
    #SimulatedAnnealing
    sa_params = {'algorithm_name': "SimulatedAnnealing",'exec_code' : 1,'qtt_iter' : 1000,'qtt_points' : 1,'interval' : 100,'show_neighbor' : True,'show_current' : True}
    #GeneticAlgorithm
    ga_params = {'algorithm_name': "GeneticAlgorithm",'exec_code' : 1,'qtt_iter' : 50,'qtt_points' : 20,'interval' : 100,'show_neighbor' : True,'show_current' : True}


    if __name__ == '__main__':
        #execute_view(**shc_params)
        #execute_view(**rhc_params)
        execute_view(**sa_params)
        #execute_view(**ga_params)

``` 
