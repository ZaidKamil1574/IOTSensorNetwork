# IOTSensorNetwork

For this project, three different algorithms were used and were mentioned in the supporting documents with various assumptions as suited for the proper implementation of the work.

greedy_1
The first algorithm which is greedy_1, uses a greedy approach to determine the best path between the beginning node s and the target node t within the boundaries of the budget B that is provided. At each step until the target node is reached or the budget is used up, it chooses the unvisited node with the biggest prize that is attainable within the budget.

greedy_2
The second method greedy_2, is similar to greedy_1 but selects nodes in a different way. At each stage, it chooses the unvisited node with the highest prize-to-cost ratio that is feasible given the available funds.

MARL
The third algorithm used combines the learning and execution phases. It is called MARL (Multi-Agent Reinforcement Learning). It updates the Q-values during the learning stage after learning the Q-values for various state-action pairings based on the rewards. The next node is chosen during the execution stage based on the Q-values and the budget, and this process continues until the target node is reached or there are no suitable nodes left to choose.

<img width="852" alt="image" src="https://github.com/user-attachments/assets/9c8a82f8-e8a0-4ebf-b3c6-2e52608802f3" />




<img width="852" alt="image" src="https://github.com/user-attachments/assets/8564d046-51b7-44d6-81c2-d51dc0d415eb" />


![Screenshot 2024-12-23 at 10 01 01 PM](https://github.com/user-attachments/assets/7a88b568-d0b3-41f2-90ba-76b6e591bf52)



