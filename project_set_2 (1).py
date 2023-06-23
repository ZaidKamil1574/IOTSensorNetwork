import random
import numpy as np
import time

def Greedy1_Algo(Graph, source, destination, budget_left):
    
    start_time = time.time()
    # Initaializing route, current node, prize collected, cost, list of unvisited nodes  
    Route = [source]
    Prize_collected = 0
    Cost = 0
    Unvisited_nodes = []
    for i in Graph['all_nodes']:
        Unvisited_nodes.append((Graph['data'][i], i))
    Unvisited_nodes.remove((Graph['data'][source], source))
    curr_node = source

    # Sorting the unvisited nodes in the descending order of its data.
    Unvisited_nodes.sort(reverse=True)
    
    while True:

        if len(Unvisited_nodes) == 0:
            break
            
        # Finding next unvisited node which is feasible and has largest prize.
        
        new_node = Unvisited_nodes[0][1]
        if Graph['cost'][curr_node][new_node] + Graph['cost'][new_node][destination] <= budget_left:
            Route.append(new_node)
            budget_left -= Graph['cost'][curr_node][new_node]
            Cost += Graph['cost'][curr_node][new_node]
            Prize_collected += Graph['data'][new_node]
            curr_node = new_node

        Unvisited_nodes.pop(0)    

    # Adding destination node to the route.
    Route.append(destination)
    budget_left -= Graph['cost'][curr_node][destination]
    Cost += Graph['cost'][curr_node][destination]
    Prize_collected += Graph['data'][destination]

    budget_left = budget_left/0.002
    Cost = Cost/0.002

    end_time = time.time()
    print()
    print("Results for Greedy1 Algorithm are as follows:")
    print("Route taken by the Robot: ", Route)
    print("Total Prize Collected by the Robot: ", Prize_collected)
    print("Total cost of the route taken bt Robot: ", Cost)
    print("Energy left in the Robot: ", budget_left)
    print("Running time for this algorithm: ", end_time - start_time)


def Greedy2_Algo(Graph, source, destination, budget_left):
  
    start_time = time.time()
    
    # Initaializing route, current node, prize collected, cost, list of unvisited nodes  
    Route = [source]
    Prize_collected = 0
    Cost = 0
    curr_node = source

    while True:
      
        Unvisited_nodes = []
        for node in Graph['all_nodes']:
            if node in Graph['edges'][curr_node] and node not in Route:
                Unvisited_nodes.append((Graph['data'][node]/Graph['cost'][node][curr_node], node))
        
        Unvisited_nodes.sort(reverse=True)
        
        while len(Unvisited_nodes):

            # Find the unvisited node with the largest prize that is in the feasible set.
            new_node = Unvisited_nodes[0][1]
            if Graph['cost'][curr_node][new_node] + Graph['cost'][new_node][destination] <= budget_left:
                Route.append(new_node)
                budget_left -= Graph['cost'][curr_node][new_node]
                Cost += Graph['cost'][curr_node][new_node]
                Prize_collected += Graph['data'][new_node]
                curr_node = new_node
                break
            
            Unvisited_nodes.pop(0)
        
        if len(Unvisited_nodes) == 0:
            break

    # Adding destination node to the route.
    Route.append(destination)
    budget_left -= Graph['cost'][curr_node][destination]
    Cost += Graph['cost'][curr_node][destination]
    Prize_collected += Graph['data'][destination]

    budget_left = budget_left/0.002
    Cost = Cost/0.002

    end_time = time.time()
    print()
    print("Results for Greedy2 Algorithm are as follows:")
    print("Route taken by the Robot: ", Route)
    print("Total Prize Collected by the Robot: ", Prize_collected)
    print("Total cost of the route taken bt Robot: ", Cost)
    print("Energy left in the Robot: ", budget_left)
    print("Running time for this algorithm: ", end_time - start_time)


