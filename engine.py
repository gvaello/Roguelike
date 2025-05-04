import sys
import os
from random import randint

from tcod import libtcodpy

from entity import Entity
from fov_functions import initialize_fov, recompute_fov
from game_map.game_map import GameMap
from input_handlers import handle_keys
from map_objects.dungeon import Dungeon
from render_functions import render_all, clear_entities

os.environ['path'] = os.path.dirname(sys.executable) + ";" + os.environ['path']

DATA_FOLDER = "resources"
IMAGES_FOLDER = os.path.join(DATA_FOLDER, "images")
FONT_FILE = os.path.join(IMAGES_FOLDER, "main_tileset.png")


def main():
    screen_width = 80
    screen_height = 60
    map_height = 50
    map_width = 70

    fov_algortithm = libtcodpy.FOV_RESTRICTIVE
    fov_light_walls = True
    fov_radius = 10
    fov_recompute = True

    dungeon_config = Dungeon(30, 10, 10, 6)

    game_map = GameMap(map_width, map_height)

    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    libtcodpy.console_set_custom_font(FONT_FILE, libtcodpy.FONT_TYPE_GREYSCALE | libtcodpy.FONT_LAYOUT_TCOD)

    libtcodpy.console_init_root(screen_width, screen_height, "debug", False)
    blit_console = libtcodpy.console_new(screen_width, screen_height)

    key = libtcodpy.Key()
    mouse = libtcodpy.Mouse()
    player = Entity(player_x, player_y, '@', libtcodpy.white)

    game_map.make_map(dungeon_config, player)
    npc = Entity(player.x - 1, player.y - 1, 'A', libtcodpy.yellow)
    game_map.tiles[int(npc.x)][int(npc.y)].entity = npc

    fov_map = initialize_fov(game_map)

    while not libtcodpy.console_is_window_closed():

        if fov_recompute:
            x = int(player.x)
            y = int(player.y)
            recompute_fov(fov_map, x, y, fov_radius, fov_light_walls, fov_algortithm)

        libtcodpy.sys_check_for_event(libtcodpy.EVENT_KEY_PRESS, key, mouse)

        #region HOW WE USED TO CREATE ENTITIES
        #libtcodpy.console_set_default_foreground(blit_console, libtcodpy.white)
        #libtcodpy.console_put_char(blit_console, player_x, player_y , '@', libtcodpy.BKGND_NONE)
        #libtcodpy.console_blit(blit_console, 0, 0, screen_width, screen_height, 0,0,0)
        #endregion

        render_all(blit_console, screen_width, screen_height, fov_map, fov_recompute, game_map= game_map, entities=[player, npc])
        libtcodpy.console_flush()

        #clean the player pos and put a whitespace on it
        clear_entities(blit_console, [player,npc])

        action = handle_keys(key)

        move_cmd = action.get("move")
        exit_cmd = action.get("exit")
        fullscreen_cmd = action.get("fullscreen")

        if move_cmd:
            dx, dy = move_cmd
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                fov_recompute = True
                player.move(dx, dy)

        if exit_cmd:
            return True
        if fullscreen_cmd:
            libtcodpy.console_set_fullscreen(not libtcodpy.console_is_fullscreen())
    return None


if __name__ == '__main__':
    main()