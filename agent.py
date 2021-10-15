# we add this above so you can write
# this main agent code into a file for submission later

# for kaggle-environments
from lux.game import Game
# from lux.game_map import Cell
from lux.constants import Constants
from agent_utils import nearest_resource, find_resources, can_move, nearest_citytile
import random
from sys import stderr

# we declare this global game_state object so that state persists across turns
# so we do not need to reinitialize it all the time
game_state = None
epsilon = 0.05
queued = {}


def agent(observation, configuration):
    global game_state
    global epsilon
    global queued

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
    directions = [Constants.DIRECTIONS.NORTH, Constants.DIRECTIONS.EAST,
                  Constants.DIRECTIONS.SOUTH, Constants.DIRECTIONS.WEST]

    if len(player.cities) == 0:
        return actions

    resources = find_resources(game_state.map)

    map = game_state.map
    turn = observation["step"] % 40
    safe_cargo_left = 0

    if turn > 30:
        safe_cargo_left = 4 * (40 - turn)
    elif turn > 25:
        safe_cargo_left = 40

    built_worker = False

    total_tiles = 0

    for city in player.cities.values():
        total_tiles += len(city.citytiles)

    for city in player.cities.values():
        for citytile in city.citytiles:
            for d in directions:
                cell = map.get_cell_by_pos(citytile.pos.translate(d, 1))
                if cell.resource is None and cell.citytile is None:
                    queued[cell] = -1

            if citytile.can_act():
                if not built_worker and len(player.units) < total_tiles:
                    built_worker = True
                    actions.append(citytile.build_worker())
                else:
                    actions.append(citytile.research())

    unit_n = 0
    for unit in player.units:

        if not unit.can_act():
            continue

        r = random.random()

        if r <= epsilon:
            direct = directions[random.randint(0, 3)]
            actions.append(unit.move(direct))
            continue

        if unit.get_cargo_space_left() > 0:
            nearest = nearest_resource(unit.pos,
                                       Constants.RESOURCE_TYPES.WOOD,
                                       resources)
            direct = unit.pos.direction_to(nearest)

            if unit.can_act() and can_move(width, height, unit, direct):
                actions.append(unit.move(direct))
        else:
            if turn <= 20:
                got_assignment = False
                for cell, assigned in queued.items():
                    if assigned == unit_n:
                        got_assignment = True
                        if cell.pos == unit.pos:
                            actions.append(unit.build_city())
                            queued.pop(cell)
                            break
                        else:
                            actions.append(unit.move(unit.pos.direction_to(cell.pos)))
                            break

                if not got_assignment:
                    for cell, assigned in queued.items():
                        if assigned == -1:
                            print(f"Assigning {cell} to {unit_n}", file=stderr)
                            queued[cell] = unit_n
                            if cell.pos == unit.pos:
                                actions.append(unit.build_city())
                                got_assignment = True
                                break
                            else:
                                actions.append(unit.move(unit.pos.direction_to(cell.pos)))
                                got_assignment = True
                                break

            else:
                tile_pos = nearest_citytile(unit.pos, player.cities)

                if tile_pos is None:
                    continue
                if tile_pos == unit.pos:
                    actions.append(unit.transfer(city.id,
                                                 Constants.RESOURCE_TYPES.WOOD, 100 - safe_cargo_left
                                                 ))
                else:
                    direction_home = unit.pos.direction_to(tile_pos)
                    actions.append(unit.move(direction_home))
        unit_n += 1

    return actions