def MARL_Algo(Graph, source, destination, budget_left):

    start_time = time.time()

    #initializing number of episodes and agents
    # total_episodes = random.randint(1, 100)
    # total_agents = random.randint(1, 100)  

    total_episodes = 100
    total_agents = 100

    # Initializing other important variables
    agents_U_nodes = []
    agents_budget_left = []
    agents_Routes = [] 
    agents_cost = []
    agents_data_coll = []
    agents_curr_node = []
    agents_isDone = []
    
    for i in range(total_agents):
        agents_U_nodes.append([])
        agents_U_nodes[i] = Graph['all_nodes'].copy()
        agents_U_nodes[i].pop(source)
        agents_budget_left.append(budget_left)
        agents_Routes.append([])
        agents_data_coll.append(0)
        agents_cost.append(0)
        agents_curr_node.append(source)
        agents_isDone.append(False)
    
    # Initializing Q value and rewards of edges
    Q_value = {}
    Rewards = {} 

    for node1 in range(len(Graph['all_nodes'])):
        for node2 in Graph['edges'][node1]:
            Q_value[(node1, node2)] = (Graph['data'][node1] + Graph['data'][node2])/Graph['cost'][node1][node2]
            Q_value[(node1, node2)] = (Graph['data'][node1] + Graph['data'][node2])/Graph['cost'][node1][node2]
            
    for node1 in range(len(Graph['all_nodes'])):
        for node2 in Graph['edges'][node1]:
            Rewards[(node1, node2)] = float('-inf')
            Rewards[(node2, node1)] = float('-inf')
            if Graph['data'][node2] != 0:
                Rewards[(node1, node2)] = -Graph['cost'][node1][node2]/Graph['data'][node2]
            if Graph['data'][node1] != 0:
                Rewards[(node2, node1)] = -Graph['cost'][node1][node2]/Graph['data'][node1]

    # Initializing some important varibles with given default value
    a = 0.1
    b = 2  
    c = 0.3 
    d = 1 
    w = 10 
    q0 = 0.5 

    # Learning phase starts here
    episodes_left = total_episodes 
    while True:

        if episodes_left == 0:
            break
        
        episodes_left -= 1
        for i in range(total_agents):
            agents_U_nodes[i] = Graph['all_nodes'].copy()
            agents_U_nodes[i].pop(source)
            agents_budget_left[i] = budget_left
            agents_Routes[i] = []
            agents_data_coll[i] = 0
            agents_cost[i] = 0
            agents_curr_node[i] = source
            agents_isDone[i] = False

        while True:
            
            isAllDone = True
            for j in range(total_agents):
                if agents_isDone == False:
                    isAllDone = False
            
            if isAllDone == True:
                break

            for j in range(total_agents):
                if agents_isDone[j] == False:
                    feasible_nodes = []
                    for node in agents_U_nodes[j]:
                        if Graph['cost'][agents_curr_node[j]][node] + Graph['cost'][node][destination] <= budget_left:
                            feasible_nodes.append(node)

                    if feasible_nodes != []:

                        next_node = None
                        q = random.uniform(0, 1)
                        if q>q0:
                            # finding next node using exploitation rule
                            nodes_probabilities = []
                            sum = 0
                            for node in feasible_nodes:
                                probability = ((Q_value[(agents_curr_node[j],node)] ** d) * Graph['data'][node]) / (Graph['cost'][agents_curr_node[j]][node] ** b)
                                nodes_probabilities.append(probability)
                                sum += probability
                            if sum == 0:
                                next_node = agents_U_nodes[j][0]
                            else:
                                probability_distribution = []
                                for prob in nodes_probabilities:
                                    probability_distribution.append(prob/sum)
                                next_node = random.choices(agents_U_nodes, weights = probability_distribution)[0]
                        
                        else:
                            # finding next node using exploitation rule
                            max = float('-inf')
                            for node in agents_U_nodes[j]:
                                val = ((Q_value[(agents_curr_node[j],node)] ** d) * Graph['data'][node]) / (Graph['cost'][agents_curr_node[j]][node] ** b)
                                if val > max:
                                    max = val
                                    next_node = node

                        agents_Routes[j].append(next_node)
                        agents_cost[j] += Graph['cost'][agents_curr_node[j]][next_node]
                        agents_budget_left[j] -= Graph['cost'][agents_curr_node[j]][next_node]
                        agents_data_coll[j] += Graph['data'][next_node]
                        
                        if agents_curr_node[j] != next_node:
                            max_val = 0
                            for node in agents_U_nodes:
                                if node not in Graph['edges'][next_node]:
                                    continue
                                if Q_value[(next_node, node)] > max_val:
                                    max_val = Q_value[(next_node, node)]
                            # Q value updated      
                            Q_value[(agents_curr_node[j], next_node)] = (1 - a) * Q_value[(agents_curr_node[j], next_node)] + a * c * max_val
                        
                        agents_curr_node[j] = next_node
                        agents_U_nodes[j].remove(next_node)

                    else:
                        agents_isDone[j] = True
                        agents_Routes[j].append(destination)
                        agents_cost[j] += Graph['cost'][agents_curr_node[j]][destination]
                        
                        if agents_curr_node[j] != next_node:
                            max_val = 0
                            for node in agents_U_nodes:
                                if node not in Graph['edges'][next_node]:
                                    continue
                                if Q_value[(next_node, node)] > max_val:
                                    max_val = Q_value[(next_node, node)]
                            # Q value updated      
                            Q_value[(agents_curr_node[j], next_node)] = (1 - a) * Q_value[(agents_curr_node[j], next_node)] + a * c * max_val

        # Updating reward values and Q-values for the edges in the route with maximum prize
        max_val = 0
        max_id = 0 
        for agent in range(total_agents):
            if agents_data_coll[agent] > max_val:
                max_val = agents_data_coll[agent]
                max_id = agent

        for node1, node2 in zip(agents_Routes[max_id][:-1], agents_Routes[max_id][1:]):
            if node1 != node2:
                Rewards[(node1, node2)] = Rewards[(node1, node2)] + w / agents_data_coll[max_id]
            
            # Updating Q-value
            if Rewards[(node1, node2)] == float('-inf'):
                continue
            if node1 != node2:
                max_val = 0
                for node in agents_U_nodes[max_id]:
                    if node not in Graph['edges'][node2]:
                        continue
                    if Q_value[(node1, node2)] > max_val:
                        max_val = Q_value[(node1, node2)]
                # Q value updated      
                Q_value[(node1, node2)] = (1 - a) * Q_value[(node1, node2)] + a *(Rewards[(node1, node2)] + c * max_val)

    
    Route = [source]
    Prize_collected = 0
    Cost = 0
    Unvisited_nodes = Graph['data'].copy()
    Unvisited_nodes.remove(source)
    curr_node = source
    
    # Execution stage
    while True:
        max_val = float('-inf')
        max_node = None
        for node in Graph['edges'][curr_node]:
            val = Q_value[(curr_node, node)]
            if val > max_val:
                if destination not in Graph['edges'][node] or node not in Unvisited_nodes:
                    continue
                if Graph['cost'][curr_node][node] + Graph['cost'][node][destination] <= budget_left:
                    max_val = val
                    max_node = node
        if max_node == None:
            break
        
        Route.append(max_node)
        Cost += Graph['cost'][curr_node][max_node]
        Prize_collected += Graph['data'][max_node]
        budget_left -= Graph['cost'][curr_node][max_node]
        curr_node = max_node
        Unvisited_nodes.remove(max_node)

    Route.append(destination)
    Cost += Graph['cost'][curr_node][destination]
    Prize_collected += Graph['data'][destination]
    budget_left -= Graph['cost'][curr_node][destination]
    
    budget_left = budget_left/0.002
    Cost = Cost/0.002

    end_time = time.time()
    print()
    print("Results for MARL Algorithm are as follows:")
    print("Route taken by the Robot: ", Route)
    print("Total Prize Collected by the Robot: ", Prize_collected)
    print("Total cost of the route taken bt Robot: ", Cost)
    print("Energy left in the Robot: ", budget_left)
    print("Running time for this algorithm: ", end_time - start_time)

