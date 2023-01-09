
import numpy as np
from mesa.visualization.ModularVisualization import VisualizationElement, CHART_JS_FILE
import mesa
from mai import ARModel


class HistogramModule(VisualizationElement): 
    package_includes = [CHART_JS_FILE] 
    local_includes = ["HistogramModule.js"]
    def __init__(self, bins, canvas_height, canvas_width): 
        self.canvas_height = canvas_height 
        self.canvas_width = canvas_width
        self.bins = bins
        new_element = "new HistogramModule({}, {}, {})" 
        new_element = new_element.format(bins,
                                         canvas_width,
                                         canvas_height)
        self.js_code = "elements.push(" + new_element + ");"
    
    def render(self, model):

        agent_resistance = []
        for agent in model.schedule.agents:
            if agent.type == 'bacteria':
                agent_resistance.append(agent.resistance)        
        hist = np.histogram(agent_resistance, bins=self.bins)[0]
        return [int(x) for x in hist]


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.5}

    if agent.type == "bacteria":
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    else:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2
    return portrayal

grid = mesa.visualization.CanvasGrid(agent_portrayal, 10, 10, 500, 500)
chart = mesa.visualization.ChartModule([{"Label": "Resistance",
                      "Color": "Black"}],
                    data_collector_name='datacollector')
chart2 = mesa.visualization.ChartModule([{"Label": "Count",
                      "Color": "Black"}],
                    data_collector_name='datacollector_bacteria')
histogram = HistogramModule(list(range(10)), 200, 500)
server = mesa.visualization.ModularServer(ARModel,
                       [grid, chart, chart2],
                       "Resistance Model",
                       {"bacteria_number":5, "food_number":55,  "antibiotic_number":20, "power_of_antibiotic": 0.01, "width":10, "height":10})
server.launch()