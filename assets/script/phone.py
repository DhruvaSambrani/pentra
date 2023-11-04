def main(app, player, source):
    from assets import load_asset

    maxx, maxy = app.current_map.map_surf.get_size()
    x, y = player.rect.center
    threshold = 40
    if (
        (x < threshold)
        or (x > maxx - threshold)
        or (y < threshold)
        or (y > maxy - threshold)
    ):
        app.current_scenes.append(load_asset("scene", "no_mess.scn", app=app))
    else:
        app.current_scenes.append(load_asset("scene", "no_conn.scn", app=app))

    return False
