from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import CanvasGrid, ChartModule

from .agents import MouseAgent, SoundAgent, CricketAgent, GrassAgent
from .model import HuntingGrounds

def MouseAgent_portrayal(agent):
    assert agent is not None
    portrayal={}

    if type(agent) is GrassAgent and agent.value == 1:
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["Color"] = "#A7D670"
        portrayal["Layer"] = 0

    if type(agent) is MouseAgent:
        #portrayal["Shape"] = "crickethunt/resources/mouseoutline.png"
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        #portrayal["scale"]= 4
        portrayal["h"]=1
        portrayal["w"]=1
        portrayal["Color"] = "#000000"
        portrayal["Layer"] = 1

        portrayal["x"]= agent.pos[0]
        portrayal["y"]= agent.pos[1]

    elif type(agent) is CricketAgent:
        #portrayal["Shape"] = "crickethunt/resources/cricket.png"
        portrayal["Layer"] = 1
        #portrayal["scale"]= 1
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["h"]=2
        portrayal["w"]=2
        if agent.chirp==1:
            portrayal["Color"] = "#ff0000"
        else:
            portrayal["Color"] = "#00A757"

    return portrayal

canvas_element = CanvasGrid(MouseAgent_portrayal, 85, 115, 500, 500)

model_params = {
    "mouse_dwell_probability": UserSettableParameter(
        "slider", "Mouse Dwell Probability", 0, 0.1, 1
    )
}

#chart_element = ChartModule([{"Label": "SsAgent", "Color": "#AA0000"}])

server = ModularServer(
    HuntingGrounds, [canvas_element], "Hunting Simulation"
)
# server.launch()
