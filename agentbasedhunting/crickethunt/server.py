from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule

from .agents import MouseAgent, SoundAgent, CricketAgent
from .model import HuntingGrounds

color_dic = {3: "#000000", 2: "#666666", 1: "#999999", 0: "#00A757"}

def MouseAgent_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is HexAgent:
        portrayal["Shape"] = "rect"
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["Color"] = "#009205"
        portrayal["Layer"] = 1

    if type(agent) is MouseAgent:
        portrayal["Shape"] = "crickethunt/resources/mouseoutline.png"
        portrayal["w"] = 2
        portrayal["h"] = 1
        portrayal["Layer"] = 1

    elif type(agent) is CricketAgent:
        if agent.amount != 0:
            portrayal["Color"] = color_dic[agent.amount]
        else:
            portrayal["Color"] = "#ffffff"
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


canvas_element = CanvasGrid(MouseAgent_portrayal, 50, 50, 500, 500)
chart_element = ChartModule([{"Label": "SsAgent", "Color": "#AA0000"}])

server = ModularServer(
    HuntingGrounds, [canvas_element, chart_element], "Hunting Simulation"
)
# server.launch()
