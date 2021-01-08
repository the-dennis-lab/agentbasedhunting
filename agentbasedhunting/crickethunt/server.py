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
        portrayal["scale"]=1.5
        portrayal["Layer"] = 1

    elif type(agent) is CricketAgent:
        portrayal["Shape"] = "crickethunt/resources/cricket.png"
        portrayal["Layer"] = 0
        portrayal["scale"]=3

    return portrayal

#portrayal, gridwidth, gridheight, pageusewidth, pageuseheight
canvas_element = CanvasGrid(MouseAgent_portrayal, 115, 85, 575, 425)
#chart_element = ChartModule([{"Label": "SsAgent", "Color": "#AA0000"}])

#server = ModularServer(
#    HuntingGrounds, [canvas_element, chart_element], "Hunting Simulation"
#)

server = ModularServer(
    HuntingGrounds, [canvas_element], "Hunting Simulation"
)
# server.launch()
