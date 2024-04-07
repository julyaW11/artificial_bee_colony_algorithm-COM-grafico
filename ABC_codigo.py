import pygame
import random 
import numpy as np
import sys
#Função Obejtivo
def objective_function(x):
    return np.sum(x**2)


# Inicialização do Pygame
pygame.init()

# Parâmetros gráficos
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

def  artificial_bee_colony_algorithm(objective_function, num_variables_vector, num_employed_bees,num_onlooker_bess,num_max_interations):
    
    """
    Função que irá executar o -atificil bee colony algorithm-
    Esta recebe os seguintes parâmetros: 
    
    objetctive_function: Função objetiva que buscamos otimizar
    num_variables_vector : Tamanho do vetor que contêm as soluções. 
    num_employed_bees : numero de abelhas empregadas
    num_onlooker_bees: numero de abelhas observadoras
    mum_max_interactions: numero interações(loop) que irá ocorrer
    """

    population_visual = np.random.uniform(low=-10,high=10,size=(num_employed_bees,num_variables_vector))
    
    
    #Inicializando solução global
    best_solution = None  #vetor com os numeros
    best_fitness = float ('inf') #resultado do somatório
    
    
    
    for interations in range(num_max_interations):
        
        best_solutions_for_drawing = [] # Initialize an empty list to store the best solutions for drawing
        running = True
        iteration = 0
        
        while running and iteration <= num_max_iterations:
            
        
            #Fase abelhas empregadas
            for c in range(num_employed_bees):
                solution = population_visual[c]
                
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                
                #PERTUBA a solução atual em busca de melhor solução.
                new_solution = solution + np.random.uniform(low=-1, high=1, size=num_variables_vector)
                
                fitness = objective_function(new_solution) #objective_function(função) recebe como parâmetro(new_soluction)
                
                if fitness < objective_function(solution):
                    population_visual[c]= new_solution
                    
                    if fitness < best_fitness:
                        best_solution = new_solution
                        best_fitness = fitness
            
            #Fase das abelhas observadoras            
            for c in range(num_onlooker_bess):
                
                solution = random.choice(population_visual)
                
                new_solution = solution + np.random.uniform(low=-1, high=1,size=num_variables_vector)
                
                fitness = objective_function(new_solution) 
                
                
                if fitness < objective_function(solution): #SE o novo "fitness" se mostrar melhor que o atual "fitness", faremos os passos abaixo:
                    index = np.where(population_visual == solution)[0][0] #joga o vetor solução para a posição [0][0] da matriz população
                    population_visual[index] = new_solution ##Atualiza a população colocondo OUTRO vetor no lugar do vetor solução.

                    if fitness < best_fitness:
                        best_solution = new_solution
                        best_fitness = fitness
                        
           

            screen.fill((255, 255, 255))  # Fundo branco
            
           
            # Desenha a função objetivo
            x_vals = np.linspace(-10, 10, 1000)
            print(x_vals)
            y_vals = np.array([objective_function(x) for x in x_vals])
            pygame.draw.line(screen, (0, 0, 0), (0, height//2), (width, height//2), 2)  # Eixo X
            pygame.draw.line(screen, (0, 0, 0), (width//2, 0), (width//2, height), 2)  # Eixo Y
            pygame.draw.lines(screen, (255, 0, 0), False, [(int((x+10)*(width/20)), int(height/2 - y*height/200)) for x, y in zip(x_vals, y_vals)], 2)
    


            # Draw the best solution line
            if best_solution is not None:
                best_solutions_for_drawing.append(best_solution.copy())
                pygame.draw.lines(screen, (0, 255, 0), False, [(int((x + 10) * (width / 20)), int(height / 2 - objective_function(x) * height / 200)) for x in x_vals], 2)
            # Desenha as "abelhas"
            for solution in population_visual:
                x_bee = int((solution[0] + 10) * (width / 20))
                y_bee = int(height / 2 - solution[1] * height / 20)
                pygame.draw.circle(screen, (0, 0, 0), (x_bee, y_bee), 5)

            pygame.display.flip()
            clock.tick(10)  # Ajuste a velocidade da animação conforme necessário
            iteration += 1
            
            
            #Fase das abelhas batedoras(escoteiras), existe para GARANTIR que multiplas possibilidades sejam exploradas.   
            for c in range(num_employed_bees):
                if objective_function(population_visual[c]) >= objective_function(best_solution): #verifica se a aptidão(fitness) da solução atual é maior ou igual à aptidão da melhor solução encontrada até o momento (melhor_solução).
                    population_visual[c] = np.random.uniform(low=-10, high=10, size=num_variables_vector) #Se a condição for verdadeira,  o vetor população[i] é 
                    #substituído por uma nova solução gerada pela amostragem de valores aleatórios de uma distribuição uniforme dentro do intervalo [-10, 10]
    

            best_solutions_for_drawing.append(best_solution.copy())
            

            
    return best_solution, best_fitness         

#Parâmetros
num_variables_vector = 10
num_employed_bees = 20
num_onlooker_bees = 20
num_max_iterations = 100

#Roda o algorítimo
best_solution, best_fitness = artificial_bee_colony_algorithm(objective_function, num_variables_vector, num_employed_bees, num_onlooker_bees, num_max_iterations)
pygame.quit()
sys.exit()
#Printa "best_solution" e "best_fitness"
#print("Best Solution(vetor_solução):", best_solution)
#print()
#print("Best Fitness(somatorio_vetor_solução):", best_fitness)
