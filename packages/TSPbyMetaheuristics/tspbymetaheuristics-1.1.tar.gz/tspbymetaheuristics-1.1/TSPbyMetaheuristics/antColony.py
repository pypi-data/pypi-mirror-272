import math
from random import randint, random, randrange
from time import time
import matplotlib.pyplot as plt
from .travelingSalesman import TravelingSalesman

class AntColony(TravelingSalesman):
    """ 
        AntColony class for using AntColony for solving the Travelling salesman problem.

        Attributes:
        _simulations (number) representing the number of simulations the algorithm will run by.        
        _genrations_num (number) representing the number of genrations the algorithm will use.        
        Beta (number) representing the Beta variable the algorithm will use.        
    """ 
    def __init__(self, genrations_num: int = 20, Beta: int = 5):
        TravelingSalesman.__init__(self)
        self._simulations = 20 #20 by defult
        self._genrations_num = genrations_num
        self._Beta = Beta

    
    def Roulette_wheel(self, possible_cities: list, probabilities: list):       
        Selection_probabilities = [round(p/sum(probabilities), 3) for p in probabilities]        
        Roulette_wheel = [] 
        wheel_sum = 0 
        for probability in Selection_probabilities:
            wheel_sum += probability
            Roulette_wheel.append(round(wheel_sum, 3))
        
        r = random() * 0.99        
    
        city_toGo_probability = min([p for p in Roulette_wheel if r < p])
        city_idx =  Roulette_wheel.index(city_toGo_probability)  
        city_toGo = possible_cities[city_idx]
        
        return city_toGo


    def pick_next_city(self, routes_costs, path, taw, Beta: int):
        cities = [c for c in range(1,len(routes_costs) + 1) if c not in path]
        current_city = path[-1]
        Alpha = 1        

        # get probability
        probabilities = []
        denominator = 0
        for next_city in cities:
            t = taw[current_city - 1][next_city - 1]
            d = routes_costs[current_city - 1][next_city - 1]
            denominator = denominator + (math.pow(t,Alpha) / math.pow(d,Beta))        

        for next_city in cities:
            t = taw[current_city - 1][next_city - 1]
            d = routes_costs[current_city - 1][next_city - 1]        
            Pij = (math.pow(t,Alpha) / math.pow(d,Beta)) / denominator
            probabilities.append(round(Pij ,5))

        picked_city = self.Roulette_wheel(cities, probabilities)
        return picked_city


    def update_pheromones(self, pathes: list ,taw_list: list, costs: list):   
        Q = 20
        p = 0.9
        delta_taw = [Q/cost for cost in costs]    
        new_taw = [[(1 - p)*taw_list[i][j] for i in range(len(taw_list))] for j in range(len(taw_list))] 
        
        for idx, path in enumerate(pathes):
            for c in range(len(path) - 1):
                city_from_idx  = path[c] - 1
                city_to_idx = path[c + 1] - 1
                new_taw[city_from_idx][city_to_idx] += delta_taw[idx]
                new_taw[city_to_idx][city_from_idx] += delta_taw[idx]      
    
        return new_taw 


    def AS(self, routes_costs, genrations_num: int, Beta: int):
        best_costs = []    
        best_pathes = []    
        n = len(routes_costs)
        N = len(routes_costs) + 1 #num of ants     
        #genrate random taw between 10**-6 and 10**-5
        taw = [[ 0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                r = math.pow(10, -7)*randrange(1,10)
                taw[i][j] = taw[j][i] = r if i != j else 0             
        
        for _ in range(genrations_num):      
            pathes = [[] for _ in range(N)] #create empty path of each ant   
            #Initialize the starting city of each ant
            for ant in range(N):
                city_1 = randint(1, n)
                pathes[ant].append(city_1)    
      
            for _ in range(n - 1):
                for k in range(N):                               
                    city_qk = self.pick_next_city(routes_costs, pathes[k], taw, Beta)
                    pathes[k].append(city_qk)

            #return to the first city
            for path in pathes:
                path.append(path[0])

            costs = [self.calc_path_cost(path, routes_costs) for path in pathes]
            taw = self.update_pheromones(pathes ,taw, costs)
            best_costs.append(min(costs))

            idx = costs.index(min(costs))           
            best_pathes.append(pathes[idx])

        best_path_idx = best_costs.index(min(best_costs))           
        min_path: list = best_pathes[best_path_idx]           
        min_cost: int = min(best_costs)

        return best_costs, min_cost, min_path


    def run_monte_carlo(self, simulations: int = 20):
        self._simulations = simulations
        genrations = [self._genrations_num for self._genrations_num in range(1, self._genrations_num + 1)]
        best = [0 for _ in range(self._genrations_num)]
        st = time()

        best_pathes_per_simulation = []
        best_cost_per_simulation = []

        routes_costs = self.get_routes_costs()

        for _ in range(self._simulations):
            best_AS, min_cost, min_path = self.AS(routes_costs, self._genrations_num, self._Beta)
            best_cost_per_simulation.append(min_cost)
            best_pathes_per_simulation.append(min_path)
            #sum of each genration of AS
            best = [best[i] + best_AS[i] for i in range(self._genrations_num)]

        #average of monte_carlo per each genration 
        best = [cost/self._simulations for cost in best]  

        plt.plot(genrations, best, color = 'blue')
        plt.xticks(genrations)
        plt.xlabel('genrations')
        plt.ylabel('avrage cost')
        plt.title(f'Solving TSP using Ant Colony, Beta = {self._Beta} \n {round(min(best))} is the best avrage cost after {self._simulations} monte carlo simulations')
        plt.show()  
    
        print(f'---------- total time : {round(time() - st, 3)} s ----------')

        best_path_idx = best_cost_per_simulation.index(min(best_cost_per_simulation))           
        best_path: list = best_pathes_per_simulation[best_path_idx]  

        return round(min(best)), best_path