def main():
    
    Graph = {} #initializing the graph

    print("Enter the following details:")
    print()

    # while loop to take inputs again and again graph is not completely connected
    while True:

        Graph['edges'] = []
        Graph['cost'] = []
        Graph['all_nodes'] = []
        Graph['data_nodes'] = []
        Graph['data'] = []
        Graph['node_coordinates'] = []

        # input the width, length, number of sensor nodes, transmission range, number of data nodes and budget
        
        # Using try-except to avoid incorrect inputs
        try:
            width = int(input("Sensor network width: "))
        except:
            width = 2000 

        try:   
            length = int(input("Sensor network length: "))
        except:
            length = 2000
        
        try:
            total_nodes = int(input("Number of sensor nodes: "))
        except:
            total_nodes = 100
        
        # Creating a list of all nodes in the Graph
        for i in range(total_nodes):
            Graph['all_nodes'].append(i)

        # Assigning random coordinates to all nodes in the Graph
        for node in Graph['all_nodes']:
            while True:
                x_coordinate = random.randint(1, width)
                y_coordinate = random.randint(1, length)
                if (x_coordinate, y_coordinate) not in Graph['node_coordinates']:
                    Graph['node_coordinates'].append((x_coordinate, y_coordinate))
                    break 

        try:
            Transmission_range = int(input("Transmission range of sensor nodes: "))
        except:
            Transmission_range = 400

        # Creating a list of edges and cost associated with it
        for i in range(total_nodes):
            Graph['edges'].append([])
            Graph['cost'].append([])
            for j in range(total_nodes):
                Graph['cost'][i].append(float('inf'))
      
        for node1 in Graph['all_nodes']:
            for node2 in Graph['all_nodes']:
                
                # Calculating eucledian distance between two nodes.
                (node1_x, node1_y) = Graph['node_coordinates'][node1]
                (node2_x, node2_y) = Graph['node_coordinates'][node2]
                distance = ((node1_x - node2_x) ** 2 + (node1_y - node2_y) ** 2) ** 0.5
                
                if node1 == node2:
                    Graph['cost'][node1][node2] = 0
                    continue
                if distance > Transmission_range:
                    continue
                Graph['cost'][node1][node2] = distance
                Graph['edges'][node1].append(node2)

        try:
            total_data_nodes = int(input("Number of data nodes: "))
        except:
            total_data_nodes = 50
        
        # Randomly generating data nodes
        Graph['data_nodes'] = []
        for i in range(total_data_nodes):
            idx = random.randint(1, total_nodes) % (total_nodes - i)
            for j in range(total_nodes):
                if j not in Graph['data_nodes']:
                    idx -= 1
                if idx == -1:
                    Graph['data_nodes'].append(j)

        try:
            Maximum_data_packets = int(input("Data nodes maximum capacity: "))
        except:
            Maximum_data_packets = 1000

        
        Graph['data'] = []
        for i in range(total_nodes):
            Graph['data'].append(0)

        # Randomly generating data for data nodes        
        for node in Graph['data_nodes']:
            d = random.randint(1, Maximum_data_packets)
            Graph['data'][node] = d  

        try:
            total_energy = int(input("Robot's initial energy: "))
        except:

            total_energy = 1000000
        
        # total budget (in meters)
        total_budget = total_energy * 0.002

        # Checking whether the graph is connected or not
        unvisited_nodes = Graph['all_nodes'].copy()
        unvisited_nodes.remove(0)
        queue = [0]
        while True:
            if len(queue) == 0:
                break
        
            curr_node = queue[0]
            for new_node in Graph['edges'][curr_node]:
                if new_node in unvisited_nodes:
                    queue.append(new_node)
                    unvisited_nodes.remove(new_node)
            queue.remove(curr_node)

        if len(unvisited_nodes) == 0:
            break
        
        print()
        print("The given graph network is not completely connected, please provide a different input.")
        print()    


    # printing data nodes
    print()
    print("Following are the data node and the data stored in the node: ")
    for i in Graph['data_nodes']:
          print("Node =", i,", Data =", Graph['data'][i])     
  
    Greedy1_Algo(Graph, 0, 0, total_budget)
    Greedy2_Algo(Graph, 0, 0, total_budget)
    MARL_Algo(Graph, 0, 0, total_budget)  

if __name__ == "__main__":
  main()