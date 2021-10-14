# we add this above so you can write this main agent code into a file for submission later

# for kaggle-environments
from lux.game import Game
from lux.game_map import Cell, RESOURCE_TYPES
from lux.constants import Constants
from lux.game_constants import GAME_CONSTANTS
from lux import annotate
from agent_utils import *
import copy
import math
import random

# we declare this global game_state object so that state persists across turns so we do not need to reinitialize it all the time
game_state = None

# this is the basic agent definition. At the moment this agent does nothing (and actually will survive for a bit before getting consumed by darkness)
def agent(observation, configuration):
    global game_state

    ### Do not edit ###
    if observation["step"] == 0:
        game_state = Game()
        game_state._initialize(observation["updates"])
        game_state._update(observation["updates"][2:])
        game_state.id = observation.player
    else:
        game_state._update(observation["updates"])
    
    actions = []

    ### AI Code goes down here! ### 
    player = game_state.players[observation.player]
    opponent = game_state.players[(observation.player + 1) % 2]
    width, height = game_state.map.width, game_state.map.height
    D = Constants.DIRECTIONS
    directions = [Constants.DIRECTIONS.NORTH, Constants.DIRECTIONS.EAST, Constants.DIRECTIONS.SOUTH, Constants.DIRECTIONS.WEST]
    
    resources = find_resources(game_state.map)
    
    for unit in player.units:
        nearest = nearest_resource(unit.pos, Constants.RESOURCE_TYPES.WOOD, resources)
        direct = unit.pos.direction_to(nearest) #  directions[random.randint(0,3)]
        if unit.can_act() and can_move(width, height, unit, direct):
            actions.append(player.units[0].move(direct))

    return actions
