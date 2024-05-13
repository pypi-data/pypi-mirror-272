from random import choice
from time import time
import matplotlib.pyplot as plt
from .travelingSalesman import TravelingSalesman

class HillClimbing(TravelingSalesman):
        """ 
            HillClimbing class for using HillClimbing (steepest ascent version) for solving the Travelling salesman problem.

            Attributes:
            _simulations (number) representing the number of simulations the algorithm will run by.        
        """ 
        def __init__(self, simulations: int = 100):
            TravelingSalesman.__init__(self)
            self._simulations = simulations #100 by defult        

        def genrate_init_path(self):
            all_cities = self._cities_coord  
            nodes = [i+1 for i in range(len(all_cities))]  
            init_path =[]           
            while (len(init_path) != len(all_cities)):               
                rand_node = choice(nodes)
                if rand_node not in init_path:
                     init_path.append(rand_node)

            init_path.append(init_path[0])                
            return init_path        

        def genrate_random_path(self, current_path: list, k: int):  
            all_cities = self._cities_coord  
            nodes = [i+1 for i in range(len(all_cities))]  
            random_path = current_path[:k]                
            while (len(random_path) != len(all_cities)):               
                rand_node = choice(nodes)
                if rand_node not in random_path:
                     random_path.append(rand_node)

            random_path.append(random_path[0])  
            return random_path
      
        def steepest_ascent(self):
            simulations = [i for i in range(self._simulations)]         
            costs = []
            start_time = time()

            print(f'------------ solving TSP with steepest ascent ------------')
            routes_costs = self.get_routes_costs() 

            for i in range(self._simulations):
                init_path = self.genrate_init_path()     
                x0 = self.calc_path_cost(init_path, routes_costs)              
                
                random_pathes_costs = [] 
                random_pathes = []
                random_pathes.append(init_path)

                cities_num = len(self._cities_coord)
                for k in range(1, cities_num): 
                    random_path = self.genrate_random_path(init_path, k)        
                    if random_path not in random_pathes:
                        random_pathes.append(random_path)
                        x1 = self.calc_path_cost(random_path, routes_costs)
                        random_pathes_costs.append(x1)
            
                min_cost = min(random_pathes_costs)
                idx = random_pathes_costs.index(min_cost)
                best_path = random_pathes[idx]

                if min_cost < x0:
                    x0 = min_cost
                    init_path = best_path

                costs.append(min(random_pathes_costs))
        
            print(f'--------- %s seconds --------- {round(time() - start_time, 3)} sec\n\n')
            plt.plot(simulations, costs, color = 'blue')
            plt.xticks(simulations)
            plt.xlabel('simulations')
            plt.ylabel('avrage cost')
            plt.title(f'Solving TSP using steepest_ascent Hill Climbing \n {round(min(costs))} is the best avrage cost after {self._simulations} simulations')
            plt.show() 
          
            return min(costs), init_path       

