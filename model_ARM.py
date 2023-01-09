from mai import ARModel
import matplotlib.pyplot as plt
import math
import statistics

empty_model = ARModel(90,food_number=55,antibiotic_number=20,power_of_antibiotic=1,width=20,height=20)

for i in range(15):
    empty_model.step()
    print(empty_model.num_agents)

import numpy as np

agent_counts = np.zeros((empty_model.grid.width, empty_model.grid.height))
for cell in empty_model.grid.coord_iter():
    cell_content, x, y = cell
    print(cell_content)
    ave_res = []
    for content in cell_content:
        if content.type == 'bacteria':
            ave_res.append(content.resistance)
    
    if len(ave_res) == 0:
        agent_count = 0
    else:    
        agent_count = statistics.mean(ave_res)
    agent_counts[x][y] = agent_count


resistance_graph = empty_model.datacollector.get_model_vars_dataframe()
resistance_graph.plot()
plt.show()

input()


plt.imshow(agent_counts, interpolation="nearest")
plt.colorbar()

# If running from a text editor or IDE, remember you'll need the following:
plt.show()