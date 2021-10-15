# we add this above so you can write
# this main agent code into a file for submission later

# for kaggle-environments
from lux.game import Game
# from lux.game_map import Cell
from lux.constants import Constants
from agent_utils import nearest_resource, find_resources, can_move
import random

# we declare this global game_state object so that state persists across turns
# so we do not need to reinitialize it all the time
game_state = None


def agent(observation, configuration):
    global game_state

    if observation["step"] == 0:
        game_state = Game()
        game_state._initialize(observation["updates"])
        game_state._update(observation["updates"][2:])
        game_state.id = observation.player
    else:
        game_state._update(observation["updates"])

    actions = []

    # AI Code
    player = game_state.players[observation.player]
    # opponent = game_state.players[(observation.player + 1) % 2]
    width, height = game_state.map.width, game_state.map.height
    # directions = [Constants.DIRECTIONS.NORTH, Constants.DIRECTIONS.EAST,
    # Constants.DIRECTIONS.SOUTH, Constants.DIRECTIONS.WEST]

    resources = find_resources(game_state.map)
    print(resources)
    unit_action = None

    for unit in player.units:
        if unit.get_cargo_space_left() == 0:
            city = list(player.cities.values())[0]
            tile_pos = city.citytiles[0].pos
            if tile_pos == unit.pos:
                actions.append(unit.transfer(city.id,
                                             Constants.RESOURCE_TYPES.WOOD, 100
                                             ))
            else:
                direction_home = unit.pos.direction_to(tile_pos)
                print('I am broken')
                actions.append(unit.move(direction_home))
        else:
            nearest = nearest_resource(unit.pos,
                                       Constants.RESOURCE_TYPES.WOOD,
                                       resources)
            direct = unit.pos.direction_to(nearest)
            if unit.can_act() and can_move(width, height, unit, direct):
                actions.append(unit.move(direct))

    for city in player.cities:
        for citytile in city.CityTile:
            city_tile_action = None
            if citytile.can_act():
                action = random.randint(0,2)
                if action == 0:
                    city_tile_action = city_tile.research()
                if action == 1:
                    city_tile_action = city_tile.build_worker()
                if action == 2:
                    city_tile_action = city_tile.build_cart()

            actions.append(city_tile_action)

    return actions
