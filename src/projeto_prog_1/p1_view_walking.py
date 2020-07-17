"""
Módulo para vizualização da caminhada para o problema 1 - Genérico

"""
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from factory import get_factory

def plot_fn_goal(ax1, title, qtt_points):
    ax1.set_title(title)  
    ax1_x = np.linspace(-100, 100, num=1000)
    ax1_y = (ax1_x ** 2 / 100) + (10 * np.sin(ax1_x - (np.pi / 2)))
    ax1.plot(ax1_x, ax1_y)

    neighbor_points = []
    current_points = []
    for i in range(0, qtt_points):
        neighbor, = ax1.plot([],[], marker="o", color="blue", ms=5, label="Neighbor")
        neighbor_points.append(neighbor)

        current, = ax1.plot([],[], marker="o", color="red", ms=5, label="Current")
        current_points.append(current)
    
    best_point, = ax1.plot([], [], marker="D", color="green", ms=5, label="Best")

    return (neighbor_points, current_points, best_point)

def plot_evolution(ax2, title, qtt_points, qtt_iter):
    ax2.set_title(title)
    ax2.set_xlabel('Iteration') 
    ax2.set_ylabel('Fitness')
    
    ax2.set_xlim(0, qtt_iter)
    ax2.set_ylim(-20, 120)
    ax2.plot([], [])

    neighbor_line, = ax2.plot([], [], 'b-', label='Neighbor')
    current_line, = ax2.plot([], [], 'r-', label='Current')
    best_line, = ax2.plot([], [], 'g-', label='Best')
    return neighbor_line, current_line, best_line    

def execute_view(algorithm_name, exec_code=1, qtt_iter=1000, qtt_points=1, interval=100, show_neighbor=True, show_current=True):

    factory = get_factory(algorithm_name, problem_number=1)
    algorithm = factory(exec_code=exec_code)

    plt.style.use('bmh')
    fig, (ax1, ax2) = plt.subplots(2, 1)
    neighbor_points, current_points, best_point = plot_fn_goal(ax1, f'{algorithm_name} walking', qtt_points)
    neighbor_line, current_line, best_line = plot_evolution(ax2, f'{algorithm_name} evolution', qtt_points, qtt_iter)


    def init_anime():
       
        #ax1
        for i in range(qtt_points):
            neighbor_points[i].set_data([], [])
            current_points[i].set_data([], [])
        best_point.set_data([],[])

        #ax2
        neighbor_line.set_data([], [])
        current_line.set_data([], [])
        best_line.set_data([], [])

        return neighbor_points + current_points + [best_point, neighbor_line, current_line, best_line]

    def animate(i):
        neighbor_state, current_state, best_state = algorithm.__next__()
        if qtt_points == 1:
            neighbor_state = [neighbor_state] if neighbor_state else []
            current_state =  [current_state] if current_state else []
        else:
            neighbor_state = neighbor_state.states if neighbor_state else []
            current_state =  current_state.states if current_state else []

        if neighbor_state and show_neighbor:
            for i in range(0, qtt_points):
                #ax1
                neighbor_points[i].set_data(neighbor_state[i].value, neighbor_state[i].fitness)

            #ax2
            neighbor_line.set_ydata(np.append(neighbor_line.get_ydata(), neighbor_state[0].fitness))
            neighbor_line.set_xdata(np.append(neighbor_line.get_xdata(), algorithm.iteration))            
            
        if current_state and show_current:
            for i in range(0, qtt_points):
                #ax1
                current_points[i].set_data(current_state[i].value, current_state[i].fitness)

            #ax2
            current_line.set_ydata(np.append(current_line.get_ydata(), current_state[0].fitness))
            current_line.set_xdata(np.append(current_line.get_xdata(), algorithm.iteration))            

        if best_state:
            #ax1
            best_point.set_data(best_state.value, best_state.fitness)

            #ax2
            best_line.set_xdata(np.append(best_line.get_xdata(), algorithm.iteration))
            best_line.set_ydata(np.append(best_line.get_ydata(), best_state.fitness))

        return neighbor_points + current_points + [best_point, neighbor_line, current_line, best_line]

    animetion = FuncAnimation(fig, animate, init_func=init_anime, frames=qtt_iter, interval=interval, blit=True)
    wm = plt.get_current_fig_manager()
    wm.window.state('zoomed')
    plt.show()

#SimpleHillClimbing
shc_params = {'algorithm_name': "SimpleHillClimbing",'exec_code' : 1,'qtt_iter' : 1000,'qtt_points' : 1,'interval' : 100,'show_neighbor' : True,'show_current' : True}
#RestartHillClimbing
rhc_params = {'algorithm_name': "RestartHillClimbing",'exec_code' : 1,'qtt_iter' : 1000,'qtt_points' : 1,'interval' : 100,'show_neighbor' : True,'show_current' : True}
#SimulatedAnnealing
sa_params = {'algorithm_name': "SimulatedAnnealing",'exec_code' : 1,'qtt_iter' : 1000,'qtt_points' : 1,'interval' : 100,'show_neighbor' : True,'show_current' : True}
#GeneticAlgorithm
ga_params = {'algorithm_name': "GeneticAlgorithm",'exec_code' : 1,'qtt_iter' : 50,'qtt_points' : 20,'interval' : 100,'show_neighbor' : True,'show_current' : True}

if __name__ == '__main__':

    execute_view(**rhc_params)
