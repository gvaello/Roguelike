from logging import exception

from tcod import libtcodpy
import entity

colors = {
    "dark_wall": libtcodpy.Color(0, 0, 100),
    "dark_ground": libtcodpy.Color(50, 50, 150),
    "light_wall": libtcodpy.Color(130, 110, 50),
    "light_ground": libtcodpy.Color(200, 180, 50),
}

def render_all(con,screen_width, screen_height, fov_map, fov_recompute,  game_map=None, entities=None):

    if entities is not None and game_map is not None:
        render_entities(entities, con, fov_map)
        render_game_map(game_map, con, fov_map, fov_recompute)
    else:
        raise "Map and entities cannot be None"

    libtcodpy.console_blit(con, 0,0, screen_width, screen_height, 0, 0, 0)


def render_entities(entities, con, fov_map):
    for entity in entities:
        entity.x = int(entity.x)
        entity.y = int(entity.y)
        if fov_map.fov[entity.y][entity.x]:
            draw_entity(entity, con)


def render_game_map(game_map, con, fov_map, fov_recompute):
    if fov_recompute:
        for y in range(game_map.map_height):
            for x in range(game_map.map_width):
                visible = libtcodpy.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].blocked
                if visible:
                    if wall:
                        libtcodpy.console_set_char_background(con, x, y, colors.get("light_wall"), libtcodpy.BKGND_SET)
                    else:
                        libtcodpy.console_set_char_background(con, x, y, colors.get("light_ground"), libtcodpy.BKGND_SET)
                    game_map.tiles[x][y].explored = True

                    if game_map.tiles[x][y].entity is not None:
                        game_map.tiles[x][y].entity.found = True

                elif game_map.tiles[x][y].explored:
                    if wall:
                        libtcodpy.console_set_char_background(con, x, y, colors.get("dark_wall"), libtcodpy.BKGND_SET)
                    else:
                        libtcodpy.console_set_char_background(con, x, y, colors.get("dark_ground"), libtcodpy.BKGND_SET)

def draw_entity(entity, con):
    libtcodpy.console_set_default_foreground(con, entity.color)
    libtcodpy.console_put_char(con, entity.x, entity.y, entity.char, libtcodpy.BKGND_NONE)

def clear_entities(con, entities):
    for entity in entities:
        clear_entity(con, entity)

def clear_entity(con, entity):
    libtcodpy.console_put_char(con, int(entity.x), int(entity.y), ' ', libtcodpy.BKGND_NONE)
