def get_total_city_tiles(player) -> int:
    num_tiles = 0
    for city in player.cities:
        for city_tile in player.cities[city].citytiles:
            num_tiles += 1

    return num_tiles
