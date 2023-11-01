def main(app, player):
    from utils import clear_alerts
    from assets import load_asset

    flashlight = app.inventory.get_item_slot("Flashlight")[0]

    if flashlight is None:
        clear_alerts(app)
        load_asset("script", "default.py", app=app, player=player)
        return False
    else:
        if flashlight.item.state["charge"] > 0:
            clear_alerts(app)
            app.current_scenes.append(
                load_asset("scene", "battery_no_use.scn", app=app)
            )
            return False
        else:
            flashlight.item.state["charge"] = flashlight.item.state["max_charge"]
            clear_alerts(app)
            app.current_scenes.append(load_asset("scene", "battery_use.scn", app=app))
            return True
