from flight import Flight
class Circular_Queue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.front = 0
        self.rear = 0
        self.size = 0

    def is_empty(self):
        return self.size == 0

    def is_full(self):
        return self.size == self.capacity

    def resize(self):
        # Double the capacity
        new_capacity = self.capacity * 2
        new_queue = [None] * new_capacity
        
        # Rearrange elements from the old queue to the new one
        for i in range(self.size):
            new_queue[i] = self.queue[(self.front + i) % self.capacity]
        
        # Update queue and pointers
        self.queue = new_queue
        self.front = 0
        self.rear = self.size
        self.capacity = new_capacity

    def enqueue(self, item):
        if self.is_full():
            self.resize()
        self.queue[self.rear] = item
        self.rear = (self.rear + 1) % self.capacity
        self.size += 1
        return True

    def dequeue(self):
        if self.is_empty():
            return None
        item = self.queue[self.front]
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return item

    def peek(self):
        if self.is_empty():
            return None
        return self.queue[self.front]

    def __str__(self):
        if self.is_empty():
            return "Empty"
        return " ".join(str(self.queue[(self.front + i) % self.capacity]) for i in range(self.size))

#####################################################################################################################################

class Node:
    def __init__(self, flight,index, data):
        self.flight = flight
        self.index = index
        self.data = data  ######### COMPARATOR OF ADAPTIVE HEAP

    def __str__(self):
        return f"Node(index={self.index}, data={self.data})"


#####################################################################################################################################


class AdaptiveHeap:
    def __init__(self):
        self.heap = []

    def insert(self, item):
        item.index = len(self.heap)  # Set the initial index of the new node
        self.heap.append(item)
        self.heapify_up(len(self.heap) - 1)

    def extract_min(self):
        if not self.heap:
            return None
        if len(self.heap) == 1:
            min_item = self.heap.pop()
            min_item.index = None  # Clear the index as it's removed from the heap
            return min_item
        min_item = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.heap[0].index = 0  # Update the index of the new root
        self.heapify_down(0)
        min_item.index = None  # Clear the index as it's removed from the heap
        return min_item

    def heapify_up(self, i):
        parent = (i - 1) // 2
        if parent >= 0 and self.heap[parent].data > self.heap[i].data:
            self.heap[parent], self.heap[i] = self.heap[i], self.heap[parent]
            # Update indices
            self.heap[parent].index = parent
            self.heap[i].index = i
            self.heapify_up(parent)

    def heapify_down(self, i):
        left = 2 * i + 1
        right = 2 * i + 2
        smallest = i
        if left < len(self.heap) and self.heap[left].data < self.heap[smallest].data:
            smallest = left
        if right < len(self.heap) and self.heap[right].data < self.heap[smallest].data:
            smallest = right
        if smallest != i:
            self.heap[smallest], self.heap[i] = self.heap[i], self.heap[smallest]
            # Update indices
            self.heap[smallest].index = smallest
            self.heap[i].index = i
            self.heapify_down(smallest)

    def __str__(self):
        return " ".join(str(item) for item in self.heap)

    
#####################################################################################################################################



