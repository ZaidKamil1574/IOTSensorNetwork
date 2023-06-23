# IOTSensorNetwork

For this project,  three different algorithms were used and were mentioned in the supporting documents with various assumptions as suited for the proper implementation of the work.

greedy_1
The first algorithm put into place is called greedy_1, and it uses a greedy approach to determine the best path between the beginning node s and the target node t within the boundaries of the budget B that is provided. At each step until the target node is reached or the budget is used up, it chooses the unvisited node with the biggest prize that is attainable within the budget.

greedy_2
The second method used, greedy_2, is similar to greedy_1 but selects nodes in a different way. At each stage, it chooses the unvisited node with the highest prize-to-cost ratio that is feasible given the available funds.

MARL
The third algorithm used combines the learning and execution phases. It is called MARL (Multi-Agent Reinforcement Learning). It updates the Q-values during the learning stage after learning the Q-values for various state-action pairings based on the rewards. The next node is chosen during the execution stage based on the Q-values and the budget, and this process continues until the target node is reached or there are no suitable nodes left to choose.
