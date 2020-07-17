"""
Módulo para vizualização da caminhada para o problema 2 - Genérico

"""
import numpy as np
from matplotlib import cm 
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import math
import numpy as np
from factory import get_factory




def plot_fn_goal(ax, title, qtt_points):

    ax.set_title(title)

    X = np.linspace(-5.12, 5.12, 200)    
    Y = np.linspace(-5.12, 5.12, 200)
    X, Y = np.meshgrid(X, Y)
    Z = (X**2 - 10 * np.cos(2 * np.pi * X)) + (Y**2 - 10 * np.cos(2 * np.pi * Y)) + 20

    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap="jet", alpha=0.1, linewidth=0, antialiased=True, vmin=0)    

    neighbor_points = []
    current_points = []
    for i in range(0, qtt_points):
        neighbor, = ax.plot([],[], marker="o", color="blue", ms=5, label="Neighbor")
        neighbor_points.append(neighbor)
        current, = ax.plot([],[], marker="o", color="red", ms=5, label="Current")
        current_points.append(current)

    best_point, = ax.plot([], [], marker="D", color="green", ms=5, label="Best")

    return (neighbor_points, current_points, best_point)

def execute_view(algorithm_name, exec_code=1, qtt_iter=1000, qtt_points=1, interval=100, show_neighbor=True, show_current=True):

    factory = get_factory(algorithm_name, problem_number=2)
    algorithm = factory(exec_code=exec_code)

    plt.style.use('bmh')
    fig = plt.figure()
    ax1 = fig.gca(projection='3d')

    neighbor_points, current_points, best_point = plot_fn_goal(ax1, f'{algorithm_name} walking', qtt_points)

    def init_anime():
        #ax1
        for i in range(qtt_points):
            neighbor_points[i].set_data_3d([],[],[])
            current_points[i].set_data_3d([],[],[])
        best_point.set_data_3d([],[],[])

        return neighbor_points + current_points + [best_point]

    def animate(i):
        neighbor_state, current_state, best_state = algorithm.__next__()
        if qtt_points == 1:
            neighbor_state = [neighbor_state] if neighbor_state else []
            current_state =  [current_state] if current_state else []
        else:
            neighbor_state = neighbor_state.states if neighbor_state else []
            current_state =  current_state.states if current_state else []        

        #ax1
        if show_neighbor and neighbor_state:
            #ax1
            for i in range(0, qtt_points):
                neighbor_points[i].set_data_3d(neighbor_state[i].value[0], neighbor_state[i].value[1], neighbor_state[i].fitness)

        if show_current and current_state:
            #ax1
            for i in range(0, qtt_points):
                current_points[i].set_data_3d(current_state[i].value[0], current_state[i].value[1], current_state[i].fitness)

        if best_state:
            #ax1
            best_point.set_data_3d([best_state.value[0]], [best_state.value[1]], [best_state.fitness])

        return neighbor_points + current_points + [best_point]

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
    #execute_view(**shc_params)
    #execute_view(**rhc_params)
    execute_view(**sa_params)
    #execute_view(**ga_params)
