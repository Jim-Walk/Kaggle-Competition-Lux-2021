from lux.game_objects import *
from lux.constants import *
from lux.game_map import *

def can_move(width, height, agent : Unit, direction) -> bool:
    """
    Whether or not the unit can move out of bounds of the map
    """
    # check n
    if direction == "s":
        return agent.pos.y != height - 1    
    
    # check e
    if direction == "e":
        return agent.pos.x != width - 1
    
    # check s
    if direction == "n":
        return agent.pos.y != 0
    
    # check w
    if direction == "w":
        return agent.pos.x != 0
    
    
def find_resources(game_map : GameMap):
    resources = {}
    
    for x in range(game_map.height):
        for y in range(game_map.width):
            cell = game_map.get_cell(x, y)
            if cell.has_resource():
                resources[cell.resource.type] = resources.setdefault(cell.resource.type, []) + [cell]
            
    return resources

def nearest_resource(pos : Position, resource_type : Constants.RESOURCE_TYPES, resources) -> Position:
    specific_resources = resources[resource_type]
    
    nearest = specific_resources[0].pos
    for cell in specific_resources[1:]:
        if pos.distance_to(cell.pos) < pos.distance_to(nearest):
            nearest = cell.pos
    
    return nearest

def deliver_resources():
    pass
                 