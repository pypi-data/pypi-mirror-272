import numpy as np

class TravelingSalesman: 
    """ 
        Generic TravelingSalesman class for Reading the pathes and 
        calculating the costs.

        Attributes:
        _cities_coord (list of list of numbers) representing the coordinates of the cities/nodes of the problem
        _routes_costs (list of numbers) representing the costs between each cities/nodes of the problem      
    """  
    def __init__(self):
        self._cities_coord = []
        self._routes_costs = []

    def read_routes_from_file(self, cities_map: str, cities_num: int):       
        #read x,y coordinates from a file
        with open(cities_map) as f:
            for _ in range(cities_num):           
                city = [round(float(c)) for c in f.readline()[:-1].split(' ')[1:]]
                self._cities_coord.append(city)  
        
        return self._cities_coord
    
    def read_routes_from_list(self, cities_map: list):  
        self._cities_coord = cities_map
        return self._cities_coord
    
    def get_routes_costs(self):        
        # calculate Euclidean distance
        for city1 in self._cities_coord:
            city_cost = []
            for city2 in self._cities_coord:
                dist = np.linalg.norm(np.array(city1) - np.array(city2))            
                city_cost.append(round(dist))
        
            self._routes_costs.append(city_cost)
    
        return self._routes_costs
    
    def calc_path_cost(self, path: list, routes_costs: list):
        costs = []      
        for city in range(len(path) - 1):
            city_from_idx  = path[city] - 1
            city_to_idx = path[city + 1] - 1
            costs.append(routes_costs[city_from_idx][city_to_idx])       

        return sum(costs)   
