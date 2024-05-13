from random import random, choice
from time import time
from math import exp
import matplotlib.pyplot as plt
from .travelingSalesman import TravelingSalesman
        
class SimulatedAnnealing(TravelingSalesman):
        """ 
            SimulatedAnnealing class for using SimulatedAnnealing for solving the Travelling salesman problem.

            Attributes:
            _simulations (number) representing the number of simulations the algorithm will run by.        
            _T0 (number) representing the intial temperature variable the algorithm will use.        
        """ 
        def __init__(self, T0: int = 100):
            TravelingSalesman.__init__(self)
            self._simulations = T0 #100 by defult
            self._T0 = T0 #100 by defult

        def cooling_fun(self, k):        
            n = 1
            T = max((self._T0 - n * k), 0)           
            return T
        
        def genrate_init_path(self):
            path_len = len(self._cities_coord)
            init_path = [i+1 for i in range(path_len)]      
            init_path.append(init_path[0]) 
            return init_path
        

        def genrate_random_path(self):  
            all_cities = self._cities_coord  
            nodes = [i+1 for i in range(len(all_cities))]   
            random_path = []
            while (len(random_path) != len(all_cities)):               
                rand_node = choice(nodes)
                if rand_node not in random_path:
                     random_path.append(rand_node)

            random_path.append(random_path[0])

            return random_path
        
        def simulated_annealing(self):
            T = self._T0
            temperatures = []
            costs = []

            print('--------- solving TSP with simulated annealing ---------')
            start_time = time()
            routes_costs = self.get_routes_costs() 
            init_path = self.genrate_init_path()
            min_cost = self.calc_path_cost(init_path, routes_costs)   

            for i in range(self._simulations):    
                x0 = self.calc_path_cost(init_path, routes_costs)
                    
                random_path = self.genrate_random_path()           
                x1 = self.calc_path_cost(random_path, routes_costs)         

                # if minimized
                if x1 < x0:
                    init_path = [*random_path]
                    x0 = x1
                else:
                    r = round(random(), 3)
                    test = (x0 - x1) / T
                    if r < exp(test):
                        init_path = [*random_path]
                        x0 = x1

                T = self.cooling_fun(i+1)

                if i%10 == 0:
                    temperatures.append(T)
                    costs.append(x0)
                min_cost = min(min_cost, x0)

            print(f'--------- %s seconds --------- {round(time() - start_time, 3)}\n\n')
            plt.plot(temperatures, costs, color = 'blue')
            plt.xticks(temperatures)
            plt.xlabel('temperatures')
            plt.ylabel('avrage cost')
            plt.title(f'Solving TSP using Simulated Annealing, T0 = {self._T0} \n {round(min(costs))} is the best avrage cost after {self._simulations} simulations')
            plt.show() 
          
            return min_cost, init_path

         