class Planner:
    def __init__(self, flights):
        """The Planner

        Args:
            flights (List[Flight]): A list of information of all the flights (objects of class Flight)
        """
        self.flights = flights
        self.num_cities = 0
        for flight in flights:
            self.num_cities = max(self.num_cities, flight.start_city, flight.end_city)
        
        self.adjacency_list_flight_out = [[] for _ in range(self.num_cities+1)]
        self.adjacency_list_flight_in = [[] for _ in range(self.num_cities+1)]
        self.initialize_adjacency_list_flight()
        pass
    
    def initialize_adjacency_list_flight(self):
        """
        Initialize the adjacency list of the graph
        """
        for flight in self.flights:
            self.adjacency_list_flight_out[flight.start_city].append(flight)
        
        for flight in self.flights:
            self.adjacency_list_flight_in[flight.end_city].append(flight)
        pass
    
    def least_flights_earliest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        arrives the earliest
        """
        if(start_city == end_city):
            return []
        queue = Circular_Queue(1)
        visited = [False for _ in range(len(self.flights)+1)]
        parent = [-1 for _ in range(len(self.flights)+1)]
        number_of_flights = [float('inf') for _ in range(len(self.flights)+1)]
        path = []
        for flight in self.adjacency_list_flight_out[start_city]:
            if flight.departure_time >= t1 and flight.arrival_time <= t2:
                number_of_flights[flight.flight_no] = 1
                queue.enqueue(flight)
                visited[flight.flight_no] = True
                parent[flight.flight_no] = -1
        while not queue.is_empty(): 
            current = queue.dequeue()
            # if current.end_city == end_city:
            #     i = current
            #     while i != -1 and i.start_city != start_city:
            #         path.append(i)
            #         i = parent[i.flight_no]
            #     path.append(i)
            #     path.reverse()
                # return path if path[0]  != -1 else []
            for flight in self.adjacency_list_flight_out[current.end_city]:
                if flight.departure_time >= current.arrival_time + 20 and flight.arrival_time <= t2:
                    if not visited[flight.flight_no]:
                        number_of_flights[flight.flight_no] = min(number_of_flights[current.flight_no] + 1, number_of_flights[flight.flight_no])
                        queue.enqueue(flight)
                        visited[flight.flight_no] = True
                        parent[flight.flight_no] = current
        
        min_arrival_time = float('inf')
        shortest_number_of_flights = float('inf')
        i = None
        for flight in self.adjacency_list_flight_in[end_city]:
            if visited[flight.flight_no] and (number_of_flights[flight.flight_no], flight.arrival_time) < (shortest_number_of_flights, min_arrival_time):
                shortest_number_of_flights = number_of_flights[flight.flight_no]
                min_arrival_time = flight.arrival_time
                i = flight
                
                
        if i is None:
            return []
        path = []
        while i != -1 and i.start_city != start_city:
            path.append(i)
            i = parent[i.flight_no]
        path.append(i)
        path.reverse()
        return path if path[0]  != -1 else []
        pass
    
    def cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route is a cheapest route
        """
        #dijkstra
        #initialize
        if start_city == end_city:
            return []
        
        Nodes = [None for _ in range(len(self.flights)+1)]
        heap = AdaptiveHeap()
        visited = [False for _ in range(len(self.flights)+1)] 
        parent = [-1 for _ in range(len(self.flights)+1)]
        cheapest_flight_cost = [float('inf') for _ in range(len(self.flights)+1)] 
        cheapest_flight_cost[start_city] = 0
        
        # Initialize the heap with the flights from the start city
        
        for flight in self.adjacency_list_flight_out[start_city]:
            if flight.departure_time >= t1 and flight.arrival_time <= t2:
                if cheapest_flight_cost[flight.flight_no] > flight.fare:
                    cheapest_flight_cost[flight.flight_no] = flight.fare
                    parent[flight.flight_no] = -1
                    insertNode = Node(flight , None, cheapest_flight_cost[flight.flight_no]) 
                    heap.insert(insertNode)
                    visited[flight.flight_no] = True
                    Nodes[flight.flight_no] = insertNode
                

        while len(heap.heap) > 0:
            current = heap.extract_min()
            # visited[current.index] = True
            if(current.data == float('inf')):
                break
            
            for flight in self.adjacency_list_flight_out[current.flight.end_city]:
                if flight.departure_time >= current.flight.arrival_time + 20 and flight.arrival_time <= t2:
                    if cheapest_flight_cost[flight.flight_no] > cheapest_flight_cost[current.flight.flight_no] + flight.fare:
                        cheapest_flight_cost[flight.flight_no] = cheapest_flight_cost[current.flight.flight_no] + flight.fare
                        parent[flight.flight_no] = current.flight
                        visited[flight.flight_no] = True
                        if Nodes[flight.flight_no] is not None:
                            Nodes[flight.flight_no].data = cheapest_flight_cost[flight.flight_no]
                            heap.heapify_down(Nodes[flight.flight_no].index)
                            heap.heapify_up(Nodes[flight.flight_no].index)
                        else:
                            insertNode = Node(flight , None, cheapest_flight_cost[flight.flight_no]) 
                            heap.insert(insertNode)
                            Nodes[flight.flight_no] = insertNode
                    
        # print(cheapest_flight_cost)
        cheapest_flight = None
        for i in self.adjacency_list_flight_in[end_city]:
            if not cheapest_flight and visited[i.flight_no]:
                cheapest_flight = i
            elif cheapest_flight and  cheapest_flight_cost[i.flight_no] < cheapest_flight_cost[cheapest_flight.flight_no]:
                cheapest_flight = i
        i = cheapest_flight
        if i is None:
            return []
        path = []
        while i != -1 and i.start_city != start_city:
            path.append(i)
            i = parent[i.flight_no]
        path.append(i)
        path.reverse()
        return path if path[0]  != -1 else []
        
        
        
        pass
    
    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        is the cheapest
        """
        #dijkstra
        #initialize
        if start_city == end_city:
            return []
        
        Nodes = [None for _ in range(len(self.flights)+1)]
        heap = AdaptiveHeap()
        visited = [False for _ in range(len(self.flights)+1)] 
        parent = [-1 for _ in range(len(self.flights)+1)]
        cheapest_flight_cost = [(float('inf'),float('inf')) for _ in range(len(self.flights)+1)] 
        # cheapest_flight_cost[start_city] = 0
        
        # Initialize the heap with the flights from the start city
        
        for flight in self.adjacency_list_flight_out[start_city]:
            if flight.departure_time >= t1 and flight.arrival_time <= t2:
                if cheapest_flight_cost[flight.flight_no] > (0,flight.fare):
                    cheapest_flight_cost[flight.flight_no] = (0,flight.fare)
                    parent[flight.flight_no] = -1
                    insertNode = Node(flight , None, cheapest_flight_cost[flight.flight_no]) 
                    heap.insert(insertNode)
                    visited[flight.flight_no] = True
                    Nodes[flight.flight_no] = insertNode

        while len(heap.heap) > 0:
            current = heap.extract_min()
            # visited[current.index] = True
            if(current.data == float('inf')):
                break
            
            for flight in self.adjacency_list_flight_out[current.flight.end_city]:
                if flight.departure_time >= current.flight.arrival_time + 20 and flight.arrival_time <= t2:
                    check_tuple = (cheapest_flight_cost[current.flight.flight_no][0] + 1, cheapest_flight_cost[current.flight.flight_no][1] + flight.fare)
                    if cheapest_flight_cost[flight.flight_no] > check_tuple:
                        cheapest_flight_cost[flight.flight_no] = check_tuple
                        parent[flight.flight_no] = current.flight
                        visited[flight.flight_no] = True
                        if Nodes[flight.flight_no] is not None:
                            Nodes[flight.flight_no].data = cheapest_flight_cost[flight.flight_no]
                            heap.heapify_down(Nodes[flight.flight_no].index)
                            heap.heapify_up(Nodes[flight.flight_no].index)
                        else:
                            insertNode = Node(flight , None, cheapest_flight_cost[flight.flight_no]) 
                            heap.insert(insertNode)
                            Nodes[flight.flight_no] = insertNode
                    
        # print(cheapest_flight_cost)
        cheapest_flight = None
        for i in self.adjacency_list_flight_in[end_city]:
            if not cheapest_flight and visited[i.flight_no]:
                cheapest_flight = i
            elif cheapest_flight and  cheapest_flight_cost[i.flight_no] < cheapest_flight_cost[cheapest_flight.flight_no]:
                cheapest_flight = i
        i = cheapest_flight
        if i is None:
            return []
        path = []
        while i != -1 and i.start_city != start_city:
            path.append(i)
            i = parent[i.flight_no]
        path.append(i)
        path.reverse()
        return path if path[0]  != -1 else []
        
        
        pass
    
if __name__ == "__main__":
    flights = [
        # Cheaper path that leads to dead end
        Flight(0, 0, 0, 1, 60, 200),    # 1->2, fare=10
        Flight(1, 0, 0, 2, 15, 300),   # 2->3, fare=15
        
        # More expensive path that reaches destination
        Flight(2, 2, 35, 1, 40, 100),    # 1->4, fare=25
        Flight(3, 1, 60, 3, 80, 200),   # 4->5, fare=30  
    ]
    flight_planner = Planner(flights)
    route2 = flight_planner.least_flights_earliest_route(0,3 , 0, 1000)
    print([i.flight_no for i in route2])