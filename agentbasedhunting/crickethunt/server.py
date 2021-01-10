from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule

from .agents import MouseAgent, SoundAgent, CricketAgent, GrassAgent
from .model import HuntingGrounds

def MouseAgent_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is GrassAgent and agent.value == 1:
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["Color"] = "#009205"
        portrayal["Layer"] = 0

    if type(agent) is MouseAgent:
        portrayal["Shape"] = "crickethunt/resources/mouseoutline.png"
        portrayal["scale"]= 1
        portrayal["Layer"] = 0

    elif type(agent) is CricketAgent:
        portrayal["Shape"] = "crickethunt/resources/cricket.png"
        portrayal["Layer"] = 0
        portrayal["scale"]= 2

    return portrayal

canvas_element = CanvasGrid(MouseAgent_portrayal, 85, 115, 500, 500)

#chart_element = ChartModule([{"Label": "SsAgent", "Color": "#AA0000"}])

#server = ModularServer(
#    HuntingGrounds, [canvas_element, chart_element], "Hunting Simulation"
#)

server = ModularServer(
    HuntingGrounds, [canvas_element], "Hunting Simulation"
)
# server.launch()
