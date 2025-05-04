from tcod import libtcodpy

def handle_keys(keys):
    match keys.vk:
        case libtcodpy.KEY_UP:
            return {"move":(0, -1)}
        case libtcodpy.KEY_DOWN:
            return {"move":(0, 1)}
        case libtcodpy.KEY_LEFT:
            return {"move":(-1, 0)}
        case libtcodpy.KEY_RIGHT:
            return {"move":(1, 0)}
        case libtcodpy.KEY_ENTER:
            #Alt + Enter : toggle full screen
            if keys.lalt:
                return {"fullscreen": True}
            else:
                return {"fullscreen": False}
        case libtcodpy.KEY_ESCAPE:
            #exit game
            return {"exit": True}
        case _:
            return {}