def main(app, player):
    from assets import load_asset
    from utils import get_scene_id, clear_alerts
    import scriptable

    item = app.inventory.get_item_slot("Flashlight")[0].item
    clear_alerts(app)

    # manually set charge to zero when triggered by the No Charge scene
    idx = get_scene_id("FlashlightNoCharge", app)
    if idx != -1:
        item.state["charge"] = 0

    if not item.state["is_on"]:
        if item.state["charge"] > 0:
            item.state["is_on"] = True
            app.current_map.light_scale = 0.95
            # visual cue for using light;
            app.current_scenes.append(load_asset("scene", "flashlight_on.scn", app=app))

            # start internal timer for time-out
            app.current_scenes.append(
                scriptable.Scriptable(
                    [
                        "TRANSPARENT TRANSPARENT -n FlashlightTimer",
                        f"pause {item.state['charge']}",
                        "load_scene flashlight_no_charge.scn",
                    ],
                    app,
                    False,
                )
            )
        else:
            # if charge is already gone, continue displaying no charge scene
            app.current_scenes.append(
                scriptable.Scriptable(
                    [
                        "WHITE TRANSPARENT -n ALERT",
                        "print 'I need to find some batteries...' -l 400x400",
                        "pause 60",
                    ],
                    app,
                    False,
                )
            )
    else:
        app.current_map.light_scale = 0.85
        item.state["is_on"] = False

        if item.state["charge"] > 0:
            # remove internal timer and store time left
            idx = get_scene_id("FlashlightTimer", app)
            item.state["charge"] = app.current_scenes[idx].actions.pop(0).data
            app.current_scenes.pop(idx)

    # doesn't matter because flashlight is not one-shot
    return True
